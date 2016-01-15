/***************************************************************************
 * \file ClientSocket.h
 *
 * \brief NDR651 client socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_CYBERRADIO_NDR651_CLIENTSOCKET_H
#define INCLUDED_CYBERRADIO_NDR651_CLIENTSOCKET_H

//#include <unistd.h>
#include <iostream>    //cout
#include <stdio.h> //printf
#include <string.h>    //strlen
#include <string>  //string
#include <sys/socket.h>    //socket
#include <arpa/inet.h> //inet_addr
#include <netdb.h> //hostent
#include <vector>
#include "CyberRadio/BasicList.h"
#include <boost/thread/mutex.hpp>

#define RX_BUFF_SIZE 1024

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
			class ClientSocket {
			private:
				bool _connected;
				int _sockfd;
				fd_set set;

				std::string _serverHostname;
				int _serverPort;
				bool _debug;

				char _rxBuff[RX_BUFF_SIZE];
				void _clearRxBuff(void) { memset(_rxBuff, 0, RX_BUFF_SIZE); }
				void _tcpRx(void) { recv(_sockfd, _rxBuff, RX_BUFF_SIZE, 0); }
				
				boost::mutex _trxMutex;

			public:
				ClientSocket(const std::string& hostname, unsigned int port,
						     bool debug=true);
				virtual ~ClientSocket();
				bool isConnected(void) { return _connected; }
				bool connectToServer(void);
				bool disconnect(void);

				bool sendCmd(const std::string& cmd);
				bool getRsp(BasicStringList &rsp, float timeout);
				bool sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp, float timeout, bool print);
				bool sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp, float timeout);
			};

		}
	}
}

#endif /* INCLUDED_CYBERRADIO_NDR651_CLIENTSOCKET_H */
