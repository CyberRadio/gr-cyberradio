/***************************************************************************
 * \file WbddcGroupComponent.cpp
 * \brief Defines the WBDDC group interface for the NDR651.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR651/WbddcGroupComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR651
        {

            WbddcGroupComponent::WbddcGroupComponent(int index,
                                           ::LibCyberRadio::Driver::RadioHandler* parent,
                                           bool debug) :
                ::LibCyberRadio::Driver::WbddcGroupComponent(
                               /* const std::string& name */ (boost::format("NDR651-WBG%02d") % \
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

        } /* namespace NDR651 */

    } // namespace Driver

} // namespace LibCyberRadio

