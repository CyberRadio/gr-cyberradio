/***************************************************************************
 * \file TransmitSocket.cpp
 *
 * \brief NDR651 transmitter socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

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
#include <iostream>


namespace LibCyberRadio
{
    namespace NDR651
    {

        TransmitSocket::TransmitSocket(const std::string& ifname, unsigned int sport) :
            _isBroadcast(true),
            _txBytes(0),
            _sendCount(0),
            _byteCount(0),
            _isRaw(geteuid()==0),
            _ifname(ifname),
            _sport(sport)
        {
            // TODO Auto-generated constructor stub
            //_ifname = ifname;
            //_usingRingBuffer = useRingBuffer;
            _makeSocket();
        }

        TransmitSocket::~TransmitSocket() {
            // TODO Auto-generated destructor stub
        }

        bool TransmitSocket::_makeRawSocket() {
            //~ std::cout << "\t..._makeRawSocket\n";
            int optval; /* flag value for setsockopt */
            int rv;
            struct sockaddr_ll addr; /* link layer address */

            //std::cout << "Creating socket...";
            _sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
            //if (_sockfd< 0)
            //std::cout << "ERROR?";
            //else
            //std::cout << "success!";
            //std::cout << std::endl;

            optval = 1;
            setsockopt(_sockfd, SOL_SOCKET, SO_REUSEADDR,
                    (const void *)&optval , sizeof(int));

            /* bind the socket */
            memset(&addr,0,sizeof(addr));
            addr.sll_family=AF_PACKET;
            addr.sll_protocol=htons(ETH_P_IP);
            addr.sll_ifindex=if_nametoindex(_ifname.c_str());

            //std::cout << "Binding socket...";
            if (bind(_sockfd,(struct sockaddr*)&addr,sizeof(addr))) {
                //std::cerr << "ERROR?";
            } else {
                //std::cout << "success!";
            }
            //std::cout << std::endl;
            return _sockfd>0;
        }

        bool TransmitSocket::_makeUdpSocket() {
            //~ std::cout << "\t..._makeUdpSocket\n";
            int rv;
            struct sockaddr_in serveraddr; /* server's addr */
            struct ifreq ifr;
            char str[INET_ADDRSTRLEN];

            _sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

            // get interface's IP address
            ifr.ifr_addr.sa_family = AF_INET;
            strncpy(ifr.ifr_name, "eth0", IFNAMSIZ-1);
            ioctl(_sockfd, SIOCGIFADDR, &ifr);

            int optval = 1;
            /*
             * Set the "resuse address" flag
             */
            //~ rv = setsockopt(_sockfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval, sizeof(int));

            /*
             * build the server's Internet address
             */
            memset((char *) &serveraddr, 0, sizeof(serveraddr));
            serveraddr.sin_family = AF_INET;
            serveraddr.sin_port = htons((unsigned short)_sport);
            serveraddr.sin_addr = ((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr;

            /*
             * bind: associate the parent socket with a port
             */
            //~ std::cout << "Binding socket...";
            //~ if (bind(_sockfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) < 0)
            //~ std::cerr << "ERROR?";
            //~ else
            //~ std::cout << "success!";

            /*
             * Set destination address
             */
            if (_isBroadcast||true) {
                rv = setsockopt(_sockfd, SOL_SOCKET, SO_BROADCAST, (const void *)&optval, sizeof(int) );
                //std::cout << "setsockopt SO_BROADCAST: " << ((rv==0)?"Success":"Fail") << std::endl;

                struct ifaddrs *ifap, *ifa;
                struct sockaddr_in *sa;
                char *addr;
                std::string retString;
                getifaddrs (&ifap);
                for (ifa = ifap; ifa; ifa = ifa->ifa_next) {
                    if ( strcmp(ifa->ifa_name,_ifname.c_str())==0 ){
                        if (ifa->ifa_addr->sa_family==AF_INET) {
                            sa = (struct sockaddr_in *) ifa->ifa_ifu.ifu_broadaddr;
                            sa->sin_port = htons(_sport);
                            addr = inet_ntoa(sa->sin_addr);
                            rv = connect(_sockfd, (struct sockaddr *)sa, sizeof(sockaddr_in));
                            //~ std::cout << "Connect: " << ((rv==0)?"Success":"Fail") << std::endl;
                            break;
                        }
                    }
                }
                freeifaddrs(ifap);

            } else {
                std::cerr << "I NEED A DESTINATION ADDRESS" << std::endl;
            }

            //~ rv = setsockopt(_sockfd, SOL_SOCKET, SO_BINDTODEVICE, _ifname.c_str(), IF_NAMESIZE);
            return _sockfd>0;
        }

        bool TransmitSocket::_makeSocket() {
            //~ std::cout << "_makeSocket...\n";
            if (_isRaw) {
                return _makeRawSocket();
            } else {
                return _makeUdpSocket();
            }
        }

        std::string TransmitSocket::getMacAddress() {
            // Source MAC Address
            char macstring[32];
            struct ifreq ifr;
            memset(&ifr, 0x00, sizeof(ifr));
            strcpy(ifr.ifr_name, _ifname.c_str());
            ioctl(_sockfd, SIOCGIFHWADDR, &ifr);
            sprintf(macstring, "%02x:%02x:%02x:%02x:%02x:%02x",
                    (unsigned char)ifr.ifr_hwaddr.sa_data[0],
                    (unsigned char)ifr.ifr_hwaddr.sa_data[1],
                    (unsigned char)ifr.ifr_hwaddr.sa_data[2],
                    (unsigned char)ifr.ifr_hwaddr.sa_data[3],
                    (unsigned char)ifr.ifr_hwaddr.sa_data[4],
                    (unsigned char)ifr.ifr_hwaddr.sa_data[5]);
            return std::string(macstring);
        }

        std::string TransmitSocket::getIpAddress() {
            struct ifreq ifr;
            /* I want to get an IPv4 IP address */
            ifr.ifr_addr.sa_family = AF_INET;
            /* I want IP address attached to "eth0" */
            strncpy(ifr.ifr_name, _ifname.c_str(), IFNAMSIZ-1);
            ioctl(_sockfd, SIOCGIFADDR, &ifr);
            /* display result */
            return std::string(inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));
        }

        std::string TransmitSocket::getIpBroadcastAddress() {
            struct ifaddrs *ifap, *ifa;
            struct sockaddr_in *sa;
            char *addr;
            getifaddrs (&ifap);
            for (ifa = ifap; ifa; ifa = ifa->ifa_next) {
                if ( strcmp(ifa->ifa_name,_ifname.c_str())==0 ){
                    if (ifa->ifa_addr->sa_family==AF_INET) {
                        sa = (struct sockaddr_in *) ifa->ifa_ifu.ifu_broadaddr;
                        addr = inet_ntoa(sa->sin_addr);
                        break;
                    }
                }
            }
            freeifaddrs(ifap);
            return std::string(addr);
        }

        bool TransmitSocket::sendFrame(unsigned char * frame, const int & frameLen) {
            _txMutex.lock();
            _txBytes = send(_sockfd, frame, frameLen, 0);
            _txMutex.unlock();
            _sendCount ++;
            _byteCount += _txBytes;
            return (_txBytes>0);
        }

    } /* namespace NDR651 */
}
