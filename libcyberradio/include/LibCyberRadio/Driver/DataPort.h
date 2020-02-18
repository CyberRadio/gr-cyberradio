/***************************************************************************
 * \file DataPort.h
 * \brief Defines the basic 10GigE data port interface for an
 *    NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_DATAPORT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_DATAPORT_H

#include "LibCyberRadio/Driver/Configurable.h"
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
        // Forward declaration for RadioHandler object
        class RadioHandler;

        /**
         * \brief 10GigE data port class.
         *
         * A radio handler object maintains one DataPort object for each
         * 10GigE data port on the radio.
         *
         * Configuration dictionary items:
         * * "sourceIP": Source IP address [string]
         * * "errors": Whether errors are enabled [Boolean/integer/string]
         * * "flowControl": Whether flow control is enabled [Boolean/integer/string]
         */
        class DataPort : public Configurable
        {
            public:
                /**
                 * \brief Constructs a DataPort object.
                 * \param name The name of this configurable object.
                 * \param index The index number of this object.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    object.
                 * \param debug Whether the object supports debug output.
                 * \param sourceIP Source IP address.
                 * \param numDataPortDipEntries Number of entries in the DIP table.
                 * \param dataPortDipEntryIndexBase Where DIP entries are numbered from.
                 */
                DataPort(const std::string& name = "DATAPORT",
                        int index = 0,
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        const std::string& sourceIP = "0.0.0.0",
                        int numDataPortDipEntries = 0,
                        int dataPortDipEntryIndexBase = 0);
                /**
                 * \brief Destroys a DataPort object.
                 */
                virtual ~DataPort();
                /**
                 * \brief Copies a DataPort object.
                 * \param other The DataPort object to copy.
                 */
                DataPort(const DataPort& other);
                /**
                 * \brief Assignment operator for DataPort objects.
                 * \param other The DataPort object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual DataPort& operator=(const DataPort& other);
                // Configurable interface
                /**
                 * \brief Sets the configuration dictionary for this object.
                 *
                 * \param cfg The configuration dictionary.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setConfiguration(ConfigurationDict& cfg);
                /**
                 * \brief Tells the object to create its configuration dictionary.
                 */
                virtual void queryConfiguration();
                // DataPort extensions
                /**
                 * \brief Gets the number of destination IP table entries.
                 * \returns The number of entries, as an integer.
                 */
                virtual int getNumDestEntries() const;
                /**
                 * \brief Gets the list of destination IP table entry indices.
                 * \returns The list of indices.
                 */
                virtual BasicIntList getDestEntryIndexRange() const;
                /**
                 * \brief Gets the source IP address.
                 * \returns The source IP address.
                 */
                virtual std::string getSourceIP() const;
                /**
                 * \brief Sets the source IP address.
                 * \param ipAddr The new source IP address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setSourceIP(const std::string& ipAddr);
                /**
                 * \brief Gets the MAC address for a given entry in the
                 *    destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The MAC address.
                 */
                virtual std::string getDestMACAddress(int dipIndex) const;
                /**
                 * \brief Gets the IP address for a given entry in the
                 *    destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The IP address.
                 */
                virtual std::string getDestIPAddress(int dipIndex) const;
                /**
                 * \brief Gets the source UDP port number for a given entry
                 *    in the destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The port number.
                 */
                virtual unsigned int getDestSourcePort(int dipIndex) const;
                /**
                 * \brief Gets the destination UDP port number for a given entry
                 *    in the destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \returns The port number.
                 */
                virtual unsigned int getDestDestPort(int dipIndex) const;
                /**
                 * \brief Sets the destination table information for a given entry
                 *    in the DIP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param ipAddr The IP address.
                 * \param macAddr The MAC address.
                 * \param sourcePort The source UDP port number.
                 * \param destPort The destination UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestInfo(int dipIndex,
                        const std::string& ipAddr,
                        const std::string& macAddr,
                        unsigned int sourcePort,
                        unsigned int destPort);
                /**
                 * \brief Sets the MAC address for a given entry in the
                 *    destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param macAddr The new MAC address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestMACAddress(int dipIndex, const std::string& macAddr);
                /**
                 * \brief Sets the IP address for a given entry in the
                 *    destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param ipAddr The new IP address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestIPAddress(int dipIndex, const std::string& ipAddr);
                /**
                 * \brief Sets the source UDP port number for a given entry
                 *    in the destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param sourcePort The source UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestSourcePort(int dipIndex, unsigned int sourcePort);
                /**
                 * \brief Sets the destination UDP port number for a given entry
                 *    in the destination IP table.
                 * \param dipIndex Index number for the entry in the DIP table.
                 * \param destPort The destination UDP port number.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestDestPort(int dipIndex, unsigned int destPort);
                /**
                 * \brief Enables errors on the data port.
                 * \param enabled Whether or not errors should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableErrors(bool enabled = true);
                /**
                 * \brief Disables errors on the data port.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableErrors();
                /**
                 * \brief Enables flow control on the data port.
                 * \param enabled Whether or not errors should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enableFlowControl(bool enabled = true);
                /**
                 * \brief Disables flow control on the data port.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disableFlowControl();

            protected:
                // Configurable interface
                /**
                 * \brief Initializes the configuration dictionary, defining the allowed
                 *    keys.
                 */
                virtual void initConfigurationDict();
                /**
                 * \brief Updates the configuration dictionary from object settings.
                 */
                virtual void updateConfigurationDict();
                // DataPort extensions
                /**
                 * \brief Executes the source IP query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index Data port index.
                 * \param ipAddr Source IP address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSourceIPQuery(int index, std::string& ipAddr);
                /**
                 * \brief Executes the source IP set command.
                 * \param index Data port index.
                 * \param ipAddr Source IP address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSourceIPCommand(int index, std::string& ipAddr);
                /**
                 * \brief Executes the destination IP query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index Data port index.
                 * \param dipIndex DIP table entry index.
                 * \param ipAddr Destination IP address (return).
                 * \param macAddr Destination MAC address (return).
                 * \param sourcePort Source UDP port (return).
                 * \param destPort Destination UDP port (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestIPQuery(int index,
                        int dipIndex,
                        std::string& ipAddr,
                        std::string& macAddr,
                        unsigned int& sourcePort,
                        unsigned int& destPort);
                /**
                 * \brief Executes the destination IP set command.
                 * \param index Data port index.
                 * \param dipIndex DIP table entry index.
                 * \param ipAddr Destination IP address.
                 * \param macAddr Destination MAC address.
                 * \param sourcePort Source UDP port.
                 * \param destPort Destination UDP port.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestIPCommand(int index,
                        int dipIndex,
                        std::string& ipAddr,
                        std::string& macAddr,
                        unsigned int& sourcePort,
                        unsigned int& destPort);
                /**
                 * \brief Executes the error enabled query.
                 * \param index Data port index.
                 * \param enabled Error enabled [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeErrorEnabledQuery(int index, bool& enabled);
                /**
                 * \brief Executes the error enabled command.
                 * \param index Data port index.
                 * \param enabled Error enabled.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeErrorEnabledCommand(int index, bool& enabled);
                /**
                 * \brief Executes the flow control enabled query.
                 * \param index Data port index.
                 * \param enabled Flow control enabled [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFlowControlEnabledQuery(int index, bool& enabled);
                /**
                 * \brief Executes the flow control enabled command.
                 * \param index Data port index.
                 * \param enabled Flow control enabled.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeFlowControlEnabledCommand(int index, bool& enabled);

            protected:
                // Index number of the data port
                int _index;
                // Parent radio handler object
                RadioHandler* _parent;
                // Source IP address
                std::string _sourceIP;
                // Number of DIP table entries
                int _numDipEntries;
                // DIP entry index base
                int _dipEntryIndexBase;
                // Whether errors are enabled or not
                bool _errorsEnabled;
                // Whether flow control is enabled or not
                bool _flowControlEnabled;
                // Dict of MAC addresses, keyed by DIP table index
                BasicIntStringDict _macAddresses;
                // Dict of IP addresses, keyed by DIP table index
                BasicIntStringDict _ipAddresses;
                // Dict of source UDP port numbers, keyed by DIP table index
                BasicIntUIntDict _sourcePorts;
                // Dict of destination UDP port numbers, keyed by DIP table index
                BasicIntUIntDict _destPorts;


        }; /* class DataPort */

        /**
         * \brief A dictionary of data ports, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, DataPort*> DataPortDict;

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_DATAPORT_H0 */
