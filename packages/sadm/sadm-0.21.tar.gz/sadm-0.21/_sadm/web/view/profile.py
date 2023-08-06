# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log, cfg
from _sadm.web import tpl
from _sadm.web.app import wapp, view

@wapp.route('/profile')
@view('profile.html')
@tpl.data('profile')
def index():
	log.debug('index')
	return {
		'profiles': _getallProfiles(),
	}

def _getallProfiles():
	config = cfg.new()
	l = []
	for p in config.listProfiles():
		l.append(_getProfile(p, config))
	return l

def _getProfile(p, config):
	return {
		'name': p,
		'envs': config.listEnvs(p),
	}
