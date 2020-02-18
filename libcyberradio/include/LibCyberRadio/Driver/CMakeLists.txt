########################################################################
# Install Public Header Files
########################################################################
# The LIST()-ADD_CUSTOM_TARGET() construction enables these headers
# to be listed in CMake projects for QT Creator and other IDEs.
LIST(APPEND libcyberradio_headers_Driver
    ConfigString.h
    Configurable.h
    CWToneGenComponent.h
    DataPort.h
    Driver.h
    DucComponent.h
    NbddcComponent.h
    NbddcGroupComponent.h
    RadioComponent.h
    RadioHandler.h
    RadioTransport.h
    SimpleIpSetup.h
    TransmitterComponent.h
    TunerComponent.h
    VitaIfSpec.h
    WbddcComponent.h
    WbddcGroupComponent.h
)
ADD_CUSTOM_TARGET(libcyberradio_headers_Driver
    SOURCES ${libcyberradio_headers_Driver}
)
INSTALL(FILES
    ${libcyberradio_headers_Driver}
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Driver
)

########################################################################
# Subdirectories for Individual Radio Support
########################################################################
ADD_SUBDIRECTORY(NDR308)
ADD_SUBDIRECTORY(NDR308TS)
ADD_SUBDIRECTORY(NDR472)
ADD_SUBDIRECTORY(NDR651)
ADD_SUBDIRECTORY(NDR810)

