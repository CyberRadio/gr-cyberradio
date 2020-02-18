/***************************************************************************
 * \file TransmitterComponent.cpp
 * \brief Defines the basic transmitter interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/TransmitterComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {

        TransmitterComponent::TransmitterComponent(
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
                int numToneGen,
                int toneGenIndexBase,
                double frequency,
                double attenuation) :
            RadioComponent(name, index, parent, debug),
            _freqRangeMin(freqRangeMin),
            _freqRangeMax(freqRangeMax),
            _freqRes(freqRes),
            _freqUnits(freqUnits),
            _attRangeMin(attRangeMin),
            _attRangeMax(attRangeMax),
            _attRes(attRes),
            _numToneGen(numToneGen),
            _toneGenIndexBase(toneGenIndexBase),
            _frequency(frequency),
            _attenuation(attenuation)
        {
            // Call init function
            initConfigurationDict();
        }

        TransmitterComponent::~TransmitterComponent()
        {
            for ( CWToneGenComponentDict::iterator it = _cwToneGens.begin();
                    it != _cwToneGens.end(); it++)
            {
                delete it->second;
            }
        }

        TransmitterComponent::TransmitterComponent(const TransmitterComponent& other) :
            RadioComponent(other),
            _freqRangeMin(other._freqRangeMin),
            _freqRangeMax(other._freqRangeMax),
            _freqRes(other._freqRes),
            _freqUnits(other._freqUnits),
            _attRangeMin(other._attRangeMin),
            _attRangeMax(other._attRangeMax),
            _attRes(other._attRes),
            _numToneGen(other._numToneGen),
            _toneGenIndexBase(other._toneGenIndexBase),
            _frequency(other._frequency),
            _attenuation(other._attenuation)
        {
        }

        TransmitterComponent& TransmitterComponent::operator=(const TransmitterComponent& other)
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
                _numToneGen = other._numToneGen;
                _toneGenIndexBase = other._toneGenIndexBase;
                _frequency = other._frequency;
                _attenuation = other._attenuation;
            }
            return *this;
        }

        bool TransmitterComponent::enable(bool enabled)
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

        bool TransmitterComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[TransmitterComponent::setConfiguration] Called\n");
            // Call the base-class version to modify the configuration dictionary
            // (this including any enabling/disabling)
            bool ret = RadioComponent::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed via hardware calls.
            if ( cfg.hasKey("frequency") && _config.hasKey("frequency") )
            {
                try
                {
                    double inFreq = boost::lexical_cast<double>( cfg["frequency"] );
                    //this->debug("[setConfiguration] -- set freq = %0.1f\n", inFreq);
                    ret &= setFrequency( inFreq );
                }
                catch(std::exception& ex)
                {
                }
            }
            else
            {
                //this->debug("[setConfiguration] -- CAN'T set freq = not in incoming\n");
            }
            if ( cfg.hasKey("attenuation") && _config.hasKey("attenuation") )
            {
                try
                {
                    double inAtten = boost::lexical_cast<double>( cfg["attenuation"] );
                    //this->debug("[setConfiguration] -- set atten = %0.1f\n", inAtten);
                    ret &= setAttenuation( inAtten );
                }
                catch(std::exception& ex)
                {
                }
            }
            else
            {
                //this->debug("[setConfiguration] -- CAN'T set atten = not in incoming\n");
            }
            this->debug("[TransmitterComponent::setConfiguration] Returning %s\n", debugBool(ret));
            return ret;
        }

        void TransmitterComponent::queryConfiguration()
        {
            this->debug("[TransmitterComponent::queryConfiguration] Called\n");
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
            updateConfigurationDict();
            // Query configuration of CW tone generators
            for ( CWToneGenComponentDict::iterator it = _cwToneGens.begin();
                    it != _cwToneGens.end(); it++)
            {
                it->second->queryConfiguration();
            }
            this->debug("[TransmitterComponent::queryConfiguration] Returning\n");
        }

        double TransmitterComponent::getFrequency() const
        {
            return _frequency;
        }

        bool TransmitterComponent::setFrequency(double freq)
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

        double TransmitterComponent::getAttenuation() const
        {
            return _attenuation;
        }

        bool TransmitterComponent::setAttenuation(double atten)
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

        BasicDoubleList TransmitterComponent::getFrequencyRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_freqRangeMin);
            ret.push_back(_freqRangeMax);
            return ret;
        }

        double TransmitterComponent::getFrequencyRes() const
        {
            return _freqRes;
        }

        double TransmitterComponent::getFrequencyUnit() const
        {
            return _freqUnits;
        }

        BasicDoubleList TransmitterComponent::getAttenuationRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_attRangeMin);
            ret.push_back(_attRangeMax);
            return ret;
        }

        double TransmitterComponent::getAttenuationRes() const
        {
            return _attRes;
        }

        bool TransmitterComponent::supportsCW() const
        {
            return ( _numToneGen > 0 );
        }

        int TransmitterComponent::getCWNum() const
        {
            return _numToneGen;
        }

        BasicIntList TransmitterComponent::getCWIndexRange() const
        {
            BasicIntList ret;
            for (int num = _toneGenIndexBase; num < _toneGenIndexBase + _numToneGen;
                    num++)
                ret.push_back(num);
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWFrequencyRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double TransmitterComponent::getCWFrequencyRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWAmplitudeRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getAmplitudeRange();
            return ret;
        }

        double TransmitterComponent::getCWAmplitudeRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getAmplitudeRes();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWPhaseRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getPhaseRange();
            return ret;
        }

        double TransmitterComponent::getCWPhaseRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getPhaseRes();
            return ret;
        }

        bool TransmitterComponent::supportsCWSweep() const
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->supportsSweep();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWSweepStartRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStartRange();
            return ret;
        }

        double TransmitterComponent::getCWSweepStartRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStartRes();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWSweepStopRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStopRange();
            return ret;
        }

        double TransmitterComponent::getCWSweepStopRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStopRes();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWSweepStepRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStepRange();
            return ret;
        }

        double TransmitterComponent::getCWSweepStepRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStepRes();
            return ret;
        }

        BasicDoubleList TransmitterComponent::getCWSweepDwellRange() const
        {
            BasicDoubleList ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getDwellTimeRange();
            return ret;
        }

        double TransmitterComponent::getCWSweepDwellRes() const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getDwellTimeRes();
            return ret;
        }

        bool TransmitterComponent::enableCW(int index, bool enabled)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool TransmitterComponent::disableCW(int index)
        {
            return enableCW(index, false);
        }

        ConfigurationDict TransmitterComponent::getCWConfiguration(int index) const
        {
            ConfigurationDict ret;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool TransmitterComponent::setCWConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        double TransmitterComponent::getCWFrequency(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool TransmitterComponent::setCWFrequency(int index, double freq)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        double TransmitterComponent::getCWAmplitude(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getAmplitude();
            return ret;
        }

        bool TransmitterComponent::setCWAmplitude(int index, double amp)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->setAmplitude(amp);
            return ret;
        }

        double TransmitterComponent::getCWPhase(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getPhase();
            return ret;
        }

        bool TransmitterComponent::setCWPhase(int index, double phase)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->setPhase(phase);
            return ret;
        }

        bool TransmitterComponent::supportsCWSweep(int index) const
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->supportsSweep();
            return ret;
        }

        double TransmitterComponent::getCWSweepStartFrequency(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStartFrequency();
            return ret;
        }

        double TransmitterComponent::getCWSweepStopFrequency(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepStopFrequency();
            return ret;
        }

        double TransmitterComponent::getCWSweepFrequencyStep(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepFrequencyStep();
            return ret;
        }

        double TransmitterComponent::getCWSweepDwellTime(int index) const
        {
            double ret = 0.0;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->getSweepDwellTime();
            return ret;
        }

        bool TransmitterComponent::setCWFrequencySweep(int index, double start,
                double stop, double step,
                double dwell)
        {
            bool ret = false;
            CWToneGenComponentDict::const_iterator it = _cwToneGens.begin();
            if ( it != _cwToneGens.end() )
                ret = it->second->setFrequencySweep(start, stop, step, dwell);
            return ret;
        }

        void TransmitterComponent::initConfigurationDict()
        {
            //this->debug("[TransmitterComponent::initConfigurationDict] Called\n");
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define tuner-specific keys
            _config["frequency"] = "";
            _config["attenuation"] = "";
            //this->debug("[TransmitterComponent::initConfigurationDict] Returning\n");
        }

        void TransmitterComponent::updateConfigurationDict()
        {
            this->debug("[TransmitterComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("frequency") )
            {
                setConfigurationValueToDbl("frequency", _frequency);
            }
            if ( _config.hasKey("attenuation") )
            {
                setConfigurationValueToDbl("attenuation", _attenuation);
            }
            this->debug("[TransmitterComponent::updateConfigurationDict] Returning\n");
        }

        // Enable query uses the NDR651 implementation as the base
        bool TransmitterComponent::executeEnableQuery(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXP? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TXP ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Powered state (0=off, 1=on)
                    enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                    ret = true;
                }
            }
            return ret;

        }

        // Frequency query uses the NDR651 implementation as the base
        bool TransmitterComponent::executeFreqQuery(int index, double& freq)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXF? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TXF ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Frequency (MHz) [FLOATING POINT]
                    freq = boost::lexical_cast<double>(vec[1]) * _freqUnits;
                    ret = true;
                }
            }
            return ret;
        }

        // Attenuation query uses the NDR651 implementation as the base
        bool TransmitterComponent::executeAttenQuery(int index, double& atten)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXA? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TXA ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Atten (dB)
                    atten = boost::lexical_cast<double>(vec[1]);
                    ret = true;
                }
            }
            return ret;
        }

        // Enable command uses the NDR651 implementation as the base
        bool TransmitterComponent::executeEnableCommand(int index, bool& enabled)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXP " << index
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

        // Frequency command uses the NDR651 implementation as the base
        bool TransmitterComponent::executeFreqCommand(int index, double& freq)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXF " << index
                        << ", " << std::setprecision(6) << std::fixed << (freq / _freqUnits)
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    freq = (freq / _freqUnits);
                    ret = true;
                }
            }
            return ret;
        }

        // Attenuation command uses the NDR651 implementation as the base
        bool TransmitterComponent::executeAttenCommand(int index, double& atten)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "TXA " << index
                        << ", " << std::setprecision(1) << std::fixed << atten
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

