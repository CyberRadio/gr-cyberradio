########################################################################
# Example Applications
########################################################################
# To add a new example application:
# (1) Use list(APPEND ...) to create a list of source files
# (2) Use set() to define the name of the example application
# (3) Use add_executable() to add the example app to the project
# (4) If necessary, use target_link_libraries() and link_directories()
#     to link in external libraries
# (5) Use install(TARGETS ...) to install the example app
# (6) Use install(FILES ...) to install the source files for the example 

########################################################################
# testvitaiq
########################################################################
list(APPEND testvitaiq_sources
     testvitaiq.cpp)
set(testvitaiq_executable testvitaiq)
add_executable(${testvitaiq_executable} ${testvitaiq_sources})
target_link_libraries(${testvitaiq_executable}
                      cyberradio 
                      ${Boost_LIBRARIES} 
                      )
link_directories(
    ${CMAKE_BINARY_DIR}/libcyberradio}
    ${Boost_LIBRARY_DIRS}
)
install(TARGETS ${testvitaiq_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
install(FILES ${testvitaiq_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

########################################################################
# NDR651 TX Example
########################################################################
list(APPEND ndr651_tx_test_sources
     ndr651_tx_test.cpp)
set(ndr651_tx_test_executable ndr651_tx_test)
add_executable(${ndr651_tx_test_executable} ${ndr651_tx_test_sources})
target_link_libraries(${ndr651_tx_test_executable}
                      cyberradio 
                      ${Boost_LIBRARIES} 
                      )
link_directories(
    ${CMAKE_BINARY_DIR}/libcyberradio}
    ${Boost_LIBRARY_DIRS}
)
install(TARGETS ${ndr651_tx_test_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
install(FILES ${ndr651_tx_test_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )


########################################################################
# NDR651 TXClient Example
########################################################################
list(APPEND TXClientDriver_sources
     TXClientDriver.cpp)
set(TXClientDriver_executable TXClientDriver)
add_executable(${TXClientDriver_executable} ${TXClientDriver_sources})
target_link_libraries(${TXClientDriver_executable}
                      cyberradio 
                      ${Boost_LIBRARIES} 
                      )
link_directories(
    ${CMAKE_BINARY_DIR}/libcyberradio}
    ${Boost_LIBRARY_DIRS}
)
install(TARGETS ${TXClientDriver_executable}
        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )
install(FILES ${TXClientDriver_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

########################################################################
# NDR651 SyncTXClient Example
########################################################################
list(APPEND SyncTXClientDriver_sources
     SyncTXClientDriver.cpp)
#set(SyncTXClientDriver_executable SyncTXClientDriver)
#add_executable(${SyncTXClientDriver_executable} ${SyncTXClientDriver_sources})
#target_link_libraries(${SyncTXClientDriver_executable}
#                      cyberradio 
#                      ${Boost_LIBRARIES}
#                      gnuradio-digital
#                      )
link_directories(
    ${CMAKE_BINARY_DIR}/libcyberradio}
    ${Boost_LIBRARY_DIRS}
)
#install(TARGETS ${SyncTXClientDriver_executable}
#        RUNTIME DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
#        )
install(FILES ${SyncTXClientDriver_sources}
        DESTINATION ${LIBCYBERRADIO_EXAMPLES_DIR}
        )

