/***************************************************************************
 * \file VitaIfSpec.h
 * \brief Defines the VITA interface specification for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_VITAIFSPEC_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_VITAIFSPEC_H

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
         * \brief Class that defines the VITA interface specification
         *    for an NDR-class radio.
         *
         * The VITA interface specification indicates how the radio
         * formats its VITA 49 packets.  Each radio must define its
         * own instance of this class so that accessor methods can
         * report the parameters of this interface to clients.
         */
        class VitaIfSpec
        {
            public:
                VitaIfSpec(int headerSizeWords = 0,
                        int payloadSizeWords = 0,
                        int tailSizeWords = 0,
                        const char* byteOrder = "little",
                        bool iqSwapped = false,
                        bool usesV491 = true);
                virtual ~VitaIfSpec();
                VitaIfSpec(const VitaIfSpec& other);
                VitaIfSpec& operator=(const VitaIfSpec& other);

            public:
                //! Size of the VITA 49 header, in 32-byte words
                int headerSizeWords;
                //! Size of the payload, in 32-byte words
                int payloadSizeWords;
                //! Size of the VITA 49 "tail", in 32-byte words
                int tailSizeWords;
                //! Byte order used by the radio.
                const char* byteOrder;
                //! Whether the I/Q data in the payload are swapped
                bool iqSwapped;
                //! Whether the data packets use VITA 49.1 framing
                bool usesV491;

        };

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_VITAIFSPEC_H */
