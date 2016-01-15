/***************************************************************************
 * \file ClientSocket.cpp
 *
 * \brief NDR651 client socket class.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include "ClientSocket.h"
#include "CyberRadio/Pythonesque.h"

namespace gr
{
	namespace CyberRadio
	{
		namespace NDR651
		{
			ClientSocket::ClientSocket(const std::string& hostname, unsigned int port,
					                   bool debug) {
				// TODO Auto-generated constructor stub
				_serverHostname = hostname;
				_serverPort = port;
				_debug = debug;
			}

			ClientSocket::~ClientSocket() {
				// TODO Auto-generated destructor stub
				disconnect();
			}

			bool ClientSocket::connectToServer() {
				struct sockaddr_in serv_addr;
				struct hostent *server;
				BasicStringList cmdVec, rspVec;
				BasicStringList::iterator cmd, rsp;
				bool cmdRspError = false;

				//std::cout << "Client Connecting...";

				server = gethostbyname(_serverHostname.c_str());
				_sockfd = socket(AF_INET, SOCK_STREAM, 0);
				bzero((char *) &serv_addr, sizeof(serv_addr));
				serv_addr.sin_family = AF_INET;
				bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
				serv_addr.sin_port = htons(_serverPort);
				if (connect(_sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0) {
					//std::cout << "ERROR?";
				} else {
					//std::cout << "success!";
					_connected = true;
				}
				//std::cout << std::endl;

				FD_ZERO(&set);
				FD_SET(_sockfd, &set);

				cmdVec.push_back(std::string("\n"));
				cmdVec.push_back(std::string("*IDN?\n"));
				cmdVec.push_back(std::string("VER?\n"));
				cmdVec.push_back(std::string("HREV?\n"));

				for (cmd=cmdVec.begin(); cmd<cmdVec.end(); cmd++) {
					rspVec.clear();
					cmdRspError |= sendCmdAndGetRsp(*cmd, rspVec, 2000, _debug);
				}

				return isConnected();
			}

			bool ClientSocket::disconnect() {
				//std::cout << std::endl << "Client disconnecting...";
				if (isConnected()) {
			//		shutdown(_sockfd,SHUT_WR);
			//		usleep(1000);
					shutdown(_sockfd,SHUT_RDWR);
			//		usleep(1000);
			//		close(_sockfd);
					_connected = false;
					//std::cout << "success!";
				} else {
					//std::cout << "but we weren't connected?";
				}
				//std::cout << std::endl;

				return !isConnected();
			}

			bool ClientSocket::sendCmd(const std::string& cmd) {
				if (isConnected()) {
					return write(_sockfd, cmd.c_str(), cmd.size())!=(int)cmd.size();
				} else {
					return true;
				}
			}

			bool ClientSocket::getRsp(BasicStringList &rsp, float timeout) {
				struct timeval tout;
				tout.tv_sec = (long int) timeout/1000;
				tout.tv_usec = (long int)(1000*timeout)%1000000;
				_clearRxBuff();
				FD_SET(_sockfd, &set);
				if (select(FD_SETSIZE, &set, NULL, NULL, &tout)>0) {
					_tcpRx();
					rsp.push_back(std::string(_rxBuff));
					return false;
				} else {
					return true;
				}
			}

			bool ClientSocket::sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp, float timeout) {
				return sendCmdAndGetRsp(cmd, rsp, timeout, _debug);
			}

			bool ClientSocket::sendCmdAndGetRsp(const std::string& cmd, BasicStringList &rsp, float timeout, bool print) {
				_trxMutex.lock();
				unsigned int i;
				std::string temp;
				bool txError=false, rxError=false;
				struct timeval tout;
				tout.tv_sec = (long int) timeout/1000;
				tout.tv_usec = (long int)(1000*timeout)%1000000;

				txError = sendCmd(cmd);
				FD_SET(_sockfd, &set);
				while((!rxError)&&((rsp.size()==0)||((rsp.size()>0)&&(rsp.back().find("OK>")==std::string::npos)))) {
			//		txRxError = getRsp(rsp, timeout);
					if (select(FD_SETSIZE, &set, NULL, NULL, &tout)>0) {
						_clearRxBuff();
						_tcpRx();
						BasicStringList x = Pythonesque::Split(std::string(_rxBuff),"\n");
			//			std::cout << "\t**  Separate strings in RSP = " << x.size() << std::endl;
						for (i=0; i<x.size(); i++) {
							temp = Pythonesque::Strip(x.at(i));
							if (temp.size()>0) {
								rsp.push_back(temp);
							}
			//				std::cout << "\t**  " << i << "(" << temp.size() << ") = '" << temp << "'" << std::endl;
						}
			//			rsp.push_back(Pythonesque::Strip( std::string(_rxBuff) ));
					} else {
						rxError = true;
					}
				}
				_trxMutex.unlock();
				if (print) {
					std::cerr << "CMD = '" << Pythonesque::Strip(cmd) << "' & RSP = '" << Pythonesque::Join(rsp, "; ") << "'" << std::endl;
					for (BasicStringList::iterator it=rsp.begin(); it<rsp.end(); it++) {
						std::cerr << "\tRSP = '" << *it << "'" << std::endl;
					}
				}
				return txError||rxError;
			}
		}

	}
}
