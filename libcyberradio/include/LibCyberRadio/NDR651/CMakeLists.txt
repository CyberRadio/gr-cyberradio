########################################################################
# Install Public Header Files
########################################################################
install(FILES
    DUCSink.h
    ClientSocket.h
    FlowControlClient.h
    PacketTypes.h
    TransmitPacketizer.h
    TransmitSocket.h
    UdpStatusReceiver.h
    DESTINATION ${LIBCYBERRADIO_INCLUDE_DIR}/NDR651
)
