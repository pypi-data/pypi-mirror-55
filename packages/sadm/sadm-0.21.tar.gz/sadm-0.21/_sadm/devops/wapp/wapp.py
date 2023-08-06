# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from _sadm import libdir, log, version
from _sadm.devops.wapp import cfg, errors, handlers
from _sadm.devops.wapp.plugin.auth import AuthPlugin
from _sadm.devops.wapp.session import session
from _sadm.utils import path

__all__ = ['init']

_wappcfg = libdir.fpath('devops', 'wapp', 'wapp.conf')
_cfgfn = path.join(path.sep, 'etc', 'opt', 'sadm', 'devops.cfg')

wapp = bottle.Bottle()

def init(cfgfn = _cfgfn):
	config = cfg.new(cfgfn)

	log.init(config.get('sadm', 'log', fallback = 'error'))
	log.debug(version.string('sadm-devops'))
	log.debug("read config %s" % cfgfn)

	log.debug("bottle config %s" % _wappcfg)
	wapp.config.load_config(_wappcfg)

	tpldir = libdir.fpath('devops', 'wapp', 'tpl')
	log.debug("templates dir %s" % tpldir)
	bottle.TEMPLATE_PATH = [tpldir]

	rmplugins = [p.strip() for p in wapp.config.get('plugins.uninstall', '').split(' ')]
	for p in rmplugins:
		if p != '':
			log.debug("plugin uninstall %s" % p)
			wapp.uninstall(p)

	log.debug('install auth plugins')
	wapp.install(AuthPlugin(config))

	errors.init(wapp)
	handlers.init(wapp)

	session.init(config)

	log.debug("loaded handlers %s" % [r.name for r in wapp.routes])
	return wapp
