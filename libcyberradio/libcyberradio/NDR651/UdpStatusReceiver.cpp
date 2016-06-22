/*
 * UdpStatusReceiver.cpp
 *
 *  Created on: Dec 1, 2015
 *      Author: nh
 */
#include <cstdio>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "LibCyberRadio/NDR651/PacketTypes.h"
#include "LibCyberRadio/NDR651/UdpStatusReceiver.h"
#include <sys/types.h>
#include <sys/ioctl.h>
#include <net/if.h>


namespace LibCyberRadio {

	namespace NDR651 {

		UdpStatusReceiver::UdpStatusReceiver(std::string ifname, unsigned int port, bool debug) :
			LibCyberRadio::Thread("UdpStatusReceiver", "UdpStatusReceiver"),
			LibCyberRadio::Debuggable(debug, "UdpStatusReceiver"),
			_sockfd(-1),
			_shutdown(false),
			_651freeSpace(0),
			_sendLock(false),
			_ifname(ifname),
			_port(port)
		{
			// TODO Auto-generated constructor stub
			bzero(&_rxbuff, MAX_RX_SIZE);
			FD_ZERO(&set);
			_makeSocket();
		}

		UdpStatusReceiver::~UdpStatusReceiver() {
			// TODO Auto-generated destructor stub
			this->debug("Interrupting\n");
			if (this->isRunning()) {
				this->interrupt();
			}
			_shutdown = true;
			this->_fcMutex.lock();
			this->_selMutex.lock();
			if (_sockfd>=0) {
				this->debug("Closing socket\n");
				//TODO: Close the socket...
				//  this interferes with the select statement in run(), so care must be taken.
			}
			this->debug("Goodbye!\n");
		}

		bool UdpStatusReceiver::_makeSocket(void) {
			int optval; /* flag value for setsockopt */
			struct sockaddr_in serveraddr; /* server's addr */
			char ip_addr_string[INET_ADDRSTRLEN];
			_selMutex.lock();
			// Kill existing socket if it exists.
			if (_sockfd>=0) {
				close(_sockfd);
				_sockfd = -1;
				FD_ZERO(&set);
			}
			// Create new socket.
			if ((_sockfd<0)&&(_port>0)) {
				_sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
				if (_sockfd<0) {
					std::cerr << "Error opening socket" << std::endl;
					return false;
				}

				optval = 1;
				setsockopt(_sockfd, SOL_SOCKET, SO_REUSEADDR,
					(const void *)&optval , sizeof(int));

				// We're binding to a specific device. With this, we won't need to bind to an IP.
				setsockopt(_sockfd, SOL_SOCKET, SO_BINDTODEVICE,
					(void *)_ifname.c_str(), _ifname.length()+1);

				/*
				* build the server's Internet address
				*/
				memset((char *) &serveraddr, 0, sizeof(serveraddr));
				serveraddr.sin_family = AF_INET;
				serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
				inet_ntop(AF_INET, &(serveraddr.sin_addr), ip_addr_string, INET_ADDRSTRLEN);
				serveraddr.sin_port = htons((unsigned short)_port);
				/*
				* bind: associate the parent socket with a port
				*/
				if (bind(_sockfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) < 0) {
					std::cerr << "ERROR on binding socket" << std::endl;
					_sockfd = -1;
					return false;
				}
				FD_ZERO(&set);
				FD_SET(_sockfd, &set);
			}
			_selMutex.unlock();
			return _sockfd>=0;
		}

		bool UdpStatusReceiver::setStatusInterface(std::string ifname) {
			return setStatusInterface(ifname, true);
		}

		bool UdpStatusReceiver::setStatusInterface(std::string ifname, bool makeSocketFlag) {
			_ifname = ifname;
			if (makeSocketFlag) {
				return _makeSocket();
			} else {
				return true;
			}
		}

		bool UdpStatusReceiver::setStatusPort(unsigned int port) {
			_port = port;
			return setStatusPort(port, true);
		}

		bool UdpStatusReceiver::setStatusPort(unsigned int port, bool makeSocketFlag) {
			_port = port;
			if (makeSocketFlag) {
				return _makeSocket();
			} else {
				return true;
			}
		}

		void UdpStatusReceiver::run() {
			struct timeval tout;
			struct sockaddr_in clientaddr; /* client addr */
			socklen_t clientlen = sizeof(clientaddr); /* byte size of client's address */
			struct TxStatusFrame * status;
			int numBytesRx;
			while(this->isRunning() && (!_shutdown)) {
				tout.tv_sec = (long int) 0;
				tout.tv_usec = (long int) 250000;
				_selMutex.lock();
				if (select(FD_SETSIZE, &set, NULL, NULL, &tout)>0) {
					numBytesRx = recvfrom(_sockfd, _rxbuff, MAX_RX_SIZE, 0, (struct sockaddr *) &clientaddr, &clientlen);
					_selMutex.unlock();
					if (numBytesRx==sizeof(TxStatusFrame)) {
						_fcMutex.lock();
						status = (struct TxStatusFrame *)_rxbuff;
						_651freeSpace = ((long int) status->status.spaceAvailable);
						_fcMutex.unlock();
						if (status->status.underrunFlag || status->status.emptyFlag) {
							std::cerr << "_u" << status->v49.streamId << "@" << status->v49.timeSeconds << "_" << std::flush;
						}
					}
				} else {
					_selMutex.unlock();
					this->debug("Timeout\n");
					usleep(1000);
				}
			}
		}

		bool UdpStatusReceiver::okToSend(long int numSamples, bool lockIfOk) {
			_fcMutex.lock();
			bool ok = _651freeSpace>=numSamples;
			if (!(ok&&lockIfOk)) {
				_fcMutex.unlock();
			} else {
				_sendLock = true;
			}
			return ok;
		}

		long int UdpStatusReceiver::getFreeSpace(void) {
			boost::mutex::scoped_lock lock(_fcMutex);
			return _651freeSpace;
		}

		bool UdpStatusReceiver::sentNSamples(long int samplesSent) {
			if (!_sendLock) {
				_fcMutex.lock();
			}
			_651freeSpace -= samplesSent;
			_fcMutex.unlock();
			return _651freeSpace>0;
		}

	} /* namespace NDR651 */

} /* namespace CyberRadio */
