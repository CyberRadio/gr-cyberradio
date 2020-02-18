/***************************************************************************
 * \file TransmitterComponent.cpp
 * \brief Defines the transmitter interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR651/CWToneGenComponent.h"
#include "LibCyberRadio/Driver/NDR651/TransmitterComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR651
        {
            TransmitterComponent::TransmitterComponent(
                    int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     double frequency,
                     double attenuation) :
                ::LibCyberRadio::Driver::TransmitterComponent(
                        /* const std::string& name */ ( boost::format("NDR651-TX%02d") % index ).str(),
                        /* int index */ index,
                        /* RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* double freqRangeMin */ 20e6,
                        /* double freqRangeMax */ 6000e6,
                        /* double freqRes */ 1e6,
                        /* double freqUnits */ 1e6,
                        /* double attRangeMin */ 0.0,
                        /* double attRangeMax */ 10.0,
                        /* double attRes */ 1.0,
                        /* int numToneGen */ 2,
                        /* int toneGenIndexBase */ 1,
                        /* double frequency */ frequency,
                        /* double attenuation */ attenuation )
            {
                initConfigurationDict();
                // Allocate CW tone generators
                for (int toneGen = _toneGenIndexBase; toneGen < _toneGenIndexBase + _numToneGen;
                        toneGen++)
                {
                    _cwToneGens[toneGen] = new CWToneGenComponent(
                            /* int index */ toneGen,
                            /* RadioHandler* parent */ parent,
                            /* bool debug */ debug,
                            /* int txIndex */ index,
                            /* double frequency */ 900e6,
                            /* double amplitude */ 0.0,
                            /* double phase */ 0.0,
                            /* double sweepStart */ 900e6,
                            /* double sweepStop */ 900e6,
                            /* double sweepStep */ 1.0,
                            /* double dwellTime */ 1000.0
                    );
                }
            }

            TransmitterComponent::~TransmitterComponent()
            {
            }

            TransmitterComponent::TransmitterComponent(const TransmitterComponent& other) :
                ::LibCyberRadio::Driver::TransmitterComponent(other)
            {
            }

            TransmitterComponent& TransmitterComponent::operator=(const TransmitterComponent& other)
            {
                ::LibCyberRadio::Driver::TransmitterComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } // namespace NDR651

    } // namespace Driver

} // namespace LibCyberRadio
