import giga
import logging
from giga import configs
from lura import net
from lura.hash import hashs
from lura.time import poll
from shlex import quote

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Charts(giga.Ensurer):

    def present(self, charts):
      sys = self.system
      for chart, name, values in charts:
        with self.item(f'{chart} {name}'):
          if sys.nonzero(f'helm status {name}'):
            argv = [f'helm install {chart} --name {name}']
            if values:
              for opt, val in values.items():
                argv.append(f'--set {quote(opt)}={quote(str(val))}')
            argv = ' '.join(argv)
            sys(argv)
            +self.task

    def absent(self, charts, purge=True):
      sys = self.system
      for chart, name, _ in charts:
        with self.item(f'{chart} {name}'):
          if sys.zero(f'helm status {name}'):
            if purge:
              sys(f'helm delete --purge {name}')
            else:
              sys(f'helm delete {name}')
            +self.task

    def status(self, charts):
      return all(
        self.system.zero(f'helm status {name}')
        for (_, name, _) in charts
      )

giga.ensure.add_ensurers('helm', Ensurers)

class Helm(giga.Config):
  'Apply Helm binaries to a system.'

  version = '2.14.3'
  bin_dir = '/usr/local/bin'
  keep = False

  _bins = ['linux-amd64/helm', 'linux-amd64/tiller']

  def on_init(self):
    super().on_init()
    self.url = 'https://get.helm.sh/helm-v%s-linux-amd64.tar.gz' % self.version

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with giga.Task(f'Apply {len(self._bins)} helm bins') as task:
      with self.system.tempdir() as temp_dir:
        tar = f'{temp_dir}/helm.tgz'
        for bin in self._bins:
          path = f'{self.bin_dir}/{bin.split("/")[-1]}'
          with task.item(path):
            if not sys.isfile(path):
              if not sys.exists(tar):
                alg = 'sha256'
                sum = net.wgets(f'{self.url}.{alg}').rstrip().split()[0]
                sys.wget(self.url, tar, alg, sum)
              sys(f'tar xf {tar} -C {self.bin_dir} --strip=1 {bin}')
              +task
          giga.ensure.fs.modes.present([(path, 0o755)])
          giga.ensure.fs.chowns.present([(path, 'root', 'root')])

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self._bins)} helm bins') as task:
      if not self.keep:
        bins = (f'{self.bin_dir}/{bin.split("/")[-1]}' for bin in self._bins)
        giga.ensure.fs.files.absent(bins)

  def on_is_applied(self):
    bins = tuple(f'{self.bin_dir}/{bin.split("/")[-1]}' for bin in self._bins)
    return (
      super().on_is_applied() and
      giga.ensure.fs.files.status(bins) and
      giga.ensure.fs.modes.status((bin, 0o755) for bin in bins)
    )

class Tiller(configs.kube.Resource):
  'Apply Tiller to a cluster.'

  history_max = 200
  force_delete = False
  keep = False

  _poll_interval = 0.2

  def get_pods(self):
    return tuple(
      pod for pod in self.get('pod', namespace='kube-system').get('items', [])
      if pod.metadata.name.startswith('tiller-deploy-')
    )

  def on_apply(self):
    super().on_apply()
    with giga.Task('Apply tiller') as task:
      sys = self.system
      with task.item('helm init'):
        if not self.get_pods():
          sys(f'helm init --history-max {self.history_max}')
          +task
    self.wait_for_deploy_create('tiller-deploy', 'kube-system')
    self.wait_for_pods_ready(self.get_pods)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with giga.Task('Apply helm reset') as task:
      with task.item('helm reset'):
        if not self.keep:
          if self.get_pods():
            if self.force_delete:
              sys('helm reset --force')
            else:
              sys('helm reset')
            +task

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      bool(self.get_pods()) # FIXME
    )

class Charts(configs.kube.Resource):

  charts = None
  purge = True
  keep = False

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with giga.Task(f'Apply {len(self.charts)} helm chart(s)') as task:
      giga.ensure.helm.charts.present(self.charts)

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with giga.Task(f'Delete {len(self.charts)} helm chart(s)') as task:
      if not self.keep:
        giga.ensure.helm.charts.absent(self.charts, self.purge)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.helm.charts.status(self.charts)
    )

class DockerRegistry(Charts):

  persistence = True
  node_port = 32000

  @property
  def charts(self):
    return [
      (
        'stable/docker-registry',
        'docker-registry',
        {
          'persistence.enabled': 'true' if self.persistence else 'false',
          'service.type': 'NodePort',
          'service.nodePort': self.node_port,
        })]

  def get_pods(self):
    return tuple(
      pod for pod in self.get('pod', namespace='default').get('items', [])
      if pod.metadata.name.startswith('docker-registry-')
    )

  def on_apply(self):
    super().on_apply()
    self.wait_for_deploy_create('docker-registry', namespace='default')
    self.wait_for_pods_ready(self.get_pods)

giga.utils.set_config_logger(__name__, log)
