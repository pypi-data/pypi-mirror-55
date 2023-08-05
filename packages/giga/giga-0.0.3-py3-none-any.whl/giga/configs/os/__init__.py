import giga
import logging
from giga import ensure
from shlex import quote

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers): pass

giga.ensure.add_ensurers('os', Ensurers)

class Shell(giga.Config):

  # command-line utility

  shell = None
  quiet = False

  def on_init(self):
    super().on_init()
    if 'shell' in self.kwargs:
      self.shell = self.kwargs.shell
    if not self.shell:
      self.shell = self.system.shell
    self.argv = self.kwargs.argv if 'argv' in self.kwargs else self.args[0]

  def on_apply(self):
    super().on_apply()
    argv = self.argv
    with self.task(f'Run {argv}') as task:
      with task.item(argv):
        res = self.system.run(f'{self.shell} -i -c {quote(argv)}')
        +task
    quiet = as_bool(self.kwargs.get('quiet', self.quiet))
    if not quiet:
      self.log('\n' + res.format().rstrip() + '\n')

  def on_is_applied(self):
    return False

giga.utils.set_config_logger(__name__, log)

from giga.configs.os import debian
from giga.configs.os import redhat
