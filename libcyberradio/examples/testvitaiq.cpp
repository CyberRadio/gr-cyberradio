/*
 ============================================================================
 Name        : testvitaiq.cpp
 Author      : CyberRadio Solutions
 Version     :
 Copyright   : (c) 2016 CyberRadio Solutions, Inc.  All rights reserved.
 Description : Uses shared library to print greeting
               To run the resulting executable the LD_LIBRARY_PATH must be
               set to ${project_loc}/libcyberradio/.libs
               Alternatively, libtool creates a wrapper shell script in the
               build directory of this program which can be used to run it.
               Here the script will be called testvitaiq.
 ============================================================================
 */

#include "LibCyberRadio/Common/VitaIqSource.h"
#include "LibCyberRadio/Common/Vita49Packet.h"
#include <vector>
#include <complex>
#include <iostream>


int main(void)
{
    /* Set up a VITA-I/Q source for an NDR304 radio */
    LibCyberRadio::VitaIqSource wbddc1(
            /* const std::string& name */ "NDR304 WBDDC 1",
            /* int vita_type */ 1,
            /* size_t payload_size */ 1536,
            /* size_t vita_header_size */ 28,
            /* size_t vita_tail_size */ 4,
            /* bool byte_swapped */ false,
            /* bool iq_swapped */ true,
            /* const std::string& host */ "0.0.0.0",
            /* unsigned short port */ 41000,
            /* bool debug */ true);
    /* Delay for looping over data coming from the radio */
    struct timespec ts_delay = {0, 100};
    /* VITA packet vector */
    LibCyberRadio::Vita49PacketVector vitaPackets;
    /* Packets retrieved on loop */
    int packetsReceived = 0;

    /* Loop over packets */
    do
    {
        packetsReceived = wbddc1.getPackets(
                /* int noutput_items */ 10,
                /* std::vector<Vita49Packet> */ vitaPackets);
        std::cout << "packetsReceived = " << packetsReceived
                << "  len(vitaPackets) = " << vitaPackets.size()
                << std::endl;
        for (LibCyberRadio::Vita49PacketVector::iterator it = vitaPackets.begin();
                it != vitaPackets.end(); it++)
            std::cout << it->dump() << std::endl;
        vitaPackets.clear();
        nanosleep(&ts_delay, NULL);
    } while (true);

    return 0;
}
