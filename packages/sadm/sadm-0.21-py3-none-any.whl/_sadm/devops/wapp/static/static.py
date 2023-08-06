# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

import bottle

from os import path

from _sadm import libdir, log

__all__ = ['serve']

_rootdir = libdir.fpath('devops', 'wapp', 'static')
_serveExtension = {
	'.css': True,
	'.ico': True,
}

def serve(filename):
	filename = path.normpath(filename)
	ext = path.splitext(filename)[1]
	if ext == '' or filename.startswith('.') or \
		not _serveExtension.get(ext, False):
		log.warn("static file refuse %s" % filename)
		return bottle.HTTPError(404, "file not found")
	log.debug("serve %s" % filename)
	return bottle.static_file(filename, root = _rootdir)
