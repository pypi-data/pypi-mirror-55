# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.utils import systemd, path
from _sadm.utils.cmd import call, callCheck
from _sadm.utils.sh import mktmp

__all__ = ['deploy']

# run as root at last pass
sumode = 'post'

def deploy(env):
	_autoconf(env)
	_prune(env)
	systemd.restart('munin-node')

def _autoconf(env):
	env.log('autoconf')
	tmpfh = mktmp(prefix = __name__)
	tmpfh.write('exit 128')
	tmpfh.close()
	tmpfn = tmpfh.name()
	env.debug("tmpfn %s" % tmpfn)
	try:
		call("munin-node-configure --shell >%s 2>&1" % tmpfn)
		callCheck("/bin/sh -eu %s" % tmpfn)
	finally:
		tmpfh.unlink()

def _prune(env):
	dstdir = env.settings.get('service.munin_node',
		'target.dir', fallback = path.join('etc', 'munin'))
	pl = env.settings.getlist('service.munin_node',
		'prune.plugins', fallback = [])
	for x in pl:
		x = path.normpath(x)
		fl = path.glob(path.join(dstdir, 'plugins', x))
		for fn in fl:
			env.log("prune %s" % fn)
			path.unlink(fn)
