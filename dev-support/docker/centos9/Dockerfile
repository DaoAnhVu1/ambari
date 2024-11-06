FROM quay.io/centos/centos:stream9

RUN yum update -y

RUN yum -q -y install epel-release 

# RUN yum -q -y install "Development Tools"

RUN yum -q -y install \
    gcc \
    gcc-c++ \
    git \
    java-1.8.0-openjdk-devel \
    make \
    openssl \
    python \
    python-devel \
    python-setuptools \
    rpm-build \
    which \
    openssl-devel bzip2-devel libffi-devel \
    zlib-devel ncurses-devel readline-devel sqlite-devel

RUN yum -q -y install \
    python3.11\* --skip-broken --allowerasing

RUN yum clean all \
  && rm -rf /var/cache/yum

RUN curl -LSs -o /usr/local/bin/jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 \
  && chmod 755 /usr/local/bin/jq