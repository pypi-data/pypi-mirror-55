#!/usr/bin/env bash
set -eu

NAME='sadmproxy'
IMAGE='jrmsdev/sadm:proxy'
ENVVARS='-e PYTHONPATH=/opt/src/sadm -e SADMTEST_LOG=debug'

docker run -it --rm --name=${NAME} --hostname=${NAME} --user sadm \
	-v ${PWD}/docker/proxy/nginx/sites-enabled:/etc/nginx/sites-enabled \
	-v ${PWD}/docker/proxy/certs:/etc/ssl/private \
	-v ${PWD}/docker/proxy/config:/etc/opt/sadm \
	-p 127.0.0.1:4333:443 -v ${PWD}:/opt/src/sadm ${ENVVARS} ${IMAGE} $@

exit 0
