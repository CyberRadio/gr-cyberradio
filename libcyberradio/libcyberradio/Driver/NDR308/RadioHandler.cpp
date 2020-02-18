/***************************************************************************
 * \file RadioHandler.cpp
 * \brief Defines the radio handler interface for the NDR308.
 * \author DA
 * \author NH
 * \author MN
 * \copyright (c) 2017 CyberRadio Solutions, Inc.  All rights reserved.
 *
 ***************************************************************************/

#include "LibCyberRadio/Driver/NDR308/RadioHandler.h"
#include "LibCyberRadio/Driver/NDR308/DataPort.h"
#include "LibCyberRadio/Driver/NDR308/NbddcComponent.h"
#include "LibCyberRadio/Driver/NDR308/TunerComponent.h"
#include "LibCyberRadio/Driver/NDR308/VitaIfSpec.h"
#include "LibCyberRadio/Driver/NDR308/WbddcComponent.h"
#include "LibCyberRadio/Driver/NDR308/WbddcGroupComponent.h"
#include "LibCyberRadio/Driver/NDR308/NbddcGroupComponent.h"
#include "LibCyberRadio/Common/Pythonesque.h"
#include <sstream>
#include <cstdio>


namespace LibCyberRadio
{

    namespace Driver
    {

        namespace NDR308
        {

            RadioHandler::RadioHandler(bool debug) :
                ::LibCyberRadio::Driver::RadioHandler(
                        /* const std::string& name */ "NDR308",
                        /* int numTuner */ 8,
                        /* int tunerIndexBase */ 1,
                        /* int numWbddc */ 8,
                        /* int wbddcIndexBase */ 1,
                        /* int numNbddc */ 32,
                        /* int nbddcIndexBase */ 1,
                        /* int numTunerBoards */ 2,
                        /* int maxTunerBw */ 6000,
                        /* int numTransmitters */ 0,
                        /* int transmitterIndexBase */ 1,
                        /* int numDuc */ 0,
                        /* int ducIndexBase */ 1,
                        /* int numWbddcGroups */ 4,
                        /* int wbddcGroupIndexBase */ 1,
                        /* int numNbddcGroups */ 8,
                        /* int nbddcGroupIndexBase */ 1,
                        /* int numDdcGroups */ 0,
                        /* int ddcGroupIndexBase */ 1,
                        /* int numDataPorts */ 2,
                        /* int dataPortIndexBase */ 1,
                        /* int numSimpleIpSetups */ 0,
                        /* double adcRate */ 102.4e6,
                        /* VitaIfSpec ifSpec */ NDR308::VitaIfSpec(),
                        /* bool debug */ debug)
            {
                initConfigurationDict();
                _connModesSupported.push_back("tcp");
                _defaultDeviceInfo = 8617;
                // Allocate tuner components
                for (int tuner = _tunerIndexBase;
                        tuner < (_tunerIndexBase + _numTuner); tuner++)
                {

                    _tuners[tuner] = new NDR308::TunerComponent(
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
                    _wbddcs[wbddc] = new NDR308::WbddcComponent(
                            /* int index */ wbddc,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug,
                            /* int dataPort */ 1,
                            /* int rateIndex */ 0,
                            /* int udpDestination */ 0,
                            /* int vitaEnable */ 0,
                            /* int streamId */ 0);
                }
                // Allocate NBDDC components
                for (int nbddc = _nbddcIndexBase;
                        nbddc < (_nbddcIndexBase + _numNbddc); nbddc++)
                {
                    _nbddcs[nbddc] = new NDR308::NbddcComponent(
                            /* int index */ nbddc,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug,
                            /* int dataPort */ 1,
                            /* int rateIndex */ 0,
                            /* int udpDestination */ 0,
                            /* int vitaEnable */ 0,
                            /* int streamId */ 0,
                            /* double frequency */ 0.0,
                            /* int source */ 1);
                }
                // Allocate WBDDC group components
                for (int group = _wbddcGroupIndexBase;
                        group < (_wbddcGroupIndexBase + _numWbddcGroups); group++)
                {
                    _wbddcGroups[group] = new NDR308::WbddcGroupComponent(
                            /* int index */ group,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug);
                }
                // Allocate NBDDC group components
                for (int group = _nbddcGroupIndexBase;
                        group < (_nbddcGroupIndexBase + _numNbddcGroups); group++)
                {
                    _nbddcGroups[group] = new NDR308::NbddcGroupComponent(
                            /* int index */ group,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug);
                }
                // Allocate data ports
                for (int dataPort = _dataPortIndexBase;
                        dataPort < (_dataPortIndexBase + _numDataPorts); dataPort++)
                {
                    _dataPorts[dataPort] = new NDR308::DataPort(
                            /* int index */ dataPort,
                            /* RadioHandler* parent */ this,
                            /* bool debug */ _debug,
                    /* const std::string& sourceIP */ "0.0.0.0");
                }
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

            void RadioHandler::queryConfiguration()
            {
                this->debug("[NDR308::RadioHandler::queryConfiguration] Called\n");
                // Purge the banner sent over when a connection is made.
                BasicStringList rsp = _transport.receive(_defaultTimeout);
                // Call the base-class queryConfiguration() to retrieve identity info
                // and query configuration for all components
                ::LibCyberRadio::Driver::RadioHandler::queryConfiguration();
                this->debug("[NDR308::RadioHandler::queryConfiguration] Returning\n");
            }

            bool RadioHandler::queryVersionInfo()
            {
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Called\n");
                // First, call the base-class version
                bool ret = ::LibCyberRadio::Driver::RadioHandler::queryVersionInfo();
                // Next, use the hardware version info string to determine
                // -- unit revision
                // -- number of tuner boards
                // -- max tuner bandwidth
                if ( ret )
                {
                    // Set number of installed tuner boards to zero
                    _numTunerBoards = 0;
                    // Progress state tracker: 0=Unit, 1=Digital Board, 2+=Tuner Boards
                    int stateTracker = -1;
                    // Split the hardware version info string into separate lines
                    BasicStringList vec = Pythonesque::Split(_versionInfo["hardwareVersion"], "\n");
                    // Iterate over the list
                    for (BasicStringList::iterator it = vec.begin(); it != vec.end(); it++)
                    {
                        // First, determine if the current line indicates a change in progress state
                        if ( it->find("Unit") == 0 )
                            stateTracker = 0;
                        else if ( it->find("Digital Board") == 0 )
                            stateTracker = 1;
                        else if ( it->find("Tuner Quad") == 0 )
                            stateTracker = 2;
                        // Then use the current line to determine other quantities
                        switch( stateTracker )
                        {
                            case 0:
                                if ( it->find("  Revision: ") != std::string::npos )
                                    _versionInfo["unitRevision"] = Pythonesque::Replace(*it, "  Revision: ", "");
                                break;
                            case 1:
                                break;
                            case 2:
                                if ( ( it->find("Tuner Quad") == 0) && ( it->find("Not Installed") != std::string::npos) )
                                    _numTunerBoards++;
                                else if ( it->find("Bandwidth: ") == 0 )
                                {
                                    std::string tmp = Pythonesque::Replace(*it, "Bandwidth: ", "");
                                    std::istringstream iss(tmp);
                                    // Handle the corner case where the radio doesn't report its
                                    // maximum tuner bandwidth properly (returning 0 for BW).
                                    int value;
                                    iss >> value;
                                    if ( value != 0 )
                                        _maxTunerBw = value;
                                }
                                break;
                            default:
                                break;
                        }

                    }
                }
                // Calculate number of tuners/WBDDCs from tuner boards
                _numTuner = std::min(_numTuner, _numTunerBoards * 4);
                _numWbddc = _numTuner;
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Number of tuner boards=%d\n", _numTunerBoards);
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Number of tuners=%d\n", _numTuner);
                // Deallocate any tuners and DDCs that don't have a tuner board
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Deallocating nonexistent tuners/WBDDCs\n");
                TunerComponentDict::iterator it = _tuners.begin();
                for (; it != _tuners.end(); )
                {
                    if ( it->first >= (_tunerIndexBase + _numTuner) )
                    {
                        this->debug("[NDR308::RadioHandler::queryVersionInfo] -- Deallocating tuner=%d\n", it->first);
                        delete it->second;
                        _tuners.erase(it++);
                    }
                    else
                    {
                        this->debug("[NDR308::RadioHandler::queryVersionInfo] -- OK tuner=%d\n", it->first);
                        it++;
                    }
                }
                WbddcComponentDict::iterator it2 = _wbddcs.begin();
                for (; it2 != _wbddcs.end(); )
                {
                    if ( it2->first >= (_wbddcIndexBase + _numWbddc) )
                    {
                        this->debug("[NDR308::RadioHandler::queryVersionInfo] -- Deallocating WBDDC=%d\n", it2->first);
                        delete it2->second;
                        _wbddcs.erase(it2++);
                    }
                    else
                    {
                        this->debug("[NDR308::RadioHandler::queryVersionInfo] -- OK WBDDC=%d\n", it2->first);
                        it2++;
                    }
                }
                // Determine frequency range from max bandwidth
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Max tuner bandwidth=%d MHz\n", _maxTunerBw);
                for (it = _tuners.begin(); it != _tuners.end(); it++)
                {
                    it->second->setFrequencyRangeMax(_maxTunerBw * 1e6);
                }
                // Debug dump
                if (ret)
                {
                    for (BasicStringStringDict::iterator it = _versionInfo.begin(); it != _versionInfo.end(); it++)
                    {
                        this->debug("[NDR308::RadioHandler::queryVersionInfo] %s = \"%s\"\n", it->first.c_str(), it->second.c_str());
                    }
                }
                this->debug("[NDR308::RadioHandler::queryVersionInfo] Returning %s\n", debugBool(ret));
                return ret;
            }

            // NOTE: The default implementation is the NDR308 implementation,
            // but this just makes it explicit in the code.
            bool RadioHandler::executeQueryIDN(std::string& model,
                    std::string& serialNumber)
            {
                return ::LibCyberRadio::Driver::RadioHandler::executeQueryIDN(model, serialNumber);
            }

            // NOTE: The default implementation is the NDR308 implementation,
            // but this just makes it explicit in the code.
            bool RadioHandler::executeQueryVER(std::string& softwareVersion,
                    std::string& firmwareVersion,
                    std::string& referenceVersion,
                    std::string& firmwareDate)
            {

                return ::LibCyberRadio::Driver::RadioHandler::executeQueryVER(softwareVersion,
                        firmwareVersion,
                        referenceVersion,
                        firmwareDate);
            }

            // NOTE: The default implementation is the NDR308 implementation,
            // but this just makes it explicit in the code.
            bool RadioHandler::executeQueryHREV(std::string& hardwareInfo)
            {
                return ::LibCyberRadio::Driver::RadioHandler::executeQueryHREV(hardwareInfo);
            }

        } /* namespace NDR308 */

    } /* namespace Driver */

} /* namespace LibCyberRadio */
