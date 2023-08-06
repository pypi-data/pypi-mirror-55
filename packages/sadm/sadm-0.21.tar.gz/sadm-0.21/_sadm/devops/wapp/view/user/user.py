# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.devops.wapp.tpl import tpl

__all__ = ['home']

def home(user):
	return tpl.parse('user/home', user = user)
