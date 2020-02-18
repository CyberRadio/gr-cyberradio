/***************************************************************************
 * \file DataPort.h
 * \brief Defines the 10GigE data port interface for an NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DATAPORT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DATAPORT_H

#include "LibCyberRadio/Driver/DataPort.h"


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
             * \brief 10GigE data port class.
             *
             * A radio handler object maintains one DataPort object for each
             * 10GigE data port on the radio.
             *
             */
            class DataPort : public ::LibCyberRadio::Driver::DataPort
            {
                public:
                    /**
                     * \brief Constructs a DataPort object.
                     * \param index The index number of this object.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    object.
                     * \param debug Whether the object supports debug output.
                     * \param sourceIP Source IP address.
                     */
                    DataPort(int index = 0,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             const std::string& sourceIP = "0.0.0.0");
                    /**
                     * \brief Destroys a DataPort object.
                     */
                    virtual ~DataPort();
                    /**
                     * \brief Copies a DataPort object.
                     * \param other The DataPort object to copy.
                     */
                    DataPort(const DataPort& other);
                    /**
                     * \brief Assignment operator for DataPort objects.
                     * \param other The DataPort object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual DataPort& operator=(const DataPort& other);

            }; /* class DataPort */

        } /* namespace NDR651 */


    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DATAPORT_H */
