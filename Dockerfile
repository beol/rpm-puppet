FROM centos:centos6
MAINTAINER Leo Laksmana <beol@laksmana.com>

COPY RPM-GPG-KEY-laksmana /etc/pki/rpm-gpg/RPM-GPG-KEY-laksmana
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-laksmana

COPY laksmana_centos.repo /etc/yum.repos.d/laksmana_centos.repo
#RUN curl -s https://packagecloud.io/install/repositories/laksmana/centos/script.rpm.sh | bash

RUN yum clean all \
    && \
    yum install -y \
    rpm-build \
    rpmdevtools \
    ruby21 \
    vim-enhanced \
    && \
    yum clean all

RUN useradd -m -u 1000 rpmbuild

WORKDIR /home/rpmbuild
USER rpmbuild
COPY .rpmmacros .
