/***************************************************************************
 * \file RadioTransport.h
 * \brief Defines an interface for transporting data to and from a radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_RADIOTRANSPORT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_RADIOTRANSPORT_H

#include "LibCyberRadio/Common/BasicList.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Common/HttpsSession.h"
#include "LibCyberRadio/Common/SerialPort.h"
#include <string>


/**
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /**
     * \brief Provides programming elements for driving CRS NDR-class radios.
     */
    namespace Driver
    {
        /**
         * \brief Generic radio transport class.
         *
         * The radio transport class provides a unified interface for transmitting
         * data to and from the radio, regardless of the connection method used
         * (serial/TTY, TCP, UDP, or HTTPS).
         */
        class RadioTransport : public Debuggable
        {
            public:
                /**
                 * \brief Constructs a RadioTransport object.
                 * \param json Whether the transport should expect JSON-formatted
                 *    commands and responses (Boolean).
                 * \param debug Whether the transport emits debug output (Boolean).
                 */
                RadioTransport(
                        bool json = false,
                        bool debug = false
                );
                /**
                 * \brief Destroys a RadioTransport object.
                 */
                virtual ~RadioTransport();
                /**
                 * \brief Copies a RadioTransport object.
                 * \param other The RadioTransport object to copy.
                 */
                RadioTransport(const RadioTransport& other);
                /**
                 * \brief Assignment operator for RadioTransport objects.
                 * \param other The RadioTransport object to copy.
                 * \returns A reference to the assigned object.
                 */
                RadioTransport& operator=(const RadioTransport& other);
                /**
                 * \brief Connects to the radio.
                 * \param mode The connection mode.  One of "tty", "tcp", "udp",
                 *    or "https".
                 * \param host_or_dev Either the host name or IP address (for TCP
                 *    or UDP) or the serial device name (for TTY).
                 * \param port_or_baudrate Either the port number (for TCP or UDP)
                 *    or the serial baud rate (for TTY).TCP
                 * \returns True if the connection succeeds, false otherwise.
                 */
                virtual bool connect(
                        const std::string& mode,
                        const std::string& host_or_dev,
                        const int port_or_baudrate
                );
                /**
                 * \brief Disconnects from the radio.
                 */
                virtual void disconnect();
                /**
                 * \brief Gets whether the transport is connected.
                 * \returns True if connected, false otherwise.
                 */
                virtual bool isConnected() const;
                /**
                 * \brief Sends a command to the radio over the transport.
                 * \param cmdString The command to send.
                 * \param clearRx Whether or not to clear the receive buffer before
                 *    sending the command.
                 * \returns True if the command was sent successfully, false otherwise.
                 */
                virtual bool sendCommand(
                        const std::string& cmdString,
                        bool clearRx = true
                );
                /**
                 * \brief Receives a command response from the radio.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns If the transport is using JSON, this is a JSON-formatted
                 *    string; if not, this is a list of received data strings.
                 */
                virtual BasicStringList receive(
                        double timeout = -1
                );
                /**
                 * \brief Gets the error information for the last command.
                 * \returns A string containing the error message.
                 */
                virtual std::string getLastCommandErrorInfo() const;

            protected:
                /**
                 * \brief Connects to the radio using TCP.
                 * \param host The host name or IP address.
                 * \param port The port number.
                 * \returns True if the connection succeeds, false otherwise.
                 */
                virtual bool connectTcp(
                        const std::string& host,
                        int port
                );
                /**
                 * \brief Connects to the radio using UDP.
                 * \param host The host name or IP address.
                 * \param port The port number.
                 * \returns True if the connection succeeds, false otherwise.
                 */
                virtual bool connectUdp(
                        const std::string& host,
                        int port
                );
                /**
                 * \brief Connects to the radio using HTTPS.
                 * \param host The host name or IP address.
                 * \param port The port number.
                 * \returns True if the connection succeeds, false otherwise.
                 */
                virtual bool connectHttps(
                        const std::string& host,
                        int port
                );
                /**
                 * \brief Connects to the radio using a serial link.
                 * \param dev The device name for the serial port.
                 * \param baudrate The serial baud rate.
                 * \returns True if the connection succeeds, false otherwise.
                 */
                virtual bool connectTty(
                        const std::string& dev,
                        int baudrate
                );
                /**
                 * \brief Sends a command to the radio over TCP.
                 * \param cmdString The command to send.
                 * \param clearRx Whether or not to clear the receive buffer before
                 *    sending the command.
                 * \returns True if the command was sent successfully, false otherwise.
                 */
                virtual bool sendCommandTcp(
                        const std::string& cmdString,
                        bool clearRx = true
                );
                /**
                 * \brief Sends a command to the radio over UDP.
                 * \param cmdString The command to send.
                 * \param clearRx Whether or not to clear the receive buffer before
                 *    sending the command.
                 * \returns True if the command was sent successfully, false otherwise.
                 */
                virtual bool sendCommandUdp(
                        const std::string& cmdString,
                        bool clearRx = true
                );
                /**
                 * \brief Sends a command to the radio over HTTPS.
                 * \param cmdString The command to send.
                 * \param clearRx Whether or not to clear the receive buffer before
                 *    sending the command.
                 * \returns True if the command was sent successfully, false otherwise.
                 */
                virtual bool sendCommandHttps(
                        const std::string& cmdString,
                        bool clearRx = true
                );
                /**
                 * \brief Sends a command to the radio over TTY.
                 * \param cmdString The command to send.
                 * \param clearRx Whether or not to clear the receive buffer before
                 *    sending the command.
                 * \returns True if the command was sent successfully, false otherwise.
                 */
                virtual bool sendCommandTty(
                        const std::string& cmdString,
                        bool clearRx = true
                );
                /**
                 * \brief Receives a JSON-formatted command response from the radio.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveJson(
                        double timeout = -1
                );
                // receiveJsonTcp()
                // receiveJsonTty()
                // receiveJsonUdp()
                /**
                 * \brief Receives a JSON-formatted command response from the radio
                 *    using HTTPS.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveJsonHttps(
                        double timeout = -1
                );
                /**
                 * \brief Receives a client (AT-command-style) command response from
                 *    the radio.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveCli(
                        double timeout = -1
                );
                /**
                 * \brief Receives a client (AT-command-style) command response over TCP.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveCliTcp(
                        double timeout = -1
                );
                /**
                 * \brief Receives a client (AT-command-style) command response over UDP.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveCliUdp(
                        double timeout = -1
                );
                /**
                 * \brief Receives a client (AT-command-style) command response over TTY.
                 * \param timeout The timeout value to use for receiving data.  If -1,
                 *    use the default timeout value for the transport.
                 * \returns A list of received data strings.
                 */
                virtual BasicStringList receiveCliTty(
                        double timeout = -1
                );
                /**
                 * \brief Translates an errno value into an error message.
                 */
                virtual void translateErrno();

            protected:
                // Is this transport using JSON?
                bool _isJson;
                // TCP socket descriptor
                int _tcpSocket;
                // UDP socket descriptor
                int _udpSocket;
                // TTY (serial) link object
                ::LibCyberRadio::SerialPort* _serial;
                // HTTPS session variables
                HttpsSession* _httpsSession;
                // -- Connection test and API command URLs
                std::string _httpsConnTestUrl;
                std::string _httpsApiCmdUrl;
                // Error message from the last command executed
                std::string _lastCmdErrInfo;

        };


    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_RADIOTRANSPORT_H */
