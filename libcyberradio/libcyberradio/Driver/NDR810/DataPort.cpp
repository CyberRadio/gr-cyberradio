/***************************************************************************
 * \file DataPort.cpp
 * \brief Defines the 10GigE data port interface for an NDR810.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR810/DataPort.h"
#include <boost/format.hpp>


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR810
        {

            DataPort::DataPort(int index,
                    ::LibCyberRadio::Driver::RadioHandler* parent,
                     bool debug,
                     const std::string& sourceIP) :
                ::LibCyberRadio::Driver::DataPort(/* const std::string& name */ (boost::format("NDR810-DP%02d") % \
                        index).str(),
                        /* int index */ index,
                        /* RadioHandler* parent */ parent,
                        /* bool debug */ debug,
                        /* const std::string& sourceIP */ sourceIP,
                        /* int numDataPortDipEntries */ 64,
                        /* int dataPortDipEntryIndexBase */ 0)
            {
                initConfigurationDict();
            }

            DataPort::~DataPort()
            {
            }

            DataPort::DataPort(const DataPort& other) :
                ::LibCyberRadio::Driver::DataPort(other)
            {
            }

            DataPort& DataPort::operator=(const DataPort& other)
            {
                ::LibCyberRadio::Driver::DataPort::operator=(other);
                if ( this != &other )
                {
                }
                return *this;
            }

        } // namespace NDR810

    } /* namespace Driver */

} /* namespace LibCyberRadio */

