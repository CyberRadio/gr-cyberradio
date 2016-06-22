
SUBDIRS=include \
        libcyberradio \
        testvitaiq
        
ACLOCAL_AMFLAGS=-I m4

## Include rules for Doxygen support

include $(top_srcdir)/doxygen.am

## Define a "dummy" data file rule that has no recipe.
## This is needed because make executes the data file rule 
## prior to executing target all-local (which runs Doxygen
## to create the target data files).  

$(DATA): ;

## Define rules to automatically rebuild documentation each time
## we do a build.

clean-local:
	$(RM) $(DX_CLEANFILES)
	
all-local: clean-local doxygen-doc

## HTML/JS/CSS/PNG files that Doxygen creates for us.  These will be 
## installed (or placed in an installation package).  But since they 
## don't need to be included in our source distribution, we don't 
## put the "dist_" prefix on the variable name.
html_DATA = \
            @DX_DOCDIR@/html/annotated.html \
            @DX_DOCDIR@/html/annotated.js \
            @DX_DOCDIR@/html/BasicList_8h_source.html \
            @DX_DOCDIR@/html/bc_s.png \
            @DX_DOCDIR@/html/classes.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1ClientSocket.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1ClientSocket.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1DUCSink.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1DUCSink.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1FlowControlClient.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1FlowControlClient.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1FlowControlClient.png \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1TransmitPacketizer.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1TransmitPacketizer.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1TransmitSocket.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1TransmitSocket.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1UdpStatusReceiver.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1UdpStatusReceiver.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1NDR651_1_1UdpStatusReceiver.png \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Pythonesque.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Pythonesque.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Thread.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Thread.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Thread.png \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Vita49Packet.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1Vita49Packet.js \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1VitaIqSource.html \
            @DX_DOCDIR@/html/classLibCyberRadio_1_1VitaIqSource.js \
            @DX_DOCDIR@/html/ClientSocket_8cpp_source.html \
            @DX_DOCDIR@/html/ClientSocket_8h_source.html \
            @DX_DOCDIR@/html/closed.png \
            @DX_DOCDIR@/html/cyberradio-logo.png \
            @DX_DOCDIR@/html/doxygen.css \
            @DX_DOCDIR@/html/doxygen.png \
            @DX_DOCDIR@/html/DUCSink_8cpp_source.html \
            @DX_DOCDIR@/html/DUCSink_8h_source.html \
            @DX_DOCDIR@/html/files.html \
            @DX_DOCDIR@/html/files.js \
            @DX_DOCDIR@/html/FlowControlClient_8cpp_source.html \
            @DX_DOCDIR@/html/FlowControlClient_8h_source.html \
            @DX_DOCDIR@/html/ftv2blank.png \
            @DX_DOCDIR@/html/ftv2doc.png \
            @DX_DOCDIR@/html/ftv2folderclosed.png \
            @DX_DOCDIR@/html/ftv2folderopen.png \
            @DX_DOCDIR@/html/ftv2lastnode.png \
            @DX_DOCDIR@/html/ftv2link.png \
            @DX_DOCDIR@/html/ftv2mlastnode.png \
            @DX_DOCDIR@/html/ftv2mnode.png \
            @DX_DOCDIR@/html/ftv2node.png \
            @DX_DOCDIR@/html/ftv2plastnode.png \
            @DX_DOCDIR@/html/ftv2pnode.png \
            @DX_DOCDIR@/html/ftv2splitbar.png \
            @DX_DOCDIR@/html/ftv2vertline.png \
            @DX_DOCDIR@/html/functions_func.html \
            @DX_DOCDIR@/html/functions.html \
            @DX_DOCDIR@/html/functions_vars.html \
            @DX_DOCDIR@/html/hierarchy.html \
            @DX_DOCDIR@/html/hierarchy.js \
            @DX_DOCDIR@/html/index.html \
            @DX_DOCDIR@/html/jquery.js \
            @DX_DOCDIR@/html/namespaceLibCyberRadio_1_1NDR651.html \
            @DX_DOCDIR@/html/namespaceLibCyberRadio_1_1NDR651.js \
            @DX_DOCDIR@/html/namespaceLibCyberRadio.html \
            @DX_DOCDIR@/html/namespaceLibCyberRadio.js \
            @DX_DOCDIR@/html/namespacemembers.html \
            @DX_DOCDIR@/html/namespacemembers_type.html \
            @DX_DOCDIR@/html/namespaces.html \
            @DX_DOCDIR@/html/namespaces.js \
            @DX_DOCDIR@/html/nav_f.png \
            @DX_DOCDIR@/html/nav_h.png \
            @DX_DOCDIR@/html/navtree.css \
            @DX_DOCDIR@/html/navtreeindex.js \
            @DX_DOCDIR@/html/navtree.js \
            @DX_DOCDIR@/html/open.png \
            @DX_DOCDIR@/html/PacketTypes_8h_source.html \
            @DX_DOCDIR@/html/Pythonesque_8cpp_source.html \
            @DX_DOCDIR@/html/Pythonesque_8h_source.html \
            @DX_DOCDIR@/html/resize.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Payload.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Payload.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxFrame.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxFrame.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxStatusFrame.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxStatusFrame.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxStatusPayload.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1TxStatusPayload.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Vita49Header.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Vita49Header.js \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Vita49Trailer.html \
            @DX_DOCDIR@/html/structLibCyberRadio_1_1NDR651_1_1Vita49Trailer.js \
            @DX_DOCDIR@/html/tab_a.png \
            @DX_DOCDIR@/html/tab_b.png \
            @DX_DOCDIR@/html/tab_h.png \
            @DX_DOCDIR@/html/tabs.css \
            @DX_DOCDIR@/html/tab_s.png \
            @DX_DOCDIR@/html/Thread_8cpp_source.html \
            @DX_DOCDIR@/html/Thread_8h_source.html \
            @DX_DOCDIR@/html/TransmitPacketizer_8cpp_source.html \
            @DX_DOCDIR@/html/TransmitPacketizer_8h_source.html \
            @DX_DOCDIR@/html/TransmitSocket_8cpp_source.html \
            @DX_DOCDIR@/html/TransmitSocket_8h_source.html \
            @DX_DOCDIR@/html/UdpStatusReceiver_8cpp_source.html \
            @DX_DOCDIR@/html/UdpStatusReceiver_8h_source.html \
            @DX_DOCDIR@/html/Vita49Packet_8cpp_source.html \
            @DX_DOCDIR@/html/Vita49Packet_8h_source.html \
            @DX_DOCDIR@/html/VitaIqSource_8cpp_source.html \
            @DX_DOCDIR@/html/VitaIqSource_8h_source.html \
            @DX_DOCDIR@/html/VitaIqUdpPort_8cpp_source.html \
            @DX_DOCDIR@/html/VitaIqUdpPort_8h_source.html

## Add DX_CLEANFILES to MOSTLYCLEANFILES so that the documentation 
## directory that gets created during the build process is eliminated 
## during "make clean".

MOSTLYCLEANFILES = $(DX_CLEANFILES)

## Add files that should be included in the source distribution 
## (created with "make dist") but aren't included by default:
## * Doxygen configuration file

EXTRA_DIST = $(DX_CONFIG)
