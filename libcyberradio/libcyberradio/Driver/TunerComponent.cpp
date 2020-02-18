/***************************************************************************
 * \file TunerComponent.cpp
 * \brief Defines the basic tuner interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/TunerComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {

        TunerComponent::TunerComponent(
                const std::string& name,
                int index,
                RadioHandler* parent,
                bool debug,
                double freqRangeMin,
                double freqRangeMax,
                double freqRes,
                double freqUnits,
                double attRangeMin,
                double attRangeMax,
                double attRes,
                bool agc,
                double frequency,
                double attenuation,
                int filter) :
            RadioComponent(name, index, parent, debug),
            _freqRangeMin(freqRangeMin),
            _freqRangeMax(freqRangeMax),
            _freqRes(freqRes),
            _freqUnits(freqUnits),
            _attRangeMin(attRangeMin),
            _attRangeMax(attRangeMax),
            _attRes(attRes),
            _agc(agc),
            _frequency(frequency),
            _attenuation(attenuation),
            _filter(filter),
            _timingAdj(0)
        {
            // Call init function
            initConfigurationDict();
        }

        TunerComponent::~TunerComponent()
        {
        }

        TunerComponent::TunerComponent(const TunerComponent& other) :
            RadioComponent(other),
            _freqRangeMin(other._freqRangeMin),
            _freqRangeMax(other._freqRangeMax),
            _freqRes(other._freqRes),
            _freqUnits(other._freqUnits),
            _attRangeMin(other._attRangeMin),
            _attRangeMax(other._attRangeMax),
            _attRes(other._attRes),
            _agc(other._agc),
            _frequency(other._frequency),
            _attenuation(other._attenuation),
            _filter(other._filter),
            _timingAdj(other._timingAdj)
        {
        }

        TunerComponent& TunerComponent::operator=(const TunerComponent& other)
        {
            RadioComponent::operator=(other);
            if ( this != &other )
            {
                _freqRangeMin = other._freqRangeMin;
                _freqRangeMax = other._freqRangeMax;
                _freqRes = other._freqRes;
                _freqUnits = other._freqUnits;
                _attRangeMin = other._attRangeMin;
                _attRangeMax = other._attRangeMax;
                _attRes = other._attRes;
                _agc = other._agc;
                _frequency = other._frequency;
                _attenuation = other._attenuation;
                _filter = other._filter;
                _timingAdj = other._timingAdj;
            }
            return *this;
        }

        bool TunerComponent::enable(bool enabled)
        {
            bool adjEnabled = enabled;
            bool ret = false;
            if ( _config.hasKey("enable") )
            {
                ret = executeEnableCommand(_index, adjEnabled);
                if ( ret )
                {
                    // If the hardware call succeeds, call the base class version
                    RadioComponent::enable(adjEnabled);
                }
            }
            return ret;
        }

        bool TunerComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[TunerComponent::setConfiguration] Called\n");
            // Call the base-class version to modify the configuration dictionary
            // (this including any enabling/disabling)
            bool ret = RadioComponent::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed via hardware calls.
            double adjFrequency = _frequency;
            double adjAttenuation = _attenuation;
            int adjFilter = _filter;
            int adjAdj = _timingAdj;
            bool freqCmdNeedsExecuting = false;
            bool attCmdNeedsExecuting = false;
            bool filCmdNeedsExecuting = false;
            bool adjCmdNeedsExecuting = false;
            if ( cfg.hasKey("frequency") && _config.hasKey("frequency") )
            {
                adjFrequency = getConfigurationValueAsDbl("frequency");
                freqCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("attenuation") && _config.hasKey("attenuation") )
            {
                adjAttenuation = getConfigurationValueAsDbl("attenuation");
                attCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("filter") && _config.hasKey("filter") )
            {
                adjFilter = getConfigurationValueAsInt("filter");
                filCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("timingAdj") && _config.hasKey("timingAdj") )
            {
                adjAdj = getConfigurationValueAsInt("timingAdj");
                adjCmdNeedsExecuting = true;
            }
            if ( freqCmdNeedsExecuting )
            {
                ret &= executeFreqCommand(_index, adjFrequency);
            }
            if ( attCmdNeedsExecuting )
            {
                ret &= executeAttenCommand(_index, adjAttenuation);
            }
            if ( filCmdNeedsExecuting )
            {
                ret &= executeFilterCommand(_index, adjFilter);
            }
            if ( adjCmdNeedsExecuting )
            {
                ret &= executeTimingAdjustmentCommand(_index, adjAdj);
            }
            this->debug("[TunerComponent::setConfiguration] Returning %s\n", debugBool(ret));
            return ret;
        }

        void TunerComponent::queryConfiguration()
        {
            this->debug("[TunerComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("enable") )
            {
                executeEnableQuery(_index, _enabled);
            }
            if ( _config.hasKey("frequency") )
            {
                executeFreqQuery(_index, _frequency);
            }
            if ( _config.hasKey("attenuation") )
            {
                executeAttenQuery(_index, _attenuation);
            }
            if ( _config.hasKey("filter") )
            {
                executeFilterQuery(_index, _filter);
            }
            if ( _config.hasKey("timingAdj") )
            {
                executeTimingAdjustmentQuery(_index, _timingAdj);
            }
            updateConfigurationDict();
            this->debug("[TunerComponent::queryConfiguration] Returning\n");
        }

        double TunerComponent::getFrequency() const
        {
            return _frequency;
        }

        bool TunerComponent::setFrequency(double freq)
        {
            double adjFreq = freq;
            bool ret = false;
            if ( _config.hasKey("frequency") )
            {
                ret = executeFreqCommand(_index, adjFreq);
                if ( ret )
                {
                    _frequency = adjFreq;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        double TunerComponent::getAttenuation() const
        {
            return _attenuation;
        }

        bool TunerComponent::setAttenuation(double atten)
        {
            double adjAtten = atten;
            bool ret = false;
            if ( _config.hasKey("attenuation") )
            {
                ret = executeAttenCommand(_index, adjAtten);
                if ( ret )
                {
                    _attenuation = adjAtten;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int TunerComponent::getFilter() const
        {
            return _filter;
        }

        bool TunerComponent::setFilter(int filter)
        {
            int adjFilter = filter;
            bool ret = false;
            if ( _config.hasKey("filter") )
            {
                ret = executeFilterCommand(_index, adjFilter);
                if ( ret )
                {
                    _filter = adjFilter;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int TunerComponent::getTimingAdjustment() const
        {
            return _timingAdj;
        }

        bool TunerComponent::setTimingAdjustment(int timingAdj)
        {
            int adjAdj = timingAdj;
            bool ret = false;
            if ( _config.hasKey("timingAdj") )
            {
                ret = executeTimingAdjustmentCommand(_index, adjAdj);
                if ( ret )
                {
                    _timingAdj = adjAdj;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        BasicDoubleList TunerComponent::getFrequencyRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_freqRangeMin);
            ret.push_back(_freqRangeMax);
            return ret;
        }

        double TunerComponent::getFrequencyRes() const
        {
            return _freqRes;
        }

        double TunerComponent::getFrequencyUnit() const
        {
            return _freqUnits;
        }

        BasicDoubleList TunerComponent::getAttenuationRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_attRangeMin);
            ret.push_back(_attRangeMax);
            return ret;
        }

        double TunerComponent::getAttenuationRes() const
        {
            return _attRes;
        }

        bool TunerComponent::isAgcSupported() const
        {
            return _agc;
        }

        bool TunerComponent::setFrequencyRangeMax(double freq)
        {
            _freqRangeMax = freq;
            return true;
        }

        void TunerComponent::initConfigurationDict()
        {
            //this->debug("[TunerComponent::initConfigurationDict] Called\n");
            _config.clear();
            _config["enable"] = "";
            _config["frequency"] = "";
            _config["attenuation"] = "";
            _config["filter"] = "";
            _config["timingAdj"] = "";
            //this->debug("[TunerComponent::initConfigurationDict] Returning\n");
        }

        void TunerComponent::updateConfigurationDict()
        {
            this->debug("[TunerComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            bool res;
            if ( _config.hasKey("frequency") )
            {
                res = setConfigurationValueToDbl("frequency", _frequency);
            }
            if ( _config.hasKey("attenuation") )
            {
                res = setConfigurationValueToDbl("attenuation", _attenuation);
            }
            if ( _config.hasKey("filter") )
            {
                res = setConfigurationValueToInt("filter", _filter);
            }
            if ( _config.hasKey("timingAdj") )
            {
                res = setConfigurationValueToInt("timingAdj", _timingAdj);
            }
            //this->debug("[TunerComponent::updateConfigurationDict] Current configuration\n");
            //this->dumpConfiguration();
            this->debug("[TunerComponent::updateConfigurationDict] Returning\n");
        }

        bool TunerComponent::executeEnableQuery(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TPWR? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TPWR ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Powered state (0=off, 1=on)
                    enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                    ret = true;
                }
            }
            return ret;

        }

        // Frequency query uses the NDR308 implementation as the base
        bool TunerComponent::executeFreqQuery(int index, double& freq)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "FRQ? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "FRQ ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Frequency (MHz)
                    freq = boost::lexical_cast<int>(vec[1]) * _freqUnits;
                    ret = true;
                }
            }
            return ret;
        }

        // Attenuation query uses the NDR308 implementation as the base
        bool TunerComponent::executeAttenQuery(int index, double& atten)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "ATT? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "ATT ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Atten (dB)
                    atten = boost::lexical_cast<double>(vec[1]);
                    ret = true;
                }
            }
            return ret;
        }

        // Filter query uses the NDR308 implementation as the base
        bool TunerComponent::executeFilterQuery(int index, int& filter)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "FIF? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "FIF ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Filter index
                    filter = boost::lexical_cast<int>(vec[1]);
                    ret = true;
                }
            }
            return ret;
        }

        bool TunerComponent::executeTimingAdjustmentQuery(int index, int& timingAdj)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TADJ? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TADJ ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Timing adjustment
                    timingAdj = boost::lexical_cast<int>(vec[1]);
                    ret = true;
                }
            }
            return ret;
        }

        bool TunerComponent::executeEnableCommand(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TPWR " << index
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

        // Frequency command uses the NDR308 implementation as the base
        bool TunerComponent::executeFreqCommand(int index, double& freq)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "FRQ " << index
                        << ", " << boost::lexical_cast<int>(freq / _freqUnits)
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    freq = (int)(freq / _freqUnits) * _freqUnits;
                    ret = true;
                }
            }
            return ret;
        }

        // Attenuation command uses the NDR308 implementation as the base
        bool TunerComponent::executeAttenCommand(int index, double& atten)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "ATT " << index
                        << ", " << atten
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    atten = (double)((int)atten);
                    ret = true;
                }
            }
            return ret;
        }

        // Filter command uses the NDR308 implementation as the base
        bool TunerComponent::executeFilterCommand(int index, int& filter)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "FIF " << index
                        << ", " << filter
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        bool TunerComponent::executeTimingAdjustmentCommand(int index, int& timingAdj)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TADJ " << index
                        << ", " << timingAdj
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

