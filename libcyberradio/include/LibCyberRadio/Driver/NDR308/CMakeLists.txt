########################################################################
# Install Public Header Files
########################################################################
# The LIST()-ADD_CUSTOM_TARGET() construction enables these headers
# to be listed in CMake projects for QT Creator and other IDEs.
LIST(APPEND libcyberradio_headers_Driver_NDR308
    DataPort.h
    RadioHandler.h
    NbddcComponent.h
    NbddcGroupComponent.h
    TunerComponent.h
    VitaIfSpec.h
    WbddcComponent.h
    WbddcGroupComponent.h
)
ADD_CUSTOM_TARGET(libcyberradio_headers_Driver_NDR308
    SOURCES ${libcyberradio_headers_Driver_NDR308}
)
INSTALL(FILES
    ${libcyberradio_headers_Driver_NDR308}
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Driver/NDR308
)
