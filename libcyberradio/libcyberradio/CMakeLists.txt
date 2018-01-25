########################################################################
# Setup Library
########################################################################
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# -- Source files
list(APPEND libcyberradio_sources
       Common/Debuggable.cpp
       Common/Pythonesque.cpp
       Common/Thread.cpp
       Common/VitaIqSource.cpp
       Common/VitaIqUdpPort.cpp
       Common/Vita49Packet.cpp
       Common/Throttle.cpp
       NDR651/ClientSocket.cpp
       NDR651/DUCSink.cpp
       NDR651/FlowControlClient.cpp
       NDR651/Packetizer.cpp
       NDR651/RadioController.cpp
       NDR651/SyncTXClient.cpp
       NDR651/StatusReceiver.cpp
       NDR651/TransmitPacketizer.cpp
       NDR651/TXClient.cpp
       NDR651/TransmitSocket.cpp
       NDR651/UdpStatusReceiver.cpp
)
set(libcyberradio_sources "${libcyberradio_sources}" PARENT_SCOPE)
if(NOT libcyberradio_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT libcyberradio_sources)
# -- Library name
set(libcyberradio_lib_name cyberradio)

########################################################################
# Link Library
########################################################################
add_library(${libcyberradio_lib_name} SHARED ${libcyberradio_sources})
target_link_libraries(${libcyberradio_lib_name} 
                      ${Boost_LIBRARIES}
                      pcap 
                      )
set_target_properties(${libcyberradio_lib_name} PROPERTIES DEFINE_SYMBOL "libcyberradio_EXPORTS")

########################################################################
# Install Library
########################################################################
install(TARGETS ${libcyberradio_lib_name}
    LIBRARY DESTINATION ${LIBCYBERRADIO_LIBRARY_DIR} # .so/.dylib file
    ARCHIVE DESTINATION ${LIBCYBERRADIO_LIBRARY_DIR} # .lib file
    RUNTIME DESTINATION ${LIBCYBERRADIO_BINARY_DIR}  # .dll file
)
