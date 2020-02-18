#ifndef INCLUDED_LIBCYBERRADIO_NDR651_PACKETIZER_H
#define INCLUDED_LIBCYBERRADIO_NDR651_PACKETIZER_H

#define DAC_RATE 102400000

#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <linux/filter.h>
#include "LibCyberRadio/NDR651/TransmitSocket.h"
#include <netpacket/packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <unistd.h>
#include <ifaddrs.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <unistd.h>

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/NDR651/PacketTypes.h"

namespace LibCyberRadio
{
    namespace NDR651
    {

        class Packetizer : public Debuggable
        {

            private:
                std::string txInterfaceName;
                unsigned short txUdpPort;
                unsigned int samplesPerFrame;
                unsigned long long sampleRate;
                int txSocket;
                struct iovec txVec[3];  // Will hold Vita Header, Payload of Samples, Vita Footer
                uint32_t fracTimestampIncrement;

                /* Instance methods */
                void setVitaHeader(unsigned short streamId);
                void incrementVitaHeader();
                void initBroadcastTxSocket(const std::string &txInterfaceName, unsigned short port);
                unsigned long long calculateSampleRate(unsigned int ducRateIndex);


            public:
                Packetizer(const std::string &txInterfaceName, unsigned short port, unsigned int ducRateIndex, bool debug = false);
                ~Packetizer();

                int getSocketFd();
                void start();
                void sendFrame(short * samples);
                void setSamplesPerFrame(unsigned int samplesPerFrame);


        };
    }
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_PACKETIZER_H */
