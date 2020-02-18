/***************************************************************************
 * \file CWToneGenComponent.cpp
 * \brief Defines the basic continuous-wave (CW) tone generator interface
 *    for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/CWToneGenComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>
#include <string>


namespace LibCyberRadio
{

    namespace Driver
    {

        CWToneGenComponent::CWToneGenComponent(
            const std::string& name,
            int index,
            RadioHandler* parent,
            bool debug,
            int txIndex,
            double freqRangeMin,
            double freqRangeMax,
            double freqRes,
            double freqUnits,
            double ampRangeMin,
            double ampRangeMax,
            double ampRes,
            double phaseRangeMin,
            double phaseRangeMax,
            double phaseRes,
            double sweepStartRangeMin,
            double sweepStartRangeMax,
            double sweepStartRes,
            double sweepStopRangeMin,
            double sweepStopRangeMax,
            double sweepStopRes,
            double sweepStepRangeMin,
            double sweepStepRangeMax,
            double sweepStepRes,
            double dwellTimeRangeMin,
            double dwellTimeRangeMax,
            double dwellTimeRes,
            double frequency,
            double amplitude,
            double phase,
            double sweepStart,
            double sweepStop,
            double sweepStep,
            double dwellTime
        ) :
            RadioComponent(name, index, parent, debug),
            _txIndex(txIndex),
            _freqRangeMin(freqRangeMin),
            _freqRangeMax(freqRangeMax),
            _freqRes(freqRes),
            _freqUnits(freqUnits),
            _ampRangeMin(ampRangeMin),
            _ampRangeMax(ampRangeMax),
            _ampRes(ampRes),
            _phaseRangeMin(phaseRangeMin),
            _phaseRangeMax(phaseRangeMax),
            _phaseRes(phaseRes),
            _sweepStartRangeMin(sweepStartRangeMin),
            _sweepStartRangeMax(sweepStartRangeMax),
            _sweepStartRes(sweepStartRes),
            _sweepStopRangeMin(sweepStopRangeMin),
            _sweepStopRangeMax(sweepStopRangeMax),
            _sweepStopRes(sweepStopRes),
            _sweepStepRangeMin(sweepStepRangeMin),
            _sweepStepRangeMax(sweepStepRangeMax),
            _sweepStepRes(sweepStepRes),
            _dwellTimeRangeMin(dwellTimeRangeMin),
            _dwellTimeRangeMax(dwellTimeRangeMax),
            _dwellTimeRes(dwellTimeRes),
            _frequency(frequency),
            _amplitude(amplitude),
            _phase(phase),
            _sweepStart(sweepStart),
            _sweepStop(sweepStop),
            _sweepStep(sweepStep),
            _dwellTime(dwellTime)
        {
            // Call init function
            initConfigurationDict();
        }

        CWToneGenComponent::~CWToneGenComponent()
        {

        }

        CWToneGenComponent::CWToneGenComponent(const CWToneGenComponent& other) :
            RadioComponent(other),
            _txIndex(other._txIndex),
            _freqRangeMin(other._freqRangeMin),
            _freqRangeMax(other._freqRangeMax),
            _freqRes(other._freqRes),
            _freqUnits(other._freqUnits),
            _ampRangeMin(other._ampRangeMin),
            _ampRangeMax(other._ampRangeMax),
            _ampRes(other._ampRes),
            _phaseRangeMin(other._phaseRangeMin),
            _phaseRangeMax(other._phaseRangeMax),
            _phaseRes(other._phaseRes),
            _sweepStartRangeMin(other._sweepStartRangeMin),
            _sweepStartRangeMax(other._sweepStartRangeMax),
            _sweepStartRes(other._sweepStartRes),
            _sweepStopRangeMin(other._sweepStopRangeMin),
            _sweepStopRangeMax(other._sweepStopRangeMax),
            _sweepStopRes(other._sweepStopRes),
            _sweepStepRangeMin(other._sweepStepRangeMin),
            _sweepStepRangeMax(other._sweepStepRangeMax),
            _sweepStepRes(other._sweepStepRes),
            _dwellTimeRangeMin(other._dwellTimeRangeMin),
            _dwellTimeRangeMax(other._dwellTimeRangeMax),
            _dwellTimeRes(other._dwellTimeRes),
            _frequency(other._frequency),
            _amplitude(other._amplitude),
            _phase(other._phase),
            _sweepStart(other._sweepStart),
            _sweepStop(other._sweepStop),
            _sweepStep(other._sweepStep),
            _dwellTime(other._dwellTime)
        {

        }

        CWToneGenComponent& CWToneGenComponent::operator=(const CWToneGenComponent& other)
        {
            RadioComponent::operator=(other);
            if ( this != &other )
            {
                _txIndex = other._txIndex;
                _freqRangeMin = other._freqRangeMin;
                _freqRangeMax = other._freqRangeMax;
                _freqRes = other._freqRes;
                _freqUnits = other._freqUnits;
                _ampRangeMin = other._ampRangeMin;
                _ampRangeMax = other._ampRangeMax;
                _ampRes = other._ampRes;
                _phaseRangeMin = other._phaseRangeMin;
                _phaseRangeMax = other._phaseRangeMax;
                _phaseRes = other._phaseRes;
                _sweepStartRangeMin = other._sweepStartRangeMin;
                _sweepStartRangeMax = other._sweepStartRangeMax;
                _sweepStartRes = other._sweepStartRes;
                _sweepStopRangeMin = other._sweepStopRangeMin;
                _sweepStopRangeMax = other._sweepStopRangeMax;
                _sweepStopRes = other._sweepStopRes;
                _sweepStepRangeMin = other._sweepStepRangeMin;
                _sweepStepRangeMax = other._sweepStepRangeMax;
                _sweepStepRes = other._sweepStepRes;
                _dwellTimeRangeMin = other._dwellTimeRangeMin;
                _dwellTimeRangeMax = other._dwellTimeRangeMax;
                _dwellTimeRes = other._dwellTimeRes;
                _frequency = other._frequency;
                _amplitude = other._amplitude;
                _phase = other._phase;
                _sweepStart = other._sweepStart;
                _sweepStop = other._sweepStop;
                _sweepStep = other._sweepStep;
                _dwellTime = other._dwellTime;
            }
            return *this;
        }

        bool CWToneGenComponent::enable(bool enabled)
        {
            return setAmplitude(enabled ? _amplitude : 0);
        }

        bool CWToneGenComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[CWToneGenComponent::setConfiguration] Called\n");
            // Call the "grandparent" version of this method instead of the
            // parent version. We want the normalization, but not the
            // automatic enabling.
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed via hardware calls.
            double adjFrequency = _frequency;
            double adjAmplitude = _amplitude;
            double adjPhase = _phase;
            double adjStart = _sweepStart;
            double adjStop = _sweepStop;
            double adjStep = _sweepStep;
            double adjDwell = _dwellTime;
            bool adjEnabled = _enabled;
            bool toneCmdNeedsExecuting = false;
            bool sweepCmdNeedsExecuting = false;
            if ( cfg.hasKey("enable") && _config.hasKey("enable") )
            {
                adjEnabled = getConfigurationValueAsBool("enable");
                toneCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwFrequency") && _config.hasKey("cwFrequency") )
            {
                adjFrequency = getConfigurationValueAsDbl("cwFrequency");
                toneCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwAmplitude") && _config.hasKey("cwAmplitude") )
            {
                adjAmplitude = getConfigurationValueAsInt("cwAmplitude");
                toneCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwPhase") && _config.hasKey("cwPhase") )
            {
                adjPhase = getConfigurationValueAsInt("cwPhase");
                toneCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwSweepStart") && _config.hasKey("cwSweepStart") )
            {
                adjStart = getConfigurationValueAsDbl("cwSweepStart");
                sweepCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwSweepStop") && _config.hasKey("cwSweepStop") )
            {
                adjStop = getConfigurationValueAsDbl("cwSweepStop");
                sweepCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwSweepStep") && _config.hasKey("cwSweepStep") )
            {
                adjStep = getConfigurationValueAsDbl("cwSweepStep");
                sweepCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("cwSweepDwell") && _config.hasKey("cwSweepDwell") )
            {
                adjDwell = getConfigurationValueAsInt("cwSweepDwell");
                sweepCmdNeedsExecuting = true;
            }
            if ( toneCmdNeedsExecuting )
            {
                ret &= executeToneCommand(_index, _txIndex, adjFrequency, adjAmplitude,
                        adjPhase);
            }
            if ( sweepCmdNeedsExecuting )
            {
                ret &= executeSweepCommand(_index, _txIndex, adjStart, adjStop,
                        adjStep, adjDwell);
            }
            if ( ret )
            {
                _enabled = adjEnabled;
                _frequency = adjFrequency;
                _amplitude = adjAmplitude;
                _phase = adjPhase;
                _sweepStart = adjStart;
                _sweepStop = adjStop;
                _sweepStep = adjStep;
                _dwellTime = adjDwell;
                updateConfigurationDict();
            }
            this->debug("[CWToneGenComponent::setConfiguration] Returning\n");
            return ret;
        }

        void CWToneGenComponent::queryConfiguration()
        {
            this->debug("[CWToneGenComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("cwFrequency") &&
                    _config.hasKey("cwAmplitude") &&
                    _config.hasKey("cwPhase") )
            {
                executeToneQuery(_index, _txIndex, _frequency, _amplitude, _phase);
            }
            if ( _config.hasKey("cwSweepStart") &&
                    _config.hasKey("cwSweepStop") &&
                    _config.hasKey("cwSweepStep") &&
                    _config.hasKey("cwSweepDwell") )
            {
                executeSweepQuery(_index, _txIndex, _sweepStart, _sweepStop, _sweepStep,
                        _dwellTime);
            }
            _enabled = (_amplitude != 0);
            updateConfigurationDict();
            this->debug("[CWToneGenComponent::queryConfiguration] Returning\n");
        }

        BasicDoubleList CWToneGenComponent::getFrequencyRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_freqRangeMin);
            ret.push_back(_freqRangeMax);
            return ret;
        }

        double CWToneGenComponent::getFrequencyRes() const
        {
            return _freqRes;
        }

        BasicDoubleList CWToneGenComponent::getAmplitudeRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_ampRangeMin);
            ret.push_back(_ampRangeMax);
            return ret;
        }

        double CWToneGenComponent::getAmplitudeRes() const
        {
            return _ampRes;
        }

        BasicDoubleList CWToneGenComponent::getPhaseRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_phaseRangeMin);
            ret.push_back(_phaseRangeMax);
            return ret;
        }

        double CWToneGenComponent::getPhaseRes() const
        {
            return _phaseRes;
        }

        BasicDoubleList CWToneGenComponent::getSweepStartRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_sweepStartRangeMin);
            ret.push_back(_sweepStartRangeMax);
            return ret;
        }

        double CWToneGenComponent::getSweepStartRes() const
        {
            return _sweepStartRes;
        }

        BasicDoubleList CWToneGenComponent::getSweepStopRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_sweepStopRangeMin);
            ret.push_back(_sweepStopRangeMax);
            return ret;
        }

        double CWToneGenComponent::getSweepStopRes() const
        {
            return _sweepStopRes;
        }

        BasicDoubleList CWToneGenComponent::getSweepStepRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_sweepStepRangeMin);
            ret.push_back(_sweepStepRangeMax);
            return ret;
        }

        double CWToneGenComponent::getSweepStepRes() const
        {
            return _sweepStepRes;
        }

        BasicDoubleList CWToneGenComponent::getDwellTimeRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_dwellTimeRangeMin);
            ret.push_back(_dwellTimeRangeMax);
            return ret;
        }

        double CWToneGenComponent::getDwellTimeRes() const
        {
            return _dwellTimeRes;
        }

        double CWToneGenComponent::getFrequency() const
        {
            return _frequency;
        }

        bool CWToneGenComponent::setFrequency(double freq)
        {
            bool ret = false;
            if ( _config.hasKey("frequency") )
            {
                double adjFrequency = freq;
                double adjAmplitude = _amplitude;
                double adjPhase = _phase;
                ret = executeToneCommand(_index, _txIndex, adjFrequency, adjAmplitude, adjPhase);
                if ( ret )
                {
                    _frequency = adjFrequency;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        double CWToneGenComponent::getAmplitude() const
        {
            return _amplitude;
        }

        bool CWToneGenComponent::setAmplitude(double amp)
        {
            bool ret = false;
            if ( _config.hasKey("cwAmplitude") )
            {
                double adjFrequency = _frequency;
                double adjAmplitude = amp;
                double adjPhase = _phase;
                ret = executeToneCommand(_index, _txIndex, adjFrequency, adjAmplitude, adjPhase);
                if ( ret )
                {
                    _amplitude = adjAmplitude;
                    _enabled = (_amplitude != 0);
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        double CWToneGenComponent::getPhase() const
        {
            return _phase;
        }

        bool CWToneGenComponent::setPhase(double phase)
        {
            bool ret = false;
            if ( _config.hasKey("cwPhase") )
            {
                double adjFrequency = _frequency;
                double adjAmplitude = _amplitude;
                double adjPhase = phase;
                ret = executeToneCommand(_index, _txIndex, adjFrequency, adjAmplitude, adjPhase);
                if ( ret )
                {
                    _phase = adjPhase;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        bool CWToneGenComponent::supportsSweep() const
        {
            bool ret = ( _sweepStartRangeMin != _sweepStartRangeMax );
            return ret;
        }

        double CWToneGenComponent::getSweepStartFrequency() const
        {
            return _sweepStart;
        }

        double CWToneGenComponent::getSweepStopFrequency() const
        {
            return _sweepStop;
        }

        double CWToneGenComponent::getSweepFrequencyStep() const
        {
            return _sweepStep;
        }

        double CWToneGenComponent::getSweepDwellTime() const
        {
            return _dwellTime;
        }

        bool CWToneGenComponent::setFrequencySweep(double start, double stop,
                double step, double dwell)
        {
            bool ret = false;
            if ( _config.hasKey("cwSweepStart") &&
                    _config.hasKey("cwSweepStop") &&
                    _config.hasKey("cwSweepStep") &&
                    _config.hasKey("cwSweepDwell") )
            {
                double adjStart = start;
                double adjStop = stop;
                double adjStep = step;
                double adjDwell = dwell;
                ret = executeSweepCommand(_index, _txIndex, adjStart, adjStop, adjStep,
                        adjDwell);
                if ( ret )
                {
                    _sweepStart = adjStart;
                    _sweepStop = adjStop;
                    _sweepStep = adjStep;
                    _dwellTime = adjDwell;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        void CWToneGenComponent::initConfigurationDict()
        {
            //this->debug("[CWToneGenComponent::initConfigurationDict] Called\n");
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define tone generator-specific keys
            _config["cwFrequency"] = "0";
            _config["cwAmplitude"] = "0";
            _config["cwPhase"] = "0";
            _config["cwSweepStart"] = "0";
            _config["cwSweepStop"] = "0";
            _config["cwSweepStep"] = "0";
            _config["cwSweepDwell"] = "0";
            //this->debug("[CWToneGenComponent::initConfigurationDict] Returning\n");
        }

        void CWToneGenComponent::updateConfigurationDict()
        {
            this->debug("[CWToneGenComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("cwFrequency") )
                setConfigurationValueToDbl("cwFrequency", _frequency);
            if ( _config.hasKey("cwAmplitude") )
                setConfigurationValueToDbl("cwAmplitude", _amplitude);
            if ( _config.hasKey("cwPhase") )
                setConfigurationValueToDbl("cwPhase", _phase);
            if ( _config.hasKey("cwSweepStart") )
                setConfigurationValueToDbl("cwSweepStart", _sweepStart);
            if ( _config.hasKey("cwSweepStop") )
                setConfigurationValueToDbl("cwSweepStop", _sweepStop);
            if ( _config.hasKey("cwSweepStep") )
                setConfigurationValueToDbl("cwSweepStep", _sweepStep);
            if ( _config.hasKey("cwSweepDwell") )
                setConfigurationValueToDbl("cwSweepDwell", _dwellTime);
            this->debug("[CWToneGenComponent::updateConfigurationDict] Returning\n");
        }

        // CW tone query uses the NDR651 implementation as the base
        bool CWToneGenComponent::executeToneQuery(int index,
                int txIndex,
                double& freq,
                double& amp,
                double& phase)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "CWT? " << txIndex << ", " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "CWT ", ""),
                            ", ");
                    // vec[0] = TX Index
                    // vec[1] = CWTG Index
                    // vec[2] = Frequency (Hz)
                    freq = boost::lexical_cast<double>(vec[2]);
                    // vec[3] = Amplitude
                    amp = boost::lexical_cast<double>(vec[3]);
                    // vec[4] = Phase (deg)
                    phase = boost::lexical_cast<double>(vec[4]);
                    ret = true;
                }
            }
            return ret;
        }

        // CW tone command uses the NDR651 implementation as the base
        bool CWToneGenComponent::executeToneCommand(int index,
                int txIndex,
                double& freq,
                double& amp,
                double& phase)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "CWT " << txIndex
                        << ", " << index
                        << ", " << std::setprecision(1) << std::fixed << freq
                        << ", " << std::setprecision(1) << std::fixed << amp
                        << ", " << std::setprecision(1) << std::fixed << phase
                        << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            return ret;
        }

        // CW sweep query uses the NDR651 implementation as the base
        bool CWToneGenComponent::executeSweepQuery(int index,
                int txIndex,
                double& sweepStart,
                double& sweepStop,
                double& sweepStep,
                double& dwellTime)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "CWS? " << txIndex << ", " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "CWS ", ""),
                            ", ");
                    // vec[0] = TX Index
                    // vec[1] = CWTG Index
                    // vec[2] = Start frequency (Hz)
                    sweepStart = boost::lexical_cast<double>(vec[2]);
                    // vec[3] = Stop frequency (Hz)
                    sweepStop = boost::lexical_cast<double>(vec[3]);
                    // vec[4] = Frequency step (Hz)
                    sweepStep = boost::lexical_cast<double>(vec[4]);
                    // vec[5] = Dwell time (sample clocks)
                    dwellTime = boost::lexical_cast<double>(vec[5]);
                    ret = true;
                }
            }
            return ret;
        }

        // CW sweep command uses the NDR651 implementation as the base
        bool CWToneGenComponent::executeSweepCommand(int index,
                int txIndex,
                double& sweepStart,
                double& sweepStop,
                double& sweepStep,
                double& dwellTime)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "CWS " << txIndex
                        << ", " << index
                        << ", " << std::setprecision(1) << std::fixed << sweepStart
                        << ", " << std::setprecision(1) << std::fixed << sweepStop
                        << ", " << std::setprecision(1) << std::fixed << sweepStep
                        << ", " << std::setprecision(1) << std::fixed << dwellTime
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





