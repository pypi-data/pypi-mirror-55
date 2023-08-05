import giga
import logging
from giga import ensure
from lura.formats import json
from lura.threads import synchronize
from shlex import quote

log = logging.getLogger(__name__)

def name(pkg):
  return pkg if isinstance(pkg, str) else pkg[0]

def source(pkg):
  return pkg if isinstance(pkg, str) else pkg[1]

class Python:

  pys = {
    2: ('python2', 'python2.7'),
    3: ('python3', 'python3.8', 'python3.7', 'python3.6'),
  }

  def __init__(self, system, py=3, python=None):
    super().__init__()
    self.system = system
    self.python = python
    if python is None:
      self.python = system.which(self.pys[py], error=True)

  def run(self, argv, *args, **kwargs):
    return self.system.run(f'{self.python} {argv}', *args, **kwargs)

  __call__ = run

  @property
  def installed_packages(self):
    try:
      packages = json.loads(self('-m pip list --format json').stdout)
      return dict((pkg.name, pkg.get('version')) for pkg in packages)
    except giga.RunError:
      # was this error raised because pip is not installed?
      if self('-m pip --help', enforce=False).code == 0:
        # pip is installed, so something went wrong
        raise
    # pip is not installed
    raise FileNotFoundError(f'pip is not installed for {self.python}')

  def missing(self, packages):
    return [pkg for pkg in packages if name(pkg) not in self.installed_packages]

  def present(self, packages):
    return [pkg for pkg in packages if name(pkg) in self.installed_packages]

  def install(self, packages):
    if packages:
      packages = ' '.join(quote(source(pkg)) for pkg in packages)
      self(f'-m pip install {packages}')

  def remove(self, packages):
    if packages:
      packages = ' '.join(quote(name(pkg)) for pkg in packages)
      self.system.run(f'yes|{self.python} -m pip uninstall {packages}')

  def install_editable(self, packages):
    if packages:
      for _, path in packages:
        self(f'-m pip install -e {quote(path)}')

  def remove_editable(self, packages):
    if packages:
      for _, path in packages:
        self('setup.py develop -u', cwd=path)

class Ensurers(giga.Ensurers):

  class Packages(giga.Ensurer):

    def present(self, packages, py=3, python=None):
      python = Python(self.system, py, python)
      missing = python.missing(packages)
      python.install(missing)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in missing:
            +self.task

    def absent(self, packages, py=3, python=None):
      python = Python(self.system, py, python)
      present = python.present(packages)
      python.remove(present)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in present:
            +self.task

    def status(self, packages, py=3, python=None):
      try:
        return not Python(self.system, py, python).missing(packages)
      except FileNotFoundError: # python binary is missing
        return False

  class Editables(giga.Ensurer):

    def present(self, packages, py=3, python=None):
      python = Python(self.system, py, python)
      missing = python.missing(packages)
      python.install_editable(missing)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in missing:
            +self.task

    def absent(self, packages, py=3, python=None):
      python = Python(self.system, py, python)
      present = python.present(packages)
      python.remove_editable(present)
      for pkg in packages:
        with self.item(name(pkg)):
          if pkg in present:
            +self.task

    def status(self, packages, py=3, python=None):
      try:
        return not Python(self.system, py, python).missing(packages)
      except FileNotFoundError: # python binary is missing
        return False

giga.ensure.add_ensurers('python', Ensurers)

class Packages(giga.Config):

  packages = None
  py = 3
  python = None
  keep = True

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.packages)} python package(s)') as task:
      giga.ensure.python.packages.present(self.packages, self.py, self.python)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.packages)} python package(s)') as task:
      if not self.keep:
        packages = list(reversed(self.packages))
        giga.ensure.python.packages.absent(packages, self.py, self.python)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.python.packages.status(self.packages, self.py, self.python)
    )

class Editables(giga.Config):

  packages = None
  py = 3
  python = None
  keep = False
  synchronize = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.packages)} editable packages') as task:
      packages = self.packages
      if self.coordinator and self.synchronize:
        with synchronize(self.coordinator):
          giga.ensure.python.editables.present(packages, self.py, self.python)
      else:
        giga.ensure.python.editables.present(packages, self.py, self.python)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.packages)} editable packages') as task:
      if not self.keep:
        packages = list(reversed(self.packages))
        if self.coordinator and self.synchronize:
          with synchronize(self.coordinator):
            giga.ensure.python.editables.absent(packages, self.py, self.python)
        else:
          giga.ensure.python.editables.absent(packages, self.py, self.python)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.python.editables.status(self.packages, self.py, self.python)
    )

giga.utils.set_config_logger(__name__, log)
