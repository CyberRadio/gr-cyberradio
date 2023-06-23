Summary: GNU Radio Blocks for CyberRadio Solutions, Inc. Radios
Name: gr-cyberradio
Version: 20.09.02
Release: centos7
License: Proprietary
Group: Applications/Programming
Source: gr-cyberradio-20.09.02.tar.gz
URL: http://www.cyberradiosolutions.com
Vendor: CyberRadio Solutions, Inc.
Packager: CyberRadio Solutions, Inc. <sales@cyberradiosolutions.com>
BuildRequires: gnuradio-devel
BuildRequires: libcyberradio-devel
BuildRequires: cppunit-devel
BuildRequires: fftw-devel

%define debug_package %{nil}

%description
This package provides blocks for controlling CyberRadio Solutions, Inc. 
radios using GNU Radio and GNU Radio Companion.

Requires GNU Radio (and its associated dependencies).

%prep
%setup

%build
if [ -e gnuradio-volk-devel-3.7.11b1.55-centos7.x86_64.rpm ]
then
    mkdir gnuradio-volk-devel
    cd gnuradio-volk-devel
    rpm2cpio ../gnuradio-volk-devel-3.7.11b1.55-centos7.x86_64.rpm | cpio -idmv 
    ln -sf /usr/lib64/libvolk.so.1.3 usr/lib64/libvolk.so
    cd ..
fi
cmake . -DPACKAGE_VERSION=20.09.02 -DCMAKE_INSTALL_PREFIX=/usr
%{__make} %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%{_sysconfdir}/*
%{_includedir}/*
%{_bindir}/*
%{_libdir}/*
%{_docdir}/*
%{_datadir}/CyberRadio/*
%{_datadir}/gnuradio/*
%{_datadir}/applications/*

%post
mkdir -p /public/ndrDemoGui
chmod 777 /public /public/ndrDemoGui
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

