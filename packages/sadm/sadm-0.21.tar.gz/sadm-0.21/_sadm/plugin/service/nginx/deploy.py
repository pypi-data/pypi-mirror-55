# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.utils import systemd

__all__ = ['deploy']

# run as root at last pass
sumode = 'post'

def deploy(env):
	if systemd.status('nginx') != 0:
		systemd.restart('nginx')
	else:
		systemd.reload('nginx')
