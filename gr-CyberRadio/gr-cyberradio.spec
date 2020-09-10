# Spec file template for package: gr-cyberradio
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
Summary: GNU Radio Blocks for CyberRadio Solutions, Inc. Radios
Name: RPM_PKG_NAME
Version: RPM_PKG_VERSION
Release: RPM_PKG_OSRPM_PKG_OS_VER
License: Proprietary
Group: Applications/Programming
Source: RPM_PKG_NAME-RPM_PKG_VERSION.tar.gz
URL: http://www.cyberradiosolutions.com
Vendor: CyberRadio Solutions, Inc.
Packager: CyberRadio Solutions, Inc. <sales@cyberradiosolutions.com>
BuildRequires: gnuradio-devel
BuildRequires: libcyberradio-devel
BuildRequires: cppunit-devel
BuildRequires: fftw-devel

# Don't build a "debuginfo" package
%define debug_package %{nil}

%description
This package provides blocks for controlling CyberRadio Solutions, Inc. 
radios using GNU Radio and GNU Radio Companion.

Requires GNU Radio (and its associated dependencies).

%prep
# Use setup macro without arguments if using the makerpm script.
%setup

%build
# Unpack gnuradio-volk-devel RPM into the current folder if it exists
if [ -e gnuradio-volk-devel-3.7.11b1.55-centos7.x86_64.rpm ]
then
    mkdir gnuradio-volk-devel
    cd gnuradio-volk-devel
    rpm2cpio ../gnuradio-volk-devel-3.7.11b1.55-centos7.x86_64.rpm | cpio -idmv 
    ln -sf /usr/lib64/libvolk.so.1.3 usr/lib64/libvolk.so
    cd ..
fi
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
%{_sysconfdir}/*
# -- Projects that generate header files under /usr/include
%{_includedir}/*
# -- Projects that generate executables under /usr/bin
%{_bindir}/*
# -- Projects that generate libraries under /usr/lib (/usr/lib64 on RedHat)
%{_libdir}/*
# -- Projects that generate docs under /usr/share/docs
%{_docdir}/*
# -- Projects that generate Python libraries under /usr/lib/python[ver]
#%{python_sitelib}/*
#%{python_sitearch}/*
# -- Projects that generate auxiliary files under /usr/share/<name>
#%{_datadir}/%{name}/*
%{_datadir}/CyberRadio/*
%{_datadir}/gnuradio/*
# -- Projects that generate app shortcuts under /usr/share/applications
%{_datadir}/applications/*

# Post-install script section
%post
# -- Make directories /public and /public/ndrDemoGui if needed
mkdir -p /public/ndrDemoGui
# -- Change directory permissions on /public and /public/ndrDemoGui
chmod 777 /public /public/ndrDemoGui
# -- Fix GNU Radio flowgraph template for Qt
for TEMPLATE in `find /usr/{local/,}lib64/python* -name "flow_graph.tmpl"`
do
	IFS=''
	grep -q "Qt App Signal Handlers" $TEMPLATE
	if [ $? -ne 0 ]
	then
		echo "MODDING $TEMPLATE"
		while read LINE
		do
			sed -i "s/    def quitting():/    $LINE\n    def quitting():/" $TEMPLATE
			echo "-> $LINE"
		done <<< "##  vvvv  gr-CyberRadio  vvvv
\##Qt App Signal Handlers.
from PyQt4.QtCore import QTimer
import signal
signal.signal(signal.SIGINT, lambda sig,_: qapp.quit())
signal.signal(signal.SIGTERM, lambda sig,_: qapp.quit())
timer = QTimer()
timer.start(200)
timer.timeout.connect(lambda: None)
\##  ^^^^  gr-CyberRadio  ^^^^
"
	else
		echo "SKIPPING $TEMPLATE"
	fi
done
for TEMPLATE in `find /usr/{local/,}lib64/python* -name "flow_graph.tmpl"`
do
	IFS=''
	grep -q "Wait for QT flowgraph to end" $TEMPLATE
	if [ $? -ne 0 ]
	then
		echo "MODDING $TEMPLATE"
		while read LINE
		do
			sed -i "s/    def quitting():/    $LINE\n    def quitting():/" $TEMPLATE
			echo "-> $LINE"
		done <<< "##  vvvv  gr-CyberRadio  vvvv
\##Wait for QT flowgraph to end.
import threading
def doWait(tb,qapp):
    tb.wait()
    print('done waiting')
    qapp.exit() 
t = threading.Thread(name='doWait', target = doWait, args=(tb,qapp))
t.start()
\##  ^^^^  gr-CyberRadio  ^^^^
"
	else
		echo "SKIPPING $TEMPLATE"
	fi
done

