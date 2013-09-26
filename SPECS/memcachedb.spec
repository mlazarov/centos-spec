Name:		memcachedb
Version:	1.2.1
Release:	1%{?dist}
Summary:	A distributed key-value storage system designed for persistent.

Group:		Applications/Databases
License:	New BSD License
URL:		http://memcachedb.org
Source0:	memcachedb-1.2.1.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	libevent-devel, db4-devel
# Requires:	

%description
MemcacheDB is a distributed key-value storage system designed for persistent. 
It is NOT a cache solution, but a persistent storage engine for fast and 
reliable key-value based object storage and retrieval. It conforms to 
memcache protocol(not completed, see below), so any memcached client can 
have connectivity with it. MemcacheDB uses Berkeley DB as a storing backend,
so lots of features including transaction and replication are supported.

%prep
%setup -q


%build
%configure --enable-threads
make %{?_smp_mflags}


%install


rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
cp /root/rpmbuild/SOURCES/memcachedb $RPM_BUILD_ROOT/etc/init.d/
cp tools/mcben.py $RPM_BUILD_ROOT/usr/bin/
cp tools/mdbtest.py $RPM_BUILD_ROOT/usr/bin/
cp tools/mdbtop.py $RPM_BUILD_ROOT/usr/bin/
%{__mkdir} -p "${RPM_BUILD_ROOT}/var/lib/memcachedb/"
%{__mkdir} -p "${RPM_BUILD_ROOT}/var/run/memcachedb/"



%clean
#rm -rf $RPM_BUILD_ROOT

%post
if test $1 = 1
then
  /sbin/chkconfig --add memcachedb
fi

%preun
if test $1 = 0
then
  /sbin/chkconfig --del memcachedb
fi

%postun
if test $1 -ge 1
then
  /sbin/service memcachedb condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
/usr/bin/memcachedb
/usr/bin/mcben.py
/usr/bin/mdbtest.py
/usr/bin/mdbtop.py
/etc/init.d/memcachedb
%attr(700,nobody,nobody)/var/lib/memcachedb/
%attr(700,nobody,nobody)/var/run/memcachedb/

%changelog
* Thu May 29 2012 Martin Lazarov <martin@lazarov.bg>
- Initial version of package


