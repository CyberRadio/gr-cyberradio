/***************************************************************************
 * \file RadioHandler.h
 * \brief Defines the basic radio handler interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_RADIOHANDLER_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_RADIOHANDLER_H

#include "LibCyberRadio/Common/BasicDict.h"
#include "LibCyberRadio/Common/BasicList.h"
#include "LibCyberRadio/Driver/Configurable.h"
#include "LibCyberRadio/Driver/DataPort.h"
#include "LibCyberRadio/Driver/DucComponent.h"
#include "LibCyberRadio/Driver/NbddcComponent.h"
#include "LibCyberRadio/Driver/NbddcGroupComponent.h"
#include "LibCyberRadio/Driver/RadioTransport.h"
#include "LibCyberRadio/Driver/SimpleIpSetup.h"
#include "LibCyberRadio/Driver/TransmitterComponent.h"
#include "LibCyberRadio/Driver/TunerComponent.h"
#include "LibCyberRadio/Driver/VitaIfSpec.h"
#include "LibCyberRadio/Driver/WbddcComponent.h"
#include "LibCyberRadio/Driver/WbddcGroupComponent.h"
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
         * \brief Generic radio handler class.
         *
         * The generic radio handler class provides a standard API for manipulating
         * the various radios supported by the driver.  All radio handler objects
         * provided through the driver will conform to this interface.  However, not
         * all radios will support all of the capabilities of this interface.
         *
         * Radio handler objects can also use configuration dictionaries like their
         * components can.  Support for configuration dictionaries varies by radio,
         * so see the documentation for the specific radio handler for details.
         */
        class RadioHandler : public Configurable
        {
            public:
                /**
                 * \brief Constructs a RadioHandler object.
                 * \param name Name of the radio.
                 * \param numTuner Number of tuners on the radio.
                 * \param tunerIndexBase Number that tuner indices start on.
                 * \param numWbddc Number of WBDDCs on the radio.
                 * \param wbddcIndexBase Number that WBDDC indices start on.
                 * \param numNbddc Number of NBDDCs on the radio.
                 * \param nbddcIndexBase Number that NBDDC indices start on.
                 * \param numTunerBoards Number of tuner boards expected to be
                 *    on the radio.
                 * \param maxTunerBw Expected maximum tuner bandwidth.
                 * \param numTransmitter Number of transmitters on the radio.
                 * \param transmitterIndexBase Number that transmitter indices start on.
                 * \param numDuc Number of DUCs on the radio.
                 * \param ducIndexBase Number that DUC indices start on.
                 * \param numWbddcGroups Number of WBDDC groups on the radio.
                 * \param wbddcGroupIndexBase Number that WBDDC group indices start on.
                 * \param numNbddcGroups Number of NBDDC groups on the radio.
                 * \param nbddcGroupIndexBase Number that NBDDC group indices start on.
                 * \param numDdcGroups Number of combined DDC groups on the radio.
                 * \param ddcGroupIndexBase Number that combined DDC group indices start on.
                 * \param numDataPorts Number of 10GigE data ports on the radio.
                 * \param dataPortIndexBase Number that 10GigE data port indices
                 *    start on.
                 * \param numSimpleIpSetups Number of simple IP setups for 1Gig data
                 *    channels.
                 * \param adcRate ADC sample rate, in Hz.
                 * \param ifSpec VITA 49 interface specification for this radio.
                 * \param debug Whether the object supports debug output.
                 */
                RadioHandler(
                        const std::string& name = "NDR",
                        int numTuner = 0,
                        int tunerIndexBase = 1,
                        int numWbddc = 0,
                        int wbddcIndexBase = 1,
                        int numNbddc = 0,
                        int nbddcIndexBase = 1,
                        int numTunerBoards = 1,
                        int maxTunerBw = 0,
                        int numTransmitter = 0,
                        int transmitterIndexBase = 1,
                        int numDuc = 0,
                        int ducIndexBase = 1,
                        int numWbddcGroups = 0,
                        int wbddcGroupIndexBase = 1,
                        int numNbddcGroups = 0,
                        int nbddcGroupIndexBase = 1,
                        int numDdcGroups = 0,
                        int ddcGroupIndexBase = 1,
                        int numDataPorts = 0,
                        int dataPortIndexBase = 1,
                        int numSimpleIpSetups = 0,
                        double adcRate = 102.4e6,
                        VitaIfSpec ifSpec = VitaIfSpec(),
                        bool debug = false
                );
                /**
                 * \brief Destroys a RadioHandler object.
                 */
                virtual ~RadioHandler();
                /**
                 * \brief Copies a RadioHandler object.
                 * \param other The RadioHandler object to copy.
                 */
                RadioHandler(const RadioHandler& other);
                /**
                 * \brief Assignment operator for RadioHandler objects.
                 * \param other The RadioHandler object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual RadioHandler& operator=(const RadioHandler& other);
                /**
                 * \brief Gets whether or not the handler is connected.
                 * \returns True if connected, false otherwise.
                 */
                virtual bool isConnected() const;
                /**
                 * \brief Gets version information for the radio.
                 * \returns The version info dictionary.
                 */
                virtual BasicStringStringDict getVersionInfo();
                /**
                 * \brief Gets connection information for the radio.
                 * \returns The connection info dictionary.
                 */
                virtual BasicStringStringDict getConnectionInfo();
                /**
                 * \brief Connects to the radio.
                 * \param mode Connection mode. One of "tcp", "udp", or "tty".
                 * \param host_or_dev Either the host name or IP address (TCP/UDP) or
                 *    the serial device name (TTY).
                 * \param port_or_baudrate Either the port number (TCP/UDP) or the
                 *    serial baud rate (TTY).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool connect(
                        const std::string& mode,
                        const std::string& host_or_dev,
                        const int port_or_baudrate
                );
                /**
                 * \brief Disconnects from the radio.
                 */
                virtual void disconnect();
                /**
                 * \brief Sends a command to the radio.
                 * \param cmdString The command string.
                 * \param timeout Timeout value (seconds). If this is -1, use the transport's
                 *    default timeout.
                 * \returns A list of response strings from the radio.
                 */
                virtual BasicStringList sendCommand(
                        const std::string& cmdString,
                        double timeout = -1
                );
                /**
                 * \brief Sets the configuration dictionary for this object.
                 *
                 * This method is intended to allow users to change the object's
                 * settings based on the configuration dictionary. It should
                 * not be used to set configuration dictionary elements that the
                 * object does not use.
                 *
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setConfiguration(ConfigurationDict& cfg);
                /**
                 * \brief Tells the radio to query its hardware configuration in
                 *    order to create its configuration dictionary (including the
                 *    dictionaries of any components managed by the radio).
                 */
                virtual void queryConfiguration();
                /**
                 * \brief Gets the error message from the last command attempted.
                 * \returns The error message. This is an empty string if the last command
                 *    executed successfully.
                 */
                virtual std::string getLastCommandErrorInfo() const;
                /**
                 * \brief Resets the radio.
                 * \param resetType The type of reset to perform. Varies by radio.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool sendReset(int resetType=0);
                /**
                 * \brief Gets the pulse-per-second (PPS) rising edge from the radio.
                 * \note This method does not return until the PPS edge occurs.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool getPps();
                /**
                 * \brief Sets the time for the next PPS rising edge on the radio.
                 * \param checkTime Whether to check that the set time is the time we
                 *    wanted.
                 * \param useGpsTime Whether to use the radio's GPS time for this.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTimeNextPps(bool checkTime=false, bool useGpsTime=false);
                /**
                 * \brief Gets the current radio time.
                 * \returns The time, in seconds since the Epoch.
                 */
                virtual time_t getTimeNow();
                /**
                 * \brief Gets the time for the next PPS rising edge on the radio.
                 * \returns The time, in seconds since the Epoch.
                 */
                virtual time_t getTimeNextPps();
                /**
                 * \brief Gets the status from the radio.
                 * \return The status bitmask provided by the radio, as an integer value.
                 *     This command returns 0 if the radio does not support status queries.
                 */
                virtual unsigned int getStatus();
                /**
                 * \brief Gets the tuner status from the radio.
                 * \return The status bitmask provided by the radio, as an integer value.
                 *     This command returns 0 if the radio does not support status queries.
                 */
                virtual unsigned int getTstatus();
                /**
                 * \brief Sets the reference mode on the radio.
                 * \param mode An integer indicating the reference mode to set.  Valid
                 *    reference mode numbers vary by radio.
                 * \return True if successful, false if unsuccessful or if reference mode
                 *    setting is not supported on the radio.
                 */
                virtual bool setReferenceMode(int mode);
                /**
                 * \brief Sets the reference bypass mode on the radio.
                 * \param mode An integer indicating the bypass mode to set.  Valid
                 *    bypass mode numbers vary by radio.
                 * \return True if successful, false if unsuccessful or if bypass mode
                 *    setting is not supported on the radio.
                 */
                virtual bool setBypassMode(int mode);
                /**
                 * \brief Sets the time adjustment for tuners on the radio.
                 *
                 * \param tunerIndex Tuner index number.
                 * \param timeAdjustValue Time adjustment value.
                 * \return True if successful, false if unsuccessful or if adjusting
                 *    the time is not supported.
                 */
                virtual bool setTimeAdjustment(int tunerIndex, int timeAdjustValue);
                /**
                 * \brief Gets the current GPS position the radio.
                 * \returns A 2-element list of floating-point values: [latitude,
                 *    longitude].  Both values are in decimal degrees.  If the
                 *    GPS position is unavailable, this method returns zeros.
                 */
                virtual BasicDoubleList getGpsPosition();
                /**
                 * \brief Gets the current radio temperature.
                 * \return The temperature, in degrees Celsius.  If the radio does
                 *    not support temperature querying, this method returns 0.
                 */
                virtual int getTemperature();
                /**
                 * \brief Gets the current GPIO output bits.
                 * \return The GPIO output bits, as an integer bitmask.  If the GPIO
                 *    module is running in sequence mode, then this value is undefined.
                 */
                virtual int getGpioOutput();
                /**
                 * \brief Gets the GPIO output settings for a given sequence index.
                 * \param index The GPIO sequence index.
                 * \return A list of three integers: (bitmask, duration, loop).
                 */
                virtual BasicIntList getGpioOutputByIndex(int index);
                /**
                 * \brief Sets the current GPIO output bits.
                 * \note Executing this method puts the GPIO module into static mode.
                 * \param value The GPIO output value, as an integer bitmask.
                 * \return True if successful, false if unsuccessful or if setting
                 *    GPIO output is not supported.
                 */
                virtual bool setGpioOutput(int value);
                /**
                 * \brief Sets the GPIO output settings for a given sequence index.
                 * \note Executing this method puts the GPIO module into sequence mode
                 *    if the "go" parameter is 1.
                 * \param index The GPIO sequence index.
                 * \param value The GPIO output value, as an integer bitmask.
                 * \param duration The duration for that value, as a number of ADC
                 *    clock cycles.
                 * \param loop Whether the sequence loops back to the beginning after
                 *    this step (1) or not (0).
                 * \param go Whether to execute the sequence (1) or not (0).
                 * \return True if successful, false if unsuccessful or if setting
                 *    GPIO output is not supported.
                 */
                virtual bool setGpioOutputByIndex(int index, int value,
                        int duration, int loop, int go);
                /**
                 * \brief Gets the calibration frequency.
                 * \returns The calibration frequency, in MHz. A value of 0 means
                 *    that the calibration function is not on.
                 */
                virtual double getCalibrationFrequency() const;
                /**
                 * \brief Sets the calibration frequency.
                 * \param freq The new calibration frequency, in MHz. A value of 0
                 *    turns off the calibration function.
                 * \returns True if the call succeeds, false otherwise.
                 */
                virtual bool setCalibrationFrequency(double freq);
                /**
                 * \brief Gets the number of 10GigE data ports on the radio.
                 * \returns The number of data ports.
                 */
                virtual int getNumDataPorts() const;
                /**
                 * \brief Gets the range of indices 10GigE data ports on the radio.
                 * \returns The list of 10GigE indices.
                 */
                virtual BasicIntList getDataPortIndexRange() const;
                /**
                 * \brief Gets the number of UDP destination table entries for the
                 *    10GigE data ports on the radio.
                 * \returns The number of entries.  Returns 0 if the radio does not
                 *    have 10GigE data ports.
                 */
                virtual int getNumDataPortDipEntries() const;
                /**
                 * \brief Gets the list of UDP destination table indices for the
                 *    10GigE data ports on the radio.
                 * \returns The list of destination indices.
                 */
                virtual BasicIntList getDataPortDipEntryIndexRange() const;
                /**
                 * \brief Gets the list of connection methods that the radio supports.
                 * \returns The mode list.
                 */
                virtual BasicStringList getConnectionModeList() const;
                /**
                 * \brief Gets whether the radio supports the given connection mode.
                 * \returns True if the mode is supported, false otherwise.
                 */
                virtual bool isConnectionModeSupported(const std::string& mode) const;
                /**
                 * \brief Gets the ADC sample rate.
                 * \returns The sample rate, in Hz.
                 */
                virtual double getAdcRate() const;
                /**
                 * \brief Gets the size of the VITA 49 header.
                 * \returns The header size, in bytes.
                 */
                virtual int getVitaHeaderSize() const;
                /**
                 * \brief Gets the size of the VITA 49 payload.
                 * \returns The payload size, in bytes.
                 */
                virtual int getVitaPayloadSize() const;
                /**
                 * \brief Gets the size of the VITA 49 tail.
                 * \returns The tail size, in bytes.
                 */
                virtual int getVitaTailSize() const;
                /**
                 * \brief Gets whether the VITA 49 is byte-swapped with respect
                 *    to the host operating system.
                 * \returns True if byte-swapped, false otherwise.
                 */
                virtual bool isByteswapped() const;
                /**
                 * \brief Gets whether the VITA 49 format swaps real and imaginary
                 *    (I and Q) portions of each sample.
                 * \returns True if I and Q are swapped, false otherwise.
                 */
                virtual bool isIqSwapped() const;
                /**
                 * \brief Gets the byte order (endianness) of the VITA 49.
                 * \returns The byte order, either "little" or "big".
                 */
                virtual const char* getByteOrder() const;
                // getVitaEnableOptionSet()
                /**
                 * \brief Gets the number of tuners on the radio.
                 * \returns The number of tuners.
                 */
                virtual int getNumTuner() const;
                /**
                 * \brief Gets the number of tuner boards on the radio.
                 * \returns The number of tuners.
                 */
                virtual int getNumTunerBoards() const;
                /**
                 * \brief Gets the tuner index range.
                 * \returns A list containing the tuner indices.
                 */
                virtual BasicIntList getTunerIndexRange() const;
                /**
                 * \brief Gets the tunable frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getTunerFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getTunerFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units for tuners.
                 *
                 * The frequency unit is a floating-point value that indicates
                 * how the frequency is specified in commands given to the radio.
                 * <ul>
                 * <li> 1.0: Frequency given in Hz
                 * <li> 1.0e6: Frequency given in MHz
                 * </ul>
                 *
                 * \return The frequency unit.
                 */
                virtual double getTunerFrequencyUnit() const;
                /**
                 * \brief Gets the tuner attenuation range.
                 * \returns A list containing the minimum and maximum attenuation values.
                 */
                virtual BasicDoubleList getTunerAttenuationRange() const;
                /**
                 * \brief Gets the attenuation resolution.
                 * \returns The resolution.
                 */
                virtual double getTunerAttenuationRes() const;
                /**
                 * \brief Gets whether or not a given tuner is enabled.
                 * \param index The tuner index number.
                 * \returns True if the tuner is enabled, false otherwise.
                 */
                virtual bool isTunerEnabled(int index) const;
                /**
                 * \brief Enables a given tuner.
                 * \param index The tuner index number.
                 * \param enabled Whether or not this tuner should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableTuner(int index, bool enabled = true);
                /**
                 * \brief Disables a given tuner.
                 * \param index The tuner index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableTuner(int index);
                /**
                 * \brief Gets the tuned frequency for a given tuner.
                 * \param index The tuner index number.
                 * \returns The tuned frequency, in Hz.
                 */
                virtual double getTunerFrequency(int index) const;
                /**
                 * \brief Sets the tuned frequency for a given tuner.
                 * \param index The tuner index number.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTunerFrequency(int index, double freq);
                /**
                 * \brief Gets the attenuation for a given tuner.
                 * \param index The tuner index number.
                 * \returns The attenuation, in dB.
                 */
                virtual double getTunerAttenuation(int index) const;
                /**
                 * \brief Sets the attenuation for a given tuner.
                 * \param index The tuner index number.
                 * \param atten The new attenuation (dB).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTunerAttenuation(int index, double atten);
                /**
                 * \brief Gets the filter setting for a given tuner.
                 * \param index The tuner index number.
                 * \returns The filter setting.
                 */
                virtual int getTunerFilter(int index) const;
                /**
                 * \brief Sets the filter setting for a given tuner.
                 * \param index The tuner index number.
                 * \param filter The new filter setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTunerFilter(int index, int filter);
                /**
                 * \brief Gets the configuration dictionary for a given tuner.
                 * \param index The tuner index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getTunerConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given tuner.
                 * \param index The tuner index number.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTunerConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the number of WBDDCs on the radio.
                 * \returns The number of WBDDCs.
                 */
                virtual int getNumWbddc() const;
                /**
                 * \brief Gets the range of WBDDC indices on the radio.
                 * \returns A list of WBDDC indices.
                 */
                virtual BasicIntList getWbddcIndexRange() const;
                /**
                 * \brief Gets whether the WBDDCs on this radio are tunable.
                 * \returns True if tunable, false otherwise.
                 */
                virtual bool isWbddcTunable() const;
                /**
                 * \brief Gets whether the WBDDCs on this radio support selecting
                 *    their tuner source.
                 * \returns True if selectable, false otherwise.
                 */
                virtual bool isWbddcSelectableSource() const;
                /**
                 * \brief Gets the tunable frequency range for WBDDCs.
                 * \returns A list containing the minimum and maximum frequencies.
                 *    These numbers have no meaning if the WBDDCs are not tunable.
                 */
                virtual BasicDoubleList getWbddcFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution for WBDDCs.
                 * \returns The frequency resolution, in Hz.  This value has no
                 *    meaning if the WBDDCs are not tunable.
                 */
                virtual double getWbddcFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units for WBDDCs.
                 *
                 * The frequency unit is a floating-point value that indicates
                 * how the frequency is specified in commands given to the radio.
                 * <ul>
                 * <li> 1.0: Frequency given in Hz
                 * <li> 1.0e6: Frequency given in MHz
                 * </ul>
                 *
                 * \return The frequency unit.
                 */
                virtual double getWbddcFrequencyUnit() const;
                /**
                 * \brief Gets the WBDDC rate set.
                 * \returns The rate set.
                 */
                virtual WbddcRateSet getWbddcRateSet() const;
                /**
                 * \brief Gets the list of allowed WBDDC sample rates, based on the
                 *    rate set.
                 * \returns The rate list.
                 */
                virtual BasicDoubleList getWbddcRateList() const;
                /**
                 * \brief Gets whether or not a given WBDDC is enabled.
                 * \param index WBDDC index number.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isWbddcEnabled(int index) const;
                /**
                 * \brief Enables a given WBDDC.
                 * \param index WBDDC index number.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableWbddc(int index, bool enabled = true);
                /**
                 * \brief Disables a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableWbddc(int index);
                /**
                 * \brief Gets the tuned frequency for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The tuned frequency, in Hz.  This value has no meaning if
                 *    the WBDDC is not tunable.
                 */
                virtual double getWbddcFrequency(int index) const;
                /**
                 * \brief Sets the tuned frequency for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.  Returns
                 *    false if the WBDDC is not tunable.
                 */
                virtual bool setWbddcFrequency(int index, double freq);
                /**
                 * \brief Gets the source (which tuner is supplying the signal) for
                 *    a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The source index.  This value has no meaning if the WBDDC
                 *    does not support selectable source.
                 */
                virtual int getWbddcSource(int index) const;
                /**
                 * \brief Sets the source (which tuner is supplying the signal) for
                 *    a given WBDDC.
                 * \param index WBDDC index number.
                 * \param source The new WBDDC source index.
                 * \returns True if successful, false otherwise.  Returns false if the
                 *    WBDDC does not support selectable source.
                 */
                virtual bool setWbddcSource(int index, int source);
                /**
                 * \brief Gets the rate index for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The rate index.
                 */
                virtual int getWbddcRateIndex(int index) const;
                /**
                 * \brief Sets the rate index for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param rateIndex The new rate index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcRateIndex(int index, int rateIndex);
                /**
                 * \brief Gets the UDP destination for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The UDP destination.
                 */
                virtual int getWbddcUdpDestination(int index) const;
                /**
                 * \brief Sets the UDP destination for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param dest The new UDP destination.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcUdpDestination(int index, int dest);
                /**
                 * \brief Gets the VITA 49 setting for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The VITA 49 setting.
                 */
                virtual int getWbddcVitaEnable(int index) const;
                /**
                 * \brief Sets the VITA 49 setting for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param enable The new VITA 49 setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcVitaEnable(int index, int enable);
                /**
                 * \brief Gets the VITA 49 stream ID for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The VITA 49 stream ID.
                 */
                virtual unsigned int getWbddcStreamId(int index) const;
                /**
                 * \brief Sets the VITA 49 stream ID for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param sid The new stream ID.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcStreamId(int index, unsigned int sid);
                /**
                 * \brief Gets the data port for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The data port. This number has no meaning if the
                 *    radio does not use data ports.
                 */
                virtual int getWbddcDataPort(int index) const;
                /**
                 * \brief Sets the data port for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param port The new data port.
                 * \returns True if successful, false otherwise. Returns false
                 *    if the radio does not use data ports.
                 */
                virtual bool setWbddcDataPort(int index, int port);
                /**
                 * \brief Sets the rate set for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param set The new rate set.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcRateSet(int index, const WbddcRateSet& set);
                /**
                 * \brief Gets the configuration dictionary for a given WBDDC.
                 * \param index WBDDC index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getWbddcConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given WBDDC.
                 * \param index WBDDC index number.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the number of NBDDCs on the radio.
                 * \returns The number of NBDDCs.
                 */
                virtual int getNumNbddc() const;
                /**
                 * \brief Gets the range of NBDDC indices on the radio.
                 * \returns A list of NBDDC indices.
                 */
                virtual BasicIntList getNbddcIndexRange() const;
                /**
                 * \brief Gets the tunable frequency range for NBDDCs.
                 * \returns A list containing the minimum and maximum frequencies.
                 *    These numbers have no meaning if the NBDDCs are not tunable.
                 */
                virtual BasicDoubleList getNbddcFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution for NBDDCs.
                 * \returns The frequency resolution, in Hz.  This value has no
                 *    meaning if the NBDDCs are not tunable.
                 */
                virtual double getNbddcFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units for NBDDCs.
                 *
                 * The frequency unit is a floating-point value that indicates
                 * how the frequency is specified in commands given to the radio.
                 * <ul>
                 * <li> 1.0: Frequency given in Hz
                 * <li> 1.0e6: Frequency given in MHz
                 * </ul>
                 *
                 * \return The frequency unit.
                 */
                virtual double getNbddcFrequencyUnit() const;
                /**
                 * \brief Gets the NBDDC rate set.
                 * \returns The rate set.
                 */
                virtual NbddcRateSet getNbddcRateSet() const;
                /**
                 * \brief Gets the list of allowed NBDDC sample rates, based on the
                 *    rate set.
                 * \returns The rate list.
                 */
                virtual BasicDoubleList getNbddcRateList() const;
                /**
                 * \brief Gets whether or not a given NBDDC is enabled.
                 * \param index NBDDC index number.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isNbddcEnabled(int index) const;
                /**
                 * \brief Enables a given NBDDC.
                 * \param index NBDDC index number.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableNbddc(int index, bool enabled = true);
                /**
                 * \brief Disables a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableNbddc(int index);
                /**
                 * \brief Gets the tuned frequency for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The tuned frequency, in Hz.  This value has no meaning if
                 *    the NBDDC is not tunable.
                 */
                virtual double getNbddcFrequency(int index) const;
                /**
                 * \brief Sets the tuned frequency for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.  Returns
                 *    false if the NBDDC is not tunable.
                 */
                virtual bool setNbddcFrequency(int index, double freq);
                /**
                 * \brief Gets the source (which tuner is supplying the signal) for
                 *    a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The source index.  This value has no meaning if the NBDDC
                 *    does not support selectable source.
                 */
                virtual int getNbddcSource(int index) const;
                /**
                 * \brief Sets the source (which tuner is supplying the signal) for
                 *    a given NBDDC.
                 * \param index NBDDC index number.
                 * \param source The new NBDDC source index.
                 * \returns True if successful, false otherwise.  Returns false if the
                 *    NBDDC does not support selectable source.
                 */
                virtual bool setNbddcSource(int index, int source);
                /**
                 * \brief Gets the rate index for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The rate index.
                 */
                virtual int getNbddcRateIndex(int index) const;
                /**
                 * \brief Sets the rate index for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param rateIndex The new rate index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcRateIndex(int index, int rateIndex);
                /**
                 * \brief Gets the UDP destination for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The UDP destination.
                 */
                virtual int getNbddcUdpDestination(int index) const;
                /**
                 * \brief Sets the UDP destination for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param dest The new UDP destination.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcUdpDestination(int index, int dest);
                /**
                 * \brief Gets the VITA 49 setting for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The VITA 49 setting.
                 */
                virtual int getNbddcVitaEnable(int index) const;
                /**
                 * \brief Sets the VITA 49 setting for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param enable The new VITA 49 setting.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcVitaEnable(int index, int enable);
                /**
                 * \brief Gets the VITA 49 stream ID for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The VITA 49 stream ID.
                 */
                virtual unsigned int getNbddcStreamId(int index) const;
                /**
                 * \brief Sets the VITA 49 stream ID for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param sid The new stream ID.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcStreamId(int index, unsigned int sid);
                /**
                 * \brief Gets the data port for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The data port. This number has no meaning if the
                 *    radio does not use data ports.
                 */
                virtual int getNbddcDataPort(int index) const;
                /**
                 * \brief Sets the data port for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param port The new data port.
                 * \returns True if successful, false otherwise. Returns false
                 *    if the radio does not use data ports.
                 */
                virtual bool setNbddcDataPort(int index, int port);
                /**
                 * \brief Sets the rate set for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param set The new rate set.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcRateSet(int index, const NbddcRateSet& set);
                /**
                 * \brief Gets the configuration dictionary for a given NBDDC.
                 * \param index NBDDC index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getNbddcConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given NBDDC.
                 * \param index NBDDC index number.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the number of transmitters on the radio.
                 * \returns The number of transmitters.
                 */
                virtual int getNumTransmitters() const;
                /**
                 * \brief Gets the list of transmitter indices on the radio.
                 * \returns The list of transmitter indices.
                 */
                virtual BasicIntList getTransmitterIndexRange() const;
                /**
                 * \brief Gets the frequency range for the transmitters on the radio.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getTransmitterFrequencyRange() const;
                /**
                 * \brief Gets the frequency resolution for transmitters on the radio.
                 * \returns The frequency resolution.
                 */
                virtual double getTransmitterFrequencyRes() const;
                /**
                 * \brief Gets the frequency unit for transmitters on the radio.
                 *
                 * The frequency unit is a floating-point value that indicates
                 * how the frequency is specified in commands given to the radio.
                 * <ul>
                 * <li> 1.0: Frequency given in Hz
                 * <li> 1.0e6: Frequency given in MHz
                 * </ul>
                 *
                 * \return The frequency unit.
                 */
                virtual double getTransmitterFrequencyUnit() const;
                /**
                 * \brief Gets the attenuation range for the transmitters on the radio.
                 *
                 * \return A list containing the minimum and maximum attenuation values.
                 */
                virtual BasicDoubleList getTransmitterAttenuationRange() const;
                /**
                 * \brief Gets the attenuation resolution for transmitters on the radio.
                 * \returns The attenuation resolution.
                 */
                virtual double getTransmitterAttenuationRes() const;
                /**
                 * \brief Gets whether a given transmitter is enabled.
                 * \param index Transmitter index.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isTransmitterEnabled(int index) const;
                /**
                 * \brief Enables a given transmitter.
                 * \param index Transmitter index.
                 * \param enabled Whether or not to enable the transmitter.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableTransmitter(int index, bool enabled = true);
                /**
                 * \brief Disables a given transmitter.
                 * \param index Transmitter index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableTransmitter(int index);
                /**
                 * \brief Gets the frequency for a given transmitter.
                 * \param index Transmitter index.
                 * \returns The frequency (Hz).
                 */
                virtual double getTransmitterFrequency(int index) const;
                /**
                 * \brief Sets the frequency for a given transmitter.
                 * \param index Transmitter index.
                 * \param freq The new transmitter frequency, in Hz.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterFrequency(int index, double freq);
                /**
                 * \brief Gets the attenuation for a given transmitter.
                 * \param index Transmitter index.
                 * \returns The attenuation (dB).
                 */
                virtual double getTransmitterAttenuation(int index) const;
                /**
                 * \brief Sets the attenuation for a given transmitter.
                 * \param index Transmitter index.
                 * \param atten The new attenuation, in dB.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterAttenuation(int index, double atten);
                /**
                 * \brief Gets the configuration dictionary for a given transmitter.
                 * \param index Transmitter index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getTransmitterConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given transmitter.
                 * \param index Transmitter index number.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets whether transmitters support continuous-wave (CW) tone
                 *    generation.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool transmitterSupportsCW() const;
                /**
                 * \brief Gets the number of CW tone generators associated with
                 *     transmitters on this radio.
                 * \returns The number of generators.
                 */
                virtual int getTransmitterCWNum() const;
                /**
                 * \brief Gets the range of indices for CW tone generators.
                 * \returns A list containing the generator indices.
                 */
                virtual BasicIntList getTransmitterCWIndexRange() const;
                /**
                 * \brief Gets the CW frequency range.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getTransmitterCWFrequencyRange() const;
                /**
                 * \brief Gets the CW frequency resolution.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getTransmitterCWFrequencyRes() const;
                /**
                 * \brief Gets the CW amplitude range.
                 * \returns A list containing the minimum and maximum amplitude values.
                 */
                virtual BasicDoubleList getTransmitterCWAmplitudeRange() const;
                /**
                 * \brief Gets the CW amplitude resolution.
                 * \returns The resolution.
                 */
                virtual double getTransmitterCWAmplitudeRes() const;
                /**
                 * \brief Gets the CW phase range.
                 * \returns A list containing the minimum and maximum phase values.
                 */
                virtual BasicDoubleList getTransmitterCWPhaseRange() const;
                /**
                 * \brief Gets the CW phase resolution.
                 * \returns The resolution.
                 */
                virtual int getTransmitterCWPhaseRes() const;
                /**
                 * \brief Gets whether the transmitter supports CW tone sweeping.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool transmitterSupportsCWSweep() const;
                /**
                 * \brief Gets the CW start frequency range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getTransmitterCWSweepStartRange() const;
                /**
                 * \brief Gets the CW start frequency resolution.
                 * \returns The resolution.
                 */
                virtual double getTransmitterCWSweepStartRes() const;
                /**
                 * \brief Gets the CW stop frequency range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getTransmitterCWSweepStopRange() const;
                /**
                 * \brief Gets the CW stop frequency resolution.
                 * \returns The resolution.
                 */
                virtual double getTransmitterCWSweepStopRes() const;
                /**
                 * \brief Gets the CW frequency step range.
                 * \returns A list containing the minimum and maximum frequency values.
                 */
                virtual BasicDoubleList getTransmitterCWSweepStepRange() const;
                /**
                 * \brief Gets the CW frequency step resolution.
                 * \returns The resolution.
                 */
                virtual double getTransmitterCWSweepStepRes() const;
                /**
                 * \brief Gets the CW dwell time range.
                 * \returns A list containing the minimum and maximum dwell time values.
                 */
                virtual BasicDoubleList getTransmitterCWSweepDwellRange() const;
                /**
                 * \brief Gets the CW dwell time resolution.
                 * \returns The resolution.
                 */
                virtual double getTransmitterCWSweepDwellRes() const;
                /**
                 * \brief Enables a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableTransmitterCW(int index, int cwIndex,
                        bool enabled = true);
                /**
                 * \brief Disables a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableTransmitterCW(int index, int cwIndex);
                /**
                 * \brief Gets the configuration for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getTransmitterCWConfiguration(int index,
                        int cwIndex) const;
                /**
                 * \brief Sets the configuration dictionary for a given CW tone
                 *    generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterCWConfiguration(int index, int cwIndex,
                        ConfigurationDict& cfg);
                /**
                 * \brief Gets the constant frequency for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The constant frequency, in Hz.
                 */
                virtual double getTransmitterCWFrequency(int index, int cwIndex) const;
                /**
                 * \brief Sets the constant frequency for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param freq The new constant frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterCWFrequency(int index, int cwIndex, double freq);
                /**
                 * \brief Gets the signal amplitude for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The signal amplitude, in scale units.
                 */
                virtual double getTransmitterCWAmplitude(int index, int cwIndex) const;
                /**
                 * \brief Sets the signal amplitude for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param amp The new signal amplitude (scale units).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterCWAmplitude(int index, int cwIndex, double amp);
                /**
                 * \brief Gets the signal phase for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The signal phase, in degrees.
                 */
                virtual double getTransmitterCWPhase(int index, int cwIndex) const;
                /**
                 * \brief Sets the signal phase for a given CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param phase The new signal phase (degrees).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterCWPhase(int index, int cwIndex, double phase);
                /**
                 * \brief Gets whether or not a given CW tone generator supports
                 *    signal sweeps.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool transmitterSupportsCWSweep(int index, int cwIndex) const;
                /**
                 * \brief Gets the start frequency for a signal sweep for a given
                 *    CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The start frequency, in Hz.
                 */
                virtual double getTransmitterCWSweepStartFrequency(int index, int cwIndex) const;
                /**
                 * \brief Gets the stop frequency for a signal sweep for a given
                 *    CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The stop frequency, in Hz.
                 */
                virtual double getTransmitterCWSweepStopFrequency(int index, int cwIndex) const;
                /**
                 * \brief Gets the frequency step for a signal sweep for a given
                 *    CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The frequency step, in Hz.
                 */
                virtual double getTransmitterCWSweepFrequencyStep(int index, int cwIndex) const;
                /**
                 * \brief Gets the dwell time for a signal sweep for a given
                 *    CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \returns The dwell time, in ADC samples.
                 */
                virtual double getTransmitterCWSweepDwellTime(int index, int cwIndex) const;
                /**
                 * \brief Sets the parameters for a frequency sweep for a given
                 *    CW tone generator.
                 * \param index Transmitter index.
                 * \param cwIndex CW tone generator index.
                 * \param start The new start frequency (Hz).
                 * \param stop The new stop frequency (Hz).
                 * \param step The new frequency step (Hz).
                 * \param dwell The new dwell time (ADC samples).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTransmitterCWFrequencySweep(int index, int cwIndex, double start,
                        double stop, double step, double dwell);
                /**
                 * \brief Gets the number of DUCs on the radio.
                 * \returns The number of DUCs.
                 */
                virtual int getNumDuc() const;
                /**
                 * \brief Gets the range of DUC indices on the radio.
                 * \returns A list of DUC indices.
                 */
                virtual BasicIntList getDucIndexRange() const;
                /**
                 * \brief Gets whether DUCs support loading snapshot files.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool ducSupportsSnapshotLoad() const;
                /**
                 * \brief Gets whether DUCs support transmitting snapshots.
                 * \returns True if supported, false otherwise.
                 */
                virtual bool ducSupportsSnapshotTransmit() const;
                /**
                 * \brief Enables a given DUC.
                 * \param index The DUC index number.
                 * \param enabled Whether or not the DUC should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableDuc(int index, bool enabled);
                /**
                 * \brief Disables a given DUC.
                 * \param index The DUC index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableDuc(int index);
                /**
                 * \brief Gets the configuration dictionary for a given DUC.
                 * \param index DUC index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getDucConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given DUC.
                 * \param index The DUC index number.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the data port for a given DUC.
                 * \param index The DUC index number.
                 * \returns The data port.
                 */
                virtual int getDucDataPort(int index) const;
                /**
                 * \brief Sets the data port for a given DUC.
                 * \param index The DUC index number.
                 * \param port The new data port. Setting this to 0 disables
                 *    streaming.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucDataPort(int index, int port);
                /**
                 * \brief Gets the tuned frequency for a given DUC.
                 * \param index The DUC index number.
                 * \returns The tuned frequency, in Hz.
                 */
                virtual double getDucFrequency(int index) const;
                /**
                 * \brief Sets the tuned frequency for a given DUC.
                 * \param index The DUC index number.
                 * \param freq The new tuned frequency (Hz).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucFrequency(int index, double freq);
                /**
                 * \brief Gets the tunable frequency range for DUCs.
                 * \returns A list containing the minimum and maximum frequencies.
                 */
                virtual BasicDoubleList getDucFrequencyRange() const;
                /**
                 * \brief Gets the tuned frequency resolution for DUCs.
                 * \returns The frequency resolution, in Hz.
                 */
                virtual double getDucFrequencyRes() const;
                /**
                 * \brief Gets the tuned frequency units for DUCs.
                 * \returns The frequency units, in Hz.
                 */
                virtual double getDucFrequencyUnit() const;
                /**
                 * \brief Gets the attenuation for a given DUC.
                 * \param index The DUC index number.
                 * \returns The attenuation, in dB.
                 */
                virtual double getDucAttenuation(int index) const;
                /**
                 * \brief Sets the attenuation for a given DUC.
                 * \param index The DUC index number.
                 * \param atten The new attenuation (dB).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucAttenuation(int index, double atten);
                /**
                 * \brief Gets the DUC attenuation range.
                 * \returns A list containing the minimum and maximum attenuation values.
                 */
                virtual BasicDoubleList getDucAttenuationRange() const;
                /**
                 * \brief Gets the DUC attenuation resolution.
                 * \returns The resolution.
                 */
                virtual double getDucAttenuationRes() const;
                /**
                 * \brief Gets the rate index for a given DUC.
                 * \param index The DUC index number.
                 * \returns The rate index.
                 */
                virtual int getDucRateIndex(int index) const;
                /**
                 * \brief Sets the rate index for a given DUC.
                 * \param index The DUC index number.
                 * \param rateIndex The new rate index.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucRateIndex(int index, int rateIndex);
                /**
                 * \brief Gets the transmit channel bitmap for a given DUC.
                 * \param index The DUC index number.
                 * \returns Bitmap indicating which transmitters are outputting the
                 *    signal from this DUC.  If a bit position is 1, the associated
                 *    transmitter is active. The LSB corresponds to TX 1, and each
                 *    succeeding bit corresponds to the other transmitters.
                 */
                virtual int getDucTxChannelBitmap(int index) const;
                /**
                 * \brief Sets the transmit channel bitmap for a given DUC.
                 * \param index The DUC index number.
                 * \param txChannels Bitmap indicating which transmitters output the
                 *    signal from this DUC.  Setting a bit position to 1 enables transmit
                 *    on the associated transmitter. The LSB corresponds to TX 1, and each
                 *    succeeding bit corresponds to the other transmitters.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucTxChannelBitmap(int index, int txChannels);
                /**
                 * \brief Gets the mode for a given DUC.
                 * \param index The DUC index number.
                 * \returns The mode.  This is either 0 (streaming) or 1 (playback).
                 */
                virtual int getDucMode(int index) const;
                /**
                 * \brief Sets the mode for a given DUC.
                 * \param index The DUC index number.
                 * \param mode The new mode.  This is either 0 (streaming) or 1 (playback).
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucMode(int index, int mode);
                /**
                 * \brief Gets the VITA 49 stream ID for a given DUC.
                 * \param index The DUC index number.
                 * \returns The VITA 49 stream ID.
                 */
                virtual unsigned int getDucStreamId(int index) const;
                /**
                 * \brief Sets the VITA 49 stream ID for a given DUC.
                 * \param index The DUC index number.
                 * \param sid The new stream ID.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDucStreamId(int index, unsigned int sid);
                /**
                 * \brief Load a snapshot file into a given DUC's memory block.
                 *
                 * Snapshot files contain 16-bit complex I/Q data samples.
                 *
                 * \param index The DUC index number.
                 * \param filename Snapshot file name.  The snapshot file needs to be
                 *    present on the radio.
                 * \param startSample Starting address in DUC's memory block.  Must
                 *    be a multiple of 1024.
                 * \param samples Number of I/Q samples to load.  Must be a multiple
                 *    of 16.  If specified as 0, load the maximum number of samples
                 *    from the file.
                 * \returns True if successful, false otherwise.  Returns false if
                 *    the DUC does not support snapshot loading.
                 */
                virtual bool loadDucSnapshot(int index,
                        const std::string& filename,
                        unsigned int startSample = 0,
                        unsigned int samples = 0
                );
                /**
                 * \brief Gets the DUC's rate set.
                 * \returns The rate set.
                 */
                virtual DucRateSet getDucRateSet() const;
                /**
                 * \brief Gets the list of allowed DUC sample rates, based on the
                 *    rate set.
                 * \returns The rate list.
                 */
                virtual BasicDoubleList getDucRateList() const;
                /**
                 * \brief Gets the number of WBDDC groups on the radio.
                 * \returns The number of WBDDC groups.
                 */
                virtual int getNumWbddcGroups() const;
                /**
                 * \brief Gets the range of WBDDC group indices on the radio.
                 * \returns A list of WBDDC group indices.
                 */
                virtual BasicIntList getWbddcGroupIndexRange() const;
                /**
                 * \brief Gets whether or not a given WBDDC group is enabled.
                 * \param index WBDDC group index number.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isWbddcGroupEnabled(int index) const;
                /**
                 * \brief Enables a given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \param enabled Whether or not the WBDDC group should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableWbddcGroup(int index, bool enabled);
                /**
                 * \brief Disables a given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableWbddcGroup(int index);
                /**
                 * \brief Gets the configuration dictionary for a given WBDDC group.
                 * \param index WBDDC group index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getWbddcGroupConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcGroupConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the list of group members for a given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \returns List of WBDDC group members.
                 */
                virtual BasicIntList getWbddcGroupMembers(int index) const;
                /**
                 * \brief Sets the list of group members for a given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \param groupMembers List of WBDDC group members.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setWbddcGroupMembers(int index, const BasicIntList& groupMembers);
                /**
                 * \brief Adds a WBDDC to the given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \param member WBDDC to add.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool addWbddcGroupMember(int index, int member);
                /**
                 * \brief Removes a WBDDC from the given WBDDC group.
                 * \param index The WBDDC group index number.
                 * \param member WBDDC to remove.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool removeWbddcGroupMember(int index, int member);
                /**
                 * \brief Gets the number of NBDDC groups on the radio.
                 * \returns The number of NBDDC groups.
                 */
                virtual int getNumNbddcGroups() const;
                /**
                 * \brief Gets the range of NBDDC group indices on the radio.
                 * \returns A list of NBDDC group indices.
                 */
                virtual BasicIntList getNbddcGroupIndexRange() const;
                /**
                 * \brief Gets whether or not a given NBDDC group is enabled.
                 * \param index NBDDC group index number.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isNbddcGroupEnabled(int index) const;
                /**
                 * \brief Enables a given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \param enabled Whether or not the NBDDC group should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableNbddcGroup(int index, bool enabled);
                /**
                 * \brief Disables a given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableNbddcGroup(int index);
                /**
                 * \brief Gets the configuration dictionary for a given NBDDC group.
                 * \param index NBDDC group index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getNbddcGroupConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \param cfg The component configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcGroupConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the list of group members for a given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \returns List of NBDDC group members.
                 */
                virtual BasicIntList getNbddcGroupMembers(int index) const;
                /**
                 * \brief Sets the list of group members for a given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \param groupMembers List of NBDDC group members.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setNbddcGroupMembers(int index, const BasicIntList& groupMembers);
                /**
                 * \brief Adds a NBDDC to the given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \param member NBDDC to add.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool addNbddcGroupMember(int index, int member);
                /**
                 * \brief Removes a NBDDC from the given NBDDC group.
                 * \param index The NBDDC group index number.
                 * \param member NBDDC to remove.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool removeNbddcGroupMember(int index, int member);
                /**
                 * \brief Disables flow control on all 10GigE data ports.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableTenGigFlowControl();
                /**
                 * \brief Enables flow control on all 10GigE data ports.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableTenGigFlowControl();
                /**
                 * \brief Sets flow control status on all 10GigE data ports.
                 * \param enable True if flow control should be enabled, false if not.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setTenGigFlowControlStatus(bool enable);
                /**
                 * \brief Gets flow control status on all 10GigE data ports.
                 * \returns A dictionary of flow control statuses (Booleans) keyed
                 *    by data port indices (integers).
                 */
                virtual BasicIntBoolDict getTenGigFlowControlStatus();
                /**
                 * \brief Gets the configuration dictionary for a given data port.
                 * \param index Data port index number.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getDataPortConfiguration(int index) const;
                /**
                 * \brief Sets the configuration dictionary for a given data port.
                 *
                 * \param index Data port index number.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortConfiguration(int index, ConfigurationDict& cfg);
                /**
                 * \brief Gets the source IP address for a given data port.
                 * \param index Data port index number.
                 * \returns The source IP address.
                 */
                virtual std::string getDataPortSourceIP(int index) const;
                /**
                 * \brief Sets the source IP address for a given data port.
                 * \param index Data port index number.
                 * \param ipAddr The new source IP address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortSourceIP(int index, const std::string& ipAddr);
                /**
                 * \brief Enables errors on the data port.
                 * \param index Data port index number.
                 * \param enabled Whether or not errors should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableDataPortErrors(int index, bool enabled = true);
                /**
                 * \brief Disables errors on the data port.
                 * \param index Data port index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableDataPortErrors(int index);
                /**
                 * \brief Enables flow control on the data port.
                 * \param index Data port index number.
                 * \param enabled Whether or not errors should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableDataPortFlowControl(int index, bool enabled = true);
                /**
                 * \brief Disables flow control on the data port.
                 * \param index Data port index number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableDataPortFlowControl(int index);
                /**
                 * \brief Gets the MAC address for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The MAC address.
                 */
                virtual std::string getDataPortDestMACAddress(int index, int dipIndex) const;
                /**
                 * \brief Sets the MAC address for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param macAddr The new MAC address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortDestMACAddress(int index, int dipIndex,
                        const std::string& macAddr);
                /**
                 * \brief Gets the IP address for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The IP address.
                 */
                virtual std::string getDataPortDestIPAddress(int index, int dipIndex) const;
                /**
                 * \brief Sets the IP address for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param ipAddr The new IP address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortDestIPAddress(int index, int dipIndex,
                        const std::string& ipAddr);
                /**
                 * \brief Gets the source UDP port number for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The port number.
                 */
                virtual unsigned int getDataPortDestSourcePort(int index, int dipIndex) const;
                /**
                 * \brief Sets the UDP port number for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param sourcePort The source UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortDestSourcePort(int index, int dipIndex,
                        unsigned int sourcePort);
                /**
                 * \brief Gets the destination UDP port number for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The stream ID.
                 */
                virtual unsigned int getDataPortDestDestPort(int index, int dipIndex) const;
                /**
                 * \brief Sets the VITA stream ID for a given entry in the
                 *    destination IP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param destPort The destination UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortDestDestPort(int index, int dipIndex,
                        unsigned int destPort);
                /**
                 * \brief Sets the destination table information for a given entry
                 *    in the DIP table on a given data port.
                 * \param index Data port index number.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param ipAddr The IP address.
                 * \param macAddr The MAC address.
                 * \param sourcePort The source UDP port number.
                 * \param destPort The destination UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDataPortDestInfo(int index,
                        int dipIndex,
                        const std::string& ipAddr,
                        const std::string& macAddr,
                        unsigned int sourcePort,
                        unsigned int destPort);
                /**
                 * \brief Gets the "simple" IP configuration dictionary for
                 *     radios without 10Gig data ports.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getSimpleIPConfiguration() const;
                /**
                 * \brief Sets the "simple" IP configuration dictionary for
                 *     radios without 10Gig data ports.
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setSimpleIPConfiguration(ConfigurationDict& cfg);
                /**
                 * \brief Gets the source MAC address for radios without
                 *     10Gig data ports.
                 * \returns The source MAC address [string]
                 */
                virtual std::string getSimpleSourceMACAddress() const;
                /**
                 * \brief Gets the source IP address for radios without
                 *     10Gig data ports.
                 * \returns The source IP address [string]
                 */
                virtual std::string getSimpleSourceIPAddress() const;
                /**
                 * \brief Sets the source IP address for radios without
                 *     10Gig data ports.
                 * \param ipAddr The IP address [string]
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setSimpleSourceIPAddress(const std::string& ipAddr);
                /**
                 * \brief Gets the destination MAC address for radios without
                 *     10Gig data ports.
                 * \returns The destination MAC address [string]
                 */
                virtual std::string getSimpleDestMACAddress() const;
                /**
                 * \brief Sets the destination MAC address for radios without
                 *     10Gig data ports.
                 * \param macAddr The MAC address [string]
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setSimpleDestMACAddress(const std::string& macAddr);
                /**
                 * \brief Gets the destination IP address for radios without
                 *     10Gig data ports.
                 * \returns The destination IP address [string]
                 */
                virtual std::string getSimpleDestIPAddress() const;
                /**
                 * \brief Sets the destination IP address for radios without
                 *     10Gig data ports.
                 * \param ipAddr The IP address [string]
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setSimpleDestIPAddress(const std::string& ipAddr);
                /**
                 * \brief Gets the default device information.
                 *
                 * The default device information is either a default
                 * port to use for network connections, or a default
                 * baud rate to use for serial connections.
                 *
                 * \returns Default device info [integer]
                 */
                virtual int getDefaultDeviceInfo() const;

            protected:
                /**
                 * \brief Initializes the configuration dictionary, defining the allowed
                 *    keys.
                 *
                 * Derived classes should use this method to define which settings
                 *    are configurable through a configuration dictionary.
                 *
                 * \note Derived classes must also call this method explicitly in
                 *    order to initialize their configuration dictionary.
                 */
                virtual void initConfigurationDict();
                /**
                 * \brief Updates the configuration dictionary from object settings.
                 *
                 * Derived classes should use this method to convert the object's
                 * configurable settings into a configuration dictionary.
                 */
                virtual void updateConfigurationDict();
                // Queries the radio for its version information.
                virtual bool queryVersionInfo();
                // Queries the radio for its specific configuration information.
                // Individual radios should override this as necessary.
                virtual bool queryRadioConfiguration();
                // Executes the *IDN? query on the radio.
                virtual bool executeQueryIDN(std::string& model,
                        std::string& serialNumber);
                // Executes the VER? query on the radio.
                virtual bool executeQueryVER(std::string& softwareVersion,
                        std::string& firmwareVersion,
                        std::string& referenceVersion,
                        std::string& firmwareDate);
                // Executes the HREV? query on the radio.
                virtual bool executeQueryHREV(std::string& hardwareInfo);
                // Executes the reset command on the radio.
                // Override this as needed for radios that support this command.
                virtual bool executeResetCommand(int resetType=0);
                // Executes the PPS command on the radio.
                // Override this as needed for radios that support this command.
                virtual bool executePpsQuery();
                // Executes the time query on the radio.
                // Override this as needed for radios that support this command.
                // Time is an in/out parameter
                virtual bool executeTimeQuery(std::string& timeStr);
                // Executes the time command on the radio.
                // Override this as needed for radios that support this command.
                // Time is an in/out parameter
                virtual bool executeTimeCommand(std::string& timeStr);
                // Executes the GPS time query on the radio.
                // Override this as needed for radios that support this command.
                // Time is an in/out parameter
                virtual bool executeGpsTimeQuery(std::string& timeStr);
                // Executes the config mode query on the radio.
                // Override this as needed for radios that support this command.
                // Config mode is an in/out parameter
                virtual bool executeConfigModeQuery(int& configMode);
                // Executes the config mode command on the radio.
                // Override this as needed for radios that support this command.
                // Config mode is an input parameter
                virtual bool executeConfigModeCommand(int& configMode);
                // Executes the coherent mode query on the radio.
                // Override this as needed for radios that support this command.
                // Coherent mode is an in/out parameter
                virtual bool executeCoherentModeQuery(int& coherentMode);
                // Executes the coherent mode command on the radio.
                // Override this as needed for radios that support this command.
                // Coherent mode is an in/out parameter
                virtual bool executeCoherentModeCommand(int& coherentMode);
                // Executes the frequency normalization query on the radio.
                // Override this as needed for radios that support this command.
                // FNR mode is an in/out parameter
                virtual bool executeFreqNormalizationQuery(int& fnrMode);
                // Executes the frequency normalization command on the radio.
                // Override this as needed for radios that support this command.
                // FNR mode is an in/out parameter
                virtual bool executeFreqNormalizationCommand(int& fnrMode);
                // Executes the GPS enabled query on the radio.
                // Override this as needed for radios that support this command.
                // GPS mode is an in/out parameter
                virtual bool executeGpsEnabledQuery(int& enabled);
                // Executes the GPS enabled command on the radio.
                // Override this as needed for radios that support this command.
                // GPS mode is an in/out parameter
                virtual bool executeGpsEnabledCommand(int& enabled);
                // Executes the GPS position query on the radio.
                // Override this as needed for radios that support this command.
                // GPS position are in/out parameters
                virtual bool executeGpsPositionQuery(double& lat, double& lon);
                // Executes the reference mode query on the radio.
                // Override this as needed for radios that support this command.
                // Ref mode is an in/out parameter
                virtual bool executeReferenceModeQuery(int& refMode);
                // Executes the reference mode command on the radio.
                // Override this as needed for radios that support this command.
                // Ref mode is an in/out parameter
                virtual bool executeReferenceModeCommand(int& refMode);
                // Executes the reference bypass query on the radio.
                // Override this as needed for radios that support this command.
                // Ref bypass is an in/out parameter
                virtual bool executeReferenceBypassQuery(int& bypassMode);
                // Executes the reference bypass command on the radio.
                // Override this as needed for radios that support this command.
                // Ref bypass is an in/out parameter
                virtual bool executeReferenceBypassCommand(int& bypassMode);
                // Executes the reference tuning voltage query on the radio.
                // Override this as needed for radios that support this command.
                // Ref tuning voltage is an in/out parameter
                virtual bool executeReferenceVoltageQuery(int& voltage);
                // Executes the reference tuning voltage command on the radio.
                // Override this as needed for radios that support this command.
                // Ref tuning voltage is an in/out parameter
                virtual bool executeReferenceVoltageCommand(int& voltage);
                // Executes the status query on the radio.
                // Override this as needed for radios that support this command.
                // Status is an in/out parameter
                virtual bool executeStatusQuery(unsigned int& stat);
                // Executes the tuner status query on the radio.
                // Override this as needed for radios that support this command.
                // Status is an in/out parameter
                virtual bool executeTstatusQuery(unsigned int& stat);
                // Executes the temperature query on the radio.
                // Override this as needed for radios that support this command.
                // Temperature is an in/out parameter
                virtual bool executeTemperatureQuery(int& temp);
                // Executes the GPIO static query
                // Override this as needed for radios that support this command.
                // Value is an in/out parameter
                virtual bool executeGpioStaticQuery(int& value);
                // Executes the GPIO sequence query
                // Override this as needed for radios that support this command.
                // Value, duration, loop are in/out parameters
                virtual bool executeGpioSequenceQuery(int index, int& value,
                        int &duration, int& loop);
                // Executes the GPIO static command
                // Override this as needed for radios that support this command.
                // Value is an in/out parameter
                virtual bool executeGpioStaticCommand(int& value);
                // Executes the GPIO sequence comamnd
                // Override this as needed for radios that support this command.
                // Value, duration, loop, go are in/out parameters
                virtual bool executeGpioSequenceCommand(int index, int& value,
                        int &duration, int& loop,
                        int &go);
                // Executes the calibration frequency query
                // Override this as needed for radios that support this command.
                // Freq is an in/out parameter
                virtual bool executeCalibFrequencyQuery(double& freq);
                // Executes the calibration frequency command
                // Override this as needed for radios that support this command.
                // Freq is an in/out parameter
                virtual bool executeCalibFrequencyCommand(double& freq);
                // Converts an NMEA 0183-formatted coordinate string to decimal degrees.
                virtual double getDecimalDegreesFromNmea(const std::string& coord);


            protected:
                std::string _name;
                RadioTransport _transport;
                BasicStringList _connModesSupported;
                // Radio capabilities
                int _numTuner;
                int _tunerIndexBase;
                int _numWbddc;
                int _wbddcIndexBase;
                int _numNbddc;
                int _nbddcIndexBase;
                int _numTunerBoards;
                int _maxTunerBw;
                int _numTransmitter;
                int _transmitterIndexBase;
                int _numDuc;
                int _ducIndexBase;
                int _numWbddcGroups;
                int _wbddcGroupIndexBase;
                int _numNbddcGroups;
                int _nbddcGroupIndexBase;
                int _numDdcGroups;
                int _ddcGroupIndexBase;
                int _numDataPorts;
                int _dataPortIndexBase;
                int _numSimpleIpSetups;
                double _adcRate;
                VitaIfSpec _ifSpec;
                // Radio configuration items
                int _configMode;
                int _coherentMode;
                int _freqNormalization;
                int _gpsEnabled;
                int _referenceMode;
                int _referenceTuningVoltage;
                int _referenceBypass;
                double _calibFrequency;
                // Components
                TunerComponentDict _tuners;
                WbddcComponentDict _wbddcs;
                NbddcComponentDict _nbddcs;
                TransmitterComponentDict _txs;
                DucComponentDict _ducs;
                WbddcGroupComponentDict _wbddcGroups;
                NbddcGroupComponentDict _nbddcGroups;
                // Other configurables
                DataPortDict _dataPorts;
                SimpleIpSetupDict _simpleIpSetups;
                // Status
                std::string _lastCmdErrorInfo;
                BasicStringStringDict _versionInfo;
                BasicStringStringDict _connectionInfo;
                double _defaultTimeout;
                int _defaultDeviceInfo;

        }; /* class RadioHandler */

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_RADIOHANDLER_H */
