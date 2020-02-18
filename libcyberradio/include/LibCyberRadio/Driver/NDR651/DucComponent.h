/***************************************************************************
 * \file DucComponent.h
 * \brief Defines the DUC interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DUCCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DUCCOMPONENT_H

#include "LibCyberRadio/Driver/DucComponent.h"
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
             * \brief DUC component class for the NDR651.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DUC is enabled [Boolean/integer/string]
             * * "dataPort": Data port index [integer/string]
             * * "frequency": Tuned frequency (Hz) [double/string]
             * * "attenuation": Attenuation (dB) [double/string]
             * * "rateIndex": Rate index [integer/string]
             * * "txChannels": Transmit channel bitmap [integer/string]
             * * "mode": DUC mode [integer/string]
             * * "streamId": VITA stream ID [integer/string]
             * * "filename": Snapshot file name [string]
             * * "startSample": Start sample number [integer/string]
             * * "samples": Number of samples [integer/string]
             * * "singlePlayback": Whether or not to do a single playback
             *   [Boolean/integer/string]
             * * "pauseUntilEnabled": Whether or not to pause snapshot until enabled
             *   [Boolean/integer/string]
             *
             */
            class DucComponent : public ::LibCyberRadio::Driver::DucComponent
            {
                public:
                    /**
                     * \brief Constructs a DucComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param dataPort Data port used by this DUC.  Setting this to 0 stops
                     *    streaming.
                     * \param frequency Tuned frequency (Hz).
                     * \param attenuation Attenuation (dB).
                     * \param rateIndex DUC rate index.  This should be one of the rate
                     *    indices in the DUC's rate set.
                     * \param txChannels Bitmap indicating which transmitters output the
                     *    signal from this DUC.  Setting a bit position to 1 enables transmit
                     *    on the associated transmitter. The LSB corresponds to TX 1, and each
                     *    succeeding bit corresponds to the other transmitters.
                     * \param mode DUC mode. Either 0 (streaming mode) or 1 (playback mode).
                     * \param streamId VITA 49 stream ID.
                     */
                    DucComponent(int index = 1,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             int dataPort = 0,
                             double frequency = 0.0,
                             double attenuation = 0.0,
                             int rateIndex = 0,
                             int txChannels = 0,
                             int mode = 0,
                             int streamId = 0);
                    /**
                     * \brief Destroys a DucComponent object.
                     */
                    virtual ~DucComponent();
                    /**
                     * \brief Copies a DucComponent object.
                     * \param other The DucComponent object to copy.
                     */
                    DucComponent(const DucComponent& other);
                    /**
                     * \brief Assignment operator for DucComponent objects.
                     * \param other The DucComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual DucComponent& operator=(const DucComponent& other);

            }; // class DucComponent

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR651_DUCCOMPONENT_H
