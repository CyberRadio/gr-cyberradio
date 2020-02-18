/***************************************************************************
 * \file VitaIfSpec.cpp
 * \brief Implements the VITA interface specification for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/VitaIfSpec.h"


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR472
        {

            VitaIfSpec::VitaIfSpec() :
                ::LibCyberRadio::Driver::VitaIfSpec(
                        /* int headerSizeWords */ 7,
                        /* int payloadSizeWords */ 288,
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

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio

