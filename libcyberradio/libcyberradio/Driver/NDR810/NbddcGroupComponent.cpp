/***************************************************************************
 * \file NbddcGroupComponent.cpp
 * \brief Defines the NBDDC group interface for the NDR810.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR810/NbddcGroupComponent.h"
#include "LibCyberRadio/Driver/RadioHandler.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{
    namespace Driver
    {

        namespace NDR810
        {

            NbddcGroupComponent::NbddcGroupComponent(int index,
                                           ::LibCyberRadio::Driver::RadioHandler* parent,
                                           bool debug) :
                ::LibCyberRadio::Driver::NbddcGroupComponent(
                               /* const std::string& name */ (boost::format("NDR810-NBG%02d") % \
                                                                 index).str(),
                               /* int index */ index,
                               /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                               /* bool debug */ debug,
                               /* int numGroupMembers */ 32,
                               /* int groupMemberIndexBase */ 1)
            {
                initConfigurationDict();
            }

            NbddcGroupComponent::~NbddcGroupComponent()
            {
            }

            NbddcGroupComponent::NbddcGroupComponent(const NbddcGroupComponent& other) :
                ::LibCyberRadio::Driver::NbddcGroupComponent(other)
            {
            }

            NbddcGroupComponent& NbddcGroupComponent::operator=(const NbddcGroupComponent& other)
            {
                ::LibCyberRadio::Driver::NbddcGroupComponent::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } /* namespace NDR810 */

    } // namespace Driver

} // namespace LibCyberRadio

