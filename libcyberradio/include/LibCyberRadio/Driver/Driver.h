/***************************************************************************
 * \file Driver.h
 * \brief Main entry point for the C++ CyberRadio Driver.
 * \author DA
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_DRIVER_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_DRIVER_H

#include "LibCyberRadio/Driver/RadioHandler.h"
#include <memory>


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
         * \brief A pointer to a radio handler object.
         */
        typedef std::shared_ptr<RadioHandler> RadioHandlerPtr;

        /**
         * \brief Factory method for returning a radio handler object for
         *     a given radio.
         *
         * The pointer returned by this object refers to an object that
         * supports the standard RadioHandler interface.  However, certain
         * radios may not support all features of this interface.  Refer to
         * the radio's specific documentation for details.
         *
         * This method supports automatically connecting to the specified
         * radio device.  Setting \c device to the device name (network
         * host name/IP address or serial device) -- and \c devicePort
         * if necessary -- activates this functionality.
         *
         * \param nameString A name string identifying the radio type.
         * \param device Device name [string].  This is either a host name/
         *     IP address (for network devices) or a serial device name (for
         *     USB-connected radios).
         * \param devicePort Device port [integer].  This is either a
         *     port number (for network devices) or a serial baud rate (for
         *     USB-connected radios).  Setting this to -1 means to use the
         *     default for the radio handler.
         * \param debug Whether or not the radio handler creates debug output
         *     [Boolean].
         *
         * \returns A shared pointer referring to the radio handler object.
         *    Returns NULL if an appropriate radio handler cannot be
         *    determined.
         */
        RadioHandlerPtr getRadioObject(
                    const std::string& nameString,
                    const std::string& device = "",
                    int devicePort = -1,
                    bool debug = false
                );

    } // namespace Driver

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_DRIVER_H */
