/***************************************************************************
 * \file NbddcGroupComponent.h
 * \brief Defines the NBDDC group interface for the NDR308.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_NBDDCGROUPCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_NBDDCGROUPCOMPONENT_H

#include "LibCyberRadio/Driver/NbddcGroupComponent.h"
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
         * \brief Provides programming elements for driving NDR308 radios.
         */
        namespace NDR308
        {

            /**
             * \brief NBDDC group component class for the NDR308.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
             * * "members": Comma-separated list of NBDDCs in this group [string]
             */
            class NbddcGroupComponent : public ::LibCyberRadio::Driver::NbddcGroupComponent
            {
                public:
                    /**
                     * \brief Constructs a NbddcGroupComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     */
                    NbddcGroupComponent(int index = 1,
                                        ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                                        bool debug = false);
                    /**
                     * \brief Destroys a NbddcGroupComponent object.
                     */
                    virtual ~NbddcGroupComponent();
                    /**
                     * \brief Copies a NbddcGroupComponent object.
                     * \param other The NbddcGroupComponent object to copy.
                     */
                    NbddcGroupComponent(const NbddcGroupComponent& other);
                    /**
                     * \brief Assignment operator for NbddcGroupComponent objects.
                     * \param other The NbddcComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual NbddcGroupComponent& operator=(const NbddcGroupComponent& other);

            }; // class NbddcGroupComponent

        } /* namespace NDR308 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_NBDDCGROUPCOMPONENT_H
