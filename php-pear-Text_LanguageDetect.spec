# $Revision: 1.20 $, $Date: 2012/03/25 20:40:03 $
%define		status		alpha
%define		pearname	Text_LanguageDetect
%include	/usr/lib/rpm/macros.php
Summary:	%{pearname} - language detection class
Name:		php-pear-Text-LanguageDetect
Version:	0.3.0
Release:	1
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/%{pearname}-%{version}.tgz
# Source0-md5:	efa27a43517533d653d4bc7074b15f18
URL:		http://pear.php.net/package/Text_LanguageDetect/
#BuildRequires:	php-pear-PEAR
#BuildRequires:	rpm-php-pearprov >= 4.4.2-11
#BuildRequires:	rpmbuild(macros) >= 1.580
Requires:	php-common >= 5.3.1
Requires:	php-pcre
Requires:	php-pear
#Suggests:	php-mbstring
Obsoletes:	php-pear-Text_LanguageDetect-tests
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Text_LanguageDetect can identify 52 human languages from text samples
and return confidence scores for each.

In PEAR status of this package is: %{status}.

%prep

%setup -q -c

#%patch0

cd %{pearname}-%{version}
# Package is V2
mv ../package.xml %{name}.xml


%build
cd %{pearname}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pearname}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml


# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}



%files
%defattr(644,root,root,755)
%doc %{php_pear_dir}/doc/
%dir %{php_pear_dir}/Text/LanguageDetect
%{php_pear_dir}/Text/LanguageDetect.php
%{php_pear_dir}/Text/LanguageDetect/Exception.php
%{php_pear_dir}/Text/LanguageDetect/ISO639.php
%{php_pear_dir}/Text/LanguageDetect/Parser.php
%{php_pear_dir}/data/Text_LanguageDetect
%exclude %{php_pear_dir}/test/
%exclude %{php_pear_dir}/.pkgxml/




%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)

%changelog

* Wed Jan 18 2012 Martin Lazarov <martin@lazarov.bg>  -  0.3.0-1
 - Initial version
