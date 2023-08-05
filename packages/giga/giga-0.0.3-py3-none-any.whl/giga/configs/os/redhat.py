import giga
import logging
from giga import configs
from giga import ensure

log = logging.getLogger(__name__)

def name(pkg):
  return pkg if isinstance(pkg, str) else pkg[0]

def source(pkg):
  return pkg if isinstance(pkg, str) else pkg[1]

class Manager:

  def __init__(self, system):
    super().__init__()
    self.system = system

  @property
  def installed_packages(self):
    argv = "rpm -qa --queryformat '%{NAME}|%{VERSION}&'"
    packages = self.system.stdout(argv)[:-1]
    return dict(pkg.split('|') for pkg in packages.split('&'))

  @property
  def yum(self):
    return 'dnf' if self.system.which('dnf') else 'yum'

  def missing(self, packages):
    return [pkg for pkg in packages if name(pkg) not in self.installed_packages]

  def present(self, packages):
    return [pkg for pkg in packages if name(pkg) in self.installed_packages]

  def install(self, packages):
    if packages:
      packages = ' '.join(source(pkg) for pkg in packages)
      self.system(f'{self.yum} -y install {packages}')

  def remove(self, packages):
    if packages:
      packages = ' '.join(name(pkg) for pkg in packages)
      self.system(f'{self.yum} -y remove {packages}')

class Ensurers(giga.Ensurers):

  class Packages(giga.Ensurer):

    def present(self, packages):
      mgr = Manager(self.system)
      missing = mgr.missing(packages)
      mgr.install(missing)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in missing:
            +self.task

    def absent(self, packages):
      mgr = Manager(self.system)
      present = mgr.present(packages)
      mgr.remove(present)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in present:
            +self.task

    def status(self, packages):
      return not Packages(self.system).missing(packages)

giga.ensure.os.add_ensurers('redhat', Ensurers)

class Packages(giga.Config):

  packages = None
  keep = True

  def on_apply(self):
    with giga.Task(f'Apply {len(self.packages)} yum package(s)') as task:
      giga.ensure.os.redhat.packages.present(self.packages)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.packages)} yum package(s)') as task:
      if not self.keep:
        packages = reversed(self.packages)
        giga.ensure.os.redhat.packages.absent(self.packages)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.os.redhat.packages.status(self.packages)
    )

class Epel(Packages):
  'Apply epel.'

  version = None

  def on_init(self):
    super().on_init()
    self.packages = [
      ('epel-release', f'https://dl.fedoraproject.org/pub/epel/epel-release-latest-{self.version}.noarch.rpm'),
    ]

class Ius(Packages):
  'Apply ius.'

  version = None

  def on_init(self):
    super().on_init()
    self.packages = [
      ('ius-release', f'https://repo.ius.io/ius-release-el{self.version}.rpm'),
    ]

class RcLocal755(giga.Config):
  'Make /etc/rc.d/rc.local executable.'

  keep = True

  def on_apply(self):
    super().on_apply()
    with giga.Task('Apply rc.local executable bit') as task:
      giga.ensure.fs.modes.present([('/etc/rc.d/rc.local', 0o755)])

  def on_delete(self):
    super().on_delete()
    with giga.Task('Delete rc.local executable bit') as task:
      if not self.keep:
        giga.ensure.fs.modes.present([('/etc/rc.d/rc.local', 0o644)])

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.modes.status([('/etc/rc.d/rc.local', 0o755)])
    )

giga.utils.set_config_logger(__name__, log)
