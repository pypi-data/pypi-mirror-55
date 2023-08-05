'Apply kubespray to systems.'

import deepmerge
import logging
import giga
import io
from configparser import ConfigParser
from giga import configs
from lura import fs
from lura import net
from lura import threads
from lura.formats import yaml
from shlex import quote
from time import sleep

log = logging.getLogger(__name__)

merge = deepmerge.Merger(
  [
    (dict, ['merge']),
  ],
  ['override'],
  ['override'],
).merge

class Kubespray(giga.Config):
  '''
  Apply kubernetes to systems using Kubespray and Ansible.

  * Overview

  This is a unique Config, as Configs go.

  Several important values are passed to this configuration as arguments
  to apply():

  - ssh hosts for which we will be orchestrating k8s
  - ssh username for the k8s hosts
  - ssh password for the k8s hosts, if needed
  - sudo password for the k8s hosts, if needed

  These are also things we would typically pass to `giga.Ssh` or to
  `giga.Group`; but we will never run this Configuration on the k8s hosts
  that we're orchestrating. Rather, this Configuration would typically be
  applied to localhost, which will call Ansible against Kubespray on the
  local machine to orchestrate the remote k8s hosts. The arguments passed to
  apply() are passed directly to Ansible.

  You could of course apply this configuration to a remote host, and then
  that remote host would call Ansible to orchestrate the remote k8s hosts.
  This could even be useful in certain situations, but the typical use case
  is to apply this Configuration to localhost.

  * Applying

  The kwargs accepted by apply() are:

  - hosts      - hosts we will be ochestrating, required
  - user       - ssh username, required
  - login_pass - login password, optional
  - sudo_pass  - sudo password, optional
  - logfile    - override the standard logfile path, optional

  In my experience, Kubespray can take anywhere from 10 to 30 minutes to run,
  depending on your hosts' capabilities and network conditions.

  In the typical case where this Configuration is being applied locally, we
  take advantage of some knowledge of the underlying implementation to send
  Ansible's output to this module's logger, which users can configure to
  their liking.

  In the unusual case where this Configuration is being applied remotely, the
  log file on the remote will have to be tailed in a terminal in order to
  watch Ansible do its work.

  * group_vars

  Kubespray is quite configurable via its Ansible group_vars. This
  Configuration provides a hook for applying arbitrary custom group_vars
  values to a kubespray inventory. That hook is the `group_vars` class
  attribute (may also be passed as a kwarg to the constructor).

  `group_vars` is a dict. Each key is a relative path to a group_vars file in
  a given inventory's directory. Each value is a dict of variable names to
  values. The values dict will be merged onto the group_vars file, allowing
  us to override any setting in any group_vars file.

  For example:

    group_vars = {
      'all/all.yml': {
        'upstream_dns_servers': ['8.8.8.8', '8.8.4.4']
      },
      'k8s-cluster/k8s-cluster.yml': {
        'kube_version': 'v1.14.7',
        'kube_network_plugin': 'flannel'
      },
      'k8s-cluster/addons.yml': {
        'registry_enabled': True
      },
    }

  * Subclassing

  This Configuration should be friendly to inheritors, but if the existing
  methods of passing in settings (class attributes, constructor kwargs,
  apply() kwargs) are for some reason insufficient, just override vars(), add
  your settings to self or to self.kwargs or whatever, and then super().vars().
  Disco.
  '''

  config_include = [
    configs.python.Packages(packages=['pipenv'])
  ]

  kubespray_version = '2.11.0'
  logfile = '/tmp/kubespray.log'
  inventory_name = 'giga'
  group_vars = None
  connect_timeout = 180
  pipelining = True
  set_hostnames = False
  keep = False
  python = None

  _kubespray_tar_url = 'https://github.com/kubernetes-sigs/kubespray/archive/v%s.tar.gz'
  _pythons = ('python3', 'python3.7', 'python3.6')

  def on_init(self):
    super().on_init()
    sys = self.system
    if self.python is None:
      self.python = sys.which(*self._pythons, error=True)
    self.work_dir = sys.mktempdir(prefix='kubespray.')
    self.kubespray_tar_url = self._kubespray_tar_url % self.kubespray_version
    self.kubespray_tar_file = self.kubespray_tar_url.split('/')[-1]
    self.kubespray_tar_path = f'{self.work_dir}/{self.kubespray_tar_file}'
    self.kubespray_dir = f'{self.work_dir}/kubespray-{self.kubespray_version}'
    self.sample_dir = f'{self.kubespray_dir}/inventory/sample'
    self.inventory_dir = f'{self.kubespray_dir}/inventory/{self.inventory_name}'
    self.inventory_hosts_path = f'{self.inventory_dir}/hosts.yml'
    self.group_vars_dir = f'{self.inventory_dir}/group_vars'
    self.ansible_cfg_path = f'{self.kubespray_dir}/ansible.cfg'
    self.builder_dir = f'{self.kubespray_dir}/contrib/inventory_builder'
    self.user = self.kwargs.user
    self.login_pass = self.kwargs.get('login_pass')
    self.sudo_pass = self.kwargs.get('sudo_pass')
    self.hosts = []
    # the `hosts` kwarg can be either a list of hosts, or a comma-delimited
    # string
    hosts = self.kwargs.hosts
    if isinstance(hosts, str):
      hosts = hosts.split(',')
    for host in hosts:
      # the inventory builder allows only ip addresses
      if not net.is_ip_address(host):
        addr = net.resolve(host)
        if not addr:
          raise ValueError(f'Unable to resolve ip address for host: {host}')
        host = addr
      self.hosts.append(host)
    self.logfile = self.kwargs.get('logfile', self.logfile)
    self.keep = self.kwargs.get('keep', self.keep)

  def apply_kubespray_tar(self):
    with giga.Task('Apply kubespray tar') as task:
      sys = self.system
      sys.wget(self.kubespray_tar_url, self.kubespray_tar_path)
      sys(f'tar -C {self.work_dir} -xf {self.kubespray_tar_path}')
      task + 2

  def apply_pipenv(self):
    with giga.Task('Apply pipenv') as task:
      sys = self.system
      sys('pipenv install', cwd=self.kubespray_dir)
      +task

  def apply_requirements(self):
    sys = self.system
    reqs = (
      ('kubespray',         f'{self.kubespray_dir}/requirements.txt'),
      ('inventory builder', f'{self.builder_dir}/requirements.txt'),
    )
    for pkg, req in reqs:
      with giga.Task(f'Apply {pkg} requirements') as task:
        sys(f'pipenv install -r {quote(req)}', cwd=self.kubespray_dir)
        +task

  def apply_inventory(self):
    with giga.Task('Apply inventory') as task:
      sys = self.system
      sys.cprf(self.sample_dir, self.inventory_dir)
      env = {'CONFIG_FILE': self.inventory_hosts_path}
      argv = 'pipenv run %s contrib/inventory_builder/inventory.py %s' % (
        self.python, ' '.join(self.hosts))
      sys(argv, env=env, cwd=self.kubespray_dir)
      +task

  def apply_ansible_cfg(self):
    with giga.Task('Apply ansible.cfg') as task:
      sys = self.system
      cfg = ConfigParser()
      with io.StringIO(sys.loads(self.ansible_cfg_path)) as buf:
        cfg.read_file(buf)
      cfg.setdefault('ssh_connection', {})
      cfg['ssh_connection']['pipelining'] = str(self.pipelining)
      with io.StringIO() as buf:
        cfg.write(buf)
        giga.ensure.fs.contents([(self.ansible_cfg_path, buf.getvalue())])

  def apply_group_vars(self):
    sys = self.system
    if not self.group_vars:
      return
    for path, update in self.group_vars.items():
      with giga.Task(f'Applying group_vars/{path}') as task:
        path = f'{self.group_vars_dir}/{path}'
        vars = yaml.loads(sys.loads(path))
        merge(vars, update)
        giga.ensure.fs.contents([(path, yaml.dumps(vars))])

  def apply_ansible(self):
    with giga.Task('Apply ansible') as task:
      sys = self.system
      env = dict(
        ANSIBLE_TIMEOUT = str(self.connect_timeout),
        ANSIBLE_INVALID_TASK_ATTRIBUTE_FAILED = 'False',
      )
      set_hostnames = str(self.set_hostnames).lower()
      extra_vars = [f'override_system_hostname={set_hostnames}']
      if self.login_pass:
        extra_vars.append(f'ansible_pass={self.login_pass}')
      if self.sudo_pass:
        extra_vars.append(f'ansible_become_pass={self.sudo_pass}')
      extra_vars = quote(' '.join(extra_vars))
      argv = 'pipenv run ansible-playbook cluster.yml -i %s -e %s -u %s -b' % (
        self.inventory_hosts_path, extra_vars, self.user)
      argv = f'{argv} </dev/null 2>&1 | tee {quote(self.logfile)}'
      if isinstance(sys, giga.unix.Local):
        from lura import run
        with run.log(self.config_logger, self.config_log_level): # fuck yeah
          sys(argv, env=env, cwd=self.kubespray_dir)
      else:
        sys(argv, env=env, cwd=self.kubespray_dir)
      +task

  def apply_pipenv_cleanup(self):
    with giga.Task('Apply pipenv cleanup') as task:
      try:
        self.system('pipenv --rm', cwd=self.kubespray_dir)
        +task
      except Exception:
        log.exception('Unhandled exception while cleaning up pipenv')

  def apply_work_dir_cleanup(self):
    with giga.Task('Apply work dir cleanup') as task:
      if self.keep:
        return
      self.system.rmrf(self.work_dir)
      +task

  def on_apply_start(self):
    if self.coordinator:
      # ensure this configuration is running against only one host
      kubesprays = tuple(
        config for config in self.coordinator.configs
        if isinstance(config, Kubespray)
      )
      if len(kubesprays) > 1:
        raise RuntimeError('Refusing to apply Kubespray to multiple hosts')

  def on_apply(self):
    self.init()
    try:
      try:
        super().on_apply()
        self.apply_kubespray_tar()
        self.apply_pipenv()
        try:
          self.apply_requirements()
          self.apply_inventory()
          self.apply_ansible_cfg()
          self.apply_group_vars()
          self.apply_ansible()
        finally:
          self.apply_pipenv_cleanup()
      finally:
        self.apply_work_dir_cleanup()
    finally:
      self.reset()

  def on_is_applied(self):
    return False

giga.utils.set_config_logger(__name__, log)
