Name:		dos2unix
Version:	7.3.4
Release:	1%{?dist}
Summary:	Text file format converter (unix2dos dos2unix)
Group:		Applications/Text
License:	BSD
URL:		http://waterlan.home.xs4all.nl/dos2unix.html
Source0:	http://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz

BuildRequires:	gcc make intltool gettext
Requires:	gettext

%description
dos2unix includes utilities to convert text files with DOS or MAC line breaks to Unix line breaks and vice versa. It also includes conversion of UTF-16 to UTF-8.

%prep
%setup -q


%build
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/dos2unix
%{_bindir}/unix2dos
%{_bindir}/mac2unix
%{_bindir}/unix2mac
%{_datadir}

%changelog
* Mon  Nov 7 2016 Martin Lazarov <martin@lazarov.bg> 7.3.4-1
 - Initial version of the spec package
