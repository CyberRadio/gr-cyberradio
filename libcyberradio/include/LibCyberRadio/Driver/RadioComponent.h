/***************************************************************************
 * \file RadioComponent.h
 * \brief Defines the basic component interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_RADIOCOMPONENT_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_RADIOCOMPONENT_H

#include "LibCyberRadio/Driver/Configurable.h"
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
         * \brief Base hardware component class.
         *
         * A radio handler object maintains a series of component objects, one
         * per component of each type (tuner, WBDDC, NBDDC, etc.).  Each component
         * object is responsible for managing the hardware object that it represents.
         * Each component object is also responsible for querying the component's
         * current configuration and for maintaining the object's configuration
         * as it changes during radio operation.
         *
         * See each individual component's documentation to determine the layout
         * of its configuration dictionary.
         */
        class RadioComponent : public Configurable
        {
            public:
                /**
                 * \brief Constructs a RadioComponent object.
                 * \param name The name of this component.
                 * \param index The index number of this component.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    component.
                 * \param debug Whether the component supports debug output.
                 */
                RadioComponent(const std::string& name = "<unknown>",
                        int index = 0,
                        RadioHandler* parent = NULL,
                        bool debug = false);
                /**
                 * \brief Destroys a RadioComponent object.
                 */
                virtual ~RadioComponent();
                /**
                 * \brief Copies a RadioComponent object.
                 * \param other The RadioComponent object to copy.
                 */
                RadioComponent(const RadioComponent& other);
                /**
                 * \brief Assignment operator for RadioComponent objects.
                 * \param other The RadioComponent object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual RadioComponent& operator=(const RadioComponent& other);
                /**
                 * \brief Gets the index number of the component.
                 * \returns The index number, as an integer.
                 */
                virtual int getIndex() const;
                /**
                 * \brief Sets the index number of the component.
                 * \param index The index number.
                 */
                virtual void setIndex(int index);
                /**
                 * \brief Gets the "parent" radio handler for this component.
                 * \returns A pointer to the RadioHandler object.
                 */
                virtual RadioHandler* getParent() const;
                /**
                 * \brief Sets the "parent" radio handler for this component.
                 * \param parent A pointer to the RadioHandler object.
                 */
                virtual void setParent(RadioHandler* parent);
                /**
                 * \brief Disables this component.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool disable();
                /**
                 * \brief Enables this component.
                 * \param enabled Whether or not this component should be enabled.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool enable(bool enabled = true);
                /**
                 * \brief Gets whether or not the component is enabled.
                 * \returns True if enabled, false otherwise.
                 */
                virtual bool isEnabled() const;
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

            protected:
                /**
                 * \brief Initializes the configuration dictionary, defining the allowed
                 *    keys.
                 */
                virtual void initConfigurationDict();
                /**
                 * \brief Updates the configuration dictionary from component settings.
                 */
                virtual void updateConfigurationDict();

            protected:
                // Index number of the component
                int _index;
                // Parent radio handler object
                RadioHandler* _parent;
                // Whether or not the component is enabled
                bool _enabled;

        }; // class RadioComponent

    } // namespace Driver

} // namespace LibCyberRadio


#endif // INCLUDED_LIBCYBERRADIO_DRIVER_RADIOCOMPONENT_H
