/***************************************************************************
 * \file UdpStatusReceiver.h
 *
 * \brief NDR651 UDP status receiver.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_UDPSTATUSRECEIVER_H_
#define INCLUDED_LIBCYBERRADIO_NDR651_UDPSTATUSRECEIVER_H_

#include <boost/thread/mutex.hpp>
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/Thread.h"

#define MAX_RX_SIZE 8192
#define MAX_RADIO_BUFFSIZE 67108862 // (2^26)-2 samples
#define RADIO_BUFFER_RESERVE 1048576

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
		 * \brief UDP status receiver.
		 */
		class UdpStatusReceiver: public LibCyberRadio::Thread, public LibCyberRadio::Debuggable
		{
			public:
				/*!
				 * \brief Constructs a UdpStatusReceiver object.
				 * \param ifname Ethernet interface name
				 * \param port UDP port
				 * \param debug Whether or not to produce debug output
				 */
				UdpStatusReceiver(std::string ifname, unsigned int port, bool debug, bool updatePE);
				/*!
				 * \brief Destroys a UdpStatusReceiver object.
				 */
				virtual ~UdpStatusReceiver();
				/*!
				 * \brief Executes the main processing loop for the thread.
				 */
				virtual void run();
				/*!
				 * \brief Sets the interface name.
				 * \param ifname Ethernet interface name
				 * \returns True if the action succeeded, false otherwise.
				 */
				bool setStatusInterface(std::string ifname);
				/*!
				 * \brief Sets the interface name.
				 * \param ifname Ethernet interface name
				 * \param makeSocketFlag Whether or not to create a UDP socket
				 * \returns True if the action succeeded, false otherwise.
				 */
				bool setStatusInterface(std::string ifname, bool makeSocketFlag);
				/*!
				 * \brief Sets the UDP port.
				 * \param port UDP port
				 * \returns True if the action succeeded, false otherwise.
				 */
				bool setStatusPort(unsigned int port);
				/*!
				 * \brief Sets the UDP port.
				 * \param port UDP port
				 * \param makeSocketFlag Whether or not to create a UDP socket
				 * \returns True if the action succeeded, false otherwise.
				 */
				bool setStatusPort(unsigned int port, bool makeSocketFlag);
				/*!
				 * \brief Determines if it is OK to send data.
				 * \param pendingSamples Number of samples pending
				 * \param lockIfOk Whether or not to lock sending if sending is OK
				 * \returns True if OK to send, false otherwise.
				 */
				bool okToSend(long int pendingSamples, bool lockIfOk);
				/*!
				 * \brief Gets the amount of free space available.
				 * \returns Amount of free space.
				 */
				long int getFreeSpace(void);
				/*!
				 * \brief Updates status based on the number of samples sent.
				 * \param samplesSent Number of samples sent
				 * \returns True if there is free space available, false otherwise.
				 */
				bool sentNSamples(long int samplesSent);
				
				bool setUpdatePE(bool updatePE);
				bool getUpdatePE(void) { return _updatePE; };
				int setMaxFreeSpace(float fs, float maxLatency);
				int getMaxFreeSpace(void) { return _freeSpaceMax; };
				//~ bool setUdpPort(unsigned int port);
				int getUdpPort(void) { return _port; };

			private:
				int _sockfd;
				char _rxbuff[MAX_RX_SIZE];
				fd_set set;
				boost::mutex _fcMutex, _selMutex;
				bool _sendLock;
				bool _shutdown;
				bool _updatePE;

				std::string _ifname;
				unsigned int _port;
				uint64_t timeoutCount;

				int _651freeSpace;
				int _freeSpaceMax;

				bool _makeSocket(void);
				bool _setFreeSpace(int, bool, bool, bool);
		};

	} /* namespace NDR651 */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_UDPSTATUSRECEIVER_H_ */
