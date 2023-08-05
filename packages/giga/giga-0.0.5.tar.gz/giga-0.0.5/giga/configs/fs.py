'Filesystem provisioners.'

import giga
import logging
import os
from lura import fs
from lura.hash import hashs
from lura.plates import jinja2
from shlex import quote

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Directories(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path in paths:
        with self.item(path):
          if not sys.isdir(path):
            sys.mkdirp(path)
            +self.task

    def absent(self, paths, nonempty=False):
      sys = self.system
      for path in paths:
        with self.item(path):
          if sys.isdir(path):
            if nonempty or len(sys.ls(path)) == 0:
              sys.rmrf(path)
              +self.task

    def status(self, paths):
      return all(self.system.isdir(path) for path in paths)

  class Files(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path in paths:
        with self.item(path):
          if not sys.isfile(path):
            sys.touch(path)
            +self.task

    def absent(self, paths):
      sys = self.system
      for path in paths:
        with self.item(path):
          if sys.isfile(path):
            sys.rmf(path)
            +self.task

    def status(self, paths):
      return all(self.system.isfile(path) for path in paths)

  class Copies(giga.Ensurer):

    def _same(self, src, dst, exc):
      sys = self.system
      if not sys.exists(src):
        if exc:
          raise RuntimeError(f"Can't copy, source file doesn't exist: {src}")
        return False
      if sys.isfile(src) and sys.isfile(dst):
        return sys.hash(src) == sys.hash(dst)
      return sys.exists(dst) # FIXME

    def present(self, paths):
      sys = self.system
      for src, dst in paths:
        with self.item(dst):
          if not self._same(src, dst, exc=True):
            self.system.cprf(src, dst)
            +self.task

    def absent(self, paths):
      giga.ensure.fs.files.absent(dst for (_, dst) in paths)

    def status(self, paths):
      return all(self._same(src, dst, exc=False) for (src, dst) in paths)

  class Templates(giga.Ensurer):

    def present(self, paths, env):
      for src, dst in paths:
        contents = jinja2.expandss(self.env, fs.loads(src))
        giga.ensure.fs.contents(dst, contents)

    def absent(self, paths):
      giga.ensure.fs.files.absent(dst for (_, dst) in paths)

    def status(self, paths, env):
      sys = self.system
      return all(
        sys.iscontents(dst, jinja2.expandss(self.env, fs.loads(src)))
        for (src, dst) in paths
      )

  class Symlinks(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for src, dst in paths:
        with self.item(dst):
          if not sys.islink(dst):
            sys.lns(src, dst)
            +self.task

    def absent(self, paths):
      sys = self.system
      for _, dst in paths:
        with self.item(dst):
          if sys.islink(dst):
            sys.rmf(dst)
            +self.task

    def status(self, paths):
      return all(self.system.islink(dst) for (_, dst) in paths)

  class Modes(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, mode in paths:
        with self.item(f'{oct(mode)[2:]} {path}'):
          if not sys.ismode(path, mode):
            sys.chmod(path, mode)
            +self.task

    def status(self, paths):
      return all(self.system.ismode(path, mode) for (path, mode) in paths)

  class Owners(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, owner in paths:
        with self.item(f'{owner} {path}'):
          if not sys.isowner(path, owner):
            sys.chown(path, owner)
            +self.task

    def status(self, paths):
      return all(self.system.isowner(path) for path in paths)

  class Groups(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, group in paths:
        with self.item(f'{group} {path}'):
          if not sys.isgroup(path, group):
            sys.chgrp(path, group)
            +self.task

    def status(self, paths):
      return all(self.system.isgroup(path) for path in paths)

  class Chowns(giga.Ensurer):

    def _owners(self, paths):
      return ((path, owner) for (path, owner, _) in paths if owner)

    def _groups(self, paths):
      return ((path, group) for (path, _, group) in paths if group)

    def present(self, paths):
      giga.ensure.fs.owners.present(self._owners(paths))
      giga.ensure.fs.groups.present(self._groups(paths))

    def status(self, paths):
      return all(
        giga.ensure.fs.owners.status(self._owners(paths)) and
        giga.ensure.fs.groups.status(self._roups(paths))
      )

  class Contents(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      alg = 'sha512'
      for path, contents in paths:
        with self.item(path):
          if sys.isfile(path) and sys.ishash(path, alg, hashs(contents, alg)):
            continue
          sys.dumps(path, contents)
          +self.task

    def absent(self, paths):
      giga.ensure.fs.files.absent(path for (path, _) in paths)

    def status(self, paths):
      sys = self.system
      alg = 'sha512'
      return all(
        sys.ishash(path, alg, hashs(contents, alg))
        for (path, contents) in paths
      )

  class Contains(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, contents in paths:
        with self.item(path):
          buf = ''
          if sys.isfile(path):
            buf = sys.loads(path)
          if contents not in buf:
            buf += contents
            sys.dumps(path, buf)
            +self.task

    def absent(self, paths):
      sys = self.system
      for path, contents in paths:
        with self.item(path):
          if sys.isfile(path):
            buf = sys.loads(path)
            if contents in buf:
              buf = buf.replace(contents, '')
              sys.dumps(path, buf)
              +self.task

    def status(self, paths):
      sys = self.system
      return all(sys.contains(path, contents) for (path, contents) in paths)

  class Backupfiles(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      end = '.dist'
      for path in paths:
        backup = f'{path}{end}'
        with self.item(backup):
          if not sys.exists(backup):
            sys.cpf(path, backup)
            +self.task

    def status(self, paths):
      end = '.dist'
      return all(self.system.exists(f'{path}{end}') for path in paths)

  class Pseudofs(giga.Ensurer):

    def present(self, paths):
      sys = self.system
      for path, value in paths:
        path, value = quote(path), quote(str(value))
        with self.item(path):
          if not sys.zero(f'test $(cat {path}) = {value}'):
            sys(f'tee {path} <<< {value}') # FIXME replace bashism
            +self.task

    def status(self, paths):
      return all(
        self.system.loads(path).rstrip() == str(value)
        for (path, value) in paths
      )

giga.ensure.add_ensurers('fs', Ensurers)

class Directories(giga.Config):
  'Create directories.'

  paths = None
  nonempty = False
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} directories') as task:
      giga.ensure.fs.directories.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} directories') as task:
      if not self.keep:
        paths = reversed(self.paths)
        giga.ensure.fs.directories.absent(paths, nonempty=self.nonempty)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.directories.status(self.paths)
    )

class Files(giga.Config):
  'Create files.'

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} files') as task:
      giga.ensure.fs.files.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} files') as task:
      if not self.keep:
        giga.ensure.fs.files.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.files.status(self.paths)
    )

class Copies(giga.Config):
  'Create copies.'

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} copies') as task:
      giga.ensure.fs.copies.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} copies') as task:
      if not self.keep:
        giga.ensure.fs.copies.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.copies.status(self.paths)
    )

class Templates(giga.Config):
  'Expand templates from the local system.'

  paths = None
  env = None
  keep = False

  def on_apply(self):
    super().on_apply()
    sys = self.system
    with giga.Task(f'Apply {len(self.path)} templates') as task:
      giga.ensure.fs.templates.present(self.paths, self.env)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} assets') as task:
      if not self.keep:
        paths = list(reversed(self.paths))
        giga.ensure.fs.templates.absent(self.paths)

  def on_is_applied(self):
    sys = self.system
    return (
      super().on_is_applied() and
      giga.ensure.fs.templates.status(self.paths, self.env)
    )

class Symlinks(giga.Config):
  'Create symlinks.'

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} symlinks') as task:
      giga.ensure.fs.symlinks.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} symlinks') as task:
      giga.ensure.fs.symlinks.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.symlinks.status(self.paths)
    )

class Modes(giga.Config):
  'Set file modes.'

  paths = None

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} modes') as task:
      giga.ensure.fs.modes.present(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.modes.status(self.paths)
    )

class Chowns(giga.Config):

  paths = None

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} owners') as task:
      giga.ensure.fs.chowns.present(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.chowns.status(self.paths)
    )

class Contents(giga.Config):

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} file content(s)') as task:
      giga.ensure.fs.contents.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} file content(s)') as task:
      if not self.keep:
        giga.ensure.fs.contents.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.contents.status(self.paths)
    )

class Contains(giga.Config):

  paths = None
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.paths)} file contains(s)') as task:
      giga.ensure.fs.contains.present(self.paths)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.paths)} file contains(s)') as task:
      if not self.keep:
        giga.ensure.fs.contains.absent(self.paths)

  def on_is_applied(self):
    return (
      super().on_is_applied() and
      giga.ensure.fs.contains.status(self.paths)
    )

giga.utils.set_config_logger(__name__, log)
