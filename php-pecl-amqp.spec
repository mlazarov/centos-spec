%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name amqp

%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}

Summary:      PHP AMQP client driver
Name:         php-pecl-amqp
Version:      0.3.1
Release:      2%{?dist}
License:      PHP License
Packager:     Martin Lazarov <martin@lazarov.bg>
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}

Source:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: php-devel >= 5.1.0
BuildRequires: php-pear >= 1.4.0

Requires(post): %{__pecl}
Requires(postun): %{__pecl}

%if 0%{?php_zend_api}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
%else
Requires:     php-api = %{php_apiver}
%endif

Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}


%description
This package provides an interface for communicating with the MongoDB database
in PHP.

%prep 
%setup -c -q
cd %{pecl_name}-%{version}


%build
cd %{pecl_name}-%{version}
phpize
%configure 
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

;  option documentation: http://www.php.net/manual/en/amqp.configuration.php

;  The host to which to connect.
;amqp.host = "localhost"

;  The virtual host to which to connect on the host.
;amqp.vhost = "/"

;  The port on which to connect.
;amqp.port = 5672

;  The login (username) used for authenticating against the host.
;amqp.login = "guest"

;  The password used for authenticating against the host.
;amqp.password = "gust"

EOF

# Install XML package description
%{__mkdir_p} %{buildroot}%{pecl_xmldir}
%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


%post
%if 0%{?pecl_install:1}
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%postun
%if 0%{?pecl_uninstall:1}
if [ "$1" -eq "0" ]; then
%{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
cd %{pecl_name}-%{version}
# only check if build extension can be loaded

%{_bindir}/php \
    -n -d extension_dir=modules \
    -d extension=%{pecl_name}.so \
    -i | grep "AMQP protocol version"


%files
%defattr(-, root, root, -)
#%doc %{pecl_name}-%{version}/README.md
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Tue Sep 27 2011 Martin Lazarov <martin@lazarov.bg> - 0.3.1-1
- Initial RPM
