import giga
import logging
from giga import configs

log = logging.getLogger(__name__)

class Debian(configs.os.debian.Packages):

  packages = ['docker.io']

class RedHat(configs.os.redhat.Packages):
  'Install Docker on a RedHat system.'

  pass # FIXME

class Docker(giga.Config):

  def config_include(self):
    family = self.system.os.family
    if family == 'debian':
      return [Debian]
    elif family == 'redhat':
      return [RedHat]
    else:
      raise giga.error.NotImplementedFor(family)

class DockerCompose(configs.wget.Bins):
  'Install docker-compose on a system.'

  version = '1.24.1'
  bin_dir = '/usr/local/bin'

  def on_init(self):
    super().on_init()
    url = f'https://github.com/docker/compose/releases/download/{self.version}/docker-compose-Linux-x86_64'
    self.paths = [(f'{self.bin_dir}/docker-compose', url, 'sha256', f'{url}.sha256')]

giga.utils.set_config_logger(__name__, log)
