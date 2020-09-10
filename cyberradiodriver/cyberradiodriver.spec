# Spec file template for package: cyberradiodriver
#
# If using the makerpm script, use the following placeholders:
# * RPM_PKG_NAME: Name of the RPM package
# * RPM_PKG_VERSION: Version number of the RPM package
# * RPM_PKG_OS: Name of the OS that the RPM is built on
# * RPM_PKG_OS_VER: Version (major) of the OS
#
# Also, makerpm will build a source tarball with the version number in
# its name, so just use the %setup macro without arguments.

# For RHEL 6, we need to build this under its Python 2.7 SCL environment,
# so we need to redefine some of the standard RPM macros.
%if "RPM_PKG_OSRPM_PKG_OS_VER" == "redhat6"
%define __pyroot /opt/rh/python27/root
%define __python2 %{python27__python2}
%define python2_sitelib %{python27python_sitelib}
%define python2_sitearch %{python27python2_sitearch}
%define __python_provides %{python27_python_provides}
%define __python_requires %{python27_python_requires}
%define __python %{__python2}
%define _prefix %{__pyroot}/usr
%define __os_install_post %{python27_os_install_post}
%define _datadir /usr/share
%endif
%if "RPM_PKG_OSRPM_PKG_OS_VER" == "centos8"
%define __python /usr/bin/python2
%endif

Summary: CyberRadio Solutions, Inc., NDR-series Radio Control Driver
Name: RPM_PKG_NAME
Version: RPM_PKG_VERSION
Release: RPM_PKG_OSRPM_PKG_OS_VER
License: Proprietary
Group: Applications/Programming
Source: RPM_PKG_NAME-RPM_PKG_VERSION.tar.gz
URL: http://www.cyberradiosolutions.com
Vendor: CyberRadio Solutions, Inc.
Packager: CyberRadio Solutions, Inc. <sales@cyberradiosolutions.com>
BuildRequires: doxygen
Requires: numpy
Requires: pyserial
Requires: python-requests

# Don't build a "debuginfo" package
%define debug_package %{nil}

%description
Provides a unified driver for controlling all NDR-series radios from
CyberRadio Solutions, Inc.

%prep
# Use setup macro without arguments if using the makerpm script.
%setup

%build
# Uncomment the build steps necessary for the project you are building.
# -- Makefile project: Just the "make" step
# -- CMake project: Both the "%cmake" and "make" steps
# -- Autotools project: TBD
# -- Python project: None (the install step takes care of this)
#%cmake .
#make %{?_smp_mflags}

%install
# Uncomment the install steps necessary for the project you are building.
# -- Makefile project: The "make install" step
# -- CMake project: The "make install" step
# -- Autotools project: The "make install" step
# -- Python project: The "%{__python} setup.py install" step
# -- Projects with docs that are not installed via Makefile: The "mkdir" and "mv" steps
#make install DESTDIR=%{buildroot}
%{__python} setup.py install --root=%{buildroot}
mkdir -p %{buildroot}/%{_docdir}
mv docs/* %{buildroot}/%{_docdir}

%files
# Uncomment the entries necessary for the project you are building.
# -- Projects that generate system configuration files under /etc
#%{_sysconfdir}/*
# -- Projects that generate header files under /usr/include
#%{_includedir}/*
# -- Projects that generate executables under /usr/bin
%{_bindir}/*
# -- Projects that generate libraries under /usr/lib (/usr/lib64 on RedHat)
#%{_libdir}/*
# -- Projects that generate docs under /usr/share/docs
%{_docdir}/*
# -- Projects that generate Python libraries under /usr/lib/python[ver]
%{python_sitelib}/*
# -- Projects that generate auxiliary files under /usr/share/<name>
#%{_datadir}/%{name}/*
# -- Projects that generate app shortcuts under /usr/share/applications
%{_datadir}/applications/*


