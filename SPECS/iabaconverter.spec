Name:		iabaconverter
Version:	1.0
Release:	8%{?dist}
Summary:	Iabaconverter uses JODConverter to automates conversions between office document formats using OpenOffice.org
License:	GPL
URL:		http://sourceforge.net/projects/jodconverter/
Source0:	jodconverter-2.2.2.zip
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	libreoffice-headless, libreoffice-calc, libreoffice-draw, libreoffice-impress, libreoffice-writer

%description
Iabaconverter uses JODConverter to automates conversions between office document formats using OpenOffice.org. 
Supported formats include OpenDocument, PDF, RTF, Word, Excel, PowerPoint, and Flash. 
It can be used as a Java library, a command line tool, or a Web application.

# /root/rpmbuild/SOURCES/jodconverter-2.2.2/lib/

%prep
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}/opt/jodconverter/
mkdir -p %{buildroot}/etc/init.d/
mkdir -p %{buildroot}/usr/bin/

%install
cp -R /root/rpmbuild/SOURCES/jodconverter-2.2.2/lib/ %{buildroot}/opt/jodconverter/
cp /root/rpmbuild/SOURCES/libreoffice-headless %{buildroot}/etc/init.d/
cp /root/rpmbuild/SOURCES/iabaconverter %{buildroot}/usr/bin/

%post
if [ $1 == 1 ]; then
    /sbin/chkconfig --add libreoffice-headless
fi

%preun
if [ $1 = 0 ]; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del libreoffice-headless
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/jodconverter/*
/etc/init.d/libreoffice-headless
/usr/bin/iabaconverter

%changelog
* Mon Dec 10 2012 Martin Lazarov <martin@lazarov.bg>
- Initial version
