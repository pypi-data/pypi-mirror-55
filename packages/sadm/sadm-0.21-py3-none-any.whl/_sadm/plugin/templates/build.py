# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from string import Template

from _sadm.errors import PluginError
from _sadm.utils import builddir

__all__ = ['build']

def build(env):
	for x in env.session.get('templates.build', []):
		name = x[0]
		src = x[1]
		dst = x[2]
		attr = x[3]
		args = x[4]
		_parse(env, name, src, dst, attr, args)

def _parse(env, name, src, dst, attr, args):
	env.log("parse %s: src=%s dst=%s" % (name, src, dst))
	with env.assets.open(src) as srcfh:
		tpl = Template(srcfh.read())
		with builddir.create(env, dst, **attr) as dstfh:
			try:
				dstfh.write(tpl.substitute(args))
			except KeyError as err:
				raise PluginError("template %s key miss: %s" % (name, err))
