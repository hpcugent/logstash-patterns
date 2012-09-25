%define instdir %{?_datarootdir}%{!?_datarootdir:%{_datadir}}/grok

Name: logstash-patterns
Version: 0.1.0
Release: 1%{?dist}
Summary: GROK patterns for parsing the logs from different services.

License: Apache 2
URL: http://www.ugent.be/hpc
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description

Files containing patterns to parse different software services.

Some log entries have special formats for fields like dates. Here we
ship the patterns needed to give correct structure to shuch crappy
logs, and even more.

%prep
%setup -q

%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{instdir}
cp -r * $RPM_BUILD_ROOT/%{instdir}/

%files
%defattr(-,root,root,-)
%{instdir}/*



%changelog
* Tue Sep 11 2012 Luis Fernando Muñoz Mejías <munoz@Luis.Munoz@UGent.be> - 0.1.0-1
- Initial build.
