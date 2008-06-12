%define ver	031220
%define	name	links-hacked
%define	release	%mkrel 19

Summary:	Lynx-like text WWW browser
Name:		%{name}
Version:	0.0.%{ver}
Release:	%{release}
License:	GPL
Group:		Networking/WWW
Source0:	%{name}-%{ver}.tar.bz2
Source1:	links-16.png
Source2:	links-32.png
Source3:	links-48.png
Source4:        links.cfg
# links fonts (overriding links-hacked ones):
Source5:	links-fonts-new.tar.bz2
Patch7:		links-0.96-no-domain-security.patch
Patch8:		links-current-color-by-default--and-vt100-frames.patch
Patch10:	links-2.0pre1-be-graphic-when-called-_links-graphic_.patch
Patch11:	links-hacked-030620-convert-old-bookmarks-in-new-format.patch
Patch12:	links-hacked-030620-fix-default-charset.patch
Patch13:	links-hacked-030709-config-file.patch
Patch15:	links-hacked-031220-gcc34.patch
Patch16:	links-hacked-031220-lua5.patch
Patch17:	links-hacked-031220-lua5compil.patch
Patch18:	links-hacked-031220-gcc401.patch
URL:		http://xray.sai.msu.ru/~karpov/links-hacked/
BuildConflicts: libsvgalib1-devel
BuildRequires:	gpm-devel ncurses-devel png-devel jpeg-devel lua-devel >= 5.0.2-9mdk
BuildRequires:	ncurses-devel => 5.0 
BuildRequires:	freetype2-devel tiff-devel directfb-devel
BuildRequires:	openssl-devel
BuildRequires:  automake1.7
BuildRequires:  X11-devel
Provides:	webclient
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Links is a text based WWW browser, at first look similar to Lynx, but
somehow different:

- renders tables and frames
- displays colors as specified in current HTML page
- uses drop-down menu (like in Midnight Commander)
- can download files in background
- partially handle Javascript

Links-hacked is based on top of links and offer the below features:
- Lua scripting
- HTTP Auth - stable, ported form Elinks 
- Blocking of selected images 
- Cookies saving
- New options system (c-o)
- Open new windows instead of new links instances in graphics mode
- Url copying
- Full-text selection
- Simple printing
- Forward history
- Extended and configurable 'toolbar'
- Configurable 'mini-status'
- various small improvements:
  o support for "small" and "big" tags,
  o keybinding ("i") to turn on/off images,
  o possibility to show HTTP header ("|"),
  o support for compressed content
  o configurable support for Accept-Charset and Accept-Language. 
- Modularized font subsystem
- Font manager (c-i)
- Dialogs shadows and borders
- Tabbed browsing

%prep
%setup  -q -n %name-%ver
%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch15 -p0
%patch16 -p0 -b .lua
%patch17 -p0 -b .lua5
%patch18 -p0 -b .gcc401

chmod a+r *

%build
./autogen.sh
perl -pi -e 's!"-g!"!g' configure
cp -a %SOURCE5 .

%configure2_5x --enable-graphics --enable-javascript
(cd Unicode ; LC_ALL=C ./gen )
# even more dirty :)
perl -pi -e 's!wget xray.sai.msu.ru/\~karpov/links-hacked/downloads/links-fonts-new.tgz \&\& tar xzvf links-fonts-new.tgz!tar -jxvf links-fonts-new.tar.bz2!' Makefile{,.am,.in}

%make || :
# hacky & dirty
perl -pi -e 's!^@.*!!' utils/Makefile
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

rm -f %buildroot%{_bindir}/links
install links %buildroot%{_bindir}/%name

install -D -m 644 %SOURCE4 %buildroot/etc/links.cfg


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Links (hacked)
Comment=Lynx-like text WWW browser
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Network;WebBrowser;X-MandrivaLinux-Internet-WebBrowsers;
EOF

install -d %buildroot/%_liconsdir/
install -d %buildroot/%_miconsdir/
install -m 644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE2 %buildroot/%_iconsdir/%name.png
install -m 644 %SOURCE3 %buildroot/%_liconsdir/%name.png
# fix conflicts with links-graphic:
mv %buildroot/%_mandir/man1/{links,%name}.1

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- links
if [ ! -e /usr/bin/links ]; then
  update-alternatives --auto links
fi

%post
%if %mdkversion < 200900
%{update_menus}
%endif
update-alternatives --install /usr/bin/links links /usr/bin/%name 5

%postun
%if %mdkversion < 200900
%{clean_menus}
%endif
if [ "$1" = "0" ]; then
  update-alternatives --remove links /usr/bin/%name
fi

%files 
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog README SITES TODO 
%config(noreplace) /etc/links.cfg
%_bindir/%name
%_bindir/arrow
%_bindir/generate_font
%_bindir/make_included
%_bindir/rasterizer
%_mandir/*/*
%_datadir/applications/mandriva-*
#
%_miconsdir/*.png
%_iconsdir/*.png
%_liconsdir/*.png




