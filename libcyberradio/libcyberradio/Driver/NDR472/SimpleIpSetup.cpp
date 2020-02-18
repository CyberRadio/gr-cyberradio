/***************************************************************************
 * \file SimpleIpSetup.cpp
 * \brief Defines the tuner interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/SimpleIpSetup.h"
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

            SimpleIpSetup::SimpleIpSetup(::LibCyberRadio::Driver::RadioHandler* parent,
                    bool debug,
                    const std::string& sourceIP,
                    const std::string& destIP,
                    const std::string& destMAC) :
                ::LibCyberRadio::Driver::SimpleIpSetup(
                        /* const std::string& name */ "NDR472-IP",
                        /* ::LibCyberRadio::Driver::RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* const std::string& sourceIP */ "0.0.0.0",
                        /* const std::string& destIP */ "0.0.0.0",
                        /* const std::string& destMAC */ "00:00:00:00:00:00")
            {
                initConfigurationDict();
            }

            SimpleIpSetup::~SimpleIpSetup()
            {
            }

            SimpleIpSetup::SimpleIpSetup(const SimpleIpSetup& other) :
                ::LibCyberRadio::Driver::SimpleIpSetup(other)
            {
            }

            SimpleIpSetup& SimpleIpSetup::operator=(const SimpleIpSetup& other)
            {
                ::LibCyberRadio::Driver::SimpleIpSetup::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } /* namespace NDR472 */

    } // namespace Driver

} // namespace LibCyberRadio



