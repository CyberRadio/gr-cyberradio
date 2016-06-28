#######################################
# The list of libraries we are building seperated by spaces.
# The 'lib_' indicates that these build products will be installed
# in the $(libdir) directory. For example /usr/lib
lib_LTLIBRARIES = libcyberradio.la

#######################################
# Build information for each library

# Sources for libcyberradio
libcyberradio_la_SOURCES = \
                           Common/Debuggable.cpp \
                           Common/Pythonesque.cpp \
                           Common/Thread.cpp \
                           Common/VitaIqSource.cpp \
                           Common/VitaIqUdpPort.cpp \
                           Common/Vita49Packet.cpp \
                           NDR651/ClientSocket.cpp \
                           NDR651/DUCSink.cpp \
                           NDR651/FlowControlClient.cpp \
                           NDR651/TransmitPacketizer.cpp \
                           NDR651/TransmitSocket.cpp \
                           NDR651/UdpStatusReceiver.cpp

# Linker options for libcyberradio
libcyberradio_la_LDFLAGS = $(BOOST_ASIO_LIB) \
                           $(BOOST_CHRONO_LIB) \
                           $(BOOST_THREAD_LIB) \
                           $(BOOST_SYSTEM_LIB) \
                           -lpthread 

# Compiler options. Here we are adding the include directory
# to be searched for headers included in the source code.
libcyberradio_la_CPPFLAGS = -I$(top_srcdir)/include

