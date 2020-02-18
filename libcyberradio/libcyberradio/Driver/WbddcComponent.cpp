/***************************************************************************
 * \file WbddcComponent.cpp
 * \brief Defines the basic WBDDC interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Driver/WbddcComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {

        WbddcComponent::WbddcComponent(
                const std::string& name,
                int index,
                RadioHandler* parent,
                bool debug,
                bool tunable,
                bool selectableSource,
                bool selectableDataPort,
                bool agc,
                double freqRangeMin,
                double freqRangeMax,
                double freqRes,
                double freqUnits,
                int source,
                int dataPort,
                double frequency,
                int rateIndex,
                int udpDestination,
                int vitaEnable,
                unsigned int streamId) :
            RadioComponent(name, index, parent, debug),
            _tunable(tunable),
            _selectableSource(selectableSource),
            _selectableDataPort(selectableDataPort),
            _agc(agc),
            _freqRangeMin(freqRangeMin),
            _freqRangeMax(freqRangeMax),
            _freqRes(freqRes),
            _freqUnits(freqUnits),
            _source(source),
            _dataPort(dataPort),
            _frequency(frequency),
            _rateIndex(rateIndex),
            _udpDestination(udpDestination),
            _vitaEnable(vitaEnable),
            _streamId(streamId)
        {
            initConfigurationDict();
        }

        WbddcComponent::~WbddcComponent()
        {
        }

        WbddcComponent::WbddcComponent(const WbddcComponent& other) :
            RadioComponent(other),
            _tunable(other._tunable),
            _selectableSource(other._selectableSource),
            _selectableDataPort(other._selectableDataPort),
            _agc(other._agc),
            _freqRangeMin(other._freqRangeMin),
            _freqRangeMax(other._freqRangeMax),
            _freqRes(other._freqRes),
            _freqUnits(other._freqUnits),
            _source(other._source),
            _dataPort(other._dataPort),
            _frequency(other._frequency),
            _rateIndex(other._rateIndex),
            _udpDestination(other._udpDestination),
            _vitaEnable(other._vitaEnable),
            _streamId(other._streamId)
        {
        }

        WbddcComponent& WbddcComponent::operator=(const WbddcComponent& other)
        {
            RadioComponent::operator=(other);
            if ( this != &other )
            {
                _tunable = other._tunable;
                _selectableSource = other._selectableSource;
                _selectableDataPort = other._selectableDataPort;
                _agc = other._agc;
                _freqRangeMin = other._freqRangeMin;
                _freqRangeMax = other._freqRangeMax;
                _freqRes = other._freqRes;
                _freqUnits = other._freqUnits;
                _source = other._source;
                _dataPort = other._dataPort;
                _frequency = other._frequency;
                _rateIndex = other._rateIndex;
                _udpDestination = other._udpDestination;
                _vitaEnable = other._vitaEnable;
                _streamId = other._streamId;
            }
            return *this;
        }

        bool WbddcComponent::enable(bool enabled)
        {
            bool ret = false;
            if ( _config.hasKey("enable") )
            {
                int adjRateIndex = _rateIndex;
                int adjUdpDest = _udpDestination;
                int adjVita = _vitaEnable;
                unsigned int adjStream = _streamId;
                bool adjEnabled = enabled;
                ret = executeWbddcCommand(_index, adjRateIndex, adjUdpDest, adjEnabled, adjVita, adjStream);
                if ( ret )
                {
                    _enabled = adjEnabled;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        bool WbddcComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[WbddcComponent::setConfiguration] Called\n");
            // Call the "grandparent" version of this method instead of the
            // parent version. We want the normalization, but not the
            // automatic enabling.
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed via hardware calls.
            int adjRateIndex = _rateIndex;
            int adjUdpDest = _udpDestination;
            int adjVita = _vitaEnable;
            unsigned int adjStream = _streamId;
            bool adjEnabled = _enabled;
            double adjFreq = _frequency;
            int adjSource = _source;
            int adjDataPort = _dataPort;
            bool ddcCmdNeedsExecuting = false;
            bool freqCmdNeedsExecuting = false;
            bool srcCmdNeedsExecuting = false;
            bool dpCmdNeedsExecuting = false;
            if ( cfg.hasKey("enable") && _config.hasKey("enable") )
            {
                adjEnabled = getConfigurationValueAsBool("enable");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("rateIndex") && _config.hasKey("rateIndex") )
            {
                adjRateIndex = getConfigurationValueAsInt("rateIndex");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("udpDestination") && _config.hasKey("udpDestination") )
            {
                adjUdpDest = getConfigurationValueAsInt("udpDestination");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("vitaEnable") && _config.hasKey("vitaEnable") )
            {
                adjVita = getConfigurationValueAsInt("vitaEnable");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("streamId") && _config.hasKey("streamId") )
            {
                adjStream = getConfigurationValueAsUInt("streamId");
                ddcCmdNeedsExecuting = true;
            }
            if ( _tunable )
            {
                if ( cfg.hasKey("frequency") && _config.hasKey("frequency") )
                {
                    adjFreq = getConfigurationValueAsDbl("frequency");
                    freqCmdNeedsExecuting = true;
                }
            }
            if ( _selectableSource )
            {
                if ( cfg.hasKey("source") && _config.hasKey("source") )
                {
                    adjSource = getConfigurationValueAsInt("source");
                    srcCmdNeedsExecuting = true;
                }
            }
            if ( _selectableDataPort )
            {
                if ( cfg.hasKey("dataPort") && _config.hasKey("dataPort") )
                {
                    adjDataPort = getConfigurationValueAsInt("dataPort");
                    dpCmdNeedsExecuting = true;
                }
            }
            if ( ddcCmdNeedsExecuting )
            {
                ret &= executeWbddcCommand(_index, adjRateIndex, adjUdpDest,
                        adjEnabled, adjVita, adjStream);
            }
            if ( freqCmdNeedsExecuting )
            {
                ret &= executeFreqCommand(_index, adjFreq);
            }
            if ( srcCmdNeedsExecuting )
            {
                ret &= executeSourceCommand(_index, adjSource);
            }
            if ( dpCmdNeedsExecuting )
            {
                ret &= executeDataPortCommand(_index, adjDataPort);
            }
            if ( ret )
            {
                _rateIndex = adjRateIndex;
                _udpDestination = adjUdpDest;
                _vitaEnable = adjVita;
                _streamId = adjStream;
                _enabled = adjEnabled;
                _frequency = adjFreq;
                _source = adjSource;
                _dataPort = adjDataPort;
                updateConfigurationDict();
            }
            this->debug("[WbddcComponent::setConfiguration] Returning\n");
            return ret;
        }

        void WbddcComponent::queryConfiguration()
        {
            this->debug("[WbddcComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("enable") &&
                    _config.hasKey("rateIndex") &&
                    _config.hasKey("udpDestination") &&
                    _config.hasKey("vitaEnable") &&
                    _config.hasKey("streamId") )
            {
                executeWbddcQuery(_index, _rateIndex, _udpDestination, _enabled,
                        _vitaEnable, _streamId);
            }
            if ( _tunable && _config.hasKey("frequency") )
            {
                executeFreqQuery(_index, _frequency);
            }
            if ( _selectableSource && _config.hasKey("source") )
            {
                executeSourceQuery(_index, _source);
            }
            if ( _selectableDataPort && _config.hasKey("dataPort") )
            {
                executeDataPortQuery(_index, _dataPort);
            }
            updateConfigurationDict();
            this->debug("[WbddcComponent::queryConfiguration] Returning\n");
        }

        double WbddcComponent::getFrequency() const
        {
            return _frequency;
        }

        bool WbddcComponent::setFrequency(double freq)
        {
            bool ret = false;
            if ( _tunable && _config.hasKey("frequency") )
            {
                double adjFreq = _frequency;
                ret = executeFreqCommand(_index, adjFreq);
                if ( ret )
                {
                    _frequency = adjFreq;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        BasicDoubleList WbddcComponent::getFrequencyRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_freqRangeMin);
            ret.push_back(_freqRangeMax);
            return ret;
        }

        double WbddcComponent::getFrequencyRes() const
        {
            return _freqRes;
        }

        double WbddcComponent::getFrequencyUnit() const
        {
            return _freqUnits;
        }

        bool WbddcComponent::isAgcSupported() const
        {
            return _agc;
        }

        bool WbddcComponent::isTunable() const
        {
            return _tunable;
        }

        bool WbddcComponent::isSourceSelectable() const
        {
            return _selectableSource;
        }

        int WbddcComponent::getSource() const
        {
            return _source;
        }

        bool WbddcComponent::setSource(int source)
        {
            bool ret = false;
            if ( _selectableSource && _config.hasKey("source") )
            {
                int adjSource = _source;
                ret = executeSourceCommand(_index, adjSource);
                if ( ret )
                {
                    _source = adjSource;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int WbddcComponent::getRateIndex() const
        {
            return _rateIndex;
        }

        bool WbddcComponent::setRateIndex(int index)
        {
            bool ret = false;
            if ( _config.hasKey("rateIndex") )
            {
                int adjRateIndex = index;
                int adjUdpDest = _udpDestination;
                int adjVita = _vitaEnable;
                unsigned int adjStream = _streamId;
                bool adjEnabled = _enabled;
                ret = executeWbddcCommand(_index, adjRateIndex, adjUdpDest, adjEnabled, adjVita, adjStream);
                if ( ret )
                {
                    _rateIndex = adjRateIndex;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int WbddcComponent::getUdpDestination() const
        {
            return _udpDestination;
        }

        bool WbddcComponent::setUdpDestination(int dest)
        {
            bool ret = false;
            if ( _config.hasKey("udpDestination") )
            {
                int adjRateIndex = _rateIndex;
                int adjUdpDest = dest;
                int adjVita = _vitaEnable;
                unsigned int adjStream = _streamId;
                bool adjEnabled = _enabled;
                ret = executeWbddcCommand(_index, adjRateIndex, adjUdpDest, adjEnabled, adjVita, adjStream);
                if ( ret )
                {
                    _udpDestination = adjUdpDest;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int WbddcComponent::getVitaEnable() const
        {
            return _vitaEnable;
        }

        bool WbddcComponent::setVitaEnable(int enable)
        {
            bool ret = false;
            if ( _config.hasKey("vitaEnable") )
            {
                int adjRateIndex = _rateIndex;
                int adjUdpDest = _udpDestination;
                int adjVita = enable;
                unsigned int adjStream = _streamId;
                bool adjEnabled = _enabled;
                ret = executeWbddcCommand(_index, adjRateIndex, adjUdpDest, adjEnabled, adjVita, adjStream);
                if ( ret )
                {
                    _vitaEnable = adjVita;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        unsigned int WbddcComponent::getStreamId() const
        {
            return _streamId;
        }

        bool WbddcComponent::setStreamId(unsigned int sid)
        {
            bool ret = false;
            if ( _config.hasKey("streamId") )
            {
                int adjRateIndex = _rateIndex;
                int adjUdpDest = _udpDestination;
                int adjVita = _vitaEnable;
                unsigned int adjStream = sid;
                bool adjEnabled = _enabled;
                ret = executeWbddcCommand(_index, adjRateIndex, adjUdpDest, adjEnabled, adjVita, adjStream);
                if ( ret )
                {
                    _streamId = adjStream;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int WbddcComponent::getDataPort() const
        {
            return _dataPort;
        }

        bool WbddcComponent::setDataPort(int port)
        {
            bool ret = false;
            if ( _selectableDataPort && _config.hasKey("dataPort") )
            {
                int adjDataPort = port;
                ret = executeDataPortCommand(_index, adjDataPort);
                if ( ret )
                {
                    _dataPort = adjDataPort;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        WbddcRateSet WbddcComponent::getRateSet() const
        {
            return _rateSet;
        }

        bool WbddcComponent::setRateSet(const WbddcRateSet& set)
        {
            _rateSet = set;
            return true;
        }

        BasicDoubleList WbddcComponent::getRateList() const
        {
            BasicDoubleList ret;
            for (WbddcRateSet::const_iterator it = _rateSet.begin(); it != _rateSet.end(); it++)
            {
                ret.push_back(it->second);
            }
            return ret;
        }

        void WbddcComponent::initConfigurationDict()
        {
            //this->debug("[WbddcComponent::initConfigurationDict] Called\n");
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define tuner-specific keys
            _config["rateIndex"] = "";
            _config["udpDestination"] = "";
            _config["vitaEnable"] = "";
            _config["streamId"] = "";
            if ( _tunable )
            {
                _config["frequency"] = "";
            }
            if ( _selectableSource )
            {
                _config["source"] = "";
            }
            if ( _selectableDataPort )
            {
                _config["dataPort"] = "";
            }
            //this->debug("[WbddcComponent::initConfigurationDict] Returning\n");
        }

        void WbddcComponent::updateConfigurationDict()
        {
            this->debug("[WbddcComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("rateIndex") )
                setConfigurationValueToInt("rateIndex", _rateIndex);
            if ( _config.hasKey("udpDestination") )
                setConfigurationValueToInt("udpDestination", _udpDestination);
            if ( _config.hasKey("vitaEnable") )
                setConfigurationValueToInt("vitaEnable", _vitaEnable);
            if ( _config.hasKey("streamId") )
                setConfigurationValueToUInt("streamId", _streamId);
            if ( _tunable && _config.hasKey("frequency") )
            {
                setConfigurationValueToDbl("frequency", _frequency);
            }
            if ( _selectableSource && _config.hasKey("source") )
            {
                setConfigurationValueToInt("source", _source);
            }
            if ( _selectableDataPort && _config.hasKey("dataPort") )
            {
                setConfigurationValueToInt("dataPort", _dataPort);
            }
            this->debug("[WbddcComponent::updateConfigurationDict] Returning\n");
        }

        // Default implementation uses the NDR308 syntax.
        // WBDDC? <index>
        bool WbddcComponent::executeWbddcQuery(int index, int& rateIndex,
                int& udpDestination, bool& enabled, int& vitaEnable,
                unsigned int& streamId)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBDDC? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "WBDDC ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Rate index
                    rateIndex = boost::lexical_cast<int>(vec[1]);
                    udpDestination = boost::lexical_cast<int>(vec[2]);
                    enabled = (boost::lexical_cast<int>(vec[3]) == 1);
                    vitaEnable = boost::lexical_cast<int>(vec[4]);
                    streamId = boost::lexical_cast<unsigned int>(vec[5]);
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 syntax.
        // WBDDC <index>, <rate index>, <udp dest>, <enable>, <vita enable>, <stream id>
        bool WbddcComponent::executeWbddcCommand(int index, int& rateIndex,
                int& udpDestination, bool& enabled, int& vitaEnable,
                unsigned int& streamId)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBDDC " << index
                        << ", " << rateIndex
                        << ", " << udpDestination
                        << ", " << (enabled ? 1 : 0)
                        << ", " << vitaEnable
                        << ", " << streamId
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation returns false, since it is based on
        // the NDR308, which does not support tunable WBDDCs.
        bool WbddcComponent::executeFreqQuery(int index, double& freq)
        {
            return false;
        }

        // Default implementation returns false, since it is based on
        // the NDR308, which does not support tunable WBDDCs.
        bool WbddcComponent::executeFreqCommand(int index, double& freq)
        {
            return false;
        }

        // Default implementation returns false, since it is based on
        // the NDR308, which does not support selectable-source WBDDCs.
        bool WbddcComponent::executeSourceQuery(int index, int& source)
        {
            return false;
        }
        // Default implementation uses the NDR308 syntax.

        // Default implementation returns false, since it is based on
        // the NDR308, which does not support selectable-source WBDDCs.
        bool WbddcComponent::executeSourceCommand(int index, int& source)
        {
            return false;
        }

        // Default implementation uses the NDR308 syntax.
        // WBDP? <index>
        bool WbddcComponent::executeDataPortQuery(int index, int& dataPort)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBDP? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "WBDP ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Data Port
                    dataPort = boost::lexical_cast<int>(vec[1]);
                    ret = true;
                }
            }
            return ret;
        }

        // Default implementation uses the NDR308 syntax.
        // WBDP <index>, <data port>
        bool WbddcComponent::executeDataPortCommand(int index, int& dataPort)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBDP " << index
                        << ", " << dataPort
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

    } // namespace Driver

} // namespace LibCyberRadio

