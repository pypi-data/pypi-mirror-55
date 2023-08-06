# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

__all__ = ['configure']

def configure(env, cfg):
	env.settings.merge(cfg, 'service.munin_node', (
		'config.dir',
		'target.dir',
		'prune.plugins',
	))
