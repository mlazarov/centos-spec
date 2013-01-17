%{!?__pecl:	%{expand: %%global __pecl	%{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name memcached

Name:		php-pecl-memcached
Version:	2.1.0
Release:	1%{?dist}
Summary:	PHP wrapper to memcachedb

Group:		Development/Tools
License:	PHP
URL:		http://memcachedb.org
Source0:	memcached-2.1.0.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	php-devel, libmemcached-devel > 1.0
BuildRequires:	php-pear
# Required by phpize
BuildRequires: autoconf, automake, libtool

Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Requires:	php-common

%description

This extension uses libmemcached library to provide API for
communicating with memcached

%prep
%setup -q -n memcached-%{version}

%build
phpize
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_ROOT=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/memcached.ini << 'EOF'
; enable memcached extension
extension="memcached.so"
EOF
# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pecl_xmldir}
install -m 644 ../package.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%clean
rm -rf $RPM_BUILD_ROOT

%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif

%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif

%{_sysconfdir}/php.d/memcached.ini
%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/memcached.ini
%{php_extdir}/memcached.so
%{pecl_xmldir}/%{name}.xml

%doc ChangeLog CREDITS LICENSE


%changelog
* Thu Jan 17 2013 Martin Lazarov <martin@lazarov.bg> 2.2.7
- Updating to version 2.2.7

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-4
- fix setup and package.xml install

* Mon Apr 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-3
- correct macros, add license to files

* Fri Apr 08 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-2
- correct package following pecl packaging guidelines

* Fri Mar 11 2011 Paul Whalen <paul.whalen@senecac.on.ca> 0.7.0-1
- Initial Packaging

