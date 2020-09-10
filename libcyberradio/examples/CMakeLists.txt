########################################################################
# Example Applications
########################################################################
# To add a new example application:
# (1) Use LIST(APPEND ...) to create a list of source files
# (2) Use SET() to define the name of the example application
# (3) Use ADD_EXECUTABLE() to add the example app to the project
# (4) If necessary, use TARGET_LINK_LIBRARIES() and LINK_DIRECTORIES()
#     to link in external libraries
# (5) Use INSTALL(TARGETS ...) to install the example app
# (6) Use INSTALL(FILES ...) to install the source files for the example 

# -- C++11 compiler support
IF(${CMAKE_MAJOR_VERSION} LESS "3")
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
ELSE()
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
ENDIF()

########################################################################
# testvitaiq
########################################################################
LIST(APPEND testvitaiq_sources
     testvitaiq.cpp)
SET(testvitaiq_executable testvitaiq)
ADD_EXECUTABLE(${testvitaiq_executable} ${testvitaiq_sources})
TARGET_LINK_LIBRARIES(${testvitaiq_executable}
                      cyberradio 
                      )
LINK_DIRECTORIES(
    ${CMAKE_BINARY_DIR}/libcyberradio}
)
INSTALL(TARGETS ${testvitaiq_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
INSTALL(FILES ${testvitaiq_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

########################################################################
# ndr651_driver
########################################################################
LIST(APPEND ndr651_driver_sources
     ndr651_driver.cpp)
SET(ndr651_driver_executable ndr651_driver)
ADD_EXECUTABLE(${ndr651_driver_executable} ${ndr651_driver_sources})
TARGET_LINK_LIBRARIES(${ndr651_driver_executable}
                      cyberradio 
                      )
LINK_DIRECTORIES(
    ${CMAKE_BINARY_DIR}/libcyberradio}
)
INSTALL(TARGETS ${ndr651_driver_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
INSTALL(FILES ${ndr651_driver_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

########################################################################
# NDR651 TX Example
########################################################################
LIST(APPEND ndr651_tx_test_sources
     ndr651_tx_test.cpp)
SET(ndr651_tx_test_executable ndr651_tx_test)
ADD_EXECUTABLE(${ndr651_tx_test_executable} ${ndr651_tx_test_sources})
TARGET_LINK_LIBRARIES(${ndr651_tx_test_executable}
                      cyberradio 
                      )
LINK_DIRECTORIES(
    ${CMAKE_BINARY_DIR}/libcyberradio}
)
INSTALL(TARGETS ${ndr651_tx_test_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
INSTALL(FILES ${ndr651_tx_test_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )


########################################################################
# NDR651 TXClient Example
########################################################################
LIST(APPEND TXClientDriver_sources
     TXClientDriver.cpp)
SET(TXClientDriver_executable TXClientDriver)
ADD_EXECUTABLE(${TXClientDriver_executable} ${TXClientDriver_sources})
TARGET_LINK_LIBRARIES(${TXClientDriver_executable}
                      cyberradio 
                      )
LINK_DIRECTORIES(
    ${CMAKE_BINARY_DIR}/libcyberradio}
)
INSTALL(TARGETS ${TXClientDriver_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
INSTALL(FILES ${TXClientDriver_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

########################################################################
# NDR651 SyncTXClient Example
#
# NOTE: Only the source code is installed for this example. Building
#    the example introduces a dependency on GNU Radio that we do not
#    want, as nothing else in the library relies on it.
#
########################################################################
LIST(APPEND SyncTXClientDriver_sources
     SyncTXClientDriver.cpp)
#SET(SyncTXClientDriver_executable SyncTXClientDriver)
#ADD_EXECUTABLE(${SyncTXClientDriver_executable} ${SyncTXClientDriver_sources})
#TARGET_LINK_LIBRARIES(${SyncTXClientDriver_executable}
#                      cyberradio 
#                      gnuradio-digital
#                      )
LINK_DIRECTORIES(
    ${CMAKE_BINARY_DIR}/libcyberradio}
)
#INSTALL(TARGETS ${SyncTXClientDriver_executable}
#        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
#        )
INSTALL(FILES ${SyncTXClientDriver_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

