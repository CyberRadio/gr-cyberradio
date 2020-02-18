/***************************************************************************
 * \file TunerComponent.h
 * \brief Defines the tuner interface for the NDR308.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_TUNERCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_TUNERCOMPONENT_H

#include "LibCyberRadio/Driver/TunerComponent.h"
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
             * \brief Tuner component class for the NDR308.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this tuner is enabled [Boolean/integer/string]
             * * "frequency": Tuned frequency (Hz) [double/string]
             * * "attenuation": Attenuation (dB) [double/string]
             * * "filter": Filter setting [integer/string]
             *
             */
            class TunerComponent : public ::LibCyberRadio::Driver::TunerComponent
            {
                public:
                    /**
                     * \brief Constructs a TunerComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param frequency Tuned frequency (Hz).
                     * \param attenuation Attenuation (dB).
                     * \param filter Filter setting.
                     */
                    TunerComponent(int index = 1,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             double frequency = 800e6,
                             double attenuation = 0.0,
                             int filter = 0);
                    /**
                     * \brief Destroys a TunerComponent object.
                     */
                    virtual ~TunerComponent();
                    /**
                     * \brief Copies a TunerComponent object.
                     * \param other The TunerComponent object to copy.
                     */
                    TunerComponent(const TunerComponent& other);
                    /**
                     * \brief Assignment operator for TunerComponent objects.
                     * \param other The TunerComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual TunerComponent& operator=(const TunerComponent& other);

            }; /* class TunerComponent */

        } /* namespace NDR308 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR308_TUNERCOMPONENT_H
