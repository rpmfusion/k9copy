
Name:           k9copy
Version:        2.0.0
Release:        6%{?dist}
Summary:        Video DVD backup and creation program
Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://k9copy.sourceforge.net/
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}-Source.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: k9copy-2.0.0-libdvdread_so4.patch
Patch2: k9copy-2.0.0-gcc43.patch

# build fails here
ExcludeArch: ppc ppc64

BuildRequires:  cmake
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  hal-devel
BuildRequires:  kdelibs4-devel
BuildRequires:  libdvdread-devel
BuildRequires:  xine-lib-devel

Requires(post): coreutils
Requires(postun): coreutils

Requires:       dvd+rw-tools
Requires:       dvdauthor

# Optional, not *strictly* required:
Requires:       libdvdcss
Requires:       mencoder
Requires:       mplayer

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

%patch1 -p1 -b .libdvdread_so4
%patch2 -p1 -b .gcc43


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%postun
touch --no-create %{_datadir}/icons/hicolor
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_kde4_bindir}/k9copy
%{_kde4_bindir}/k9xineplayer
%{_kde4_appsdir}/k9copy/
%{_kde4_datadir}/applications/kde4/k9copy.desktop
%{_kde4_datadir}/icons/hicolor/*/*/*
%{_kde4_datadir}/kde4/services/*

%changelog
* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.0.0-6
- rebuild

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
