/***************************************************************************
 * \file NbddcGroupComponent.cpp
 * \brief Defines the basic NBDDC group interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Driver/NbddcGroupComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {
        NbddcGroupComponent::NbddcGroupComponent(
                const std::string& name,
                int index,
                RadioHandler* parent,
                bool debug,
                int numGroupMembers,
                int groupMemberIndexBase) :
            RadioComponent(name, index, parent, debug),
            _numGroupMembers(numGroupMembers),
            _groupMemberIndexBase(groupMemberIndexBase)
        {
            initConfigurationDict();
        }

        NbddcGroupComponent::~NbddcGroupComponent()
        {
        }

        NbddcGroupComponent::NbddcGroupComponent(const NbddcGroupComponent& other) :
            RadioComponent(other),
            _numGroupMembers(other._numGroupMembers),
            _groupMemberIndexBase(other._groupMemberIndexBase)
        {
        }

        NbddcGroupComponent& NbddcGroupComponent::operator=(const NbddcGroupComponent& other)
        {
            RadioComponent::operator=(other);
            if ( this != &other )
            {
                _numGroupMembers = other._numGroupMembers;
                _groupMemberIndexBase = other._groupMemberIndexBase;
            }
            return *this;
        }

        bool NbddcGroupComponent::enable(bool enabled)
        {
            bool adjEnabled = enabled;
            bool ret = false;
            if ( _config.hasKey("enable") )
            {
                ret = executeNbddcGroupEnableCommand(_index, adjEnabled);
                if ( ret )
                {
                    _enabled = adjEnabled;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        bool NbddcGroupComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[NbddcGroupComponent::setConfiguration] Called\n");
            // Call the "grandparent" version of this method instead of the
            // parent version. We want the normalization, but not the
            // automatic enabling.
            bool ret = Configurable::setConfiguration(cfg);
            bool adjEnabled = _enabled;
            BasicIntList adjMembers = _groupMembers;
            bool enableCmdNeedsExecuting = false;
            bool memberCmdNeedsExecuting = false;
            if ( cfg.hasKey("enable") && _config.hasKey("enable") )
            {
                adjEnabled = getConfigurationValueAsBool("enable");
                enableCmdNeedsExecuting = true;
            }
            if ( cfg.hasKey("members") && _config.hasKey("members") )
            {
                BasicStringList vec = Pythonesque::Split(getConfigurationValue("members"), ",");
                adjMembers.clear();
                for( BasicStringList::const_iterator it = vec.begin(); it != vec.end(); it++ )
                {
                    adjMembers.push_back( boost::lexical_cast<int>(Pythonesque::Strip(*it)) );
                }
                memberCmdNeedsExecuting = true;
            }
            if ( memberCmdNeedsExecuting )
            {
                ret &= executeNbddcGroupCommand(_index, adjMembers);
            }
            if ( enableCmdNeedsExecuting )
            {
                ret &= executeNbddcGroupEnableCommand(_index, adjEnabled);
            }
            if ( ret )
            {
                _enabled = adjEnabled;
                _groupMembers = adjMembers;
                updateConfigurationDict();
            }
            this->debug("[NbddcGroupComponent::setConfiguration] Returning\n");
            return ret;
        }

        void NbddcGroupComponent::queryConfiguration()
        {
            this->debug("[NbddcGroupComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("enable") )
            {
                executeNbddcGroupEnableQuery(_index, _enabled);
            }
            if ( _config.hasKey("members") )
            {
                executeNbddcGroupQuery(_index, _groupMembers);
            }
            updateConfigurationDict();
            this->debug("[NbddcGroupComponent::queryConfiguration] Returning\n");
        }

        BasicIntList NbddcGroupComponent::getMembers() const
        {
            return _groupMembers;
        }

        bool NbddcGroupComponent::setMembers(const BasicIntList& groupMembers)
        {
            this->debug("[NbddcGroupComponent::setMembers] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                BasicIntList adjMembers = groupMembers;
                ret = this->executeNbddcGroupCommand(_index, adjMembers);
                if (ret)
                {
                    _groupMembers = groupMembers;
                    updateConfigurationDict();
                }
            }
            this->debug("[NbddcGroupComponent::setMembers] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool NbddcGroupComponent::addMember(int member)
        {
            this->debug("[NbddcGroupComponent::addMember] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                bool isMember = true;
                ret = this->executeNbddcGroupMemberCommand(_index, member, isMember);
                if (ret)
                {
                    if ( std::count(_groupMembers.begin(), _groupMembers.end(), member) == 0 )
                    {
                        _groupMembers.push_back(member);
                        std::sort(_groupMembers.begin(), _groupMembers.end());
                        updateConfigurationDict();
                    }
                }
            }
            this->debug("[NbddcGroupComponent::addMember] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool NbddcGroupComponent::removeMember(int member)
        {
            this->debug("[NbddcGroupComponent::removeMember] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                bool isMember = false;
                ret = this->executeNbddcGroupMemberCommand(_index, member, isMember);
                if (ret)
                {
                    if ( std::count(_groupMembers.begin(), _groupMembers.end(), member) == 0 )
                    {
                        _groupMembers.push_back(member);
                        std::sort(_groupMembers.begin(), _groupMembers.end());
                        updateConfigurationDict();
                    }
                }
            }
            this->debug("[NbddcGroupComponent::removeMember] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        void NbddcGroupComponent::initConfigurationDict()
        {
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define component-specific keys
            _config["members"] = "";
        }

        void NbddcGroupComponent::updateConfigurationDict()
        {
            this->debug("[NbddcGroupComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("members") )
                setConfigurationValue("members", getMembersString());
            this->debug("[NbddcGroupComponent::updateConfigurationDict] Returning\n");
        }

        std::string NbddcGroupComponent::getMembersString()
        {
            BasicStringList vec;
            for (BasicIntList::const_iterator it = _groupMembers.begin();
                 it != _groupMembers.end(); it++)
            {
                vec.push_back( std::to_string(*it) );
            }
            std::string memberStr = Pythonesque::Join(vec, ", ");
            return memberStr;
        }

        // Default implementation is based on the NDR308 model
        bool NbddcGroupComponent::executeNbddcGroupEnableQuery(int index,
                                                               bool& enabled)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupEnableQuery] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "NBGE? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                   BasicStringList vec = Pythonesque::Split(
                                             Pythonesque::Replace(rsp.front(), "NBGE ", ""),
                                             ", ");
                   // vec[0] = Index
                   // vec[1] = Enabled indicator
                   enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                   ret = true;
                }
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupEnableQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool NbddcGroupComponent::executeNbddcGroupEnableCommand(int index,
                                                                 bool& enabled)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupEnableCommand] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "NBGE " << index
                    << ", " << (enabled ? 1 : 0)
                    << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                   ret = true;
                }
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupEnableCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool NbddcGroupComponent::executeNbddcGroupQuery(int index,
                                                         BasicIntList& groupMembers)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupQuery] Called\n");
            bool ret = true;
            bool isMember;
            groupMembers.clear();
            for (int member = _groupMemberIndexBase;
                 member < (_groupMemberIndexBase + _numGroupMembers); member++)
            {
                ret &= executeNbddcGroupMemberQuery(index, member, isMember);
                if (ret)
                {
                    if ( isMember )
                        groupMembers.push_back(member);
                }
                else
                    break;
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool NbddcGroupComponent::executeNbddcGroupCommand(int index,
                                                           BasicIntList& groupMembers)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupCommand] Called\n");
            bool ret = true;
            bool isMember;
            for (int member = _groupMemberIndexBase;
                 member < (_groupMemberIndexBase + _numGroupMembers); member++)
            {
                isMember = ( std::count(groupMembers.begin(), groupMembers.end(), member) > 0 );
                ret &= executeNbddcGroupMemberCommand(index, member, isMember);
                if (!ret)
                    break;
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool NbddcGroupComponent::executeNbddcGroupMemberQuery(int index, int groupMember,
                                                               bool& isMember)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupMemberQuery] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                BasicStringList rsp, vec;
                int inGroup;
                oss << "NBG? " << index
                    << ", " << groupMember
                    << "\n";
                rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    vec = Pythonesque::Split(
                                             Pythonesque::Replace(rsp.front(), "NBG ", ""),
                                             ", ");
                    // vec[0] = Group index
                    // vec[1] = Member index
                    // vec[2] = 0 if member is not in group, 1 if it is
                    isMember = ( boost::lexical_cast<int>(vec[2]) == 1 );
                    ret = true;
                }
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupMemberQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool NbddcGroupComponent::executeNbddcGroupMemberCommand(int index, int groupMember,
                                                                 bool& isMember)
        {
            this->debug("[NbddcGroupComponent::executeNbddcGroupMemberCommand] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "NBG " << index
                    << ", " << groupMember
                    << ", " << ( isMember ? 1 : 0 )
                    << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[NbddcGroupComponent::executeNbddcGroupMemberCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

    } // namespace Driver

} // namespace LibCyberRadio

