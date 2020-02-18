/***************************************************************************
 * \file RadioHandler.cpp
 * \brief Defines the basic radio handler interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <arpa/inet.h>


namespace LibCyberRadio
{

    namespace Driver
    {
        RadioHandler::RadioHandler(
                const std::string& name,
                int numTuner,
                int tunerIndexBase,
                int numWbddc,
                int wbddcIndexBase,
                int numNbddc,
                int nbddcIndexBase,
                int numTunerBoards,
                int maxTunerBw,
                int numTransmitter,
                int transmitterIndexBase,
                int numDuc,
                int ducIndexBase,
                int numWbddcGroups,
                int wbddcGroupIndexBase,
                int numNbddcGroups,
                int nbddcGroupIndexBase,
                int numDdcGroups,
                int ddcGroupIndexBase,
                int numDataPorts,
                int dataPortIndexBase,
                int numSimpleIpSetups,
                double adcRate,
                VitaIfSpec ifSpec,
                bool debug) :
            Configurable(name, debug),
            _numTuner(numTuner),
            _tunerIndexBase(tunerIndexBase),
            _numWbddc(numWbddc),
            _wbddcIndexBase(wbddcIndexBase),
            _numNbddc(numNbddc),
            _nbddcIndexBase(nbddcIndexBase),
            _numTunerBoards(numTunerBoards),
            _maxTunerBw(maxTunerBw),
            _numTransmitter(numTransmitter),
            _transmitterIndexBase(transmitterIndexBase),
            _numDuc(numDuc),
            _ducIndexBase(ducIndexBase),
            _numWbddcGroups(numWbddcGroups),
            _wbddcGroupIndexBase(wbddcGroupIndexBase),
            _numNbddcGroups(numNbddcGroups),
            _nbddcGroupIndexBase(nbddcGroupIndexBase),
            _numDdcGroups(numDdcGroups),
            _ddcGroupIndexBase(ddcGroupIndexBase),
            _numDataPorts(numDataPorts),
            _dataPortIndexBase(dataPortIndexBase),
            _numSimpleIpSetups(numSimpleIpSetups),
            _adcRate(adcRate),
            _ifSpec(ifSpec),
            _configMode(0),
            _coherentMode(0),
            _freqNormalization(0),
            _gpsEnabled(0),
            _referenceMode(0),
            _referenceTuningVoltage(0),
            _referenceBypass(0),
            _calibFrequency(0.0),
            _lastCmdErrorInfo(""),
            _defaultTimeout(2.0),
            _defaultDeviceInfo(0)
        {
            _versionInfo["model"] = "N/A";
            _versionInfo["serialNumber"] = "N/A";
            _versionInfo["unitRevision"] = "N/A";
            _versionInfo["softwareVersion"] = "N/A";
            _versionInfo["firmwareVersion"] = "N/A";
            _versionInfo["firmwareDate"] = "N/A";
            _versionInfo["referenceVersion"] = "N/A";
            _versionInfo["hardwareVersion"] = "N/A";
            this->initConfigurationDict();
        }

        RadioHandler::~RadioHandler()
        {
            if ( isConnected() )
            {
                disconnect();
            }
            for ( TunerComponentDict::iterator it = _tuners.begin();
                    it != _tuners.end(); it++)
            {
                delete it->second;
            }
            for ( WbddcComponentDict::iterator it = _wbddcs.begin();
                    it != _wbddcs.end(); it++)
            {
                delete it->second;
            }
            for ( NbddcComponentDict::iterator it = _nbddcs.begin();
                    it != _nbddcs.end(); it++)
            {
                delete it->second;
            }
            for ( TransmitterComponentDict::iterator it = _txs.begin();
                    it != _txs.end(); it++)
            {
                delete it->second;
            }
            for ( DataPortDict::iterator it = _dataPorts.begin();
                    it != _dataPorts.end(); it++)
            {
                delete it->second;
            }
            for ( DucComponentDict::iterator it = _ducs.begin();
                    it != _ducs.end(); it++)
            {
                delete it->second;
            }
            for ( WbddcGroupComponentDict::iterator it = _wbddcGroups.begin();
                    it != _wbddcGroups.end(); it++)
            {
                delete it->second;
            }
            for ( NbddcGroupComponentDict::iterator it = _nbddcGroups.begin();
                    it != _nbddcGroups.end(); it++)
            {
                delete it->second;
            }
            for ( SimpleIpSetupDict::iterator it = _simpleIpSetups.begin();
                    it != _simpleIpSetups.end(); it++)
            {
                delete it->second;
            }
        }

        RadioHandler::RadioHandler(const RadioHandler &other) :
            Configurable(other)
        {
            _connModesSupported = other._connModesSupported;
            _numTuner = other._numTuner;
            _tunerIndexBase = other._tunerIndexBase;
            _numWbddc = other._numWbddc;
            _wbddcIndexBase = other._wbddcIndexBase;
            _numNbddc = other._numNbddc;
            _nbddcIndexBase = other._nbddcIndexBase;
            _numTunerBoards = other._numTunerBoards;
            _maxTunerBw = other._maxTunerBw;
            _numTransmitter = other._numTransmitter;
            _transmitterIndexBase = other._transmitterIndexBase;
            _numDuc = other._numDuc;
            _ducIndexBase = other._ducIndexBase;
            _numWbddcGroups = other._numWbddcGroups;
            _wbddcGroupIndexBase = other._wbddcGroupIndexBase;
            _numNbddcGroups = other._numNbddcGroups;
            _nbddcGroupIndexBase = other._nbddcGroupIndexBase;
            _numDdcGroups = other._numDdcGroups;
            _ddcGroupIndexBase = other._ddcGroupIndexBase;
            _numDataPorts = other._numDataPorts;
            _dataPortIndexBase = other._dataPortIndexBase;
            _numSimpleIpSetups = other._numSimpleIpSetups;
            _adcRate = other._adcRate;
            _ifSpec = other._ifSpec;
            _configMode = other._configMode;
            _coherentMode = other._coherentMode;
            _freqNormalization = other._freqNormalization;
            _gpsEnabled = other._gpsEnabled;
            _referenceMode = other._referenceMode;
            _referenceTuningVoltage = other._referenceTuningVoltage;
            _referenceBypass = other._referenceBypass;
            _calibFrequency = other._calibFrequency;
            _lastCmdErrorInfo = other._lastCmdErrorInfo;
            _transport = other._transport;
            _versionInfo = other._versionInfo;
            _connectionInfo = other._connectionInfo;
            _defaultTimeout = other._defaultTimeout;
            _defaultDeviceInfo = other._defaultDeviceInfo;
        }

        RadioHandler& RadioHandler::operator=(const RadioHandler& other)
        {
            Configurable::operator=(other);
            // Block self-assignment
            if (this != &other)
            {
                _connModesSupported = other._connModesSupported;
                _numTuner = other._numTuner;
                _tunerIndexBase = other._tunerIndexBase;
                _numWbddc = other._numWbddc;
                _wbddcIndexBase = other._wbddcIndexBase;
                _numNbddc = other._numNbddc;
                _nbddcIndexBase = other._nbddcIndexBase;
                _numTunerBoards = other._numTunerBoards;
                _maxTunerBw = other._maxTunerBw;
                _numTransmitter = other._numTransmitter;
                _transmitterIndexBase = other._transmitterIndexBase;
                _numDuc = other._numDuc;
                _ducIndexBase = other._ducIndexBase;
                _numWbddcGroups = other._numWbddcGroups;
                _wbddcGroupIndexBase = other._wbddcGroupIndexBase;
                _numNbddcGroups = other._numNbddcGroups;
                _nbddcGroupIndexBase = other._nbddcGroupIndexBase;
                _numDdcGroups = other._numDdcGroups;
                _ddcGroupIndexBase = other._ddcGroupIndexBase;
                _numDataPorts = other._numDataPorts;
                _dataPortIndexBase = other._dataPortIndexBase;
                _numSimpleIpSetups = other._numSimpleIpSetups;
                _adcRate = other._adcRate;
                _ifSpec = other._ifSpec;
                _configMode = other._configMode;
                _coherentMode = other._coherentMode;
                _freqNormalization = other._freqNormalization;
                _gpsEnabled = other._gpsEnabled;
                _referenceMode = other._referenceMode;
                _referenceTuningVoltage = other._referenceTuningVoltage;
                _referenceBypass = other._referenceBypass;
                _calibFrequency = other._calibFrequency;
                _lastCmdErrorInfo = other._lastCmdErrorInfo;
                _transport = other._transport;
                _versionInfo = other._versionInfo;
                _connectionInfo = other._connectionInfo;
                _defaultTimeout = other._defaultTimeout;
                _defaultDeviceInfo = other._defaultDeviceInfo;
            }
            return *this;
        }

        bool RadioHandler::isConnected() const
        {
            return _transport.isConnected();
        }

        BasicStringStringDict RadioHandler::getVersionInfo()
        {
            return _versionInfo;
        }

        BasicStringStringDict RadioHandler::getConnectionInfo()
        {
            return _connectionInfo;
        }

        bool RadioHandler::connect(const std::string &mode, const std::string &host_or_dev, const int port_or_baudrate)
        {
            this->debug("[RadioHandler::connect] Called; mode=\"%s\", HorD=\"%s\", PorB=%d\n", mode.c_str(), host_or_dev.c_str(), port_or_baudrate);
            bool ret = false;
            _connectionInfo = BasicStringStringDict();
            // Sanity check: Make sure radio supports the given connection mode
            if ( isConnectionModeSupported(mode) )
            {
                ret = _transport.connect(mode, host_or_dev, port_or_baudrate);
                this->debug("[RadioHandler::connect] Connect result: %s\n", debugBool(ret));
                if (ret)
                {
                    _connectionInfo["mode"] = mode;
                    if ( (mode == "tcp") or (mode == "udp") )
                    {
                        _connectionInfo["hostname"] = host_or_dev;
                        _connectionInfo["port"] = ( boost::format("%d") % port_or_baudrate ).str();
                    }
                    else if ( (mode == "tty") )
                    {
                        _connectionInfo["device"] = host_or_dev;
                        _connectionInfo["baudrate"] = ( boost::format("%d") % port_or_baudrate ).str();
                    }
                    this->debug("[RadioHandler::connect] Querying configuration\n");
                    this->queryConfiguration();
                }
                else
                    _lastCmdErrorInfo = _transport.getLastCommandErrorInfo();
            }
            else
            {
                std::ostringstream oss;
                oss << "Unsupported connection mode: " << mode;
                _lastCmdErrorInfo = oss.str();
            }
            this->debug("[RadioHandler::connect] Returning %s\n", debugBool(ret));
            return ret;
        }

        void RadioHandler::disconnect()
        {
            this->debug("[RadioHandler::disconnect] Called\n");
            if (_transport.isConnected())
                _transport.disconnect();
            this->debug("[RadioHandler::disconnect] Returning\n");
        }

        BasicStringList RadioHandler::sendCommand(const std::string &cmdString, double timeout)
        {
            this->debug("[RadioHandler::sendCommand] Called; cmd=\"%s\"\n",
                    Pythonesque::Strip(cmdString).c_str());
            BasicStringList ret;
            _lastCmdErrorInfo = "";
            if ( _transport.sendCommand(cmdString) )
            {
                ret = _transport.receive(timeout);
            }
            else
                _lastCmdErrorInfo = _transport.getLastCommandErrorInfo();
            // This covers the case where the act of sending the command itself
            // generates an error, but not the case where the command/response happens
            // but the response contains an error message.  This section looks for
            // error messages in the response and sets last command error info accordingly.
            BasicStringList::iterator it;
            for (it = ret.begin(); it != ret.end(); it++)
            {
                if ( it->find("ERROR") != std::string::npos )
                {
                    _lastCmdErrorInfo = Pythonesque::Replace(*it, "ERROR: ", "");
                    break;
                }
            }
            // If the first line of the response just echoed the command, remove it
            if ( (ret.size() > 0) && (ret.front() == Pythonesque::Strip(cmdString)) )
                ret.erase(ret.begin());
            // Debug print
            this->debug("[RadioHandler::sendCommand] Returning %lu elements\n", ret.size());
            for (it = ret.begin(); it != ret.end(); it++)
                this->debug("[RadioHandler::sendCommand] -- %s\n", it->c_str());
            return ret;
        }

        void RadioHandler::queryConfiguration()
        {
            this->queryVersionInfo();
            if ( this->queryRadioConfiguration() )
                this->updateConfigurationDict();
            for ( TunerComponentDict::iterator it = _tuners.begin();
                    it != _tuners.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( WbddcComponentDict::iterator it = _wbddcs.begin();
                    it != _wbddcs.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( NbddcComponentDict::iterator it = _nbddcs.begin();
                    it != _nbddcs.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( TransmitterComponentDict::iterator it = _txs.begin();
                    it != _txs.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( DataPortDict::iterator it = _dataPorts.begin();
                    it != _dataPorts.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( DucComponentDict::iterator it = _ducs.begin();
                    it != _ducs.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( WbddcGroupComponentDict::iterator it = _wbddcGroups.begin();
                    it != _wbddcGroups.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( NbddcGroupComponentDict::iterator it = _nbddcGroups.begin();
                    it != _nbddcGroups.end(); it++)
            {
                it->second->queryConfiguration();
            }
            for ( SimpleIpSetupDict::iterator it = _simpleIpSetups.begin();
                    it != _simpleIpSetups.end(); it++)
            {
                it->second->queryConfiguration();
            }
        }

        bool RadioHandler::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[RadioHandler::setConfiguration] Called\n");
            // Call the parent version.
            bool ret = Configurable::setConfiguration(cfg);
            int adjCfg = _configMode;
            int adjCoh = _coherentMode;
            int adjFnr = _freqNormalization;
            int adjGps = _gpsEnabled;
            int adjRef = _referenceMode;
            int adjRtv = _referenceTuningVoltage;
            int adjByp = _referenceBypass;
            double adjCal = _calibFrequency;
            if ( cfg.find("configMode") != cfg.end() )
            {
                adjCfg = getConfigurationValueAsInt("configMode");
                ret &= this->executeConfigModeCommand(adjCfg);
            }
            if ( cfg.find("coherentMode") != cfg.end() )
            {
                adjCoh = getConfigurationValueAsInt("coherentMode");
                ret &= this->executeCoherentModeCommand(adjCoh);
            }
            if ( cfg.find("freqNormalization") != cfg.end() )
            {
                adjFnr = getConfigurationValueAsInt("freqNormalization");
                ret &= this->executeFreqNormalizationCommand(adjFnr);
            }
            if ( cfg.find("gpsEnabled") != cfg.end() )
            {
                adjGps = getConfigurationValueAsInt("gpsEnabled");
                ret &= this->executeGpsEnabledCommand(adjGps);
            }
            if ( cfg.find("referenceMode") != cfg.end() )
            {
                adjRef = getConfigurationValueAsInt("referenceMode");
                ret &= this->executeReferenceModeCommand(adjRef);
            }
            if ( cfg.find("referenceTuningVoltage") != cfg.end() )
            {
                adjRtv = getConfigurationValueAsInt("referenceTuningVoltage");
                ret &= this->executeReferenceVoltageCommand(adjRtv);
            }
            if ( cfg.find("bypassMode") != cfg.end() )
            {
                adjByp = getConfigurationValueAsInt("bypassMode");
                ret &= this->executeReferenceBypassCommand(adjByp);
            }
            if ( cfg.find("calibFrequency") != cfg.end() )
            {
                adjCal = getConfigurationValueAsDbl("calibFrequency");
                ret &= this->executeCalibFrequencyCommand(adjCal);
            }
            if ( ret )
            {
                _configMode = adjCfg;
                _coherentMode = adjCoh;
                _freqNormalization = adjFnr;
                _gpsEnabled = adjGps;
                _referenceMode = adjRef;
                _referenceTuningVoltage = adjRtv;
                _referenceBypass = adjByp;
                _calibFrequency = adjCal;
                updateConfigurationDict();
            }
            this->debug("[RadioHandler::setConfiguration] Returning\n");
            return ret;
        }

        std::string RadioHandler::getLastCommandErrorInfo() const
        {
            return _lastCmdErrorInfo;
        }

        bool RadioHandler::sendReset(int resetType)
        {
            return this->executeResetCommand(resetType);
        }

        bool RadioHandler::getPps()
        {
            return this->executePpsQuery();
        }

        bool RadioHandler::setTimeNextPps(bool checkTime, bool useGpsTime)
        {
            bool ret = this->getPps();
            if ( ret )
            {
                // Determine target time -- either the next whole second
                // after current system time, or GPS time, as requested.
                time_t targetTime = time(NULL) + 1;
                std::string adjTime;
                if ( useGpsTime )
                {
                    // Set target time based on GPS time
                    adjTime = "G";
                    ret = this->executeTimeCommand(adjTime);
                }
                else
                {
                    // Set target time based on system time
                    adjTime = boost::lexical_cast<std::string>(targetTime);
                    ret = this->executeTimeCommand(adjTime);
                }
                if ( ret )
                {
                    if ( checkTime )
                    {
                        time_t radioUtc = this->getTimeNextPps();
                        ret = (radioUtc == targetTime);
                    }
                }
            }
            else
            {
                ret = false;
            }
            return ret;
        }

        time_t RadioHandler::getTimeNow()
        {
            time_t ret = 0;
            std::string adjTime;
            this->debug("[RadioHandler::getTimeNow] Executing time query\n");
            if ( this->executeTimeQuery(adjTime) )
            {
                this->debug("[RadioHandler::getTimeNow] -- query result: %s\n", adjTime.c_str());
                ret = (time_t)boost::lexical_cast<unsigned int>(adjTime);
                //this->debug("[RadioHandler::getTimeNow] -- converted: %lu\n", ret);
            }
            return ret;
        }

        time_t RadioHandler::getTimeNextPps()
        {
            time_t ret = 0;
            bool ok = this->getPps();
            if ( ok )
            {
                ret = this->getTimeNow();
            }
            return ret;
        }

        unsigned int RadioHandler::getStatus()
        {
            unsigned int ret = 0;
            unsigned int stat = 0;
            if ( this->executeStatusQuery(stat) )
            {
                ret = stat;
            }
            return ret;
        }

        unsigned int RadioHandler::getTstatus()
        {
            unsigned int ret = 0;
            unsigned int stat = 0;
            if ( this->executeTstatusQuery(stat) )
            {
                ret = stat;
            }
            return ret;
        }

        bool RadioHandler::setReferenceMode(int mode)
        {
            ConfigurationDict cfg;
            cfg["referenceMode"] = mode;
            return this->setConfiguration(cfg);
        }

        bool RadioHandler::setBypassMode(int mode)
        {
            ConfigurationDict cfg;
            cfg["bypassMode"] = mode;
            return this->setConfiguration(cfg);
        }

        bool RadioHandler::setTimeAdjustment(int tunerIndex, int timeAdjustValue)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(tunerIndex);
            if ( it != _tuners.end() )
                ret = it->second->setTimingAdjustment(timeAdjustValue);
            return ret;
        }

        BasicDoubleList RadioHandler::getGpsPosition()
        {
            BasicDoubleList ret = {0.0, 0.0};
            double lat = 0.0;
            double lon = 0.0;
            if ( this->executeGpsPositionQuery(lat, lon) )
            {
                ret[0] = lat;
                ret[1] = lon;
            }
            return ret;
        }

        int RadioHandler::getTemperature()
        {
            int ret = 0;
            int temp = 0;
            if ( this->executeTemperatureQuery(temp) )
            {
                ret = temp;
            }
            return ret;
        }

        int RadioHandler::getNumDataPorts() const
        {
            return _numDataPorts;
        }

        int RadioHandler::getGpioOutput()
        {
            int ret = 0;
            int value = 0;
            if ( this->executeGpioStaticQuery(value) )
            {
                ret = value;
            }
            return ret;
        }

        BasicIntList RadioHandler::getGpioOutputByIndex(int index)
        {
            BasicIntList ret = {0, 0, 0};
            int value = 0;
            int duration = 0;
            int loop = 0;
            if ( this->executeGpioSequenceQuery(index, value, duration, loop) )
            {
                ret[0] = value;
                ret[1] = duration;
                ret[2] = loop;
            }
            return ret;
        }

        bool RadioHandler::setGpioOutput(int value)
        {
            bool ret = false;
            int adjValue = value;
            if ( this->executeGpioStaticCommand(adjValue) )
                ret = true;
            return ret;
        }

        bool RadioHandler::setGpioOutputByIndex(int index, int value,
                int duration, int loop, int go)
        {
            bool ret = false;
            int adjValue = value;
            int adjDur = duration;
            int adjLoop = loop;
            int adjGo = go;
            if ( this->executeGpioSequenceCommand(index, adjValue, adjDur, adjLoop, adjGo) )
                ret = true;
            return ret;
        }

        double RadioHandler::getCalibrationFrequency() const
        {
            return _calibFrequency;
        }

        bool RadioHandler::setCalibrationFrequency(double freq)
        {
            bool ret = false;
            if ( _config.find("calibFrequency") != _config.end() )
            {
                ConfigurationDict cfg;
                cfg["calibFrequency"] = freq;
                ret = this->setConfiguration(cfg);
            }
            return ret;
        }

        BasicIntList RadioHandler::getDataPortIndexRange() const
        {
            BasicIntList ret;
            for (int num = _dataPortIndexBase; num < _dataPortIndexBase + _numDataPorts; num++)
                ret.push_back(num);
            return ret;
        }

        int RadioHandler::getNumDataPortDipEntries() const
        {
            int ret;
            DataPortDict::const_iterator it = _dataPorts.begin();
            if ( it != _dataPorts.end() )
                ret = it->second->getNumDestEntries();
            return ret;
        }

        BasicIntList RadioHandler::getDataPortDipEntryIndexRange() const
        {
            BasicIntList ret;
            DataPortDict::const_iterator it = _dataPorts.begin();
            if ( it != _dataPorts.end() )
                ret = it->second->getDestEntryIndexRange();
            return ret;
        }

        BasicStringList RadioHandler::getConnectionModeList() const
        {
            return _connModesSupported;
        }

        bool RadioHandler::isConnectionModeSupported(const std::string &mode) const
        {
            bool ret = false;
            if (std::find(_connModesSupported.begin(), _connModesSupported.end(), mode) != _connModesSupported.end())
            {
                ret = true;
            }
            return ret;
        }

        double RadioHandler::getAdcRate() const
        {
            return _adcRate;
        }

        int RadioHandler::getVitaHeaderSize() const
        {
            return _ifSpec.headerSizeWords * 4;
        }

        int RadioHandler::getVitaPayloadSize() const
        {
            return _ifSpec.payloadSizeWords * 4;
        }

        int RadioHandler::getVitaTailSize() const
        {
            return _ifSpec.tailSizeWords * 4;
        }

        bool RadioHandler::isByteswapped() const
        {
            // Get our byte order
            const char *ourByteOrder = "little";
            if ( htonl(0xDEAD) == 0xDEAD )
                ourByteOrder = "big";
            // Compare it to the IF spec
            return ( strcmp(ourByteOrder, _ifSpec.byteOrder) != 0 );
        }

        bool RadioHandler::isIqSwapped() const
        {
            return _ifSpec.iqSwapped;
        }

        const char* RadioHandler::getByteOrder() const
        {
            return _ifSpec.byteOrder;
        }

        int RadioHandler::getNumTuner() const
        {
            return _numTuner;
        }

        int RadioHandler::getNumTunerBoards() const
        {
            return _numTunerBoards;
        }

        BasicIntList RadioHandler::getTunerIndexRange() const
        {
            BasicIntList ret;
            for (int num = _tunerIndexBase; num < _tunerIndexBase + _numTuner; num++)
                ret.push_back(num);
            return ret;
        }

        BasicDoubleList RadioHandler::getTunerFrequencyRange() const
        {
            BasicDoubleList ret;
            TunerComponentDict::const_iterator it = _tuners.begin();
            if ( it != _tuners.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double RadioHandler::getTunerFrequencyRes() const
        {
            double ret = 0.0;
            TunerComponentDict::const_iterator it = _tuners.begin();
            if ( it != _tuners.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        double RadioHandler::getTunerFrequencyUnit() const
        {
            double ret = 0.0;
            TunerComponentDict::const_iterator it = _tuners.begin();
            if ( it != _tuners.end() )
                ret = it->second->getFrequencyUnit();
            return ret;
        }

        BasicDoubleList RadioHandler::getTunerAttenuationRange() const
        {
            BasicDoubleList ret;
            TunerComponentDict::const_iterator it = _tuners.begin();
            if ( it != _tuners.end() )
                ret = it->second->getAttenuationRange();
            return ret;
        }

        double RadioHandler::getTunerAttenuationRes() const
        {
            double ret = 0.0;
            TunerComponentDict::const_iterator it = _tuners.begin();
            if ( it != _tuners.end() )
                ret = it->second->getAttenuationRes();
            return ret;
        }

        bool RadioHandler::isTunerEnabled(int index) const
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableTuner(int index, bool enabled)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableTuner(int index)
        {
            return enableTuner(index, false);
        }

        double RadioHandler::getTunerFrequency(int index) const
        {
            double ret = 0.0;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool RadioHandler::setTunerFrequency(int index, double freq)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        double RadioHandler::getTunerAttenuation(int index) const
        {
            double ret = 0.0;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->getAttenuation();
            return ret;
        }

        bool RadioHandler::setTunerAttenuation(int index, double atten)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->setAttenuation(atten);
            return ret;
        }

        int RadioHandler::getTunerFilter(int index) const
        {
            int ret = 0;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->getFilter();
            return ret;
        }

        bool RadioHandler::setTunerFilter(int index, int filter)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->setFilter(filter);
            return ret;
        }

        ConfigurationDict RadioHandler::getTunerConfiguration(int index) const
        {
            ConfigurationDict ret;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setTunerConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            TunerComponentDict::const_iterator it = _tuners.find(index);
            if ( it != _tuners.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        int RadioHandler::getNumWbddc() const
        {
            return _numWbddc;
        }

        BasicIntList RadioHandler::getWbddcIndexRange() const
        {
            BasicIntList ret;
            for (int num = _wbddcIndexBase; num < _wbddcIndexBase + _numWbddc; num++)
                ret.push_back(num);
            return ret;
        }

        bool RadioHandler::isWbddcTunable() const
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->isTunable();
            return ret;
        }

        bool RadioHandler::isWbddcSelectableSource() const
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->isSourceSelectable();
            return ret;
        }

        BasicDoubleList RadioHandler::getWbddcFrequencyRange() const
        {
            BasicDoubleList ret;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double RadioHandler::getWbddcFrequencyRes() const
        {
            double ret = 0.0;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        double RadioHandler::getWbddcFrequencyUnit() const
        {
            double ret = 0.0;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->getFrequencyUnit();
            return ret;
        }

        WbddcRateSet RadioHandler::getWbddcRateSet() const
        {
            WbddcRateSet ret;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->getRateSet();
            return ret;
        }

        BasicDoubleList RadioHandler::getWbddcRateList() const
        {
            BasicDoubleList ret;
            WbddcComponentDict::const_iterator it = _wbddcs.begin();
            if ( it != _wbddcs.end() )
                ret = it->second->getRateList();
            return ret;
        }

        bool RadioHandler::isWbddcEnabled(int index) const
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableWbddc(int index, bool enabled)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableWbddc(int index)
        {
            return enableWbddc(index, false);
        }

        double RadioHandler::getWbddcFrequency(int index) const
        {
            double ret = 0.0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool RadioHandler::setWbddcFrequency(int index, double freq)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        int RadioHandler::getWbddcSource(int index) const
        {
            int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getSource();
            return ret;
        }

        bool RadioHandler::setWbddcSource(int index, int source)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setSource(source);
            return ret;
        }

        int RadioHandler::getWbddcRateIndex(int index) const
        {
            int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getRateIndex();
            return ret;
        }

        bool RadioHandler::setWbddcRateIndex(int index, int rateIndex)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setRateIndex(rateIndex);
            return ret;
        }

        int RadioHandler::getWbddcUdpDestination(int index) const
        {
            int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getUdpDestination();
            return ret;
        }

        bool RadioHandler::setWbddcUdpDestination(int index, int dest)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setUdpDestination(dest);
            return ret;
        }

        int RadioHandler::getWbddcVitaEnable(int index) const
        {
            int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getVitaEnable();
            return ret;
        }

        bool RadioHandler::setWbddcVitaEnable(int index, int enable)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setVitaEnable(enable);
            return ret;
        }

        unsigned int RadioHandler::getWbddcStreamId(int index) const
        {
            unsigned int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getStreamId();
            return ret;
        }

        bool RadioHandler::setWbddcStreamId(int index, unsigned int sid)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setStreamId(sid);
            return ret;
        }

        int RadioHandler::getWbddcDataPort(int index) const
        {
            int ret = 0;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getDataPort();
            return ret;
        }

        bool RadioHandler::setWbddcDataPort(int index, int port)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setDataPort(port);
            return ret;
        }

        bool RadioHandler::setWbddcRateSet(int index, const WbddcRateSet& set)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setRateSet(set);
            return ret;
        }

        ConfigurationDict RadioHandler::getWbddcConfiguration(int index) const
        {
            ConfigurationDict ret;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setWbddcConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            WbddcComponentDict::const_iterator it = _wbddcs.find(index);
            if ( it != _wbddcs.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        int RadioHandler::getNumNbddc() const
        {
            return _numNbddc;
        }

        BasicIntList RadioHandler::getNbddcIndexRange() const
        {
            BasicIntList ret;
            for (int num = _nbddcIndexBase; num < _nbddcIndexBase + _numNbddc; num++)
                ret.push_back(num);
            return ret;
        }

        BasicDoubleList RadioHandler::getNbddcFrequencyRange() const
        {
            BasicDoubleList ret;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double RadioHandler::getNbddcFrequencyRes() const
        {
            double ret = 0.0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        double RadioHandler::getNbddcFrequencyUnit() const
        {
            double ret = 0.0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getFrequencyUnit();
            return ret;
        }

        NbddcRateSet RadioHandler::getNbddcRateSet() const
        {
            NbddcRateSet ret;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getRateSet();
            return ret;
        }

        BasicDoubleList RadioHandler::getNbddcRateList() const
        {
            BasicDoubleList ret;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getRateList();
            return ret;
        }

        bool RadioHandler::isNbddcEnabled(int index) const
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableNbddc(int index, bool enabled)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableNbddc(int index)
        {
            return enableNbddc(index, false);
        }

        ConfigurationDict RadioHandler::getNbddcConfiguration(int index) const
        {
            ConfigurationDict ret;
            NbddcComponentDict::const_iterator it = _nbddcs.find(index);
            if ( it != _nbddcs.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setNbddcConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        double RadioHandler::getNbddcFrequency(int index) const
        {
            double ret = 0.0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool RadioHandler::setNbddcFrequency(int index, double freq)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        int RadioHandler::getNbddcSource(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getSource();
            return ret;
        }

        bool RadioHandler::setNbddcSource(int index, int source)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setSource(source);
            return ret;
        }

        int RadioHandler::getNbddcRateIndex(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getRateIndex();
            return ret;
        }

        bool RadioHandler::setNbddcRateIndex(int index, int rateIndex)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setRateIndex(rateIndex);
            return ret;
        }

        int RadioHandler::getNbddcUdpDestination(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getUdpDestination();
            return ret;
        }

        bool RadioHandler::setNbddcUdpDestination(int index, int dest)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setUdpDestination(dest);
            return ret;
        }

        int RadioHandler::getNbddcVitaEnable(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getVitaEnable();
            return ret;
        }

        bool RadioHandler::setNbddcVitaEnable(int index, int enable)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setVitaEnable(enable);
            return ret;
        }

        unsigned int RadioHandler::getNbddcStreamId(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getStreamId();
            return ret;
        }

        bool RadioHandler::setNbddcStreamId(int index, unsigned int sid)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setStreamId(sid);
            return ret;
        }

        int RadioHandler::getNbddcDataPort(int index) const
        {
            int ret = 0;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->getDataPort();
            return ret;
        }

        bool RadioHandler::setNbddcDataPort(int index, int port)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setDataPort(port);
            return ret;
        }

        bool RadioHandler::setNbddcRateSet(int index, const NbddcRateSet& set)
        {
            bool ret = false;
            NbddcComponentDict::const_iterator it = _nbddcs.begin();
            if ( it != _nbddcs.end() )
                ret = it->second->setRateSet(set);
            return ret;
        }

        int RadioHandler::getNumTransmitters() const
        {
            return _numTransmitter;
        }

        BasicIntList RadioHandler::getTransmitterIndexRange() const
        {
            BasicIntList ret;
            for (int num = _transmitterIndexBase; num < _transmitterIndexBase + _numTransmitter;
                    num++)
                ret.push_back(num);
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterFrequencyRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double RadioHandler::getTransmitterFrequencyRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        double RadioHandler::getTransmitterFrequencyUnit() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getFrequencyUnit();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterAttenuationRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getAttenuationRange();
            return ret;
        }

        double RadioHandler::getTransmitterAttenuationRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getAttenuationRes();
            return ret;
        }

        bool RadioHandler::isTransmitterEnabled(int index) const
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableTransmitter(int index, bool enabled)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableTransmitter(int index)
        {
            return enableTransmitter(index, false);
        }

        double RadioHandler::getTransmitterFrequency(int index) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool RadioHandler::setTransmitterFrequency(int index, double freq)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        double RadioHandler::getTransmitterAttenuation(int index) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getAttenuation();
            return ret;
        }

        bool RadioHandler::setTransmitterAttenuation(int index, double atten)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setAttenuation(atten);
            return ret;
        }

        ConfigurationDict RadioHandler::getTransmitterConfiguration(int index) const
        {
            ConfigurationDict ret;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setTransmitterConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        bool RadioHandler::transmitterSupportsCW() const
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->supportsCW();
            return ret;
        }

        int RadioHandler::getTransmitterCWNum() const
        {
            int ret = 0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWNum();
            return ret;
        }

        BasicIntList RadioHandler::getTransmitterCWIndexRange() const
        {
            BasicIntList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWIndexRange();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWFrequencyRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWFrequencyRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWFrequencyRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWFrequencyRes();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWAmplitudeRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWAmplitudeRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWAmplitudeRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWAmplitudeRes();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWPhaseRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWPhaseRange();
            return ret;
        }

        int RadioHandler::getTransmitterCWPhaseRes() const
        {
            int ret = 0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWPhaseRes();
            return ret;
        }

        bool RadioHandler::transmitterSupportsCWSweep() const
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->supportsCWSweep();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWSweepStartRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStartRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepStartRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStartRes();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWSweepStopRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStopRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepStopRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStopRes();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWSweepStepRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStepRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepStepRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStepRes();
            return ret;
        }

        BasicDoubleList RadioHandler::getTransmitterCWSweepDwellRange() const
        {
            BasicDoubleList ret;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepDwellRange();
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepDwellRes() const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.begin();
            if ( it != _txs.end() )
                ret = it->second->getCWSweepDwellRes();
            return ret;
        }

        bool RadioHandler::enableTransmitterCW(int index, int cwIndex, bool enabled)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->enableCW(cwIndex);
            return ret;
        }

        bool RadioHandler::disableTransmitterCW(int index, int cwIndex)
        {
            return enableTransmitterCW(index, cwIndex, false);
        }

        ConfigurationDict RadioHandler::getTransmitterCWConfiguration(int index,
                int cwIndex) const
        {
            ConfigurationDict ret;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWConfiguration(cwIndex);
            return ret;
        }

        bool RadioHandler::setTransmitterCWConfiguration(int index, int cwIndex,
                ConfigurationDict& cfg)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setCWConfiguration(cwIndex, cfg);
            return ret;
        }

        double RadioHandler::getTransmitterCWFrequency(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWFrequency(cwIndex);
            return ret;
        }

        bool RadioHandler::setTransmitterCWFrequency(int index, int cwIndex, double freq)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setCWFrequency(cwIndex, freq);
            return ret;
        }

        double RadioHandler::getTransmitterCWAmplitude(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWAmplitude(cwIndex);
            return ret;
        }

        bool RadioHandler::setTransmitterCWAmplitude(int index, int cwIndex, double amp)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setCWAmplitude(cwIndex, amp);
            return ret;
        }

        double RadioHandler::getTransmitterCWPhase(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWPhase(cwIndex);
            return ret;
        }

        bool RadioHandler::setTransmitterCWPhase(int index, int cwIndex, double phase)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setCWPhase(cwIndex, phase);
            return ret;
        }

        bool RadioHandler::transmitterSupportsCWSweep(int index, int cwIndex) const
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->supportsCWSweep(cwIndex);
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepStartFrequency(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStartFrequency(cwIndex);
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepStopFrequency(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWSweepStopFrequency(cwIndex);
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepFrequencyStep(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWSweepFrequencyStep(cwIndex);
            return ret;
        }

        double RadioHandler::getTransmitterCWSweepDwellTime(int index, int cwIndex) const
        {
            double ret = 0.0;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->getCWSweepDwellTime(cwIndex);
            return ret;
        }

        bool RadioHandler::setTransmitterCWFrequencySweep(int index, int cwIndex, double start,
                double stop, double step, double dwell)
        {
            bool ret = false;
            TransmitterComponentDict::const_iterator it = _txs.find(index);
            if ( it != _txs.end() )
                ret = it->second->setCWFrequencySweep(cwIndex, start, stop, step, dwell);
            return ret;
        }

        int RadioHandler::getNumDuc() const
        {
            return _numDuc;
        }

        BasicIntList RadioHandler::getDucIndexRange() const
        {
            BasicIntList ret;
            for (int num = _ducIndexBase; num < _ducIndexBase + _numDuc; num++)
                ret.push_back(num);
            return ret;
        }

        bool RadioHandler::ducSupportsSnapshotLoad() const
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->supportsSnapshotLoad();
            return ret;
        }

        bool RadioHandler::ducSupportsSnapshotTransmit() const
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->supportsSnapshotTransmit();
            return ret;
        }

        bool RadioHandler::enableDuc(int index, bool enabled)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableDuc(int index)
        {
            return enableDuc(index, false);
        }

        ConfigurationDict RadioHandler::getDucConfiguration(int index) const
        {
            ConfigurationDict ret;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setDucConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        int RadioHandler::getDucDataPort(int index) const
        {
            int ret = 0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getDataPort();
            return ret;
        }

        bool RadioHandler::setDucDataPort(int index, int port)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setDataPort(port);
            return ret;
        }

        double RadioHandler::getDucFrequency(int index) const
        {
            double ret = 0.0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getFrequency();
            return ret;
        }

        bool RadioHandler::setDucFrequency(int index, double freq)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setFrequency(freq);
            return ret;
        }

        BasicDoubleList RadioHandler::getDucFrequencyRange() const
        {
            BasicDoubleList ret;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getFrequencyRange();
            return ret;
        }

        double RadioHandler::getDucFrequencyRes() const
        {
            double ret = 0.0;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getFrequencyRes();
            return ret;
        }

        double RadioHandler::getDucFrequencyUnit() const
        {
            double ret = 0.0;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getFrequencyUnit();
            return ret;
        }

        double RadioHandler::getDucAttenuation(int index) const
        {
            double ret = 0.0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getAttenuation();
            return ret;
        }

        bool RadioHandler::setDucAttenuation(int index, double atten)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setAttenuation(atten);
            return ret;
        }

        BasicDoubleList RadioHandler::getDucAttenuationRange() const
        {
            BasicDoubleList ret;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getAttenuationRange();
            return ret;
        }

        double RadioHandler::getDucAttenuationRes() const
        {
            double ret = 0.0;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getAttenuationRes();
            return ret;
        }

        int RadioHandler::getDucRateIndex(int index) const
        {
            int ret = 0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getRateIndex();
            return ret;
        }

        bool RadioHandler::setDucRateIndex(int index, int rateIndex)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setRateIndex(rateIndex);
            return ret;
        }

        int RadioHandler::getDucTxChannelBitmap(int index) const
        {
            int ret = 0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getTxChannelBitmap();
            return ret;
        }

        bool RadioHandler::setDucTxChannelBitmap(int index, int txChannels)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setTxChannelBitmap(txChannels);
            return ret;
        }

        int RadioHandler::getDucMode(int index) const
        {
            int ret = 0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getMode();
            return ret;
        }

        bool RadioHandler::setDucMode(int index, int mode)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setMode(mode);
            return ret;
        }

        unsigned int RadioHandler::getDucStreamId(int index) const
        {
            int ret = 0;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->getStreamId();
            return ret;
        }

        bool RadioHandler::setDucStreamId(int index, unsigned int sid)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                ret = it->second->setStreamId(sid);
            return ret;
        }

        bool RadioHandler::loadDucSnapshot(int index,
                const std::string& filename,
                unsigned int startSample,
                unsigned int samples)
        {
            bool ret = false;
            DucComponentDict::const_iterator it = _ducs.find(index);
            if ( it != _ducs.end() )
                if ( it->second->supportsSnapshotLoad() )
                    ret = it->second->loadSnapshot(filename, startSample, samples);
            return ret;
        }

        DucRateSet RadioHandler::getDucRateSet() const
        {
            DucRateSet ret;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getRateSet();
            return ret;
        }

        BasicDoubleList RadioHandler::getDucRateList() const
        {
            BasicDoubleList ret;
            DucComponentDict::const_iterator it = _ducs.begin();
            if ( it != _ducs.end() )
                ret = it->second->getRateList();
            return ret;
        }

        int RadioHandler::getNumWbddcGroups() const
        {
            return _numWbddcGroups;
        }

        BasicIntList RadioHandler::getWbddcGroupIndexRange() const
        {
            BasicIntList ret;
            for (int num = _wbddcGroupIndexBase; num < _wbddcGroupIndexBase + _numWbddcGroups; num++)
                ret.push_back(num);
            return ret;
        }

        bool RadioHandler::isWbddcGroupEnabled(int index) const
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableWbddcGroup(int index, bool enabled)
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableWbddcGroup(int index)
        {
            return enableWbddcGroup(index, false);
        }

        ConfigurationDict RadioHandler::getWbddcGroupConfiguration(int index) const
        {
            ConfigurationDict ret;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setWbddcGroupConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        BasicIntList RadioHandler::getWbddcGroupMembers(int index) const
        {
            BasicIntList ret;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->getMembers();
            return ret;
        }

        bool RadioHandler::setWbddcGroupMembers(int index, const BasicIntList& groupMembers)
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->setMembers(groupMembers);
            return ret;
        }

        bool RadioHandler::addWbddcGroupMember(int index, int member)
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->addMember(member);
            return ret;
        }

        bool RadioHandler::removeWbddcGroupMember(int index, int member)
        {
            bool ret = false;
            WbddcGroupComponentDict::const_iterator it = _wbddcGroups.find(index);
            if ( it != _wbddcGroups.end() )
                ret = it->second->removeMember(member);
            return ret;
        }

        int RadioHandler::getNumNbddcGroups() const
        {
            return _numNbddcGroups;
        }

        BasicIntList RadioHandler::getNbddcGroupIndexRange() const
        {
            BasicIntList ret;
            for (int num = _nbddcGroupIndexBase; num < _nbddcGroupIndexBase + _numNbddcGroups; num++)
                ret.push_back(num);
            return ret;
        }

        bool RadioHandler::isNbddcGroupEnabled(int index) const
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->isEnabled();
            return ret;
        }

        bool RadioHandler::enableNbddcGroup(int index, bool enabled)
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->enable(enabled);
            return ret;
        }

        bool RadioHandler::disableNbddcGroup(int index)
        {
            return enableNbddcGroup(index, false);
        }

        ConfigurationDict RadioHandler::getNbddcGroupConfiguration(int index) const
        {
            ConfigurationDict ret;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setNbddcGroupConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        BasicIntList RadioHandler::getNbddcGroupMembers(int index) const
        {
            BasicIntList ret;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->getMembers();
            return ret;
        }

        bool RadioHandler::setNbddcGroupMembers(int index, const BasicIntList& groupMembers)
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->setMembers(groupMembers);
            return ret;
        }

        bool RadioHandler::addNbddcGroupMember(int index, int member)
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->addMember(member);
            return ret;
        }

        bool RadioHandler::removeNbddcGroupMember(int index, int member)
        {
            bool ret = false;
            NbddcGroupComponentDict::const_iterator it = _nbddcGroups.find(index);
            if ( it != _nbddcGroups.end() )
                ret = it->second->removeMember(member);
            return ret;
        }

        bool RadioHandler::disableTenGigFlowControl()
        {
            return setTenGigFlowControlStatus(true);
        }

        bool RadioHandler::enableTenGigFlowControl()
        {
            return setTenGigFlowControlStatus(false);
        }

        bool RadioHandler::setTenGigFlowControlStatus(bool enable)
        {
            bool ret = true;
            for ( DataPortDict::const_iterator it = _dataPorts.begin();
                    it != _dataPorts.end(); it++)
            {
                ret &= it->second->enableFlowControl(enable);
            }
            return ret;
        }

        BasicIntBoolDict RadioHandler::getTenGigFlowControlStatus()
        {
            BasicIntBoolDict ret;
            bool enabled;
            for ( DataPortDict::iterator it = _dataPorts.begin();
                    it != _dataPorts.end(); it++)
            {
                ret[it->first] = it->second->getConfigurationValueAsBool("flowControl");
            }
            return ret;
        }

        ConfigurationDict RadioHandler::getDataPortConfiguration(int index) const
        {
            ConfigurationDict ret;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getConfiguration();
            return ret;
        }

        bool RadioHandler::setDataPortConfiguration(int index, ConfigurationDict& cfg)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setConfiguration(cfg);
            return ret;
        }

        std::string RadioHandler::getDataPortSourceIP(int index) const
        {
            std::string ret = "";
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getSourceIP();
            return ret;
        }

        bool RadioHandler::setDataPortSourceIP(int index, const std::string& ipAddr)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setSourceIP(ipAddr);
            return ret;
        }

        bool RadioHandler::enableDataPortErrors(int index, bool enabled)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->enableErrors(enabled);
            return ret;
        }

        bool RadioHandler::disableDataPortErrors(int index)
        {
            return enableDataPortErrors(index, false);
        }

        bool RadioHandler::enableDataPortFlowControl(int index, bool enabled)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->enableFlowControl(enabled);
            return ret;
        }

        bool RadioHandler::disableDataPortFlowControl(int index)
        {
            return enableDataPortFlowControl(index, false);
        }

        std::string RadioHandler::getDataPortDestMACAddress(int index, int dipIndex) const
        {
            std::string ret = "";
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getDestMACAddress(dipIndex);
            return ret;
        }

        bool RadioHandler::setDataPortDestMACAddress(int index, int dipIndex,
                const std::string& macAddr)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setDestMACAddress(dipIndex, macAddr);
            return ret;
        }

        std::string RadioHandler::getDataPortDestIPAddress(int index, int dipIndex) const
        {
            std::string ret = "";
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getDestIPAddress(dipIndex);
            return ret;
        }

        bool RadioHandler::setDataPortDestIPAddress(int index, int dipIndex,
                const std::string& ipAddr)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setDestIPAddress(dipIndex, ipAddr);
            return ret;
        }

        unsigned int RadioHandler::getDataPortDestSourcePort(int index, int dipIndex) const
        {
            unsigned int ret = 0;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getDestSourcePort(dipIndex);
            return ret;
        }

        bool RadioHandler::setDataPortDestSourcePort(int index, int dipIndex,
                unsigned int sourcePort)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setDestSourcePort(dipIndex, sourcePort);
            return ret;
        }

        unsigned int RadioHandler::getDataPortDestDestPort(int index, int dipIndex) const
        {
            unsigned int ret = 0;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->getDestDestPort(dipIndex);
            return ret;
        }

        bool RadioHandler::setDataPortDestDestPort(int index, int dipIndex,
                unsigned int destPort)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setDestDestPort(dipIndex, destPort);
            return ret;
        }

        bool RadioHandler::setDataPortDestInfo(int index,
                int dipIndex,
                const std::string& ipAddr,
                const std::string& macAddr,
                unsigned int sourcePort,
                unsigned int destPort)
        {
            bool ret = false;
            DataPortDict::const_iterator it = _dataPorts.find(index);
            if ( it != _dataPorts.end() )
                ret = it->second->setDestInfo(dipIndex, ipAddr, macAddr, sourcePort,
                        destPort);
            return ret;
        }

        ConfigurationDict RadioHandler::getSimpleIPConfiguration() const
        {
            ConfigurationDict ret;
            if ( _numSimpleIpSetups > 0 )
            {
                ret = _simpleIpSetups.at(0)->getConfiguration();
            }
            return ret;
        }

        bool RadioHandler::setSimpleIPConfiguration(ConfigurationDict& cfg)
        {
            bool ret = false;
            if ( _numSimpleIpSetups > 0 )
            {
                ret = _simpleIpSetups.at(0)->setConfiguration(cfg);
            }
            return ret;
        }

        std::string RadioHandler::getSimpleSourceMACAddress() const
        {
        }

        std::string RadioHandler::getSimpleSourceIPAddress() const
        {
        }

        bool RadioHandler::setSimpleSourceIPAddress(const std::string& ipAddr)
        {
        }

        std::string RadioHandler::getSimpleDestMACAddress() const
        {
        }

        bool RadioHandler::setSimpleDestMACAddress(const std::string& macAddr)
        {
        }

        std::string RadioHandler::getSimpleDestIPAddress() const
        {
        }

        bool RadioHandler::setSimpleDestIPAddress(const std::string& ipAddr)
        {
        }

        int RadioHandler::getDefaultDeviceInfo() const
        {
            return _defaultDeviceInfo;
        }

        // Default implementation is the NDR308 pattern
        void RadioHandler::initConfigurationDict()
        {
            //this->debug("[RadioHandler::initConfigurationDict] Called\n");
            _config.clear();
            _config["calibFrequency"] = _calibFrequency;
            _config["coherentMode"] = _coherentMode;
            _config["configMode"] = _configMode;
            _config["referenceMode"] = _referenceMode;
            _config["bypassMode"] = _referenceBypass;
            _config["freqNormalization"] = _freqNormalization;
            _config["gpsEnable"] = _gpsEnabled;
            _config["referenceTuningVoltage"] = _referenceTuningVoltage;
            //this->debug("[RadioHandler::initConfigurationDict] Returning\n");
        }

        void RadioHandler::updateConfigurationDict()
        {
            //this->debug("[RadioHandler::updateConfigurationDict] Called\n");
            if ( _config.hasKey("configMode") )
            {
                _config["configMode"] = _configMode;
            }
            if ( _config.hasKey("coherentMode") )
            {
                _config["coherentMode"] = _coherentMode;
            }
            if ( _config.hasKey("freqNormalization") )
            {
                _config["freqNormalization"] = _freqNormalization;
            }
            if ( _config.hasKey("gpsEnable") )
            {
                _config["gpsEnable"] = _gpsEnabled;
            }
            if ( _config.hasKey("referenceMode") )
            {
                _config["referenceMode"] = _referenceMode;
            }
            if ( _config.hasKey("bypassMode") )
            {
                _config["bypassMode"] = _referenceBypass;
            }
            if ( _config.hasKey("referenceTuningVoltage") )
            {
                _config["referenceTuningVoltage"] = _referenceTuningVoltage;
            }
            if ( _config.hasKey("calibFrequency") )
            {
                _config["calibFrequency"] = _calibFrequency;
            }
            //this->debug("[RadioHandler::updateConfigurationDict] Returning\n");
        }

        bool RadioHandler::queryVersionInfo()
        {
            this->debug("[RadioHandler::queryVersionInfo] Called\n");
            bool ret = executeQueryIDN(_versionInfo["model"], _versionInfo["serialNumber"]);
            if (ret)
            {
                ret = executeQueryVER(_versionInfo["softwareVersion"],
                        _versionInfo["firmwareVersion"],
                        _versionInfo["referenceVersion"],
                        _versionInfo["firmwareDate"] );
                if ( ret )
                {
                    ret = executeQueryHREV(_versionInfo["hardwareVersion"]);
                }
            }
            this->debug("[RadioHandler::queryVersionInfo] Returning %s\n", debugBool(ret));
            if (ret)
            {
                for (BasicStringStringDict::iterator it = _versionInfo.begin(); it != _versionInfo.end(); it++)
                {
                    this->debug("[RadioHandler::queryVersionInfo] %s = \"%s\"\n", it->first.c_str(), it->second.c_str());
                }
            }
            return ret;
        }

        bool RadioHandler::queryRadioConfiguration()
        {
            bool ret = true;
            if ( _config.hasKey("configMode") )
            {
                ret &= this->executeConfigModeQuery(_configMode);
            }
            if ( _config.hasKey("coherentMode") )
            {
                ret &= this->executeCoherentModeQuery(_coherentMode);
            }
            if ( _config.hasKey("freqNormalization") )
            {
                ret &= this->executeFreqNormalizationQuery(_freqNormalization);
            }
            if ( _config.hasKey("gpsEnable") )
            {
                ret &= this->executeGpsEnabledQuery(_gpsEnabled);
            }
            if ( _config.hasKey("referenceMode") )
            {
                ret &= this->executeReferenceModeQuery(_referenceMode);
            }
            if ( _config.hasKey("bypassMode") )
            {
                ret &= this->executeReferenceBypassQuery(_referenceBypass);
            }
            if ( _config.hasKey("referenceTuningVoltage") )
            {
                ret &= this->executeReferenceVoltageQuery(_referenceTuningVoltage);
            }
            if ( _config.hasKey("calibFrequency") )
            {
                ret &= this->executeCalibFrequencyQuery(_calibFrequency);
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        //        NDR308 Receiver
        //        S/N 2038
        //        OK
        bool RadioHandler::executeQueryIDN(std::string& model,
                std::string& serialNumber)
        {
            bool ret = false;
            // Issue the identity query to get model and serial number
            BasicStringList rsp = sendCommand("*IDN?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( it->find(" Receiver") != std::string::npos )
                        model = Pythonesque::Replace(*it, " Receiver", "");
                    else if ( it->find("NDR") != std::string::npos )
                        model = *it;
                    if ( it->find("S/N ") != std::string::npos )
                        serialNumber = Pythonesque::Replace(*it, "S/N ", "");
                }
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        //                  NDR308 Application code:
        //                     REV: 16.02.16
        //                     Date: Feb 16 2016 13:59:48
        //                  FPGA Rev: 20150923
        //                  NDR308 Digital Reference Code Version: 16.01.21
        //                  OK
        bool RadioHandler::executeQueryVER(std::string& softwareVersion,
                std::string& firmwareVersion,
                std::string& referenceVersion,
                std::string& firmwareDate)
        {
            bool ret = true;
            // Query the version command to get software versioning info
            BasicStringList rsp = sendCommand("VER?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( it->find("   REV: ") != std::string::npos )
                        softwareVersion = Pythonesque::Replace(*it, "   REV: ", "");
                    if ( it->find("   Date: ") != std::string::npos )
                        firmwareDate = Pythonesque::Replace(*it, "   Date: ", "");
                    if ( it->find("FPGA Rev: ") != std::string::npos )
                        firmwareVersion = Pythonesque::Replace(*it, "FPGA Rev: ", "");
                    std::string::size_type pos = it->find("Digital Reference Code Version: ");
                    if ( pos != std::string::npos )
                        referenceVersion = it->substr(pos+32, std::string::npos);
                }
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        //        Unit
        //          Model: NDR308 Receiver
        //          Serial: 2038
        //          Revision: 04.00
        //        Digital Board_tuners
        //           Model: 602851
        //          Serial: 51150004
        //          Revision: 05.00
        //        Tuner Quad 1:
        //          Board Model   : 603056
        //          Board Revision: 04.00
        //          Serial Number : IE7210015
        //          Bandwidth: 6000
        //        Tuner Quad 2:Not Installed
        bool RadioHandler::executeQueryHREV(std::string& hardwareInfo)
        {
            bool ret = true;
            // Query the hardware revision command to get other stuff
            BasicStringList rsp = sendCommand("HREV?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                std::ostringstream oss;
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( *it != "OK" )
                    {
                        if ( oss.str() != "" )
                            oss << "\n";
                        //oss << Pythonesque::Strip(*it);
                        oss << *it;
                    }
                }
                hardwareInfo = oss.str();
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        // (a radio that doesn't actually support this command)
        bool RadioHandler::executeResetCommand(int resetType)
        {
            bool ret = false;
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        bool RadioHandler::executePpsQuery()
        {
            bool ret = false;
            // Query the PPS
            BasicStringList rsp = sendCommand("PPS?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        bool RadioHandler::executeTimeQuery(std::string& timeStr)
        {
            bool ret = false;
            // Query the time
            BasicStringList rsp = sendCommand("UTC?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( it->find("UTC ") != std::string::npos )
                        timeStr = Pythonesque::Replace(*it, "UTC ", "");
                }
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        bool RadioHandler::executeTimeCommand(std::string& timeStr)
        {
            bool ret = false;
            // Query the time
            BasicStringList rsp = sendCommand("UTC?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( it->find("UTC ") != std::string::npos )
                        timeStr = Pythonesque::Replace(*it, "UTC ", "");
                }
                ret = true;
            }
            return ret;
        }

        // NOTE: Default implementation is based on the NDR308 response
        bool RadioHandler::executeGpsTimeQuery(std::string& timeStr)
        {
            bool ret = false;
            // Query the time
            BasicStringList rsp = sendCommand("GUTC?\n", _defaultTimeout);
            if ( getLastCommandErrorInfo() == "" )
            {
                BasicStringList::iterator it;
                for (it = rsp.begin(); it != rsp.end(); it++)
                {
                    if ( it->find("GUTC ") != std::string::npos )
                        timeStr = Pythonesque::Replace(*it, "GUTC ", "");
                }
                ret = true;
            }
            return ret;
        }

        bool RadioHandler::executeConfigModeQuery(int& configMode)
        {
            this->debug("[RadioHandler::executeConfigModeQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "CFG?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "CFG ", ""),
                            ", ");
                    // vec[0] = Config mode indicator
                    configMode = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeConfigModeQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeConfigModeCommand(int& configMode)
        {
            this->debug("[RadioHandler::executeConfigModeCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "CFG " << configMode << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeConfigModeCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeCoherentModeQuery(int& coherentMode)
        {
            this->debug("[RadioHandler::executeCoherentModeQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "COH?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "COH ", ""),
                            ", ");
                    // vec[0] = Coherent mode indicator
                    // NOTE: This is a hex string, prefixed by "0x".  Lexical_cast does
                    // not work.
                    std::istringstream iss(vec[0]);
                    iss >> std::hex >> coherentMode;
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeCoherentModeQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeCoherentModeCommand(int& coherentMode)
        {
            this->debug("[RadioHandler::executeCoherentModeCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "COH " << coherentMode << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeCoherentModeCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeFreqNormalizationQuery(int& fnrMode)
        {
            this->debug("[RadioHandler::executeFreqNormalizationQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "FNR?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "FNR ", ""),
                            ", ");
                    // vec[0] = FNR mode indicator
                    fnrMode = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeFreqNormalizationQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeFreqNormalizationCommand(int& fnrMode)
        {
            this->debug("[RadioHandler::executeFreqNormalizationCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "FNR " << fnrMode << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeFreqNormalizationCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpsEnabledQuery(int& enabled)
        {
            this->debug("[RadioHandler::executeGpsEnabledQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPS?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "GPS ", ""),
                            ", ");
                    // vec[0] = GPS mode indicator
                    enabled = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpsEnabledQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpsPositionQuery(double& lat, double& lon)
        {
            this->debug("[RadioHandler::executeGpsPositionQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPOS?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "GPOS ", ""),
                            ", ");
                    // vec[0] = GPS position string (comma-separated NMEA)
                    BasicStringList coords = Pythonesque::Split(vec[0], ",");
                    lat = this->getDecimalDegreesFromNmea(coords[0]);
                    lon = this->getDecimalDegreesFromNmea(coords[1]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpsPositionQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpsEnabledCommand(int& enabled)
        {
            this->debug("[RadioHandler::executeGpsEnabledCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPS " << enabled << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpsEnabledCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceModeQuery(int& refMode)
        {
            this->debug("[RadioHandler::executeReferenceModeQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "REF?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "REF ", ""),
                            ", ");
                    // vec[0] = Ref mode indicator
                    refMode = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceModeQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceModeCommand(int& refMode)
        {
            this->debug("[RadioHandler::executeReferenceModeCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "REF " << refMode << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceModeCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceBypassQuery(int& bypassMode)
        {
            this->debug("[RadioHandler::executeReferenceBypassQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "RBYP?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "RBYP ", ""),
                            ", ");
                    // vec[0] = Ref bypass mode indicator
                    bypassMode = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceBypassQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceBypassCommand(int& bypassMode)
        {
            this->debug("[RadioHandler::executeReferenceBypassCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "RBYP " << bypassMode << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceBypassCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceVoltageQuery(int& voltage)
        {
            this->debug("[RadioHandler::executeReferenceVoltageQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "RTV?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "RTV ", ""),
                            ", ");
                    // vec[0] = Ref tuning voltage indicator
                    voltage = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceVoltageQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeReferenceVoltageCommand(int& voltage)
        {
            this->debug("[RadioHandler::executeReferenceVoltageCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "RTV " << voltage << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeReferenceVoltageCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeStatusQuery(unsigned int& stat)
        {
            this->debug("[RadioHandler::executeStatusQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "STAT?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "STAT ", ""),
                            ", ");
                    // vec[0] = Status
                    // NOTE: This is a hex string, so lexical_cast will not work
                    std::istringstream iss(vec[0]);
                    iss >> std::hex >> stat;
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeStatusQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeTstatusQuery(unsigned int& stat)
        {
            this->debug("[RadioHandler::executeTstatusQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "TSTAT?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TSTAT ", ""),
                            ", ");
                    // vec[0] = Status
                    // NOTE: This is a hex string, so lexical_cast will not work
                    std::istringstream iss(vec[0]);
                    iss >> std::hex >> stat;
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeTstatusQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeTemperatureQuery(int& temp)
        {
            this->debug("[RadioHandler::executeTemperatureQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "TEMP?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "TEMP ", ""),
                            ", ");
                    // vec[0] = Temperature
                    temp = boost::lexical_cast<int>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeTemperatureQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpioStaticQuery(int& value)
        {
            this->debug("[RadioHandler::executeGpioStaticQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPIO?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "GPIO ", ""),
                            ", ");
                    // vec[0] = GPIO value
                    // NOTE: This is a hex string, so lexical_cast will not work
                    std::istringstream iss(vec[0]);
                    iss >> std::hex >> value;
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpioStaticQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpioSequenceQuery(int index, int& value,
                int &duration, int& loop)
        {
            this->debug("[RadioHandler::executeGpioSequenceQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPIO? " << index << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "GPIO ", ""),
                            ", ");
                    // vec[0] = Index
                    // vec[1] = Value
                    // NOTE: This is a hex string, so lexical_cast will not work
                    std::istringstream iss(vec[1]);
                    iss >> std::hex >> value;
                    // vec[2] = Duration
                    duration = boost::lexical_cast<int>(vec[2]);
                    // vec[3] = Loop
                    loop = boost::lexical_cast<int>(vec[3]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpioSequenceQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpioStaticCommand(int& value)
        {
            this->debug("[RadioHandler::executeGpioStaticCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPIO " << value << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpioStaticCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeGpioSequenceCommand(int index, int& value,
                int &duration, int& loop,
                int &go)
        {
            this->debug("[RadioHandler::executeGpioSequenceCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "GPIO " << index
                        << ", " << value
                        << ", " << duration
                        << ", " << loop
                        << ", " << go
                        << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeGpioSequenceCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeCalibFrequencyQuery(double& freq)
        {
            this->debug("[RadioHandler::executeCalibFrequencyQuery] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "CALF?" << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    BasicStringList vec = Pythonesque::Split(
                            Pythonesque::Replace(rsp.front(), "CALF ", ""),
                            ", ");
                    // vec[0] = Calibration freq
                    freq = boost::lexical_cast<double>(vec[0]);
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeCalibFrequencyQuery] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        bool RadioHandler::executeCalibFrequencyCommand(double& freq)
        {
            this->debug("[RadioHandler::executeCalibFrequencyCommand] Called\n");
            bool ret = false;
            if ( this->isConnected() )
            {
                std::ostringstream oss;
                oss << "CALF " << freq
                        << "\n";
                BasicStringList rsp = this->sendCommand(oss.str(), 2.0);
                if ( this->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[RadioHandler::executeCalibFrequencyCommand] Returning %s\n",
                    this->debugBool(ret));
            return ret;
        }

        double RadioHandler::getDecimalDegreesFromNmea(const std::string& coord)
        {
            double ret = 0.0;
            // Get the sign from the directional indicator
            int sgn = 1;
            if ( (coord[0] == 'W') || (coord[0] == 'S') )
                sgn = -1;
            // Find the decimal point position
            std::string::size_type dotPos = coord.find('.');
            // Get the degrees part of the string, then convert to decimal
            std::string degPart = coord.substr(1, dotPos - 3);
            double degs = boost::lexical_cast<double>(degPart);
            // Get the minutes part of the string, then convert to decimal
            std::string minPart = coord.substr(dotPos - 2, std::string::npos);
            double mins = boost::lexical_cast<double>(minPart);
            // Calculate decimal degrees
            ret = degs + mins / 60.0;
            ret = ret * sgn;
            return ret;
        }

    } /* namespace Driver */

} /* namespace LibCyberRadio */

