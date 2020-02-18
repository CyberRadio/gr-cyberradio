/***************************************************************************
 * \file CWToneGenComponent.h
 * \brief Defines the Continuous-wave (CW) tone generator interface
 *    for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_CWTONEGENCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_CWTONEGENCOMPONENT_H

#include "LibCyberRadio/Driver/CWToneGenComponent.h"
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
             * \brief Continuous-wave (CW) tone generator component class for the NDR651.
             *
             * A radio handler object maintains one CW tone generator component
             * object per tone generator on the radio.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this component is enabled [Boolean]
             */
            class CWToneGenComponent : public ::LibCyberRadio::Driver::CWToneGenComponent
            {
                public:
                    /**
                     * \brief Constructs a CWToneGenComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param txIndex Transmitter index associated with this component.
                     * \param frequency Constant frequency (Hz).
                     * \param amplitude Signal amplitude (scale units).
                     * \param phase Signal phase (degrees).
                     * \param sweepStart Frequency sweep start (Hz).
                     * \param sweepStop Frequency sweep stop (Hz).
                     * \param sweepStep Frequency sweep step (Hz).
                     * \param dwellTime Dwell time (ADC samples).
                     */
                    CWToneGenComponent(int index = 0,
                            RadioHandler* parent = NULL,
                            bool debug = false,
                            int txIndex = 0,
                            double frequency = 0.0,
                            double amplitude = 0.0,
                            double phase = 0.0,
                            double sweepStart = 0.0,
                            double sweepStop = 0.0,
                            double sweepStep = 0.0,
                            double dwellTime = 0.0
                    );
                    /**
                     * \brief Destroys a CWToneGenComponent object.
                     */
                    virtual ~CWToneGenComponent();
                    /**
                     * \brief Copies a CWToneGenComponent object.
                     * \param other The CWToneGenComponent object to copy.
                     */
                    CWToneGenComponent(const CWToneGenComponent& other);
                    /**
                     * \brief Assignment operator for CWToneGenComponent objects.
                     * \param other The CWToneGenComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual CWToneGenComponent& operator=(const CWToneGenComponent& other);

            }; // class CWToneGenComponent

        } // namespace NDR651

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_CWTONEGENCOMPONENT_H
