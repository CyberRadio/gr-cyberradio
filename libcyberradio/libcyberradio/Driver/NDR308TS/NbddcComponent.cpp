/***************************************************************************
 * \file NbddcComponent.cpp
 * \brief Defines the NBDDC interface for the NDR308-TS.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR308TS/NbddcComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR308TS
        {

            NbddcComponent::NbddcComponent(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     int dataPort,
                     int rateIndex,
                     int udpDestination,
                     int vitaEnable,
                     int streamId,
                     double frequency,
                     int source) :
                ::LibCyberRadio::Driver::NbddcComponent(
                    /* const std::string& name */ (boost::format("NDR308TS-NBDDC%02d") % \
                            index).str(),
                    /* int index */ index,
                    /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                    /* bool debug */ debug,
                    /* bool nbddcCommandSetsFreq */ true,
                    /* bool nbddcCommandSetsSource */ false,
                    /* bool selectableDataPort */ true,
                    /* double freqRangeMin */ -25.6e6,
                    /* double freqRangeMax */ 25.6e6,
                    /* double freqRes */ 1.0,
                    /* double freqUnits */ 1.0,
                    /* int source */ source,
                    /* int dataPort */ dataPort,
                    /* double frequency */ frequency,
                    /* int rateIndex */ rateIndex,
                    /* int udpDestination */ udpDestination,
                    /* int vitaEnable */ vitaEnable,
                    /* unsigned int streamId */ streamId)
            {
                initConfigurationDict();
                // Set rate set
                _rateSet[0] = 1.92e6;
                _rateSet[1] = 960e3;
                _rateSet[2] = 480e3;
                _rateSet[3] = 180e3;
                _rateSet[4] = 60e3;
                _rateSet[5] = 30e3;
                _rateSet[6] = 15e3;
            }

            NbddcComponent::~NbddcComponent()
            {
            }

            NbddcComponent::NbddcComponent(const NbddcComponent& other) :
                ::LibCyberRadio::Driver::NbddcComponent(other)
            {
            }

            NbddcComponent& NbddcComponent::operator=(const NbddcComponent& other)
            {
                ::LibCyberRadio::Driver::NbddcComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } /* namespace NDR308TS */

    } // namespace Driver

} // namespace LibCyberRadio

