/*
* TXClient - Refactored Implementation of TransmitPacketizer 
*	Author: Nathan Harter
*	Author: Joseph Martin
*	Date: 5/23/2017
*/

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_TXCLIENT_H
#define INCLUDED_LIBCYBERRADIO_NDR651_TXCLIENT_H

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/NDR651/FlowControlClient.h"
#include "LibCyberRadio/NDR651/PacketTypes.h"
#include "LibCyberRadio/NDR651/UdpStatusReceiver.h"
#include "LibCyberRadio/NDR651/StatusReceiver.h"
#include "LibCyberRadio/NDR651/RadioController.h"
#include "LibCyberRadio/NDR651/Packetizer.h"

#include <boost/algorithm/string.hpp>
#include <boost/thread.hpp>

#define UDP_STATUS_BASE 65500
#define INVALID_VALUE 100000

namespace LibCyberRadio
{
	namespace NDR651
	{
		class TXClient : public Debuggable
		{

			private:
				/* Instance variables */
				// Constructor Args
				std::string  txInterfaceName;
				unsigned int ducChannel;
				unsigned int tenGbeIndex;
				double ducAttenuation;
				unsigned int ducRateIndex;
				unsigned int rfChannel;
				unsigned short txUdpPort;
				double ducFreq;
				double ducFullThreshPercent;
				double ducEmptyThreshPercent;
				unsigned int updatesPerSecond;
				double txFreq;	
				double txAttenuation;
				bool txInversion;
				std::string radioHostName;
				bool debugOn;

				// Other Inits
				int txSock;
				Packetizer *packetizer;
				//UdpStatusReceiver *statusRX;
				StatusReceiver *statusRX;
				RadioController *rc;
				bool isGrouped; // Is this Client part of a sync transmit?
				bool isRunning;  // Has the user called start()
				bool DUCPaused; // Should the DUC currently paused?
				long prefillSampleCount;

				// To synchronize calls from other threads
				boost::mutex objectAccessMutex;
				
				/* Instance methods */
				std::string getSourceMac();
				std::string getSourceIP();
				bool validInputs(std::string &errors);

			public:
				/* Constructors */
				TXClient(std::string radioHostName, bool debug);
				~TXClient();

				/* Instance methods */
				void start();
				void stop(bool disableRF = false);
				void setGrouped(bool isGrouped);
				void sendFrame(short * samples, unsigned int samplesPerFrame);
				unsigned int getDucChannel();
				bool isDUCPaused();

				// Config Setters
				bool setDUCChannel(unsigned int ducChannel);                    // Required (fulfillled by setDucParameters)
				bool setTxChannel(unsigned int txChannel);                      // Required (fulfillled by setDucParameters)
				bool setDUCRateIndex(unsigned int ducRateIndex);                // Required (fulfillled by setDucParameters)
				bool setDUCFreq(double ducFreq);                                // Optional
				bool setDUCAtten(double ducAtten);                              // Optional
				bool setTxFreq(double txFreq);                                  // Optional
				bool setTxAtten(double txAttenuation);                          // Optional
				bool setDUCParameters(
					unsigned int ducChannel,
					unsigned int ducRateIndex,
					unsigned int txChannel
				);
				bool setEthernetInterface(unsigned int tenGbeIndex, const std::string &txInterfaceName, unsigned short port);  // Required
				void disableRF();
				bool setTxInversion(bool txInversion);
				bool pauseDUC(bool paused = true);

			protected:
				bool setDUCRateIndexUnlocked(unsigned int ducRateIndex);

		};
	}
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_TXCLIENT_H */
