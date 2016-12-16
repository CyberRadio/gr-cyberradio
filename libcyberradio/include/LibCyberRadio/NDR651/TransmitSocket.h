/***************************************************************************
 * \file TransmitSocket.h
 *
 * \brief NDR651 transmitter socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITSOCKET_H
#define INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITSOCKET_H

#include <string>
#include <vector>
#include <boost/thread/mutex.hpp>

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
		 * \brief Transmit socket class.
		 */
		class TransmitSocket
		{
			public:
				/*!
				 * \brief Constructs a TransmitSocket object.
				 * \param ifname Ethernet interface name
				 * \param useRingBuffer Whether or not to use a ring buffer
				 */
				TransmitSocket(const std::string& ifname, unsigned int sport);
				/*!
				 * \brief Destroys a TransmitSocket object.
				 */
				virtual ~TransmitSocket();
				/*!
				 * \brief Gets the MAC address.
				 * \returns The MAC address string.
				 */
				std::string getMacAddress();
				/*!
				 * \brief Gets the IP address.
				 * \returns The IP address string.
				 */
				std::string getIpAddress();
				/*!
				 * \brief Gets the IP broadcast address.
				 * \returns The IP broadcast address string.
				 */
				std::string getIpBroadcastAddress();
				/*!
				 * \brief Sends a frame of data.
				 * \param frame The data to send
				 * \param frameLen The length of the data
				 * \returns True if the action succeeds, false otherwise.
				 */
				bool sendFrame(unsigned char * frame, const int & frameLen);
				bool isUsingRawSocket(void) { return _isRaw; };
				bool isUsingUdpSocket(void) { return !_isRaw; };
			//	bool sendFrame(std::vector<short> frame);
			//	int sendFrame(std::vector<std::complex>);

			private:
				int _sockfd;
				std::string _ifname;
				bool _isRaw, _isBroadcast;
				boost::mutex _txMutex;
				int _txBytes;
				long unsigned int _sendCount, _byteCount;
				unsigned int _sport;

				bool _makeSocket();
				bool _makeRawSocket();
				bool _makeUdpSocket();

		};

	} /* namespace NDR651 */
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_TRANSMITSOCKET_H */
