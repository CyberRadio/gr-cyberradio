/***************************************************************************
 * \file WbddcGroupComponent.cpp
 * \brief Defines the WBDDC group interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/WbddcGroupComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR472
        {

            WbddcGroupComponent::WbddcGroupComponent(int index,
                                           ::LibCyberRadio::Driver::RadioHandler* parent,
                                           bool debug) :
                ::LibCyberRadio::Driver::WbddcGroupComponent(
                               /* const std::string& name */ (boost::format("NDR472-WBG%02d") % \
                                                                 index).str(),
                               /* int index */ index,
                               /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                               /* bool debug */ debug,
                               /* int numGroupMembers */ 2,
                               /* int groupMemberIndexBase */ 1)
            {
                initConfigurationDict();
            }

            WbddcGroupComponent::~WbddcGroupComponent()
            {
            }

            WbddcGroupComponent::WbddcGroupComponent(const WbddcGroupComponent& other) :
                ::LibCyberRadio::Driver::WbddcGroupComponent(other)
            {
            }

            WbddcGroupComponent& WbddcGroupComponent::operator=(const WbddcGroupComponent& other)
            {
                ::LibCyberRadio::Driver::WbddcGroupComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

            // OVERRIDE
            // This radio uses commas to delimit query parameters rather than commas
            bool WbddcGroupComponent::executeWbddcGroupEnableQuery(int index,
                                                                   bool& enabled)
            {
                this->debug("[NDR472::WbddcGroupComponent::executeWbddcGroupEnableQuery] Called\n");
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
                                                 " ");
                       // vec[0] = Index
                       // vec[1] = Enabled indicator
                       enabled = (boost::lexical_cast<int>(vec[1]) == 1);
                       ret = true;
                    }
                }
                this->debug("[NDR472::WbddcGroupComponent::executeWbddcGroupEnableQuery] Returning %s\n",
                            this->debugBool(ret));
                return ret;
            }

            bool WbddcGroupComponent::executeWbddcGroupMemberQuery(int index, int groupMember,
                                                                   bool& isMember)
            {
                this->debug("[NDR472::WbddcGroupComponent::executeWbddcGroupMemberQuery] Called\n");
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
                                                 " ");
                        // vec[0] = Group index
                        // vec[1] = Member index
                        // vec[2] = 0 if member is not in group, 1 if it is
                        isMember = ( boost::lexical_cast<int>(vec[2]) == 1 );
                        ret = true;
                    }
                }
                this->debug("[NDR472::WbddcGroupComponent::executeWbddcGroupMemberQuery] Returning %s\n",
                            this->debugBool(ret));
                return ret;
            }

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio

