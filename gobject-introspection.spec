# TODO:
# - requires gobject-introspection-devel to build - fix it
#
# Conditional build:
%bcond_without	cairo		# build without cairo
%bcond_without	static_libs	# do not build static libs
%bcond_without	apidocs		# do not build and package API docs

Summary:	Introspection for GObject libraries
Summary(pl.UTF-8):	Obserwacja bibliotek GObject
Name:		gobject-introspection
Version:	1.42.0
Release:	1
License:	LGPL v2+ (giscanner) and GPL v2+ (tools)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/1.42/%{name}-%{version}.tar.xz
# Source0-md5:	4fa52f6b67367d9c1b99b98683ced202
URL:		http://live.gnome.org/GObjectIntrospection
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
%{?with_cairo:BuildRequires:	cairo-gobject-devel}
BuildRequires:	flex
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	glibc-misc
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.19}
BuildRequires:	libffi-devel >= 3.0.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.6
BuildRequires:	python-Mako
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.36.0
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
Requires:	glib2-devel >= 1:2.36.0
Requires:	libffi-devel >= 3.0.0
Requires:	python-Mako
Requires:	python-modules >= 1:2.6
# for ldd
Requires:	glibc-misc
# vala 0.18 seems to fail on recently generated .gir files
Conflicts:	vala < 2:0.20

%description devel
Header files for gobject-introspection library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gobject-introspection.

%package static
Summary:	Static gobject-introspection library
Summary(pl.UTF-8):	Statyczna biblioteka gobject-introspection
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gobject-introspection library.

%description static -l pl.UTF-8
Statyczna biblioteka gobject-introspection.

%package apidocs
Summary:	gobject-introspection API documentation
Summary(pl.UTF-8):	Dokumentacja API gobject-introspection
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
gobject-introspection API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API gobject-introspection.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_cairo:--disable-tests} \
	--disable-silent-rules \
	%{__enable_disable apidocs gtk-doc} \
	%{__enable_disable static_libs static} \
	--with-html-dir=%{_gtkdocdir}
%{__make} \
	pkgpyexecdir=%{py_sitedir}/giscanner

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	pkgpyexecdir=%{py_sitedir}/giscanner \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/giscanner/*.{a,la} \
    $RPM_BUILD_ROOT%{_libdir}/*.la

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CONTRIBUTORS NEWS README TODO
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgirepository-1.0.so.1
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/DBus-1.0.typelib
%{_libdir}/girepository-1.0/DBusGLib-1.0.typelib
%{_libdir}/girepository-1.0/GIRepository-2.0.typelib
%{_libdir}/girepository-1.0/GL-1.0.typelib
%{_libdir}/girepository-1.0/GLib-2.0.typelib
%{_libdir}/girepository-1.0/GModule-2.0.typelib
%{_libdir}/girepository-1.0/GObject-2.0.typelib
%{_libdir}/girepository-1.0/Gio-2.0.typelib
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
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_includedir}/gobject-introspection-1.0
%{_pkgconfigdir}/gobject-introspection-1.0.pc
%{_pkgconfigdir}/gobject-introspection-no-export-1.0.pc
%{_aclocaldir}/introspection.m4
%dir %{_libdir}/gobject-introspection
%dir %{_libdir}/gobject-introspection/giscanner
%{_libdir}/gobject-introspection/giscanner/doctemplates
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/DBus-1.0.gir
%{_datadir}/gir-1.0/DBusGLib-1.0.gir
%{_datadir}/gir-1.0/GIRepository-2.0.gir
%{_datadir}/gir-1.0/GL-1.0.gir
%{_datadir}/gir-1.0/GLib-2.0.gir
%{_datadir}/gir-1.0/GModule-2.0.gir
%{_datadir}/gir-1.0/GObject-2.0.gir
%{_datadir}/gir-1.0/Gio-2.0.gir
%{_datadir}/gir-1.0/cairo-1.0.gir
%{_datadir}/gir-1.0/fontconfig-2.0.gir
%{_datadir}/gir-1.0/freetype2-2.0.gir
%{_datadir}/gir-1.0/libxml2-2.0.gir
%{_datadir}/gir-1.0/win32-1.0.gir
%{_datadir}/gir-1.0/xfixes-4.0.gir
%{_datadir}/gir-1.0/xft-2.0.gir
%{_datadir}/gir-1.0/xlib-2.0.gir
%{_datadir}/gir-1.0/xrandr-1.3.gir
%{_datadir}/gobject-introspection-1.0
%dir %{py_sitedir}/giscanner
%{py_sitedir}/giscanner/*.py[co]
%dir %{py_sitedir}/giscanner/collections
%{py_sitedir}/giscanner/collections/*.py[co]
%attr(755,root,root) %{py_sitedir}/giscanner/_giscanner.so

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgirepository-1.0.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gi
%endif
