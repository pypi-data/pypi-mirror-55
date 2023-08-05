import giga
import logging
import os
from giga import configs
from lura import net
from lura.time import poll
from shlex import quote
from time import sleep

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Addons(giga.Ensurer):

    @property
    def _statuses(self):
      sys = self.system
      if sys.which('minikube'):
        return dict(
          line.rstrip()[2:].split(': ', 1)
          for line in sys.stdout('minikube addons list').rstrip().split('\n')
        )
      return {}

    def present(self, addons):
      sys = self.system
      statuses = self._statuses
      for addon in addons:
        with self.item(addon):
          if statuses[addon] == 'disabled':
            sys(f'minikube addons enable {addon}')
            +self.task

    def absent(self, addons):
      sys = self.system
      statuses = self._statuses
      for addon in addons:
        with self.item(addon):
          if statuses[addon] == 'enabled':
            sys(f'minikube addons disable {addon}')
            +self.task

    def status(self, addons):
      statuses = self._statuses
      return all(statuses[addon] == 'enabled' for addon in addons)

giga.ensure.add_ensurers('minikube', Ensurers)

class Debian(configs.os.debian.Packages):
  'Apply Debian packages needed to run Minikube with vm driver `none`.'

  packages = ['socat']

class RedHat(configs.os.redhat.Packages):
  'Apply Red Hat packages needed to run Minikube with vm driver `none`.'

  pass # FIXME

class Packages(giga.Config):

  def config_include(self):
    family = self.system.os.family
    if family == 'debian':
      return Debian,
    elif family == 'redhat':
      return RedHat,
    else:
      raise giga.NotImplementedFor(family)

class Binary(configs.wget.Bins):
  'Apply the minikube binary to a system.'

  def on_init(self):
    super().on_init()
    settings = self.settings
    url = 'https://storage.googleapis.com/minikube/releases/%s/minikube-linux-amd64' % settings.minikube_version
    self.paths = [(f'{settings.bin_dir}/minikube', url, 'sha256', f'{url}.sha256')]

class Addons(giga.Config):

  settings = None

  def on_apply(self):
    super().on_apply()
    enable = self.settings.addons_enable or ()
    disable = self.settings.addons_disable or ()
    with giga.Task(f'Apply {len(enable)} addons'):
      giga.ensure.minikube.addons.present(enable)
    with giga.Task(f'Delete {len(disable)} addons'):
      giga.ensure.minikube.addons.absent(disable)

  def on_is_applied(self):
    enable = self.settings.addons_enable or ()
    disable = self.settings.addons_disable or ()
    return (
      super().on_is_applied() and
      giga.ensure.minikube.addons.status(enable) and
      (not giga.ensure.minikube.addons.status(disable)) if disable else True
    )

class Cluster(giga.Config):
  'Apply a minikube cluster to a system.'

  settings = None

  def on_apply(self):
    super().on_apply()
    sys = self.system
    settings = self.settings
    with giga.Task('Apply minikube cluster') as task:
      if sys.nonzero('minikube status'):
        sys('minikube start --kubernetes-version=v%s --vm-driver=%s' % (
          settings.kube_version, settings.vm_driver))
        sys('kubectl cluster-info')
        +task

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with giga.Task(f'Delete cluster') as task:
      if sys.zero('minikube status'):
        sys('minikube delete')
        +task

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      self.system.zero('minikube status')
    )

class Minikube(giga.Config):

  kube_version = '1.15.4'
  vm_driver = 'none'
  minikube_version = 'latest'
  addons_enable = None
  addons_disable = None
  bin_dir = '/usr/local/bin'

  def config_include(self):
    return [
      configs.docker.Docker,
      Packages,
      Binary(settings=self),
      Addons(settings=self),
      Cluster(settings=self),
    ]

giga.utils.set_config_logger(__name__, log)
