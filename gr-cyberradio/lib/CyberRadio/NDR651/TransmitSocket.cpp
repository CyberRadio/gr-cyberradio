/***************************************************************************
 * \file TransmitSocket.cpp
 *
 * \brief NDR651 transmitter socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include "TransmitSocket.h"

#include <sys/socket.h>
#include <netinet/in.h>
#include <linux/if_ether.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <linux/filter.h>
#include <netpacket/packet.h>
#include <net/ethernet.h>
#include <net/if.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <stdio.h>

namespace gr
{
	namespace CyberRadio
	{
		namespace NDR651
		{

			TransmitSocket::TransmitSocket(const std::string& ifname, bool useRingBuffer) {
				// TODO Auto-generated constructor stub
				_ifname = ifname;
				_usingRingBuffer = useRingBuffer;

				//std::cout << "Tx using RAW" << std::endl;
				int optval; /* flag value for setsockopt */
				int rv;
				struct sockaddr_ll addr; /* link layer address */

				//std::cout << "Creating socket...";
				_sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
		//		if (_sockfd< 0)
		//			std::cout << "ERROR?";
		//		else
		//			std::cout << "success!";
		//		std::cout << std::endl;

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
			}

			TransmitSocket::~TransmitSocket() {
				// TODO Auto-generated destructor stub
			}

			bool TransmitSocket::_makeSocket() {
				//std::cout << "Tx using RAW" << std::endl;
				int optval; /* flag value for setsockopt */
				int rv;
				struct sockaddr_ll addr; /* link layer address */

				//std::cout << "Creating socket...";
				_sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
		//		if (_sockfd< 0)
		//			std::cout << "ERROR?";
		//		else
		//			std::cout << "success!";
		//		std::cout << std::endl;

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

				return (_sockfd>0);
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
}
