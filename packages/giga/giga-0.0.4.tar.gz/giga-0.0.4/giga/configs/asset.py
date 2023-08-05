import giga
import logging
from lura.plates import jinja2

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Assets(giga.Ensurer):

    def present(self, paths, assets):
      giga.ensure.fs.contents.present(
        (dst, assets.loads(src)) for (src, dst) in paths
      )

    def absent(self, paths):
      giga.ensure.fs.files.absent(path for (_, path) in paths)

    def status(self, paths, assets):
      giga.ensure.fs.contents.status(
        (dst, assets.loads(src)) for (src, dst) in paths
      )

  class Templates(giga.Ensurer):

    def present(self, paths, assets, env):
      giga.ensure.fs.contents.present(
        (dst, jinja2.expandss(env, assets.loads(src)))
        for (src, dst) in paths
      )

    def absent(self, paths):
      giga.ensure.fs.files.absent(path for (_, path) in paths)

    def status(self, paths, assets, env):
      giga.ensure.fs.contents.status(
        (dst, jinja2.expandss(env, assets.loads(src)))
        for (src, dst) in paths
      )

giga.ensure.add_ensurers('asset', Ensurers)

class Assets(giga.Config):

  assets = None
  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} assets') as task:
      giga.ensure.asset.assets.present(self.paths, self.assets)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} assets') as task:
      if not self.keep:
        giga.ensure.asset.assets.absent(self.paths, self.assets)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      giga.ensure.asset.assets.status(self.paths, self.assets)
    )

class Templates(giga.Config):

  assets = None
  paths = None
  env = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} template assets') as task:
      giga.ensure.asset.templates.present(self.paths, self.assets, self.env)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} template assets') as task:
      if not self.keep:
        giga.ensure.asset.templates.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.asset.templates.status(self.paths, self.assets, self.env)
    )

giga.utils.set_config_logger(__name__, log)
