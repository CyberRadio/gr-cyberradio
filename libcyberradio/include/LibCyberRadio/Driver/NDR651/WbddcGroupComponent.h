/***************************************************************************
 * \file WbddcGroupComponent.h
 * \brief Defines the WBDDC group interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCGROUPCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCGROUPCOMPONENT_H

#include "LibCyberRadio/Driver/WbddcGroupComponent.h"
#include "LibCyberRadio/Common/BasicDict.h"
#include <string>


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
        // Forward declaration for RadioHandler
        class RadioHandler;

        /**
         * \brief Provides programming elements for driving NDR651 radios.
         */
        namespace NDR651
        {

            /**
             * \brief WBDDC group component class for the NDR651.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean]
             * * "members": Comma-separated list of group members [string]
             */
            class WbddcGroupComponent : public ::LibCyberRadio::Driver::WbddcGroupComponent
            {
                public:
                    /**
                     * \brief Constructs a WbddcGroupComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     */
                    WbddcGroupComponent(int index = 1,
                                        ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                                        bool debug = false);
                    /**
                     * \brief Destroys a WbddcGroupComponent object.
                     */
                    virtual ~WbddcGroupComponent();
                    /**
                     * \brief Copies a WbddcGroupComponent object.
                     * \param other The WbddcGroupComponent object to copy.
                     */
                    WbddcGroupComponent(const WbddcGroupComponent& other);
                    /**
                     * \brief Assignment operator for WbddcGroupComponent objects.
                     * \param other The WbddcComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual WbddcGroupComponent& operator=(const WbddcGroupComponent& other);

            }; // class WbddcGroupComponent

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCGROUPCOMPONENT_H
