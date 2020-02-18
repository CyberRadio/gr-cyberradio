/***************************************************************************
 * \file RadioHandler.cpp
 * \brief Defines the radio handler interface for the NDR472.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR472/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR472/SimpleIpSetup.h"
#include "LibCyberRadio/Driver/NDR472/TunerComponent.h"
#include "LibCyberRadio/Driver/NDR472/VitaIfSpec.h"
#include "LibCyberRadio/Driver/NDR472/WbddcComponent.h"
#include "LibCyberRadio/Driver/NDR472/WbddcGroupComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <boost/lexical_cast.hpp>
#include <sstream>
#include <cstdio>


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR472
        {

            RadioHandler::RadioHandler(bool debug) :
                ::LibCyberRadio::Driver::RadioHandler(
                        /* const std::string& name */ "NDR472",
                        /* int numTuner */ 2,
                        /* int tunerIndexBase */ 1,
                        /* int numWbddc */ 2,
                        /* int wbddcIndexBase */ 1,
                        /* int numNbddc */ 0,
                        /* int nbddcIndexBase */ 1,
                        /* int numTunerBoards */ 1,
                        /* int maxTunerBw */ 3000,
                        /* int numTransmitters */ 0,
                        /* int transmitterIndexBase */ 1,
                        /* int numDuc */ 0,
                        /* int ducIndexBase */ 1,
                        /* int numWbddcGroups */ 2,
                        /* int wbddcGroupIndexBase */ 1,
                        /* int numNbddcGroups */ 0,
                        /* int nbddcGroupIndexBase */ 1,
                        /* int numDdcGroups */ 0,
                        /* int ddcGroupIndexBase */ 1,
                        /* int numDataPorts */ 0,
                        /* int dataPortIndexBase */ 1,
                        /* int numSimpleIpSetups */ 1,
                        /* double adcRate */ 128e6,
                        /* VitaIfSpec ifSpec */ NDR472::VitaIfSpec(),
                        /* bool debug */ debug)
            {
                initConfigurationDict();
                _connModesSupported.push_back("tty");
                _defaultDeviceInfo = 921600;
                // Allocate tuner components
                for (int tuner = _tunerIndexBase;
                        tuner < (_tunerIndexBase + _numTuner); tuner++)
                {

                    _tuners[tuner] = new NDR472::TunerComponent(
                            /* int index */ tuner,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug,
                            /* double frequency */ 800e6,
                            /* double attenuation */ 0.0,
                            /* int filter */ 0);
                }
                // Allocate WBDDC components
                for (int wbddc = _wbddcIndexBase;
                        wbddc < (_wbddcIndexBase + _numWbddc); wbddc++)
                {
                    _wbddcs[wbddc] = new NDR472::WbddcComponent(
                            /* int index */ wbddc,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug,
                            /* int dataPort */ 1,
                            /* int rateIndex */ 0,
                            /* int udpDestination */ 0,
                            /* int vitaEnable */ 0,
                            /* int streamId */ 0);
                }
                // This radio has no NBDDC components
                // Allocate WBDDC group components
                for (int group = _wbddcGroupIndexBase;
                        group < (_wbddcGroupIndexBase + _numWbddcGroups); group++)
                {
                    _wbddcGroups[group] = new NDR472::WbddcGroupComponent(
                            /* int index */ group,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug);
                }
                // This radio has no NBDDC group components
                // This radio has no 10-Gig data ports
                // Allocate a simple IP setup object
                _simpleIpSetups[0] = new NDR472::SimpleIpSetup(
                        /* RadioHandler* parent */ this,
                        /* bool debug */ _debug,
                        /* const std::string& sourceIP */ "0.0.0.0",
                        /* const std::string& destIP */ "0.0.0.0",
                /* const std::string& destMAC */ "00:00:00:00:00:00");
            }

            RadioHandler::~RadioHandler()
            {
            }

            RadioHandler::RadioHandler(const RadioHandler &other) :
                ::LibCyberRadio::Driver::RadioHandler(other)
            {
            }

            RadioHandler& RadioHandler::operator=(const RadioHandler& other)
            {
                ::LibCyberRadio::Driver::RadioHandler::operator=(other);
                // Block self-assignment
                if (this != &other)
                {
                }
                return *this;
            }

            // OVERRIDE
            void RadioHandler::initConfigurationDict()
            {
                //this->debug("[NDR472::RadioHandler::initConfigurationDict] Called\n");
                _config.clear();
                _config["configMode"] = _configMode;
                _config["referenceMode"] = _referenceMode;
                _config["freqNormalization"] = _freqNormalization;
                _config["gpsEnable"] = _gpsEnabled;
                _config["referenceTuningVoltage"] = _referenceTuningVoltage;
                //this->debug("[NDR472::RadioHandler::initConfigurationDict] Returning\n");
            }

            // OVERRIDE
            void RadioHandler::queryConfiguration()
            {
                this->debug("[NDR472::RadioHandler::queryConfiguration] Called\n");
                // Call the base-class queryConfiguration() to retrieve identity info
                // and query configuration for all components
                ::LibCyberRadio::Driver::RadioHandler::queryConfiguration();
                this->debug("[NDR472::RadioHandler::queryConfiguration] Returning\n");
            }

            // OVERRIDE
            bool RadioHandler::queryVersionInfo()
            {
                this->debug("[NDR472::RadioHandler::queryVersionInfo] Called\n");
                // First, call the base-class version
                bool ret = ::LibCyberRadio::Driver::RadioHandler::queryVersionInfo();
                // Next, use the hardware version info string to determine
                // -- unit revision (N/A for this radio)
                // -- number of tuner boards (always 1)
                // -- max tuner bandwidth (always 3000)
                // Debug dump
                if (ret)
                {
                    for (BasicStringStringDict::iterator it = _versionInfo.begin(); it != _versionInfo.end(); it++)
                    {
                        this->debug("[NDR472::RadioHandler::queryVersionInfo] %s = \"%s\"\n", it->first.c_str(), it->second.c_str());
                    }
                }
                this->debug("[NDR472::RadioHandler::queryVersionInfo] Returning %s\n",
                        this->debugBool(ret));
                return ret;
            }

            // OVERRIDE
            // NDR472 response:
            //     NDR472
            //     S/N 01004
            //     OK
            bool RadioHandler::executeQueryIDN(std::string& model,
                    std::string& serialNumber)
            {
                bool ret = false;
                // Issue the identity query to get model and serial number
                BasicStringList rsp = sendCommand("*IDN?\n", _defaultTimeout);
                if ( getLastCommandErrorInfo() == "" )
                {
                    BasicStringList::iterator it;
                    for (it = rsp.begin(); it != rsp.end(); it++)
                    {
                        if ( it->find("NDR") != std::string::npos )
                            model = *it;
                        if ( it->find("S/N ") != std::string::npos )
                            serialNumber = Pythonesque::Replace(*it, "S/N ", "");
                    }
                    ret = true;
                }
                return ret;
            }

            // OVERRIDE
            // NDR472 response:
            //     NDR472 Application code:
            //        REV: 14.05.30
            //     FPGA
            //        Loaded Image: 0   Rev: 14.05.28   Date:00.00.00
            //       *FLASH Image 0: 00 FF
            //        FLASH Image 1: 01 FF
            //     OK
            bool RadioHandler::executeQueryVER(std::string& softwareVersion,
                    std::string& firmwareVersion,
                    std::string& referenceVersion,
                    std::string& firmwareDate)
            {
                bool ret = true;
                // Query the version command to get software versioning info
                BasicStringList rsp = sendCommand("VER?\n", _defaultTimeout);
                if ( getLastCommandErrorInfo() == "" )
                {
                    BasicStringList::iterator it;
                    bool parsingAppCode = false;
                    bool parsingFpga = false;
                    for (it = rsp.begin(); it != rsp.end(); it++)
                    {
                        if ( it->find("Application code") != std::string::npos )
                        {
                            parsingAppCode = true;
                            parsingFpga = false;
                        }
                        if ( it->find("FPGA") != std::string::npos )
                        {
                            parsingAppCode = false;
                            parsingFpga = true;
                        }
                        if ( parsingAppCode )
                        {
                            if ( it->find("   REV: ") != std::string::npos )
                                softwareVersion = Pythonesque::Replace(*it, "   REV: ", "");
                        }
                        else if ( parsingFpga )
                        {
                            if ( it->find("Loaded Image") != std::string::npos )
                            {
                                std::string tmp = Pythonesque::Strip(*it);
                                BasicStringList vec = Pythonesque::Split(tmp, "   ");
                                // vec[0] = FPGA image that is loaded
                                // vec[1] = Firmware version
                                firmwareVersion = Pythonesque::Replace(vec[1], "Rev: ", "");
                                // vec[2] = Firmware date
                                firmwareDate = Pythonesque::Replace(vec[2], "Date:", "");

                            }
                        }
                    }
                    ret = true;
                }
                return ret;
            }

            // OVERRIDE
            // NDR472 response:
            //     Unit Model: NDR472
            //        S/N: 01004
            //     Digital Board Model: 602863
            //        S/N: 00007
            //        Rev: 01.00  05/03/2013
            //     Tuner Board Model: 601987-02
            //        S/N 1: 00005
            //        Rev: 03.00  05/03/2013
            //     OK
            bool RadioHandler::executeQueryHREV(std::string& hardwareInfo)
            {
                bool ret = true;
                // Query the hardware revision command to get other stuff
                BasicStringList rsp = sendCommand("HREV?\n", _defaultTimeout);
                if ( getLastCommandErrorInfo() == "" )
                {
                    std::ostringstream oss;
                    BasicStringList::iterator it;
                    bool parsingUnitModel = false;
                    for (it = rsp.begin(); it != rsp.end(); it++)
                    {
                        if ( (*it != "OK") && (*it != "HREV?") )
                        {
                            if ( Pythonesque::Startswith(*it, "Unit Model") )
                            {
                                parsingUnitModel = true;
                            }
                            if ( Pythonesque::Startswith(*it, "Digital Board Model") ||
                                    Pythonesque::Startswith(*it, "Tuner Board Model") )
                            {
                                parsingUnitModel = false;
                            }
                            if ( !parsingUnitModel )
                            {
                                if ( oss.str() != "" )
                                    oss << "\n";
                                //oss << Pythonesque::Strip(*it);
                                oss << *it;
                            }
                        }
                    }
                    hardwareInfo = oss.str();
                    ret = true;
                }
                return ret;
            }

        } /* namespace NDR472 */

    } /* namespace Driver */

} /* namespace LibCyberRadio */
