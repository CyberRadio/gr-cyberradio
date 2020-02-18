/***************************************************************************
 * \file TunerComponent.cpp
 * \brief Defines the tuner interface for the NDR810.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR810/TunerComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR810
        {

            TunerComponent::TunerComponent(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     double frequency,
                     double attenuation,
                     int filter) :
                ::LibCyberRadio::Driver::TunerComponent(
                        /* const std::string& name */ (boost::format("NDR810-TUNER%02d") % \
                                index).str(),
                        /* int index */ index,
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* double freqRangeMin */ 20e6,
                        /* double freqRangeMax */ 6000e6,
                        /* double freqRes */ 1e6,
                        /* double freqUnits */ 1e6,
                        /* double attRangeMin */ 0.0,
                        /* double attRangeMax */ 46.0,
                        /* double attRes */ 1.0,
                        /* bool agc */ false,
                        /* double frequency */ frequency,
                        /* double attenuation */ attenuation,
                        /* int filter */ filter)
            {
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

        } /* namespace NDR810 */

    } // namespace Driver

} // namespace LibCyberRadio



