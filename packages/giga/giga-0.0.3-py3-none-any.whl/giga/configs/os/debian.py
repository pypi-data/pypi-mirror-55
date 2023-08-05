import giga
import logging
from giga import ensure

log = logging.getLogger(__name__)

class Manager:

  env = {'DEBIAN_FRONTEND': 'noninteractive'}

  def __init__(self, system):
    super().__init__()
    self.system = system

  @property
  def installed_packages(self):
    argv = "dpkg-query -W -f='${binary:Package}|${Version}&'"
    packages = self.system.stdout(argv)[:-1]
    return {
      name.split(':')[0]: version
      for (name, version) in (pkg.split('|') for pkg in packages.split('&'))
    }

  def missing(self, packages):
    return [pkg for pkg in packages if pkg not in self.installed_packages]

  def present(self, packages):
    return [pkg for pkg in packages if pkg in self.installed_packages]

  def update(self):
    self.system('apt-get update', env=self.env)

  def install(self, packages):
    if packages:
      packages = ' '.join(packages)
      self.system(f'apt-get install -y {packages}', env=self.env)

  def remove(self, packages):
    if packages:
      packages = ' '.join(packages)
      self.system(f'apt-get remove -y --purge {packages}', env=self.env)

class Ensurers(giga.Ensurers):

  class Packages(giga.Ensurer):

    def present(self, packages):
      mgr = Manager(self.system)
      missing = mgr.missing(packages)
      with self.item('[update]'):
        if missing:
          mgr.update()
          +self.task
      mgr.install(missing)
      for pkg in packages:
        with self.item(pkg):
          if pkg in missing:
            +self.task

    def absent(self, packages):
      mgr = Manager(self.system)
      present = mgr.present(packages)
      mgr.remove(present)
      for pkg in packages:
        with self.item(pkg):
          if pkg in present:
            +self.task

    def status(self, packages):
      return not Manager(self.system).missing(packages)

giga.ensure.os.add_ensurers('debian', Ensurers)

class Packages(giga.Config):

  packages = None
  keep = True

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.packages)} apt package(s)') as task:
      giga.ensure.os.debian.packages.present(self.packages)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.packages)} apt package(s)') as task:
      if not self.keep:
        packages = reversed(self.packages)
        giga.ensure.os.debian.packages.absent(packages)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.os.debian.packages.status(self.packages)
    )

class RcLocal755(giga.Config):
  '''
  Create /etc/rc.local if it doesn't exist and make it executable.
  '''

  keep = True

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with giga.Task('Apply rc.local executable bit') as task:
      path = '/etc/rc.local'
      giga.ensure.fs.contains.present([(path, '#!/bin/bash\n')])
      giga.ensure.fs.modes.present([(path, 0o755)])

  def on_delete(self):
    super().on_delete()
    sys = self.system
    with giga.Task('Delete rc.local executable bit') as task:
      if not self.keep:
        giga.ensure.fs.modes.present([('/etc/rc.local', 0o644)])

  def on_is_applied(self):
    sys = self.system
    path = '/etc/rc.local'
    return (
      super().on_is_applied() and
      sys.isfile(path) and
      sys.ismode(path, 0o755)
    )

giga.utils.set_config_logger(__name__, log)
