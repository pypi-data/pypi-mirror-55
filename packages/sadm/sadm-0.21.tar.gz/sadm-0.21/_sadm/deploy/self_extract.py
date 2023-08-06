#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

# sadm.env self extractor
# https://pypi.org/project/sadm/

import sys

from base64 import b64decode
from os import path, makedirs, chmod, unlink
from subprocess import call

_cargo = {}
_vars = {}

def main():
	env = _vars['env']
	rootdir = _vars['rootdir']
	dstdir = path.join(rootdir, 'env')
	extract(dstdir)
	envfn = path.join(dstdir, "%s.env" % env)
	envcmd = path.join(rootdir, 'bin', 'sadm')
	rc = call("%s import %s" % (envcmd, envfn), shell = True)
	if rc != 0:
		return rc
	rc = call("%s --env %s deploy" % (envcmd, env), shell = True)
	if rc != 0:
		return rc
	return 0

def extract(dstdir):
	makedirs(dstdir, exist_ok = True)
	chmod(dstdir, 0o700)
	for fn, data in _cargo.items():
		fn = path.join(dstdir, fn)
		if path.isfile(fn):
			unlink(fn)
		with open(fn, 'wb') as fh:
			fh.write(b64decode(data.encode()))

if __name__ == '__main__':
	sys.exit(main()) # pragma: no cover
