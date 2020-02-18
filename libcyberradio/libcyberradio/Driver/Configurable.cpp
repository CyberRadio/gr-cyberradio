/***************************************************************************
 * \file Configurable.cpp
 * \brief Defines the basic interface for an object configurable through
 *    dictionaries.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/Configurable.h"
#include <sstream>
#include <algorithm>
#include <cstdio>
#include <cstdarg>
#include <ctype.h>


namespace LibCyberRadio
{
    namespace Driver
    {

        ConfigurationDict::ConfigurationDict() :
            BASIC_DICT_CONTAINER<std::string, ConfigString>()
        {
        }

        ConfigurationDict::~ConfigurationDict()
        {

        }

        std::string ConfigurationDict::toString() const
        {
            std::ostringstream oss;
            oss << "Configuration(";
            ConfigurationDict::const_iterator it;
            for ( it = this->begin(); it != this->end(); it++)
            {
                if ( it != this->begin() )
                    oss << ", ";
                oss << it->first.c_str()
                            << "="
                            << it->second.c_str();
            }
            oss << ")";
            return oss.str();
        }

        bool ConfigurationDict::hasKey(const std::string& key) const
        {
            return ( this->find(key) != this->end() );
        }

        Configurable::Configurable(const std::string& name, bool debug) :
            Debuggable(debug, name),
            _name(name)
        {
        }

        Configurable::~Configurable()
        {
        }

        Configurable::Configurable(const Configurable& other) :
            _name(other._name),
            _config(other._config)
        {
        }

        Configurable& Configurable::operator=(const Configurable& other)
        {
            if ( this != &other )
            {
                _name = other._name;
                _config = other._config;
            }
            return *this;
        }

        std::string Configurable::getName() const
        {
            return _name;
        }

        void Configurable::setName(const std::string &name)
        {
            _name = name;
        }

        ConfigurationDict Configurable::getConfiguration() const
        {
            return _config;
        }

        ConfigString Configurable::getConfigurationValue(const std::string& key) const
        {
            ConfigString ret = "";
            ConfigurationDict::const_iterator it = _config.find(key);
            if ( it != _config.end() )
            {
                ret = it->second;
            }
            return ret;
        }

        bool Configurable::getConfigurationValueAsBool(const std::string& key) const
        {
            bool ret = false;
            try
            {
                ret = ( getConfigurationValue(key).asBool() );
            }
            catch(std::exception& ex)
            {
            }
            return ret;
        }

        int Configurable::getConfigurationValueAsInt(const std::string& key) const
        {
            int ret = 0;
            try
            {
                ret = ( getConfigurationValue(key).asInt() );
            }
            catch(std::exception& ex)
            {
            }
            return ret;
        }

        unsigned int Configurable::getConfigurationValueAsUInt(const std::string& key) const
        {
            unsigned int ret = 0;
            try
            {
                ret = ( getConfigurationValue(key).asUInt() );
            }
            catch(std::exception& ex)
            {
            }
            return ret;
        }

        double Configurable::getConfigurationValueAsDbl(const std::string& key) const
        {
            double ret = 0.0;
            try
            {
                ret = ( getConfigurationValue(key).asDouble() );
            }
            catch(std::exception& ex)
            {
            }
            return ret;
        }

        bool Configurable::setConfiguration(ConfigurationDict& cfg)
        {
            // Replace elements in the configuration dictionary with
            // normalized elements in the incoming dictionary that have the
            // same key
            ConfigurationDict normCfg = normalizedConfigurationDict(cfg);
            ConfigurationDict::iterator nit;
            for (ConfigurationDict::iterator it = _config.begin(); it != _config.end(); it++)
            {
                nit = normCfg.find(it->first);
                if ( nit != normCfg.end() )
                    it->second = nit->second;
            }
            return true;
        }

        bool Configurable::setConfigurationValue(const std::string& key,
                const std::string& value)
        {
            bool ret = false;
            ConfigurationDict::iterator it = _config.find(key);
            if ( it != _config.end() )
            {
                _config[key] = normalizedBool(value);
                ret = true;
            }
            else
            {
            }
            return ret;
        }

        bool Configurable::setConfigurationValueToBool(const std::string& key,
                const bool value)
        {
            return setConfigurationValue(key, ConfigString(value));
        }

        bool Configurable::setConfigurationValueToInt(const std::string& key,
                const int value)
        {
            return setConfigurationValue(key, ConfigString(value));
        }

        bool Configurable::setConfigurationValueToUInt(const std::string& key,
                const unsigned int value)
        {
            return setConfigurationValue(key, ConfigString(value));
        }

        bool Configurable::setConfigurationValueToDbl(const std::string& key,
                const double value)
        {
            return setConfigurationValue(key, ConfigString(value));
        }

        void Configurable::queryConfiguration()
        {
        }

        void Configurable::initConfigurationDict()
        {
        }

        void Configurable::updateConfigurationDict()
        {
        }

        // Normalization converts strings representing Boolean values to
        // standard "0" or "1"

        ConfigurationDict Configurable::normalizedConfigurationDict(
                const ConfigurationDict& cfg)
        {
            ConfigurationDict adjCfg = cfg;
            for (ConfigurationDict::iterator it = adjCfg.begin(); it != adjCfg.end(); it++)
                it->second = normalizedBool(it->second);
            return adjCfg;
        }

        std::string Configurable::normalizedBool(const std::string& val)
        {
            std::string ret = "";
            std::string adjVal = val;
            std::transform(val.begin(), val.end(), adjVal.begin(), tolower);
            if ( (adjVal == "1") || (adjVal == "yes") || (adjVal == "on") || (adjVal == "true") )
                ret = "1";
            else if ( (adjVal == "0") || (adjVal == "no") || (adjVal == "off") || (adjVal == "false") )
                ret = "0";
            else
                ret = val;
            return ret;
        }

        void Configurable::dumpConfiguration()
        {
            this->debug("Configuration:\n");
            ConfigurationDict::const_iterator it;
            for ( it = _config.begin(); it != _config.end(); it++)
            {
                this->debug("-- %s = %s\n", it->first.c_str(), it->second.c_str());
            }
            this->debug("[end configuration]\n");
        }

    } // namespace Driver

} // namespace LibCyberRadio


std::ostream& operator<<(std::ostream& os, const LibCyberRadio::Driver::ConfigurationDict& obj)
{
    os << obj.toString();
    return os;
}

