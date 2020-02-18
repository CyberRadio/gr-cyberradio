/***************************************************************************
 * \file CWToneGenComponent.h
 * \brief Defines the basic continuous-wave (CW) tone generator interface
 *    for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_CWTONEGENCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_CWTONEGENCOMPONENT_H

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
        // Forward declaration for RadioHandler
        class RadioHandler;

        /**
         * \brief Base continuous-wave (CW) tone generator component class.
         *
         * A radio handler object maintains one CW tone generator component
         * object per tone generator on the radio.
         *
         * Configuration dictionary elements:
         * * "enable": Whether or not this component is enabled [Boolean]
         */
        class CWToneGenComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a CWToneGenComponent object.
                 * \note If the CW tone generator does NOT support frequency sweeping,
                 *    set sweepStartRangeMin and sweepStartRangeMax to the same value.
                 * \param name The name of this component.
                 * \param index The index number of this component.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    component.
                 * \param debug Whether the component supports debug output.
                 * \param txIndex Transmitter index associated with this component.
                 * \param freqRangeMin Minimum tunable frequency (Hz).
                 * \param freqRangeMax Maximum tunable frequency (Hz).
                 * \param freqRes Tunable frequency resolution (Hz).
                 * \param freqUnits Tunable frequency units (Hz).
                 * \param ampRangeMin Minimum amplitude (scale units).
                 * \param ampRangeMax Maximum amplitude (scale units).
                 * \param ampRes Amplitude resolution (scale units).
                 * \param phaseRangeMin Minimum phase (degrees).
                 * \param phaseRangeMax Maximum phase (degrees).
                 * \param phaseRes Phase resolution (degrees).
                 * \param sweepStartRangeMin Minimum sweep start frequency (Hz).
                 * \param sweepStartRangeMax Maximum sweep start frequency (Hz).
                 * \param sweepStartRes Sweep start frequency resolution (Hz).
                 * \param sweepStopRangeMin Minimum sweep stop frequency (Hz).
                 * \param sweepStopRangeMax Maximum sweep stop frequency (Hz).
                 * \param sweepStopRes Sweep stop frequency resolution (Hz).
                 * \param sweepStepRangeMin Minimum sweep step frequency (Hz).
                 * \param sweepStepRangeMax Maximum sweep step frequency (Hz).
                 * \param sweepStepRes Sweep step frequency resolution (Hz).
                 * \param dwellTimeRangeMin Minimum dwell time (ADC samples).
                 * \param dwellTimeRangeMax Maximum dwell time (ADC samples).
                 * \param dwellTimeRes Dwell time resolution (ADC samples).
                 * \param frequency Constant frequency (Hz).
                 * \param amplitude Signal amplitude (scale units).
                 * \param phase Signal phase (degrees).
                 * \param sweepStart Frequency sweep start (Hz).
                 * \param sweepStop Frequency sweep stop (Hz).
                 * \param sweepStep Frequency sweep step (Hz).
                 * \param dwellTime Dwell time (ADC samples).
                 */
                CWToneGenComponent(const std::string& name = "CWTONE",
                        int index = 0,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        int txIndex = 0,
                        double freqRangeMin = 0.0,
                        double freqRangeMax = 0.0,
                        double freqRes = 0.0,
                        double freqUnits = 0.0,
                        double ampRangeMin = 0.0,
                        double ampRangeMax = 0.0,
                        double ampRes = 0.0,
                        double phaseRangeMin = 0.0,
                        double phaseRangeMax = 0.0,
                        double phaseRes = 0.0,
                        double sweepStartRangeMin = 0.0,
                        double sweepStartRangeMax = 0.0,
                        double sweepStartRes = 0.0,
                        double sweepStopRangeMin = 0.0,
                        double sweepStopRangeMax = 0.0,
                        double sweepStopRes = 0.0,
                        double sweepStepRangeMin = 0.0,
                        double sweepStepRangeMax = 0.0,
                        double sweepStepRes = 0.0,
                        double dwellTimeRangeMin = 0.0,
                        double dwellTimeRangeMax = 0.0,
                        double dwellTimeRes = 0.0,
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
                // CWToneGenComponent extensions
                /**
                 * \brief Gets the frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getFrequencyRange() const;
                /**
                 * \brief Gets the frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getFrequencyRes() const;
                /**
                 * \brief Gets the amplitude range.
                 * \returns A list containing the minimum and maximum amplitudes.
                 */
                virtual BasicDoubleList getAmplitudeRange() const;
                /**
                 * \brief Gets the amplitude resolution.
                 * \returns The amplitude resolution, in scale units.
                 */
                virtual double getAmplitudeRes() const;
                /**
                 * \brief Gets the phase range.
                 * \returns A list containing the minimum and maximum phases.
                 */
                virtual BasicDoubleList getPhaseRange() const;
                /**
                 * \brief Gets the phase resolution.
                 * \returns The phase resolution, in degrees.
                 */
                virtual double getPhaseRes() const;
                /**
                 * \brief Gets the sweep start range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getSweepStartRange() const;
                /**
                 * \brief Gets the sweep start resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getSweepStartRes() const;
                /**
                 * \brief Gets the sweep stop range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getSweepStopRange() const;
                /**
                 * \brief Gets the sweep stop resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getSweepStopRes() const;
                /**
                 * \brief Gets the sweep step range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getSweepStepRange() const;
                /**
                 * \brief Gets the sweep step resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getSweepStepRes() const;
                /**
                 * \brief Gets the dwell time range.
                 * \returns A list containing the minimum and maximum dwell times.
                 */
                virtual BasicDoubleList getDwellTimeRange() const;
                /**
                 * \brief Gets the dwell time resolution.
                 * \returns The dwell time resolution, in ADC samples.
                 */
                virtual double getDwellTimeRes() const;
                /**
                 * \brief Gets the constant frequency.
                 * \returns The constant frequency, in Hz.
                 */
                virtual double getFrequency() const;
                /**
                 * \brief Sets the constant frequency.
                 * \param freq The new constant frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFrequency(double freq);
                /**
                 * \brief Gets the signal amplitude.
                 * \returns The signal amplitude, in scale units.
                 */
                virtual double getAmplitude() const;
                /**
                 * \brief Sets the signal amplitude.
                 * \param amp The new signal amplitude (scale units).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setAmplitude(double amp);
                /**
                 * \brief Gets the signal phase.
                 * \returns The signal phase, in degrees.
                 */
                virtual double getPhase() const;
                /**
                 * \brief Sets the signal phase.
                 * \param phase The new signal phase (degrees).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setPhase(double phase);
                /**
                 * \brief Gets whether or not the generator supports signal sweeps.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool supportsSweep() const;
                /**
                 * \brief Gets the start frequency for a signal sweep.
                 * \returns The start frequency, in Hz.
                 */
                virtual double getSweepStartFrequency() const;
                /**
                 * \brief Gets the stop frequency for a signal sweep.
                 * \returns The stop frequency, in Hz.
                 */
                virtual double getSweepStopFrequency() const;
                /**
                 * \brief Gets the frequency step for a signal sweep.
                 * \returns The frequency step, in Hz.
                 */
                virtual double getSweepFrequencyStep() const;
                /**
                 * \brief Gets the dwell time for a signal sweep.
                 * \returns The dwell time, in ADC samples.
                 */
                virtual double getSweepDwellTime() const;
                /**
                 * \brief Sets the parameters for a frequency sweep.
                 * \param start The new start frequency (Hz).
                 * \param stop The new stop frequency (Hz).
                 * \param step The new frequency step (Hz).
                 * \param dwell The new dwell time (ADC samples).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setFrequencySweep(double start, double stop, double step, double dwell);

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
                // CWToneGenComponent extensions
                /**
                 * \brief Executes the CW tone query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index CW tone generator index.
                 * \param txIndex Transmitter index associated with this component.
                 * \param freq Frequency (Hz) (return).
                 * \param amp Amplitude (scale units) (return).
                 * \param phase Phase (degrees) (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeToneQuery(int index,
                        int txIndex,
                        double& freq,
                        double& amp,
                        double& phase);
                /**
                 * \brief Executes the CW tone set command.
                 * \param index CW tone generator index.
                 * \param txIndex Transmitter index associated with this component.
                 * \param freq Frequency (Hz).
                 * \param amp Amplitude (scale units).
                 * \param phase Phase (degrees).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeToneCommand(int index,
                        int txIndex,
                        double& freq,
                        double& amp,
                        double& phase);
                /**
                 * \brief Executes the CW sweep query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index CW tone generator index.
                 * \param txIndex Transmitter index associated with this component.
                 * \param sweepStart Start frequency (Hz) (return).
                 * \param sweepStop Stop frequency (Hz) (return).
                 * \param sweepStep Frequency step (Hz) (return).
                 * \param dwellTime Dwell time (ADC samples) (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSweepQuery(int index,
                        int txIndex,
                        double& sweepStart,
                        double& sweepStop,
                        double& sweepStep,
                        double& dwellTime);
                /**
                 * \brief Executes the CW sweep set command.
                 * \param index CW tone generator index.
                 * \param txIndex Transmitter index associated with this component.
                 * \param sweepStart Start frequency (Hz).
                 * \param sweepStop Stop frequency (Hz).
                 * \param sweepStep Frequency step (Hz).
                 * \param dwellTime Dwell time (ADC samples).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSweepCommand(int index,
                        int txIndex,
                        double& sweepStart,
                        double& sweepStop,
                        double& sweepStep,
                        double& dwellTime);

            protected:
                // Transmitter index
                int _txIndex;
                // Min frequency
                double _freqRangeMin;
                // Max frequency
                double _freqRangeMax;
                // Frequency resolution
                double _freqRes;
                // Frequency units
                double _freqUnits;
                // Min amplitude
                double _ampRangeMin;
                // Max amplitude
                double _ampRangeMax;
                // Amplitude resolution
                double _ampRes;
                // Min phase
                double _phaseRangeMin;
                // Max phase
                double _phaseRangeMax;
                // Phase resolution
                double _phaseRes;
                // Min sweep start
                double _sweepStartRangeMin;
                // Max sweep start
                double _sweepStartRangeMax;
                // Sweep start resolution
                double _sweepStartRes;
                // Min sweep stop
                double _sweepStopRangeMin;
                // Max sweep stop
                double _sweepStopRangeMax;
                // Sweep stop resolution
                double _sweepStopRes;
                // Min sweep step
                double _sweepStepRangeMin;
                // Max sweep step
                double _sweepStepRangeMax;
                // Sweep step resolution
                double _sweepStepRes;
                // Min dwell time
                double _dwellTimeRangeMin;
                // Max dwell time
                double _dwellTimeRangeMax;
                // Dwell time resolution
                double _dwellTimeRes;
                // Constant frequency (Hz)
                double _frequency;
                // Amplitude (scale units)
                double _amplitude;
                // Phase (degrees)
                double _phase;
                // Frequency sweep start (Hz)
                double _sweepStart;
                // Frequency sweep stop (Hz)
                double _sweepStop;
                // Frequency sweep step (Hz)
                double _sweepStep;
                // Dwell time (ADC samples)
                double _dwellTime;

        }; // class CWToneGenComponent

        /**
         * \brief A dictionary of CW tone generator components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, CWToneGenComponent*> CWToneGenComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_CWTONEGENCOMPONENT_H
