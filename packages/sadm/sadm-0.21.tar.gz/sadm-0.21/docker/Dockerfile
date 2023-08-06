FROM debian:buster-slim

LABEL maintainer="Jeremías Casteglione <jrmsdev@gmail.com>"
LABEL version="19.08.21"

USER root:root
WORKDIR /root

ENV DEBIAN_FRONTEND noninteractive
ENV APT_INSTALL sudo python3 python3-pip at uwsgi-plugin-python3 ssl-cert

RUN apt-get clean && \
	apt-get update && \
	apt-get dist-upgrade -y --purge && \
	apt-get install -y --no-install-recommends ${APT_INSTALL} && \
	apt-get clean && \
	apt-get autoremove -y --purge && \
	rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb /var/cache/apt/*cache.bin

RUN printf 'sadm\tALL=NOPASSWD: ALL\n' >/etc/sudoers.d/sadm
RUN chmod 440 /etc/sudoers.d/sadm

ARG SADM_UID=1000
ARG SADM_GID=1000

RUN groupadd -g ${SADM_GID} sadm
RUN useradd -c sadm -m -d /home/sadm -s /bin/bash -g ${SADM_GID} -u ${SADM_UID} sadm
RUN adduser sadm staff
RUN adduser sadm ssl-cert

RUN chgrp -v staff /usr/local/bin
RUN chmod -v g+ws /usr/local/bin

RUN mkdir -p /opt/src/sadm /opt/sadm /etc/opt/sadm

RUN chown -v sadm:sadm /opt/src/sadm /opt/sadm /etc/opt/sadm
RUN chmod -v 750 /opt/src/sadm /opt/sadm /etc/opt/sadm

COPY --chown=sadm:sadm requirements.txt /tmp
RUN sudo -u sadm pip3 install --system -r /tmp/requirements.txt

RUN rm -rf /root/.cache/pip
RUN rm -rf /home/sadm/.cache/pip
RUN rm -f /tmp/requirements.txt

USER sadm:sadm
WORKDIR /opt/src/sadm

CMD /bin/bash -i -l
