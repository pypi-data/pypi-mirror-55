# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

from _sadm.devops.wapp import cfg
from _sadm.devops.wapp.static import static
from _sadm.devops.wapp.view import index, view
from _sadm.devops.wapp.view.user import auth, user

__all__ = ['url']

reg = (
	('static', {
		'route': r'/static/<filename:re:.*\..*>',
		'view': static.serve,
		'skip': ['sadm.devops.auth'],
		'url': '/static/{filename}',
	}),
	('index', {
		'route': '/',
		'view': index.handle,
	}),
	('user.login', {
		'route': '/user/login',
		'view': auth.login,
		'skip': ['sadm.devops.auth'],
	}),
	('user.login_post', {
		'route': '/user/login',
		'view': auth.loginPost,
		'method': 'POST',
		'skip': ['sadm.devops.auth'],
	}),
	('user', {
		'route': '/user',
		'view': user.home,
	}),
)

__idx = None
if __idx is None:
	__idx = {}
	for h in reg:
		name = h[0]
		opt = h[1]
		__idx[name] = opt

_urlbase = None

def url(view, **kw):
	global _urlbase
	if _urlbase is None:
		b = cfg.config.get('devops', 'url.base', fallback = '/')
		if b.endswith('/'):
			_urlbase = b[:-1]
		else:
			_urlbase = b
	opt = __idx.get(view, None)
	if opt is None:
		raise RuntimeError("invalid view name: %s" % view)
	u = opt.get('url', opt['route'])
	u = u.format(**kw)
	u = u.replace('/', '', 1)
	u = '/'.join([_urlbase, u])
	return u
