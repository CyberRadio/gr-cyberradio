/***************************************************************************
 * \file Driver.cpp
 * \brief Main entry point for the C++ CyberRadio Driver.
 * \author DA
 * \copyright (c) 2018 CyberRadio Solutions, Inc.  All rights reserved.
 *
 * \note Requires C++11 compiler support.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/Driver.h"
#include "LibCyberRadio/Driver/NDR308/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR308TS/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR472/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR651/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR810/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR551/RadioHandler.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include "LibCyberRadio/Common/BasicList.h"
#include "LibCyberRadio/Common/Debuggable.h"
#include <algorithm>
#include <stdlib.h>
#include <iostream>


namespace LibCyberRadio
{

    namespace Driver
    {

        RadioHandlerPtr getRadioObject(
                const std::string& nameString,
                const std::string& device,
                int devicePort,
                bool debug)
        {
            Debuggable dbg(debug, "getRadioObject");
            dbg.debug("Called\n");
            dbg.debug("-- Name string = \"%s\"\n", nameString.c_str());
            RadioHandlerPtr sptr = NULL;
            // Adjust the incoming name string
            // -- NOTE: This operation requires that we pre-fill the adjusted
            //    name string (assume all characters are copied), and then
            //    trim the string after the conditional copy.
            std::string adjNameString = nameString;
            // -- Copy alphanumeric characters from input string to adjusted
            //    name string
            std::string::iterator its = std::copy_if(nameString.begin(),
                                                     nameString.end(),
                                                     adjNameString.begin(),
                                                     isalnum );
            adjNameString.erase(its, adjNameString.end());
            // -- Convert adjusted name string to lower case
            std::transform(adjNameString.begin(), adjNameString.end(),
                           adjNameString.begin(), tolower);
            // [FUTURE] Support radio auto-detection
            // Get an appropriate radio handler object based on name string
            dbg.debug("Getting handler for \"%s\"...\n", adjNameString.c_str());
            if ( adjNameString == "ndr308" )
            {
                dbg.debug("-- FOUND ndr308\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR308::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr308ts" )
            {
                dbg.debug("-- FOUND ndr308ts\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR308TS::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr308a" )
            {
                dbg.debug("-- FOUND ndr308\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR308::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr651" )
            {
                dbg.debug("-- FOUND ndr651\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR651::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr810" )
            {
                dbg.debug("-- FOUND ndr810\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR810::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr472" )
            {
                dbg.debug("-- FOUND ndr472\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR472::RadioHandler(debug)
                       );
            }
            else if ( adjNameString == "ndr551" )
            {
                dbg.debug("-- FOUND ndr551\n");
                sptr = std::shared_ptr<RadioHandler>(
                        (RadioHandler*)new NDR551::RadioHandler(debug)
                       );
            }
            else
            {
                dbg.debug("-- CANNOT FIND %s\n", adjNameString.c_str());
            }
            // Support radio auto-connection
            if ( (sptr != NULL) && (device != "") )
            {
                dbg.debug("Auto-connection started...\n");
                dbg.debug("-- Device = %s\n", device.c_str());
                BasicStringList connModes = sptr->getConnectionModeList();
                for (BasicStringList::const_iterator it = connModes.begin();
                     it != connModes.end(); it++)
                {
                    dbg.debug("-- Attempting connection mode: %s\n", it->c_str());
                    sptr->connect(*it, device, sptr->getDefaultDeviceInfo());
                    if ( sptr->isConnected() )
                        break;
                }
            }
            // Return the pointer to the radio handler (or NULL)
            //dbg.debug("Returning %08p\n", sptr.get());
            return sptr;
        }

    } // namespace Driver

} // namespace LibCyberRadio

