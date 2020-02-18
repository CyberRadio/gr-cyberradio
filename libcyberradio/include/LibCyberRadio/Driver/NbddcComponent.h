/***************************************************************************
 * \file NbddcComponent.h
 * \brief Defines the basic NBDDC interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENT_H

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
         * \brief A rate set for a NBDDC.
         *
         * A rate set is a series of sample rates (in samples per second), keyed
         * by rate index.
         */
        typedef BASIC_DICT_CONTAINER<int, double> NbddcRateSet;

        /**
         * \brief Base NBDDC component class.
         *
         * A radio handler object maintains one NBDDC component object per NBDDC
         * on the radio.
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
         * \note Support for these elements varies by radio.  See the documentation
         *    for the particular radio's NBDDC specialization to determine what
         *    elements are supported.
         */
        class NbddcComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a NbddcComponent object.
                 * \param name The name of this component.
                 * \param index The index number of this component.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    component.
                 * \param debug Whether the component supports debug output.
                 * \param nbddcCommandSetsFreq Whether or not the NBDDC command sets the
                 *    frequency.
                 * \param nbddcCommandSetsSource Whether or not the NBDDC command sets the
                 *    source.
                 * \param selectableDataPort Whether or not the NBDDC can select which
                 *    data port is data comes out on.
                 * \param freqRangeMin Minimum tunable frequency (Hz).  This parameter has
                 *    no meaning if the NBDDC is not tunable.
                 * \param freqRangeMax Maximum tunable frequency (Hz).  This parameter has
                 *    no meaning if the NBDDC is not tunable.
                 * \param freqRes Tunable frequency resolution (Hz).  This parameter has
                 *    no meaning if the NBDDC is not tunable.
                 * \param freqUnits Tunable frequency units (Hz).  This parameter has
                 *    no meaning if the NBDDC is not tunable.
                 * \param source Source (tuner) index supplying the signal for this NBDDC.
                 *    This parameter has no meaning if the NBDDC does not support selectable
                 *    source.
                 * \param dataPort Data port used by this NBDDC.  This parameter has no
                 *    meaning if the radio has no dedicated data ports.
                 * \param frequency Tuned frequency (Hz).  This parameter has no meaning if
                 *    the NBDDC is not tunable.
                 * \param rateIndex NBDDC rate index.  This should be one of the rate
                 *    indices in the NBDDC's rate set.
                 * \param udpDestination UDP destination.  The meaning of this parameter
                 *    depends on the radio's UDP addressing scheme.
                 * \param vitaEnable VITA 49 framing setting.  The meaning of this parameter
                 *    depends on the radio's allowed VITA settings.
                 * \param streamId VITA 49 stream ID.
                 */
                NbddcComponent(const std::string& name = "NBDDC",
                        int index = 1,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        bool nbddcCommandSetsFreq = false,
                        bool nbddcCommandSetsSource = false,
                        bool selectableDataPort = false,
                        double freqRangeMin = 0.0,
                        double freqRangeMax = 0.0,
                        double freqRes = 1.0,
                        double freqUnits = 1.0,
                        int source = 1,
                        int dataPort = 1,
                        double frequency = 0.0,
                        int rateIndex = 0,
                        int udpDestination = 0,
                        int vitaEnable = 0,
                        unsigned int streamId = 0);
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
                // NbddcComponent extensions
                /**
                 * \brief Gets the tuned frequency.
                 * \returns The tuned frequency, in Hz.  This value has no meaning if
                 *    the NBDDC is not tunable.
                 */
                virtual double getFrequency() const;
                /**
                 * \brief Sets the NBDDC tuned frequency.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.  Returns
                 *    false if the NBDDC is not tunable.
                 */
                virtual bool setFrequency(double freq);
                /**
                 * \brief Gets the tunable frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 *    These numbers have no meaning if the NBDDC is not tunable.
                 */
                virtual BasicDoubleList getFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution.
                 * \returns The frequency resolution, in Hz.  This value has no
                 *    meaning if the NBDDC is not tunable.
                 */
                virtual double getFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units.
                 * \returns The frequency units, in Hz.  This value has no
                 *    meaning if the NBDDC is not tunable.
                 */
                virtual double getFrequencyUnit() const;
                /**
                 * \brief Gets the NBDDC's source (which tuner is supplying the signal).
                 * \returns The source index.  This value has no meaning if the NBDDC
                 *    does not support selectable source.
                 */
                virtual int getSource() const;
                /**
                 * \brief Sets the NBDDC's source (which tuner is supplying the signal).
                 * \param source The new NBDDC source index.
                 * \returns True if successful, false otherwise.  Returns false if the
                 *    NBDDC does not support selectable source.
                 */
                virtual bool setSource(int source);
                /**
                 * \brief Gets the NBDDC's rate index.
                 * \returns The rate index.
                 */
                virtual int getRateIndex() const;
                /**
                 * \brief Sets the NBDDC's rate index.
                 * \param index The new rate index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setRateIndex(int index);
                /**
                 * \brief Gets the NBDDC's UDP destination.
                 * \returns The UDP destination.
                 */
                virtual int getUdpDestination() const;
                /**
                 * \brief Sets the NBDDC's UDP destination.
                 * \param dest The new UDP destination.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setUdpDestination(int dest);
                /**
                 * \brief Gets the NBDDC's VITA 49 setting.
                 * \returns The VITA 49 setting.
                 */
                virtual int getVitaEnable() const;
                /**
                 * \brief Sets the NBDDC's VITA 49 setting.
                 * \param enable The new VITA 49 setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setVitaEnable(int enable);
                /**
                 * \brief Gets the NBDDC's VITA 49 stream ID.
                 * \returns The VITA 49 stream ID.
                 */
                virtual unsigned int getStreamId() const;
                /**
                 * \brief Sets the NBDDC's VITA 49 stream ID.
                 * \param sid The new stream ID.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setStreamId(unsigned int sid);
                /**
                 * \brief Gets the NBDDC's data port.
                 * \returns The data port. This number has no meaning if the
                 *    radio does not use data ports.
                 */
                virtual int getDataPort() const;
                /**
                 * \brief Sets the NBDDC's data port.
                 * \param port The new data port.
                 * \returns True if successful, false otherwise. Returns false
                 *    if the radio does not use data ports.
                 */
                virtual bool setDataPort(int port);
                /**
                 * \brief Gets the NBDDC's rate set.
                 * \returns The rate set.
                 */
                virtual NbddcRateSet getRateSet() const;
                /**
                 * \brief Sets the NBDDC rate set.
                 * \param set The new rate set.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setRateSet(const NbddcRateSet& set);
                /**
                 * \brief Gets the list of allowed sample rates, based on the
                 *    rate set.
                 * \returns The rate list.
                 */
                virtual BasicDoubleList getRateList() const;

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
                // NbddcComponent extensions
                /**
                 * \brief Executes the NBDDC configuration query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \note Because the NBDDC configuration query varies between radios, this
                 *    method may not use all of the parameters passed to it.
                 * \param index NBDDC index.
                 * \param rateIndex NBDDC's rate index (return).
                 * \param udpDestination NBDDC's UDP destination (return).
                 * \param enabled Whether or not NBDDC is enabled (return).
                 * \param vitaEnable NBDDC's VITA 49 setting (return).
                 * \param streamId NBDDC's VITA 49 stream ID (return).
                 * \param frequency NBDDC's frequency (return).
                 * \param source NBDDC's source (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcQuery(int index,
                        int& rateIndex,
                        int& udpDestination,
                        bool& enabled,
                        int& vitaEnable,
                        unsigned int& streamId,
                        double& frequency,
                        int& source);
                /**
                 * \brief Executes the NBDDC configuration set command.
                 * \note Because the NBDDC configuration command varies between radios, this
                 *    method may not use all of the parameters passed to it.
                 * \param index NBDDC index.
                 * \param rateIndex NBDDC's rate index.
                 * \param udpDestination NBDDC's UDP destination.
                 * \param enabled Whether or not NBDDC is enabled.
                 * \param vitaEnable NBDDC's VITA 49 setting.
                 * \param streamId NBDDC's VITA 49 stream ID.
                 * \param frequency NBDDC's frequency.
                 * \param source NBDDC's source.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcCommand(int index,
                        int& rateIndex,
                        int& udpDestination,
                        bool& enabled,
                        int& vitaEnable,
                        unsigned int& streamId,
                        double& frequency,
                        int& source);
                /**
                 * \brief Executes the NBDDC frequency query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC index.
                 * \param freq NBDDC's tuned frequency (return).
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the NBDDC is not tunable.
                 */
                virtual bool executeFreqQuery(int index, double& freq);
                /**
                 * \brief Executes the NBDDC frequency set command.
                 * \param index NBDDC index.
                 * \param freq NBDDC's tuned frequency.
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the NBDDC is not tunable.
                 */
                virtual bool executeFreqCommand(int index, double& freq);
                /**
                 * \brief Executes the NBDDC source query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC index.
                 * \param source NBDDC's source index (return).
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the NBDDC does not support selectable source.
                 */
                virtual bool executeSourceQuery(int index, int& source);
                /**
                 * \brief Executes the NBDDC source set command.
                 * \param index NBDDC index.
                 * \param source NBDDC's source index.
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the NBDDC does not support selectable source.
                 */
                virtual bool executeSourceCommand(int index, int& source);
                /**
                 * \brief Executes the NBDDC data port query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC index.
                 * \param dataPort NBDDC's data port (return).
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the radio does not use data ports.
                 */
                virtual bool executeDataPortQuery(int index, int& dataPort);
                /**
                 * \brief Executes the NBDDC data port set command.
                 * \param index NBDDC index.
                 * \param dataPort NBDDC's data port.
                 * \returns True if the command succeeded, false otherwise. Returns false if
                 *    the radio does not use data ports.
                 */
                virtual bool executeDataPortCommand(int index, int& dataPort);

            protected:
                // Whether or not the NBDDC config command sets its frequency
                bool _nbddcCommandSetsFreq;
                // Whether or not the NBDDC config command sets its source
                bool _nbddcCommandSetsSource;
                // Whether or not radio uses data ports
                bool _selectableDataPort;
                // Minimum tunable frequency (Hz)
                double _freqRangeMin;
                // Maximum tunable frequency (Hz)
                double _freqRangeMax;
                // Frequency resolution (Hz)
                double _freqRes;
                // Frequency units (Hz)
                double _freqUnits;
                // Source
                int _source;
                // Data port
                int _dataPort;
                // Tuned frequency
                double _frequency;
                // Rate index
                int _rateIndex;
                // UDP destination
                int _udpDestination;
                // VITA 49 framing setting
                int _vitaEnable;
                // VITA 49 stream ID
                unsigned int _streamId;
                // Rate set
                NbddcRateSet _rateSet;

        }; // class NbddcComponent

        /**
         * \brief A dictionary of NBDDC components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, NbddcComponent*> NbddcComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENT_H
