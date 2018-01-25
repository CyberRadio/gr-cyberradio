/***************************************************************************
 * \file FlowControlClient.h
 *
 * \brief NDR651 flow control client.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_FLOWCONTROLCLIENT_H
#define INCLUDED_LIBCYBERRADIO_NDR651_FLOWCONTROLCLIENT_H

#include "LibCyberRadio/Common/BasicList.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/Thread.h"
#include "LibCyberRadio/NDR651/ClientSocket.h"
#include "LibCyberRadio/NDR651/PacketTypes.h"
#include <boost/thread/mutex.hpp>
#include <boost/ptr_container/ptr_vector.hpp>
#include <vector>

//#define TX_BUFFER_MAX_SIZE 67108862 // (2^26)-2
#define TX_BUFFER_MAX_SIZE 67108862 // (2^26)-2
#define TX_BUFFER_MIN_SIZE 0

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
		 * \brief Flow control client class.
		 */
		class FlowControlClient : public Thread, public Debuggable
		{
			public:
				/*!
				 * \brief Constructs a FlowControlClient object.
				 * \param ducChannel DUC channel number
				 * \param config_tx Whether or not to configure the transmitter
				 * \param updatesPerSecond Number of updates to make per second
				 * \param debug Whether or not to produce debug output
				 */
				FlowControlClient(unsigned int ducChannel,
									bool config_tx,
									unsigned int updatesPerSecond,
									bool debug = false);
				/*!
				 * \brief Destroys a FlowControlClient object.
				 */
				virtual ~FlowControlClient();
				/*!
				 * \brief Executes the main processing loop for the thread.
				 */
				virtual void run();
				/*!
				 * \brief Updates the flow controller.
				 */
				void update(void);
				/*!
				 * \brief Connects to the radio.
				 * \param hostname Radio host name
				 * \param port Radio TCP port number
				 * \returns True if the action succeeded, false otherwise.
				 */
				bool connectToRadio(const std::string& hostname, unsigned int port);
				/*!
				 * \brief Sets the update rate.
				 * \param updatesPerSecond Number of updates to make per second
				 * \returns The new update rate.
				 */
				unsigned int setUpdateRate(unsigned int updatesPerSecond);
				/*!
				 * \brief Gets the update delay.
				 * \returns The update delay.
				 */
				unsigned int getUpdateDelay() { return _fcUpdateDelay; };
				/*!
				 * \brief Sets the DUC channel number.
				 * \param ducChannel DUC channel number
				 */
				void setDucChannel(unsigned int ducChannel);
				/*!
				 * \brief Gets whether or not the client is connected.
				 * \returns True if the client is connected, false otherwise.
				 */
				bool isConnected(void) { return _mySocket->isConnected(); };
			//	bool tryBoostSocket(void);
				/*!
				 * \brief Disconnects the flow control client.
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool disconnect(void);
				/*!
				 * \brief Tests the flow control queries.
				 */
				void testQueries(void);
				/*!
				 * \brief Gets the radio's UTC time.
				 * \returns The UTC time, in seconds from the Epoch.
				 */
				long unsigned int getUtc(void) {return _utc;};
				/*!
				 * \brief Gets the MAC address of a 10GigE port on the radio.
				 * \param tenGbeIndex 10GigE interface index
				 * \returns The MAC address string.
				 */
				std::string getRadioMac(unsigned int tenGbeIndex);
				/*!
				 * \brief Gets the IP address of a 10GigE port on the radio.
				 * \param tenGbeIndex 10GigE interface index
				 * \returns The IP address string.
				 */
				std::string getRadioIp(unsigned int tenGbeIndex);
				/*!
				 * \brief Disables the DUC.
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool disableDuc();// { return _sendDuc(false); };
				//bool enableDuc() { return _setDucConfig(true); };
				/*!
				 * \brief Enables the DUC.
				 * \param rateIndex DUC rate index
				 * \param txChannel Bitmap of transmitters the DUC will use
				 * \param streamId Stream ID
				 * \param tenGbeIndex 10GigE interface index
				 * \param attenuation DUC attenuation (dB)
				 * \param txFreq Transmitter frequency (Hz)
				 * \param ducFreq DUC frequency (Hz)
				 * \param txAtten Transmitter attenuation (dB)
				 * \param ducEnable Whether or not to enable the DUC
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool enableDuc(unsigned int rateIndex, unsigned int txChannel,
						unsigned int streamId, unsigned int tenGbeIndex, float attenuation,
						double txFreq, long ducFreq, unsigned int txAtten, bool ducEnable = true);
				//bool enableDucChannel(unsigned int ducChannel, bool enable, unsigned int ducRate, unsigned int streamId, unsigned int tenGbeIndex, unsigned int ducTxChannel, float ducFreq, float ducAtten);
				//bool enableDucChannel(unsigned int ducChannel, bool enable, unsigned int ducRate, unsigned int streamId, unsigned int tenGbeIndex, unsigned int ducTxChannel, float ducFreq, float ducAtten, bool enableTxChannels, float txFreq, unsigned int txAtten);
				/*!
				 * \brief Sets the transmitter frequency.
				 * \param txFreq Transmitter frequency (Hz)
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setTxFrequency(double txFreq, bool applySetting = true);
				/*!
				 * \brief Sets the transmitter attenuation.
				 * \param txAttenuation Transmitter attenuation (dB)
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setTxAttenuation(unsigned int txAttenuation, bool applySetting = true);
				/*!
				 * \brief Sets the DUC transmitter bitmap.
				 * \param txChannel Bitmap of transmitters the DUC will use
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucTxChannel(unsigned int txChannel, bool applySetting = true);
				/*!
				 * \brief Sets the DUC rate index.
				 * \param rateIndex DUC rate index
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucRateIndex(unsigned int rateIndex, bool applySetting = true);
				/*!
				 * \brief Sets the Stream ID.
				 * \param streamId Stream ID
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucStreamId(unsigned int streamId, bool applySetting = true);
				/*!
				 * \brief Sets the DUC attenuation.
				 * \param attenuation DUC attenuation (dB)
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucAttenuation(float attenuation, bool applySetting = true);
				/*!
				 * \brief Sets the DUC frequency.
				 * \param ducFreq DUC frequency (Hz)
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucFrequency(long ducFreq, bool applySetting = true);
				/*!
				 * \brief Sets the DUC TX Inversion Mode.
				 * \param txinvMode TX Inversion Mode (0=normal, 1=inverted)
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucTxinvMode(unsigned int txinvMode, bool applySetting = true);
				/*!
				 * \brief Sets whether or not the DUC is enabled.
				 * \param ducEnable Whether or not to enable the DUC
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucEnable(bool ducEnable, bool applySetting = true);
				/*!
				 * \brief Sets the 10GigE port used by the DUC.
				 * \param ducTenGbePort 10GigE interface index
				 * \param applySetting Whether or not to apply the new setting immediately
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool setDucTenGbePort(unsigned int ducTenGbePort, bool applySetting = true);
				/*!
				 * \brief Determines if it is OK to send data.
				 * \param pendingSamples Number of samples pending
				 * \param lockIfOk Whether or not to lock sending if sending is OK
				 * \returns True if OK to send, false otherwise.
				 */
				bool okToSend(long int pendingSamples, bool lockIfOk);
			//	bool okToSend(long int pendingSamples, bool lockIfOk, unsigned int ducChannel);
				/*!
				 * \brief Gets the amount of free space available.
				 * \returns Amount of free space.
				 */
				long int getFreeSpace(void);
			//	long int getFreeSpace(unsigned int ducChannel);
				/*!
				 * \brief Updates status based on the number of samples sent.
				 * \param samplesSent Number of samples sent
				 * \returns True if there is free space available, false otherwise.
				 */
				bool sentNSamples(long int samplesSent);
			//	bool sentNSamples(long int samplesSent, unsigned int ducChannel);
				
				bool setDucDipStatusEntry(int dipIndex, std::string dip, std::string dmac, unsigned int ducStatusPort);
				bool setDuchsParameters(unsigned int duchsFullThresh, unsigned int duchsEmptyThresh, unsigned int duchsPeriod);
				
				bool unpause(void);

			private:

				std::string _radioHostname;
				unsigned int _radioTcpPort;

				struct TxStatusFrame _statusFrame;
				int _statusSockfd;
				socklen_t _statusDestLen; /* byte size of client's address */
				struct sockaddr_in _statusDestAddr, _statusCopyAddr; /* client addr */

				unsigned int _tbsChannel;
				unsigned int _tbsSpace;
				unsigned int _tbsUnderrunFlag;
				unsigned int _tbsUnderrunCount;
				unsigned int _tbsOverrunFlag;
				unsigned int _tbsOverrunCount;
				unsigned int _tbsEmptyFlag;
				unsigned int _tbsFullFlag;

				bool _validDucChannel, _multiChannel;
				bool _ducEnable;
				unsigned int _ducChannel;
				unsigned int _ducRateIndex;
				unsigned int _ducStreamId;
				unsigned int _ducTxChannel;
				unsigned int _ducTenGbePort;
				unsigned int _ducDipIndex;
				unsigned int _ducAttenuation;
				unsigned int _txinvMode;
				unsigned int _txAttenuation;
				double _txFreq;
				int _shfMode;
				long _ducFreq;
				bool _config_tx;
				
				unsigned int _duchsFullThresh;
				unsigned int _duchsEmptyThresh;
				unsigned int _duchsPeriod;
				unsigned int _duchsUdpPort;

				BasicStringList _rspVec;

				boost::ptr_vector<boost::mutex> _fcMutexVector;
				std::vector<long int> _freeSpaceVector;

				boost::mutex _fcMutex, _fcSendMutex, _fcUpdateMutex;
				bool _sendLock;
				unsigned int _fcUpdateRate, _fcUpdateDelay;
				bool _firstUpdate;
			//	long int _651bufferSize;
				unsigned long int _utc;
				long int _651freeSpace;
				long int _651freeSpaceArray[8];
				long int _651freeSpaceLast;
				long int _samplesPerUpdate;
			//	long int _651minFreeSpace;
				//std::string _tqbaQuery, _tqouQuery;
				std::string _tbsQuery;
				ClientSocket * _mySocket;


				bool _sendCmdAndQry(const std::string& cmd, const std::string& qry);
				bool _setShfMode();
				bool _sendShf();
				bool _sendTxf();
				bool _sendTxa();
				bool _sendTxp();
				bool _sendTxinv();
				bool _sendWbduc();
				bool _sendDuc();
				bool _sendDucp();
				bool _sendWba();
				bool _sendWbf();
				bool _sendDuchs();
				bool _sendDip();
				
				bool _clearDucSettingsInRadio(void);

				void _initStatusFrame(void);
				void _initStatusSocket(void);
				void _initStatusAddress(void);
				void _sendStatusFrame(void);

				//bool _setDucConfig(bool enable);
				void _queryBufferState(void);
				void _queryUtc(void);
				void _queryStatus(void);
				long _getDucSampleRate(void) const;

		};

	}
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_FLOWCONTROLCLIENT_H */
