# Spec file template for package: libcyberradio
#
# If using the makerpm script, use the following placeholders:
# * RPM_PKG_NAME: Name of the RPM package
# * RPM_PKG_VERSION: Version number of the RPM package
# * RPM_PKG_OS: Name of the OS that the RPM is built on
# * RPM_PKG_OS_VER: Version (major) of the OS
#
# Also, makerpm will build a source tarball with the version number in
# its name, so just use the %setup macro without arguments.
#
Summary: CyberRadio Solutions Common Library
Name: RPM_PKG_NAME
Version: RPM_PKG_VERSION
Release: RPM_PKG_OSRPM_PKG_OS_VER
License: Proprietary
Group: Applications/Programming
Source: RPM_PKG_NAME-RPM_PKG_VERSION.tar.gz
URL: http://www.cyberradiosolutions.com
Vendor: CyberRadio Solutions, Inc.
Packager: CyberRadio Solutions, Inc. <sales@cyberradiosolutions.com>
BuildRequires: boost-devel >= 1.60
BuildRequires: jsoncpp-devel
BuildRequires: libpcap-devel
BuildRequires: doxygen

%description
Provides a common set of software components for interacting with 
CyberRadio Solutions radios.

# Macro to extract the major version number from the overall package version
%define major_version %(echo RPM_PKG_VERSION | cut -d. -f1)
# Don't build a "debuginfo" package
%define debug_package %{nil}

%prep
# Use setup macro without arguments if using the makerpm script.
%setup

%build
# FEDORA 28 HACK -- jsoncpp-devel on Fedora 28 puts its include files
# in /usr/include/json rather than /usr/include/jsoncpp/json, so look
# for jsoncpp paths and replace them accordingly. -- DA
%if "RPM_PKG_OS" == "fedora"
grep -rlZ "jsoncpp/json" . | xargs -r -0 sed -i -e 's|jsoncpp/json|json|g'
%endif
# Uncomment the build steps necessary for the project you are building.
# -- Makefile project: Just the "%{__make}" step
# -- CMake project: Both the "%cmake" and "%{__make}" steps
# -- Autotools project: TBD
# -- Python project: None (the install step takes care of this)
cmake . -DPACKAGE_VERSION=RPM_PKG_VERSION -DCMAKE_INSTALL_PREFIX=/usr
%{__make} %{?_smp_mflags}

%install
# Uncomment the install steps necessary for the project you are building.
# -- Makefile project: The "make install" step
# -- CMake project: The "make install" step
# -- Autotools project: The "make install" step
# -- Python project: The "%{__python} setup.py install" step
# -- Projects with docs that are not installed via Makefile: The "mkdir" and "mv" steps
make install DESTDIR=%{buildroot}
#%{__python} setup.py install --root=%{buildroot}
#mkdir -p %{buildroot}/%{_docdir}
#mv docs/* %{buildroot}/%{_docdir}

%files
# Uncomment the entries necessary for the project you are building.
# -- Projects that generate system configuration files under /etc
#%{_sysconfdir}/*
# -- Projects that generate header files under /usr/include
#%{_includedir}/*
# -- Projects that generate executables under /usr/bin
#%{_bindir}/*
# -- Projects that generate libraries under /usr/lib (/usr/lib64 on RedHat)
%{_libdir}/libcyberradio.so.RPM_PKG_VERSION
# -- Projects that generate docs under /usr/share/docs
#%{_docdir}/*
# -- Projects that generate Python libraries under /usr/lib/python[ver]
#%{python_sitelib}/*
# -- Projects that generate auxiliary files under /usr/share/<name>
#%{_datadir}/%{name}/*
# -- Projects that generate app shortcuts under /usr/share/applications
#%{_datadir}/applications/*

%package devel

Summary: CyberRadio Solutions Common Library: Development Files
Requires: libcyberradio = RPM_PKG_VERSION

%description devel
Provides a common set of software components for interacting with 
CyberRadio Solutions radios.

%files devel

# Uncomment the entries necessary for the project you are building.
# -- Projects that generate system configuration files under /etc
#%{_sysconfdir}/*
# -- Projects that generate header files under /usr/include
%{_includedir}/*
# -- Projects that generate executables under /usr/bin
#%{_bindir}/*
# -- Projects that generate libraries under /usr/lib (/usr/lib64 on RedHat)
%{_libdir}/cmake/*
%{_libdir}/cmake/*
%{_libdir}/libcyberradio.so
%{_libdir}/libcyberradio.so.%{major_version}
# -- Projects that generate docs under /usr/share/docs
#%{_docdir}/*
# -- Projects that generate Python libraries under /usr/lib/python[ver]
#%{python_sitelib}/*
# -- Projects that generate auxiliary files under /usr/share/<name>
%{_datadir}/%{name}/*
# -- Projects that generate app shortcuts under /usr/share/applications
#%{_datadir}/applications/*

%package doc

Summary: CyberRadio Solutions Common Library: Development Documentation

%description doc
Provides documentation for using the CyberRadio Solutions Common Library.

%files doc

# -- Projects that generate docs under /usr/share/docs
%{_docdir}/*


