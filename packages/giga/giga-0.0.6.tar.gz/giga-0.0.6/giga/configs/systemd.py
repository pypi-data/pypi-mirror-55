import giga
import logging
from giga import configs
from giga import ensure

log = logging.getLogger(__name__)

class Ensurers(giga.Ensurers):

  class Starts(giga.Ensurer):

    def present(self, services):
      sys = self.system
      for svc in services:
        with self.item(svc):
          if sys.nonzero(f'systemctl status {svc}'):
            sys(f'systemctl start {svc}')
            +self.task

    def absent(self, services):
      sys = self.system
      for svc in services:
        with self.item(svc):
          if sys.zero(f'systemctl status {svc}'):
            sys(f'systemctl stop {svc}')
            +self.task

    def status(self, services):
      return all(
        self.system.zero(f'systemctl status {svc}')
        for svc in services
      )

  class Enables(giga.Ensurer):

    def present(self, services):
      sys = self.system
      for svc in services:
        with self.item(svc):
          if sys.nonzero(f'systemctl is-enabled {svc}'):
            sys(f'systemctl enable {svc}')
            +self.task

    def absent(self, services):
      sys = self.system
      for svc in services:
        with self.item(svc):
          if sys.zero(f'systemctl is-enabled {svc}'):
            sys(f'systemctl disable {svc}')
            +self.task

    def status(self, services):
      return all(
        self.system.zero(f'systemctl is-enabled {svc}') for svc in services
      )

giga.ensure.add_ensurers('systemd', Ensurers)

class ReloadSystemd(giga.Config):

  def apply_systemd_reload(self):
    with giga.Task('Apply systemd reload') as task:
      if self.changed:
        self.system('systemctl daemon-reload')

  def on_apply(self):
    super().on_apply()
    self.apply_systemd_reload()

  def on_delete(self):
    super().on_delete()
    self.apply_systemd_reload()

class Starts(giga.Config):
  'Enable and start services.'

  services = None
  enable = True
  disable = True
  keep = False

  def on_apply(self):
    super().on_apply()
    with giga.Task(f'Apply {len(self.services)} systemd services') as task:
      giga.ensure.systemd.starts.present(self.services)
      if self.enable:
        giga.ensure.systemd.enables.present(self.services)

  def on_delete(self):
    super().on_delete()
    with giga.Task(f'Delete {len(self.services)} systemd services') as task:
      if not self.keep:
        services = tuple(reversed(self.services))
        giga.ensure.systemd.starts.absent(services)
        if self.disable:
          giga.ensure.systemd.enables.absent(services)

  def on_is_applied(self):
    res = [super().on_is_applied()]
    res.append(giga.ensure.systemd.starts.status(self.services))
    if self.enable:
      res.append(giga.ensure.systemd.enables.status(self.services))
    return all(res)

giga.utils.set_config_logger(__name__, log)
