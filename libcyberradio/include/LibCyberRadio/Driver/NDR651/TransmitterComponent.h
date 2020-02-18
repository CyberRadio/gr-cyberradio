/***************************************************************************
 * \file TransmitterComponent.h
 * \brief Defines the transmitter interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_TRANSMITTERCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_TRANSMITTERCOMPONENT_H

#include "LibCyberRadio/Driver/TransmitterComponent.h"
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
             * \brief Transmitter component class for the NDR651.
             *
             * A radio handler object maintains one transmitter component object per
             * transmitter on the radio.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this transmitter is enabled [Boolean/integer/string]
             * * "frequency": Tuned frequency (Hz) [double]
             * * "attenuation": Attenuation (dB) [double]
             *
             */
            class TransmitterComponent : public ::LibCyberRadio::Driver::TransmitterComponent
            {
                public:
                    /**
                     * \brief Constructs a TransmitterComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param frequency Transmitter center frequency (Hz).
                     * \param attenuation Transmitter attenuation (dB).
                     */
                    TransmitterComponent(int index = 1,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             double frequency = 900e6,
                             double attenuation = 0.0);
                    /**
                     * \brief Destroys a TransmitterComponent object.
                     */
                    virtual ~TransmitterComponent();
                    /**
                     * \brief Copies a TransmitterComponent object.
                     * \param other The TransmitterComponent object to copy.
                     */
                    TransmitterComponent(const TransmitterComponent& other);
                    /**
                     * \brief Assignment operator for TransmitterComponent objects.
                     * \param other The TransmitterComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual TransmitterComponent& operator=(const TransmitterComponent& other);

            }; // class TransmitterComponent

        } // namespace NDR651

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_TRANSMITTERCOMPONENT_H
