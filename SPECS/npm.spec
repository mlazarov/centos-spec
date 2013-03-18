Name:          npm
Version:       1.0.106
Release:       0%{?dist}
Summary:       A package manager for Node.js
Packager:      Martin Lazarov <martin@lazarov.bg>
Group:         Development/Libraries
License:       MIT License
URL:           http://npmjs.org/
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
Source0:       npm-%{version}.tgz
# Source http://search.npmjs.org/#/npm
BuildRequires: nodejs
Requires:      nodejs

%description
NPM is a package manager for Node.js.
You can use it to install and publish your node programs.
It manages dependencies and does other cool stuff.

%prep
%setup -q -c
install_module() {
    tar --transform "s|^package|node_modules/$1|g" --show-transformed -zxf $2
}

%build

%install
cd package
rm -rf $RPM_BUILD_ROOT
npm_config_prefix=$RPM_BUILD_ROOT/usr \
npm_config_root=$RPM_BUILD_ROOT/usr/lib/node \
npm_config_binroot=$RPM_BUILD_ROOT%{_bindir} \
npm_config_manroot=$RPM_BUILD_ROOT%{_mandir} \
node ./cli.js install -g

# workaround for automatically compresses manfile
custom_mandir_1=$RPM_BUILD_ROOT%{_mandir}/man1
rm -rf $RPM_BUILD_ROOT%{_mandir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
cp -rf $RPM_BUILD_ROOT/usr/lib/node_modules/npm/man/man1 $RPM_BUILD_ROOT%{_mandir}
cd ${custom_mandir_1}
for manfile in *; do mv -i $manfile `echo $manfile | sed 's/^/npm_/'`; done
mv npm_npm.1 npm.1

custom_mandir_3=$RPM_BUILD_ROOT%{_mandir}/man3
cp -rf $RPM_BUILD_ROOT/usr/lib/node_modules/npm/man/man3 $RPM_BUILD_ROOT%{_mandir}
cd ${custom_mandir_3}
for manfile in *; do mv -i $manfile `echo $manfile | sed 's/^/npm_/'`; done

%files
%defattr(-,root,root,-)
%{_prefix}/lib/node_modules/npm
%{_bindir}/npm*
%{_mandir}/man1/*
%{_mandir}/man3/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
# This section is the workaround does not work properly npm install.
/usr/bin/npm config set registry http://registry.npmjs.org/

%changelog
* Fri Dec 02 2011 Martin Lazarov <martin@lazarov.bg>
- Updated to npm version 1.0.116
* Mon Oct 17 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.99
* Fri Oct 14 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.96
* Thu Oct 13 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.95
* Thu Oct  6 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.94
* Tue Oct  4 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.93
* Tue Oct  4 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.92
* Tue Oct  4 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.91
* Mon Oct  3 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.90
* Sun Sep 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.30
* Thu Sep  1 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed manfile
* Fri Aug 26 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.27
* Thu Aug 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.26
* Wed Aug 17 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.25
* Mon Aug 15 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.24
- Added workaround does not work properly npm install
* Mon Aug  8 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to mpn version 1.0.23
* Fri Jul 29 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Initial version
