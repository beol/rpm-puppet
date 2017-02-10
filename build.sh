#!/bin/env bash

set -ev
export PATH="${HOME}/.gem/ruby/2.1.0/bin:/opt/ruby21/bin:${PATH}"

BASE_DIR="$(dirname $0)"

cd $BASE_DIR

spectool -g -R puppet.spec

gem install rpmbuild/SOURCES/bundler-1.13.7.gem --local --no-document --user-install

cp -p Gemfile Gemfile.lock rpmbuild/SOURCES/

rpmbuild -bb puppet.spec

[[ -n "${GPG_PASSPHRASE}" ]] && find ${BASE_DIR}/rpmbuild/RPMS -type f -name "*.rpm" | xargs -I{} sh -c "${BASE_DIR}/rpm-sign.exp {} && rpm --checksig {}"
