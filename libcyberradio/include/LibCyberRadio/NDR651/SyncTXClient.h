/*
 *    SyncTXClient.cpp
 *    Author: Joseph Martin
 */
#ifndef INCLUDED_LIBCYBERRADIO_NDR651_SYNCTXCLIENT_H_
#define INCLUDED_LIBCYBERRADIO_NDR651_SYNCTXCLIENT_H_

#include <LibCyberRadio/Common/Debuggable.h>
#include <LibCyberRadio/NDR651/TXClient.h>
#include <LibCyberRadio/Common/Debuggable.h>
#include <LibCyberRadio/NDR651/FlowControlClient.h>
#include <LibCyberRadio/NDR651/PacketTypes.h>
#include <LibCyberRadio/NDR651/UdpStatusReceiver.h>
#include <LibCyberRadio/NDR651/StatusReceiver.h>
#include <LibCyberRadio/NDR651/RadioController.h>
#include <LibCyberRadio/NDR651/Packetizer.h>
#include <vector>

namespace LibCyberRadio
{
    namespace NDR651
    {
        class SyncTXClient : public Debuggable
        {

            public:
                SyncTXClient(std::vector<TXClient *> txClients, std::string hostname="ndr651", bool debug = false);
                ~SyncTXClient();

                void start();
                void stop();
                void sendFrames(short **frames, unsigned int samplesPerFrame);
                void setDucGroup(int ducGroup);
                int getDucGroup();

                bool sendFrameToClient(short *frame, unsigned int samplesPerFrame, int client);
                bool checkClientStatus(void);
                bool areAllDucsPaused(void);

            private:
                std::vector<TXClient *> txClients;
                std::string hostname;
                RadioController *rc;
                bool isRunning;
                int ducGroup;
                bool waitingToEnableDUCGE;
        };
    }
}


#endif
