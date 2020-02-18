/***************************************************************************
 * \file WbddcGroupComponent.h
 * \brief Defines the basic WBDDC group interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_WBDDCCOMPONENTGROUP_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_WBDDCCOMPONENTGROUP_H

#include "LibCyberRadio/Driver/RadioComponent.h"
#include "LibCyberRadio/Common/BasicDict.h"
#include "LibCyberRadio/Common/BasicList.h"


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
         * \brief Base WBDDC group component class.
         *
         * A radio handler object maintains one WBDDC group component object
         * per WBDDC group on the radio.
         *
         * Potential configuration dictionary elements:
         * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
         * * "members": Comma-separated list of WBDDCs in this group [string]
         *
         * \note Support for these elements varies by radio.  See the documentation
         *    for the particular radio's WBDDC group specialization to determine what
         *    elements are supported.
         */
        class WbddcGroupComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a WbddcGroupComponent object.
                 * \param name The name of this component.
                 * \param index The index number of this component.
                 * \param parent A pointer to the RadioHandler object that "owns" this
                 *    component.
                 * \param debug Whether the component supports debug output.
                 * \param numGroupMembers Number of potential group members (commonly
                 *     the number of NBDDCs on the radio)
                 * \param groupMemberIndexBase Number that group members start with
                 *     (commonly the index base for the NBDDCs)
                 */
                WbddcGroupComponent(const std::string& name = "WBG",
                                    int index = 1,
                                    RadioHandler* parent = NULL,
                                    bool debug = false,
                                    int numGroupMembers = 0,
                                    int groupMemberIndexBase = 1);
                /**
                 * \brief Destroys a WbddcGroupComponent object.
                 */
                virtual ~WbddcGroupComponent();
                /**
                 * \brief Copies a WbddcGroupComponent object.
                 * \param other The WbddcGroupComponent object to copy.
                 */
                WbddcGroupComponent(const WbddcGroupComponent& other);
                /**
                 * \brief Assignment operator for WbddcGroupComponent objects.
                 * \param other The WbddcGroupComponent object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual WbddcGroupComponent& operator=(const WbddcGroupComponent& other);
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
                // WbddcGroupComponent extensions
                /**
                 * \brief Gets the list of group members.
                 * \returns List of WBDDC group members.
                 */
                virtual BasicIntList getMembers() const;
                /**
                 * \brief Sets the list of group members.
                 * \param groupMembers List of WBDDC group members.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setMembers(const BasicIntList& groupMembers);
                /**
                 * \brief Adds a WBDDC to the list of group members.
                 * \param member WBDDC to add.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool addMember(int member);
                /**
                 * \brief Removes a WBDDC from the list of group members.
                 * \param member WBDDC to remove.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool removeMember(int member);


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
                // WbddcGroupComponent extensions
                /**
                 * \brief Gets the string representation of the member list.
                 * \returns A comma-separated list of members [string].
                 */
                virtual std::string getMembersString();
                /**
                 * \brief Executes the WBDDC group enable query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index WBDDC group index.
                 * \param enabled Whether or not this group is enabled [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupEnableQuery(int index,
                                                          bool& enabled);
                /**
                 * \brief Executes the WBDDC group enable command.
                 * \param index WBDDC group index.
                 * \param enabled Whether or not this group is enabled.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupEnableCommand(int index,
                                                            bool& enabled);
                /**
                 * \brief Executes the WBDDC group configuration query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index WBDDC group index.
                 * \param groupMembers List of WBDDC group members [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupQuery(int index,
                                                    BasicIntList& groupMembers);
                /**
                 * \brief Executes the WBDDC group configuration set command.
                 * \param index WBDDC group index.
                 * \param groupMembers List of WBDDC group members.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupCommand(int index,
                                                      BasicIntList& groupMembers);
                /**
                 * \brief Executes the WBDDC group member query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index WBDDC group index.
                 * \param groupMember Group member index.
                 * \param isMember True if the WBDDC is a member of the group [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupMemberQuery(int index, int groupMember,
                                                          bool& isMember);
                /**
                 * \brief Executes the WBDDC group member set command.
                 * \param index WBDDC group index.
                 * \param groupMember Group member index.
                 * \param isMember True if the WBDDC is a member of the group.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeWbddcGroupMemberCommand(int index, int groupMember,
                                                            bool& isMember);

            protected:
                // Number of potential members in this group
                int _numGroupMembers;
                // Index that group members start with
                int _groupMemberIndexBase;
                // Group members
                BasicIntList _groupMembers;

        }; // class WbddcGroupComponent

        /**
         * \brief A dictionary of WBDDC group components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, WbddcGroupComponent*> WbddcGroupComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_WBDDCCOMPONENTGROUP_H */
