/***************************************************************************
 * \file SimpleIpSetup.cpp
 * \brief Defines a simple 1Gig data for NDR-class radios without 10Gig
 *     ports.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/SimpleIpSetup.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>


namespace LibCyberRadio
{

    namespace Driver
    {

        SimpleIpSetup::SimpleIpSetup(const std::string& name,
                RadioHandler* parent,
                bool debug,
                const std::string& sourceIP,
                const std::string& destIP,
                const std::string& destMAC) :
            Configurable(name, debug),
            _parent(parent),
            _sourceIP(sourceIP),
            _sourceMAC("00:00:00:00:00:00"),
            _destIP(destIP),
            _destMAC(destMAC)
        {
            initConfigurationDict();
        }

        SimpleIpSetup::~SimpleIpSetup()
        {
        }

        SimpleIpSetup::SimpleIpSetup(const SimpleIpSetup& other) :
            Configurable(other),
            _parent(other._parent),
            _sourceIP(other._sourceIP),
            _sourceMAC(other._sourceMAC),
            _destIP(other._destIP),
            _destMAC(other._destMAC)
        {
        }

        SimpleIpSetup& SimpleIpSetup::operator=(const SimpleIpSetup& other)
        {
            Configurable::operator=(other);
            if ( this != &other )
            {
                _parent = other._parent;
                _sourceIP = other._sourceIP;
                _sourceMAC = other._sourceMAC;
                _destIP = other._destIP;
                _destMAC = other._destMAC;
            }
            return *this;
        }

        bool SimpleIpSetup::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[SimpleIpSetup::setConfiguration] Called\n");
            // Call the base-class version to modify the configuration dictionary
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed.
            if ( cfg.hasKey("sourceIP") && _config.hasKey("sourceIP") )
            {
                ret &= setSourceIP(cfg["sourceIP"]);
            }
            if ( cfg.hasKey("destIP") && _config.hasKey("destIP") )
            {
                ret &= setDestIPAddress(cfg["destIP"]);
            }
            if ( cfg.hasKey("destMAC") && _config.hasKey("destMAC") )
            {
                ret &= setDestMACAddress(cfg["destMAC"]);
            }
            this->debug("[SimpleIpSetup::setConfiguration] Returning\n");
            return ret;
        }

        void SimpleIpSetup::queryConfiguration()
        {
            this->debug("[SimpleIpSetup::queryConfiguration] Called\n");
            // Query source and destination information
            if ( _config.hasKey("sourceIP") )
                executeSourceIPQuery(_sourceIP);
            if ( _config.hasKey("sourceMAC") )
                executeSourceMACQuery(_sourceMAC);
            if ( _config.hasKey("destIP") )
                executeDestIPQuery(_destIP);
            if ( _config.hasKey("destMAC") )
                executeDestMACQuery(_destMAC);
            updateConfigurationDict();
            this->debug("[SimpleIpSetup::queryConfiguration] Returning\n");
        }

        std::string SimpleIpSetup::getSourceMAC() const
        {
            return _sourceMAC;
        }

        std::string SimpleIpSetup::getSourceIP() const
        {
            return _sourceIP;
        }

        bool SimpleIpSetup::setSourceIP(const std::string& ipAddr)
        {
            bool ret = false;
            if ( _config.hasKey("sourceIP") )
            {
                std::string adjSourceIP = ipAddr;
                ret = executeSourceIPCommand(adjSourceIP);
                if ( ret )
                {
                    _sourceIP = adjSourceIP;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        std::string SimpleIpSetup::getDestMACAddress() const
        {
            return _destMAC;
        }

        std::string SimpleIpSetup::getDestIPAddress() const
        {
            return _destIP;
        }

        bool SimpleIpSetup::setDestMACAddress(const std::string& macAddr)
        {
            bool ret = false;
            if ( _config.hasKey("destMAC") )
            {
                std::string adjDestMAC = macAddr;
                ret = executeDestMACCommand(adjDestMAC);
                if ( ret )
                {
                    _destMAC = adjDestMAC;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        bool SimpleIpSetup::setDestIPAddress(const std::string& ipAddr)
        {
            bool ret = false;
            if ( _config.hasKey("destIP") )
            {
                std::string adjDestIP = ipAddr;
                ret = executeDestIPCommand(adjDestIP);
                if ( ret )
                {
                    _destIP = adjDestIP;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        void SimpleIpSetup::initConfigurationDict()
        {
            _config.clear();
            //this->debug("[SimpleIpSetup::initConfigurationDict] Called\n");
            _config["sourceIP"] = _sourceIP;
            _config["sourceMAC"] = _sourceMAC;
            _config["destIP"] = _destIP;
            _config["destMAC"] = _destMAC;
            //this->debug("[SimpleIpSetup::initConfigurationDict] Returning\n");
        }

        void SimpleIpSetup::updateConfigurationDict()
        {
            this->debug("[SimpleIpSetup::updateConfigurationDict] Called\n");
            if ( _config.hasKey("sourceIP") )
                setConfigurationValue("sourceIP", _sourceIP);
            if ( _config.hasKey("sourceMAC") )
                setConfigurationValue("sourceMAC", _sourceMAC);
            if ( _config.hasKey("destIP") )
                setConfigurationValue("destIP", _destIP);
            if ( _config.hasKey("destMAC") )
                setConfigurationValue("destMAC", _destMAC);
            this->debug("[SimpleIpSetup::updateConfigurationDict] Returning\n");
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeSourceMACQuery(std::string& macAddr)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "#MAC?" << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "#MAC ", ""),
                            ", ");
                    // vec[0] = Source MAC address
                    macAddr = vec[0];
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeSourceIPQuery(std::string& sourceIP)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "SIP?" << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "SIP ", ""),
                            ", ");
                    // vec[0] = Source IP address
                    sourceIP = vec[0];
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeSourceIPCommand(std::string& sourceIP)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "SIP "
                        << sourceIP
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeDestIPQuery(std::string& ipAddr)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "DIP?" << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "DIP ", ""),
                            ", ");
                    // vec[0] = Destination IP address
                    ipAddr = vec[0];
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeDestIPCommand(std::string& ipAddr)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "DIP "
                        << ipAddr
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeDestMACQuery(std::string& macAddr)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TDMAC?" << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TDMAC ", ""),
                            ", ");
                    // vec[0] = Destination MAC address
                    macAddr = vec[0];
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR472 pattern
        bool SimpleIpSetup::executeDestMACCommand(std::string& macAddr)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TDMAC "
                        << macAddr
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

    } /* namespace Driver */

} /* namespace LibCyberRadio */

