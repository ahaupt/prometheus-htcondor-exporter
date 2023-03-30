Summary: HTCondor exporter for Prometheus
Name: __NAME__
Version: __VERSION__
Release: 1
License: GPL
Group: DESY
URL: https://repo.zeuthen.desy.de/rpm/%{name}
BuildArch: noarch
Requires: condor
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: %{name}-%{version}.tar.gz

%define sbindir __SBINDIR__

%description
HTCondor exporter for Prometheus

%prep
%setup

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{sbindir}
for script in htcondor-exporter htcondor-exporter-daemon ; do
	sed -e 's@__sbindir__@%{sbindir}@' src/$script > %{buildroot}%{sbindir}/$script
done

mkdir -p %{buildroot}%{_unitdir}
for unit in htcondor-exporter ; do
	sed -e 's@__sbindir__@%{sbindir}@' src/${unit}.service > %{buildroot}%{_unitdir}/${unit}.service
done

%post

if [ $1 -eq 1 ] ; then 
	# Initial installation 
	systemctl preset htcondor-exporter.service >/dev/null 2>&1 || : 
fi

%preun

if [ $1 -eq 0 ] ; then 
	# Package removal, not upgrade 
	systemctl --no-reload disable htcondor-exporter.service > /dev/null 2>&1 || : 
	systemctl stop htcondor-exporter.service > /dev/null 2>&1 || : 
fi

%postun

systemctl daemon-reload >/dev/null 2>&1 || : 
if [ $1 -ge 1 ] ; then 
	# Package upgrade, not uninstall 
	systemctl try-restart htcondor-exporter.service >/dev/null 2>&1 || : 
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,-,-) %{sbindir}/*
%attr(0644,-,-) %{_unitdir}/*

%changelog
* Thu Mar 30 2023 <andreas.haupt@desy.de> - 1.1.1-1
- export node offline status
* Tue Mar 15 2022 <andreas.haupt@desy.de> - 1.1-3
- export ImageSize_RAW job metric
* Tue Mar  1 2022 <andreas.haupt@desy.de> - 1.1-2
- fix update of condor_slot_ metrics
* Wed Feb  2 2022 <andreas.haupt@desy.de> - 1.1-1
- export some job metrics
* Tue Feb  1 2022 <andreas.haupt@desy.de> - 1.0-3
- export gpu metrics
* Mon Jan  3 2022 <andreas.haupt@desy.de> - 1.0-2
- improve daemon logic
* Mon Mar 22 2021 <andreas.haupt@desy.de> - 1.0-1
- initial version
