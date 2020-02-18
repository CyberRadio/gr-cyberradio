########################################################################
# Install Public Header Files
########################################################################
# The LIST()-ADD_CUSTOM_TARGET() construction enables these headers
# to be listed in CMake projects for QT Creator and other IDEs.
LIST(APPEND libcyberradio_headers_Driver_NDR308TS
    DataPort.h
    RadioHandler.h
    NbddcComponent.h
    NbddcGroupComponent.h
    TunerComponent.h
    VitaIfSpec.h
    WbddcComponent.h
    WbddcGroupComponent.h
)
ADD_CUSTOM_TARGET(libcyberradio_headers_Driver_NDR308TS
    SOURCES ${libcyberradio_headers_Driver_NDR308TS}
)
INSTALL(FILES
    ${libcyberradio_headers_Driver_NDR308TS}
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Driver/NDR308TS
)
