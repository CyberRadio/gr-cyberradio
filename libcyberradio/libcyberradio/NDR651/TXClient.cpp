#include "LibCyberRadio/NDR651/TXClient.h"

namespace LibCyberRadio
{
    namespace NDR651
    {
        TXClient::TXClient(std::string radioHostName, bool debug):
            Debuggable(debug, "TXClient"),
            txInterfaceName(""),  // Invalid
            tenGbeIndex(INVALID_VALUE),  // Invalid
            ducChannel(INVALID_VALUE),  // Invalid
            ducAttenuation(0),  // Optional
            ducRateIndex(INVALID_VALUE), // Invalid
            rfChannel(INVALID_VALUE),  // Invalid
            txUdpPort(0),  // Invalid (use 0 to avoid overflow though)
            ducFreq(0),   // Optional
            ducFullThreshPercent(0.90),  // Optional
            ducEmptyThreshPercent(0.82),  // Optional
            updatesPerSecond(20), // Optional (flowControlUpdatesPerSecond)
            txFreq(INVALID_VALUE),  // Invalid
            txAttenuation(0), // Optional
            txInversion(false),
            radioHostName(radioHostName),
            debugOn(debug),
            // Internals
            packetizer(NULL),
            statusRX(NULL),
            rc(NULL),
            txSock(0),
            isGrouped(false),
            isRunning(false),
            DUCPaused(true),
            DUCReady(false),
            prefillSampleCount(0L)
        {
            // Create a radio controller (sends cmds to 651)
            this->rc = new RadioController(radioHostName, 8617, debug);
        }

        TXClient::~TXClient()
        {
            if (this->rc != NULL)
            {
                delete this->rc;
            }
            if (this->statusRX != NULL)
            {
                delete this->statusRX;
            }
            if (this->packetizer != NULL)
            {
                delete this->packetizer;
            }
        }

        /********* PRIVATE METHODS **********/
        std::string TXClient::getSourceMac()
        {
            if (this->packetizer != NULL)
            {
                // Source MAC Address
                char macstring[32];
                struct ifreq ifr;
                memset(&ifr, 0x00, sizeof(ifr));
                strcpy(ifr.ifr_name, this->txInterfaceName.c_str());
                ioctl(this->packetizer->getSocketFd(), SIOCGIFHWADDR, &ifr);
                sprintf(macstring, "%02x:%02x:%02x:%02x:%02x:%02x",
                        (unsigned char)ifr.ifr_hwaddr.sa_data[0],
                        (unsigned char)ifr.ifr_hwaddr.sa_data[1],
                        (unsigned char)ifr.ifr_hwaddr.sa_data[2],
                        (unsigned char)ifr.ifr_hwaddr.sa_data[3],
                        (unsigned char)ifr.ifr_hwaddr.sa_data[4],
                        (unsigned char)ifr.ifr_hwaddr.sa_data[5]);
                return std::string(macstring);
            }
            return NULL;
        }

        std::string TXClient::getSourceIP()
        {
            if (this->packetizer != NULL)
            {
                struct ifreq ifr;
                ifr.ifr_addr.sa_family = AF_INET;
                strncpy(ifr.ifr_name, this->txInterfaceName.c_str(), IFNAMSIZ-1);
                ioctl(this->packetizer->getSocketFd(), SIOCGIFADDR, &ifr);
                return std::string(inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));
            }
            return NULL;
        }

        bool TXClient::validInputs(std::string &errors)
        {
            // I am not checking the validity of these inputs because the radio does that better (hopefully)
            // I am only checking if the default values from the constructor were changed, which is enough to determine if called the config methods were called.
            bool valid = true;
            if (this->txInterfaceName.empty()) {
                errors += "Tx Interface Name not configured\n";
                valid = false;
            }
            if (this->tenGbeIndex == INVALID_VALUE) {
                errors += "Ten GBE Index not configured.\n";
                valid = false;
            }
            if (this->ducChannel == INVALID_VALUE) {
                errors += "DUC Channel not configured.\n";
                valid = false;
            }
            if (this->ducRateIndex == INVALID_VALUE) {
                errors += "DUC Rate Index not configured.\n";
                valid = false;
            }
            if (this->rfChannel == INVALID_VALUE) {
                errors += "RF TX Channel not configured.\n";
                valid = false;
            }
            if (this->txUdpPort == 0) {
                errors += "TX UDP Port not configured.\n";
                valid = false;
            }
            // if ((((int)(this->txFreq)) == INVALID_VALUE)) {
            // errors += "TX Frequency not configured.\n";
            // valid = false;
            // }
            return valid;
        }

        /* Public Methods */

        /********* ACCESSORS **********/
        void TXClient::setGrouped(bool isGrouped)
        {
            this->isGrouped = isGrouped;
        }

        bool TXClient::isDUCPaused()
        {
            return this->DUCPaused;
        }

        bool TXClient::setDUCPaused(bool paused)
        {
            std::cout << "setDUCPaused( " << this->DUCPaused << " -> " << paused << " )" << std::endl;
            this->DUCPaused = paused;
            bool ret = true;
            return ret;
        }

        bool TXClient::isDUCReady()
        {
            // std::cout << "isDUCReady() = " << this->DUCReady << std::endl;
            return this->DUCReady;
        }

        unsigned int TXClient::getDucChannel()
        {
            return this->ducChannel;
        }

        // Public Config Functions
        void TXClient::disableRF()
        {
            // TXP off
            this->debug("[disableRF] Called\n");
            this->rc->setTXP(this->rfChannel, false);
            this->debug("[disableRF] Returning\n");
        }

        bool TXClient::setDUCChannel(unsigned int ducChannel)
        {
            this->debug("[setDUCChannel] Called\n");
            this->debug("[setDUCChannel] -- ducChannel = %u\n", ducChannel);
            bool ret = false;
            if (!this->isRunning)
            {
                this->ducChannel = ducChannel;
                ret = true;
            }
            this->debug("[setDUCChannel] Returning %s\n", debugBool(ret) );
            return ret;
        }

        bool TXClient::setTxChannel(unsigned int txChannel)
        {
            bool ret = false;
            this->debug("[setTxChannel] Called\n");
            this->debug("[setTxChannel] -- txChannel = %u\n", txChannel);
            if (!this->isRunning) {
                this->rfChannel = txChannel;
                ret = true;
            }
            this->debug("[setTxChannel] Returning %s\n", debugBool(ret) );
            return ret;
        }

        // Should be able to be called on the fly
        bool TXClient::setDUCRateIndex(unsigned int ducRateIndex)
        {
            // if (!this->isRunning) {
            // this->ducRateIndex = ducRateIndex;
            // return true;
            // }
            // return false;
            this->debug("[setDUCRateIndex] Called\n");
            this->debug("[setDUCRateIndex] -- ducRateIndex = %u\n", ducRateIndex);
            boost::mutex::scoped_lock lock(this->objectAccessMutex);
            bool ret = this->setDUCRateIndexUnlocked(ducRateIndex);
            this->debug("[setDUCRateIndex] Returning %s\n", debugBool(ret) );
            return ret;
        }

        // Should be able to be called on the fly
        bool TXClient::setDUCFreq(double ducFreq)
        {
            this->debug("[setDUCFreq] Called\n");
            this->debug("[setDUCFreq] -- ducFreq = %f\n", ducFreq);
            boost::mutex::scoped_lock lock(this->objectAccessMutex);
            bool result = false;
            if (this->ducChannel != INVALID_VALUE)
            {
                result = this->rc->setDUCF(this->ducChannel, ducFreq);
                if (result == true)
                {
                    this->ducFreq = ducFreq;
                }
            }
            else
            {
                // Not configured yet
                this->debug("[setDUCFreq] Not configured yet!\n");
            }
            this->debug("[setDUCFreq] Returning %s\n", debugBool(result) );
            return result;
        }

        // Can be called on the fly
        bool TXClient::setDUCAtten(double ducAttenuation)
        {
            this->debug("[setDUCAtten] Called\n");
            this->debug("[setDUCAtten] -- ducAttenuation = %f\n", ducAttenuation);
            boost::mutex::scoped_lock lock(this->objectAccessMutex);
            bool result = false;
            if (this->ducChannel != INVALID_VALUE)
            {
                result = this->rc->setDUCA(this->ducChannel, ducAttenuation);
                if (result == true)
                {
                    this->ducAttenuation = ducAttenuation;
                }
            }
            else
            {
                // Not configured yet
                this->debug("[setDUCAtten] Not configured yet!\n");
            }
            this->debug("[setDUCAtten] Returning %s\n", debugBool(result) );
            return result;
        }

        bool TXClient::setDUCParameters(unsigned int ducIndex, unsigned int ducRateIndex, unsigned int txChannel)
        {
            this->debug("[setDUCParameters] Called\n");
            this->debug("[setDUCParameters] -- ducIndex = %u\n", ducIndex);
            this->debug("[setDUCParameters] -- ducRateIndex = %u\n", ducRateIndex);
            this->debug("[setDUCParameters] -- txChannel = %u\n", txChannel);
            boost::mutex::scoped_lock lock(this->objectAccessMutex);
            //bool success = true;
            //success = success && this->setDUCChannel(ducIndex);
            //success = success && this->setDUCRateIndex(ducRateIndex);
            //success = success && this->setTxChannel(txChannel);
            bool success = this->setDUCChannel(ducIndex) &&
                    this->setDUCRateIndexUnlocked(ducRateIndex) &&
                    this->setTxChannel(txChannel);
            this->debug("[setDUCParameters] Returning %s\n", debugBool(success) );
            return success;
        }

        // Can be called on the fly
        bool TXClient::setTxAtten(double txAttenuation)
        {
            this->debug("[setTxAtten] Called\n");
            this->debug("[setTxAtten] -- txAttenuation = %f\n", txAttenuation);
            bool result = false;
            if (this->ducChannel != INVALID_VALUE)
            {
                result = this->rc->setTXA(this->rfChannel, txAttenuation);
                if (result == true)
                {
                    // Because TX attenuation doesn't have a well-defined behavior in
                    // the ICD -- particularly in regard to allowed resolution -- play
                    // it safe by querying what attenuation value the radio actually set.
                    this->txAttenuation = this->rc->getTXA(this->rfChannel);
                }
            }
            this->debug("[setTxAtten] Returning %s\n", debugBool(result) );
            return result;
        }

        // Can be called on the fly
        bool TXClient::setTxFreq(double txFreq)
        {
            this->debug("[setTxFreq] Called\n");
            this->debug("[setTxFreq] -- txFreq = %f\n", txFreq);
            bool result = false;
            if (this->rfChannel != INVALID_VALUE)
            {
                result = this->rc->setTXF(this->rfChannel, txFreq);
                if (result == true) {
                    this->txFreq = txFreq;
                }
            }
            this->debug("[setTxFreq] Returning %s\n", debugBool(result) );
            return result;
        }

        // Can be called on the fly
        bool TXClient::setTxInversion(bool txInversion)
        {
            if (this->ducChannel == INVALID_VALUE) return false; // Not configured yet
            bool result = this->rc->setTXINV(this->ducChannel, txInversion);
            if (result == true) {
                this->txInversion = txInversion;
            }
            return result;
        }

        bool TXClient::setEthernetInterface(unsigned int tenGbeIndex, const std::string &txInterfaceName, unsigned short port)
        {
            if (!this->isRunning) {
                this->tenGbeIndex = tenGbeIndex;
                this->txInterfaceName = std::string(txInterfaceName);
                this->txUdpPort = port;
                return true;
            }
            return false;
        }

        /********* CONTROL FUNCTIONS **********/
        void TXClient::start()
        {
            this->debug("[start] Called\n");
            if (this->isRunning)
            {
                // Stop any previous configurations
                this->stop();
            }
            std::string errors;
            if (!this->validInputs(errors))  // Don't run if something wasn't configured
            {
                std::cerr << "ERRORS CONFIGURING TX CLIENT: " << errors << std::endl;
                throw std::runtime_error(errors);
            }

            this->isRunning = true;
            this->debug("[start] Starting Transmit Client\n");

            // Prefill 50% of DUC buffer before enabling DUC
            this->prefillSampleCount = ((unsigned int )(0.50 * 67108860)) - ((unsigned int )(0.50 * 67108860)%4);

            // Create a Packetizer (wraps samples in Vita Frames and sends them)
            this->packetizer = new Packetizer(this->txInterfaceName, this->txUdpPort, this->ducRateIndex, this->debugOn);
            this->packetizer->start(); // Inits the TX socket, prepares vita headers

            // Create the status receiver for radio flow control notifications
            this->statusRX = new StatusReceiver(this->txInterfaceName, UDP_STATUS_BASE + this->ducChannel, this->debugOn, false);
            std::ostringstream statusRxName;
            statusRxName << "StatusRx" << this->txUdpPort;
            this->statusRX->setName(statusRxName.str());

            // Enable TX Channel Power (setTXP checks if it is already enabled, and that seems to avoid some timing issues)
            this->debug("[start] Enabling TX\n");
            this->rc->setTXP(
                    this->rfChannel,
                    true
            );

            // Configure DUC
            this->debug("[start] Configuring DUC\n");
            this->rc->setDUC(
                    this->ducChannel,
                    this->tenGbeIndex,
                    this->ducFreq,
                    this->ducAttenuation,
                    this->ducRateIndex,
                    this->rfChannel, // Note 3 is TX on RF1 and RF2
                    this->DUCPaused ? 2 : 0,  // Mode 2 is pause mode.  We decided to always prefill the DUC
                    this->txUdpPort // Stream ID, which is same as txUdpPort
            );
            this->debug("[start] Configuring DUC complete\n");

            // Configure DUC HS (Flow control configuration)
            this->rc->setDUCHSPercent(
                    this->ducChannel,
                    this->tenGbeIndex,
                    this->ducFullThreshPercent, // Full thresh percent
                    this->ducEmptyThreshPercent, // Empty thresh percent
                    this->updatesPerSecond, // Notifcations per second
                    this->txUdpPort
            );

            // Configure DIP for DUCHS
            this->rc->setDIP(
                    this->ducChannel,
                    this->tenGbeIndex,
                    this->getSourceIP(),
                    this->getSourceMac(),
                    this->statusRX->getUdpPort()
            );

            // Start listening for flow control from the radio.
            this->statusRX->start();
            this->debug("[start] Returning");
        }

        void TXClient::stop(bool disableRF)
        {
            if (this->isRunning)
            {
                this->debug("Stopping Transmit Client\n");
                this->statusRX->interrupt();
                this->rc->clearDUC(this->ducChannel);
                this->rc->clearDUCHS(this->ducChannel);
                this->isRunning = false;
                if (disableRF) this->disableRF();
            }

            // Delete the packetizer, which will be re-init at next call to start()
            if (this->packetizer != NULL)
            {
                delete this->packetizer;
                this->packetizer = NULL;
            }

            // Delete the status receiver, which will be re-init at next call to start()
            if (this->statusRX != NULL)
            {
                delete this->statusRX;
                this->statusRX = NULL;
            }
        }

        void TXClient::sendFrame(short * samples, unsigned int samplesPerFrame)
        {

            if (this->isRunning)
            {
                if (this->prefillSampleCount > 0)
                {
                    // Send more samples to prefill the buffer
                    this->packetizer->sendFrame(samples);
                    this->prefillSampleCount -= samplesPerFrame;
                    if ((this->prefillSampleCount <= 0))  // We have sent enough samples to prefill the buffer
                    {
                        // this->DUCPaused = false;
                        this->DUCReady = true;
                        if (!this->isGrouped)  // If we are in a group, DUCGE will be called instead
                        {
                            this->DUCPaused = false;
                            // We have sent the prefill sample amount
                            this->rc->setDUC(
                                    this->ducChannel,
                                    this->tenGbeIndex,
                                    this->ducFreq,
                                    this->ducAttenuation,
                                    this->ducRateIndex,
                                    this->rfChannel, // Note 3 is TX on RF1 and RF2
                                    this->DUCPaused ? 2 : 0,  // Mode 0 unpauses the DUC
                                    this->txUdpPort // Stream ID, which is same as txUdpPort
                            );
                        }
                    }
                }
                else // DUC is prefilled, we can use flow control
                {
                    // Wait until the radio says it can receive more frames
                    this->statusRX->blockUntilAvailable(samplesPerFrame);

                    // The radio is ready, send the frame
                    this->packetizer->sendFrame(samples);

                    // Tell the Status Receiver we have sent frames
                    this->statusRX->sentNSamples(samplesPerFrame);
                }
            }
            else
            {
                this->debug("WARNING: Called send frame without calling start()\n");
            }
        }

        bool TXClient::pauseDUC(bool paused)
        {
            this->debug("[pauseDUC] Called\n");
            this->debug("[pauseDUC] -- paused = %s\n", this->debugBool(paused));
            bool ret = false;
            boost::mutex::scoped_lock lock(this->objectAccessMutex);
            this->DUCPaused = paused;
            if (this->ducChannel != INVALID_VALUE)
            {
                ret = this->rc->setDUCP(this->ducChannel, this->DUCPaused);
            }
            return ret;
        }

        // "Unlocked" version -- This version is designed to be called from
        // setDucParameters(), which handles mutex locking, so it doesn't have
        // a lock of its own.
        bool TXClient::setDUCRateIndexUnlocked(unsigned int ducRateIndex)
        {
            // if (!this->isRunning) {
            // this->ducRateIndex = ducRateIndex;
            // return true;
            // }
            // return false;
            this->debug("[setDUCRateIndexUnlocked] Called\n");
            this->debug("[setDUCRateIndexUnlocked] -- ducRateIndex = %u\n", ducRateIndex);
            bool result = true;
            if (this->ducChannel != INVALID_VALUE)
            {
                // Send the DUC command ONLY if we've already configured this
                if ( this->ducRateIndex != INVALID_VALUE )
                {
                    this->debug("[setDUCRateIndexUnlocked] Sending radio command\n");
                    result = this->rc->setDUC(
                            /* unsigned ducChannel */ this->ducChannel,
                            /* unsigned int tenGbeIndex */ this->tenGbeIndex,
                            /* double ducFreq */ this->ducFreq,
                            /* double attenuation */ this->ducAttenuation,
                            /* unsigned int ducRateIndex */ ducRateIndex,
                            /* unsigned int rfTxChannel */ this->rfChannel,
                            /* unsigned int mode */ this->DUCPaused ? 2 : 0,
                            /* unsigned int streamID */ this->txUdpPort);
                }
                if (result == true)
                {
                    this->debug("[setDUCRateIndexUnlocked] Skipping radio command\n");
                    this->ducRateIndex = ducRateIndex;
                }
            }
            else
            {
                // Not configured yet
                this->debug("[setDUCRateIndexUnlocked] Not configured yet!\n");
            }
            this->debug("[setDUCRateIndexUnlocked] Returning %s\n", debugBool(result) );
            return result;
        }

    }
}
