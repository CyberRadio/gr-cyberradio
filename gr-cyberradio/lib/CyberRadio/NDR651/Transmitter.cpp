/***************************************************************************
 * \file Transmitter.cpp
 *
 * \brief NDR651 transmitter class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include <stdio.h>
#include <stdlib.h>     /* strtol */
#include <boost/algorithm/string.hpp>
#include <boost/tokenizer.hpp>
#include <boost/format.hpp>
#include <iostream>
#include "Transmitter.h"
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <net/if.h>
#include <boost/interprocess/sync/scoped_lock.hpp>
#include <boost/interprocess/sync/named_mutex.hpp>

using namespace boost::algorithm;
using namespace boost::interprocess;

namespace gr
{
	namespace CyberRadio
	{
		namespace NDR651
		{
			static unsigned short compute_checksum(unsigned short *addr, unsigned int count) {
				register unsigned long sum = 0;
				while (count > 1) {
					//std::cout << count << "  |  " << *addr << "  |  " << sum << std::endl;
					sum += * addr++;
					count -= 2;
				}
				//if any bytes left, pad the bytes and add
				if(count > 0) {
					sum += ((*addr)&htons(0xFF00));
				}
				//Fold sum to 16 bits: add carrier to result
				while (sum>>16) {
					sum = (sum & 0xffff) + (sum >> 16);
				}
				//one's complement
				sum = ~sum;
				return ((unsigned short)sum);
			}

			Transmitter::Transmitter(std::string ifname, unsigned int ducChannel, unsigned int udpPort, bool udpInsteadOfRaw, bool useRingBuffer) {
				// TODO Auto-generated constructor stub
				_ifname = ifname;
				_ducChannel = ducChannel;
				_sport = udpPort;
				_usingRingBuffer = useRingBuffer;
				_usingUdp = _usingRingBuffer?false:udpInsteadOfRaw;

			//	std::string mutexName( (boost::format("%s_651flow") % ifname).str() );
			//	std::cout << "Trying to open||create a named mutex: " << boost::format("%s_651flow") % ifname << std::endl;

				_clearBuffer();
				_mapFrameToBuffer();
				if ( _makeSocket() ) {

				}
			}

			Transmitter::~Transmitter() {
				// TODO Auto-generated destructor stub
			}

			void Transmitter::_mapFrameToBuffer() {
				_frame = (struct TxFrame *)_buffer;
				_frameStart = _buffer;
				_frameLength = sizeof(TxFrame);
				if (_usingUdp) {
					// TODO create udp frame instead of Raw frame
					//    ...or maybe always use a raw frame and just point to vita49 payload instead of ethernet header when sending
					//    yeah, let's try that instead so I don't have to change pointer types and all that junk.
					//    we can always fix this, but it's not that many wasted bytes in memory so I'm not worried.
					_frameStart = _frameStart + sizeof(ethhdr) + sizeof(iphdr) + sizeof(udphdr);
					_frameLength -= (_frameStart-_buffer);
				}
			}

			bool Transmitter::_makeRawSocket() {
				//std::cout << "Tx using RAW" << std::endl;
				int optval; /* flag value for setsockopt */
				int rv;
				struct sockaddr_ll addr; /* link layer address */

				//std::cout << "Creating socket...";
				_sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_IP));
			//	if (_sockfd< 0)
			//		std::cout << "ERROR?";
			//	else
			//		std::cout << "success!";
			//	std::cout << std::endl;

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

			//	if (_usingRingBuffer) {
			//		std::cout << "Allocating ring buffer...";
			//		struct tpacket_req ring;
			//		ring.tp_block_size = blkSize;
			//		ring.tp_block_nr = blkCount;
			//		ring.tp_frame_size = blkSize/frmPerBlock;
			//		ring.tp_frame_nr = blkCount*frmPerBlock;
			//
			//		rv = setsockopt(rawSock, SOL_PACKET, PACKET_TX_RING, &ring, sizeof(ring));
			//		int s = blkSize*blkCount;
			//		void * mem = mmap(0, s, PROT_READ|PROT_WRITE, MAP_SHARED, _sockfd, 0);
			//		if (mem==(void*)-1) {
			//			std::cout << "Failure?";
			//		} else {
			//			std::cout << "Success!";
			//		}
			//		std::cout << std::endl;
			//	}

				return _sockfd>0;
			}
	
			bool Transmitter::_makeUdpSocket() {
				//std::cout << "Tx using UDP" << std::endl;
				int rv;
				struct sockaddr_in serveraddr; /* server's addr */
				struct ifreq ifr;

				_sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);

				// get interface's IP address
				ifr.ifr_addr.sa_family = AF_INET;
				strncpy(ifr.ifr_name, _ifname.c_str(), IFNAMSIZ-1);
				ioctl(_sockfd, SIOCGIFADDR, &ifr);

				/*
				* build the server's Internet address
				*/
				memset((char *) &serveraddr, 0, sizeof(serveraddr));
				serveraddr.sin_family = AF_INET;
				serveraddr.sin_port = htons((unsigned short)_sport);
				serveraddr.sin_addr = ((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr;

				int optval = 1;
					rv = setsockopt(_sockfd, SOL_SOCKET, SO_REUSEADDR, (const void *)&optval , sizeof(int));

				/*
				* bind: associate the parent socket with a port
				*/
				//std::cout << "Binding socket...";
				if (bind(_sockfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) < 0) {
					// std::cerr << "ERROR?";
				} else {
					//std::cout << "success!";
				}


				rv = setsockopt(_sockfd, SOL_SOCKET, SO_BINDTODEVICE, _ifname.c_str(), IF_NAMESIZE);

				return _sockfd>0;
			}

			bool Transmitter::_makeSocket() {
				if (_usingUdp) {
					return _makeUdpSocket();
				} else {
					return _makeRawSocket();
				}
			}

			bool Transmitter::buildFrameHeaders(std::string dmac, std::string dip, unsigned int dport, unsigned int streamId) {
				bool success = true;
				if (_usingUdp) {
					memset((char *) &_radioAddr, 0, sizeof(_radioAddr));
					_radioAddr.sin_family = AF_INET;
					inet_pton(_radioAddr.sin_family, dip.c_str(), &(_radioAddr.sin_addr));
					_radioAddr.sin_port = htons(dport);

					//TODO: Replace the following system() call with the ioctl to manually add the radio to the ARP table
					// also, the whole arpCmd thing is probably stupid, but it works. I'm not losing sleep over it, but we should probably make it nicer.
					std::string arpCmd = (boost::format("arp -s %s %s -i %s") % dip % dmac % _ifname).str();
					//std::cout << "Issuing ARP Command: " << arpCmd << ", rv = ";
					int rv = system(arpCmd.c_str());
					std::cout << rv << ", ";
					if (rv==0) {
						//std::cout << "SUCCESS!";
					} else {
						//std::cout << "FAILURE?";
					}
				}
				std::cout << std::endl;
				success &= _initEthernetHeader(dmac);
				success &= _initIpHeader(dip);
				success &= _initUdpHeader(dport, _sport);
				success &= _initVitaHeader(streamId);
				return success;
			}

			bool Transmitter::_initEthernetHeader(std::string dmac) {
				// Destination MAC Address
				std::vector<std::string> macVec;
				split(macVec, dmac, is_any_of(":"));
				//std::cout << "header dMAC = ";
				int ind = 0;
				for (std::vector<std::string>::iterator i=macVec.begin(); i!=macVec.end(); i++) {
					unsigned char val = strtol((*i).c_str(), NULL, 16);
					//std::cout << "  " << (*i) << " (" << (int)val << ")";
					_frame->eth.h_dest[ind++] = val;
				}
				//std::cout << std::endl;

				// Source MAC Address
				struct ifreq buffer;
				memset(&buffer, 0x00, sizeof(buffer));
				strcpy(buffer.ifr_name, _ifname.c_str());
				ioctl(_sockfd, SIOCGIFHWADDR, &buffer);
				//std::cout << "header dMAC = " << buffer.ifr_hwaddr.sa_data;
				for (int i=0; i<6; i++) {
					unsigned char val = (buffer.ifr_hwaddr.sa_data[i])&0xff;
					//std::cout << boost::format(" @i=%d->'%d' ") % i % (int)val;
					//printf("%.2X ", val);
					_frame->eth.h_source[i] = val;
				}
				//std::cout << std::endl;

				_frame->eth.h_proto = htons(ETH_P_IP);

				//Vita49
				_frame->v49.frameStart = 0x56524c50;
				_frame->vend.frameEnd = 0x56454e44;

				return true;
			}

			bool Transmitter::_initIpHeader(std::string dip) {
				_frame->ip.version = 4;
				_frame->ip.ihl = sizeof(iphdr)/4;
			//	_frame->ip.frag_off = htons(0x4000);
				_frame->ip.protocol = 17;
				_frame->ip.tot_len = htons(sizeof(TxFrame)-sizeof(ethhdr));
				_frame->ip.ttl = 255;

				// Destination IP address
				inet_pton(AF_INET, dip.c_str(), &(_frame->ip.daddr));

				// Add the source IP address. This is ugly, but it works. It was late when I created this from pieces found on the internet.
				struct ifreq ifr;
				/* I want to get an IPv4 IP address */
				ifr.ifr_addr.sa_family = AF_INET;
				/* I want IP address attached to "eth0" */
				strncpy(ifr.ifr_name, _ifname.c_str(), IFNAMSIZ-1);
				ioctl(_sockfd, SIOCGIFADDR, &ifr);
				/* display result */
				//printf("%s\n", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));
				inet_pton(AF_INET, inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr), &(_frame->ip.saddr));

				// IP Header checksum
				_frame->ip.check = 0;
				_frame->ip.check = compute_checksum((unsigned short*)&(_frame->ip), _frame->ip.ihl<<2);

				return true;
			}

			bool Transmitter::_initUdpHeader(unsigned int dport, unsigned int sport) {
				_frame->udp.source = htons(sport);
				_frame->udp.dest = htons(dport);
				_frame->udp.len = htons(sizeof(TxFrame)-sizeof(ethhdr)-sizeof(iphdr));
				return true;
			}

			bool Transmitter::_initVitaHeader(unsigned int streamId) {
				_frame->v49.frameStart = 0x56524c50;
				_frame->v49.streamId = streamId;
				_frame->v49.packetType = 0x1;
				_frame->v49.TSF = 0x1;
				_frame->v49.TSF = 0x1;
				_frame->v49.T = 0;
				_frame->v49.C = 1;
				_frame->v49.classId1 = 0x00fffffa;
				_frame->v49.classId2 = 0x00130000;
				_frame->v49.frameSize = SAMPLES_PER_FRAME+10;
				_frame->v49.packetSize = SAMPLES_PER_FRAME+7;
				_frame->vend.frameEnd = 0x56454e44;
				return true;
			}

			bool Transmitter::_incrementVitaHeader(void) {
				_frame->v49.frameCount+=1;
				_frame->v49.packetCount+=1;
				return true;
			}

			unsigned int Transmitter::getFrame(const short * samples, unsigned char * frame) {
				// short amplitude = 0x0200;// + (short)(frameCount%0x0fff);
				short amplitude = 1;// + (short)(frameCount%0x0fff);
				for(int i=0; i<2*SAMPLES_PER_FRAME; i++) {
					_frame->payload.samples[i] = samples[i]*amplitude;
				}
				frame = _frameStart;
				return _frameLength;
			}

			int Transmitter::sendFrame(short * samples) {
			//	memcpy(_frame->payload.payload, samples, 4*SAMPLES_PER_FRAME);
				// short amplitude = 0x0200;// + (short)(frameCount%0x0fff);
				short amplitude = 1;// + (short)(frameCount%0x0fff);
				for(int i=0; i<2*SAMPLES_PER_FRAME; i++) {
					_frame->payload.samples[i] = samples[i]*amplitude;
				}
			//	scoped_lock<named_mutex> ethLock;
				if (_usingUdp) {
					_txBytes = sendto(_sockfd, _frameStart, _frameLength, 0, (struct sockaddr *) &_radioAddr, sizeof(_radioAddr));
				} else {
					_txBytes = send(_sockfd, _frameStart, _frameLength, 0);
				}
				if (_txBytes>0) {
					_incrementVitaHeader();
					frameCount++;
				} else {
					//std::cout << "Dropped frame?!?" << std::endl;
				}
				return SAMPLES_PER_FRAME;
			}

			int Transmitter::sendFrame(short * samples, NDR651::TransmitSocket * txsock) {
			//	memcpy(_frame->payload.payload, samples, 4*SAMPLES_PER_FRAME);
				//short amplitude = 0x0200;// + (short)(frameCount%0x0fff);
				short amplitude = 1;// + (short)(frameCount%0x0fff);
				for(int i=0; i<2*SAMPLES_PER_FRAME; i++) {
					_frame->payload.samples[i] = samples[i]*amplitude;
				}
				_txBytes = txsock->sendFrame(_frameStart, _frameLength);
				if (_txBytes>0) {
					_incrementVitaHeader();
					frameCount++;
				} else {
					//std::cout << "Dropped frame?!?" << std::endl;
				}
				return SAMPLES_PER_FRAME;
			}

		}
	}
}

