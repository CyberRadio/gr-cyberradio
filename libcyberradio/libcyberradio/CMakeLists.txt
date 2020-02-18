########################################################################
# Setup Library
########################################################################
# -- C++11 compiler support
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# -- Source files
LIST(APPEND libcyberradio_sources
       Common/App.cpp
       Common/Debuggable.cpp
       Common/HttpsSession.cpp
       Common/Pythonesque.cpp
       Common/SerialPort.cpp
       Common/Thread.cpp
       Common/VitaIqSource.cpp
       Common/VitaIqUdpPort.cpp
       Common/Vita49Packet.cpp
       Common/Throttle.cpp
       Driver/NDR308/DataPort.cpp
       Driver/NDR308/RadioHandler.cpp
       Driver/NDR308/NbddcComponent.cpp
       Driver/NDR308/NbddcGroupComponent.cpp
       Driver/NDR308/TunerComponent.cpp
       Driver/NDR308/VitaIfSpec.cpp
       Driver/NDR308/WbddcComponent.cpp
       Driver/NDR308/WbddcGroupComponent.cpp
       Driver/NDR308TS/DataPort.cpp
       Driver/NDR308TS/RadioHandler.cpp
       Driver/NDR308TS/NbddcComponent.cpp
       Driver/NDR308TS/NbddcGroupComponent.cpp
       Driver/NDR308TS/TunerComponent.cpp
       Driver/NDR308TS/VitaIfSpec.cpp
       Driver/NDR308TS/WbddcComponent.cpp
       Driver/NDR308TS/WbddcGroupComponent.cpp
       Driver/NDR472/RadioHandler.cpp
       Driver/NDR472/SimpleIpSetup.cpp
       Driver/NDR472/TunerComponent.cpp
       Driver/NDR472/VitaIfSpec.cpp
       Driver/NDR472/WbddcComponent.cpp
       Driver/NDR472/WbddcGroupComponent.cpp
       Driver/NDR651/CWToneGenComponent.cpp
       Driver/NDR651/DataPort.cpp
       Driver/NDR651/DucComponent.cpp
       Driver/NDR651/RadioHandler.cpp
       Driver/NDR651/NbddcComponent.cpp
       Driver/NDR651/NbddcGroupComponent.cpp
       Driver/NDR651/TransmitterComponent.cpp
       Driver/NDR651/TunerComponent.cpp
       Driver/NDR651/VitaIfSpec.cpp
       Driver/NDR651/WbddcComponent.cpp
       Driver/NDR651/WbddcGroupComponent.cpp
       Driver/NDR810/DataPort.cpp
       Driver/NDR810/RadioHandler.cpp
       Driver/NDR810/NbddcComponent.cpp
       Driver/NDR810/NbddcGroupComponent.cpp
       Driver/NDR810/TunerComponent.cpp
       Driver/NDR810/VitaIfSpec.cpp
       Driver/NDR810/WbddcComponent.cpp
       Driver/NDR810/WbddcGroupComponent.cpp
       Driver/ConfigString.cpp
       Driver/Configurable.cpp
       Driver/CWToneGenComponent.cpp
       Driver/DataPort.cpp
       Driver/Driver.cpp
       Driver/DucComponent.cpp
       Driver/NbddcComponent.cpp
       Driver/NbddcGroupComponent.cpp
       Driver/RadioComponent.cpp
       Driver/RadioHandler.cpp
       Driver/RadioTransport.cpp
       Driver/SimpleIpSetup.cpp
       Driver/TransmitterComponent.cpp
       Driver/TunerComponent.cpp
       Driver/VitaIfSpec.cpp
       Driver/WbddcComponent.cpp
       Driver/WbddcGroupComponent.cpp
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
SET(libcyberradio_sources "${libcyberradio_sources}" PARENT_SCOPE)
IF(NOT libcyberradio_sources)
MESSAGE(STATUS "No C++ sources... skipping lib/")
RETURN()
ENDIF(NOT libcyberradio_sources)
# -- Library name
SET(libcyberradio_lib_name cyberradio)

########################################################################
# Link Library
########################################################################
ADD_LIBRARY(${libcyberradio_lib_name} SHARED ${libcyberradio_sources})
TARGET_LINK_LIBRARIES(${libcyberradio_lib_name} 
                      ${Boost_LIBRARIES}
                      ${PCAP_LIBRARIES} 
                      ${CURL_LIBRARIES}
                      ${JSONCPP_LIB}
                      )
SET_TARGET_PROPERTIES(${libcyberradio_lib_name} PROPERTIES 
                      DEFINE_SYMBOL "libcyberradio_EXPORTS"
                      VERSION ${PACKAGE_VERSION}
                      SOVERSION ${VERSION_INFO_MAJOR_VERSION})

########################################################################
# Install Library
########################################################################
INSTALL(TARGETS ${libcyberradio_lib_name}
    LIBRARY DESTINATION ${LIBCYBERRADIO_LIBRARY_DIR} # .so/.dylib file
    ARCHIVE DESTINATION ${LIBCYBERRADIO_LIBRARY_DIR} # .lib file
    RUNTIME DESTINATION ${LIBCYBERRADIO_BINARY_DIR}  # .dll file
)
