/***************************************************************************
 * \file WbddcGroupComponent.cpp
 * \brief Defines the WBDDC group interface for the NDR308-TS.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR308TS/WbddcGroupComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR308TS
        {

            WbddcGroupComponent::WbddcGroupComponent(int index,
                                           ::LibCyberRadio::Driver::RadioHandler* parent,
                                           bool debug) :
                ::LibCyberRadio::Driver::WbddcGroupComponent(
                               /* const std::string& name */ (boost::format("NDR308TS-WBG%02d") % \
                                                                 index).str(),
                               /* int index */ index,
                               /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                               /* bool debug */ debug,
                               /* int numGroupMembers */ 8,
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

        } /* namespace NDR308TS */

    } // namespace Driver

} // namespace LibCyberRadio

