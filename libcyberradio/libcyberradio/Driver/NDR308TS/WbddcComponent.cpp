/***************************************************************************
 * \file WbddcComponent.cpp
 * \brief Defines the WBDDC interface for the NDR308-TS.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR308TS/WbddcComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR308TS
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
                        /* const std::string& name */ (boost::format("NDR308TS-WBDDC%02d") % \
                                index).str(),
                        /* int index */ index,
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* bool tunable */ false,
                        /* bool selectableSource */ false,
                        /* bool selectableDataPort */ true,
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
                _rateSet[0] = 61.44e6;
                _rateSet[1] = 30.72e6;
                _rateSet[2] = 15.36e6;
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

        } /* namespace NDR308TS */

    } // namespace Driver

} // namespace LibCyberRadio

