/***************************************************************************
 * \file DucComponent.cpp
 * \brief Defines the basic DUC interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Driver/DucComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {

        DucComponent::DucComponent(
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
                int dataPort,
                double frequency,
                double attenuation,
                int rateIndex,
                int txChannels,
                int mode,
                unsigned int streamId) :
            RadioComponent(name, index, parent, debug),
            _freqRangeMin(freqRangeMin),
            _freqRangeMax(freqRangeMax),
            _freqRes(freqRes),
            _freqUnits(freqUnits),
            _attRangeMin(attRangeMin),
            _attRangeMax(attRangeMax),
            _attRes(attRes),
            _dataPort(dataPort),
            _frequency(frequency),
            _attenuation(attenuation),
            _rateIndex(rateIndex),
            _txChannels(txChannels),
            _mode(mode),
            _streamId(streamId),
            _supportsSnapLoad(false),
            _snapFilename(""),
            _snapStartSample(0),
            _snapSamples(0),
            _supportsSnapTransmit(false),
            _snapSinglePlayback(false),
            _snapPauseUntilEnabled(false)
        {
            // Call init function
            initConfigurationDict();
        }

        DucComponent::~DucComponent()
        {
        }

        DucComponent::DucComponent(const DucComponent& other) :
            RadioComponent(other),
            _freqRangeMin(other._freqRangeMin),
            _freqRangeMax(other._freqRangeMax),
            _freqRes(other._freqRes),
            _freqUnits(other._freqUnits),
            _attRangeMin(other._attRangeMin),
            _attRangeMax(other._attRangeMax),
            _attRes(other._attRes),
            _dataPort(other._dataPort),
            _frequency(other._frequency),
            _attenuation(other._attenuation),
            _rateIndex(other._rateIndex),
            _txChannels(other._txChannels),
            _mode(other._mode),
            _streamId(other._streamId),
            _supportsSnapLoad(other._supportsSnapLoad),
            _snapFilename(other._snapFilename),
            _snapStartSample(other._snapStartSample),
            _snapSamples(other._snapSamples),
            _supportsSnapTransmit(other._supportsSnapTransmit),
            _snapSinglePlayback(other._snapSinglePlayback),
            _snapPauseUntilEnabled(other._snapPauseUntilEnabled)
        {
        }

        DucComponent& DucComponent::operator=(const DucComponent& other)
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
                _dataPort = other._dataPort;
                _frequency = other._frequency;
                _attenuation = other._attenuation;
                _rateIndex = other._rateIndex;
                _txChannels = other._txChannels;
                _mode = other._mode;
                _streamId = other._streamId;
                _supportsSnapLoad = other._supportsSnapLoad;
                _snapFilename = other._snapFilename;
                _snapStartSample = other._snapStartSample;
                _snapSamples = other._snapSamples;
                _supportsSnapTransmit = other._supportsSnapTransmit;
                _snapSinglePlayback = other._snapSinglePlayback;
                _snapPauseUntilEnabled = other._snapPauseUntilEnabled;
            }
            return *this;
        }

        bool DucComponent::enable(bool enabled)
        {
            return false;
        }

        bool DucComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[DucComponent::setConfiguration] Called\n");
            // Call the "grandparent" version of this method instead of the
            // parent version. We want the normalization, but not the
            // automatic enabling.
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed via hardware calls.
            int adjDataPort = _dataPort;
            double adjFrequency = _frequency;
            double adjAttenuation = _attenuation;
            int adjRateIndex = _rateIndex;
            int adjTxChannels = _txChannels;
            int adjMode = _mode;
            unsigned int adjStreamId = _streamId;
            bool ddcCmdNeedsExecuting = false;
            bool snapLoadCmdNeedsExecuting = false;
            bool snapTxCmdNeedsExecuting = false;
            if ( cfg.hasKey("frequency") && _config.hasKey("frequency") )
            {
                adjFrequency = getConfigurationValueAsDbl("frequency");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("attenuation") && _config.hasKey("attenuation") )
            {
                adjAttenuation = getConfigurationValueAsDbl("attenuation");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("dataPort") && _config.hasKey("dataPort") )
            {
                adjDataPort = getConfigurationValueAsInt("dataPort");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("rateIndex") && _config.hasKey("rateIndex") )
            {
                adjRateIndex = getConfigurationValueAsInt("rateIndex");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("txChannels") && _config.hasKey("txChannels") )
            {
                adjTxChannels = getConfigurationValueAsInt("txChannels");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("mode") && _config.hasKey("mode") )
            {
                adjMode = getConfigurationValueAsInt("mode");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("streamId") && _config.hasKey("streamId") )
            {
                adjStreamId = getConfigurationValueAsUInt("streamId");
                ddcCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("filename") && _config.hasKey("filename") )
            {
                snapLoadCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("singlePlayback") && _config.hasKey("singlePlayback") )
            {
                snapTxCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("pauseUntilEnabled") && _config.hasKey("pauseUntilEnabled") )
            {
                snapTxCmdNeedsExecuting = true;
            }
            if ( ddcCmdNeedsExecuting )
            {
                ret &= executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
            }
            if ( snapLoadCmdNeedsExecuting )
            {
                ret &= executeSnapshotLoadCommand(_index, _snapFilename, _snapStartSample,
                        _snapSamples);
            }
            if ( snapTxCmdNeedsExecuting )
            {
                //ret &= executeSnapshotTxCommand(_index, _snapStartSample,
                //                   _snapSamples, _snapSinglePlayback,
                //                   _snapPauseUntilEnabled);
            }
            if ( ret )
            {
                _dataPort = adjDataPort;
                _frequency = adjFrequency;
                _attenuation = adjAttenuation;
                _rateIndex = adjRateIndex;
                _txChannels = adjTxChannels;
                _mode = adjMode;
                _streamId = adjStreamId;
                updateConfigurationDict();
            }
            this->debug("[DucComponent::setConfiguration] Returning\n");
        }

        void DucComponent::queryConfiguration()
        {
            this->debug("[DucComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("frequency") &&
                    _config.hasKey("attenuation") &&
                    _config.hasKey("dataPort") &&
                    _config.hasKey("rateIndex") &&
                    _config.hasKey("txChannels") &&
                    _config.hasKey("mode") &&
                    _config.hasKey("streamId") &&
                    _config.hasKey("filename") &&
                    _config.hasKey("singlePlayback") &&
                    _config.hasKey("pauseUntilEnabled") )
            {
                executeDucQuery(_index, _dataPort, _frequency, _attenuation,
                        _rateIndex, _txChannels, _mode, _streamId);
            }
            updateConfigurationDict();
            this->debug("[DucComponent::queryConfiguration] Returning\n");
        }

        int DucComponent::getDataPort() const
        {
            return _dataPort;
        }

        bool DucComponent::setDataPort(int port)
        {
            bool ret = false;
            if ( _config.hasKey("dataPort") )
            {
                int adjDataPort = port;
                double adjFrequency = _frequency;
                double adjAttenuation = _attenuation;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = _txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = _streamId;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _dataPort = adjDataPort;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        double DucComponent::getFrequency() const
        {
            return _frequency;
        }

        bool DucComponent::setFrequency(double freq)
        {
            bool ret = false;
            if ( _config.hasKey("frequency") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = freq;
                double adjAttenuation = _attenuation;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = _txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = _streamId;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _frequency = adjFrequency;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        BasicDoubleList DucComponent::getFrequencyRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_freqRangeMin);
            ret.push_back(_freqRangeMax);
            return ret;
        }

        double DucComponent::getFrequencyRes() const
        {
            return _freqRes;
        }

        double DucComponent::getFrequencyUnit() const
        {
            return _freqUnits;
        }

        double DucComponent::getAttenuation() const
        {
            return _attenuation;
        }

        bool DucComponent::setAttenuation(double atten)
        {
            bool ret = false;
            if ( _config.hasKey("attenuation") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = _frequency;
                double adjAttenuation = atten;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = _txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = _streamId;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _attenuation = adjAttenuation;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        BasicDoubleList DucComponent::getAttenuationRange() const
        {
            BasicDoubleList ret;
            ret.push_back(_attRangeMin);
            ret.push_back(_attRangeMax);
            return ret;
        }

        double DucComponent::getAttenuationRes() const
        {
            return _attRes;
        }

        int DucComponent::getRateIndex() const
        {
            return _rateIndex;
        }

        bool DucComponent::setRateIndex(int index)
        {
            bool ret = false;
            if ( _config.hasKey("rateIndex") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = _frequency;
                double adjAttenuation = _attenuation;
                int adjRateIndex = index;
                int adjTxChannels = _txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = _streamId;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _rateIndex = adjRateIndex;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int DucComponent::getTxChannelBitmap() const
        {
            return _txChannels;
        }

        bool DucComponent::setTxChannelBitmap(int txChannels)
        {
            bool ret = false;
            if ( _config.hasKey("txChannels") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = _frequency;
                double adjAttenuation = _attenuation;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = _streamId;
                bool ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _txChannels = adjTxChannels;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        int DucComponent::getMode() const
        {
            return _mode;
        }

        bool DucComponent::setMode(int mode)
        {
            bool ret = false;
            if ( _config.hasKey("mode") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = _frequency;
                double adjAttenuation = _attenuation;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = _txChannels;
                int adjMode = mode;
                unsigned int adjStreamId = _streamId;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _mode = adjMode;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        unsigned int DucComponent::getStreamId() const
        {
            return _streamId;
        }

        bool DucComponent::setStreamId(unsigned int sid)
        {
            bool ret = false;
            if ( _config.hasKey("streamId") )
            {
                int adjDataPort = _dataPort;
                double adjFrequency = _frequency;
                double adjAttenuation = _attenuation;
                int adjRateIndex = _rateIndex;
                int adjTxChannels = _txChannels;
                int adjMode = _mode;
                unsigned int adjStreamId = sid;
                ret = executeDucCommand(_index, adjDataPort, adjFrequency, adjAttenuation,
                        adjRateIndex, adjTxChannels, adjMode, adjStreamId);
                if ( ret )
                {
                    _streamId = adjStreamId;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        DucRateSet DucComponent::getRateSet() const
        {
            return _rateSet;
        }

        bool DucComponent::setRateSet(const DucRateSet& set)
        {
            _rateSet = set;
            return true;
        }

        BasicDoubleList DucComponent::getRateList() const
        {
            BasicDoubleList ret;
            for (WbddcRateSet::const_iterator it = _rateSet.begin(); it != _rateSet.end(); it++)
            {
                ret.push_back(it->second);
            }
            return ret;
        }

        bool DucComponent::supportsSnapshotLoad() const
        {
            return true;
        }

        bool DucComponent::loadSnapshot(const std::string& filename,
                unsigned int startSample,
                unsigned int samples)
        {
            bool ret = executeSnapshotLoadCommand(_index, filename,
                    startSample, samples);
            if ( ret )
            {
                _snapFilename = filename;
                _snapStartSample = startSample;
                _snapSamples = samples;
                updateConfigurationDict();
            }
            return ret;
        }

        bool DucComponent::supportsSnapshotTransmit() const
        {
            return false;
        }

        void DucComponent::initConfigurationDict()
        {
            //this->debug("[DucComponent::initConfigurationDict] Called\n");
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define DUC-specific keys
            _config["dataPort"] = "";
            _config["frequency"] = "";
            _config["attenuation"] = "";
            _config["rateIndex"] = "";
            _config["txChannels"] = "";
            _config["mode"] = "";
            _config["streamId"] = "";
            _config["filename"] = "";
            _config["startSample"] = "";
            _config["samples"] = "";
            _config["singlePlayback"] = "";
            _config["pauseUntilEnabled"] = "";
            //this->debug("[DucComponent::initConfigurationDict] Returning\n");
        }

        void DucComponent::updateConfigurationDict()
        {
            this->debug("[DucComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("dataPort") )
                setConfigurationValueToInt("dataPort", _dataPort);
            if ( _config.hasKey("frequency") )
                setConfigurationValueToDbl("frequency", _frequency);
            if ( _config.hasKey("attenuation") )
                setConfigurationValueToDbl("attenuation", _attenuation);
            if ( _config.hasKey("rateIndex") )
                setConfigurationValueToInt("rateIndex", _rateIndex);
            if ( _config.hasKey("txChannels") )
                setConfigurationValueToInt("txChannels", _txChannels);
            if ( _config.hasKey("mode") )
                setConfigurationValueToInt("mode", _mode);
            if ( _config.hasKey("streamId") )
                setConfigurationValueToUInt("streamId", _streamId);
            if ( _config.hasKey("filename") )
                setConfigurationValue("filename", _snapFilename);
            if ( _config.hasKey("startSample") )
                setConfigurationValueToUInt("startSample", _snapStartSample);
            if ( _config.hasKey("samples") )
                setConfigurationValueToUInt("samples", _snapSamples);
            if ( _config.hasKey("singlePlayback") )
                setConfigurationValueToBool("singlePlayback", _snapSinglePlayback);
            if ( _config.hasKey("pauseUntilEnabled") )
                setConfigurationValueToBool("pauseUntilEnabled", _snapPauseUntilEnabled);
            this->debug("[DucComponent::updateConfigurationDict] Returning\n");
        }

        bool DucComponent::executeDucQuery(int index,
                int& dataPort,
                double& frequency,
                double& attenuation,
                int& rateIndex,
                int& txChannels,
                int& mode,
                unsigned int& streamId)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "DUC? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "DUC ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Data port
                    dataPort = boost::lexical_cast<int>(vec[1]);
                    // vec[2] = Frequency
                    frequency = boost::lexical_cast<double>(vec[2]);
                    // vec[3] = Attenuation
                    attenuation = boost::lexical_cast<double>(vec[3]);
                    // vec[4] = Rate index
                    rateIndex = boost::lexical_cast<int>(vec[4]);
                    // vec[5] = TX channel bitmap
                    txChannels = boost::lexical_cast<int>(vec[5]);
                    // vec[6] = Mode
                    mode = boost::lexical_cast<int>(vec[6]);
                    // vec[7] = Stream ID
                    streamId = boost::lexical_cast<unsigned int>(vec[7]);
                    ret = true;
                }
            }
            return ret;
        }

        bool DucComponent::executeDucCommand(int index,
                int& dataPort,
                double& frequency,
                double& attenuation,
                int& rateIndex,
                int& txChannels,
                int& mode,
                unsigned int& streamId)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "DUC " << index
                        << ", " << dataPort
                        << ", " << std::setprecision(1) << std::fixed << frequency
                        << ", " << std::setprecision(1) << std::fixed << attenuation
                        << ", " << rateIndex
                        << ", " << txChannels
                        << ", " << mode
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

        bool DucComponent::executeSnapshotLoadCommand(int index,
                const std::string& filename,
                unsigned int startSample,
                unsigned int samples)
        {
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "LWF "
                        << filename
                        << ", " << index
                        << ", " << startSample;
                if (samples > 0)
                {
                    oss << ", " << samples;
                }
                oss << "\n";
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
