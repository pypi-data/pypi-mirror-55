import giga
import logging

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Clones(giga.Ensurer):

    def present(self, repos):
      sys = self.system
      for path, remote, branch in repos:
        with self.item(path):
          if not sys.isdir(path):
            if branch:
              sys(f'git clone -b {branch} {remote} {path}')
            else:
              sys(f'git clone {remote} {path}')
            +self.task

    def absent(self, repos):
      paths = (path for (path, _, _) in self.repos)
      giga.ensure.fs.directories.absent(paths, nonempty=True)

    def status(self, repos):
      return giga.ensure.fs.directories.status(
        path for (path, _, _) in self.paths
      )

  class Pulls(giga.Ensurer):

    def _needs_pull(self, path):
      sys = self.system
      sys('git remote update', cwd=path)
      ref = sys.stdout("git branch --format '%(refname)'", cwd=path).rstrip()
      diff = sys.stdout(f'git revlist --count HEAD..{ref}', cwd=path).rstrip()
      return int(diff) == 0

    def present(self, repos):
      sys = self.system
      for path in repos:
        with self.item(path):
          if self._needs_pull(path):
            sys('git pull --all', cwd=path)
            +self.task

    def status(self, repos):
      return not any(
        self.system.isdir(path) and self._needs_pull(path)
        for path in repos
      )

giga.ensure.add_ensurers('git', Ensurers)

class Clones(giga.Config):
  'Apply git clones if needed.'

  repos = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.repos)} git clones') as task:
      giga.ensure.git.clones.present(self.repos)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.repos)} git repo clones') as task:
      if not self.keep:
        giga.ensure.git.clones.absent(self.repos)

  def on_is_applied(self):
    return (
      super.on_is_applied() and
      giga.ensure.git.clones.status(self.repos)
    )

class Pulls(giga.Config):
  'Apply git pulls if needed.'

  repos = None

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.repos)} git pulls') as task:
      giga.ensure.git.pulls.present(self.repos)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.git.pulls.status(self.repos)
    )

giga.utils.set_config_logger(__name__, log)
