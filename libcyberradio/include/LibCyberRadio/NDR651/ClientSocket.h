/***************************************************************************
 * \file ClientSocket.h
 *
 * \brief NDR651 client socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_CLIENTSOCKET_H
#define INCLUDED_LIBCYBERRADIO_NDR651_CLIENTSOCKET_H

//#include <unistd.h>
#include <iostream>    //cout
#include <stdio.h> //printf
#include <string.h>    //strlen
#include <string>  //string
#include <sys/socket.h>    //socket
#include <arpa/inet.h> //inet_addr
#include <netdb.h> //hostent
#include <vector>
#include <boost/thread/mutex.hpp>
#include "LibCyberRadio/Common/BasicList.h"

#define RX_BUFF_SIZE 1024


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
         * \brief Client socket class.
         */
        class ClientSocket
        {
            public:
                /*!
                 * \brief Constructs a ClientSocket object.
                 * \param hostname Host name
                 * \param port UDP port
                 * \param debug Whether or not to produce debug output
                 */
                ClientSocket(const std::string& hostname, unsigned int port,
                        bool debug=true);
                /*!
                 * \brief Destroys a ClientSocket object.
                 */
                virtual ~ClientSocket();
                /*!
                 * \brief Gets whether or not the socket is connected.
                 * \returns True if the socket is connected, false otherwise.
                 */
                bool isConnected(void) { return _connected; }
                /*!
                 * \brief Connects to the server.
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool connectToServer(void);
                /*!
                 * \brief Disconnects from the server.
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool disconnect(void);
                /*!
                 * \brief Sends a command to the server.
                 * \param cmd The command string to send
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool sendCmd(const std::string& cmd);
                /*!
                 * \brief Gets a command response from the server.
                 * \param rsp A list of response strings
                 * \param timeout Response timeout, in seconds
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool getRsp(BasicStringList &rsp, float timeout);
                /*!
                 * \brief Sends a command to the server and gets the response.
                 * \param cmd The command string to send
                 * \param rsp A list of response strings
                 * \param timeout Response timeout, in seconds
                 * \param print Whether or not to print the result
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp,
                        float timeout, bool print);
                /*!
                 * \brief Sends a command to the server and gets the response.
                 * \param cmd The command string to send
                 * \param rsp A list of response strings
                 * \param timeout Response timeout, in seconds
                 * \returns True if the action succeeds, false otherwise.
                 */
                bool sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp,
                        float timeout);

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

        };

    }
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_CLIENTSOCKET_H */
