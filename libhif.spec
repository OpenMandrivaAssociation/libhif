%global major 1
%define libname %mklibname hif %major
%define devname %mklibname -d hif

Summary:   Simple package library built on top of hawkey and librepo
Name:      libhif
Group:     System/Libraries
Version:   0.2.2
Release:   %mkrel 2
License:   LGPLv2+
URL:       https://github.com/hughsie/libhif
Source0:   http://people.freedesktop.org/~hughsient/releases/libhif-%{version}.tar.xz

# Patches from Fedora
Patch0:    libhif-yumdb-fixes.patch

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: libtool
BuildRequires: docbook-utils
BuildRequires: gtk-doc
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: hawkey-devel >= 0.4.6
BuildRequires: rpm-devel >= 4.11.0
BuildRequires: librepo-devel >= 1.7.11
BuildRequires: pkgconfig(libsolv)

# Bootstrap build requirements
BuildRequires: automake autoconf libtool

%description
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package -n %{libname}
Summary: Simple package library built on top of hawkey and librepo
Group:   System/Libraries

%description -n %{libname}
This library provides a simple interface to hawkey and librepo and is currently
used by PackageKit and rpm-ostree.

%package -n %{devname}
Summary: GLib Libraries and headers for libhif
Group:   Development/C
Provides: %{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{libname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{devname}
GLib headers and libraries for libhif.

%prep
%setup -q
%apply_patches

# for patch2
rm -f configure

%build
# Support builds of both git snapshots and tarballs
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
%configure \
        --enable-gtk-doc \
        --enable-dnf-yumdb \
        --disable-static \
        --disable-silent-rules
)

%make

%install
%make_install

rm -f %{buildroot}%{_libdir}/libhif*.la

%files -n %{libname}
%{_libdir}/libhif.so.%{major}
%{_libdir}/libhif.so.%{major}.*
%{_libdir}/girepository-1.0/*.typelib

%files -n %{devname}
%license COPYING
%doc README.md AUTHORS NEWS
%{_libdir}/libhif.so
%{_libdir}/pkgconfig/libhif.pc
%dir %{_includedir}/libhif
%{_includedir}/libhif/*.h
%{_datadir}/gtk-doc
%{_datadir}/gir-1.0/*.gir
