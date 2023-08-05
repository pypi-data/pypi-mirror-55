import giga
import logging
from giga import configs
from lura.run import run

log = logging.getLogger(__name__)

def image_present(sys, tag):
  argv = "docker images %s --format '{{json . }}'" % tag
  return sys(argv).stdout.rstrip() != ''

def verbose(config):
  verbose = config.config_verbose
  if config.coordinator:
    verbose = config.coordinator.verbose
  return verbose

class Ensurers(giga.Ensurers):

  class Builds(giga.Ensurer):

    def present(self, images):
      config = self.config
      for path, local in images:
        with self.item(local):
          if verbose(config):
            with run.log(config.config_logger, config.config_log_level):
              self.system(f'docker build . -t {local}', cwd=path)
          else:
            self.system(f'docker build . -t {local}', cwd=path)
          +self.task

    def status(self, images):
      return all(image_present(self.system, local) for (_, local, _) in images)

  class Pushes(giga.Ensurer):

    def present(self, images):
      config = self.config
      sys = self.system
      for local, remote in images:
        with self.item(remote):
          if verbose(config):
            with run.log(config.config_logger, config.config_log_level):
              sys(f'docker tag {local} {remote}')
              sys(f'docker push {remote}')
          else:
            sys(f'docker tag {local} {remote}')
            sys(f'docker push {remote}')
          self.task + 2

    def status(self, images):
      sys = self.system
      return all(image_present(sys, remote) for (_, _, remote) in images)

giga.ensure.add_ensurers('docker', Ensurers)

class Builds(giga.Config):

  images = None

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.images)} image builds'):
      giga.ensure.docker.builds.present(self.images)

  def on_is_applied(self):
    return (
      super().on_is_appled() and
      giga.ensure.docker.builds.status(self.images)
    )

class Pushes(giga.Config):

  images = None

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.images)} image pushes'):
      giga.ensure.docker.pushes.present(self.images)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.docker.pushes.status(self.images)
    )

class Debian(configs.os.debian.Packages):

  packages = ['docker.io']

class RedHat(configs.os.redhat.Packages):
  'Install Docker on a RedHat system.'

  pass # FIXME

class Docker(giga.Config):

  def config_include(self):
    family = self.system.os.family
    if family == 'debian':
      return Debian,
    elif family == 'redhat':
      return RedHat,
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
