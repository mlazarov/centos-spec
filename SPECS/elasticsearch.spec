Name:		elasticsearch
Version:	1.0
Release:	1%{?dist}
Summary:	Elasticsearch is a distributed, highly available, RESTful search engine
Group:		Duvamis
License:	GPL
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	java-1.7.0-openjdk

%description
Elasticsearch is a distributed, highly available, RESTful search engine
# /root/rpmbuild/SOURCES/jodconverter-2.2.2/lib/

%prep
rm -rf %{buildroot}
mkdir %{buildroot}
mkdir -p %{buildroot}/opt/elasticsearch/

%install
cp -r /root/rpmbuild/SOURCES/elasticsearch/ %{buildroot}/opt/

%post
if [ $1 == 1 ]; then
    /opt/elasticsearch/bin/service/elasticsearch install > /dev/null 2>&1
fi

%preun
if [ $1 = 0 ]; then
    /opt/elasticsearch/bin/service/elasticsearch remove > /dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/elasticsearch/*

%changelog
* Mon Dec 10 2012 Martin Lazarov <martin@lazarov.bg>
- Initial version
