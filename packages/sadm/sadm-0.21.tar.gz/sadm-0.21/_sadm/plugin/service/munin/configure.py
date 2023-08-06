# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

__all__ = ['configure']

def configure(env, cfg):
	env.settings.merge(cfg, 'service.munin', (
		'config.dir',
		'db.dir',
		'dbdir.user',
		'dbdir.group',
	))
	for s in cfg.sections():
		if s.startswith('munin.prune:'):
			env.settings.merge(cfg, s, cfg.options(s))
