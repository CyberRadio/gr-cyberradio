#include <LibCyberRadio/NDR651/SyncTXClient.h>

namespace LibCyberRadio
{
    namespace NDR651
    {
        SyncTXClient::SyncTXClient(
                std::vector<TXClient *> txClients,
                std::string hostname, 
                bool debug
        ):
            Debuggable(debug, "SyncTXClient"),
            txClients(txClients),
            hostname(hostname),
            ducGroup(1),
            rc(NULL),
            isRunning(false)
        {
            // Put the TXClient objects in grouped mode
            for (int i = 0; i < this->txClients.size(); i++)
            {
                this->txClients[i]->setGrouped(true);
            }
            // Create a radio controller (sends cmds to 651)
            this->rc = new RadioController(this->hostname, 8617, debug);
        }

        SyncTXClient::~SyncTXClient()
        {
            if (this->rc != NULL)
            {
                delete this->rc;
            }

            // Iterate of client list and delete all TXClient objects
            for (int i = 0; i < this->txClients.size(); i++)
            {
                delete this->txClients[i];
            }
            this->txClients.clear();
        }

        // Starts transmission to radio
        void SyncTXClient::start()
        {
            if (this->isRunning)
            {
                // Stop any previous clients
                this->stop();
            }
            this->isRunning = true;

            // Set up DUC group to cover the DUCs managed by the
            // member TXClient objects
            this->debug("[start] Setting up DUC Group %d\n", ducGroup);
            // -- Clear all DUC group members
            this->rc->clearDUCG(ducGroup);
            // -- Add DUCs from TXClients to DUC group
            for (int i = 0; i < this->txClients.size(); i++)
            {
//                this->debug("[start] Adding DUC %d to DUC Group %d\n",
//                            this->txClients[i]->getDucChannel(),
//                            ducGroup);
                this->rc->setDUCG(ducGroup, this->txClients[i]->getDucChannel(), true);
            }

            // Disable the DUC group for now.  We will enable it later when
            // the managed TXClients pre-fill the DUC buffers enough.
            this->debug("[start] Disabling DUC Group %d\n", ducGroup);
            this->rc->setDUCGE(ducGroup, false);

            // Start the individual clients
            for (int i = 0; i < this->txClients.size(); i++)
            {
                this->debug("[start] Starting TX Client for DUC %d\n",
                            this->txClients[i]->getDucChannel(),
                            ducGroup);
                // Start the clients
                this->txClients[i]->start();
            }
            this->waitingToEnableDUCGE = true;
        }

        // Stops transmission to radio
        void SyncTXClient::stop()
        {
            if (this->isRunning)
            {
                this->rc->setDUCGE(ducGroup, false);
                for (int i = 0; i < this->txClients.size(); i++)
                {
                    this->txClients[i]->stop();
                }
                this->isRunning = false;
            }
        }

        bool SyncTXClient::areAllDucsPaused(void) {
            bool allDucsInPause = true;
            for (int i = 0; i < this->txClients.size(); i++)
            {
                allDucsInPause &= this->txClients[i]->isDUCPaused();
            }
            return allDucsInPause;
        }

        bool SyncTXClient::checkClientStatus(void) {
            bool ducsStarted = false;
            bool anyDucsInPause = false;
            bool anyDucsReady = false;
            bool allDucsReady = true;
            for (int i = 0; i < this->txClients.size(); i++)
            {
                anyDucsInPause |= this->txClients[i]->isDUCPaused();
                anyDucsReady |= !(this->txClients[i]->isDUCReady());
                allDucsReady &= !(this->txClients[i]->isDUCReady());
            }
            // -- Proceed only if we had DUCs "in pause" waiting for pre-filling
            if ( anyDucsInPause && allDucsReady )
            {
                this->debug("[sendFrames] DUCs are ready, enabling DUC Group %d", ducGroup);
                this->rc->setDUCGE(ducGroup, true);
                for (int i = 0; i < this->txClients.size(); i++)
                {
                    this->txClients[i]->setDUCPaused(false);
                }
                ducsStarted = true;
            }
            return ducsStarted;
        }

        bool SyncTXClient::sendFrameToClient(short *frame, unsigned int samplesPerFrame, int client) {
            bool rv = false;
            if (client < this->txClients.size()) {
                this->txClients[client]->sendFrame(frame, samplesPerFrame);
                rv = true;
            }
            return rv;
        }

        void SyncTXClient::sendFrames(short **frames, unsigned int samplesPerFrame)
        {
            // When this method is called, the managed DUCs may be in the
            // "paused" state, waiting to be pre-filled with data before we
            // enable the DUC group.
            
            // -- First, check to see if any DUCs are in the "paused" state,
            //    waiting for pre-filling.
            bool anyDucsInPause = false;
            for (int i = 0; i < this->txClients.size(); i++)
            {
                anyDucsInPause |= this->txClients[i]->isDUCPaused();
            }
            
            // -- Call send frame on each client.  This will either pre-fill
            //    the buffer if paused, or send the data if not.
            for (int i = 0; i < this->txClients.size(); i++)
            {
                this->txClients[i]->sendFrame(frames[i], samplesPerFrame);
            }
            
            // -- Proceed only if we had DUCs "in pause" waiting for pre-filling
            if (anyDucsInPause) {
                // this->debug("[sendFrames] DUCs are paused, Checking to see if we should enable the DUC Group %d", ducGroup);
                bool anyDucsReady = false;
                for (int i = 0; i < this->txClients.size(); i++)
                {
                    anyDucsReady |= this->txClients[i]->isDUCReady();
                }
                if (anyDucsReady) {
                    // this->debug("[sendFrames] DUCs are ready, enabling DUC Group %d", ducGroup);
                    this->rc->setDUCGE(ducGroup, true);
                    for (int i = 0; i < this->txClients.size(); i++)
                    {
                        this->txClients[i]->setDUCPaused(false);
                    }
                }
            }
            // if ( anyDucsInPause )
            // {
            //     // -- Check to see if any DUCs are pre-filled and ready to go.
            //     bool anyDucsReady = false;
            //     for (int i = 0; i < this->txClients.size(); i++)
            //     {
            //         anyDucsReady |= !(this->txClients[i]->isDUCPaused());
            //     }
            //     // If any DUCs are ready, then enable the DUC group.
            //     if (anyDucsReady)
            //     {
            //         this->debug("[sendFrames] DUCs are ready, enabling DUC Group %d", ducGroup);
            //         this->rc->setDUCGE(ducGroup, true);
            //     }
            // }
        }

        void SyncTXClient::setDucGroup(int ducGroup)
        {
            if (ducGroup >= 1 && ducGroup <= 4) {
                this->ducGroup = ducGroup;
            }
        }

        int SyncTXClient::getDucGroup()
        {
            return(this->ducGroup);
        }

    }
}
