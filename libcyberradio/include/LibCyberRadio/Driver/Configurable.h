/***************************************************************************
 * \file Configurable.h
 * \brief Defines the basic interface for an object configurable through
 *    dictionaries.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGURABLE_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGURABLE_H

#include "LibCyberRadio/Common/BasicDict.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/Driver/ConfigString.h"
#include <string>
#include <ostream>


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
         * \brief A configuration dictionary.
         *
         * A configuration dictionary contains the settings employed by
         * some configurable object. It contains a number of values
         * (using ConfigString objects) accessible using key strings.
         *
         * The ConfigString class allows users to assign values to a
         * configuration dictionary using a number of basic types, not just
         * strings.  Boolean values, integers, and floating-point values
         * are supported.  When retrieving values from the dictionary,
         * users can use their string forms, or they can convert these
         * values back to basic types using methods of the ConfigString
         * class.
         *
         * Each configurable object defines its own configuration dictionary,
         * so see its documentation for further details.
         */
        //typedef BASIC_DICT_CONTAINER<std::string, ConfigString> ConfigurationDict;
        class ConfigurationDict : public BASIC_DICT_CONTAINER<std::string, ConfigString>
        {
            public:
                /**
                 * \brief Constructs a ConfigurationDict object.
                 */
                ConfigurationDict();
                /**
                 * \brief Destroys a ConfigurationDict object.
                 */
                virtual ~ConfigurationDict();
                /**
                 * \brief Construct a string representation of this object.
                 * \returns A string representing this object's configuration.
                 */
                virtual std::string toString() const;
                /**
                 * \brief Determines if the dictionary has the given key.
                 * \param key Key string
                 * \returns True if the key is in the dictionary, false otherwise.
                 */
                virtual bool hasKey(const std::string& key) const;

        };

        /**
         * \brief Base configurable object class.
         */
        class Configurable : public Debuggable
        {
            public:
                /**
                 * \brief Constructs a Configurable object.
                 * \param name The name of this configurable object.
                 * \param debug Whether or not this object supports debug output methods.
                 */
                Configurable(const std::string& name = "<unknown>", bool debug = false);
                /**
                 * \brief Destroys a Configurable object.
                 */
                virtual ~Configurable();
                /**
                 * \brief Copies a Configurable object.
                 * \param other The Configurable object to copy.
                 */
                Configurable(const Configurable& other);
                /**
                 * \brief Assignment operator for Configurable objects.
                 * \param other The Configurable object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual Configurable& operator=(const Configurable& other);
                /**
                 * \brief Gets the name of the configurable object.
                 * \returns The name, as a string.
                 */
                virtual std::string getName() const;
                /**
                 * \brief Sets the name of the configurable object.
                 * \param name The new name.
                 */
                virtual void setName(const std::string &name);
                /**
                 * \brief Gets the configuration dictionary for this object.
                 * \returns The configuration dictionary.
                 */
                virtual ConfigurationDict getConfiguration() const;
                /**
                 * \brief Gets a named configuration value as a string.
                 * \param key The key string in the configuration dictionary.
                 * \returns The value represented by this key.  Returns an empty
                 *    string if the key is not in the configuration dictionary.
                 */
                virtual ConfigString getConfigurationValue(const std::string& key) const;
                /**
                 * \brief Gets a named configuration value as a Boolean.
                 * \param key The key string in the configuration dictionary.
                 * \returns The Boolean value represented by this key.  Returns false
                 *    if the key is not in the configuration dictionary, or cannot
                 *    be represented as a Boolean.
                 */
                virtual bool getConfigurationValueAsBool(const std::string& key) const;
                /**
                 * \brief Gets a named configuration value as an integer value.
                 * \param key The key string in the configuration dictionary.
                 * \returns The integer value represented by this key.  Returns 0
                 *    if the key is not in the configuration dictionary, or if the
                 *    value cannot be represented as an integer.
                 */
                virtual int getConfigurationValueAsInt(const std::string& key) const;
                /**
                 * \brief Gets a named configuration value as an unsigned integer value.
                 * \param key The key string in the configuration dictionary.
                 * \returns The integer value represented by this key.  Returns 0
                 *    if the key is not in the configuration dictionary, or if the
                 *    value cannot be represented as an integer.
                 */
                virtual unsigned int getConfigurationValueAsUInt(const std::string& key) const;
                /**
                 * \brief Gets a named configuration value as a double value.
                 * \param key The key string in the configuration dictionary.
                 * \returns The double value represented by this key.  Returns 0.0
                 *    if the key is not in the configuration dictionary, or if the
                 *    value cannot be represented as a double.
                 */
                virtual double getConfigurationValueAsDbl(const std::string& key) const;
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
                 * \brief Sets a named configuration value to a string.
                 * \note The default behavior of this method is to normalize the
                 *    incoming value.
                 * \param key The key string in the configuration dictionary.
                 * \param value The new value.
                 * \returns True if the key was set, false otherwise.  Returns
                 *    false if the key is not in the configuration dictionary.
                 */
                virtual bool setConfigurationValue(const std::string& key,
                        const std::string& value);
                /**
                 * \brief Sets a named configuration value to a Boolean.
                 * \param key The key string in the configuration dictionary.
                 * \param value The new value.
                 * \returns True if the key was set, false otherwise.  Returns
                 *    false if the key is not in the configuration dictionary.
                 */
                virtual bool setConfigurationValueToBool(const std::string& key,
                        const bool value);
                /**
                 * \brief Sets a named configuration value to an integer value.
                 * \param key The key string in the configuration dictionary.
                 * \param value The new value.
                 * \returns True if the key was set, false otherwise.  Returns
                 *    false if the key is not in the configuration dictionary.
                 */
                virtual bool setConfigurationValueToInt(const std::string& key,
                        const int value);
                /**
                 * \brief Sets a named configuration value to an unsigned
                 *    integer value.
                 * \param key The key string in the configuration dictionary.
                 * \param value The new value.
                 * \returns True if the key was set, false otherwise.  Returns
                 *    false if the key is not in the configuration dictionary.
                 */
                virtual bool setConfigurationValueToUInt(const std::string& key,
                        const unsigned int value);
                /**
                 * \brief Sets a named configuration value to a double value.
                 * \param key The key string in the configuration dictionary.
                 * \param value The new value.
                 * \returns True if the key was set, false otherwise.  Returns
                 *    false if the key is not in the configuration dictionary.
                 */
                virtual bool setConfigurationValueToDbl(const std::string& key,
                        const double value);
                /**
                 * \brief Tells the object to create its configuration dictionary.
                 *
                 * Derived classes should override this so that they issue
                 * hardware commands to determine initial configuration.
                 */
                virtual void queryConfiguration();

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
                /**
                 * \brief Normalizes an incoming configuration dictionary.
                 *
                 * "Normalizing" a configuration dictionary replaces certain strings
                 * representing Boolean values ("yes", "on", "true", "no", "off", and
                 * "false", case is irrelevant) with standard values ("0" and "1").
                 *
                 * \note The default behavior of this method normalizes every string
                 *    in the configuration dictionary. Override this method if
                 *    certain configuration items need to be protected from
                 *    normalization.
                 *
                 * \returns The new configuration dictionary.
                 */
                virtual ConfigurationDict normalizedConfigurationDict(
                        const ConfigurationDict& cfg);
                /**
                 * \brief Normalizes a Boolean string value.
                 * \returns The "normalized" string value.
                 */
                virtual std::string normalizedBool(const std::string& val);
                /**
                 * \brief Dumps this object's configuration dictionary to debug output.
                 */
                virtual void dumpConfiguration();

            protected:
                // Name of this configurable object
                std::string _name;
                // Configuration dictionary
                ConfigurationDict _config;

        }; // class Configurable

    } // namespace Driver

} // namespace LibCyberRadio

/**
 * \brief Stream insertion operator for ConfigurationDict objects.
 *
 * This puts the string representation of the ConfigurationDict out on
 * the stream.
 *
 * \param os The output stream.
 * \param obj The ConfigurationDict object.
 * \returns A reference to the output stream.
 */
std::ostream& operator<<(std::ostream& os, const LibCyberRadio::Driver::ConfigurationDict& obj);


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_CONFIGURABLE_H
