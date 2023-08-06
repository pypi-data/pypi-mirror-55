# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from contextlib import contextmanager
from os import path, makedirs
from shutil import rmtree
from unittest.mock import Mock

from _sadm import cfg

import _sadm.devops.wapp.cfg
import _sadm.devops.wapp.tpl.tpl
import _sadm.devops.wapp.session.session
import _sadm.devops.wapp.wapp

from _sadmtest import mock
from _sadmtest.wapp import TestingWebapp

class DevopsWebapp(TestingWebapp):
	name = 'devops'

	@contextmanager
	def mock(self, tag = 'devops'):
		mockcfg = None
		if path.isfile(self.cfgfn):
			mockcfg = cfg.new(self.cfgfn)
		bup = Mock()
		# bup bottle
		bup.bottle = bup.mock.bottle
		bup.bottle.template = bottle.template
		# bup wapp
		bup.wapp = _sadm.devops.wapp.wapp.wapp
		# bup tpl
		bup.tpl = bup.mock.tpl
		bup.tpl.parse = _sadm.devops.wapp.tpl.tpl.parse
		bup.tpl.version = _sadm.devops.wapp.tpl.tpl.version
		# bup session
		bup.session = bup.mock.session
		bup.session._secret = _sadm.devops.wapp.session.session._secret
		with mock.log(), mock.utils(mockcfg, tag = tag):
			ctx = Mock()
			ctx.orig = bup
			try:
				# mock bottle
				ctx.bottle = ctx.mock.bottle
				ctx.bottle.template = ctx.mock.bottle.template
				bottle.template = ctx.bottle.template
				# test session db dir
				sessdbdir = path.join('tdata', 'tmp', 'devops', 'wapp', 'session')
				if path.isdir(sessdbdir):
					print('mock.devops.wapp rmtree', sessdbdir)
					rmtree(sessdbdir)
				# mock wapp
				print('mock.devops.wapp init')
				_sadm.devops.wapp.wapp.init(cfgfn = self.cfgfn)
				ctx.wapp = ctx.mock.wapp
				_sadm.devops.wapp.wapp.wapp = ctx.wapp
				# mock config
				ctx.config = _sadm.devops.wapp.cfg.config
				# mock tpl
				ctx.tpl = ctx.mock.tpl
				ctx.tpl.parse = ctx.mock.tpl.parse
				_sadm.devops.wapp.tpl.tpl.parse = ctx.tpl.parse
				ctx.tpl.version = ctx.mock.tpl.version
				ctx.tpl.version.string = ctx.mock.tpl.version.string
				ctx.tpl.version.string.return_value = 'testing'
				_sadm.devops.wapp.tpl.tpl.version = ctx.tpl.version
				yield ctx
			finally:
				print('mock.devops.wapp.restore')
				# restore bottle
				del bottle.template
				bottle.template = bup.bottle.template
				# restore wapp
				del _sadm.devops.wapp.wapp.wapp
				_sadm.devops.wapp.wapp.wapp = bup.wapp
				# restore config
				del _sadm.devops.wapp.cfg.config
				_sadm.devops.wapp.cfg.config = None
				# restore tpl
				del _sadm.devops.wapp.tpl.tpl.parse
				_sadm.devops.wapp.tpl.tpl.parse = bup.tpl.parse
				del _sadm.devops.wapp.tpl.tpl.version
				_sadm.devops.wapp.tpl.tpl.version = bup.tpl.version
				# restore session
				del _sadm.devops.wapp.session.session._secret
				_sadm.devops.wapp.session.session._secret = bup.session._secret

	def mock_req(self, sessid, user = 'testing'):
		req = Mock()
		req.get_cookie.return_value = sessid
		req.forms = {
			'username': user,
			'password': 'testing.password',
		}
		req.headers = {
			'X-Forwarded-Proto': 'https',
			'X-Auth-Token': '76543210',
			'X-Client-Fingerprint': 'abc123def',
		}
		return req

	def mock_sess(self, wa, sessid, user = 'testing'):
		sess = wa.sess.save(sessid, user)
		return (sess, self.mock_req(sessid, user = user))
