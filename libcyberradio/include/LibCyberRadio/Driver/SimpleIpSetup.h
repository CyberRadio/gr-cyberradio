/***************************************************************************
 * \file SimpleIpSetup.h
 * \brief Defines a simple 1Gig data for NDR-class radios without 10Gig
 *     ports.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_SIMPLEIPSETUP_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_SIMPLEIPSETUP_H

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
         * \brief Simple IP setup class for radios without 10GigE data ports.
         *
         * A radio handler object maintains one SimpleIpSetup object for each
         * 1GigE interface on the radio that must handle data as well as control.
         *
         * Configuration dictionary items:
         * * "sourceIP": Source IP address [string]
         * * "sourceMAC": Source MAC address [string] [read-only]
         * * "destIP": Destination IP address [string]
         * * "destMAC": Destination MAC address [string]
         */
        class SimpleIpSetup : public Configurable
        {
            public:
                /**
                 * \brief Constructs a SimpleIpSetup object.
                 * \param name The name of this configurable object.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    object.
                 * \param debug Whether the object supports debug output.
                 * \param sourceIP Source IP address.
                 * \param destIP Destination IP address.
                 * \param destMAC Destination MAC address.
                 */
                SimpleIpSetup(const std::string& name = "SIMPLEIPSETUP",
                        RadioHandler* parent = NULL,
                        bool debug = false,
                        const std::string& sourceIP = "0.0.0.0",
                        const std::string& destIP = "0.0.0.0",
                        const std::string& destMAC = "00:00:00:00:00:00");
                /**
                 * \brief Destroys a SimpleIpSetup object.
                 */
                virtual ~SimpleIpSetup();
                /**
                 * \brief Copies a SimpleIpSetup object.
                 * \param other The SimpleIpSetup object to copy.
                 */
                SimpleIpSetup(const SimpleIpSetup& other);
                /**
                 * \brief Assignment operator for SimpleIpSetup objects.
                 * \param other The SimpleIpSetup object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual SimpleIpSetup& operator=(const SimpleIpSetup& other);
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
                // SimpleIpSetup extensions
                /**
                 * \brief Gets the source MAC address.
                 * \returns The source MAC address.
                 */
                virtual std::string getSourceMAC() const;
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
                 * \brief Gets the destination MAC address.
                 * \returns The MAC address.
                 */
                virtual std::string getDestMACAddress() const;
                /**
                 * \brief Gets the destination IP address.
                 * \returns The IP address.
                 */
                virtual std::string getDestIPAddress() const;
                /**
                 * \brief Sets the destination MAC address.
                 * \param macAddr The new MAC address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestMACAddress(const std::string& macAddr);
                /**
                 * \brief Sets the destination IP address.
                 * \param ipAddr The new IP address.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setDestIPAddress(const std::string& ipAddr);

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
                // SimpleIpSetup extensions
                /**
                 * \brief Executes the source MAC query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param macAddr Source MAC address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSourceMACQuery(std::string& macAddr);
                /**
                 * \brief Executes the source IP query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param ipAddr Source IP address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSourceIPQuery(std::string& ipAddr);
                /**
                 * \brief Executes the source IP set command.
                 * \param ipAddr Source IP address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeSourceIPCommand(std::string& ipAddr);
                /**
                 * \brief Executes the destination IP query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param ipAddr Destination IP address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestIPQuery(std::string& ipAddr);
                /**
                 * \brief Executes the destination IP set command.
                 * \param ipAddr Destination IP address.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestIPCommand(std::string& ipAddr);
                /**
                 * \brief Executes the destination MAC query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param macAddr Destination MAC address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestMACQuery(std::string& macAddr);
                /**
                 * \brief Executes the destination MAC set command.
                 * \param macAddr Destination MAC address (return).
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeDestMACCommand(std::string& macAddr);

            protected:
                // Parent radio handler object
                RadioHandler* _parent;
                // Source IP address
                std::string _sourceIP;
                // Source MAC address
                std::string _sourceMAC;
                // Destination IP address
                std::string _destIP;
                // Destination MAC address
                std::string _destMAC;

        }; /* class SimpleIpSetup */

        /**
         * \brief A dictionary of data ports, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, SimpleIpSetup*> SimpleIpSetupDict;

    } /* namespace Driver */

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_SIMPLEIPSETUP_H */
