////============================================================================
//// Name        : ndr651_tx_test.cpp
//// Author      : NH
//// Version     :
//// Copyright   : Copyright (c) 2015-2021 CyberRadio Solutions, Inc.  All rights reserved.
//// Description : Hello World in C++, Ansi-style
////============================================================================

#include <signal.h>
#include <iostream>
#include <math.h>

#include <arpa/inet.h>
#include <ifaddrs.h>
#include <string.h>


#include "LibCyberRadio/NDR651/TransmitPacketizer.h"

static int keep_looping = true;
void intHandler(int dummy) {
    keep_looping = false;
    printf("SIGINT CAUGHT!\n");
}

int main(int argc, char **argv) {
    signal(SIGINT, intHandler);

    const std::string& radioHostName = "ndr651"; // hostname or IP address for radio
    int radioTcpPort = 8617; // default value
    unsigned int ducChannel = 1;
    const std::string& ifname = "eth7"; // local 10GbE interface name
    unsigned int tenGigIndex = 2; // radio 10GbE interface index, 1 or 2
    int dipIndex = -1;
    unsigned int ducRate = 1; // DUC Rate Index
    unsigned int ducTxChannels = 3; // DUC Tx Channel bit map (1=1, 2=2, 3=1&2)
    float ducFreq = 1e5; // DUC frequency offset
    float ducAtten = 0; // DUC attenuation
    float txFreq = 1000; // RF Frequency
    float txAtten = 0; // RF Attenuation
    unsigned int streamId = 0xcafe; // stream ID
    bool configTx = true; // flag to allow for Tx configuration - if false, RF settings will not be applied.
    bool debug = true; // Mainly to print out configuration messages
    bool usePE = false;
    unsigned int txinvMode = 0;

    for (int i=1; i<argc; i++) {
        std::cout << "arg #" << i << " = " << argv[i];
        switch (i) {
            case 1:
                ducRate = (unsigned int) atoi(argv[i]);
                std::cout << " -> ducRate";
                break;
            case 2:
                usePE = (bool)atoi(argv[i]);
                std::cout << " -> usePE";
                break;
            case 3:
                ducChannel = (unsigned int) atoi(argv[i]);
                std::cout << " -> ducChannel";
                break;
            case 4:
                ducTxChannels = (unsigned int) atoi(argv[i]);
                std::cout << " -> ducTxChannels";
                break;
            case 5:
                txFreq = atof(argv[i]);
                std::cout << " -> txFreq";
                break;
            case 6:
                txinvMode = atoi(argv[i]);
                std::cout << " -> txinvMode";
                break;
            default:
                break;
        }
        std::cout << std::endl;
    }
    //~ streamId = streamId+ducChannel-1;

    // Pre-compute a set of samples for transmission - a sinusoid that spans a number of frames
    const int period = 127;
    int row;
    short sampleBuffer[period][2*SAMPLES_PER_FRAME] = {{0}};
    {
        double amplitude = 0x7fff;
        double t, re, im;
        int ind = 0;
        for (row=0; row<period; row++) {
            for (int samp=0; samp<SAMPLES_PER_FRAME; samp++) {
                ind = (row*SAMPLES_PER_FRAME) + samp;
                t = ((double)ind)/SAMPLES_PER_FRAME;
                re = cos( 2*M_PI*t/period );
                im = sin( 2*M_PI*t/period );
                sampleBuffer[row][2*samp] = (short)(re*amplitude);
                sampleBuffer[row][(2*samp)+1] = (short)(im*amplitude);
            }
        }
    }


    // Create TransmitPacketizer object w/ relevant parameters.
    LibCyberRadio::NDR651::TransmitPacketizer * tx = new LibCyberRadio::NDR651::TransmitPacketizer(radioHostName,
            radioTcpPort,
            ducChannel,
            ifname,
            tenGigIndex,
            dipIndex,
            ducRate,
            ducTxChannels,
            ducFreq,
            ducAtten,
            txFreq,
            txAtten,
            streamId,
            configTx,
            debug);

    // Transmit loop.
    row = 0;
    //~ if (usePE) {
    //~ tx->setDuchsParameters(25, 24, 50, true);
    //~ } else {
    //~ tx->setDuchsParameters(0, 0, 10, false);
    //~ }
    //~ tx->setDucTxinvMode(txinvMode);
    tx->start(); // start flow control thread
    std::cout << "Started transmitter!" << std::endl;
    while (keep_looping && tx->isReadyToReceive()) {
        while (keep_looping && (tx->sendFrame(sampleBuffer[row])>0)) {
            // if the # of samples sent is greater than 0, move to the next row
            row = (row+1)%period;
        }
        // If no samples have been sent, then the DUC's buffer is full
        // Let's wait a while...
        usleep(1e4);
    }
    std::cout << "tx->stop();..." << std::endl;
    //~ tx->setDuchsParameters(0, 0, 0, false);
    tx->stop();
    std::cout << "stopped." << std::endl;
    return 0;
}
