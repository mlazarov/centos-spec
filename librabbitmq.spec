Name:		librabbitmq
Version:	0.9.1
Release:	1%{?dist}
Summary:	RabbitMQ C client libraries (EXPERIMENTAL)
Packager:       Martin Lazarov <martin@lazarov.bg>
Group:		Development/Libraries
License:	GPL-2.0
URL:		http://hg.rabbitmq.com/rabbitmq-c/
Source0:	librabbitmq-0.9.1.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	make autoconf libtool
#Requires:	

%description
RabbitMQ C client libraries (EXPERIMENTAL)

%prep
%setup -q


%build
autoreconf -i
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/include/amqp*
/usr/lib64/librabbitmq.*


%changelog
%changelog
* Tue Sep 27 2011 Martin Lazarov <martin@lazarov.bg> - 0.9.1-1
- Initial RPM

