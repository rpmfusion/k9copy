
%if 0%{?fedora} > 6
%define kdelibs3 kdelibs3
%define kdepim3 kdepim3
%else
%define kdelibs3 kdelibs
BuildRequires: libutempter-devel
%endif

Name:           k9copy
Version:        1.2.4
Release:        1%{?dist}
Summary:        Video DVD backup and creation program
Group:          Applications/Multimedia
License:        GPLv2
URL:            http://k9copy.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  dbus-qt-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  gettext
BuildRequires:  hal-devel
BuildRequires:  %{kdelibs3}-devel
BuildRequires:  libdvdread-devel

Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires(post): xdg-utils
Requires(postun): xdg-utils

# Optional
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
%setup -q

# Permission fixes
chmod -x */*.h */*.cpp AUTHORS COPYING TODO

# .desktop Key corrections
sed -i \
  -e 's|^DocPath=|X-DocPath=|g' \
  src/%{name}.desktop


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

CPPFLAGS="$(pkg-config --cflags libavcodec) $(pkg-config --cflags libavformat) $CPPFLAGS"
export CPPFLAGS

%configure \
  --disable-rpath \
  --enable-new-ldflags \
  --disable-dependency-tracking --disable-final \
  --disable-debug 

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%find_lang %{name}

# remove empty key Mimetypes
desktop-file-install \
  --vendor="" \
  --dir=%{buildroot}%{_datadir}/applications/kde \
  --remove-key=MimeTypes \
  %{buildroot}%{_datadir}/applications/kde/*.desktop

# Convert symlink to relative
rm -f %{buildroot}%{_docdir}/HTML/en/%{name}/common
pushd %{buildroot}%{_docdir}/HTML/en/%{name}
ln -s ../common common
popd


%clean
rm -rf %{buildroot}


%post
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%postun
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO
%{_docdir}/HTML/en/k9copy/
%{_bindir}/*
%{_datadir}/applications/kde/*.desktop
%{_datadir}/apps/k9copy/
%{_datadir}/apps/konqueror/servicemenus/*.desktop
%{_datadir}/icons/hicolor/*/*/*


%changelog
* Thu Oct 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.2.4-1
- k9copy-1.2.4

* Fri Sep 19 2008 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-3 
- drop Requires: libdvdcss

* Mon Sep 15 2008 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-2
- rebuild for rpmfusion

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
