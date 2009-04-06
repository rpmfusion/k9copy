
Name:    k9copy
Version: 2.3.1
Release: 1%{?dist}
Summary: Video DVD backup and creation program
Group:   Applications/Multimedia
License: GPLv2+
URL:     http://k9copy.sourceforge.net/
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: k9copy-2.3.1-ffmpeg.patch
Patch2: k9copy-2.1.0-mimetype.patch
Patch3: k9copy-2.3.1-gcc44.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-devel
BuildRequires: gettext
BuildRequires: hal-devel
BuildRequires: kdelibs4-devel
BuildRequires: libdvdread-devel
BuildRequires: libmpeg2-devel
BuildRequires: pkgconfig
BuildRequires: xine-lib-devel

Requires: dvd+rw-tools
Requires: dvdauthor

# Optional, not *strictly* required:
Requires(hint): mencoder
Requires(hint): mplayer

%description
Video DVD backup and creation program, features include:
* Video stream compression for fit onto a single layer 4.7GB DVD
* DVD Burning
* Creation of ISO images
* Audio tracks and subtitle selection
* Video title preview
* Preservation of the original menus


%prep
%setup -q  -n %{name}-%{version}-Source

%patch1 -p1 -b .ffmpeg
%patch2 -p1 -b .mimetype
%patch3 -p1 -b .gcc44


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  -DAVCODEC_INCLUDE_DIR=$(pkg-config libavcodec --variable=includedir) \
  -DAVFORMAT_INCLUDE_DIR=$(pkg-config libavformat --variable=includedir) \
  -DFFMPEGSCALE_INCLUDE_DIR=$(pkg-config libswscale --variable=includedir) \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name}


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/k9copy.desktop
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/k9copy_assistant.desktop


%clean
rm -rf %{buildroot}


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
%defattr(-,root,root,-)
%doc COPYING
%{_kde4_bindir}/k9copy
%{_kde4_bindir}/k9play
%{_kde4_bindir}/k9xineplayer
%{_kde4_appsdir}/k9copy/
%{_kde4_appsdir}/solid/actions/*.desktop
%{_kde4_datadir}/applications/kde4/k9copy.desktop
%{_kde4_datadir}/applications/kde4/k9copy_assistant.desktop
%{_kde4_docdir}/HTML/en/k9copy/
%{_kde4_iconsdir}/hicolor/*/*/*


%changelog
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
