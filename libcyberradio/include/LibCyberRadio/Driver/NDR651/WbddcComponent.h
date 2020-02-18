/***************************************************************************
 * \file WbddcComponent.h
 * \brief Defines the WBDDC interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCCOMPONENT_H

#include "LibCyberRadio/Driver/WbddcComponent.h"
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
             * \brief WBDDC component class for the NDR651.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean]
             * * "rateIndex": Rate index [integer]
             * * "udpDestination": UDP destination [integer, meaning varies by radio]
             * * "vitaEnable": VITA 49 framing setting [integer, meaning varies by radio]
             * * "streamId": VITA 49 streamId [integer]
             * * "dataPort": Data port index [integer]
             *
             */
            class WbddcComponent : public ::LibCyberRadio::Driver::WbddcComponent
            {
                public:
                    /**
                     * \brief Constructs a WbddcComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param dataPort Data port used by this WBDDC.
                     * \param rateIndex WBDDC rate index.  This should be one of the rate
                     *    indices in the WBDDC's rate set.
                     * \param udpDestination UDP destination index.
                     * \param vitaEnable VITA 49 framing setting (0-3).
                     * \param streamId VITA 49 stream ID.
                     */
                    WbddcComponent(int index = 1,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             int dataPort = 1,
                             int rateIndex = 0,
                             int udpDestination = 0,
                             int vitaEnable = 0,
                             int streamId = 0);
                    /**
                     * \brief Destroys a WbddcComponent object.
                     */
                    virtual ~WbddcComponent();
                    /**
                     * \brief Copies a WbddcComponent object.
                     * \param other The WbddcComponent object to copy.
                     */
                    WbddcComponent(const WbddcComponent& other);
                    /**
                     * \brief Assignment operator for WbddcComponent objects.
                     * \param other The WbddcComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual WbddcComponent& operator=(const WbddcComponent& other);

            }; // class WbddcComponent

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_WBDDCCOMPONENT_H
