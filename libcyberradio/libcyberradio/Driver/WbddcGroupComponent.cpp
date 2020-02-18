/***************************************************************************
 * \file WbddcGroupComponent.cpp
 * \brief Defines the basic WBDDC group interface for an NDR-class radio.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Driver/WbddcGroupComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <iomanip>


namespace LibCyberRadio
{
    namespace Driver
    {
        WbddcGroupComponent::WbddcGroupComponent(
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

        WbddcGroupComponent::~WbddcGroupComponent()
        {
        }

        WbddcGroupComponent::WbddcGroupComponent(const WbddcGroupComponent& other) :
            RadioComponent(other),
            _numGroupMembers(other._numGroupMembers),
            _groupMemberIndexBase(other._groupMemberIndexBase)
        {
        }

        WbddcGroupComponent& WbddcGroupComponent::operator=(const WbddcGroupComponent& other)
        {
            RadioComponent::operator=(other);
            if ( this != &other )
            {
                _numGroupMembers = other._numGroupMembers;
                _groupMemberIndexBase = other._groupMemberIndexBase;
            }
            return *this;
        }

        bool WbddcGroupComponent::enable(bool enabled)
        {
            bool adjEnabled = enabled;
            bool ret = false;
            if ( _config.hasKey("enable") )
            {
                ret = executeWbddcGroupEnableCommand(_index, adjEnabled);
                if ( ret )
                {
                    _enabled = adjEnabled;
                    updateConfigurationDict();
                }
            }
            return ret;
        }

        bool WbddcGroupComponent::setConfiguration(ConfigurationDict& cfg)
        {
            this->debug("[WbddcGroupComponent::setConfiguration] Called\n");
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
                ret &= executeWbddcGroupCommand(_index, adjMembers);
            }
            if ( enableCmdNeedsExecuting )
            {
                ret &= executeWbddcGroupEnableCommand(_index, adjEnabled);
            }
            if ( ret )
            {
                _enabled = adjEnabled;
                _groupMembers = adjMembers;
                updateConfigurationDict();
            }
            this->debug("[WbddcGroupComponent::setConfiguration] Returning\n");
            return ret;
        }

        void WbddcGroupComponent::queryConfiguration()
        {
            this->debug("[WbddcGroupComponent::queryConfiguration] Called\n");
            if ( _config.hasKey("enable") )
            {
                executeWbddcGroupEnableQuery(_index, _enabled);
            }
            if ( _config.hasKey("members") )
            {
                executeWbddcGroupQuery(_index, _groupMembers);
            }
            updateConfigurationDict();
            this->debug("[WbddcGroupComponent::queryConfiguration] Returning\n");
        }

        BasicIntList WbddcGroupComponent::getMembers() const
        {
            return _groupMembers;
        }

        bool WbddcGroupComponent::setMembers(const BasicIntList& groupMembers)
        {
            this->debug("[WbddcGroupComponent::setMembers] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                BasicIntList adjMembers = groupMembers;
                ret = this->executeWbddcGroupCommand(_index, adjMembers);
                if (ret)
                {
                    _groupMembers = groupMembers;
                    updateConfigurationDict();
                }
            }
            this->debug("[WbddcGroupComponent::setMembers] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool WbddcGroupComponent::addMember(int member)
        {
            this->debug("[WbddcGroupComponent::addMember] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                bool isMember = true;
                ret = this->executeWbddcGroupMemberCommand(_index, member, isMember);
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
            this->debug("[WbddcGroupComponent::addMember] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool WbddcGroupComponent::removeMember(int member)
        {
            this->debug("[WbddcGroupComponent::removeMember] Called\n");
            bool ret = false;
            if ( _config.hasKey("members") )
            {
                bool isMember = false;
                ret = this->executeWbddcGroupMemberCommand(_index, member, isMember);
                if (ret)
                {
                    BasicIntList::iterator it = std::find(_groupMembers.begin(), _groupMembers.end(),
                                                                member);
                    if ( it != _groupMembers.end() )
                    {
                        _groupMembers.erase(it);
                        updateConfigurationDict();
                    }
                }
            }
            this->debug("[WbddcGroupComponent::removeMember] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        void WbddcGroupComponent::initConfigurationDict()
        {
            _config.clear();
            // Call the base-class version
            RadioComponent::initConfigurationDict();
            // Define component-specific keys
            _config["members"] = "";
        }

        void WbddcGroupComponent::updateConfigurationDict()
        {
            this->debug("[WbddcGroupComponent::updateConfigurationDict] Called\n");
            RadioComponent::updateConfigurationDict();
            if ( _config.hasKey("members") )
                setConfigurationValue("members", getMembersString());
            this->debug("[WbddcGroupComponent::updateConfigurationDict] Returning\n");
        }

        std::string WbddcGroupComponent::getMembersString()
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
        bool WbddcGroupComponent::executeWbddcGroupEnableQuery(int index,
                                                               bool& enabled)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupEnableQuery] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBGE? " << index << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                   BasicStringList vec = Pythonesque::Split(
                                             Pythonesque::Replace(rsp.front(), "WBGE ", ""),
                                             ", ");
                   // vec[0] = Index
                   // vec[1] = Enabled indicator
                   enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                   ret = true;
                }
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupEnableQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool WbddcGroupComponent::executeWbddcGroupEnableCommand(int index,
                                                                 bool& enabled)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupEnableCommand] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBGE " << index
                    << ", " << (enabled ? 1 : 0)
                    << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                   ret = true;
                }
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupEnableCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool WbddcGroupComponent::executeWbddcGroupQuery(int index,
                                                         BasicIntList& groupMembers)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupQuery] Called\n");
            bool ret = true;
            bool isMember;
            groupMembers.clear();
            for (int member = _groupMemberIndexBase;
                 member < (_groupMemberIndexBase + _numGroupMembers); member++)
            {
                ret &= executeWbddcGroupMemberQuery(index, member, isMember);
                if (ret)
                {
                    if ( isMember )
                        groupMembers.push_back(member);
                }
                else
                    break;
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool WbddcGroupComponent::executeWbddcGroupCommand(int index,
                                                           BasicIntList& groupMembers)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupCommand] Called\n");
            bool ret = true;
            bool isMember;
            for (int member = _groupMemberIndexBase;
                 member < (_groupMemberIndexBase + _numGroupMembers); member++)
            {
                isMember = ( std::count(groupMembers.begin(), groupMembers.end(), member) > 0 );
                ret &= executeWbddcGroupMemberCommand(index, member, isMember);
                if (!ret)
                    break;
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        bool WbddcGroupComponent::executeWbddcGroupMemberQuery(int index, int groupMember,
                                                               bool& isMember)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupMemberQuery] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                BasicStringList rsp, vec;
                int inGroup;
                oss << "WBG? " << index
                    << ", " << groupMember
                    << "\n";
                rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    vec = Pythonesque::Split(
                                             Pythonesque::Replace(rsp.front(), "WBG ", ""),
                                             ", ");
                    // vec[0] = Group index
                    // vec[1] = Member index
                    // vec[2] = 0 if member is not in group, 1 if it is
                    isMember = ( boost::lexical_cast<int>(vec[2]) == 1 );
                    ret = true;
                }
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupMemberQuery] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

        // Default implementation is based on the NDR308 model
        bool WbddcGroupComponent::executeWbddcGroupMemberCommand(int index, int groupMember,
                                                                 bool& isMember)
        {
            this->debug("[WbddcGroupComponent::executeWbddcGroupMemberCommand] Called\n");
            bool ret = false;
            if ( (_parent != NULL) && (_parent->isConnected()) )
            {
                std::ostringstream oss;
                oss << "WBG " << index
                    << ", " << groupMember
                    << ", " << ( isMember ? 1 : 0 )
                    << "\n";
                BasicStringList rsp = _parent->sendCommand(oss.str(), 2.0);
                if ( _parent->getLastCommandErrorInfo() == "" )
                {
                    ret = true;
                }
            }
            this->debug("[WbddcGroupComponent::executeWbddcGroupMemberCommand] Returning %s\n",
                        this->debugBool(ret));
            return ret;
        }

    } // namespace Driver

} // namespace LibCyberRadio

