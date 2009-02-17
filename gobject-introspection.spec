# TODO:
# - check whether gir data is needed only to build applications,
#   if so it can be moved to -devel
#
Summary:	Introspection for GObject libraries
Name:		gobject-introspection
Version:	0.6.2
Release:	1
License:	LGPL v2+ (giscanner) and GPL v2+ (tools)
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gobject-introspection/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	53d4dc57f08ea29da84aa095e7229a64
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
Requires:	%{name}-libs = %{version}-%{release}
Suggests:	gir-repository
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Tools for introspecting GObject-based frameworks.

%package libs
Summary:	Libraries for gobject-introspection
Group:		Development/Libraries

%description libs
Libraries for gobject-introspection.

%package devel
Summary:	Header files for gobject-introspection library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 2.16.0

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{py_sitedir}/giscanner/*.{a,la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_bindir}/g-ir-compiler
%attr(755,root,root) %{_bindir}/g-ir-generate
%attr(755,root,root) %{_bindir}/g-ir-scanner
%{_mandir}/man1/g-ir-compiler.1*
%{_mandir}/man1/g-ir-generate.1*
%{_mandir}/man1/g-ir-scanner.1*
%{py_sitedir}/giscanner/*.py[co]
%{py_sitedir}/giscanner/_giscanner.so

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so.1.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-everything-1.0.so.1
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so.0.0.0
%attr(755,root,root) %ghost %{_libdir}/libgirepository-1.0.so.0
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgirepository-everything-1.0.so
%attr(755,root,root) %{_libdir}/libgirepository-1.0.so
%{_pkgconfigdir}/gobject-introspection-1.0.pc
%{_includedir}/gobject-introspection-1.0
%{_libdir}/libgirepository-1.0.la
%{_libdir}/libgirepository-everything-1.0.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libgirepository-1.0.a
%{_libdir}/libgirepository-everything-1.0.a
