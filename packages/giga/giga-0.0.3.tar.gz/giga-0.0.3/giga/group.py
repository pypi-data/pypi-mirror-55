'System groups.'

import giga
import logging
import os
import traceback
from collections import Sequence
from giga import exec
from lura import net
from lura import utils
from lura.attrs import attr

log = logging.getLogger(__name__)

super_ = super

class Group(utils.Kwargs):

  synchronize       = True
  fail_early        = True
  workers           = None
  executor_type     = exec.Executor
  local_system_type = giga.unix.Local
  ssh_system_type   = giga.unix.Ssh
  verbose           = False

  def __init__(
    self, hosts, port=22, user=None, password=None, key_file=None,
    private_key=None, passphrase=None, connect_timeout=60.0, auth_timeout=60.0,
    compress=True, name=None, super=False, super_user=None, super_password=None,
    **kwargs
  ):
    super_().__init__(**kwargs)
    self._hosts = hosts
    self._ssh_system_args = attr(
      port=port, user=user, password=password, key_file=key_file,
      passphrase=passphrase, connect_timeout=connect_timeout,
      auth_timeout=auth_timeout, compress=compress, super=super,
      super_user=super_user, super_password=super_password)
    self._reset()
    if self.workers is not None:
      self.workers = min(self.workers, len(systems) or 1)

  def _reset(self):
    self.config = None
    self.systems = None
    self.args = None
    self.kwargs = None

  def _create_systems(self):
    history = []
    systems = []
    for host in self._hosts:
      name = None
      args = self._ssh_system_args.copy()
      if isinstance(host, str):
        args.host = host
      elif isinstance(host, Sequence) and len(host) == 2:
        args.name, args.host = host
      elif isinstance(host, giga.System):
        systems.append(host)
        continue
      else:
        raise ValueError(f'Unknown type for host in hosts list: {args.host}')
      # FIXME
      if args.host == '127.0.0.1':
        args.host = 'localhost'
      addr = net.resolve(args.host)
      if addr is None:
        raise RuntimeError(f'Could not resolve hostname: {args.host}')
      elif addr in history:
        log.warn(f'Duplicate host in hosts list: {args.host} ({addr})')
        continue
      history.append(addr)
      if args.host == 'localhost':
        sys = self.local_system_type(
          name='localhost', super=args.super, super_user=args.super_user,
          super_password=args.super_password)
      else:
        sys = self.ssh_system_type(**args)
      systems.append(sys)
    return systems

  def _format_result(self, res):
    ok = [
      (self.systems[_], res[_])
      for _ in range(0, len(res))
      if not utils.isexc(res[_])
    ]
    err = [
      (self.systems[_], res[_])
      for _ in range(0, len(res))
      if utils.isexc(res[_])
    ]
    return ok, err

  def _run(self, method, config, args, kwargs):
    if isinstance(config, type):
      config = config()
    self.config = config
    self.systems = self._create_systems()
    self.args = args
    self.kwargs = kwargs
    try:
      res = method(self)
      ok, err = self._format_result(res)
      return ok, err
    finally:
      self._reset()

  def apply(self, config, *args, **kwargs):
    ok, err = self._run(self.executor_type().apply, config, args, kwargs)
    return ok, err

  def delete(self, config, *args, **kwargs):
    try:
      ok, err = self._run(self.executor_type().delete, config, args, kwargs)
      return ok, err
    finally:
      self._reset()

  def is_applied(self, config, *args, **kwargs):
    try:
      ok, err = self._run(self.executor_type().is_applied, config, args, kwargs)
      return ok, err
    finally:
      self._reset()

  @classmethod
  def log_errors(cls, err, logger=log, level=log.ERROR):
    'Attempt to log exceptions from hosts in a readable way.'

    def mark():
      log('')
      log('-' * 50)
    log = logger[logger.ERROR]
    for sys, exc_info in err:
      _, exc, _ = exc_info
      if isinstance(exc, giga.Cancel):
        continue
      assert(isinstance(exc, giga.Fail))
      exc = exc.exc_info
      msg = f'[{sys.name}] Failed with unhandled exception' + os.linesep
      tb = ''.join(traceback.format_exception(*exc)).rstrip()
      mark()
      log(msg + tb)
    mark()

  @classmethod
  def log_changes(cls, ok, err, logger=log, level=log.INFO):
    'Log the change count for each host for apply/delete.'

    log = logger[level]
    results = sorted(ok + err, key=lambda res: res[0].name)
    for res in results:
      sys, res = res
      if isinstance(res, int):
        if res == 0:
          log(f'[{sys.name}] (  done) %5d changes' % res)
        else:
          log(f'[{sys.name}] [  done] %5d changes' % res)
      elif isinstance(res, bool):
          status = 'Applied' if res else 'Not applied'
          log(f'[{sys.name}] (  done) {status}')
      else: # res is exc_info
        _, exc, _ = res
        assert(isinstance(exc, giga.Abort))
        if res[1].changes is not None:
          # apply/delete
          log(f'[{sys.name}] [ error] %5d changes' % res[1].changes)
        # don't print applied status on exception

  @classmethod
  def log_results(cls, ok, err, logger=log):
    log_errors(err, logger)
    log_changes(ok, err, logger, level)
