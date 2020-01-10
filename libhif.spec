%define major 1
%define api 1.0
%define libname %mklibname hif %major
%define devname %mklibname -d hif
%define libgir %mklibname hif-gir %{api} %{major}

Summary:	Simple package library built on top of hawkey and librepo
Name:		libhif
Group:		System/Libraries
Version:	0.2.3
Release:	1
License:	LGPLv2+
URL:		https://github.com/hughsie/libhif
Source0:	http://people.freedesktop.org/~hughsient/releases/libhif-%{version}.tar.xz

# rpm5 adoptation
Patch1:		rpm5-adoptation.patch

BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	docbook-utils
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	hawkey-devel
BuildRequires:	pkgconfig(rpm)
BuildRequires:	pkgconfig(librepo)
BuildRequires:	pkgconfig(libsolv)

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package -n %{libname}
Summary:	Simple package library built on top of hawkey and librepo
Group:		System/Libraries

%description -n %{libname}
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package -n %{libgir}
Summary:	Simple package library built on top of hawkey and librepo
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}

%description -n %{libgir}
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package -n %{devname}
Summary:	GLib Libraries and headers for libhif
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libgir} = %{EVRD}

%description -n %{devname}
GLib headers and libraries for libhif.

%prep
%setup -q
%autopatch -p1

# for patch2
rm -f configure
libtoolize --copy --force
autoreconf -fiv

%build
# Support builds of both git snapshots and tarballs
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
%configure \
        --enable-gtk-doc \
        --enable-dnf-yumdb \
        --disable-static \
        --disable-silent-rules
)

mkdir %{name}/%{_lib}
%make

%install
%makeinstall_std

rm -f %{buildroot}%{_libdir}/libhif*.la

%files -n %{libname}
%{_libdir}/libhif.so.%{major}*

%files -n %{libgir}
%{_libdir}/girepository-1.0/*.typelib

%files -n %{devname}
%doc README.md AUTHORS NEWS COPYING
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir
