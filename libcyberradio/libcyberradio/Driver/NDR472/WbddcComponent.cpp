/***************************************************************************
 * \file WbddcComponent.cpp
 * \brief Defines the WBDDC interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/WbddcComponent.h"
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

            WbddcComponent::WbddcComponent(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     int dataPort,
                     int rateIndex,
                     int udpDestination,
                     int vitaEnable,
                     int streamId) :
                ::LibCyberRadio::Driver::WbddcComponent(
                        /* const std::string& name */ (boost::format("NDR472-WBDDC%02d") % \
                                index).str(),
                        /* int index */ index,
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* bool tunable */ false,
                        /* bool selectableSource */ false,
                        /* bool selectableDataPort */ false,
                        /* bool agc */ false,
                        /* double freqRangeMin */ 0.0,
                        /* double freqRangeMax */ 0.0,
                        /* double freqRes */ 1e6,
                        /* double freqUnits */ 1e6,
                        /* int source */ index,
                        /* int dataPort */ dataPort,
                        /* double frequency */ 0.0,
                        /* int rateIndex */ rateIndex,
                        /* int udpDestination */ udpDestination,
                        /* int vitaEnable */ vitaEnable,
                        /* unsigned int streamId */ streamId)
            {
                initConfigurationDict();
                // Set rate set
                _rateSet[0] = 12.8e6;
            }

            WbddcComponent::~WbddcComponent()
            {
            }

            WbddcComponent::WbddcComponent(const WbddcComponent& other) :
                ::LibCyberRadio::Driver::WbddcComponent(other)
            {
            }

            WbddcComponent& WbddcComponent::operator=(const WbddcComponent& other)
            {
                ::LibCyberRadio::Driver::WbddcComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

            // OVERRIDE
            // This radio uses spaces to delimit command paramters rather than commas.
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
                                " ");
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

            // OVERRIDE
            // This radio doesn't have data ports.
            bool WbddcComponent::executeDataPortQuery(int index, int& dataPort)
            {
                bool ret = false;
                return ret;
            }

            // OVERRIDE
            // This radio doesn't have data ports.
            bool WbddcComponent::executeDataPortCommand(int index, int& dataPort)
            {
                bool ret = false;
                return ret;
            }

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio

