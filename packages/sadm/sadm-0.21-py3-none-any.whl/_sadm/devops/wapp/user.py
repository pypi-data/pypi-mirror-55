# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm import log

__all__ = ['WebappUser', 'userOptions']

userOptions = {
	'email': True,
}

class WebappUser(object):
	name = None

	def __init__(self, name, sess = None, info = None):
		self.name = name
		self._sess = sess
		self._info = info

	@property
	def sess(self):
		return self._sess

	@property
	def email(self):
		return self._info.get('email', None)
