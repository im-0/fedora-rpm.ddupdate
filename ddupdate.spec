%global __python __python3

%global gittag      0.6.5
#global commit      eb302484417d85cbf497958ba2a651f738ad7420

%global shortcommit %{?commit:%(c=%{commit}; echo ${c:0:7})}%{!?commit:%nil}
%global shortdir    %{?gittag}%{?shortcommit}
%global srcdir      %{?gittag}%{?commit}

# mageia 6- fix:
%{!?_userunitdir: %global _userunitdir /usr/lib/systemd/system}

#Suse fix:
%{!?python3_pkgversion:%global python3_pkgversion 3}

Name:           ddupdate
Version:        0.6.5
Release:        4%{?dist}
Summary:        Tool updating DNS data for dynamic IP addresses

Group:          Applications/System
License:        MIT
URL:            http://github.com/leamas/ddupdate
BuildArch:      noarch
Source0:        %{url}/archive/%{srcdir}/%{name}-%{shortdir}.tar.gz

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  systemd
BuildRequires:  /usr/bin/pkg-config

Requires:       python%{python3_pkgversion}-requests
Requires:       /usr/sbin/ip
Requires:       sudo

%{?systemd_requires}

%description

A tool to update dynamic IP addresses typically obtained using DHCP
with dynamic DNS services such as changeip.com, duckdns.org or no-ip.com.
It makes it  possible to access a machine with a fixed name like
myhost.duckdns.org even if the ip address changes. ddupdate caches the
address, and only attempts the update if the address actually is changed.

The tool has a plugin structure with plugins for obtaining the actual
address (typically hardware-dependent) and to update it (service depen‐
dent). For supported services, it's a linux-centric, user-friendly and
flexible alternative to the ubiquitous ddclient.

ddupdate is distributed with systemd support to run at regular intervals,
and with NetworkManager templates to run when interfaces goes up or down.


%prep
%autosetup -p1 -n %{name}-%{srcdir}
sed -i '/ExecStart/s|/usr/local|/usr|' systemd/ddupdate.service
sed -i 's|/lib/systemd/system|%{_unitdir}|' setup.py
sed -i '/cmdclass=/s/^/#/' setup.py


%build
%py3_build


%install
%py3_install
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/ddupdate/plugins


%files
%license LICENSE.txt
%doc README.md NEWS CONTRIBUTE.md CONFIGURATION.md
%{_bindir}/ddupdate
%{_bindir}/ddupdate-config
%{_userunitdir}/ddupdate*
%{_datadir}/ddupdate
%{_datadir}/bash-completion/completions/ddupdate
%{_mandir}/man8/ddupdate.8*
%{_mandir}/man8/ddupdate-config.8*
%{_mandir}/man5/ddupdate.conf.5*
%{python3_sitelib}/*


%changelog
* Thu Feb 18 2021 Ivan Mironov <mironov.ivan@gmail.com> - 0.6.5-4
- Add python*-requests which is required for Cloudflare plugin

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 12 2020 Alec Leamas <leamas.alec@nowhere.net> - 0.6.5-1
- New upstream version
- Some attempts to make it build on opensuse.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-6
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Alec Leamas <leamas.alec@gmail.com> - 0.6.4-1
- New upstream version
- Move systemd files: systemd/system -> systemd/user

* Mon Jun 17 2019 Alec Leamas <leamas.alec@gmail.com> - 0.6.3-1
- New upstream version
- Fixes upstream #21, ipv6 config file parsing bug.

* Tue Apr 09 2019 Alec Leamas <leamas.alec@gmail.com> - 0.6.2-1
- new version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-2
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Alec Leamas <leamas.alec@gmail.com> - 0.6.1-1
- New upstream maintenance release.

* Sun Feb 18 2018 Alec Leamas <leamas.alec@gmail.com> - 0.6.0-2
- Drop redundant R: python3-straight-plugin

* Sun Feb 18 2018 Alec Leamas <leamas.alec@gmail.com> - 0.6.0-1
- New upstream version.
- Drop support for system-wide services.
- New BR pkg-config.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
§
* Sun Jan 28 2018 Alec Leamas <leamas.alec@gmail.com> - 0.5.2-1
- New upstream release

* Sat Jan 13 2018 Alec Leamas <leamas.alec@gmail.com> - 0.2.0-1
- New upstream release.

* Mon Jan 08 2018 Alec Leamas <leamas.alec@gmail.com> - 0.1.0-3
- Review remarks: Use %%{_unitdir}, %%py3_install, skip debug_package nil

* Sun Jan 07 2018 Alec Leamas <leamas.alec@gmail.com> - 0.1.0-2
- Fix unpackaged document file.

* Sun Jan 07 2018 Alec Leamas <leamas.alec@gmail.com> - 0.1.0-1
- New upstream release

* Thu Jan 04 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.6-3
- NetworkManager support patch, from upstream

* Thu Jan 04 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.6-2
- Fix epel-7 build error

* Wed Jan 03 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.6-1
- New upstream release.

* Wed Jan 03 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.5-0.6.eb30248
- rebuilt

* Tue Jan 02 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.5-0.5.rc2
- Published on COPR.
- Fix version-release
- Fix python version references.

* Tue Jan 02 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.5rc2-0.4
- New upstream release

* Tue Jan 02 2018 Alec Leamas <leamas.alec@gmail.com> - 0.0.5rc1-0.1
- New upstream release

* Fri Dec 29 2017 Alec Leamas <leamas.alec@gmail.com> - 0.0.2-0.2
- New upstream release, initial install testing done.

* Tue Dec 26 2017 Alec Leamas <leamas.alec@gmail.com> - 0.1-0.1.95f9fd8%{?dist}
- Initial release
