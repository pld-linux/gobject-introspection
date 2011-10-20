# TODO:
# - requires gobject-introspection-devel to build - fix it
Summary:	Introspection for GObject libraries
Summary(pl.UTF-8):	Obserwacja bibliotek GObject
Name:		gobject-introspection
Version:	0.10.8
Release:	2
Epoch:		1
License:	LGPL v2+ (giscanner) and GPL v2+ (tools)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/0.10/%{name}-%{version}.tar.bz2
# Source0-md5:	b5da58a5327d13b4d1e08b8e42b2456d
Patch0:		%{name}-libtool.patch
URL:		http://live.gnome.org/GObjectIntrospection
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	bison
BuildRequires:	cairo-devel
BuildRequires:	flex
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	glibc-misc
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	libffi-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
Requires:	glib2 >= 1:2.24.0
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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	glib2-devel >= 1:2.24.0
Requires:	libffi-devel
Requires:	python-modules

%description devel
Header files for gobject-introspection library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gobject-introspection.

%package static
Summary:	Static gobject-introspection library
Summary(pl.UTF-8):	Statyczna biblioteka gobject-introspection
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{py_sitedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT%{py_sitedir}

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/giscanner/*.{a,la}

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
%{_libdir}/girepository-1.0/xfixes-4.0.typelib
%{_libdir}/girepository-1.0/xft-2.0.typelib
%{_libdir}/girepository-1.0/xlib-2.0.typelib
%{_libdir}/girepository-1.0/xrandr-1.3.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/g-ir-annotation-tool
%attr(755,root,root) %{_bindir}/g-ir-compiler
%attr(755,root,root) %{_bindir}/g-ir-generate
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_libdir}/libgirepository-1.0.la
%{_includedir}/gobject-introspection-1.0
%{_pkgconfigdir}/gobject-introspection-1.0.pc
%{_pkgconfigdir}/gobject-introspection-no-export-1.0.pc
%{_aclocaldir}/introspection.m4
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
%{_datadir}/gir-1.0/xfixes-4.0.gir
%{_datadir}/gir-1.0/xft-2.0.gir
%{_datadir}/gir-1.0/xlib-2.0.gir
%{_datadir}/gir-1.0/xrandr-1.3.gir
%{_datadir}/gobject-introspection-1.0
%dir %{py_sitedir}/giscanner
%{py_sitedir}/giscanner/*.py[co]
%attr(755,root,root) %{py_sitedir}/giscanner/_giscanner.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libgirepository-1.0.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gi
