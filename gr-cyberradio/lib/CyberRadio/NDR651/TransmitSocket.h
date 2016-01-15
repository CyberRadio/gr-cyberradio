/***************************************************************************
 * \file TransmitSocket.h
 *
 * \brief NDR651 transmitter socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_TRANSMITSOCKET_H
#define INCLUDED_CYBERRADIO_NDR651_TRANSMITSOCKET_H

#include <string>
#include <vector>
#include <boost/thread/mutex.hpp>

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
			class TransmitSocket
			{
				public:
					TransmitSocket(const std::string& ifname, bool useRingBuffer);
					virtual ~TransmitSocket();

					std::string getMacAddress();
					std::string getIpAddress();

					bool sendFrame(unsigned char * frame, const int & frameLen);
				//	bool sendFrame(std::vector<short> frame);
				//	int sendFrame(std::vector<std::complex>);

				private:
					int _sockfd;
					std::string _ifname;
					bool _usingRingBuffer;
					boost::mutex _txMutex;
					int _txBytes;
					long unsigned int _sendCount, _byteCount;

					bool _makeSocket();

			};

		} /* namespace NDR651 */
	}
}

#endif /* INCLUDED_CYBERRADIO_NDR651_TRANSMITSOCKET_H */
