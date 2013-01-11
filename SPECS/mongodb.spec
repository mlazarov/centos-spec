Name: mongodb
Version: 2.2.2
Release: 0%{?dist}
Summary: mongo client shell and tools
License: AGPL 3.0
URL: http://www.mongodb.org
Group: Applications/Databases

Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: js-devel, readline-devel, boost-devel, pcre-devel
BuildRequires: gcc-c++, scons

%description
Mongo (from "huMONGOus") is a schema-free document-oriented database.
It features dynamic profileable queries, full indexing, replication
and fail-over support, efficient storage of large binary data objects,
and auto-sharding.

This package provides the mongo shell, import/export tools, and other
client utilities.


#### Router
%package router
Summary: mongo server, sharding server, and support scripts
Group: Applications/Databases
Requires: mongodb

%description router
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo server software, mongo sharding server
softwware, default configuration files, and init.d scripts.


#### Shard #########
%package shard
Summary: mongo shard, sharding server, and support scripts
Group: Applications/Databases
Requires: mongodb

%description shard
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo server sharding software, mongo sharding server
software, default configuration files, and init.d scripts.

#### Config ########
%package config
Summary: Mongo config server 
Group: Applications/Databases
Requires: mongodb

%description config
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo static library and header files needed
to develop mongo client software.

##### Devel #######
%package devel
Summary: Headers and libraries for mongo development.
Group: Applications/Databases
Requires: mongodb

%description devel
MongoDB headers and libraries for mongo development


##### Arbiter #######
%package arbiter
Summary: Mongo arbiter server.
Group: Applications/Databases
Requires: mongodb

%description arbiter
Mongo (from "huMONGOus") is a schema-free document-oriented database.

This package provides the mongo arbiter server software and default 
configuration files required for mongo arbiter server, also and init.d scripts

%prep
%setup

%build
scons --prefix=$RPM_BUILD_ROOT/usr -j 8 all
# XXX really should have shared library here

%install
scons --prefix=$RPM_BUILD_ROOT/usr install
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
cp debian/*.1 $RPM_BUILD_ROOT/usr/share/man/man1/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p $RPM_BUILD_ROOT/var/lib/mongodb/
mkdir -p $RPM_BUILD_ROOT/var/log/mongodb/
mkdir -p $RPM_BUILD_ROOT/var/run/mongodb/

#%install router
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongodb-router $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-router
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-router
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongodb-router $RPM_BUILD_ROOT/etc/sysconfig/mongodb-router
cp /root/rpmbuild/SOURCES/mongodb/etc/mongodb-router.conf $RPM_BUILD_ROOT/etc/mongodb-router.conf
touch $RPM_BUILD_ROOT/var/log/mongodb/mongodb-router.log


#%install shard
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongodb-shard $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-shard
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-shard
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongodb-shard $RPM_BUILD_ROOT/etc/sysconfig/mongodb-shard
cp /root/rpmbuild/SOURCES/mongodb/etc/mongodb-shard.conf $RPM_BUILD_ROOT/etc/mongodb-shard.conf
touch $RPM_BUILD_ROOT/var/log/mongodb/mongodb-shard.log
mkdir -p $RPM_BUILD_ROOT/var/lib/mongodb/


#%install config
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongodb-config $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-config
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-config
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongodb-config $RPM_BUILD_ROOT/etc/sysconfig/mongodb-config
cp /root/rpmbuild/SOURCES/mongodb/etc/mongodb-config.conf $RPM_BUILD_ROOT/etc/mongodb-config.conf
touch $RPM_BUILD_ROOT/var/log/mongodb/mongodb-config.log
mkdir -p $RPM_BUILD_ROOT/var/lib/mongodb/configdb

#%install arbiter
cp /root/rpmbuild/SOURCES/mongodb/etc/rc.d/init.d/mongodb-arbiter $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-arbiter
chmod a+x $RPM_BUILD_ROOT/etc/rc.d/init.d/mongodb-arbiter
cp /root/rpmbuild/SOURCES/mongodb/etc/sysconfig/mongodb-arbiter $RPM_BUILD_ROOT/etc/sysconfig/mongodb-arbiter
cp /root/rpmbuild/SOURCES/mongodb/etc/mongodb-arbiter.conf $RPM_BUILD_ROOT/etc/mongodb-arbiter.conf
touch $RPM_BUILD_ROOT/var/log/mongodb/mongodb-arbiter.log
mkdir -p $RPM_BUILD_ROOT/var/lib/mongodb/arbiter

%clean
scons -c
rm -rf $RPM_BUILD_ROOT


#### All
%pre
if ! /usr/bin/id -g mongod &>/dev/null; then
    /usr/sbin/groupadd -r mongod
fi
if ! /usr/bin/id mongod &>/dev/null; then
    /usr/sbin/useradd -M -r -g mongod -d /var/lib/mongo -s /bin/false \
	-c mongod mongod > /dev/null 2>&1
fi

#############################
#### Router

%post router
if test $1 = 1
then
  /sbin/chkconfig --add mongodb-router
fi

%preun router
if test $1 = 0
then
  /sbin/chkconfig --del mongodb-router
fi

%postun router
if test $1 -ge 1
then
  /sbin/service mongodb-router condrestart >/dev/null 2>&1 || :
fi

#############################
#### Shard

%post shard
if test $1 = 1
then
  /sbin/chkconfig --add mongodb-shard
fi

%preun shard
if test $1 = 0
then
  /sbin/chkconfig --del mongodb-shard
fi

%postun shard
if test $1 -ge 1
then
  /sbin/service mongodb-shard condrestart >/dev/null 2>&1 || :
fi

#############################
#### Config

%post config
if test $1 = 1
then
  /sbin/chkconfig --add mongodb-config
fi

%preun config
if test $1 = 0
then
  /sbin/chkconfig --del mongodb-config
fi

%postun config
if test $1 -ge 1
then
  /sbin/service mongodb-config condrestart >/dev/null 2>&1 || :
fi


#############################
#### Arbiter

%post arbiter
if test $1 = 1
then
  /sbin/chkconfig --add mongodb-arbiter
fi

%preun arbiter
if test $1 = 0
then
  /sbin/chkconfig --del mongodb-arbiter
fi

%postun arbiter
if test $1 -ge 1
then
  /sbin/service mongodb-arbiter condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc README GNU-AGPL-3.0.txt

%{_bindir}/mongo
%{_bindir}/mongodump
%{_bindir}/mongoexport
%{_bindir}/mongofiles
%{_bindir}/mongoimport
%{_bindir}/mongorestore
%{_bindir}/mongostat
%{_bindir}/bsondump
%{_bindir}/mongotop
%{_bindir}/mongod
%{_bindir}/mongos
%{_bindir}/mongooplog
%{_bindir}/mongoperf

%{_mandir}/man1/mongo.1*
%{_mandir}/man1/mongod.1*
%{_mandir}/man1/mongodump.1*
%{_mandir}/man1/mongoexport.1*
%{_mandir}/man1/mongofiles.1*
%{_mandir}/man1/mongoimport.1*
%{_mandir}/man1/mongosniff.1*
%{_mandir}/man1/mongostat.1*
%{_mandir}/man1/mongorestore.1*
%{_mandir}/man1/bsondump.1*
%{_mandir}/man1/mongos.1*

%attr(0755,mongod,mongod) %dir /var/log/mongodb/
%attr(0755,mongod,mongod) %dir /var/run/mongodb/
%attr(0755,mongod,mongod) %dir /var/lib/mongodb/


%files router
%defattr(-,root,root,-)
%config(noreplace) /etc/mongodb-router.conf
/etc/rc.d/init.d/mongodb-router
/etc/sysconfig/mongodb-router
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongodb/mongodb-router.log


%files shard
%defattr(-,root,root,-)
%config(noreplace) /etc/mongodb-shard.conf
/etc/rc.d/init.d/mongodb-shard
/etc/sysconfig/mongodb-shard
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongodb/mongodb-shard.log


%files config
%defattr(-,root,root,-)
%config(noreplace) /etc/mongodb-config.conf
/etc/rc.d/init.d/mongodb-config
/etc/sysconfig/mongodb-config
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongodb/mongodb-config.log

%files devel
%defattr(-,root,root,-)
%attr(0755,mongod,mongod) %dir /usr/include/mongo/
/usr/include/mongo/*
/usr/lib/libmongoclient.a

%files arbiter
%defattr(-,root,root,-)
%config(noreplace) /etc/mongodb-arbiter.conf
/etc/rc.d/init.d/mongodb-arbiter
/etc/sysconfig/mongodb-arbiter
%attr(0640,mongod,mongod) %config(noreplace) %verify(not md5 size mtime) /var/log/mongodb/mongodb-arbiter.log


%changelog
* Fri Jan 01 2013 Martin Lazarov <martin@lazarov.bg>
- Adding arbiter package

* Tue Sep 11 2012 Martin Lazarov <martin@lazarov.bg>
- Updated mongodb version 2.2.0
- Added devel package

* Tue Jul 10 2012 Martin Lazarov <martin@lazarov.bg>
- Update mongodb version to 2.06

* Mon Jan 16 2012 Martin Lazarov <martin@lazarov.bg>
- removed devel & server packages and added router, shard and config packages

* Thu Jan 28 2010 Richard M Kreuter <richard@10gen.com>
- Minor fixes.

* Sat Oct 24 2009 Joe Miklojcik <jmiklojcik@shopwiki.com> - 
- Wrote mongo.spec.
