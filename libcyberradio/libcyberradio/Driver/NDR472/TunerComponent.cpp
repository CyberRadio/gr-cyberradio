/***************************************************************************
 * \file TunerComponent.cpp
 * \brief Defines the tuner interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/TunerComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR472
        {

            TunerComponent::TunerComponent(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     double frequency,
                     double attenuation,
                     int filter) :
                ::LibCyberRadio::Driver::TunerComponent(
                        /* const std::string& name */ (boost::format("NDR472-TUNER%02d") % \
                                index).str(),
                        /* int index */ index,
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* double freqRangeMin */ 20e6,
                        /* double freqRangeMax */ 3000e6,
                        /* double freqRes */ 1e6,
                        /* double freqUnits */ 1e6,
                        /* double attRangeMin */ 0.0,
                        /* double attRangeMax */ 30.0,
                        /* double attRes */ 1.0,
                        /* bool agc */ false,
                        /* double frequency */ frequency,
                        /* double attenuation */ attenuation,
                        /* int filter */ filter)
            {
                // Call init function
                initConfigurationDict();
            }

            TunerComponent::~TunerComponent()
            {
            }

            TunerComponent::TunerComponent(const TunerComponent& other) :
                ::LibCyberRadio::Driver::TunerComponent(other)
            {
            }

            TunerComponent& TunerComponent::operator=(const TunerComponent& other)
            {
                ::LibCyberRadio::Driver::TunerComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

            // OVERRIDE
            void TunerComponent::initConfigurationDict()
            {
                this->debug("[NDR472::TunerComponent::initConfigurationDict] Called\n");
                _config.clear();
                // Call the base-class version
                RadioComponent::initConfigurationDict();
                // Define tuner-specific keys
                _config["frequency"] = "";
                _config["attenuation"] = "";
                _config["timingAdj"] = "";
                this->debug("[NDR472::TunerComponent::initConfigurationDict] Returning\n");
            }

            // OVERRIDE
            void TunerComponent::updateConfigurationDict()
            {
                this->debug("[NDR472::TunerComponent::updateConfigurationDict] Called\n");
                RadioComponent::updateConfigurationDict();
                bool res;
                res = setConfigurationValueToDbl("frequency", _frequency);
                res = setConfigurationValueToDbl("attenuation", _attenuation);
                res = setConfigurationValueToInt("timingAdj", _timingAdj);
                //this->debug("[TunerComponent::updateConfigurationDict] Current configuration\n");
                //this->dumpConfiguration();
                this->debug("[NDR472::TunerComponent::updateConfigurationDict] Returning\n");
            }

            // OVERRIDE
            void TunerComponent::queryConfiguration()
            {
                this->debug("[NDR472::TunerComponent::queryConfiguration] Called\n");
                executeEnableQuery(_index, _enabled);
                executeFreqQuery(_index, _frequency);
                executeAttenQuery(_index, _attenuation);
                executeTimingAdjustmentQuery(_index, _timingAdj);
                updateConfigurationDict();
                this->debug("[NDR472::TunerComponent::queryConfiguration] Returning\n");
            }

            // OVERRIDE
            // On this radio, the query parameters are space-delimited, not comma-delimited.
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
                                " ");
                        // vec[0] = Index
                        // vec[1] = Powered state (0=off, 1=on)
                        enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                        ret = true;
                    }
                }
                return ret;

            }

            // OVERRIDE
            // On this radio, the query parameters are space-delimited, not comma-delimited.
            // Also, the radio appends "Mhz" to the returned frequency values.
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
                        std::string tmp = Pythonesque::Replace(rsp.front(), "FRQ ", "");
                        tmp = Pythonesque::Replace(tmp, "Mhz", "");
                        BasicStringList vec = Pythonesque::Split(tmp, " ");
                        // vec[0] = Index
                        // vec[1] = Frequency (MHz)
                        freq = boost::lexical_cast<int>(vec[1]) * _freqUnits;
                        ret = true;
                    }
                }
                return ret;
            }

            // OVERRIDE
            // On this radio, the query parameters are space-delimited, not comma-delimited.
            // Also, the radio appends "dB" to the returned attenuation values.
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
                        std::string tmp = Pythonesque::Replace(rsp.front(), "ATT ", "");
                        tmp = Pythonesque::Replace(tmp, "dB", "");
                        BasicStringList vec = Pythonesque::Split(tmp, " ");
                        // vec[0] = Index
                        // vec[1] = Atten (dB)
                        atten = boost::lexical_cast<double>(vec[1]);
                        ret = true;
                    }
                }
                return ret;
            }

            // OVERRIDE
            // Filters are neither gettable or settable on this radio
            bool TunerComponent::executeFilterQuery(int index, int& filter)
            {
                bool ret = false;
                return ret;
            }

            // OVERRIDE
            // On this radio, the query parameters are space-delimited, not comma-delimited.
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
                                " ");
                        // vec[0] = Index
                        // vec[1] = Timing adjustment
                        timingAdj = boost::lexical_cast<int>(vec[1]);
                        ret = true;
                    }
                }
                return ret;
            }

            // OVERRIDE
            // Filters are neither gettable or settable on this radio
            bool TunerComponent::executeFilterCommand(int index, int& filter)
            {
                bool ret = false;
                return ret;
            }

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio



