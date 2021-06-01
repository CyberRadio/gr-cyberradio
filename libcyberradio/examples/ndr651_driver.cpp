/************************************************************************
 * \file ndr651_driver.cpp
 * \brief NDR651 test app using the CyberRadio Driver (C++)
 * \author DA
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.  All rights
 *    reserved.
 */

#include "LibCyberRadio/Common/App.h"
#include "LibCyberRadio/Driver/Driver.h"
#include <unistd.h>
#include <iostream>

/**
 * \brief Provides application functionality.
 */
class App : public LibCyberRadio::App
{
    public:
        /**
         * \brief Constructor.
         */
        App() : LibCyberRadio::App(),
            _verbose(false),
            _channel(1),
            _dataPort(1),
            _dipIndex(0),
            _frequency(900e6),
            _attenuation(0.0),
            _dwellTime(10),
            _host("ndr651")
        {
            description = "NDR651 Data Streaming Example";
            version = "18.06.19";
        }

        /**
         * \brief Destructor.
         */
        virtual ~App()
        {
        }

    protected:
        // Define application options
        virtual void defineOptions(const char *argv0)
        {
            LibCyberRadio::App::defineOptions(argv0);
            _optParser.setUnparsedArgText("");
            _optParser.setEpilogText("");
            _optParser.addOption("v", "verbose",
                  LibCyberRadio::AppOption::TYPE_BOOLEAN_SET_TRUE,
                  (void*)&_verbose, "", "Set verbose mode", true);
            _optParser.addOption("h", "host",
                  LibCyberRadio::AppOption::TYPE_STRING,
                  (void*)&_host, "HOST", "Set host name/IP address", true);
            _optParser.addOption("c", "channel",
                  LibCyberRadio::AppOption::TYPE_INTEGER,
                  (void*)&_channel, "CHAN", "Set channel", true);
            _optParser.addOption("d", "data-port",
                  LibCyberRadio::AppOption::TYPE_INTEGER,
                  (void*)&_dataPort, "PORT", "Set data port index", true);
            _optParser.addOption("i", "dip-index",
                  LibCyberRadio::AppOption::TYPE_INTEGER,
                  (void*)&_dipIndex, "DIP", "Set DIP table index", true);
            _optParser.addOption("f", "frequency",
                  LibCyberRadio::AppOption::TYPE_DOUBLE,
                  (void*)&_frequency, "FRQ", "Set tuner frequency (Hz)", true);
            _optParser.addOption("a", "attenuation",
                  LibCyberRadio::AppOption::TYPE_DOUBLE,
                  (void*)&_attenuation, "ATT", "Set tuner attenuation (dB)", true);
            _optParser.addOption("t", "dwell-time",
                  LibCyberRadio::AppOption::TYPE_INTEGER,
                  (void*)&_dwellTime, "SECS", "Set dwell time (seconds)", true);
        }

        // Run main processing loop
        virtual int mainLoop()
        {
            int ret = 0;
            std::cout << "Connecting radio handler..." << std::endl;
            std::shared_ptr<LibCyberRadio::Driver::RadioHandler> handler =
                    LibCyberRadio::Driver::getRadioObject("ndr651", _host,
                                                          -1, _verbose);
            if ( (handler != NULL) && handler->isConnected() )
            {
                std::cout << "-- Connect SUCCESS" << std::endl;
                handler->setTenGigFlowControlStatus(true);
                if ( setupBroadcastOnDataPorts(handler.get(), 11001) == false )
                    ret = 1;
                if ( ret == 0 )
                {
                    if ( setupChannel(handler.get(), _channel, _dataPort,
                                      _dipIndex, _frequency, _attenuation) == false )
                        ret = 1;
                }
                if ( ret == 0 )
                {
                    std::cout << "Collecting data for " << _dwellTime
                              << " seconds..." << std::endl;
                    sleep(_dwellTime);
                    std::cout << "-- Complete" << std::endl;
                    std::cout << "Disabling WBDDC..." << std::endl;
                    handler->disableWbddc(_channel);
                    LibCyberRadio::Driver::ConfigurationDict cfg = handler->getConfiguration();
                    dumpConfig(cfg);
                    std::cout << "Disconnecting radio handler..." << std::endl;
                    handler->disconnect();
                }
            }
            else
            {
                std::cout << "-- Connect FAILED" << std::endl;
                ret = 1;
            }
            std::cout << "DONE" << std::endl;
            return ret;
        }

        /**
         * \brief Dumps a configuration dictionary to standard output.
         * \param cfg Configuration dictionary.
         */
        virtual void dumpConfig(const LibCyberRadio::Driver::ConfigurationDict& cfg)
        {
            std::cout << "    Configuration(" << std::endl;
            LibCyberRadio::Driver::ConfigurationDict::const_iterator it;
            for ( it = cfg.begin(); it != cfg.end(); it++)
            {
                std::cout << "        " << it->first << " = " << it->second << std::endl;
            }
            std::cout << "    )" << std::endl;
        }

        /**
         * \brief Configures the given radio's DIP table entries so that it sends data
         *    using UDP broadcast.
         *
         * Starting at the given port base, this method assigns one UDP port number
         * per DIP table entry affected.  It iterates through all DIP table entries
         * on a data port before moving on to the next.
         *
         * \param handler Radio handler object.
         * \param udpPortBase Base port number for UDP destination ports.
         * \returns True if the operation completes successfully, false otherwise.
         */
        virtual bool setupBroadcastOnDataPorts(
                LibCyberRadio::Driver::RadioHandler* handler,
                unsigned int udpPortBase)
        {
            // Return code
            bool ret = true;
            // Collect data port information from the driver
            LibCyberRadio::BasicIntList dataPorts = handler->getDataPortIndexRange();
            LibCyberRadio::BasicIntList dipIndices = handler->getDataPortDipEntryIndexRange();
            // Base for assigning UDP ports
            int currPort = udpPortBase;
            // Iterate over all data port indices
            for (LibCyberRadio::BasicIntList::const_iterator it = dataPorts.begin();
                 it != dataPorts.end(); it++)
            {
                std::cout << "Setting Data Port "
                          << *it
                          << " configuration..." << std::endl;
                // Set the source IP address for the data port
                // -- NOTE: Using 0.0.0.0 for source IP because we are doing broadcast
                ret &= handler->setDataPortSourceIP(*it, "0.0.0.0");
                if (ret)
                {
                    // Iterate over all DIP entry indices
                    for (LibCyberRadio::BasicIntList::const_iterator itd = dipIndices.begin();
                         itd != dipIndices.end(); itd++)
                    {
                        // Set info for this destination table index
                        // -- NOTE: Using 255.255.255.255 for destination IP and
                        //    FF:FF:FF:FF:FF:FF for destination MAC because we are
                        //    doing broadcast
                        ret &= handler->setDataPortDestInfo(*it, *itd,
                                                           "255.255.255.255",
                                                           "FF:FF:FF:FF:FF:FF",
                                                           currPort,
                                                           currPort);
                        // Stop iterating if an error occurs
                        if (!ret)
                            break;
                        // Increment data port
                        currPort++;
                    }
                }
                // Stop iterating if an error occurs
                if (!ret)
                    break;
            }
            return ret;
        }

        /**
         * \brief Configures the radio to start streaming data for a given
         *     channel.
         * \param handler Radio handler object.
         * \param channel Channel number.
         * \param dataPort Data port index used for transmitting the data.
         * \param dipIndex DIP table index specifying the UDP destination info.
         * \param frequency Tuner frequency (Hz).
         * \param attenuation Tuner attenuation (dB).
         * \returns True if the operation completes successfully, false otherwise.
         */
        virtual bool setupChannel(
                LibCyberRadio::Driver::RadioHandler* handler,
                int channel, int dataPort, int dipIndex,
                double frequency, double attenuation)
        {
            // Return value
            bool ret = true;
            // Configuration dictionary objects
            // -- NOTE: Using configuration dictionaries allows users to
            //    affect multiple settings at the same time.
            // -- NOTE: Configuration dictionary entries can be assigned
            //    most simple data types -- Booleans, integers, floating-
            //    point values, and strings.
            LibCyberRadio::Driver::ConfigurationDict tcfg, wcfg;
            // Set up the tuner for the given channel
            std::cout << "Setting up Tuner "
                      << channel
                      << "..." << std::endl;
            tcfg["frequency"] = frequency;
            tcfg["attenuation"] = attenuation;
            ret &= handler->setTunerConfiguration(channel, tcfg);
            if ( ret )
            {
                // Set up the WBDDC for the given channel
                std::cout << "Setting up WBDDC "
                          << channel
                          << "..." << std::endl;
                // -- Set "enable" to true so that it will transmit data
                wcfg["enable"] = true;
                wcfg["rateIndex"] = 0;
                wcfg["udpDestination"] = dipIndex;
                wcfg["vitaEnable"] = 3;
                wcfg["streamId"] = channel;
                wcfg["dataPort"] = dataPort;
                ret &= handler->setWbddcConfiguration(channel, wcfg);
            }
            return ret;
        }

    protected:
        // Verbose mode
        bool _verbose;
        // Channel number
        int _channel;
        // Data port number
        int _dataPort;
        // DIP table index number
        int _dipIndex;
        // Tuner frequency
        double _frequency;
        // Tuner attenuation
        double _attenuation;
        // Dwell time (seconds)
        int _dwellTime;
        // Host name/IP address
        std::string _host;
};


/**
 * \brief Main program loop.
 * \param argc Number of command-line arguments.
 * \param argv Array of strings containing the command-line arguments.
 * \returns 0 on success, anything else on error.
 */
int main(int argc, char *argv[])
{
    App app;
    return app.run(argc, argv);
}
