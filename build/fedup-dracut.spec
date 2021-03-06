%global dracutmoddir %{_prefix}/lib/dracut/modules.d
%global plymouthver 0.8.6

Name:       fedup-dracut
Version:    0.9.2
Release:    1%{?dist}
Summary:    The Fedora Upgrade tool initramfs environment

License:    GPLv2+
URL:        https://github.com/rhinstaller/fedup-dracut
Source0:    https://github.com/rhinstaller/%{name}/archive/%{version}.tar.gz
Source1:    throbber-korora.tar.gz

Summary:        initramfs environment for system upgrades
BuildRequires:  rpm-devel >= 4.10.0
BuildRequires:  plymouth-devel >= %{plymouthver}
BuildRequires:  glib2-devel
Requires:       rpm >= 4.10.0
Requires:       plymouth >= %{plymouthver}
Requires:       systemd >= 195-8
Requires:       dracut >= 025

%package plymouth
BuildRequires:  plymouth-devel
BuildArch:      noarch
Requires:       plymouth-plugin-two-step >= %{plymouthver}
Summary:        plymouth theme for system upgrade progress

%description
These dracut modules provide the framework for upgrades and the tool that
actually runs the upgrade itself.

%description plymouth
The plymouth theme used during system upgrade.


%prep
%setup -q

tar -xf %{SOURCE1} -C plymouth/

%build
make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT \
             LIBEXECDIR=%{_libexecdir} \
             DRACUTMODDIR=%{dracutmoddir}

%files
%doc README.asciidoc TODO.asciidoc COPYING makefeduprepo
%{_libexecdir}/system-upgrade-fedora
%{dracutmoddir}/85system-upgrade-fedora
%{dracutmoddir}/90system-upgrade

%files plymouth
%{_datadir}/plymouth/themes/fedup


%changelog
* Mon May 18 2015 Will Woods <wwoods@redhat.com> 0.9.2-1
- Fix reboot at end of upgrade (#1209941)

* Tue Feb 03 2015 Will Woods <wwoods@redhat.com> 0.9.0-2
- Don't write the entire system journal to upgrade.log (#1161366)
- Try to disable console blanking during upgrade (#1173135)

* Tue Oct 21 2014 Will Woods <wwoods@redhat.com> 0.9.0-1
- Use rpm's selinux plugin if available (#1146580)
- Fix racy LUKS unlock failure (#1044484)
- Enlongthen progress bar in fedup plymouth theme
- Other small progress fixes

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 10 2013 Will Woods <wwoods@redhat.com> 0.8.0-2
- Fix compatibility with fedup 0.7.x

* Wed Dec 4 2013 Will Woods <wwoods@redhat.com> 0.8.0-1
- Always put a shell on tty2
- Show text output from upgrade if graphics not available
- Fix --iso upgrades to F20 (#1024223)

* Mon Mar 18 2013 Will Woods <wwoods@redhat.com> 0.7.3-0
- Include 'makefeduprepo' script
- Fix plymouthd crash with encrypted /home (#896023)

* Wed Dec 05 2012 Will Woods <wwoods@redhat.com> 0.7.2-1
- Remove awful hack to forcibly sync data to disk (fixed in systemd 195-8)
- Clean up after upgrade finishes
- Fix progress screen and text output

* Thu Nov 15 2012 Will Woods <wwoods@redhat.com> 0.7.1-1
- install new kernel without removing old ones (#876366)

* Wed Nov 14 2012 Will Woods <wwoods@redhat.com> 0.7-2
- Awful hack to make journal work
- Send output to systemd journal
- Fix Requires: for fedup-dracut-plymouth
- Awful hack to make sure data gets written before reboot

* Thu Oct 25 2012 Will Woods <wwoods@redhat.com> 0.7-1
- Initial packaging
