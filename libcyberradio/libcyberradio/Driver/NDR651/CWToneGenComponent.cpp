/***************************************************************************
 * \file CWToneGenComponent.cpp
 * \brief Defines the Continuous-wave (CW) tone generator interface
 *    for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR651/CWToneGenComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR651
        {
            CWToneGenComponent::CWToneGenComponent(
                    int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     int txIndex,
                     double frequency,
                     double amplitude,
                     double phase,
                     double sweepStart,
                     double sweepStop,
                     double sweepStep,
                     double dwellTime ) :
                ::LibCyberRadio::Driver::CWToneGenComponent(
                        /* const std::string& name */ ( boost::format("NDR651-TX%02d-CW%02d") % txIndex % index ).str(),
                        /* int index */ index,
                        /* RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* int txIndex */ txIndex,
                        /* double freqRangeMin */ -512e5,
                        /* double freqRangeMax */ 512e5,
                        /* double freqRes */ 1.0,
                        /* double freqUnits */ 1.0,
                        /* double ampRangeMin */ 0.0,
                        /* double ampRangeMax */ 65535.0,
                        /* double ampRes */ 1.0,
                        /* double phaseRangeMin */ -180.0,
                        /* double phaseRangeMax */ 180.0,
                        /* double phaseRes */ 1.0,
                        /* double sweepStartRangeMin */ -512e5,
                        /* double sweepStartRangeMax */ 512e5,
                        /* double sweepStartRes */ 1.0,
                        /* double sweepStopRangeMin */ -512e5,
                        /* double sweepStopRangeMax */ 512e5,
                        /* double sweepStopRes */ 1.0,
                        /* double sweepStepRangeMin */ -512e5,
                        /* double sweepStepRangeMax */ 512e5,
                        /* double sweepStepRes */ 1.0,
                        /* double dwellTimeRangeMin */ 0.0,
                        /* double dwellTimeRangeMax */ (double)0xFFFFFFFF,
                        /* double dwellTimeRes */ 1.0,
                        /* double frequency */ frequency,
                        /* double amplitude */ amplitude,
                        /* double phase */ phase,
                        /* double sweepStart */ sweepStart,
                        /* double sweepStop */ sweepStop,
                        /* double sweepStep */ sweepStep,
                        /* double dwellTime */ dwellTime )
            {
                initConfigurationDict();
            }

            CWToneGenComponent::~CWToneGenComponent()
            {
            }

            CWToneGenComponent::CWToneGenComponent(const CWToneGenComponent& other) :
                ::LibCyberRadio::Driver::CWToneGenComponent(other)
            {
            }

            CWToneGenComponent& CWToneGenComponent::operator=(const CWToneGenComponent& other)
            {
                ::LibCyberRadio::Driver::CWToneGenComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } // namespace NDR651

    } // namespace Driver

} // namespace LibCyberRadio
