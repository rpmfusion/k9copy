
Name:    k9copy
Version: 3.0.3
Release: 1%{?dist}
Summary: Video DVD backup and creation program
Group:   Applications/Multimedia
License: GPLv2+
URL:     http://k9copy-reloaded.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}-reloaded/%{name}-%{version}.tar.gz

#Patch01: FindAv-compat.patch
Patch02: unbundled_dvdread_dvdnav.patch
# upstreamable patches
Patch52: k9copy-mimetype.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-devel
BuildRequires: gettext
%if 0%{?fedora} && 0%{?fedora} < 16
BuildRequires: hal-devel
%endif
BuildRequires: kdelibs4-devel
BuildRequires: libdvdread-devel libdvdnav-devel
BuildRequires: libmpeg2-devel
BuildRequires: pkgconfig
BuildRequires: xine-lib-devel

%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
Requires: dvd+rw-tools
Requires: dvdauthor

# Optional, not *strictly* required:
Requires: mencoder
Requires: mplayer

%description
Video DVD backup and creation program, features include:
* Video stream compression for fit onto a single layer 4.7GB DVD
* DVD Burning
* Creation of ISO images
* Audio tracks and subtitle selection
* Video title preview
* Preservation of the original menus


%prep
%setup -q  -n %{name}

%{__rm} -rf src/libdvdnav-NOW/
%{__rm} -rf src/libdvdread-NOW/
#patch1 -p0 -b .ffmpeg-compat
%patch2 -p1 -b .unbundle

%patch52 -p1 -b .mimetype


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/k9copy.desktop
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/k9copy_assistant.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
fi


%files -f %{name}.lang
%doc COPYING
%{_kde4_bindir}/k9copy
%{_kde4_bindir}/k9play
%{_kde4_bindir}/k9xineplayer
%{_kde4_appsdir}/k9copy/
%{_kde4_appsdir}/solid/actions/*.desktop
%{_kde4_datadir}/applications/kde4/k9copy.desktop
%{_kde4_datadir}/applications/kde4/k9copy_assistant.desktop
%{_kde4_iconsdir}/hicolor/*/*/*


%changelog
* Thu May 28 2015 Sérgio Basto <sergio@serjux.com> - 3.0.3-1
- Update to k9copy-3.0.3 .
- New upstream URL http://k9copy-reloaded.sourceforge.net/ .
- Unbundle libdvdread and libdvdnav .
- Clean up the spec file and trailing withspaces .

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 2.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Oct 23 2013 Xavier Bachelot <xavier@bachelot.org> - 2.3.8-6
- Rebuild for xine-lib 1.2.

* Mon May 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.8-5
- Rebuilt for x264/FFmpeg

* Sat Apr 27 2013 Sérgio Basto <sergio@serjux.com> - 2.3.8-4
- Switch to ffmpeg-compat.

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.3.8-3
- Mass rebuilt for Fedora 19 Features

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.8-2
- Rebuilt for c++ ABI breakage

* Fri Feb 10 2012 Rex Dieter <rdieter@fedoraproject.org> 2.3.8-1
- 2.3.8
- drop use of Requires(hint)

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 29 2010 Rex Dieter <rdieter@fedoraproject.org> 2.3.6-1
- k9copy-2.3.6

* Sun Jun 13 2010 Rex Dieter <rdieter@fedoraproject.org> 2.3.5-1
- k9copy-2.3.5

* Wed Dec 23 2009 Rex Dieter <rdieter@fedoraproject.org> 2.3.4-1
- k9copy-2.3.4

* Sat Aug 29 2009 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-1
- k9copy-2.3.3

* Wed May 27 2009 Rex Dieter <rdieter@fedoraproject.org> 2.3.2-1
- k9copy-2.3.2

* Mon Apr 06 2009 Rex Dieter <rdieter@fedoraproject.org> 2.3.1-1
- k9copy-2.3.1
- optimize scriptlets

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.3.0-2
- rebuild for new F11 features

* Thu Mar 12 2009 Rex Dieter <rdieter@fedoraproject.org> 2.3.0-1
- k9copy-2.3.0

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-1
- k9copy-2.2.0

* Thu Oct 30 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-2
- ExcludeArch: ppc ppc64 (still fails)

* Thu Oct 30 2008 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-1
- k9copy-2.1.0

* Fri Sep 19 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-4
- drop Requires: libdvdcss

* Thu Sep 18 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-3
- use pkg-config to query ffmpeg includedir(s)

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-2
- ffmpeg patch 

* Mon Jun 16 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-1
- k9copy-2.0.2

* Sat Jun 14 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- k9copy-2.0.1

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-5
- gcc43 patch (forward port malloc patch from fedoraforum)

* Fri Jun 06 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-4
- License: GPLv2+ , %%doc COPYING
- minor libdvdread dl'ing patch

* Tue Jun 03 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-3
- ExcludeArch: ppc ppc64

* Tue Jun 03 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.0-2
- use %%find_lang
- use %%_kde4_* macros

* Mon Jun 02 2008 Leigh Scott <leigh123linux@googlemail.com> 2.0.0-1
- bump to 2.0.0 release 

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.2-1
- Upgrade to 1.2.2
- Added patch to fix buffer overflows (Thanks to Gustavo Maciel Dias Vieira)

* Mon Nov 12 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.2.0-1
- Upgrade to 1.2.0

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.3-2
- d-f-i: s/Mimetypes/MimeTypes/ typo

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.1.3-1
- k9copy-1.1.3

* Sun Jul 08 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.1.1-2.rerel3
- Various minor fixes to the spec file
- Changed release to work around upstreams 'odd' suffix
- Use desktop-file-install for the desktop file

* Tue Jun 05 2007 Ian Chapman <packages[AT]amiga-hardware.com> 1.1.1-1
- Initial release
