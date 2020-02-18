/***************************************************************************
 * \file DucComponent.cpp
 * \brief Defines the DUC interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR651/DucComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR651
        {

            DucComponent::DucComponent(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     int dataPort,
                     double frequency,
                     double attenuation,
                     int rateIndex,
                     int txChannels,
                     int mode,
                     int streamId) :
                ::LibCyberRadio::Driver::DucComponent(
                        /* const std::string& name */ (boost::format("NDR651-DUC%02d") % \
                                index).str(),
                        /* int index */ index,
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* double freqRangeMin */ -25.6e6,
                        /* double freqRangeMax */ 25.6e6,
                        /* double freqRes */ 1.0,
                        /* double freqUnits */ 1.0,
                        /* double attRangeMin */ -6.0,
                        /* double attRangeMax */ 60.0,
                        /* double attRes */ 0.1,
                        /* int dataPort */ dataPort,
                        /* double frequency */ frequency,
                        /* double attenuation */ attenuation,
                        /* int rateIndex */ rateIndex,
                        /* int txChannels */ txChannels,
                        /* int mode */ mode,
                        /* unsigned int streamId */ streamId)
            {
                initConfigurationDict();
                // Set rate set
                _rateSet[0] = 102.4e6;
                _rateSet[1] = 51.2e6;
                _rateSet[2] = 25.6e6;
                _rateSet[3] = 12.8e6;
                _rateSet[4] = 6.4e6;
                _rateSet[5] = 3.2e6;
                _rateSet[6] = 1.6e6;
                _rateSet[7] = 800e3;
                _rateSet[8] = 400e3;
                _rateSet[9] = 200e3;
                _rateSet[10] = 100e3;
                _rateSet[11] = 50e3;
                _rateSet[12] = 25e3;
                _rateSet[13] = 12.5e3;
                _rateSet[16] = 13e6 / 48;
                _rateSet[20] = 5.6e6;
            }

            DucComponent::~DucComponent()
            {
            }

            DucComponent::DucComponent(const DucComponent& other) :
                ::LibCyberRadio::Driver::DucComponent(other)
            {
            }

            DucComponent& DucComponent::operator=(const DucComponent& other)
            {
                ::LibCyberRadio::Driver::DucComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio

