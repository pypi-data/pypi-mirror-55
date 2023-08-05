'Command-line interface.'

import click
import giga
import logging
import os
import traceback
from getpass import getpass
from getpass import getuser
from importlib import import_module
from lura.attrs import attr
from lura.click import StartsWithGroup
from sys import exit
from tabulate import tabulate

log = logger = logging.getLogger(__name__)

def parse_hosts(hosts):
  '''
  Parse the -h/--host argument.

  All things that accept -h handle it in the same way. The rules:

  * --host is repeatable:

      -h host1 -h host2 -h host3

  * --host can be a list of comma-delimited hosts:

      -h host1,host2,host3 -h host4,host5

  * --hosts can be given a name, which will be printed in the logs in lieu
    of long hostnames, which helps reduce the column count

      -h host1=zaybxcwd-01.mycompany.com,host2=zaybxcwd-02.mycompany.com

  * --hosts can be a filename containing a list of hosts with each line
    formatted as described above.

    The '#' character may be used in the file for comments, and blank lines
    are ignored.

      -h @myhosts.txt
  '''
  res = []
  for host in hosts:
    if host[0] == '@':
      path = host[1:]
      with open(path) as pathf:
        for line in pathf:
          line = line.strip()
          if not line or line[0] == '#':
            continue
          res.append(line)
    elif ',' in host:
      res.extend(host.rstrip(',').split(','))
    else:
      res.append(host)
  hosts = res
  res = []
  for host in hosts:
    if '=' in host:
      name, host = host.split('=', 1)
      res.append(name.strip(), host.strip())
    else:
      res.append((host, host))
  return res

def get_hosts(args, config, config_args, config_kwargs):
  '''
  Determine and return the list of hosts, a sequence of (name, host) pairs.
  The name field is intended as a short, friendly name for use in log
  messages. The host field is the address of the remote host. When no name
  is available, it should default to the host.

  If hosts are provided on the command line, then they are always used.

  If hosts are not provided on the command line, then the target Configuration
  may provide a hosts list by providing a `giga_hosts` attribute.

  The `Configuration.giga_hosts` attribute may be a sequence of pairs, or
  a callable which returns a sequence of pairs, as described above. The
  callable will be passed the exploded Configuration args and kwargs provided
  on the command line via -a and -A.

  Note that if multiple Configurations are specified for an operation, the
  `giga_hosts` from the first one will be used for all of them.
  ''' # FIXME

  name = (config if isinstance(type, config) else type(config)).__name__
  if args.host:
    return parse_hosts(args.host)
  elif hasattr(config, 'giga_hosts'):
    if callable(config.giga_hosts):
      hosts = config.giga_hosts(*config_args, **config_kwargs)
    else:
      hosts = config.giga_hosts
    if not hosts:
      log.error(f'fError: No hosts (-h) given, and {name}.giga_hosts is empty')
      exit(2)
  else:
    msg = 'Error: No hosts (-h) given, and %s has no giga_hosts attribute'
    log.error(msg % name)
    exit(2)

def get_passwords(args):
  'Sort out the password arguments.'

  password, super_password = args.login_password, args.super_password
  if not password and args.prompt_login:
    password = getpass('Login password: ')
  if not super_password and args.prompt_super:
    if password:
      super_password = getpass('Sudo password [enter to use login]: ')
      if super_password == '':
        super_password = password
    else:
      super_password = getpass('Super password: ')
  return password, super_password

def group(args):
  "Create a `giga.Group` for the systems we'll be working with."

  password, super_password = get_passwords(args)
  return giga.Group(
    args.hosts,
    user = args.user,
    password = password,
    super_password = super_password,
    connect_timeout = args.connect_timeout,
    auth_timeout = args.auth_timeout,
    super = args.super,
    compress = True,
    verbose = args.verbose,
  )

def lookup_config(config):
  'Lookup a Configuration object using its module and object name.'

  if '.' not in config:
    log.error(f'Error: invalid config "{config}", expected python object path')
    exit(2)
  mod, obj = config.rsplit('.', 1)
  try:
    mod = import_module(mod)
  except ModuleNotFoundError:
    log.error(f'Error: module not found: {mod}')
    exit(2)
  if not hasattr(mod, obj):
    log.error(f'Error: module "{mod.__name__}" has no objet "{obj}"')
    exit(2)
  obj = getattr(mod, obj)
  return obj

#####
## giga
@click.group('giga', cls=StartsWithGroup)
@click.option(
  '-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option(
  '-d', '--debug', is_flag=True, help='Enable debug output.')
@click.pass_context
def cli_giga(ctx, verbose, debug):
  'Apply or delete configurations.'

  from lura.logutils import formats
  level = logging.DEBUG if debug else logging.INFO
  format = formats.hax if verbose or debug else formats.user
  loggers = (logging.getLogger(logger) for logger in ('lura', 'giga'))
  for logger in loggers:
    logger.setLevel(level)
    logger.setConsoleFormat(format)
  ctx.obj = attr(verbose=verbose, debug=debug)

#####
## giga apply
@cli_giga.command('apply')
@click.option(
  '-u', '--user', default=getuser(),
  help='Login username, default current user.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify superuser password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to apply.')
@click.option(
  '-f', '--force', is_flag=True, help='Suppress is-applied check.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_apply(ctx, **args):
  'Apply a configuration.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  try:
    for config in configs:
      apply(config, args)
  except Exception:
    log.exception(f'Unhandled exception while applying {config}')
    exit(2)

def apply(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  if not args.force:
    ok, err = grp.is_applied(config, *config_args, **config_kwargs)
    if err:
      grp.log_errors(err, log)
      exit(2)
    if all(res for (_, res) in ok):
      return
  ok, err = grp.apply(config, *config_args, **config_kwargs)
  if err:
    grp.log_errors(err, log)
    grp.log_changes(ok, err, log)
    exit(2)
  grp.log_changes(ok, err, log)

#####
## giga delete
@cli_giga.command('delete')
@click.option(
  '-u', '--user', default=getuser(), show_default='current user',
  help='Login username.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify superuser password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to delete.')
@click.option(
  '-f', '--force', is_flag=True, help='Delete if alread deleted.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_delete(ctx, **args):
  'Delete a configuration.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  try:
    for config in configs:
      delete(config, args)
  except Exception:
    log.exception('Unhandled exception while deleting')
    exit(2)

def delete(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  if not args.force:
    ok, err = grp.is_applied(config, *config_args, **config_kwargs)
    if err:
      grp.log_errors(err, log)
      exit(2)
    if all(not res for (_, res) in ok):
      return
  ok, err = grp.delete(config, *config_args, **config_kwargs)
  if err:
    grp.log_errors(err, log)
    grp.log_changes(ok, err, log)
    exit(2)
  grp.log_changes(ok, err, log)

#####
## giga is-applied
@cli_giga.command('is-applied')
@click.option(
  '-u', '--user', default=getuser(), show_default='current user',
  help='Login username.')
@click.option(
  '-s', '--super', is_flag=True, help='Run as the superuser.')
@click.option(
  '-p', '--prompt-login', is_flag=True, help='Prompt for login password.')
@click.option(
  '-P', '--prompt-super', is_flag=True, help='Prompt for superuser password.')
@click.option(
  '--login-password', help='Specify login password.')
@click.option(
  '--super-password', help='Specify super password.')
@click.option(
  '-h', '--host', multiple=True, help='Host(s) to query.')
@click.option(
  '-a', '--set-arg', multiple=True, help='Set a config arg.')
@click.option(
  '-A', '--set-kwarg', multiple=True, help='Set a config kwarg.')
@click.option(
  '--connect-timeout', default=120, envvar='GIGA_CONNECT_TIMEOUT',
  help='Connect timeout, default 120.')
@click.option(
  '--auth-timeout', default=120, envvar='GIGA_AUTH_TIMEOUT',
  help='Auth timeout, default 120.')
@click.argument(
  'config', nargs=-1, required=True)
@click.pass_obj
def cli_giga_is_applied(ctx, **args):
  'Check if a configuration is applied.'

  args = attr(args)
  args.verbose = ctx.verbose
  configs = args.pop('config')
  res = 0
  try:
    for config in configs:
      if not is_applied(config, args):
        res = 1
  except Exception:
    log.exception('Unhandled exception while checking apply state')
    exit(2)
  exit(res)

def is_applied(config, args):
  config = lookup_config(config)
  config_args = args.set_arg
  config_kwargs = attr()
  for kwarg in args.set_kwarg:
    k, v = kwarg.split('=', 1)
    config_kwargs[k] = v
  args.hosts = get_hosts(args, config, config_args, config_kwargs)
  grp = group(args)
  ok, err = grp.is_applied(config, *config_args, **config_kwargs)
  if err:
    grp.log_errors(err, log)
    exit(2)
  return all(res for (_, res) in ok)

#####
### giga list
@cli_giga.command('list')
@click.argument(
  'module', nargs=-1)
def cli_giga_list(module):
  'List configurations in a module.'

  pass

if __name__ == '__main__':
  cli_giga()
