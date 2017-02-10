%global _name   puppet
%global _ver    3.8.7
%global _xver   %(echo %{_ver} | cut -d. -f1,2)
%global _prefix /opt/%{name}

Name: 		%{_name}%(echo %{_xver} | sed 's,\.,,')
Version: 	%{_ver}
Release: 	0a%{?dist}
Summary:  	An interpreter of object-oriented scripting language
License: 	ASL 2.0
Group: 		Development/Languages
URL:    	https://puppet.com/
Source0: 	Gemfile
Source1: 	Gemfile.lock
Source2: 	https://rubygems.org/downloads/puppet-3.8.7.gem
Source3: 	https://rubygems.org/downloads/CFPropertyList-2.2.8.gem
Source4: 	https://rubygems.org/downloads/facter-2.4.6.gem
Source5: 	https://rubygems.org/downloads/hiera-1.3.4.gem
Source6: 	https://rubygems.org/downloads/json_pure-2.0.3.gem
Source7: 	https://rubygems.org/downloads/bundler-1.13.7.gem
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

Requires:	ruby21
Provides:   puppet = %{_xver}

%description
Puppet

%prep 
%setup -n %{_name}-%{version} -c -T
mkdir -p vendor/cache
cp -p %{SOURCE0} %{SOURCE1} .
cp -p %{_sourcedir}/*.gem vendor/cache

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}
bundle install --binstubs ${RPM_BUILD_ROOT}%{_prefix}/bin --path ${RPM_BUILD_ROOT}%{_prefix}/lib --standalone --local

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/lib/ruby/2.1.0/gems/puppet-3.8.7/ext $RPM_BUILD_ROOT%{_datadir}/puppet-3.8.7
mv $RPM_BUILD_ROOT%{_prefix}/lib/ruby/2.1.0/gems/facter-2.4.6/ext $RPM_BUILD_ROOT%{_datadir}/facter-2.4.6
mv $RPM_BUILD_ROOT%{_prefix}/lib/ruby/2.1.0/gems/json_pure-2.0.3/ext $RPM_BUILD_ROOT%{_datadir}/json_pure-2.0.3
rm -rf $RPM_BUILD_ROOT%{_datadir}/**/{debian,freebsd,gentoo,ips,osx,solaris,suse,windows}

find $RPM_BUILD_ROOT%{_prefix} -type f | xargs sed -i "s,^#!/usr/bin/env ruby$,#!/opt/ruby21/bin/ruby,"
find $RPM_BUILD_ROOT%{_prefix} -type f | xargs sed -i "s,^#!/usr/bin/ruby$,#!/opt/ruby21/bin/ruby,"

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/puppet
mv $RPM_BUILD_ROOT%{_datadir}/puppet-3.8.7/redhat/puppet.conf $RPM_BUILD_ROOT%{_sysconfdir}/puppet/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}
%{_sysconfdir}/puppet/puppet.conf

