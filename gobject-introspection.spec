#
# Conditional build:
%bcond_without	cairo		# cairo support
%bcond_without	apidocs		# API documentation
%bcond_with	bootstrap	# bootstrap from glib < 2.80

Summary:	Introspection for GObject libraries
Summary(pl.UTF-8):	Obserwacja bibliotek GObject
Name:		gobject-introspection
Version:	1.80.0
Release:	1
License:	LGPL v2+ (libraries, giscanner) and GPL v2+ (tools)
Group:		Libraries
Source0:	https://download.gnome.org/sources/gobject-introspection/1.80/%{name}-%{version}.tar.xz
# Source0-md5:	003cc22c45be5edf91911050bbcfbde6
Source1:	https://download.gnome.org/sources/glib/2.80/glib-2.80.0.tar.xz
# Source1-md5:	3a51e2803ecd22c2dadcd07d9475ebe3
URL:		https://wiki.gnome.org/Projects/GObjectIntrospection
BuildRequires:	automake
BuildRequires:	bison
%{?with_cairo:BuildRequires:	cairo-gobject-devel}
BuildRequires:	flex
BuildRequires:	gcc >= 5:3.2
%{!?with_bootstrap:BuildRequires:	glib2-devel >= 1:2.80.0}
BuildRequires:	glibc-misc
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.19}
BuildRequires:	libffi-devel >= 7:3.4
BuildRequires:	meson >= 1.2.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-Mako
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-markdown
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.80.0
Requires:	libffi >= 7:3.4
Obsoletes:	gobject-introspection-libs < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools for introspecting GObject-based frameworks.

%description -l pl.UTF-8
Narzędzia do obserwacji szkieletów opartych na bibliotece GObject.

%package devel
Summary:	Header files for gobject-introspection library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gobject-introspection
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.80.0
Requires:	libffi-devel >= 7:3.4
Requires:	python3-Mako
Requires:	python3-modules >= 1:3.6
# for ldd
Requires:	glibc-misc
Obsoletes:	gobject-introspection-static < 1.62
# vala 0.18 seems to fail on recently generated .gir files
Conflicts:	vala < 2:0.20

%description devel
Header files for gobject-introspection library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gobject-introspection.

%package apidocs
Summary:	gobject-introspection API documentation
Summary(pl.UTF-8):	Dokumentacja API gobject-introspection
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
gobject-introspection API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gobject-introspection.

%prep
%setup -q %{?with_bootstrap:-a1}

%if %{with bootstrap}
%{__mv} glib-2.80.0 subprojects/glib
%endif

%{__sed} -i -e "s,^giscannerdir[[:space:]]*=[[:space:]]*.*,giscannerdir='%{py3_sitedir}/giscanner'," giscanner/meson.build
%{__sed} -i -e '/python_cmd =/ s,/usr/bin/env python@0@,/usr/bin/python@0@,' tools/meson.build

%build
%meson build \
	-Ddoctool=enabled \
	-Dgtk_doc=%{__true_false apidocs}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

%if %{with bootstrap}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{gapplication,gdbus*,gi-*,gio*,glib-*,gobject-*,gresource,gsettings,gtester*}
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/{gio-unix-2.0,glib-2.0}
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/gio-launch-desktop
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{gio,girepository,glib,gmodule,gobject,gthread}-2.0.*
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/{gio,glib-2.0}
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/{gio,gio-unix,girepository,glib,gmodule,gmodule-export,gmodule-no-export,gobject,gthread}-2.0.pc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/%{_lib}/lib{glib,gobject}-2.0.*
%{__rm} $RPM_BUILD_ROOT%{_datadir}/gettext/its/gschema.*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/glib-2.0
%{__rm} $RPM_BUILD_ROOT%{_aclocaldir}/{glib-2.0,glib-gettext,gsettings}.m4
%{__rm} $RPM_BUILD_ROOT%{bash_compdir}/{gapplication,gdbus,gio,gresource,gsettings}
%{__rm} $RPM_BUILD_ROOT%{_localedir}/*/LC_MESSAGES/glib20.mo
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README.rst
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgirepository-1.0.so.1
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/DBus-1.0.typelib
%{_libdir}/girepository-1.0/DBusGLib-1.0.typelib
%{_libdir}/girepository-1.0/GIRepository-2.0.typelib
%{_libdir}/girepository-1.0/GL-1.0.typelib
%{_libdir}/girepository-1.0/Vulkan-1.0.typelib
%{_libdir}/girepository-1.0/cairo-1.0.typelib
%{_libdir}/girepository-1.0/fontconfig-2.0.typelib
%{_libdir}/girepository-1.0/freetype2-2.0.typelib
%{_libdir}/girepository-1.0/libxml2-2.0.typelib
%{_libdir}/girepository-1.0/win32-1.0.typelib
%{_libdir}/girepository-1.0/xfixes-4.0.typelib
%{_libdir}/girepository-1.0/xft-2.0.typelib
%{_libdir}/girepository-1.0/xlib-2.0.typelib
%{_libdir}/girepository-1.0/xrandr-1.3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/g-ir-annotation-tool
%attr(755,root,root) %{_bindir}/g-ir-compiler
%attr(755,root,root) %{_bindir}/g-ir-doc-tool
%attr(755,root,root) %{_bindir}/g-ir-generate
%attr(755,root,root) %{_bindir}/g-ir-inspect
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-doc-tool.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_includedir}/gobject-introspection-1.0
%{_pkgconfigdir}/gobject-introspection-1.0.pc
%{_pkgconfigdir}/gobject-introspection-no-export-1.0.pc
%{_aclocaldir}/introspection.m4
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/DBus-1.0.gir
%{_datadir}/gir-1.0/DBusGLib-1.0.gir
%{_datadir}/gir-1.0/GIRepository-2.0.gir
%{_datadir}/gir-1.0/GL-1.0.gir
%{_datadir}/gir-1.0/Vulkan-1.0.gir
%{_datadir}/gir-1.0/cairo-1.0.gir
%{_datadir}/gir-1.0/fontconfig-2.0.gir
%{_datadir}/gir-1.0/freetype2-2.0.gir
%{_datadir}/gir-1.0/gir-1.2.rnc
%{_datadir}/gir-1.0/libxml2-2.0.gir
%{_datadir}/gir-1.0/win32-1.0.gir
%{_datadir}/gir-1.0/xfixes-4.0.gir
%{_datadir}/gir-1.0/xft-2.0.gir
%{_datadir}/gir-1.0/xlib-2.0.gir
%{_datadir}/gir-1.0/xrandr-1.3.gir
%{_datadir}/gobject-introspection-1.0
%dir %{py3_sitedir}/giscanner
%{py3_sitedir}/giscanner/*.py
%dir %{py3_sitedir}/giscanner/__pycache__
%{py3_sitedir}/giscanner/__pycache__/*.py[co]
%{py3_sitedir}/giscanner/doctemplates
%attr(755,root,root) %{py3_sitedir}/giscanner/_giscanner.cpython-*.so

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gi
%endif
