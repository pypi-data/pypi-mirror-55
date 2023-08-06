# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.devops.wapp.view.user import user

def test_home(devops_wapp):
	wapp = devops_wapp()
	with wapp.mock() as ctx:
		u = object()
		user.home(user = u)
		ctx.tpl.parse.assert_called_with('user/home', user = u)
