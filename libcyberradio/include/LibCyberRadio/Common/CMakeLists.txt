########################################################################
# Install Public Header Files
########################################################################
INSTALL(FILES
    App.h
    BasicDict.h
    BasicList.h
    Debuggable.h
    HttpsSession.h
    Pythonesque.h
    SerialPort.h
    Thread.h
    Throttle.hpp
    VitaIqSource.h
    VitaIqUdpPort.h
    Vita49Packet.h
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/Common
)
