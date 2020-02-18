/***************************************************************************
 * \file RadioHandler.h
 * \brief Defines the radio handler interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_RADIOHANDLER_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_RADIOHANDLER_H

#include "LibCyberRadio/Driver/RadioHandler.h"


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
         * \brief Provides programming elements for driving NDR472 radios.
         */
        namespace NDR472
        {

            /**
             * \brief Radio handler class for the NDR472.
             *
             * \section Radio_NDR472 Radio
             *
             * This radio has the following settings:
             * * Configuration mode: 0 (off) or 1 (on)
             * * Reference mode:
             *   * 0: Internal 10MHz
             *   * 1: External 10MHz
             *   * 2: Internal GPS Disciplined 10MHz
             *   * 3: External 1PPS disciplined internal 10MHz
             *   * 3: External 1PPS disciplined internal 10MHz with control loop
             *       optimized for external GPS PPS
             * * Frequency normalization mode: 0 (off) or 1 (on)
             * * GPS enabled: 0 (off) or 1 (on)
             * * Reference tuning voltage value: 0-65565
             *
             * Configuration dictionary items:
             * * "configMode": Configuration mode [Boolean/integer/string]
             * * "referenceMode": Reference mode [integer/string]
             * * "freqNormalization": Whether frequency normalization is in effect
             *   [Boolean/integer/string]
             * * "gpsEnable": Whether GPS is enabled [Boolean/integer/string]
             * * "referenceTuningVoltage": Reference tuning voltage value [integer/string]
             *
             * \section Tuners_NDR472 Tuners
             *
             * The NDR472 has two tuners, indexed 1-2.
             * * Frequency range: 20.0 MHz - 3.0 GHz
             * * Attenuation range: 0.0 dB - 306.0 dB
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this tuner is enabled [Boolean/integer/string]
             * * "frequency": Tuned frequency (Hz) [double/string]
             * * "attenuation": Attenuation (dB) [double/string]
             *
             * \section WBDDCs_NDR472 WBDDCs
             *
             * The NDR472 has two WBDDCs, indexed 1-2.  Each WBDDC corresponds to the
             * tuner with the same index.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean/integer/string]
             * * "rateIndex": Rate index [integer/string]
             * * "udpDestination": UDP destination [integer/string]
             * * "vitaEnable": VITA 49 framing setting [integer/string]
             * * "streamId": VITA 49 streamId [integer/string]
             *
             * Rate indices:
             *
             * <table>
             * <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th><th>Sample Type</th></tr>
             * <tr><td>0</td><td>12800000.0</td><td>Complex</td></tr>
             * </table>
             *
             * \section WbddcGroups_NDR472 WBDDC Groups
             *
             * The NDR472 has two WBDDC groups, indexed 1-2.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
             * * "members": Comma-separated list of WBDDCs in this group [string]
             *
             * \section NBDDCs_NDR472 NBDDCs
             *
             * The NDR472 has no NBDDCs.  Methods that affect NBDDCs are meaningless on
             * this radio.
             *
             * \section NbddcGroups_NDR472 NBDDC Groups
             *
             * The NDR472 has no NBDDC groups.  Methods that affect NBDDC groupss are
             * meaningless on this radio.
             *
             * \section Transmitters_NDR472 Transmitters
             *
             * The NDR472 has no transmission capability.  Methods that affect
             * transmitters are meaningless on this radio.
             *
             * \section DUCs_NDR472 DUCs
             *
             * The NDR472 has no transmission capability.  Methods that affect
             * DUCs are meaningless on this radio.
             *
             * \section DataPorts_NDR472 Data Ports
             *
             * The NDR472 has no 10GigE data ports.
             *
             * \section VitaEnable_NDR472 VITA 49 Enabling Options for DDCs
             *
             * <table>
             * <tr><th>VITA Enable Option</th><th>Meaning</th></tr>
             * <tr><td>0</td><td>VITA-49 header disabled</td></tr>
             * <tr><td>1</td><td>VITA-49 header enabled, fractional timestamp in picoseconds</td></tr>
             * <tr><td>2</td><td>VITA-49 header disabled</td></tr>
             * <tr><td>3</td><td>VITA-49 header enabled, fractional timestamp in sample counts</td></tr>
             * </table>
             *
             */
            class RadioHandler : public ::LibCyberRadio::Driver::RadioHandler
            {
                public:
                    RadioHandler(bool debug = false);
                    virtual ~RadioHandler();
                    RadioHandler(const RadioHandler& other);
                    virtual RadioHandler& operator=(const RadioHandler& other);
                    // OVERRIDE
                    virtual void queryConfiguration();

                protected:
                    // OVERRIDE
                    virtual void initConfigurationDict();
                    // OVERRIDE
                    virtual bool queryVersionInfo();
                    // OVERRIDE
                    virtual bool executeQueryIDN(std::string& model,
                            std::string& serialNumber);
                    // OVERRIDE
                    virtual bool executeQueryVER(std::string& softwareVersion,
                            std::string& firmwareVersion,
                            std::string& referenceVersion,
                            std::string& firmwareDate);
                    // OVERRIDE
                    virtual bool executeQueryHREV(std::string& hardwareInfo);


            }; /* class RadioHandler */

        } /* namespace NDR472 */

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NDR472_RADIOHANDLER_H */
