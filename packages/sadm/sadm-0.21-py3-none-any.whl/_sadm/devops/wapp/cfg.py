# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from configparser import ConfigParser, ExtendedInterpolation
from configparser import Error as ParserError

__all__ = ['config', 'new']

class Config(ConfigParser):
	_unset = object()

	def __init__(self):
		super().__init__(
			defaults = None,
			allow_no_value = False,
			delimiters = ('=',),
			comment_prefixes = ('#',),
			strict = True,
			interpolation = ExtendedInterpolation(),
			default_section = 'default',
		)

	def getlist(self, section, option, fallback = _unset):
		try:
			if fallback is self._unset:
				s = super().get(section, option)
			else:
				s = super().get(section, option, fallback = None)
				if s is None:
					return fallback
		except ParserError as err:
			raise SettingsError(str(err))
		l = deque()
		for val in s.split():
			val = val.strip()
			for val2 in val.split(','):
				val2 = val2.strip()
				if val2 != '':
					l.append(val2)
		return tuple(l)

config = None

def new(fn):
	global config
	config = Config()
	with open(fn, 'r') as fh:
		config.read_file(fh)
	if not config.has_section('devops'):
		config.add_section('devops')
	return config
