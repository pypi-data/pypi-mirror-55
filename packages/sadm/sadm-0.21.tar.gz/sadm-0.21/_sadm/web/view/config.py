# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from os import getenv
from io import StringIO

from _sadm import log, cfg
from _sadm.web import tpl
from _sadm.web.app import wapp, view

@wapp.route('/config')
@view('config.html')
@tpl.data('config')
def index():
	log.debug("index")
	config = cfg.new()
	return {
		'cfgfile': config.filename(),
		'cfg': _getCfg(config),
	}

def _getCfg(config):
	buf = StringIO()
	config.reload()
	config.write(buf)
	buf.seek(0, 0)
	return buf.read()
