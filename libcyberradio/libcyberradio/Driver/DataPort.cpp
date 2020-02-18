/***************************************************************************
 * \file DataPort.cpp
 * \brief Defines the basic 10GigE data port interface for an
 *    NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/DataPort.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>


namespace LibCyberRadio
{

    namespace Driver
    {

        DataPort::DataPort(const std::string& name,
                int index,
                RadioHandler* parent,
                bool debug,
                const std::string& sourceIP,
                int numDataPortDipEntries,
                int dataPortDipEntryIndexBase) :
            Configurable(name, debug),
            _index(index),
            _parent(parent),
            _sourceIP(sourceIP),
            _numDipEntries(numDataPortDipEntries),
            _dipEntryIndexBase(dataPortDipEntryIndexBase),
            _errorsEnabled(true),
            _flowControlEnabled(true)
        {
            initConfigurationDict();
        }

        DataPort::~DataPort()
        {
        }

        DataPort::DataPort(const DataPort& other) :
            Configurable(other),
            _index(other._index),
            _parent(other._parent),
            _sourceIP(other._sourceIP),
            _numDipEntries(other._numDipEntries),
            _macAddresses(other._macAddresses),
            _ipAddresses(other._ipAddresses),
            _sourcePorts(other._sourcePorts),
            _destPorts(other._destPorts),
            _dipEntryIndexBase(other._dipEntryIndexBase),
            _errorsEnabled(other._errorsEnabled),
            _flowControlEnabled(other._flowControlEnabled)
        {
        }

        DataPort& DataPort::operator=(const DataPort& other)
        {
            Configurable::operator=(other);
            if ( this != &other )
            {
                _index = other._index;
                _parent = other._parent;
                _sourceIP = other._sourceIP;
                _numDipEntries = other._numDipEntries;
                _macAddresses = other._macAddresses;
                _ipAddresses = other._ipAddresses;
                _sourcePorts = other._sourcePorts;
                _destPorts = other._destPorts;
                _dipEntryIndexBase = other._dipEntryIndexBase;
                _errorsEnabled = other._errorsEnabled;
                _flowControlEnabled = other._flowControlEnabled;
            }
            return *this;
        }

        bool DataPort::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[DataPort::setConfiguration] Called\n");
            // Call the base-class version to modify the configuration dictionary
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed.
            if ( cfg.hasKey("sourceIP") && _config.hasKey("sourceIP") )
            {
                ret &= setSourceIP(cfg["sourceIP"]);
            }
            if ( cfg.hasKey("errors") && _config.hasKey("errors") )
            {
                ret &= enableErrors( cfg["errors"].asBool() );
            }
            if ( cfg.hasKey("flowControl") && _config.hasKey("flowControl") )
            {
                ret &= enableFlowControl( cfg["flowControl"].asBool() );
            }
            this->debug("[DataPort::setConfiguration] Returning\n");
            return ret;
        }

        void DataPort::queryConfiguration()
        {
            this->debug("[DataPort::queryConfiguration] Called\n");
            // Query source and destination information
            if ( _config.hasKey("sourceIP") )
                executeSourceIPQuery(_index, _sourceIP);
            if ( _config.hasKey("errors") )
                executeErrorEnabledQuery(_index, _errorsEnabled);
            if ( _config.hasKey("flowControl") )
                executeFlowControlEnabledQuery(_index, _flowControlEnabled);
            for (int dipIndex = _dipEntryIndexBase;
                    dipIndex < _dipEntryIndexBase + _numDipEntries;
                    dipIndex++)
            {
                executeDestIPQuery(_index, dipIndex,
                        _macAddresses[dipIndex],
                        _ipAddresses[dipIndex],
                        _sourcePorts[dipIndex],
                        _destPorts[dipIndex]);
            }
            updateConfigurationDict();
            this->debug("[DataPort::queryConfiguration] Returning\n");
        }

        int DataPort::getNumDestEntries() const
        {
            return _numDipEntries;
        }

        BasicIntList DataPort::getDestEntryIndexRange() const
        {
            BasicIntList ret;
            for (int dipIndex = _dipEntryIndexBase;
                    dipIndex < _dipEntryIndexBase + _numDipEntries;
                    dipIndex++)
            {
                ret.push_back(dipIndex);
            }
            return ret;
        }

        std::string DataPort::getSourceIP() const
        {
            return _sourceIP;
        }

        bool DataPort::setSourceIP(const std::string& ipAddr)
        {
            bool ret = false;
            if ( _config.hasKey("sourceIP") )
            {
                std::string adjSourceIP = ipAddr;
                ret = executeSourceIPCommand(_index, adjSourceIP);
                if ( ret )
                {
                    _sourceIP = adjSourceIP;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        std::string DataPort::getDestMACAddress(int dipIndex) const
        {
            std::string ret;
            if ( _macAddresses.find(dipIndex) != _macAddresses.end() )
                ret = _macAddresses.at(dipIndex);
            return ret;
        }

        std::string DataPort::getDestIPAddress(int dipIndex) const
        {
            std::string ret;
            if ( _ipAddresses.find(dipIndex) != _ipAddresses.end() )
                ret = _ipAddresses.at(dipIndex);
            return ret;
        }

        unsigned int DataPort::getDestSourcePort(int dipIndex) const
        {
            int ret = 0;
            if ( _sourcePorts.find(dipIndex) != _sourcePorts.end() )
                ret = _sourcePorts.at(dipIndex);
            return ret;
        }

        unsigned int DataPort::getDestDestPort(int dipIndex) const
        {
            int ret = 0;
            if ( _destPorts.find(dipIndex) != _destPorts.end() )
                ret = _destPorts.at(dipIndex);
            return ret;
        }

        bool DataPort::setDestInfo(int dipIndex,
                const std::string& ipAddr,
                const std::string& macAddr,
                unsigned int sourcePort,
                unsigned int destPort)
        {
            std::string adjIp = ipAddr;
            std::string adjMac = macAddr;
            unsigned int adjSrc = sourcePort;
            unsigned int adjDst = destPort;
            bool ret = executeDestIPCommand(_index, dipIndex, adjIp, adjMac,
                    adjSrc, adjDst);
            if ( ret )
            {
                _macAddresses[dipIndex] = adjMac;
                _ipAddresses[dipIndex] = adjIp;
                _sourcePorts[dipIndex] = adjSrc;
                _destPorts[dipIndex] = adjDst;
                //updateConfigurationDict();
            }
            return ret;
        }

        bool DataPort::setDestMACAddress(int dipIndex, const std::string& macAddr)
        {
            return setDestInfo(dipIndex,
                    _ipAddresses[dipIndex],
                    macAddr,
                    _sourcePorts[dipIndex],
                    _destPorts[dipIndex]);
        }

        bool DataPort::setDestIPAddress(int dipIndex, const std::string& ipAddr)
        {
            return setDestInfo(dipIndex,
                    ipAddr,
                    _macAddresses[dipIndex],
                    _sourcePorts[dipIndex],
                    _destPorts[dipIndex]);
        }

        bool DataPort::setDestSourcePort(int dipIndex, unsigned int sourcePort)
        {
            return setDestInfo(dipIndex,
                    _ipAddresses[dipIndex],
                    _macAddresses[dipIndex],
                    sourcePort,
                    _destPorts[dipIndex]);
        }

        bool DataPort::setDestDestPort(int dipIndex, unsigned int destPort)
        {
            return setDestInfo(dipIndex,
                    _ipAddresses[dipIndex],
                    _macAddresses[dipIndex],
                    _sourcePorts[dipIndex],
                    destPort);
        }

        bool DataPort::enableErrors(bool enabled)
        {
            bool ret = false;
            if ( _config.hasKey("errors") )
            {
                bool adjEn = enabled;
                if ( executeErrorEnabledCommand(_index, adjEn) )
                {
                    _errorsEnabled = enabled;
                    updateConfigurationDict();
                    ret = true;
                }
            }
            return ret;
        }

        bool DataPort::disableErrors()
        {
            return enableErrors(false);
        }

        bool DataPort::enableFlowControl(bool enabled)
        {
            bool ret = false;
            if ( _config.hasKey("errors") )
            {
                bool adjEn = enabled;
                if ( executeFlowControlEnabledCommand(_index, adjEn) )
                {
                    _flowControlEnabled = enabled;
                    updateConfigurationDict();
                    ret = true;
                }
            }
            return ret;
        }

        bool DataPort::disableFlowControl()
        {
            return enableFlowControl(false);
        }

        void DataPort::initConfigurationDict()
        {
            _config.clear();
            //this->debug("[DataPort::initConfigurationDict] Called\n");
            _config["sourceIP"] = _sourceIP;
            _config["errors"] = _errorsEnabled;
            _config["flowControl"] = _flowControlEnabled;
            //this->debug("[DataPort::initConfigurationDict] Returning\n");
        }

        void DataPort::updateConfigurationDict()
        {
            this->debug("[DataPort::updateConfigurationDict] Called\n");
            if ( _config.hasKey("sourceIP") )
                setConfigurationValue("sourceIP", _sourceIP);
            if ( _config.hasKey("errors") )
                setConfigurationValueToBool("errors", _errorsEnabled);
            if ( _config.hasKey("flowControl") )
                setConfigurationValueToBool("flowControl", _flowControlEnabled);
            this->debug("[DataPort::updateConfigurationDict] Returning\n");
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeSourceIPQuery(int index, std::string& sourceIP)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "SIP? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "SIP ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Source IP address
                    sourceIP = vec[1];
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeSourceIPCommand(int index, std::string& sourceIP)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "SIP " << index
                        << ", " << sourceIP
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeDestIPQuery(int index,
                int dipIndex,
                std::string& ipAddr,
                std::string& macAddr,
                unsigned int& sourcePort,
                unsigned int& destPort)
        {
            bool ret = false;
            ipAddr = "";
            macAddr = "";
            sourcePort = 0;
            destPort = 0;
            if ( (_parent != NULL) && (_parent->isConnected()) &&
                    ( _macAddresses.find(dipIndex) != _macAddresses.end()) )
            {
                std::ostringstream oss;
                oss << "DIP? " << index << ", " << dipIndex << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    if ( Pythonesque::Startswith(rsp.front(), "DIP") )
                    {
                        BasicStringList vec = Pythonesque::Split(
                                Pythonesque::Replace(rsp.front(), "DIP ", ""),
                                ", ");
                        // vec[0] = Index
                        // vec[1] = Destination index
                        // vec[2] = IP address (with lots of leading spaces)
                        //this->debug("[DataPort::executeDestIPQuery] IP addr string=\"%s\"\n", vec[2].c_str());
                        ipAddr = Pythonesque::Strip(vec[2]);
                        //this->debug("[DataPort::executeDestIPQuery] -- converted=\"%s\"\n", ipAddr.c_str());
                        // vec[3] = MAC address
                        //this->debug("[DataPort::executeDestIPQuery] MAC addr string=\"%s\"\n", vec[3].c_str());
                        macAddr = Pythonesque::Strip(vec[3]);
                        //this->debug("[DataPort::executeDestIPQuery] -- converted=\"%s\"\n", macAddr.c_str());
                        // vec[4] = UDP port
                        //this->debug("[DataPort::executeDestIPQuery] Source UDP port string=\"%s\"\n", vec[4].c_str());
                        sourcePort = boost::lexical_cast<unsigned int>(Pythonesque::Strip(vec[4]));
                        //this->debug("[DataPort::executeDestIPQuery] -- converted=%u\n", udpPort);
                        // vec[5] = Stream ID
                        //this->debug("[DataPort::executeDestIPQuery] Destination UDP string=\"%s\"\n", vec[5].c_str());
                        destPort = boost::lexical_cast<unsigned int>(Pythonesque::Strip(vec[5]));
                        //this->debug("[DataPort::executeDestIPQuery] -- converted=%u\n", streamId);
                        ret = true;
                    }
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeDestIPCommand(int index,
                int dipIndex,
                std::string& ipAddr,
                std::string& macAddr,
                unsigned int& sourcePort,
                unsigned int& destPort)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "DIP " << index
                        << ", " << dipIndex
                        << ", " << ipAddr
                        << ", " << macAddr
                        << ", " << sourcePort
                        << ", " << destPort
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeErrorEnabledQuery(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TGBED? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TGBED ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Disabled indicator (1 = disabled, 0 = enabled)
                    int ind = boost::lexical_cast<int>(vec[1]);
                    enabled = (ind == 0);
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeErrorEnabledCommand(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TGBED " << index
                        << ", " << (enabled ? 0 : 1)
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeFlowControlEnabledQuery(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TGFC? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TGFC ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Enabled indicator (1 = enabled, 0 = disabled)
                    int ind = boost::lexical_cast<int>(vec[1]);
                    enabled = (ind == 1);
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 pattern
        bool DataPort::executeFlowControlEnabledCommand(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TGFC " << index
                        << ", " << (enabled ? 1 : 0)
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

