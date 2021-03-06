/***************************************************************************
 * \file VitaIfSpec.cpp
 * \brief Implements the VITA interface specification for the NDR308.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR308/VitaIfSpec.h"


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR308
        {

            VitaIfSpec::VitaIfSpec() :
                ::LibCyberRadio::Driver::VitaIfSpec(
                        /* int headerSizeWords */ 9,
                        /* int payloadSizeWords */ 1024,
                        /* int tailSizeWords */ 1,
                        /* const char* byteOrder */ "little",
                        /* bool iqSwapped */ false,
                        /* bool usesV491 */ true
                 )
            {
            }

            VitaIfSpec::~VitaIfSpec()
            {
            }

        } /* namespace NDR308 */

    } // namespace Driver

} // namespace LibCyberRadio

