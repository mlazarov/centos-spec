Name:		ssdeep
Version:	2.10
Release:	1%{?dist}
Summary:	PHP tool for computing context triggered piecewise hashes (CTPH)
Group:		Development/Tools
License:	PHP
URL:		http://ssdeep.sourceforge.net
Source0:	ssdeep-2.10.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: autoconf, automake, libtool
BuildRequires: gcc-c++
BuildRequires: libstdc++-devel

%description
Computes a checksum based on context triggered piecewise hashes for
each input file. If requested, the program matches those checksums
against a file of known checksums and reports any possible matches.
Output is written to standard out and errors to standard error.
Input from standard input is not supported.

%prep
%setup -q -n ssdeep-%{version}

%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING FILEFORMAT INSTALL NEWS README TODO
%doc %{_mandir}/man1/ssdeep.1*
%{_bindir}/ssdeep
%{_includedir}/fuzzy.h
%{_libdir}/libfuzzy.*

%changelog
* Thu Oct 01 2013 Martin Lazarov <martin@lazarov.bg> 2.10
- Initial version - 2.10


