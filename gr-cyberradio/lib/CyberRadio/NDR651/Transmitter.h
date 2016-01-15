/***************************************************************************
 * \file Transmitter.h
 *
 * \brief NDR651 transmitter class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_TRANSMITTER_H
#define INCLUDED_CYBERRADIO_NDR651_TRANSMITTER_H

#include <string>
#include <string.h>

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

#include "CyberRadio/BasicList.h"
#include "CyberRadio/Thread.h"
#include "FlowControlClient.h"
#include "TransmitSocket.h"

#include <boost/interprocess/sync/named_mutex.hpp>

//struct ether_addr
//{
//  u_int8_t ether_addr_octet[ETH_ALEN];
//} __attribute__ ((__packed__));

#define MTU_BYTES 9000
#define MTU_WORDS MTU_BYTES/4
#define SAMPLES_PER_FRAME 2048

/*!
 * \brief Provides GNU Radio blocks.
 */
namespace gr
{
	/*!
	 * \brief Provides GNU Radio blocks for CyberRadio Solutions products.
	 */
	namespace CyberRadio
	{
		/*!
		 * \brief Provides processing units for controlling an NDR651 radio.
		 */
		namespace NDR651
		{
			// borrowed from http://gandalf/svn/WidebandRecorder/trunk/recorder/recorderd/frame.h
			struct Vita49Header {
				unsigned int frameStart;    //!< ASCII "VRLP"
				unsigned int frameSize:20;    /*!< bits 0:19 Frame size */
				unsigned int frameCount:12;   /*!< bits 20:31 Frame Count */
				unsigned short packetSize;    //!< should be 0x105 (261)
				unsigned short packetCount:4;
				unsigned short TSF:2;
				unsigned short TSI:2;
				unsigned short RSVD:2;
				unsigned short T:1;
				unsigned short C:1;
				unsigned short packetType:4;
				unsigned int streamId;       //!< stream ID
				unsigned int classId1;       //!< class ID
				unsigned int classId2;       //!< class ID
				unsigned int timeSeconds;    //!< UTC integer seconds
				unsigned int timeFracSecMSB; //!< fractional seconds MSW, always zero
				unsigned int timeFracSecLSB; //!< fractional seconds LSW (sample count)
			} __attribute__((packed));

			struct Payload {
				short samples[2*SAMPLES_PER_FRAME];
			} __attribute__((packed));

			struct Vita49Trailer {
				unsigned int frameEnd;
			} __attribute__((packed));

			struct TxFrame {
				struct ethhdr eth;  //!< ethernet header
				struct iphdr ip;    //!< ip header
				struct udphdr udp;  //!< udp header
				struct Vita49Header v49;
				struct Payload payload;
				struct Vita49Trailer vend;
			} __attribute__((packed));

			class Transmitter {
			private:
				unsigned char _buffer[MTU_BYTES];
				struct TxFrame * _frame;
				unsigned char * _frameStart;
				unsigned int _frameLength, _sport, _dip;
				int _sockfd;
				std::string _ifname;
				unsigned int _ducChannel;
				struct sockaddr_in _radioAddr;
				int _txBytes;
				bool _usingUdp, _usingRingBuffer;

				bool _makeUdpSocket(void);
				bool _makeRawSocket(void);
				bool _makeSocket(void);
				void _clearBuffer(void) { memset(_buffer,0,MTU_BYTES); };
				void _mapFrameToBuffer(void);
				bool _initEthernetHeader(std::string dmac);
				bool _initIpHeader(std::string dip);
				bool _initUdpHeader(unsigned int dport, unsigned int sport);
				bool _initVitaHeader(unsigned int streamId);
				bool _incrementVitaHeader(void);
			public:
				unsigned long int frameCount;
			//	boost::interprocess::named_mutex ethMutex;

				Transmitter(std::string ifname, unsigned int ducChannel, unsigned int udpPort, bool udpInsteadOfRaw, bool useRingBuffer);
				virtual ~Transmitter();
				unsigned int getFrame(const short * samples, unsigned char * frame);

				bool buildFrameHeaders(std::string dmac, std::string dip, unsigned int dport, unsigned int streamId);
				bool isSocketBound(void) { return _sockfd>0; };
				int sendFrame(short * samples);
				int sendFrame(short * samples, TransmitSocket * txsock);
			};

		}
	}
}

#endif /* INCLUDED_CYBERRADIO_NDR651_TRANSMITTER_H */
