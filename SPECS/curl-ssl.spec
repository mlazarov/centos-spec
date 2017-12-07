%define name curl
%define tarball curl
%define version 7.57.0
%define release 2

%define curlroot %{_builddir}/%{tarball}-%{version}

Summary: get a file from an FTP or HTTP server.
Name: %{name}
Version: %{version}
Release: %{release}
Vendor: Daniel Stenberg <Daniel.Stenberg@haxx.se>
License: OpenSource
Packager: Troy Engel <tengel@sonic.net>
Group: Utilities/Console
Source: %{tarball}-%{version}.tar.gz
URL: https://curl.haxx.se/
Provides: curl
BuildRoot: %{_tmppath}/%{tarball}-%{version}-root
Requires: openssl >= 0.9.5
AutoReqProv: no

%description
curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

%package	devel
Summary:	The includes, libs, and man pages to develop with libcurl
Group:		Development/Libraries
Requires:	openssl-devel >= 0.9.5
Provides:	curl-devel

%description devel
libcurl is the core engine of curl; this packages contains all the libs,
headers, and manual pages to develop applications using libcurl.


%package -n libcurl
Summary: A library for getting files from web servers
Group: Development/Libraries
Requires: libssh2%{?_isa} >= %{libssh2_version}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.



%prep

%setup -q -n %{tarball}-%{version}

%build
cd %{curlroot} && (if [ -f configure.in ]; then mv -f configure.in configure.in.rpm; fi)
%configure
cd %{curlroot} && (if [ -f configure.in.rpm ]; then mv -f configure.in.rpm configure.in; fi)
make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} install-strip

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "%{curlroot}" != "/" ] && rm -rf %{curlroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/curl.1*
#%attr(0644,root,root) %{_mandir}/man1/mk-ca-bundle.1
#%{_libdir}/libcurl.so*
#%{_datadir}/curl/curl-ca-bundle.crt
%doc CHANGES COPYING README docs/BUGS
%doc docs/FAQ docs/FEATURES docs/INSTALL
%doc docs/KNOWN_BUGS docs/MANUAL docs/RESOURCES docs/THANKS
%doc docs/TODO docs/VERSIONS docs/TheArtOfHttpScripting tests

%files devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl-config
%attr(0644,root,root) %{_mandir}/man1/curl-config.1*
%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_includedir}/curl/*
%{_libdir}/libcurl.a
%{_libdir}/libcurl.la
%{_libdir}/pkgconfig/libcurl.pc
/usr/share/aclocal/libcurl.m4

%files -n libcurl
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libcurl.so*
