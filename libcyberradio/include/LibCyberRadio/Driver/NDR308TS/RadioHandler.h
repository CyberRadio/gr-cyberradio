/***************************************************************************
 * \file RadioHandler.h
 * \brief Defines the radio handler interface for the NDR308-TS.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_RADIOHANDLER_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_RADIOHANDLER_H

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
         * \brief Provides programming elements for driving NDR308-TS radios.
         */
        namespace NDR308TS
        {

            /**
             * \brief Radio handler class for the NDR308-TS.
             *
             * \section Radio_NDR308TS Radio
             *
             * This radio has the following settings:
             * * Calibration frequency: 20.0 MHz - 6.0 GHz
             * * Configuration mode: 0 (off) or 1 (on)
             * * Reference mode:
             *   * 0: Internal 10MHz
             *   * 1: External 10MHz
             *   * 2: Internal GPS Disciplined internal 10MHz
             *   * 3: External 1PPS
             *   * 4: External 1PPS pass-through
             *   * 5: External 10MHz and 1PPS
             * * Reference bypass mode: 0 (internal) or 1 (external)
             * * Frequency normalization mode: 0 (off) or 1 (on)
             * * GPS enabled: 0 (off) or 1 (on)
             * * Reference tuning voltage value: 0-65565
             *
             * Configuration dictionary items:
             * * "calibFrequency": Calibration frequency, in MHz [double/string]
             * * "configMode": Configuration mode [Boolean/integer/string]
             * * "referenceMode": Reference mode [integer/string]
             * * "bypassMode": Reference bypass mode [integer/string]
             * * "freqNormalization": Whether frequency normalization is in effect
             *   [Boolean/integer/string]
             * * "gpsEnable": Whether GPS is enabled [Boolean/integer/string]
             * * "referenceTuningVoltage": Reference tuning voltage value [integer/string]
             *
             * \section Tuners_NDR308TS Tuners
             *
             * The NDR308-TS has eight tuners, indexed 1-8.
             * * Frequency range: 20.0 MHz - 6.0 GHz
             * * Attenuation range: 0.0 dB - 46.0 dB
             * * Filter settings: 0 (LC), 1 (SAW)
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this tuner is enabled [Boolean/integer/string]
             * * "frequency": Tuned frequency (Hz) [double/string]
             * * "attenuation": Attenuation (dB) [double/string]
             * * "filter": Filter setting [integer/string]
             *
             * \section WBDDCs_NDR308TS WBDDCs
             *
             * The NDR308-TS has eight WBDDCs, indexed 1-8.  Each WBDDC corresponds to the
             * tuner with the same index.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean/integer/string]
             * * "rateIndex": Rate index [integer/string]
             * * "udpDestination": UDP destination [integer/string]
             * * "vitaEnable": VITA 49 framing setting [integer/string]
             * * "streamId": VITA 49 streamId [integer/string]
             * * "dataPort": Data port index [integer/string]
             *
             * Rate indices:
             *
             * <table>
             * <tr><th>Rate Index</th><th>WBDDC Rate (samples per second)</th><th>Sample Type</th></tr>
             * <tr><td>0</td><td>61440000.0</td><td>Complex</td></tr>
             * <tr><td>1</td><td>30720000.0</td><td>Complex</td></tr>
             * <tr><td>2</td><td>15360000.0</td><td>Complex</td></tr>
             * </table>
             *
             * \section WbddcGroups_NDR308TS WBDDC Groups
             *
             * The NDR308-TS has four WBDDC groups, indexed 1-4.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
             * * "members": Comma-separated list of WBDDCs in this group [string]
             *
             * \section NBDDCs_NDR308TS NBDDCs
             *
             * The NDR308-TS has 32 NBDDCs, indexed 1-32.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC is enabled [Boolean/integer/string]
             * * "rateIndex": Rate index [integer/string]
             * * "udpDestination": UDP destination [integer/string]
             * * "vitaEnable": VITA 49 framing setting [integer/string]
             * * "streamId": VITA 49 streamId [integer/string]
             * * "frequency": Tuned frequency (Hz) [double/string]
             * * "source": Source tuner index [integer/string]
             * * "dataPort": Data port index [integer/string]
             *
             * Rate indices:
             *
             * <table>
             * <tr><th>Rate Index</th><th>NBDDC Rate (samples per second)</th><th>Sample Type</th></tr>
             * <tr><td>0</td><td>1920000.0</td><td>Complex</td></tr>
             * <tr><td>1</td><td>960000.0</td><td>Complex</td></tr>
             * <tr><td>2</td><td>480000.0</td><td>Complex</td></tr>
             * <tr><td>3</td><td>180000.0</td><td>Complex</td></tr>
             * <tr><td>4</td><td>60000.0</td><td>Complex</td></tr>
             * <tr><td>5</td><td>30000.0</td><td>Complex</td></tr>
             * <tr><td>6</td><td>15000.0</td><td>Complex</td></tr>
             * </table>
             *
             * \section NbddcGroups_NDR308TS NBDDC Groups
             *
             * The NDR308-TS has eight NBDDC groups, indexed 1-8.
             *
             * Configuration dictionary elements:
             * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
             * * "members": Comma-separated list of NBDDCs in this group [string]
             *
             * \section Transmitters_NDR308TS Transmitters
             *
             * The NDR308-TS has no transmission capability.  Methods that affect
             * transmitters are meaningless on this radio.
             *
             * \section DUCs_NDR308TS DUCs
             *
             * The NDR308-TS has no transmission capability.  Methods that affect
             * DUCs are meaningless on this radio.
             *
             * \section DataPorts_NDR308TS Data Ports
             *
             * The NDR308-TS has two 10GigE data ports, indexed 1-2.
             *
             * Configuration dictionary items:
             * * "sourceIP": Source IP address [string]
             * * "errors": Whether errors are enabled [Boolean/integer/string]
             * * "flowControl": Whether flow control is enabled [Boolean/integer/string]
             *
             * Each data port has 64 destination table entries, indexed 0-63.
             *
             * \section VitaEnable_NDR308TS VITA 49 Enabling Options for DDCs
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

        } /* namespace NDR308TS */

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NDR308TS_RADIOHANDLER_H */
