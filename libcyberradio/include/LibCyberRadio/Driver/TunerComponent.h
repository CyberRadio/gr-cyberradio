/***************************************************************************
 * \file TunerComponent.h
 * \brief Defines the basic tuner interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_TUNERCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_TUNERCOMPONENT_H

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
         * \brief Base tuner component class.
         *
         * A radio handler object maintains one tuner component object per tuner
         * on the radio.
         *
         * Configuration dictionary elements:
         * * "enable": Whether or not this tuner is enabled [Boolean/integer/string]
         * * "frequency": Tuned frequency (Hz) [double/string]
         * * "attenuation": Attenuation (dB) [double/string]
         * * "filter": Filter setting [integer/string]
         * * "timingAdj": Timing adjustment, in ADC clock cycles [integer/string]
         *
         */
        class TunerComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a TunerComponent object.
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
                 * \param agc Whether or not the tuner supports automatic gain control.
                 * \param frequency Tuned frequency (Hz).
                 * \param attenuation Attenuation (dB).
                 * \param filter Filter setting.
                 */
                TunerComponent(const std::string& name = "TUNER",
                        int index = 1,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        double freqRangeMin = 20e6,
                        double freqRangeMax = 6000e6,
                        double freqRes = 1e6,
                        double freqUnits = 1e6,
                        double attRangeMin = 0.0,
                        double attRangeMax = 30.0,
                        double attRes = 1.0,
                        bool agc = false,
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
                // TunerComponent extensions
                /**
                 * \brief Gets the tuned frequency.
                 * \returns The tuned frequency, in Hz.
                 */
                virtual double getFrequency() const;
                /**
                 * \brief Sets the tuned frequency.
                 * \param freq The new tuned frequency (Hz).
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
                 * \brief Gets the filter setting.
                 * \returns The filter setting.
                 */
                virtual int getFilter() const;
                /**
                 * \brief Sets the filter setting.
                 * \param filter The new filter setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFilter(int filter);
                /**
                 * \brief Gets the timing adjustment setting.
                 * \returns The timing adjustment setting.
                 */
                virtual int getTimingAdjustment() const;
                /**
                 * \brief Sets the timing adjustment setting.
                 * \param timingAdj The new timing adjustment setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTimingAdjustment(int timingAdj);
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
                 * \brief Gets whether or not the tuner supports AGC.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool isAgcSupported() const;
                /**
                 * \brief Sets the maximum end of the tunable frequency range.
                 * \param freq New maximum frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFrequencyRangeMax(double freq);

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
                // TunerComponent extensions
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
                 * \brief Executes the tuner filter query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index tuner index.
                 * \param filter Filter setting (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFilterQuery(int index, int& filter);
                /**
                 * \brief Executes the tuner timing adjustment query.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index tuner index.
                 * \param timingAdj Timing adjustment setting (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeTimingAdjustmentQuery(int index, int& timingAdj);
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
                /**
                 * \brief Executes the tuner filter set command.
                 * \param index tuner index.
                 * \param filter Filter setting.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFilterCommand(int index, int& filter);
                /**
                 * \brief Executes the tuner timing adjustment command.
                 * \param index tuner index.
                 * \param timingAdj Timing adjustment setting.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeTimingAdjustmentCommand(int index, int& timingAdj);

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
                // Whether or not WBDDC supports AGC
                bool _agc;
                // Tuned frequency
                double _frequency;
                // Attenuation
                double _attenuation;
                // Filter setting
                int _filter;
                // Timing adjustment
                int _timingAdj;

        }; // class TunerComponent

        /**
         * \brief A dictionary of tuner components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, TunerComponent*> TunerComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_TUNERCOMPONENT_H
