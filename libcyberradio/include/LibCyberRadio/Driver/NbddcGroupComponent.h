/***************************************************************************
 * \file NbddcGroupComponent.h
 * \brief Defines the basic NBDDC group interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#ifndef INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENTGROUP_H
#define INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENTGROUP_H

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
         * \brief Base NBDDC group component class.
         *
         * A radio handler object maintains one NBDDC group component object
         * per NBDDC group on the radio.
         *
         * Configuration dictionary elements:
         * * "enable": Whether or not this DDC group is enabled [Boolean/integer/string]
         * * "members": Comma-separated list of NBDDCs in this group [string]
         *
         * \note Support for these elements varies by radio.  See the documentation
         *    for the particular radio's NBDDC group specialization to determine what
         *    elements are supported.
         */
        class NbddcGroupComponent : public RadioComponent
        {
            public:
                /**
                 * \brief Constructs a NbddcGroupComponent object.
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
                NbddcGroupComponent(const std::string& name = "NBG",
                                    int index = 1,
                                    RadioHandler* parent = NULL,
                                    bool debug = false,
                                    int numGroupMembers = 0,
                                    int groupMemberIndexBase = 1);
                /**
                 * \brief Destroys a NbddcGroupComponent object.
                 */
                virtual ~NbddcGroupComponent();
                /**
                 * \brief Copies a NbddcGroupComponent object.
                 * \param other The NbddcGroupComponent object to copy.
                 */
                NbddcGroupComponent(const NbddcGroupComponent& other);
                /**
                 * \brief Assignment operator for NbddcGroupComponent objects.
                 * \param other The NbddcGroupComponent object to copy.
                 * \returns A reference to the assigned object.
                 */
                virtual NbddcGroupComponent& operator=(const NbddcGroupComponent& other);
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
                // NbddcGroupComponent extensions
                /**
                 * \brief Gets the list of group members.
                 * \returns List of NBDDC group members.
                 */
                virtual BasicIntList getMembers() const;
                /**
                 * \brief Sets the list of group members.
                 * \param groupMembers List of NBDDC group members.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool setMembers(const BasicIntList& groupMembers);
                /**
                 * \brief Adds a NBDDC to the list of group members.
                 * \param member NBDDC to add.
                 * \returns True if successful, false otherwise.
                 */
                virtual bool addMember(int member);
                /**
                 * \brief Removes a NBDDC from the list of group members.
                 * \param member NBDDC to remove.
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
                // NbddcGroupComponent extensions
                /**
                 * \brief Gets the string representation of the member list.
                 * \returns A comma-separated list of members [string].
                 */
                virtual std::string getMembersString();
                /**
                 * \brief Executes the NBDDC group enable query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC group index.
                 * \param enabled Whether or not this group is enabled [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupEnableQuery(int index,
                                                          bool& enabled);
                /**
                 * \brief Executes the NBDDC group enable command.
                 * \param index NBDDC group index.
                 * \param enabled Whether or not this group is enabled.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupEnableCommand(int index,
                                                            bool& enabled);
                /**
                 * \brief Executes the NBDDC group configuration query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC group index.
                 * \param groupMembers List of NBDDC group members [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupQuery(int index,
                                                    BasicIntList& groupMembers);
                /**
                 * \brief Executes the NBDDC group configuration set command.
                 * \param index NBDDC group index.
                 * \param groupMembers List of NBDDC group members.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupCommand(int index,
                                                      BasicIntList& groupMembers);
                /**
                 * \brief Executes the NBDDC group member query command.
                 * \note The return value from this method only indicates if the command
                 *    succeeded or failed. This method uses reference parameters to return
                 *    the results of the query.
                 * \param index NBDDC group index.
                 * \param groupMember Group member index.
                 * \param isMember True if the NBDDC is a member of the group [output].
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupMemberQuery(int index, int groupMember,
                                                          bool& isMember);
                /**
                 * \brief Executes the NBDDC group member set command.
                 * \param index NBDDC group index.
                 * \param groupMember Group member index.
                 * \param isMember True if the NBDDC is a member of the group.
                 * \returns True if the command succeeded, false otherwise.
                 */
                virtual bool executeNbddcGroupMemberCommand(int index, int groupMember,
                                                            bool& isMember);

            protected:
                // Number of potential members in this group
                int _numGroupMembers;
                // Index that group members start with
                int _groupMemberIndexBase;
                // Group members
                BasicIntList _groupMembers;

        }; // class NbddcGroupComponent

        /**
         * \brief A dictionary of NBDDC group components, keyed by index.
         */
        typedef BASIC_DICT_CONTAINER<int, NbddcGroupComponent*> NbddcGroupComponentDict;

    } // namespace Driver

} // namespace LibCyberRadio

#endif /* INCLUDED_LIBCYBERRADIO_DRIVER_NBDDCCOMPONENTGROUP_H */
