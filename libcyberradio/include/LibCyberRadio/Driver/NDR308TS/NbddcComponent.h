/***************************************************************************
 * \file NbddcComponent.h
 * \brief Defines the NBDDC interface for the NDR308-TS.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_NBDDCCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_NBDDCCOMPONENT_H

#include "LibCyberRadio/Driver/NbddcComponent.h"
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
         * \brief Provides programming elements for driving NDR308-TS radios.
         */
        namespace NDR308TS
        {

            /**
             * \brief NBDDC component class for the NDR308-TS.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean]
             * * "rateIndex": Rate index [integer]
             * * "udpDestination": UDP destination [integer, meaning varies by radio]
             * * "vitaEnable": VITA 49 framing setting [integer, meaning varies by radio]
             * * "streamId": VITA 49 streamId [integer]
             * * "frequency": Tuned frequency (Hz) [double]
             * * "source": Source tuner index [integer]
             * * "dataPort": Data port index [integer]
             *
             */
            class NbddcComponent : public ::LibCyberRadio::Driver::NbddcComponent
            {
                public:
                    /**
                     * \brief Constructs a NbddcComponent object.
                     * \param index The index number of this component.
                     * \param parent A pointer to the RadioHandler object that "owns" this
                     *    component.
                     * \param debug Whether the component supports debug output.
                     * \param dataPort Data port used by this NBDDC.
                     * \param rateIndex NBDDC rate index.  This should be one of the rate
                     *    indices in the NBDDC's rate set.
                     * \param udpDestination UDP destination index.
                     * \param vitaEnable VITA 49 framing setting (0-3).
                     * \param streamId VITA 49 stream ID.
                     * \param frequency Tuned frequency (Hz).
                     * \param source Source (tuner) index supplying the signal for this NBDDC.
                     */
                    NbddcComponent(int index = 1,
                            ::LibCyberRadio::Driver::RadioHandler* parent = NULL,
                             bool debug = false,
                             int dataPort = 1,
                             int rateIndex = 0,
                             int udpDestination = 0,
                             int vitaEnable = 0,
                             int streamId = 0,
                             double frequency = 0.0,
                             int source = 1);
                    /**
                     * \brief Destroys a NbddcComponent object.
                     */
                    virtual ~NbddcComponent();
                    /**
                     * \brief Copies a NbddcComponent object.
                     * \param other The NbddcComponent object to copy.
                     */
                    NbddcComponent(const NbddcComponent& other);
                    /**
                     * \brief Assignment operator for NbddcComponent objects.
                     * \param other The NbddcComponent object to copy.
                     * \returns A reference to the assigned object.
                     */
                    virtual NbddcComponent& operator=(const NbddcComponent& other);

            }; /* class NbddcComponent */

        } /* namespace NDR308TS */

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_NBDDCCOMPONENT_H
