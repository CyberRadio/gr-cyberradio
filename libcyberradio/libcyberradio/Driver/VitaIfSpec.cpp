/***************************************************************************
 * \file VitaIfSpec.cpp
 * \brief Defines the VITA interface specification for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/VitaIfSpec.h"

/**
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /**
     * \brief Provides programming elements for driving CRS NDR-class radios.
     */
    namespace Driver
    {
        VitaIfSpec::VitaIfSpec(int headerSizeWords,
                int payloadSizeWords,
                int tailSizeWords,
                const char* byteOrder,
                bool iqSwapped,
                bool usesV491) :
            headerSizeWords(headerSizeWords),
            payloadSizeWords(payloadSizeWords),
            tailSizeWords(tailSizeWords),
            byteOrder(byteOrder),
            iqSwapped(iqSwapped),
            usesV491(usesV491)
        {
        }

        VitaIfSpec::~VitaIfSpec()
        {
        }

        VitaIfSpec::VitaIfSpec(const VitaIfSpec& other) :
            headerSizeWords(other.headerSizeWords),
            payloadSizeWords(other.payloadSizeWords),
            tailSizeWords(other.tailSizeWords),
            byteOrder(other.byteOrder),
            iqSwapped(other.iqSwapped),
            usesV491(other.usesV491)
        {
        }

        VitaIfSpec& VitaIfSpec::operator=(const VitaIfSpec& other)
        {
            if ( this != &other )
            {
                headerSizeWords = other.headerSizeWords;
                payloadSizeWords = other.payloadSizeWords;
                tailSizeWords = other.tailSizeWords;
                byteOrder = other.byteOrder;
                iqSwapped = other.iqSwapped;
                usesV491 = other.usesV491;
            }
            return *this;
        }

    } /* namespace Driver */

} /* namespace LibCyberRadio */

