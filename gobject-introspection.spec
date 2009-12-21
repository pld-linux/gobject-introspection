Summary:	Introspection for GObject libraries
Name:		gobject-introspection
Version:	0.6.7
Release:	1
License:	LGPL v2+ (giscanner) and GPL v2+ (tools)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	41205c14cbd86632806578448e29bd30
Patch0:		%{name}-libtool.patch
URL:		http://live.gnome.org/GObjectIntrospection
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
BuildRequires:	bison
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	libffi-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.5
BuildRequires:	python-devel >= 1:2.5
Obsoletes:	gobject-introspection-libs < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools for introspecting GObject-based frameworks.

%package devel
Summary:	Header files for gobject-introspection library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.16.0
Requires:	libffi-devel

%description devel
Header files for gobject-introspection library.

%package static
Summary:	Static gobject-introspection library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gobject-introspection library.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{py_sitedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/gobject-introspection/giscanner $RPM_BUILD_ROOT%{py_sitedir}/

rm $RPM_BUILD_ROOT%{py_sitedir}/giscanner/*.{a,la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-everything-1.0.so.1
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-1.0.so.0
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/g-ir-compiler
%attr(755,root,root) %{_bindir}/g-ir-generate
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_pkgconfigdir}/gobject-introspection-1.0.pc
%{_pkgconfigdir}/gobject-introspection-no-export-1.0.pc
%{_includedir}/gobject-introspection-1.0
%{_libdir}/libgirepository-1.0.la
%{_libdir}/libgirepository-everything-1.0.la
%{_datadir}/aclocal/introspection.m4
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gobject-introspection-1.0
%dir %{py_sitedir}/giscanner
%{py_sitedir}/giscanner/*.py[co]
%{py_sitedir}/giscanner/_giscanner.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libgirepository-1.0.a
%{_libdir}/libgirepository-everything-1.0.a
