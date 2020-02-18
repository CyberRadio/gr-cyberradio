/***************************************************************************
 * \file DucComponent.h
 * \brief Defines the basic DUC interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_DUCCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_DUCCOMPONENT_H

#include "LibCyberRadio/Driver/RadioComponent.h"
#include "LibCyberRadio/Common/BasicDict.h"
#include "LibCyberRadio/Common/BasicList.h"
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
        /**
         * \brief A rate set for a DUC.
         *
         * A rate set is a series of sample rates (in samples per second), keyed
         * by rate index.
         */
        typedef BASIC_DICT_CONTAINER<int, double> DucRateSet;

        /**
         * \brief Base DUC component class.
         *
         * A radio handler object maintains one DUC component object per DUC
         * on the radio.
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
         * \note Support for these elements varies by radio.  See the documentation
         *    for the particular radio's DUC specialization to determine what
         *    elements are supported.
         */
        class DucComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a DucComponent object.
                 * \param name The name of this component.
                 * \param index The index number of this component.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    component.
                 * \param debug Whether the component supports debug output.
                 * \param freqRangeMin Minimum tunable frequency (Hz).
                 * \param freqRangeMax Maximum tunable frequency (Hz).
                 * \param freqRes Tunable frequency resolution (Hz).
                 * \param freqUnits Tunable frequency units (Hz).
                 * \param attRangeMin Minimum attenuation (dB).
                 * \param attRangeMax Maximum attenuation (dB).
                 * \param attRes Attenuation resolution (dB).
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
                DucComponent(const std::string& name = "DUC",
                        int index = 1,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        double freqRangeMin = 0.0,
                        double freqRangeMax = 0.0,
                        double freqRes = 1.0,
                        double freqUnits = 1.0,
                        double attRangeMin = 0.0,
                        double attRangeMax = 10.0,
                        double attRes = 1.0,
                        int dataPort = 0,
                        double frequency = 0.0,
                        double attenuation = 0.0,
                        int rateIndex = 0,
                        int txChannels = 0,
                        int mode = 0,
                        unsigned int streamId = 0);
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
                // RadioComponent interface
                /**
                 * \brief Enables this component.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enable(bool enabled = true);
                /**
                 * \brief Sets the configuration dictionary for this component.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setConfiguration(ConfigurationDict& cfg);
                /**
                 * \brief Tells the component to query its hardware configuration in
                 *    order to create its configuration dictionary.
                 */
                virtual void queryConfiguration();
                // DucComponent extensions
                /**
                 * \brief Gets the DUC's data port.
                 * \returns The data port.
                 */
                virtual int getDataPort() const;
                /**
                 * \brief Sets the DUC's data port.
                 * \param port The new data port. Setting this to 0 disables
                 *    streaming.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPort(int port);
                /**
                 * \brief Gets the tuned frequency.
                 * \returns The tuned frequency, in Hz.
                 */
                virtual double getFrequency() const;
                /**
                 * \brief Sets the DUC tuned frequency.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFrequency(double freq);
                /**
                 * \brief Gets the tunable frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units.
                 * \returns The frequency units, in Hz.
                 */
                virtual double getFrequencyUnit() const;
                /**
                 * \brief Gets the attenuation.
                 * \returns The attenuation, in dB.
                 */
                virtual double getAttenuation() const;
                /**
                 * \brief Sets the attenuation.
                 * \param atten The new attenuation (dB).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setAttenuation(double atten);
                /**
                 * \brief Gets the attenuation range.
                 * \returns A list containing the minimum and maximum attenuation values.
                 */
                virtual BasicDoubleList getAttenuationRange() const;
                /**
                 * \brief Gets the attenuation resolution.
                 * \returns The resolution.
                 */
                virtual double getAttenuationRes() const;
                /**
                 * \brief Gets the DUC's rate index.
                 * \returns The rate index.
                 */
                virtual int getRateIndex() const;
                /**
                 * \brief Sets the DUC's rate index.
                 * \param index The new rate index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setRateIndex(int index);
                /**
                 * \brief Gets the DUC's transmit channel bitmap.
                 * \returns Bitmap indicating which transmitters are outputting the
                 *    signal from this DUC.  If a bit position is 1, the associated
                 *    transmitter is active. The LSB corresponds to TX 1, and each
                 *    succeeding bit corresponds to the other transmitters.
                 */
                virtual int getTxChannelBitmap() const;
                /**
                 * \brief Sets the DUC's transmit channel bitmap.
                 * \param txChannels Bitmap indicating which transmitters output the
                 *    signal from this DUC.  Setting a bit position to 1 enables transmit
                 *    on the associated transmitter. The LSB corresponds to TX 1, and each
                 *    succeeding bit corresponds to the other transmitters.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTxChannelBitmap(int txChannels);
                /**
                 * \brief Gets the DUC's mode.
                 * \returns The mode.  This is either 0 (streaming) or 1 (playback).
                 */
                virtual int getMode() const;
                /**
                 * \brief Sets the DUC's mode.
                 * \param mode The new mode.  This is either 0 (streaming) or 1 (playback).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setMode(int mode);
                /**
                 * \brief Gets the DUC's VITA 49 stream ID.
                 * \returns The VITA 49 stream ID.
                 */
                virtual unsigned int getStreamId() const;
                /**
                 * \brief Sets the DUC's VITA 49 stream ID.
                 * \param sid The new stream ID.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setStreamId(unsigned int sid);
                /**
                 * \brief Gets the DUC's rate set.
                 * \returns The rate set.
                 */
                virtual DucRateSet getRateSet() const;
                /**
                 * \brief Sets the DUC rate set.
                 * \param set The new rate set.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setRateSet(const DucRateSet& set);
                /**
                 * \brief Gets the list of allowed sample rates, based on the
                 *    rate set.
                 * \returns The rate list.
                 */
                virtual BasicDoubleList getRateList() const;
                /**
                 * \brief Gets whether or not the DUC supports loading snapshot files.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsSnapshotLoad() const;
                /**
                 * \brief Load a snapshot file into the DUC's memory block.
                 *
                 * Snapshot files contain 16-bit complex I/Q data samples.
                 *
                 * \param filename Snapshot file name.  The snapshot file needs to be
                 *    present on the radio.
                 * \param startSample Starting address in DUC's memory block.  Must
                 *    be a multiple of 1024.
                 * \param samples Number of I/Q samples to load.  Must be a multiple
                 *    of 16.  If specified as 0, load the maximum number of samples
                 *    from the file.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool loadSnapshot(const std::string& filename,
                        unsigned int startSample = 0,
                        unsigned int samples = 0);
                /**
                 * \brief Gets whether or not the DUC supports transmitting snapshots.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsSnapshotTransmit() const;

            protected:
                // RadioComponent interface
                /**
                 * \brief Initializes the configuration dictionary, defining the allowed
                 *    keys.
                 */
                virtual void initConfigurationDict();
                /**
                 * \brief Updates the configuration dictionary from component settings.
                 */
                virtual void updateConfigurationDict();
                // DucComponent extensions
                /**
                 * \brief Executes the DUC configuration query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index DUC index.
                 * \param dataPort Data port number (0 disables) (return).
                 * \param frequency Tuned frequency (Hz) (return).
                 * \param attenuation Attenuation (dB) (return).
                 * \param rateIndex DUC's rate index (return).
                 * \param txChannels DUC's TX channel output bitmap (return).
                 * \param mode DUC's mode setting (return).
                 * \param streamId DUC's VITA 49 stream ID (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDucQuery(int index,
                        int& dataPort,
                        double& frequency,
                        double& attenuation,
                        int& rateIndex,
                        int& txChannels,
                        int& mode,
                        unsigned int& streamId);
                /**
                 * \brief Executes the DUC configuration set command.
                 * \param index DUC index.
                 * \param dataPort Data port number (0 disables).
                 * \param frequency Tuned frequency (Hz).
                 * \param attenuation Attenuation (dB).
                 * \param rateIndex DUC's rate index.
                 * \param txChannels DUC's TX channel output bitmap.
                 * \param mode DUC's mode setting.
                 * \param streamId DUC's VITA 49 stream ID.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDucCommand(int index,
                        int& dataPort,
                        double& frequency,
                        double& attenuation,
                        int& rateIndex,
                        int& txChannels,
                        int& mode,
                        unsigned int& streamId);
                /**
                 * Executes the DUC snapshot load command.
                 * \param index DUC index.
                 * \param filename Snapshot file name.
                 * \param startSample Starting sample number.
                 * \param samples Number of samples (0 = load maximum).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSnapshotLoadCommand(int index,
                        const std::string& filename,
                        unsigned int startSample,
                        unsigned int samples);

            protected:
                // Minimum tunable frequency (Hz)
                double _freqRangeMin;
                // Maximum tunable frequency (Hz)
                double _freqRangeMax;
                // Frequency resolution (Hz)
                double _freqRes;
                // Frequency units (Hz)
                double _freqUnits;
                // Minimum attenuation (dB)
                double _attRangeMin;
                // Maximum attenuation (dB)
                double _attRangeMax;
                // Attenuation resolution
                double _attRes;
                // Data port
                int _dataPort;
                // Tuned frequency
                double _frequency;
                // Attenuation
                double _attenuation;
                // Rate index
                int _rateIndex;
                // TX channel bitmap
                int _txChannels;
                // DUC mode (streaming or playback)
                int _mode;
                // VITA 49 stream ID
                unsigned int _streamId;
                // Supports snapshot load
                bool _supportsSnapLoad;
                // Snapshot file name
                std::string _snapFilename;
                // Snapshot starting sample
                unsigned int _snapStartSample;
                // Snapshot number of samples
                unsigned int _snapSamples;
                // Supports snapshot transmit
                bool _supportsSnapTransmit;
                // Whether snapshot transmit is single playback
                bool _snapSinglePlayback;
                // Whether snapshot transmit should pause until enabled
                bool _snapPauseUntilEnabled;
                // Rate set
                DucRateSet _rateSet;

        }; // class DucComponent

        /**
         * \brief A dictionary of DUC components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, DucComponent*> DucComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_DUCCOMPONENT_H
