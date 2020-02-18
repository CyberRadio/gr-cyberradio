/***************************************************************************
 * \file TransmitterComponent.h
 * \brief Defines the basic transmitter interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_TRANSMITTERCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_TRANSMITTERCOMPONENT_H

#include "LibCyberRadio/Driver/CWToneGenComponent.h"
#include "LibCyberRadio/Driver/RadioComponent.h"
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
        // Forward declaration for RadioHandler
        class RadioHandler;

        /**
         * \brief Base transmitter component class.
         *
         * A radio handler object maintains one transmitter component object per
         * transmitter on the radio.
         *
         * Configuration dictionary elements:
         * * "enable": Whether or not this transmitter is enabled [Boolean/integer/string]
         * * "frequency": Tuned frequency (Hz) [double/string]
         * * "attenuation": Attenuation (dB) [double/string]
         *
         */
        class TransmitterComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a TransmitterComponent object.
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
                 * \param numToneGen Number of CW tone generators associated
                 *    with this transmitter.
                 * \param toneGenIndexBase Number where tone generator index
                 *    numbers begin.
                 * \param frequency Transmitter center frequency (Hz).
                 * \param attenuation Transmitter attenuation (dB).
                 */
                TransmitterComponent(const std::string& name = "TX",
                        int index = 1,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        double freqRangeMin = 20e6,
                        double freqRangeMax = 6000e6,
                        double freqRes = 1e6,
                        double freqUnits = 1e6,
                        double attRangeMin = 0.0,
                        double attRangeMax = 10.0,
                        double attRes = 1.0,
                        int numToneGen = 0,
                        int toneGenIndexBase = 1,
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
                // TransmitterComponent extensions
                /**
                 * \brief Gets the transmitter center frequency.
                 * \returns The transmitter center frequency, in Hz.
                 */
                virtual double getFrequency() const;
                /**
                 * \brief Sets the transmitter center frequency.
                 * \param freq The new transmitter center frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFrequency(double freq);
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
                 * \brief Gets the transmitter center frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getFrequencyRange() const;
                /**
                 * \brief Gets the transmitter center frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getFrequencyRes() const;
                /**
                 * \brief Gets the transmitter center frequency units.
                 * \returns The frequency units, in Hz.
                 */
                virtual double getFrequencyUnit() const;
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
                 * \brief Gets whether the transmitter supports CW tone generation.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsCW() const;
                /**
                 * \brief Gets the number of CW tone generators associated with this
                 *     transmitter.
                 * \returns The number of generators.
                 */
                virtual int getCWNum() const;
                /**
                 * \brief Gets the range of indices for CW tone generators.
                 * \returns A list containing the generator indices.
                 */
                virtual BasicIntList getCWIndexRange() const;
                /**
                 * \brief Gets the CW frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getCWFrequencyRange() const;
                /**
                 * \brief Gets the CW frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getCWFrequencyRes() const;
                /**
                 * \brief Gets the CW amplitude range.
                 * \returns A list containing the minimum and maximum amplitude values.
                 */
                virtual BasicDoubleList getCWAmplitudeRange() const;
                /**
                 * \brief Gets the CW amplitude resolution.
                 * \returns The resolution.
                 */
                virtual double getCWAmplitudeRes() const;
                /**
                 * \brief Gets the CW phase range.
                 * \returns A list containing the minimum and maximum phase values.
                 */
                virtual BasicDoubleList getCWPhaseRange() const;
                /**
                 * \brief Gets the CW phase resolution.
                 * \returns The resolution.
                 */
                virtual double getCWPhaseRes() const;
                /**
                 * \brief Gets whether the transmitter supports CW tone sweeping.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsCWSweep() const;
                /**
                 * \brief Gets the CW start frequency range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getCWSweepStartRange() const;
                /**
                 * \brief Gets the CW start frequency resolution.
                 * \returns The resolution.
                 */
                virtual double getCWSweepStartRes() const;
                /**
                 * \brief Gets the CW stop frequency range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getCWSweepStopRange() const;
                /**
                 * \brief Gets the CW stop frequency resolution.
                 * \returns The resolution.
                 */
                virtual double getCWSweepStopRes() const;
                /**
                 * \brief Gets the CW frequency step range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getCWSweepStepRange() const;
                /**
                 * \brief Gets the CW frequency step resolution.
                 * \returns The resolution.
                 */
                virtual double getCWSweepStepRes() const;
                /**
                 * \brief Gets the CW dwell time range.
                 * \returns A list containing the minimum and maximum dwell time values.
                 */
                virtual BasicDoubleList getCWSweepDwellRange() const;
                /**
                 * \brief Gets the CW dwell time resolution.
                 * \returns The resolution.
                 */
                virtual double getCWSweepDwellRes() const;
                /**
                 * \brief Enables a given CW tone generator.
                 * \param index CW tone generator index.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableCW(int index, bool enabled = true);
                /**
                 * \brief Disables a given CW tone generator.
                 * \param index CW tone generator index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableCW(int index);
                /**
                 * \brief Gets the configuration for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getCWConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given CW tone
                 *    generator.
                 * \param index CW tone generator index.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setCWConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the constant frequency for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The constant frequency, in Hz.
                 */
                virtual double getCWFrequency(int index) const;
                /**
                 * \brief Sets the constant frequency for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \param freq The new constant frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setCWFrequency(int index, double freq);
                /**
                 * \brief Gets the signal amplitude for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The signal amplitude, in scale units.
                 */
                virtual double getCWAmplitude(int index) const;
                /**
                 * \brief Sets the signal amplitude for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \param amp The new signal amplitude (scale units).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setCWAmplitude(int index, double amp);
                /**
                 * \brief Gets the signal phase for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The signal phase, in degrees.
                 */
                virtual double getCWPhase(int index) const;
                /**
                 * \brief Sets the signal phase for a given CW tone generator.
                 * \param index CW tone generator index.
                 * \param phase The new signal phase (degrees).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setCWPhase(int index, double phase);
                /**
                 * \brief Gets whether or not a given CW tone generator supports
                 *    signal sweeps.
                 * \param index CW tone generator index.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsCWSweep(int index) const;
                /**
                 * \brief Gets the start frequency for a signal sweep for a given
                 *    CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The start frequency, in Hz.
                 */
                virtual double getCWSweepStartFrequency(int index) const;
                /**
                 * \brief Gets the stop frequency for a signal sweep for a given
                 *    CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The stop frequency, in Hz.
                 */
                virtual double getCWSweepStopFrequency(int index) const;
                /**
                 * \brief Gets the frequency step for a signal sweep for a given
                 *    CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The frequency step, in Hz.
                 */
                virtual double getCWSweepFrequencyStep(int index) const;
                /**
                 * \brief Gets the dwell time for a signal sweep for a given
                 *    CW tone generator.
                 * \param index CW tone generator index.
                 * \returns The dwell time, in sample clocks.
                 */
                virtual double getCWSweepDwellTime(int index) const;
                /**
                 * \brief Sets the parameters for a frequency sweep for a given
                 *    CW tone generator.
                 * \param index CW tone generator index.
                 * \param start The new start frequency (Hz).
                 * \param stop The new stop frequency (Hz).
                 * \param step The new frequency step (Hz).
                 * \param dwell The new dwell time (sample clocks).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setCWFrequencySweep(int index, double start, double stop,
                        double step, double dwell);

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
                // TransmitterComponent extensions
                /**
                 * \brief Executes the tuner enabled query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index tuner index.
                 * \param enabled Whether or not tuner is enabled (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeEnableQuery(int index, bool& enabled);
                /**
                 * \brief Executes the tuner frequency query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index tuner index.
                 * \param freq Tuned frequency (Hz) (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFreqQuery(int index, double& freq);
                /**
                 * \brief Executes the tuner attenuation query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index tuner index.
                 * \param atten Attenuation (dB) (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeAttenQuery(int index, double& atten);
                /**
                 * \brief Executes the tuner enable command.
                 * \param index tuner index.
                 * \param enabled Whether or not tuner is enabled.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeEnableCommand(int index, bool& enabled);
                /**
                 * \brief Executes the tuner frequency set command.
                 * \param index tuner index.
                 * \param freq Tuned frequency (Hz).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFreqCommand(int index, double& freq);
                /**
                 * \brief Executes the tuner attenuation set command.
                 * \param index tuner index.
                 * \param atten Attenuation (dB).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeAttenCommand(int index, double& atten);

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
                // Number of CW tone generators associated with this transmitter
                int _numToneGen;
                // Number that tone generator indicates start at
                int _toneGenIndexBase;
                // Tuned frequency
                double _frequency;
                // Attenuation
                double _attenuation;
                // Tone generator dictionary
                CWToneGenComponentDict _cwToneGens;

        }; // class TransmitterComponent

        /**
         * \brief A dictionary of tuner components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, TransmitterComponent*> TransmitterComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_TRANSMITTERCOMPONENT_H
