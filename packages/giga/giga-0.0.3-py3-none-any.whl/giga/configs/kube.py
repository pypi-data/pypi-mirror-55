import giga
import logging
from giga import configs
from lura.attrs import attr
from lura.formats import json
from lura.time import poll

log = logging.getLogger(__name__)

class Kubectl(configs.wget.Bins):

  version = '1.15.4'
  bin_dir = '/usr/local/bin'

  def on_init(self):
    super().on_init()
    url = 'https://storage.googleapis.com/kubernetes-release/release/v%s/bin/linux/amd64/kubectl' % self.version
    self.paths = [(f'{self.bin_dir}/kubectl', url, 'sha256', f'{url}.sha256')]

class Kc(giga.Config):

  bin_dir = '/usr/local/bin'
  keep = False

  kc = '#!/bin/sh\nexec kubectl "$@"\n'

  @property
  def path(self):
    return f'{self.bin_dir}/kc'

  @property
  def contents(self):
    return (self.path, self.kc),

  @property
  def modes(self):
    return (self.path, 0o755),

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {self.path}') as task:
      giga.ensure.fs.contents.present(self.contents)
      giga.ensure.fs.modes.present(self.modes)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {self.path}') as task:
      if not self.keep:
        giga.ensure.fs.files.absent([self.path])

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.contents.status(self.contents) and
      giga.ensure.fs.modes.status(self.modes)
    )

class Resource(giga.Config):

  poll_interval = 0.3
  deploy_create_timeout = 300
  pods_ready_timeout = 300
  config_logger = log

  def get(self, type, name=None, namespace=None):
    'Return a parsed call to kubectl get --output=json.'

    argv = [f'kubectl get {type}']
    if name:
      argv.append(name)
    if namespace == '*':
      argv.append('--all-namespaces')
    elif namespace:
      argv.append(f'--namespace={namespace}')
    argv.append('--output=json')
    argv = ' '.join(argv)
    res = self.system(argv, enforce=False)
    if res.code != 0:
      return attr()
    return json.loads(res.stdout)

  def is_deploy_created(self, deploy, namespace):
    deploys = self.get('deploy', namespace=namespace).get('items', [])
    return any(_.metadata.name.startswith(deploy) for _ in deploys)

  def wait_for_deploy_create(self, deploy, namespace):
    with giga.Task('Wait for deploy create') as task:
      test = lambda: self.is_deploy_created(deploy, namespace)
      timeout = self.deploy_create_timeout
      if not poll(test, timeout=timeout, pause=self.poll_interval):
        raise TimeoutError(f'Timed out waiting for deploy: {deploy}')

  def wait_for_pods_ready(self, getter):
    with giga.Task(f'Wait for pods ready') as task:
      def test():
        return all(
          all(
            status.ready for status in pod.status.containerStatuses
          ) if 'containerStatuses' in pod.status else False for pod in getter()
        )
      timeout = self.pods_ready_timeout
      if not poll(test, timeout=timeout, pause=self.poll_interval):
        raise TimeoutError(f'Timed out waiting for pods')

giga.utils.set_config_logger(__name__, log)
