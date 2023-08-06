#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import sys

from _sadm import libdir
from _sadm.cmd import flags
from _sadm.devops import devops
from _sadm.errors import CommandError
from _sadm.utils import path, sh
from _sadm.utils.cmd import callCheck

def bottle():
	return devops.start()

def uwsgi():
	cmd = [
		'uwsgi',
		'--need-plugin', 'python3',
		'--set-ph', "sadm-home=%s" % sys.exec_prefix,
		'--touch-reload', path.join(path.sep, 'etc', 'opt', 'sadm', 'devops.cfg'),
		'--touch-reload', libdir.fpath('devops', 'wsgi', 'uwsgi.ini'),
		'--safe-pidfile', path.join(path.sep, 'tmp', 'sadm.devops.uwsgi.pid'),
		'--ini', libdir.fpath('devops', 'wsgi', 'uwsgi.ini'),
		'--module', '_sadm.devops.devel',
	]
	try:
		callCheck(cmd)
	except CommandError as err:
		return err.rc
	return 0

if __name__ == '__main__': # pragma: no cover
	if '--bottle' in sys.argv:
		sys.exit(bottle())
	else:
		sys.exit(uwsgi())
