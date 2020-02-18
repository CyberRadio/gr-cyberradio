/***************************************************************************
 * \file SimpleIpSetup.h
 * \brief Defines the "simple" IP configuration interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_SIMPLEIPSETUP_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_SIMPLEIPSETUP_H

#include "LibCyberRadio/Driver/SimpleIpSetup.h"
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
         * \brief Provides programming elements for driving NDR472 radios.
         */
        namespace NDR472
        {

            /**
             * \brief Simple IP setup class for the NDR472.
             *
             * Configuration dictionary elements:
             * * "sourceIP": Source IP address [string]
             * * "sourceMAC": Source MAC address [string] [read-only]
             * * "destIP": Destination IP address [string]
             * * "destMAC": Destination MAC address [string]
             *
             */
            class SimpleIpSetup : public ::LibCyberRadio::Driver::SimpleIpSetup
            {
                public:
                    /**
                     * \brief Constructs a SimpleIpSetup object.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    object.
                     * \param debug Whether the object supports debug output.
                     * \param sourceIP Source IP address.
                     * \param destIP Destination IP address.
                     * \param destMAC Destination MAC address.
                     */
                    SimpleIpSetup(::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                            bool debug = false,
                            const std::string& sourceIP = "0.0.0.0",
                            const std::string& destIP = "0.0.0.0",
                            const std::string& destMAC = "00:00:00:00:00:00");
                    /**
                     * \brief Destroys a SimpleIpSetup object.
                     */
                    virtual ~SimpleIpSetup();
                    /**
                     * \brief Copies a SimpleIpSetup object.
                     * \param other The SimpleIpSetup object to copy.
                     */
                    SimpleIpSetup(const SimpleIpSetup& other);
                    /**
                     * \brief Assignment operator for SimpleIpSetup objects.
                     * \param other The SimpleIpSetup object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual SimpleIpSetup& operator=(const SimpleIpSetup& other);

            }; /* class SimpleIpSetup */

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_SIMPLEIPSETUP_H
