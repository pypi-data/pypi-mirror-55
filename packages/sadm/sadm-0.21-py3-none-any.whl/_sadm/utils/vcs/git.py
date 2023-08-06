# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from contextlib import contextmanager

from _sadm.utils import sh
from _sadm.utils.cmd import callCheck
from _sadm.utils import path as fpath
from _sadm.utils.vcs import vcs

__all__ = ['clone', 'checkout', 'pull']

_configDone = False

def _configure():
	global _configDone
	if _configDone:
		return
	sshcmd = ('ssh',
		'-o', 'UserKnownHostsFile=/dev/null',
		'-o', 'StrictHostKeyChecking=no',
		'-o', 'BatchMode=yes',
	)
	cmd = ['git', 'config', '--global', 'core.sshCommand', ' '.join(sshcmd)]
	callCheck(cmd)
	_configDone = True

@contextmanager
def _repodir(path):
	_configure()
	with vcs.repodir(path):
		yield

def clone(path, remote, branch):
	_configure()
	cmd = ['git', 'clone', '-b', branch, remote, path]
	callCheck(cmd)

def checkout(path, commit):
	with _repodir(path):
		callCheck(['git', 'checkout', commit])

def pull(path):
	with _repodir(path):
		callCheck(['git', 'pull'])
