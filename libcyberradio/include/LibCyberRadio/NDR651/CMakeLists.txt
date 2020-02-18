########################################################################
# Install Public Header Files
########################################################################
INSTALL(FILES
    DUCSink.h
    ClientSocket.h
    FlowControlClient.h
    PacketTypes.h
    StatusReceiver.h
    SyncTXClient.h
    Packetizer.h
    RadioController.h
    TransmitPacketizer.h
    TransmitSocket.h
    UdpStatusReceiver.h
    TXClient.h
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/NDR651
)
