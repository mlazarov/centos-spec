Summary: Gearman Server and C Library
Name: gearmand
Version: 1.1.2
Release: 2
License: BSD
Group: System Environment/Libraries
BuildRequires: make,gcc-c++,bison, bison-devel, libevent-devel, mysql-devel, libmemcached-devel
URL: http://launchpad.net/gearmand
Requires: sqlite, libevent >= 1.4, boost-program-options >=  1.39

Packager: Brian Aker <brian@tangent.org>

Source: http://launchpad.net/gearmand/trunk/%{version}/+download/gearmand-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the client utilities.

%package server
Summary: Gearmand Server
Group: Applications/Databases
Requires: sqlite, libevent >= 1.4, boost-program-options >=  1.39

%description server
Gearman provides a generic framework to farm out work to other machines, dispatching function calls to machines that are better suited to do work, to do work in parallel, to load balance processing, or to call functions between languages.

This package provides the Gearmand Server.

%package devel
Summary: Header files and development libraries for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}. If you like to develop programs using %{name}, 
you will need to install %{name}-devel.

%prep
%setup -q

%configure --disable-libpq --disable-libtokyocabinet --disable-libdrizzle --disable-libmemcached --enable-jobserver=no


%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install  DESTDIR="%{buildroot}" AM_INSTALL_PROGRAM_FLAGS=""
mkdir -p $RPM_BUILD_ROOT/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/var/log/gearmand
mkdir -p $RPM_BUILD_ROOT/var/run/gearmand
install -m 755 /root/rpmbuild/SOURCES/gearman/gearmand.init $RPM_BUILD_ROOT/etc/rc.d/init.d/gearmand

%check

%clean
%{__rm} -rf %{buildroot}

%pre server
if ! /usr/bin/id -g gearmand &>/dev/null; then
    /usr/sbin/groupadd -r gearmand
fi
if ! /usr/bin/id gearmand &>/dev/null; then
    /usr/sbin/useradd -M -r -g gearmand -d /var/lib/gearmand -s /bin/false \
	-c "Gearman Server" gearmand > /dev/null 2>&1
fi

%post server
if test $1 = 1
then
  /sbin/chkconfig --add gearmand
fi

%preun server
if test $1 = 0
then
  /sbin/chkconfig --del gearmand
fi

%postun server
if test $1 -ge 1
then
  /sbin/service gearmand condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_bindir}/gearadmin
%{_bindir}/gearman
%{_libdir}/libgearman.la
%{_libdir}/libgearman.so.8
%{_libdir}/libgearman.so.8.0.0
#%{_mandir}/man1/gearadmin.1.gz
#%{_mandir}/man1/gearman.1.gz

%files server
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
#%{_mandir}/man8/gearmand.8.gz
%{_sbindir}/gearmand
/etc/rc.d/init.d/gearmand
%attr(0755,gearmand,gearmand) %dir /var/log/gearmand
%attr(0755,gearmand,gearmand) %dir /var/run/gearmand

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README HACKING THANKS
%{_includedir}/libgearman/gearman.h
%{_includedir}/libgearman-1.0/*.h
%{_libdir}/pkgconfig/gearmand.pc
%{_libdir}/libgearman.so
#{_mandir}/man3/*.3.gz


%changelog
* Wed Oct 17 2012 Martin Lazarov <martin@lazarov.bg> - 1.1.2
* Wed Jan 07 2009 Brian Aker <brian@tangent.org> - 0.1-1
- Initial package
