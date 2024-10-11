FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8

RUN apt-get update && apt-get --no-install-recommends -y install \
    locales \
    sudo mc wget \
    netbase iproute2 iputils-ping isc-dhcp-client \
    python3 python3-distutils python3-apt pip \
    pciutils kmod strace \
    && apt-get -y clean && apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

RUN pip install pyyaml

RUN locale-gen en_US.UTF-8

ADD ./trex-bin /server
WORKDIR /server

ADD ./trex-starter ./trex-starter

COPY ./docker-runner.sh ./docker-runner.sh
RUN chmod +x ./docker-runner.sh

EXPOSE 4507
EXPOSE 4500
EXPOSE 4501

CMD ./docker-runner.sh
