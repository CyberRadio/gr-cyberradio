########################################################################
# Install Public Header Files
########################################################################
install(FILES
    BasicDict.h
    BasicList.h
    Debuggable.h
    Pythonesque.h
    Thread.h
    Throttle.hpp
    VitaIqSource.h
    VitaIqUdpPort.h
    Vita49Packet.h
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Common
)
