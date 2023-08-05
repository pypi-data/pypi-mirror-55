'Configs for downloading from the web.'

import giga
import logging
from lura import net

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Files(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, url, alg, sum in paths:
        with self.item(path):
          if sum and (sum[:5] == 'http:' or sum[:6] == 'https:'):
            sum = net.wgets(sum).rstrip().rsplit()[0]
          if not (sum and sys.isfile(path) and sys.ishash(path, alg, sum)):
            sys.wget(url, path, alg, sum)
            +self.task

    def absent(self, paths):
      giga.ensure.fs.files.absent(path for (path, _, _, _) in paths)

    def status(self, paths):
      return giga.ensure.fs.files.status(path for (path, _, _, _) in paths)

  class Bins(giga.Ensurer):

    def present(self, paths, mode=0o755):
      giga.ensure.wget.files.present(paths)
      giga.ensure.fs.modes.present((path, mode) for (path, _, _, _) in paths)

    def absent(self, paths):
      giga.ensure.wget.files.absent(paths)

    def status(self, paths, mode=0o755):
      return (
        giga.ensure.wget.files.status(paths) and
        giga.ensure.fs.modes.status((path, mode) for (path, _, _, _) in paths)
      )

giga.ensure.add_ensurers('wget', Ensurers)

class Files(giga.Config):

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} downloads') as task:
      giga.ensure.wget.files.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} downloads') as task:
      if not self.keep:
        paths = reversed(self.paths)
        giga.ensure.wget.files.absent(paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.wget.files.status(self.paths)
    )

class Bins(giga.Config):

  paths = None
  mode = 0o755
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} bin downloads') as task:
      giga.ensure.wget.bins.present(self.paths, self.mode)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} bin downloads') as task:
      if not self.keep:
        paths = reversed(self.paths)
        giga.ensure.wget.bins.absent(paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.wget.bins.status(self.paths, self.mode)
    )

giga.utils.set_config_logger(__name__, log)
