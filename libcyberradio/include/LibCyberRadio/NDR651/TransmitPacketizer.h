/***************************************************************************
 * \file TransmitPacketizer.h
 *
 * \brief NDR651 transmit packetizer class.
 *
 * \author NH/DA
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITPACKETIZER_H
#define INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITPACKETIZER_H

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/NDR651/FlowControlClient.h"
#include "LibCyberRadio/NDR651/PacketTypes.h"
#include "LibCyberRadio/NDR651/TransmitSocket.h"
#include "LibCyberRadio/NDR651/UdpStatusReceiver.h"

bool setCpuAffinity(int cpu);

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
	/*!
	 * \brief Provides programming elements for controlling the CyberRadio Solutions
	 *    NDR651 radio.
	 */
	namespace NDR651
	{

		/*!
		 * \brief Transmit packetizer class.
		 */
		class TransmitPacketizer : public Debuggable
		{
			public:
				/*!
				 * \brief Constructs a TransmitPacketizer object.
				 * \param radioHostName Radio host name
				 * \param radioTcpPort Radio TCP port number
				 * \param ducChannel DUC channel number
				 * \param ifname Ethernet interface name for the 10GigE interface to use
				 * \param tenGigIndex 10GigE interface index
				 * \param ducRate DUC rate index
				 * \param ducTxChannels Bitmap of transmitters the DUC will use
				 * \param ducFreq DUC frequency (Hz)
				 * \param ducAtten DUC attenuation (dB)
				 * \param txFreq Transmitter frequency (Hz)
				 * \param txAtten Transmitter attenuation (dB)
				 * \param streamId Stream ID
				 * \param config_tx Whether or not to configure the transmitter
				 * \param debug Whether or not to produce debug output
				 */
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
				/*!
				 * \brief Destroys a TransmitPacketizer object.
				 */
				virtual ~TransmitPacketizer();
				/*!
				 * \brief Sets the radio host name.
				 * \param radioHostName Radio host name
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setRadioHostName(const std::string& radioHostName);
				/*!
				 * \brief Sets the radio TCP port.
				 * \param radioTcpPort Radio TCP port number
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setRadioTcpPort(int radioTcpPort);
				/*!
				 * \brief Sets the DUC channel number.
				 * \param ducChannel DUC channel number
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucChannel(unsigned int ducChannel);
				/*!
				 * \brief Sets the DUC interface parameters.
				 * \param ifname Ethernet interface name for the 10GigE interface to use
				 * \param tenGigIndex 10GigE interface index
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucInterface(const std::string& ifname,
									 unsigned int tenGigIndex);
				/*!
				 * \brief Sets the DUC rate index.
				 * \param ducRate DUC rate index
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucRate(unsigned int ducRate);
				/*!
				 * \brief Sets the DUC transmit channel bitmap.
				 * \param ducTxChannels Bitmap of transmitters the DUC will use
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucTxChannels(unsigned int ducTxChannels);
				/*!
				 * \brief Sets the DUC frequency.
				 * \param ducFreq DUC frequency (Hz)
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucFreq(float ducFreq);
				/*!
				 * \brief Sets the DUC attenuation.
				 * \param ducAtten DUC attenuation (dB)
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucAtten(float ducAtten);
				/*!
				 * \brief Sets the transmitter frequency.
				 * \param txFreq Transmitter frequency (Hz)
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setTxFreq(float txFreq);
				/*!
				 * \brief Sets the transmitter attenuation.
				 * \param txAtten Transmitter attenuation (dB)
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setTxAtten(float txAtten);
				/*!
				 * \brief Sets the stream ID.
				 * \param streamId Stream ID
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setStreamId(unsigned int streamId);
				/*!
				 * \brief Sets whether or not to produce debug output.
				 * \param debug Whether or not to produce debug output
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDebug(bool debug);
				/*!
				 * \brief Sets the radio parameters.
				 * \param radioHostName Radio host name
				 * \param radioTcpPort Radio TCP port number
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setRadioParameters(
								   const std::string& radioHostName,
								   int radioTcpPort);
				/*!
				 * \brief Sets the DUC parameters.
				 * \param tenGigIndex 10GigE interface index
				 * \param ducRate DUC rate index
				 * \param ducTxChannels Bitmap of transmitters the DUC will use
				 * \param ducFreq DUC frequency (Hz)
				 * \param ducAtten DUC attenuation (dB)
				 * \param txFreq Transmitter frequency (Hz)
				 * \param txAtten Transmitter attenuation (dB)
				 * \param streamId Stream ID
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucParameters(unsigned int tenGigIndex,
									  unsigned int ducRate,
									  unsigned int ducTxChannels,
									  float ducFreq,
									  float ducAtten,
									  float txFreq,
									  float txAtten,
									  unsigned int streamId);
				/*!
				 * \brief Starts the packetizer.
				 */
				void start();
				/*!
				 * \brief Stops the packetizer.
				 */
				void stop();
				/*!
				 * \brief Sends a number of samples as a VITA 49 frame.
				 * \param samples Buffer of samples.  This buffer must be twice the
				 *    number of samples in a VITA 49 frame payload.
				 * \returns The number of samples actually sent.
				 */
				unsigned int sendFrame(short * samples);
				/*!
				 * \brief Gets whether or not the packetizer is connected.
				 * \returns True if the packetizer is connected, false otherwise.
				 */
				bool isConnected(void);
				/*!
				 * \brief Gets whether or not the packetizer is ready to receive data.
				 * \returns True if the packetizer is ready, false otherwise.
				 */
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
				bool _firstFrame;
				/* Control objects */
				TransmitSocket * _txSock;
				FlowControlClient * _fcClient;
				UdpStatusReceiver * _statusRx;
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

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITPACKETIZER_H */
