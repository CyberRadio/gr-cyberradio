/***************************************************************************
 * \file TransmitPacketizer.h
 *
 * \brief NDR651 transmit packetizer class.
 *
 * \author NH/DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_TRANSMITPACKETIZER_H
#define INCLUDED_CYBERRADIO_NDR651_TRANSMITPACKETIZER_H

#include <linux/if_ether.h>
#include <netinet/ip.h>
#include <netinet/udp.h>

#include "FlowControlClient.h"
#include "TransmitSocket.h"

#define SAMPLES_PER_FRAME 2048

bool setCpuAffinity(int cpu);

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

			class TransmitPacketizer
			{
				public:
					TransmitPacketizer(const std::string& radioHostName = "",
									   int radioTcpPort = 8617,
									   unsigned int ducChannel = 1,
					                   const std::string& ifname = "eth0",
									   unsigned int tenGigIndex = 1,
									   unsigned int ducRate = 0,
									   unsigned int ducTxChannels = 0,
									   float ducFreq = 900e6,
									   float ducAtten = 0,
									   float txFreq = 900,
									   float txAtten = 0,
									   unsigned int streamId = 40001,
									   bool config_tx = false,
									   bool debug = false);
					virtual ~TransmitPacketizer();
					bool setRadioHostName(const std::string& radioHostName);
					bool setRadioTcpPort(int radioTcpPort);
					bool setDucChannel(unsigned int ducChannel);
					bool setDucInterface(const std::string& ifname,
							             unsigned int tenGigIndex);
					bool setDucRate(unsigned int ducRate);
					bool setDucTxChannels(unsigned int ducTxChannels);
					bool setDucFreq(float ducFreq);
					bool setDucAtten(float ducAtten);
					bool setTxFreq(float txFreq);
					bool setTxAtten(float txAtten);
					bool setStreamId(unsigned int streamId);
					bool setDebug(bool debug);
					bool setRadioParameters(
							           const std::string& radioHostName,
									   int radioTcpPort);
					bool setDucParameters(unsigned int tenGigIndex,
							              unsigned int ducRate,
							              unsigned int ducTxChannels,
										  float ducFreq,
										  float ducAtten,
										  float txFreq,
										  float txAtten,
										  unsigned int streamId);
					void start();
					void stop();
					unsigned int sendFrame(short * samples);
					bool isConnected(void);
					bool isReadyToReceive(void);

				private:
					unsigned int _waitLoop(void);
					void _incrementVitaHeader(void);
					bool setEthernetHeader(const std::string& sourceMac,
										   const std::string& destMac);
					bool setIpHeader(const std::string& sourceIp,
									 const std::string& destIp);
					bool setUdpHeader(unsigned short sourcePort,
									  unsigned short destPort);
					bool setVitaHeader(unsigned int streamId);
					int debug(const char *format, ...);

				private:
					/* Radio parameters */
					std::string _radioHostName;
					int _radioTcpPort;
					/* DUC parameters */
					unsigned int _ducChannel;
					std::string _ifname;
					unsigned int _tenGigIndex;
					unsigned int _ducRate;
					unsigned int _ducTxChannels;
					float _ducFreq;
					float _ducAtten;
					float _txFreq;
					float _txAtten;
					unsigned int _streamId;
					bool _config_tx;
					bool _debug;
					/* Control objects */
					TransmitSocket * _txSock;
					FlowControlClient * _fcClient;
					struct TxFrame _frame;
					unsigned char * _frameStart;
					unsigned int _frameLength;
					/* State data */
					unsigned int _samplesSent;
					std::string _sMac;
					std::string _dMac;
					std::string _sIp;
					std::string _dIp;
					unsigned short _sPort;
					unsigned short _dPort;
					bool _configuring;
					bool _constructing;

			};

		} /* namespace NDR651 */
	}
}

#endif /* INCLUDED_CYBERRADIO_NDR651_TRANSMITPACKETIZER_H */
