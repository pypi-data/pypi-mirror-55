'Task helper.'

import giga
import io
import os
from contextlib import contextmanager
from giga import ensure

def get_current():
  if not hasattr(giga._tls, 'task'):
    giga._tls.task = None
  return giga._tls.task

def _set_current(task):
  previous = get_current()
  giga._tls.task = task
  return previous

class Task:
  '''
  A context manager representing some activity which may or may not generate
  changes on a Configuration.

  This class provides a logical place to...

  - handle some automatic logging/console output
  - handle change tracking
  - provide access to an Ensure object
  - provide the thread synchronization hook
  '''

  def __init__(self, msg):
    super().__init__()
    config = giga.config.get_current()
    if not config:
      raise RuntimeError('%s cannot be used without a running config' % (
        type(self).__name__))
    self.config = config
    self.msg = msg
    self.verbose = config.config_verbose
    self.sync = config.config_sync
    coord = config.coordinator
    if coord:
      self.verbose = coord.verbose
      self.sync = coord.synchronize
    self.changes = 0
    self.previous = None
    self.items = []

  def __enter__(self):
    self.previous = _set_current(self)
    try:
      self.on_enter()
    except Exception:
      _set_current(self.previous)
      raise
    return self

  def __exit__(self, *exc_info):
    assert(self.changes >= 0)
    self.config.changes += self.changes
    try:
      self.on_exit(exc_info)
    finally:
      _set_current(self.previous)
    self.config = None
    self.previous = None
    self.items = None

  def on_enter(self):
    if self.sync:
      self.config.sync()

  def on_exit(self, exc_info):
    self.config.log(self.format_result(exc_info))

  def format_result(self, exc_info):
    config = self.config
    verbose = config.config_verbose
    if config.coordinator:
      verbose = config.coordinator.verbose
    with io.StringIO() as buf:
      if verbose:
        buf.writeline = lambda line: buf.write(line + os.linesep)
        buf.writeline(f'(  task) {self.msg}')
        for item, changed in self.items:
          c = '+' if changed else '.'
          buf.writeline(f'      {c}  {item}')
      if exc_info != (None, None, None):
        buf.write('[ error] ')
      elif self.changes == 0:
        buf.write('(    ok) ')
      else:
        buf.write('[change] ')
      buf.write(self.msg)
      return buf.getvalue()

  @contextmanager
  def item(self, item):
    changes = self.changes
    try:
      yield
    finally:
      self.items.append((item, changes != self.changes))

  @property
  def changed(self):
    return self.changes > 0

  def change(self, count=1, item=None):
    assert(count >= 0)
    self.changes += count
    if item is not None:
      self.items.append((item, count > 0))
    return self.changes

  __pos__ = change
  __add__ = change
