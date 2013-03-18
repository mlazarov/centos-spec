%define _base node

Name: %{_base}js
Version: 0.6.14
Release: 0%{?dist}
Summary: Evented I/O for V8 Javascript.
Packager: Martin Lazarov <martin@lazarov.bg>
Vendor: http://nodejs.org
Group: Development/Libraries
License: MIT License
URL: http://nodejs.org/
Source0: %{_base}-v%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: nodejs npm


BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
%setup -q -n %{_base}-v%{version}


%build
./configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_includedir}/node
%{_includedir}/node/*.h
%{_includedir}/node/c-ares/*.h
%{_includedir}/node/uv-private/*.h
#%{_includedir}/node/ev/*.h
#%{_prefix}/lib/pkgconfig/nodejs.pc
%attr(755,root,root) %{_bindir}/node
%attr(755,root,root) %{_bindir}/node-waf
%attr(755,root,root) %{_bindir}/npm
%dir %{_prefix}/lib/node
%dir %{_prefix}/lib/node/wafadmin
%dir %{_prefix}/lib/node/wafadmin/Tools
%{_prefix}/lib/node/wafadmin/*
%{_prefix}/lib/node_modules/npm
%{_mandir}/man1/*

%doc
/usr/share/man/man1/node.1.gz


%changelog
* Thu Apr 05 2012 - martin@lazarov.bg 0.6.14
* Fri Dec 02 2011 - martin@lazarov.bg 0.6.4
- nodejs version update v0.6.4
- spec file update
* Fri Sep 16 2011 - martin@lazarov.bg 0.4.12
* Thu Aug 18 2011 - martin@lazarov.bg 0.4.11
* Mon Jul 25 2011 - martin@lazarov.bg 0.4.10
- Initial version
