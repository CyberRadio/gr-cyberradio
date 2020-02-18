########################################################################
# Install Public Header Files
########################################################################
# The list()-add_custom_target() construction enables these headers
# to be listed in CMake projects for QT Creator and other IDEs.
LIST(APPEND libcyberradio_headers_Driver_NDR651
    CWToneGenComponent.h
    DataPort.h
    DucComponent.h
    NbddcComponent.h
    NbddcGroupComponent.h
    RadioHandler.h
    TransmitterComponent.h
    TunerComponent.h
    VitaIfSpec.h
    WbddcComponent.h
    WbddcGroupComponent.h
)
ADD_CUSTOM_TARGET(libcyberradio_headers_Driver_NDR651
    SOURCES ${libcyberradio_headers_Driver_NDR651}
)
INSTALL(FILES
    ${libcyberradio_headers_Driver_NDR651}
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Driver/NDR651
)
