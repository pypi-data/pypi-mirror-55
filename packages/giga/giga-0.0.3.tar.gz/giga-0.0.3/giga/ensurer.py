import giga
from lura.strutils import camel_to_snake

class Ensurer:

  def __init__(self, name):
    super().__init__()
    self.name = name

  @property
  def config(self):
    config = giga.config.get_current()
    if config is None:
      raise RuntimeError('Cannot be called without a running Config')
    return config

  @property
  def system(self):
    config = giga.config.get_current()
    if None in (config, config.system):
      raise RuntimeError('Cannot be called without a running Config')
    return config.system

  @property
  def task(self):
    task = giga.task.get_current()
    if task is None:
      raise RuntimeError('Cannot be called without a Task context')
    return task

  def item(self, item):
    task = giga.task.get_current()
    if task is None:
      raise RuntimeError('Cannot be called without a Task context')
    return task.item(f'{self.name} {item}')

  def present(self, *args, **kwargs):
    raise NotImplementedError('Ensurer %s does not implement present()' % (
      type(self).__name__))

  def absent(self, *args, **kwargs):
    raise NotImplementedError('Ensurer %s does not implement absent()' % (
      type(self).__name__))

  def status(self, *args, **kwargs):
    raise NotImplementedError('Ensurer %s does not implement status()' % (
      type(self).__name__))

class Ensurers:

  def __init__(self, name):
    super().__init__()
    self.name = name
    selfcls = type(self)
    for name in dir(selfcls):
      if name[0] != '_':
        cls = getattr(selfcls, name)
        if isinstance(cls, type) and issubclass(cls, Ensurer):
          name = camel_to_snake(cls.__name__)
          setattr(self, name, cls(f'{self.name}.{name}'))

  def add_ensurers(self, name, cls):
    giga.ensure.assert_ensurers(name, cls)
    assert(
      not hasattr(self, name) or
      isinstance(getattr(self, name), giga.Ensurers)
    )
    setattr(self, name, cls(f'{self.name}.{name}'))
