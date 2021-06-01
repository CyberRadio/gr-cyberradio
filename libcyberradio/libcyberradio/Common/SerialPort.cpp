/***************************************************************************
 * \file SerialPort.cpp
 *
 * \brief Implements a serial port connection manager.
 *
 * \author DA
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#include "LibCyberRadio/Common/SerialPort.h"
#include "LibCyberRadio/Common/BasicList.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <string.h>
#include <sys/select.h>


namespace LibCyberRadio
{

    SerialPort::SerialPort(
            const std::string& device,
            int baudrate,
            char parity,
            int databits,
            int stopbits,
            bool xonxoff,
            bool rtscts,
            bool debug
        ) :
        Debuggable(debug, "SerialPort"),
        _device(device),
        _baudrate(baudrate),
        _parity(parity),
        _databits(databits),
        _stopbits(stopbits),
        _useXonXoff(xonxoff),
        _useRtsCts(rtscts),
        _useDtsDtr(false),
        _fd(-1),
        _lastError(""),
        _recvBuf(NULL),
        _recvBufSize(1024)
    {
        memset(&_settings, 0, sizeof(struct termios));
        this->debug("CONSTRUCTED\n");
    }

    SerialPort::~SerialPort()
    {
        // Close the serial port if it is open
        close();
        // Destroy the receive buffer
        if ( _recvBuf != NULL )
            delete _recvBuf;
        this->debug("DESTROYED\n");
    }

    SerialPort::SerialPort(const SerialPort& other) :
        Debuggable(other),
        _device(other._device),
        _baudrate(other._baudrate),
        _parity(other._parity),
        _databits(other._databits),
        _stopbits(other._stopbits),
        _useXonXoff(other._useXonXoff),
        _useRtsCts(other._useRtsCts),
        _useDtsDtr(other._useDtsDtr),
        _fd(other._fd),
        _lastError(other._lastError),
        _recvBuf(other._recvBuf),
        _recvBufSize(other._recvBufSize)
    {
        memcpy(&_settings, &(other._settings), sizeof(struct termios));
    }

    SerialPort& SerialPort::operator=(const SerialPort& other)
    {
        Debuggable::operator=(other);
        // Prevent self-assignment
        if ( this != &other )
        {
            _device = other._device;
            _baudrate = other._baudrate;
            _parity = other._parity;
            _databits = other._databits;
            _stopbits = other._stopbits;
            _useXonXoff = other._useXonXoff;
            _useRtsCts = other._useRtsCts;
            _useDtsDtr = other._useDtsDtr;
            _fd = other._fd;
            _lastError = other._lastError;
            _recvBuf = other._recvBuf;
            _recvBufSize = other._recvBufSize;
            memcpy(&_settings, &(other._settings), sizeof(struct termios));
        }
        return *this;
    }

    bool SerialPort::open()
    {
        this->debug("[open] Called\n");
        bool ret = true;
        _lastError = "";
        BasicStringList errors;
        // Open the serial port device file
        this->debug("[open] Opening port\n");
        _fd = ::open(_device.c_str(), O_RDWR | O_NOCTTY | O_NDELAY);
        this->debug("[open] -- FD = %d\n", _fd);
        if ( _fd != -1 )
        {
            // Set flags on serial port device file
            ::fcntl(_fd, F_SETFL, 0);
            // Get the current port settings
            this->debug("[open] Getting port settings\n");
            if ( tcgetattr(_fd, &_settings) == 0 )
            {
                this->debug("[open] -- SUCCESS\n");
                this->debug("[open] Setting initial port settings\n");
                // Put port in "raw" mode (non-canonical N-8-1, no special processing)
                cfmakeraw(&_settings);
                // Turn on ability to read the port
                _settings.c_cflag |= CREAD;
                // Ignore modem control settings
                _settings.c_cflag |= CLOCAL;
                // Set port to retrieve bytes as they are available
                _settings.c_cc[VMIN] = 0;     // don't block if no bytes are available
                _settings.c_cc[VTIME] = 1;    // 1/10 second inter-byte timeout
                // Apply settings to the port
                if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
                {
                    this->debug("[open] -- SUCCESS\n");
                }
                else
                {
                    this->debug("[open] -- FAILED\n");
                    errors.push_back( strerror(errno) );
                }
                // Apply terminal settings
                if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
                {
                    this->debug("[open] -- SUCCESS\n");
                }
                else
                {
                    this->debug("[open] -- FAILED\n");
                    errors.push_back( strerror(errno) );
                }
                // Set baud rate
                if ( !setBaudRate(_baudrate) )
                {
                     errors.push_back( _lastError );
                }
                // Set parity
                if ( !setParity(_parity) )
                {
                     errors.push_back( _lastError );
                }
                // Set data bits
                if ( !setDataBits(_databits) )
                {
                     errors.push_back( _lastError );
                }
                // Set stop bits
                if ( !setStopBits(_stopbits) )
                {
                     errors.push_back( _lastError );
                }
                // Set XON/XOFF software flow control
                if ( !enableXonXoffFlowControl(_useXonXoff) )
                {
                     errors.push_back( _lastError );
                }
                // Set RTS/CTS hardware flow control
                if ( !enableRtsCtsFlowControl(_useRtsCts) )
                {
                     errors.push_back( _lastError );
                }
                // Set DTS/DTR hardware flow control (not supported on Linux)
            }
            else
            {
                this->debug("[open] -- FAILED\n");
                errors.push_back( strerror(errno) );
            }
        }
        // Create the receive buffer on success
        if ( errors.size() == 0 )
        {
            _recvBuf = new char[_recvBufSize];
        }
        // Set last error if there was a failure
        if ( errors.size() > 0 )
        {
            _lastError = Pythonesque::Join(errors, ", ");
            this->debug("[open] ERROR: %s\n", _lastError.c_str());
            ret = false;
            if ( _fd != -1 )
            {
                ::close(_fd);
                _fd = -1;
            }
        }
        this->debug("[open] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    bool SerialPort::close()
    {
        this->debug("[close] Called\n");
        bool ret = false;
        _lastError = "";
        if ( _fd != -1 )
        {
            ::close(_fd);
            ret = true;
        }
        else
            _lastError = "Port already closed";
        _fd = -1;
        if ( _lastError != "" )
            this->debug("[close] ERROR: %s\n", _lastError.c_str());
        this->debug("[close] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    std::string SerialPort::read()
    {
        this->debug("[read] Called\n");
        std::string ret;
        _lastError = "";
        // Check for waiting data
        ssize_t bytes = 1;
        this->debug("[read] Entering read loop\n");
        while ( (bytes > 0) && (_lastError == "") )
        {
            bytes = 0;
            memset(_recvBuf, 0, _recvBufSize);
            this->debug("[read] -- Reading data\n");
            bytes = ::read(_fd, _recvBuf, _recvBufSize);
            this->debug("[read]    -- Bytes = %d\n", bytes);
            if ( bytes > 0 )
            {
                // Data was read
                for (int i = 0; i < bytes; i++)
                {
                    this->debug("[read]       -- %02x\n", (int)_recvBuf[i]);
                }
                ret += _recvBuf;
            }
            else if ( bytes < 0 )
            {
                // Error condition
                _lastError = strerror(errno);
            }
        }
        // Identify timeout condition (no error up to this point, but
        // no data received, either)
        if ( (ret == "") && (_lastError == "") )
            _lastError = "Timeout";
        if ( _lastError != "" )
            this->debug("[read] ERROR: %s\n", _lastError.c_str());
        this->debug("[read] Returning \"%s\"\n", ret.c_str());
        return ret;
    }

    bool SerialPort::write(const std::string& data)
    {
        this->debug("[write] Called\n");
        bool ret = false;
        _lastError = "";
        this->debug("[write] Writing data\n");
        ssize_t bytes = ::write(_fd, data.c_str(), data.size());
        this->debug("[write] -- Bytes = %d\n", bytes);
        if ( bytes > 0 )
        {
            // Data was written
            ret = true;
            // Delay slightly to allow the data to be written and
            // to receive a response
            usleep(100);
        }
        else if ( bytes == 0 )
        {
            // No data was written
            _lastError = "No data written";
        }
        else
        {
            // Error condition
            _lastError = strerror(errno);
        }
        if ( !ret )
            this->debug("[write] ERROR: %s\n", _lastError.c_str());
        this->debug("[write] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    int SerialPort::getBaudRate() const
    {
        return _baudrate;
    }

    bool SerialPort::setBaudRate(int baudrate)
    {
        this->debug("[setBaudRate] Called, baudrate=%d\n", baudrate);
        bool ret = true;
        _lastError = "";
        // Translate incoming baud rate into a termios baud rate constant
        int baud = -1;
        switch( baudrate )
        {
            case 50:
                baud = B50;
                break;
            case 75:
                baud = B75;
                break;
            case 110:
                baud = B110;
                break;
            case 134:
                baud = B134;
                break;
            case 150:
                baud = B150;
                break;
            case 200:
                baud = B200;
                break;
            case 300:
                baud = B300;
                break;
            case 600:
                baud = B600;
                break;
            case 1200:
                baud = B1200;
                break;
            case 2400:
                baud = B2400;
                break;
            case 4800:
                baud = B4800;
                break;
            case 9600:
                baud = B9600;
                break;
            case 19200:
                baud = B19200;
                break;
            case 38400:
                baud = B38400;
                break;
            case 57600:
                baud = B57600;
                break;
            case 115200:
                baud = B115200;
                break;
            case 230400:
                baud = B230400;
                break;
            case 460800:
                baud = B460800;
                break;
            case 500000:
                baud = B500000;
                break;
            case 576000:
                baud = B576000;
                break;
            case 921600:
                baud = B921600;
                break;
            case 1000000:
                baud = B1000000;
                break;
            case 1152000:
                baud = B1152000;
                break;
            case 1500000:
                baud = B1500000;
                break;
            case 2000000:
                baud = B2000000;
                break;
            case 2500000:
                baud = B2500000;
                break;
            case 3000000:
                baud = B3000000;
                break;
            case 3500000:
                baud = B3500000;
                break;
            case 4000000:
                baud = B4000000;
                break;
            default:
                _lastError = "Unsupported baud rate";
                ret = false;
        }
        // If successful, apply current settings
        if (ret)
        {
            this->debug("[getBaudRate] Setting port speed settings\n");
            if ( (cfsetispeed(&_settings, baud) == 0) &&
                 (cfsetospeed(&_settings, baud) == 0) &&
                 (tcsetattr(_fd, TCSANOW, &_settings) == 0) )
            {
                this->debug("[getBaudRate] -- SUCCESS\n");
                _baudrate = baudrate;
            }
            else
            {
                this->debug("[getBaudRate] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[getBaudRate] ERROR: %s\n", _lastError.c_str());
        this->debug("[getBaudRate] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    char SerialPort::getParity() const
    {
        return _parity;
    }

    bool SerialPort::setParity(char parity)
    {
        this->debug("[setParity] Called, parity=%c\n", parity);
        bool ret = true;
        _lastError = "";
        // Validate parity setting
        if ( (parity != 'N') && (parity != 'O') && (parity != 'E') )
        {
            _lastError = "Unsupported parity setting";
            ret = false;
        }
        // If successful, apply current settings
        if (ret)
        {
            this->debug("[setParity] Setting port parity settings\n");
            // Clear parity on and odd bits (parity None)
            _settings.c_cflag &= ~PARENB;
            _settings.c_cflag &= ~PARODD;
            if ( parity != 'N' )
            {
                // Set parity on bit
                _settings.c_cflag |= PARENB;
                if ( parity == 'O' )
                    // Set parity odd bit
                    _settings.c_cflag |= PARODD;
            }
            if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
            {
                this->debug("[setParity] -- SUCCESS\n");
                _parity = parity;
            }
            else
            {
                this->debug("[setParity] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[setParity] ERROR: %s\n", _lastError.c_str());
        this->debug("[setParity] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    int SerialPort::getDataBits() const
    {
        return _databits;
    }

    bool SerialPort::setDataBits(int databits)
    {
        this->debug("[setDataBits] Called, databits=%d\n", databits);
        bool ret = true;
        _lastError = "";
        // Translate incoming data bits into a termios data bits constant
        int dbits = -1;
        switch ( databits )
        {
            case 5:
                dbits = CS5;
                break;
            case 6:
                dbits = CS6;
                break;
            case 7:
                dbits = CS7;
                break;
            case 8:
                dbits = CS8;
                break;
            default:
                _lastError = "Unsupported data bits size";
                ret = false;
        }
        // If successful, apply current settings
        if (ret)
        {
            this->debug("[setDataBits] Setting port data bit settings\n");
            // Clear existing size bits
            _settings.c_cflag &= ~CSIZE;
            // Apply new size bits
            _settings.c_cflag |= dbits;
            if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
            {
                this->debug("[setDataBits] -- SUCCESS\n");
                _databits = databits;
            }
            else
            {
                this->debug("[setDataBits] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[setDataBits] ERROR: %s\n", _lastError.c_str());
        this->debug("[setDataBits] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    int SerialPort::getStopBits() const
    {
        return _stopbits;
    }

    bool SerialPort::setStopBits(int stopbits)
    {
        this->debug("[setStopBits] Called, stopbits=%d\n", stopbits);
        bool ret = true;
        _lastError = "";
        // Validate incoming stop bits
        if ( (stopbits != 1) && (stopbits != 2) )
        {
            _lastError = "Unsupported stop bits size";
            ret = false;
        }
        // If successful, apply current settings
        if (ret)
        {
            this->debug("[setStopBits] Setting port data bit settings\n");
            if ( stopbits == 2 )
                // Set two stop bits bit
                _settings.c_cflag |= CSTOPB;
            else
                // Clear two stop bits bit
                _settings.c_cflag &= ~CSTOPB;
            if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
            {
                this->debug("[setStopBits] -- SUCCESS\n");
                _stopbits = stopbits;
            }
            else
            {
                this->debug("[setStopBits] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[setStopBits] ERROR: %s\n", _lastError.c_str());
        this->debug("[setStopBits] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    bool SerialPort::usesXonXoffFlowControl() const
    {
        return _useXonXoff;
    }

    bool SerialPort::enableXonXoffFlowControl(bool enabled)
    {
        this->debug("[enableXonXoffFlowControl] Called, enabled=%s\n",
                    this->debugBool(enabled));
        bool ret = true;
        _lastError = "";
        // Apply current settings
        if (ret)
        {
            this->debug("[enableXonXoffFlowControl] Setting port XON/XOFF settings\n");
            if ( enabled )
                // Turn ON XON/XOFF software flow control
                _settings.c_iflag |= (IXON | IXOFF | IXANY);
            else
                // Turn OFF XON/XOFF software flow control
                _settings.c_iflag &= ~(IXON | IXOFF | IXANY);
            if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
            {
                this->debug("[enableXonXoffFlowControl] -- SUCCESS\n");
                _useXonXoff = enabled;
            }
            else
            {
                this->debug("[enableXonXoffFlowControl] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[enableXonXoffFlowControl] ERROR: %s\n", _lastError.c_str());
        this->debug("[enableXonXoffFlowControl] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    bool SerialPort::usesRtsCtsFlowControl() const
    {
        return _useRtsCts;
    }

    bool SerialPort::enableRtsCtsFlowControl(bool enabled)
    {
        this->debug("[enableRtsCtsFlowControl] Called, enabled=%s\n",
                    this->debugBool(enabled));
        bool ret = true;
        _lastError = "";
        // Apply current settings
        if (ret)
        {
            this->debug("[enableRtsCtsFlowControl] Setting port XON/XOFF settings\n");
            if ( enabled )
                // Turn ON RTS/CTS hardware flow control
                _settings.c_cflag |= CRTSCTS;
            else
                // Turn OFF RTS/CTS hardware flow control
                _settings.c_cflag &= ~CRTSCTS;
            if ( tcsetattr(_fd, TCSANOW, &_settings) == 0 )
            {
                this->debug("[enableRtsCtsFlowControl] -- SUCCESS\n");
                _useRtsCts = enabled;
            }
            else
            {
                this->debug("[enableRtsCtsFlowControl] -- FAILED\n");
                _lastError = strerror(errno);
                ret = false;
            }
        }
        if ( !ret )
            this->debug("[enableRtsCtsFlowControl] ERROR: %s\n", _lastError.c_str());
        this->debug("[enableRtsCtsFlowControl] Returning %s\n", this->debugBool(ret));
        return ret;
    }

    std::string SerialPort::getLastError() const
    {
        return _lastError;
    }

} // namespace LibCyberRadio

