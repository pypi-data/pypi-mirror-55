def assert_ensurers(name, cls):
  import giga
  assert(cls is not None)
  assert(isinstance(cls, type))
  assert(issubclass(cls, giga.Ensurers))
  assert(isinstance(name, str))

def add_ensurers(name, cls):
  import giga
  assert_ensurers(name, cls)
  assert(
    not hasattr(giga.ensure, name) or
    isinstance(getattr(giga.ensure, name), giga.Ensurers)
  )
  setattr(giga.ensure, name, cls(name))
