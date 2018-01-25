#include <LibCyberRadio/NDR651/SyncTXClient.h>

namespace LibCyberRadio
{
	namespace NDR651
	{
		SyncTXClient::SyncTXClient(
			std::vector<TXClient *> txClients,
			bool debug
		):
			Debuggable(debug),
			txClients(txClients),
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
			this->rc = new RadioController("ndr651", 8617, debug);
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
			
			// Clear DUC Group
			this->rc->setDUCGE(ducGroup, 0);
			this->rc->clearDUCG(ducGroup);

			// Call SYNCDAC

			// Start the individual clients 
			for (int i = 0; i < this->txClients.size(); i++)
			{
				// Add client to DUC group
				this->rc->setDUCG(ducGroup, this->txClients[i]->getDucChannel(), true);

				// Start the clients
				this->txClients[i]->start();
			}
		}

		// Stops transmission to radio
		void SyncTXClient::stop()
		{
			if (this->isRunning)
			{
				for (int i = 0; i < this->txClients.size(); i++)
				{
					this->txClients[i]->stop();
				}
				this->isRunning = false;
			}
		}

		void SyncTXClient::sendFrames(short **frames, unsigned int samplesPerFrame)
		{
			// Call send frame on each client.
			for (int i = 0; i < this->txClients.size(); i++)
			{
				if (this->txClients[i]->isDUCPaused())
				{
					this->txClients[i]->sendFrame(frames[i], samplesPerFrame);
					if (!this->txClients[i]->isDUCPaused())
					{
						this->rc->setDUCGE(ducGroup, true);
					}
				}
				else 
				{
					this->txClients[i]->sendFrame(frames[i], samplesPerFrame);
				}
			}
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
