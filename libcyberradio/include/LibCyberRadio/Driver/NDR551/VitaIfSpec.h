/***************************************************************************
 * \file VitaIfSpec.h
 * \brief Defines the VITA interface specification for the NDR308.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR551_VITAIFSPEC_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR551_VITAIFSPEC_H

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
         * \brief Provides programming elements for driving NDR308 radios.
         */
        namespace NDR551
        {

            /**
             * \brief VITA interface specification for the NDR308.
             */
            class VitaIfSpec : public ::LibCyberRadio::Driver::VitaIfSpec
            {
                public:
                    VitaIfSpec();
                    virtual ~VitaIfSpec();
            };

        } /* namespace NDR308 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_VITAIFSPEC_H */

