#include "LibCyberRadio/NDR651/Packetizer.h"

namespace LibCyberRadio
{
    namespace NDR651
    {
        // Constructor
        Packetizer::Packetizer(const std::string &txInterfaceName, unsigned short txUdpPort, unsigned int ducRateIndex, bool debug) :
            Debuggable(debug, "Packetizer"),
            txInterfaceName(txInterfaceName),
            txUdpPort(txUdpPort),
            samplesPerFrame(1024),
            sampleRate(calculateSampleRate(ducRateIndex)),
            txSocket(-1),
            fracTimestampIncrement(2048)
        {

            // An IO Vector is used to handle transmitting the header, payload, and footer consisely.
            // Vita Header
            this->txVec[0].iov_base = new char[sizeof(struct LibCyberRadio::NDR651::Vita49Header)];
            this->txVec[0].iov_len = sizeof(struct LibCyberRadio::NDR651::Vita49Header);
            // Sample Payload
            this->txVec[1].iov_base = NULL;
            this->txVec[1].iov_len = 0;
            // Vita Footer
            this->txVec[2].iov_base = new char[sizeof(struct LibCyberRadio::NDR651::Vita49Trailer)];
            this->txVec[2].iov_len = sizeof(struct LibCyberRadio::NDR651::Vita49Trailer);

        }

        // Destructor
        Packetizer::~Packetizer()
        {
            if (this->txSocket >= 0)
            {
                close(this->txSocket);
            }

            // Free txVec
            if (this->txVec[0].iov_base != NULL)
            {
                delete [] (char *)(this->txVec[0].iov_base);
            }
            if (this->txVec[2].iov_base != NULL)
            {
                delete [] (char *)(this->txVec[2].iov_base);
            }

            this->debug("Exiting Packetizer\n");
        }

        /* Public */
        // 1) Sends a frame
        // 2) Increments Vita Headers
        void Packetizer::sendFrame(short * samples)
        {
            if (this->txSocket >= 0)
            {
                // Set out txVec to point to the current samples
                this->txVec[1].iov_base = (char *)(samples);
                this->txVec[1].iov_len = 4*(this->samplesPerFrame);
                int bytesSent = writev(this->txSocket, this->txVec, 3);
                this->incrementVitaHeader();
            }
        }

        void Packetizer::setSamplesPerFrame(unsigned int samplesPerFrame){
            this->samplesPerFrame = samplesPerFrame;
            this->setVitaHeader(this->txUdpPort);

        }

        void Packetizer::start()
        {
            this->debug("Starting the Packetizer\n");
            this->initBroadcastTxSocket(txInterfaceName, txUdpPort);
            this->setVitaHeader(txUdpPort);
        }

        int Packetizer::getSocketFd()
        {
            return this->txSocket;
        }

        /* Private */
        void Packetizer::setVitaHeader(unsigned short streamId)
        {
            // Determine sampleCount
            this->fracTimestampIncrement = ((unsigned long long)(DAC_RATE) / (this->sampleRate * 2)) * (this->samplesPerFrame*2);

            //Vita49
            struct LibCyberRadio::NDR651::Vita49Header *hdr = (struct LibCyberRadio::NDR651::Vita49Header *)(this->txVec[0].iov_base);
            struct LibCyberRadio::NDR651::Vita49Trailer *ftr = (struct LibCyberRadio::NDR651::Vita49Trailer *)(this->txVec[2].iov_base);
            hdr->frameStart = VRLP;
            hdr->frameSize = this->samplesPerFrame+10;
            hdr->streamId = streamId;
            hdr->packetType = 0x1;
            hdr->TSF = 0x1;
            hdr->TSF = 0x1;
            hdr->T = 0;
            hdr->C = 1;
            hdr->classId1 = 0x00fffffa;
            hdr->classId2 = 0x00130000;
            hdr->packetSize = this->samplesPerFrame+7;
            hdr->timeSeconds = 0;
            hdr->timeFracSecMSB = 0;
            hdr->timeFracSecLSB = 0;
            ftr->frameEnd = VEND;
        }

        void Packetizer::incrementVitaHeader()
        {
            struct LibCyberRadio::NDR651::Vita49Header *hdr = (struct LibCyberRadio::NDR651::Vita49Header *)(this->txVec[0].iov_base);
            hdr->frameCount = (hdr->frameCount + 1) % 4*(this->samplesPerFrame);
            hdr->packetCount = (hdr->packetCount + 1) % 16;

            if ((hdr->timeFracSecLSB + this->fracTimestampIncrement) >= DAC_RATE)
            {
                hdr->timeSeconds++;
            }
            hdr->timeFracSecLSB = (hdr->timeFracSecLSB + this->fracTimestampIncrement) % DAC_RATE;
        }

        void Packetizer::initBroadcastTxSocket(const std::string &txInterfaceName, unsigned short port)
        {
            // Used for both setsockopt and connect
            int rv;

            // Create a generic UDP Socket
            int sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
            if (sockfd < 0)
            {
                perror("");
                throw std::runtime_error("Could not create socket");
            }

            // Set the socket to broadcast mode
            int optval = 1;
            rv = setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, (const void *)&optval, sizeof(int) );
            if (rv != 0)
            {
                perror("");
                throw std::runtime_error("Could not set broadcast sockopt");
            }

            // Determine the broadcast IP (x.x.x.255) of the interface
            struct ifreq ifr;
            struct ifaddrs *ifap, *ifa;
            struct sockaddr_in *sa;
            char *addr;
            std::string retString;
            getifaddrs (&ifap);
            for (ifa = ifap; ifa; ifa = ifa->ifa_next) {
                if ( strcmp(ifa->ifa_name,txInterfaceName.c_str())==0 ){
                    if (ifa->ifa_addr->sa_family==AF_INET) {
                        sa = (struct sockaddr_in *) ifa->ifa_ifu.ifu_broadaddr;
                        sa->sin_port = htons(port);
                        addr = inet_ntoa(sa->sin_addr);
                        break;
                    }
                }
            }
            freeifaddrs(ifap);

            // Connect to the broadcast address (you cant't REALLY connect to a UDP socket, but it does allow us to call send instead of sendto)
            rv = connect(sockfd, (struct sockaddr *)sa, sizeof(sockaddr_in));
            if (rv != 0)
            {
                perror("");
                throw std::runtime_error("Could not call connect on the UDP socket");
            }

            // Success
            this->txSocket = sockfd;

        }

        unsigned long long Packetizer::calculateSampleRate(unsigned int ducRateIndex)
        {
            switch(ducRateIndex) {
                case 0:
                    return 102400000;
                case 1:
                    return 51200000;
                case 2:
                    return 25600000;
                case 3:
                    return 12800000;
                case 4:
                    return 6400000;
                case 5:
                    return 3200000;
                case 6:
                    return 1600000;
                case 7:
                    return 800000;
                case 8:
                    return 400000;
                case 9:
                    return 200000;
                case 10:
                    return 100000;
                case 11:
                    return 50000;
                case 12:
                    return 25000;
                case 13:
                    return 12500;
                default:
                    return 0;
            }

        }

    }
}
