/***************************************************************************
 * \file RadioTransport.cpp
 * \brief Defines an interface for transporting data to and from a radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioTransport.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include "jsoncpp/json/json.h"
#include <sstream>
#include <cstdio>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <errno.h>
#include <string.h>
#include <sys/select.h>


namespace LibCyberRadio
{

    namespace Driver
    {

        RadioTransport::RadioTransport(
                bool json,
                bool debug
            ) :
            Debuggable(debug, "RadioTransport"),
            _isJson(json),
            _tcpSocket(0),
            _udpSocket(0),
            _serial(NULL),
            _httpsSession(NULL),
            _httpsConnTestUrl(""),
            _httpsApiCmdUrl(""),
            _lastCmdErrInfo("")
        {
            this->debug("CONSTRUCTED\n");
        }

        RadioTransport::~RadioTransport()
        {
            if ( isConnected() )
                disconnect();
            if (_httpsSession != NULL)
            {
                delete _httpsSession;
                _httpsSession = NULL;
            }
            if (_serial != NULL)
            {
                delete _serial;
                _serial = NULL;
            }
            this->debug("DESTROYED\n");
        }

        RadioTransport::RadioTransport(const RadioTransport &other) :
             Debuggable(other)
        {
            _isJson = other._isJson;
            _tcpSocket = other._tcpSocket;
            _udpSocket = other._udpSocket;
            _serial = other._serial;
            _httpsSession = other._httpsSession;
            _httpsConnTestUrl = other._httpsConnTestUrl;
            _httpsApiCmdUrl = other._httpsApiCmdUrl;
            _lastCmdErrInfo = other._lastCmdErrInfo;
        }

        RadioTransport &RadioTransport::operator=(const RadioTransport &other)
        {
            Debuggable::operator=(other);
            // Protect against self-assignment
            if (this != &other)
            {
                _isJson = other._isJson;
                _tcpSocket = other._tcpSocket;
                _udpSocket = other._udpSocket;
                _serial = other._serial;
                _httpsSession = other._httpsSession;
                _httpsConnTestUrl = other._httpsConnTestUrl;
                _httpsApiCmdUrl = other._httpsApiCmdUrl;
                _lastCmdErrInfo = other._lastCmdErrInfo;
            }
            return *this;
        }

        bool RadioTransport::connect(
                const std::string &mode,
                const std::string &host_or_dev,
                const int port_or_baudrate
            )
        {
            this->debug("[connect] Called; mode=\"%s\", HorD=\"%s\", PorB=%d\n", mode.c_str(), host_or_dev.c_str(), port_or_baudrate);
            bool ret = false;
            if (mode == "https")
            {
                ret = connectHttps(host_or_dev, port_or_baudrate);
            }
            else if (mode == "udp")
            {
                ret = connectUdp(host_or_dev, port_or_baudrate);
            }
            else if (mode == "tcp")
            {
                ret = connectTcp(host_or_dev, port_or_baudrate);
            }
            else if (mode == "tty")
            {
                ret = connectTty(host_or_dev, port_or_baudrate);
            }
            this->debug("[connect] Returning %s\n", this->debugBool(ret));
            return ret;
        }

        void RadioTransport::disconnect()
        {
            this->debug("[disconnect] Called\n");
            if (_httpsSession != NULL)
            {
                delete _httpsSession;
                _httpsSession = NULL;
            }
            else if (_udpSocket > 0)
            {
                int ok = shutdown(_udpSocket, SHUT_RDWR);
                if (ok != 0)
                    translateErrno();
            }
            else if (_tcpSocket > 0)
            {
                int ok = shutdown(_tcpSocket, SHUT_RDWR);
                if (ok != 0)
                    translateErrno();
            }
            else if (_serial != NULL)
            {
                _serial->close();
                delete _serial;
                _serial = NULL;
            }
            this->debug("[disconnect] Returning\n");
        }

        bool RadioTransport::isConnected() const
        {
            bool ret = (
                    (_httpsSession != NULL) ||
                    (_serial != NULL) ||
                    (_tcpSocket > 0) ||
                    (_udpSocket > 0)
            );
            return ret;
        }

        bool RadioTransport::sendCommand(
                const std::string &cmdString,
                bool clearRx
            )
        {
            this->debug("[sendCommand] Called; cmd=\"%s\"\n",
                    this->rawString(cmdString).c_str());
            bool ret = false;
            if (_httpsSession != NULL)
            {
                ret = sendCommandHttps(cmdString, clearRx);
            }
            else if (_serial != NULL)
            {
                ret = sendCommandTty(cmdString, clearRx);
            }
            else if (_udpSocket > 0)
            {
                ret = sendCommandUdp(cmdString, clearRx);
            }
            else if (_tcpSocket > 0)
            {
                ret = sendCommandTcp(cmdString, clearRx);
            }
            else
                _lastCmdErrInfo = "Transport is not connected";
            this->debug("[sendCommand] Returning %s\n", this->debugBool(ret));
            return ret;
        }

        BasicStringList RadioTransport::receive(
                double timeout
            )
        {
            this->debug("[receive] Called\n");
            BasicStringList ret;
            if ( _isJson )
            {
                ret = receiveJson(timeout);
            }
            else
            {
                ret = receiveCli(timeout);
            }
            this->debug("[receive] Returning %u element%s\n", ret.size(),
                    ret.size() == 1 ? "" : "s");
            return ret;
        }

        std::string RadioTransport::getLastCommandErrorInfo() const
        {
            return _lastCmdErrInfo;
        }

        bool RadioTransport::connectTcp(
                const std::string &host,
                int port
            )
        {
            this->debug("[connectTcp] Called; host=\"%s\", port=%d\n", host.c_str(), port);
            _tcpSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
            this->debug("[connectTcp] Socket created; FD=%d\n", _tcpSocket);
            if (_tcpSocket > 0)
            {
                struct hostent *hent = gethostbyname(host.c_str());
                char buf[128];
                memset(buf, 0, sizeof(buf));
                inet_ntop(AF_INET, hent->h_addr_list[0], buf, sizeof(buf));
                this->debug("[connectTcp] Host IP address: %s\n", buf);
                struct sockaddr_in addr;
                memset(&addr, 0, sizeof(struct sockaddr_in));
                addr.sin_family = AF_INET;
                memcpy(&(addr.sin_addr.s_addr), hent->h_addr_list[0], hent->h_length);
                addr.sin_port = htons(port);
                this->debug("[connectTcp] Connecting\n");
                int ok = ::connect(_tcpSocket, (const sockaddr*)&addr, sizeof(struct sockaddr_in));
                this->debug("[connectTcp] -- ok = %d\n", ok);
                if (ok != 0)
                    _tcpSocket = 0;
            }
            if (_tcpSocket <= 0)
            {
                _tcpSocket = 0;
                translateErrno();
            }
            bool ret = (_tcpSocket > 0);
            return ret;
        }

        bool RadioTransport::connectUdp(
                const std::string& host,
                int port
            )
        {
            bool ret = false;
            return ret;
        }

        bool RadioTransport::connectHttps(
                const std::string &host,
                int port
            )
        {
            this->debug("[connectHttps] Called; host=\"%s\", port=%d\n", host.c_str(), port);
            bool ret = false;
            // Attempt to establish the HTTPS session
            if ( _httpsSession == NULL )
                _httpsSession = new HttpsSession( /*d_debug */ false);
            if ( _httpsSession != NULL )
            {
                this->debug("[connectHttps] Session initialized\n");
                // Form connection test and API command URLs
                std::ostringstream oss;
                oss << "https://" << host << ":" << port << "/";
                _httpsConnTestUrl = oss.str();
                oss << "api/command";
                _httpsApiCmdUrl = oss.str();
                // Test the connection
                this->debug("[connectHttps] Testing connection; URL=%s\n",
                        _httpsConnTestUrl.c_str());
                ret = _httpsSession->get(_httpsConnTestUrl, false);
                // Destroy the session object if the connection test fails
                if (!ret)
                {
                    _lastCmdErrInfo = _httpsSession->getLastRequestErrorInfo();
                    delete _httpsSession;
                    _httpsSession = NULL;
                }
            }
            else
                _lastCmdErrInfo = "Failed to establish HTTPS session";
            this->debug("[connectHttps] Returning %s\n", this->debugBool(ret));
            return ret;
        }

        bool RadioTransport::connectTty(
                const std::string& dev,
                int baudrate
            )
        {
            this->debug("[connectTty] Called; dev=\"%s\", baudrate=%d\n",
                    dev.c_str(), baudrate);
            bool ret = false;
            // Attempt to establish the TTY link
            if ( _serial == NULL )
                _serial = new ::LibCyberRadio::SerialPort(
                        dev, baudrate, 'N', 8, 1,
                        false, false, false
                );
            ret = _serial->open();
            if ( ret )
            {
                this->debug("[connectTty] Serial link established\n");
                // Test connection by sending an empty command
                this->debug("[connectTty] Testing connection\n");
                if ( sendCommand("\r\n") &&
                        (receive().size() > 0) )
                {
                }
                else
                {
                    std::ostringstream oss;
                    oss << "Connection test FAILED: ";
                    oss << _serial->getLastError();
                    _lastCmdErrInfo = oss.str();
                    ret = false;
                }
            }
            else
            {
                std::ostringstream oss;
                oss << "Serial link FAILED: ";
                if ( _serial != NULL )
                    oss << _serial->getLastError();
                else
                    oss << "Failed to establish serial link";
                _lastCmdErrInfo = oss.str();
                ret = false;
            }
            this->debug("[connectTty] Returning %s\n", this->debugBool(ret));
            return ret;
        }

        bool RadioTransport::sendCommandTcp(
                const std::string &cmdString,
                bool clearRx
            )
        {
            this->debug("[sendCommandTcp] Called; cmd=\"%s\"\n",
                    this->rawString(cmdString).c_str());
            bool ret = false;
            int bytes = send(_tcpSocket, cmdString.c_str(), cmdString.length(), 0);
            this->debug("[sendCommandTcp] -- Bytes sent: %d\n", bytes);
            if (bytes > 0)
            {
                ret = true;
            }
            else
            {
                translateErrno();
            }
            return ret;
        }

        bool RadioTransport::sendCommandUdp(
                const std::string& cmdString,
                bool clearRx
            )
        {
            bool ret = true;
            return ret;
        }

        bool RadioTransport::sendCommandHttps(
                const std::string &cmdString,
                bool clearRx
            )
        {
            this->debug("[sendCommandHttps] Called; cmd=\"%s\"\n",
                    this->rawString(cmdString).c_str());
            bool ret = false;
            if ( _httpsSession != NULL )
            {
                ret = _httpsSession->post(_httpsApiCmdUrl,
                        (void*)cmdString.c_str(),
                        cmdString.length(),
                        "application/json",
                        false);
                this->debug("[sendCommandHttps] HTTPS response code = %d\n",
                        _httpsSession->getResponseCode());
                // If the request failed, get the reason why.
                if ( !ret )
                {
                    // On a failed request, the radio may have returned a JSON
                    // response containing detailed response info.  If this is
                    // the case, it's not a problem at the transport level, so
                    // we actually want to proceed as if the request succeeded.
                    // This allows extended error info to be passed up to the
                    // radio handler level.
                    Json::Reader reader;
                    Json::Value jsonResponse;
                    if ( reader.parse(_httpsSession->getResponseBody(),
                            jsonResponse, false) )
                    {
                        ret = true;
                    }
                    // If the radio did not return a JSON response, then
                    // indicate why the transport action failed.
                    else
                    {
                        _lastCmdErrInfo = _httpsSession->getLastRequestErrorInfo();
                    }
                }
            }
            else
                _lastCmdErrInfo = "Transport is not connected";
            this->debug("[sendCommandHttps] Returning %s\n", this->debugBool(ret));
            return ret;
        }

        bool RadioTransport::sendCommandTty(
                const std::string& cmdString,
                bool clearRx
            )
        {
            this->debug("[sendCommandTty] Called; cmd=\"%s\"\n",
                    this->rawString(cmdString).c_str());
            bool ret = false;
            if ( _serial->write(cmdString) )
            {
                this->debug("[sendCommandTty] -- Command sent\n");
                ret = true;
            }
            else
            {
                _lastCmdErrInfo = _serial->getLastError();
            }
            return ret;
        }

        BasicStringList RadioTransport::receiveJson(
                double timeout
            )
        {
            std::deque<std::string> ret;
            if (_httpsSession != NULL)
                ret = receiveJsonHttps(timeout);
            return ret;
        }

        BasicStringList RadioTransport::receiveJsonHttps(
                double timeout
            )
        {
            this->debug("[receiveJsonHttps] Called; timeout=%0.1f\n", timeout);
            BasicStringList ret;
            // When receiving JSON over HTTPS, the session object gets the
            // HTTPS response body while servicing the request, so all we have
            // to do is retrieve it.
            if ( _httpsSession != NULL )
            {
                this->debug("[receiveJsonHttps] HTTPS response body = \"%s\"\n",
                        _httpsSession->getResponseBody().c_str());
                ret = Pythonesque::Split(_httpsSession->getResponseBody(), "\n");
            }
            else
                _lastCmdErrInfo = "Transport is not connected";
            return ret;
        }

        BasicStringList RadioTransport::receiveCli(
                double timeout
            )
        {
            std::deque<std::string> ret;
            if (_udpSocket > 0)
                ret = receiveCliUdp(timeout);
            else if (_tcpSocket > 0)
                ret = receiveCliTcp(timeout);
            else if (_serial != NULL)
                ret = receiveCliTty(timeout);
            return ret;
        }

        BasicStringList RadioTransport::receiveCliTcp(
                double timeout
            )
        {
            this->debug("[receiveCliTcp] Called; timeout=%0.1f\n", timeout);
            BasicStringList ret;
            std::ostringstream oss;
            fd_set ins;
            struct timeval tv;
            tv.tv_sec = (long)timeout;
            tv.tv_usec = (long)(1000000 * (timeout - (long)timeout));
            int nfds;
            char buf[1024];
            while (true)
            {
                FD_ZERO(&ins);
                FD_SET(_tcpSocket, &ins);
                this->debug("[receiveCliTcp] Selecting\n");
                nfds = select(_tcpSocket + 1, &ins, NULL, NULL, timeout < 0 ? NULL : &tv);
                this->debug("[receiveCliTcp] -- nfds = %d\n", nfds);
                if (nfds > 0)
                {
                    // data available
                    memset(buf, 0, sizeof(buf));
                    recv(_tcpSocket, buf, sizeof(buf), 0);
                    this->debug("[receiveCliTcp] Received chunk: \"%s\"\n", buf);
                    oss << buf;
                    // check for response terminator/prompt
                    if ( oss.str().rfind('>') != std::string::npos )
                        break;
                }
                else if (nfds == 0)
                {
                    // timeout
                    this->debug("[receiveCliTcp] Timeout\n");
                    _lastCmdErrInfo = "Timeout";
                    break;
                }
                else
                {
                    // Error in socket select
                    translateErrno();
                    this->debug("[receiveCliTcp] Socket select error: %s\n", _lastCmdErrInfo.c_str());
                    break;
                }
            }
            this->debug("[receiveCliTcp] Received: \"%s\"\n",
                    this->rawString(oss.str()).c_str());
            // Split the response into a list of non-empty strings
            // -- Remove carriage returns and prompt character
            std::string tmp = Pythonesque::Replace(Pythonesque::Replace(oss.str(), "\r", ""), ">", "");
            // -- Split on newlines
            BasicStringList tmpList = Pythonesque::Split(tmp, "\n");
            // -- Compile the non-empty strings into a list
            for (BasicStringList::iterator it = tmpList.begin(); it != tmpList.end(); it++)
            {
                tmp = Pythonesque::Rstrip(*it);
                if ( !tmp.empty() )
                    ret.push_back(tmp);
            }
            this->debug("[receiveCliTcp] Returning %u elements\n", ret.size());
            return ret;
        }

        BasicStringList RadioTransport::receiveCliUdp(
                double timeout
            )
        {
            BasicStringList ret;
            return ret;
        }

        BasicStringList RadioTransport::receiveCliTty(
                double timeout
            )
        {
            this->debug("[receiveCliTty] Called; timeout=%0.1f\n", timeout);
            BasicStringList ret;
            std::ostringstream oss;
            std::string rsp = "X";
            while ( rsp != "" )
            {
                rsp = _serial->read();
                oss << rsp;
                if ( Pythonesque::Endswith(oss.str(), ">") )
                    break;
            }
            this->debug("[receiveCliTty] Received: \"%s\"\n",
                    this->rawString(oss.str()).c_str());
            // Split the response into a list of non-empty strings
            // -- Remove carriage returns and prompt character
            std::string tmp = Pythonesque::Replace(Pythonesque::Replace(oss.str(), "\r", ""), ">", "");
            // -- Split on newlines
            BasicStringList tmpList = Pythonesque::Split(tmp, "\n");
            // -- Compile the non-empty strings into a list
            for (BasicStringList::iterator it = tmpList.begin(); it != tmpList.end(); it++)
            {
                tmp = Pythonesque::Rstrip(*it);
                if ( !tmp.empty() )
                    ret.push_back(tmp);
            }
            this->debug("[receiveCliTty] Returning %u elements\n", ret.size());
            return ret;
        }

        void RadioTransport::translateErrno()
        {
            char buf[256];
            memset(buf, 0, sizeof(buf));
            this->debug(strerror_r(errno, buf, sizeof(buf)));
            _lastCmdErrInfo = buf;
        }

    } /* namespace Driver */

} /* namespace LibCyberRadio */
