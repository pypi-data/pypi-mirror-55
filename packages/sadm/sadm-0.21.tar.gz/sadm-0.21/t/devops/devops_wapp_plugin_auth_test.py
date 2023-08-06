# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from pytest import raises
from unittest.mock import Mock

from _sadm.devops.wapp.auth.error import AuthError
from _sadm.devops.wapp.plugin import auth
from _sadm.devops.wapp.view import view

def test_plugin(devops_wapp):
	wapp = devops_wapp('session')
	with wapp.mock() as ctx:
		p = auth.AuthPlugin(ctx.config)
		assert p.api == 2
		assert p.name == 'sadm.devops.auth'

def test_setup(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		p = auth.AuthPlugin(ctx.config)
		p.setup(ctx.wapp)
		assert p.config is ctx.config
		assert p.auth.type == 'config'

def test_apply(devops_wapp):
	wapp = devops_wapp('session')
	with wapp.mock() as ctx:
		p = auth.AuthPlugin(ctx.config)
		p.setup(ctx.wapp)
		rtrn = object()
		ctx.callback = ctx.mock.callback
		ctx.callback.return_value = rtrn
		user = object()
		p.auth.check = Mock(return_value = user)
		resp = p.apply(ctx.callback, ctx.mock.ctx)()
		assert resp is rtrn
		ctx.callback.assert_called_with(user = user)

def test_auth_error(devops_wapp):
	wapp = devops_wapp('session')
	with wapp.mock() as ctx:
		p = auth.AuthPlugin(ctx.config)
		p.setup(ctx.wapp)
		rtrn = object()
		ctx.callback = ctx.mock.callback
		ctx.callback.return_value = rtrn
		p.auth.check = Mock()
		p.auth.check.side_effect = AuthError('testing.autherror')
		with raises(bottle.HTTPResponse) as exc:
			p.apply(ctx.callback, ctx.mock.ctx)()
		wapp.checkRedirect(exc, 302, view.url('user.login'))
