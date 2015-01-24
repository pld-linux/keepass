#
# Conditional build:
%bcond_with	doc		# don't build doc

Summary:	Password manager
Name:		keepass
Version:	2.27
Release:	1
License:	GPL v2+
Group:		X11/Applications
# Created with, e.g.:
# version=2.25 tmpdir=`mktemp -d` && cd $tmpdir && curl -LRO http://downloads.sourceforge.net/project/keepass/KeePass%202.x/$version/KeePass-$version-Source.zip && mkdir keepass-$version && unzip -d keepass-$version KeePass-$version-Source.zip && find keepass-$version -name "*dll" -delete && tar -cJf keepass-$version.tar.xz keepass-$version
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/keepass/%{name}-%{version}.tar.xz/5a4e243b7f3784db99a3f5e3ede2493b/keepass-%{version}.tar.xz
# Source0-md5:	5a4e243b7f3784db99a3f5e3ede2493b
# Upstream does not include a .desktop file, etc..
Patch0:		%{name}-desktop-integration.patch
Patch3:		%{name}-appdata.patch
# Move XSL files to /usr/share/keepass:
Patch1:		%{name}-fix-XSL-search-path.patch
# Locate locally-installed help files:
Patch2:		%{name}-enable-local-help.patch
URL:		http://keepass.info/
%{?with_doc:BuildRequires:	archmage}
BuildRequires:	desktop-file-utils
BuildRequires:	mono-devel
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	hicolor-icon-theme
Requires:	xdotool
Requires:	xsel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	%{_prefix}/lib/%{name}

%description
KeePass is a free open source password manager, which helps you to
remember your passwords in a secure way. You can put all your
passwords in one database, which is locked with one master key or a
key file. You only have to remember one single master password or
select the key file to unlock the whole database.

%package doc
Summary:	Documentation for the KeePass password manager
BuildArch:	noarch

%description doc
Documentation for KeePass, a free open source password manager.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%undos Docs/*.txt

%build
cd Build
sh PrepMonoDev.sh
cd -

xbuild /target:KeePass /property:Configuration=Release
%if %{with doc}
%{__python} -c 'import archmod.CHM; archmod.CHM.CHMDir("Docs").process_templates("Docs/Chm")'
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_prefix}/lib/%{name},%{_datadir}/%{name}/XSL,%{_desktopdir},%{_bindir},%{_datadir}/mime/packages,%{_datadir}/icons/hicolor/256x256/apps,%{_mandir}/man1,%{_docdir}/%{name},%{_datadir}/appdata}

install -p Build/KeePass/Release/KeePass.exe Ext/KeePass{.config.xml,.exe.config} $RPM_BUILD_ROOT%{_appdir}
install -p Ext/XSL/{KDBX_DetailsFull.xsl,KDBX_DetailsLite.xsl,KDBX_PasswordsOnly.xsl,KDBX_Styles.css,KDBX_Tabular.xsl,TableHeader.gif} \
	$RPM_BUILD_ROOT%{_datadir}/%{name}/XSL

install -p -T Ext/Icons/Finals/plockb.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
desktop-file-install --dir=$RPM_BUILD_ROOT%{_desktopdir} dist/%{name}.desktop
cp -p dist/%{name}.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages
cp -p dist/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p dist/%{name}.appdata.xml $RPM_BUILD_ROOT%{_datadir}/appdata
install -p dist/%{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%postun
%update_desktop_database
%update_icon_cache hicolor
%update_mime_database

%files
%defattr(644,root,root,755)
%doc Docs/{History.txt,License.txt}
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_datadir}/appdata/keepass.appdata.xml
%{_datadir}/mime/packages/keepass.xml
%{_iconsdir}/hicolor/*/apps/keepass.png

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc Docs/Chm/*
%endif
