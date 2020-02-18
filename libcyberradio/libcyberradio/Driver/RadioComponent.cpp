/***************************************************************************
 * \file RadioComponent.cpp
 * \brief Defines the basic component interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Driver/RadioComponent.h"


namespace LibCyberRadio
{
    namespace Driver
    {

        RadioComponent::RadioComponent(const std::string& name,
                int index,
                RadioHandler* parent,
                bool debug) :
            Configurable(name, debug),
            _index(index),
            _parent(parent),
            _enabled(false)
        {
            initConfigurationDict();
        }

        RadioComponent::~RadioComponent()
        {
        }

        RadioComponent::RadioComponent(const RadioComponent& other) :
            Configurable(other),
            _index(other._index),
            _parent(other._parent),
            _enabled(other._enabled)
        {
        }

        RadioComponent&RadioComponent::operator=(const RadioComponent& other)
        {
            Configurable::operator=(other);
            if ( this != &other )
            {
                _index = other._index;
                _parent = other._parent;
                _enabled = other._enabled;
            }
            return *this;
        }

        int RadioComponent::getIndex() const
        {
            return _index;
        }

        void RadioComponent::setIndex(int index)
        {
            _index = index;
        }

        RadioHandler* RadioComponent::getParent() const
        {
            return _parent;
        }

        void RadioComponent::setParent(RadioHandler* parent)
        {
            _parent = parent;
        }

        bool RadioComponent::disable()
        {
            return enable(false);
        }

        bool RadioComponent::enable(bool enabled)
        {
            _enabled = enabled;
            updateConfigurationDict();
            return true;
        }

        bool RadioComponent::isEnabled() const
        {
            return _enabled;
        }

        bool RadioComponent::setConfiguration(ConfigurationDict& cfg)
        {
            //this->debug("[RadioComponent::setConfiguration] Called\n");
            // Call the base-class version to modify the configuration dictionary
            bool ret = Configurable::setConfiguration(cfg);
            // Use the keys provided in the *incoming* dictionary to determine
            // what needs to be changed.
            if ( cfg.hasKey("enable") && _config.hasKey("enable") )
            {
                ret = enable( _config["enable"].asBool() );
            }
            //this->debug("[RadioComponent::setConfiguration] Returning\n");
            return ret;
        }

        void RadioComponent::queryConfiguration()
        {
            //this->debug("[RadioComponent::queryConfiguration] Called\n");
            // Replace this with hardware queries to determine values
            //this->debug("[RadioComponent::queryConfiguration] Returning\n");
        }

        void RadioComponent::initConfigurationDict()
        {
            //this->debug("[RadioComponent::initConfigurationDict] Called\n");
            _config["enable"] = _enabled;
            //this->debug("[RadioComponent::initConfigurationDict] Returning\n");
        }

        void RadioComponent::updateConfigurationDict()
        {
            //this->debug("[RadioComponent::updateConfigurationDict] Called\n");
            if ( _config.hasKey("enable") )
                this->setConfigurationValueToBool("enable", _enabled);
            //this->debug("[RadioComponent::updateConfigurationDict] Returning\n");
        }

    } // namespace Driver

} // namespace LibCyberRadio

