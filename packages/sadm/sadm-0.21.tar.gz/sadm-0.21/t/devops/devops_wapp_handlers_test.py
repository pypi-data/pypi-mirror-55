# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from unittest.mock import call

from _sadm.devops.wapp import handlers
from _sadm.devops.wapp.static import static
from _sadm.devops.wapp.view import index
from _sadm.devops.wapp.view.user import auth, user

def test_init(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		handlers._initdone = False
		handlers.init(ctx.wapp)
		assert ctx.wapp.route.mock_calls == [
			call(r'/static/<filename:re:.*\..*>', 'GET', static.serve,
				name = 'static', skip = ['sadm.devops.auth']),
			call('/', 'GET', index.handle, name = 'index', skip = []),

			call('/user/login', 'GET', auth.login,
				name = 'user.login', skip = ['sadm.devops.auth']),
			call('/user/login', 'POST', auth.loginPost,
				name = 'user.login_post', skip = ['sadm.devops.auth']),

			call('/user', 'GET', user.home, name = 'user', skip = []),
		]
