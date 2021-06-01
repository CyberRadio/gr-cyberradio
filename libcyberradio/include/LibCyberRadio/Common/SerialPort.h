/***************************************************************************
 * \file SerialPort.h
 *
 * \brief Serial port connection manager.
 *
 * \author DA
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_SERIALPORT_H_
#define INCLUDED_LIBCYBERRADIO_SERIALPORT_H_

#include "LibCyberRadio/Common/Debuggable.h"
#include <string>
#include <termios.h>


/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{

    /*!
     * \brief Class that manages communications with a serial port.
     */
    class SerialPort : public Debuggable
    {
        public:
            /**
             * \brief Constructs a SerialPort object.
             * \param device Serial device name (such as "/dev/ttyS0")
             * \param baudrate Baud rate
             * \param parity Parity setting. One of 'N' (none), 'E' (even), or
             *    'O' (odd).
             * \param databits Number of data bits
             * \param stopbits Number of stop bits
             * \param xonxoff Whether the serial port uses XON/XOFF (software)
             *     flow control
             * \param rtscts Whether the serial port uses RTS/CTS (hardware)
             *     flow control
             * \param debug Whether the transport emits debug output (Boolean).
             */
            SerialPort(
                    const std::string& device,
                    int baudrate = 115200,
                    char parity = 'N',
                    int databits = 8,
                    int stopbits = 1,
                    bool xonxoff = false,
                    bool rtscts = false,
                    bool debug = false
                );
            /**
             * \brief Destroys a SerialPort object.
             */
            ~SerialPort();
            /**
             * \brief Copies a SerialPort object.
             * \param other The SerialPort object to copy.
             */
            SerialPort(const SerialPort& other);
            /**
             * \brief Assignment operator for SerialPort objects.
             * \param other The RadioTransport object to copy.
             * \returns A reference to the assigned object.
             */
            SerialPort& operator=(const SerialPort& other);
            /**
             * \brief Open the serial port.
             * \returns True on success, false on error.  Use getLastError()
             *    to determine why the open failed.
             */
            bool open();
            /**
             * \brief Close the serial port.
             * \returns True on success, false on error.  Use getLastError()
             *    to determine why the open failed.
             */
            bool close();
            /**
             * \brief Reads data from the serial port.
             */
            std::string read();
            /**
             * \brief Writes data to the serial port.
             * \param data Data to write.
             * \returns True if data written successfully, false otherwise.
             */
            bool write(const std::string& data);
            /**
             * \brief Gets the current baud rate.
             * \note This method has meaning only if the port is open.
             * \returns The baud rate, in bytes per second.
             */
            int getBaudRate() const;
            /**
             * \brief Sets the current baud rate.
             * \note This method has meaning only if the port is open.
             * \param baudrate The baud rate, in bytes per second.
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool setBaudRate(int baudrate);
            /**
             * \brief Gets the current parity setting.
             * \note This method has meaning only if the port is open.
             * \returns The parity setting. One of 'N' (none), 'E' (even),
             *     or 'O' (odd).
             */
            char getParity() const;
            /**
             * \brief Sets the current parity setting.
             * \note This method has meaning only if the port is open.
             * \param parity The parity setting. One of 'N' (none), 'E' (even),
             *     or 'O' (odd).
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool setParity(char parity);
            /**
             * \brief Gets the current number of data bits.
             * \note This method has meaning only if the port is open.
             * \returns The number of data bits (5, 6, 7, or 8).
             */
            int getDataBits() const;
            /**
             * \brief Sets the current number of data bits.
             * \note This method has meaning only if the port is open.
             * \param databits The number of data bits (5, 6, 7, or 8).
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool setDataBits(int databits);
            /**
             * \brief Gets the current number of stop bits.
             * \note This method has meaning only if the port is open.
             * \returns The number of stop bits (1 or 2).
             */
            int getStopBits() const;
            /**
             * \brief Sets the current number of stop bits.
             * \note This method has meaning only if the port is open.
             * \param stopbits The number of data bits (1 or 2).
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool setStopBits(int stopbits);
            /**
             * \brief Gets whether the serial port currently uses XON/XOFF
             *    (software) flow control.
             * \note This method has meaning only if the port is open.
             * \returns True if XON/XOFF flow control is in use, false otherwise.
             */
            bool usesXonXoffFlowControl() const;
            /**
             * \brief Enables XON/XOFF (software) flow control on the serial port.
             * \note This method has meaning only if the port is open.
             * \param enabled Whether or not flow control should be used.
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool enableXonXoffFlowControl(bool enabled);
            /**
             * \brief Gets whether the serial port currently uses RTS/CTS
             *    (hardware) flow control.
             * \note This method has meaning only if the port is open.
             * \returns True if RTS/CTS flow control is in use, false otherwise.
             */
            bool usesRtsCtsFlowControl() const;
            /**
             * \brief Enables RTS/CTS (hardware) flow control on the serial port.
             * \note This method has meaning only if the port is open.
             * \param enabled Whether or not flow control should be used.
             * \returns True if successful, false otherwise.  Use getLastError()
             *    to determine why the call failed.
             */
            bool enableRtsCtsFlowControl(bool enabled);
            /**
             * \brief Gets the last error message.
             * \returns The last error message (string).
             */
            std::string getLastError() const;


        protected:
            // Serial device name
            std::string _device;
            // Baud rate
            int _baudrate;
            // Parity setting
            char _parity;
            // Data bits
            int _databits;
            // Stop bits
            int _stopbits;
            // Use XON/XOFF software flow control
            bool _useXonXoff;
            // Use RTS/CTS hardware flow control
            bool _useRtsCts;
            // Use DTS/DTR hardware flow control
            bool _useDtsDtr;
            // File descriptor
            int _fd;
            // Last error message
            std::string _lastError;
            // Receive buffer
            char* _recvBuf;
            // Receive buffer size
            int _recvBufSize;
            // Terminal settings
            struct termios _settings;
    };

} // namespace LibCyberRadio




#endif /* INCLUDED_LIBCYBERRADIO_SERIALPORT_H_ */
