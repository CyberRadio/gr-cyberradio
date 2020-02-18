/***************************************************************************
 * \file VitaIfSpec.h
 * \brief Defines the VITA interface specification for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_VITAIFSPEC_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_VITAIFSPEC_H

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

        /**
         * \brief Provides programming elements for driving NDR651 radios.
         */
        namespace NDR651
        {

            /**
             * \brief VITA interface specification for the NDR651.
             */
            class VitaIfSpec : public ::LibCyberRadio::Driver::VitaIfSpec
            {
                public:
                    VitaIfSpec();
                    virtual ~VitaIfSpec();
            };

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_VITAIFSPEC_H */

