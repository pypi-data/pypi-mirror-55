import giga
from importlib import import_module
from lura.asset import Assets
from lura.attrs import attr
from lura.utils import Kwargs

def env(obj):
  '''
  Collect and return non-internal attributes from an object and its type.
  This function is intended to be an easy way to build an evaluation
  environment from a giga.Config type or instance for activities like template
  expansion.
  '''

  def get(obj):
    return attr(
      (name, getattr(obj, name)) for name in dir(obj)
      if not name.startswith('__')
    )

  if isinstance(obj, type):
    return get(obj)
  res = get(type(obj))
  res.update(get(obj))
  return res

def set_config_logger(mod_name, logger, log_level=None):
  '''
  Set config_logger and optionally config_log_level on all giga.Config
  sub-types and instances of sub-types in the given module.
  '''

  mod = import_module(mod_name)
  for obj_name in dir(mod):
    obj = getattr(mod, obj_name)
    if isinstance(obj, type) and issubclass(obj, giga.Config):
      obj.config_logger = logger
      if log_level is not None:
        obj.config_log_level = log_level

__all__ = (Assets, Kwargs, env, set_config_logger)
