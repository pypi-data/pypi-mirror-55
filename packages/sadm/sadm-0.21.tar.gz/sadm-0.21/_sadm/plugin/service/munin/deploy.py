# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.utils import systemd, path
from _sadm.utils.sh import makedirs, chmod, chown

__all__ = ['deploy']

# run as root at last pass
sumode = 'post'

def deploy(env):
	dbdir = env.settings.get('service.munin', 'dbdir')
	dbuser = env.settings.get('service.munin', 'dbdir.user')
	dbgroup = env.settings.get('service.munin', 'dbdir.group')
	htmldir = env.settings.get('service.munin', 'htmldir')

	env.log("dbdir %s (%s:%s)" % (dbdir, dbuser, dbgroup))
	makedirs(dbdir, exists_ok = True)
	chmod(dbdir, 0o750)
	chown(dbdir, user = dbuser, group = dbgroup)

	# prune
	for s in env.settings.sections():
		if s.startswith('munin.prune:'):
			domain = s.split(':')[1].strip()
			for host in env.settings.options(s):
				_prune(env, dbdir, htmldir, s, domain, host)

	if systemd.status('cron') != 0:
		systemd.restart('cron')

	if systemd.status('munin') != 0:
		systemd.restart('munin')

def _prune(env, dbdir, htmldir, sect, domain, host):
	pl = env.settings.getlist(sect, host)
	for patt in pl:
		patt = path.normpath(patt)
		if domain.upper() == 'ALL':
			domain = '*'
		if host.upper() == 'ALL':
			host = '*'
		fl = path.glob(path.join(dbdir, domain, "%s-%s-*.rrd" % (host, patt)))
		fl.extend(path.glob(path.join(htmldir, domain, host, "%s.html" % patt)))
		fl.extend(path.glob(path.join(htmldir, domain, host, "%s-*.png" % patt)))
		for fn in fl:
			env.log("prune %s" % fn)
			path.unlink(fn)
