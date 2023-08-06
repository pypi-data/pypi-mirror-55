# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from contextlib import contextmanager

from _sadm.utils import sh
from _sadm.utils.cmd import callCheck
from _sadm.utils import path as fpath

__all__ = ['repodir', 'deploy']

@contextmanager
def repodir(path):
	oldwd = sh.getcwd()
	try:
		sh.chdir(path)
		yield
	finally:
		sh.chdir(oldwd)

_deployScripts = ('install.sh', 'build.sh',  'check.sh', 'deploy.sh')

def deploy(path):
	with repodir(path):
		if fpath.isdir('.sadm'):
			for sn in _deployScripts:
				script = fpath.join('.', '.sadm', sn)
				if fpath.isfile(script):
					callCheck(['/bin/sh', script])
