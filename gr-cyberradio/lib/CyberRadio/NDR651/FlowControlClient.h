/***************************************************************************
 * \file FlowControlClient.h
 *
 * \brief NDR651 flow control client.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_FLOWCONTROLCLIENT_H
#define INCLUDED_CYBERRADIO_NDR651_FLOWCONTROLCLIENT_H

#include "ClientSocket.h"
#include "CyberRadio/BasicList.h"
#include "CyberRadio/Thread.h"
#include <boost/thread/mutex.hpp>
#include <boost/ptr_container/ptr_vector.hpp>

#include <vector>

//#define TX_BUFFER_MAX_SIZE 67108862 // (2^26)-2
#define TX_BUFFER_MAX_SIZE 67108862 // (2^26)-2
#define TX_BUFFER_MIN_SIZE 0

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
			class FlowControlClient : public CyberRadio::Thread
			{
				public:
					FlowControlClient(unsigned int ducChannel,
										bool config_tx,
										unsigned int updatesPerSecond,
										bool debug = false);
					virtual ~FlowControlClient();
					virtual void run(void);
					void update(void);

					bool connectToRadio(const std::string& hostname, unsigned int port);
					unsigned int setUpdateRate(unsigned int updatesPerSecond);
					unsigned int getUpdateDelay() { return _fcUpdateDelay; };
					void setDucChannel(unsigned int);
					bool isConnected(void) { return _mySocket->isConnected(); };

				//	bool tryBoostSocket(void);
					bool disconnect(void);
					void testQueries(void);
					long unsigned int getUtc(void) {return _utc;};
					std::string getRadioMac(unsigned int tenGbeIndex);
					std::string getRadioIp(unsigned int tenGbeIndex);

					bool disableDuc() { return _sendWbduc(false); };
					//bool enableDuc() { return _setDucConfig(true); };
					bool enableDuc(unsigned int rateIndex, unsigned int txChannel, unsigned int streamId, unsigned int tenGbeIndex, float attenuation, float txFreq, long ducFreq, unsigned int txAtten);
					//bool enableDucChannel(unsigned int ducChannel, bool enable, unsigned int ducRate, unsigned int streamId, unsigned int tenGbeIndex, unsigned int ducTxChannel, float ducFreq, float ducAtten);
					//bool enableDucChannel(unsigned int ducChannel, bool enable, unsigned int ducRate, unsigned int streamId, unsigned int tenGbeIndex, unsigned int ducTxChannel, float ducFreq, float ducAtten, bool enableTxChannels, float txFreq, unsigned int txAtten);
					
					bool setTxFrequency(int txFreq, bool applySetting = true);
					bool setTxAttenuation(unsigned int txAttenuation, bool applySetting = true);
					bool setDucTxChannel(unsigned int txChannel, bool applySetting = true);
					bool setDucRateIndex(unsigned int rateIndex, bool applySetting = true);
					bool setDucStreamId(unsigned int streamId, bool applySetting = true);
					bool setDucAttenuation(float attenuation, bool applySetting = true);
					bool setDucFrequency(long ducFreq, bool applySetting = true);

					bool okToSend(long int pendingSamples, bool lockIfOk);
				//	bool okToSend(long int pendingSamples, bool lockIfOk, unsigned int ducChannel);
					long int getFreeSpace(void);
				//	long int getFreeSpace(unsigned int ducChannel);
					bool sentNSamples(long int samplesSent);
				//	bool sentNSamples(long int samplesSent, unsigned int ducChannel);

				private:

					std::string _radioHostname;
					unsigned int _radioTcpPort;

					bool _validDucChannel, _multiChannel;
					unsigned int _ducChannel;
					unsigned int _ducRateIndex;
					unsigned int _ducStreamId;
					unsigned int _ducTxChannel;
					unsigned int _ducTenGbePort;
					unsigned int _ducAttenuation;
					unsigned int _txAttenuation;
					float _txFreq;
					long _ducFreq;
					bool _config_tx;
					bool _debug;
					
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
					bool _sendTxf();
					bool _sendTxa();
					bool _sendTxp();
					bool _sendWbduc(bool enable = true);
					bool _sendWba();
					bool _sendWbf();
					
					//bool _setDucConfig(bool enable);
					void _queryBufferState(void);
					void _queryUtc(void);
					long _getDucSampleRate(void) const;
					int debug(const char *format, ...);

			};

		}
	}
}

#endif /* INCLUDED_CYBERRADIO_NDR651_FLOWCONTROLCLIENT_H */
