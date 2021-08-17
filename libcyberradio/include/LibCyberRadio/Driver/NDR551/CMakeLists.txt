########################################################################
# Install Public Header Files
########################################################################
# The LIST()-ADD_CUSTOM_TARGET() construction enables these headers
# to be listed in CMake projects for QT Creator and other IDEs.
LIST(APPEND libcyberradio_headers_Driver_NDR551
    RadioHandler.h
    VitaIfSpec.h
)
ADD_CUSTOM_TARGET(libcyberradio_headers_Driver_NDR551
    SOURCES ${libcyberradio_headers_Driver_NDR308}
)
INSTALL(FILES
    ${libcyberradio_headers_Driver_NDR551}
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Driver/NDR551
)
