# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from datetime import datetime

from _sadm import version
from _sadm.devops.wapp.view import view
from _sadm.utils import path

__all__ = ['parse']

class Template(object):
	name = None
	__unset = object()

	def __init__(self, name, data):
		self.name = name
		self.data = data
		self.data.update({
			'sadm': {
				'version': version.string('sadm'),
			}
		})

	@property
	def error(self):
		return self.get('error')

	@property
	def now(self):
		return datetime.strftime(datetime.now().astimezone(), '%Y-%m-%d %H:%M:%S %z')

	@property
	def user(self):
		return self.get('user')

	@property
	def auth(self):
		return self.get('auth')

	@property
	def lang(self):
		return 'en'

	def __getitem__(self, name):
		return self.get(name)

	def get(self, name, default = __unset):
		val = self.data.get(name, self.__unset)
		if val is self.__unset:
			if default is self.__unset:
				raise KeyError("template %s: %s" % (self.name, name))
			else:
				return default
		return val

	def url(self, name, **kw):
		return view.url(name, **kw)

def parse(name, **data):
	fn = "%s.html" % path.join(*name.split('/'))
	return bottle.template(fn, tpl = Template(name, data))
