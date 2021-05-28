/***************************************************************************
 * \file TransmitPacketizer.cpp
 *
 * \brief NDR651 transmit packetizer class.
 *
 * \author NH
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#include "LibCyberRadio/NDR651/TransmitPacketizer.h"
#include <boost/algorithm/string.hpp>
#include <boost/tokenizer.hpp>
#include <unistd.h>

#define BOOL_DEBUG(x) (x ? "true" : "false")

using namespace boost::algorithm;


static unsigned short compute_checksum(unsigned short *addr, unsigned int count) {
    register unsigned long sum = 0;
    while (count > 1) {
        //std::cout << count << "  |  " << *addr << "  |  " << sum << std::endl;
        sum += * addr++;
        count -= 2;
    }
    //if any bytes left, pad the bytes and add
    if(count > 0) {
        sum += ((*addr)&htons(0xFF00));
    }
    //Fold sum to 16 bits: add carrier to result
    while (sum>>16) {
        sum = (sum & 0xffff) + (sum >> 16);
    }
    //one's complement
    sum = ~sum;
    return ((unsigned short)sum);
}

bool setCpuAffinity(int cpu) {
    cpu_set_t set;
    CPU_ZERO(&set);
    CPU_SET(cpu, &set);
    if (sched_setaffinity(0, sizeof(set), &set)) {
        return false;
    } else {
        return true;
    }
}

namespace LibCyberRadio
{
    namespace NDR651
    {

        TransmitPacketizer::TransmitPacketizer(
                const std::string& radioHostName,
                int radioTcpPort,
                unsigned int ducChannel,
                const std::string& ifname,
                unsigned int tenGigIndex,
                int dipIndex,
                unsigned int ducRate,
                unsigned int ducTxChannels,
                float ducFreq,
                float ducAtten,
                double txFreq,
                float txAtten,
                unsigned int streamId,
                bool config_tx,
                bool debug):
            Debuggable(debug, "TransmitPacketizer"),
            _radioHostName(""),
            _radioTcpPort(0),
            _ducChannel(0),
            _ifname(""),
            _tenGigIndex(0),
            _dipIndex(-1),
            _ducRate(0),
            _ducTxChannels(0),
            _ducFreq(0),
            _ducAtten(0),
            _txFreq(0),
            _txAtten(0),
            _streamId(streamId),
            _config_tx(config_tx),
            _txSock(NULL),
            _numSock(8),
            _fcClient(NULL),
            _frameStart((unsigned char*)(&_frame)),
            _frameLength(sizeof(TxFrame)),
            _samplesSent(0),
            _sMac(""),
            _dMac(""),
            _sIp(""),
            _dIp(""),
            _sPort(0),
            _dPort(0),
            _updatePE(false),
            _duchsPfThresh(61*(67108862/64)),
            _duchsPeThresh(58*(67108862/64)),
            _duchsPeriod(10),
            _samplesPerFrame(SAMPLES_PER_FRAME),
            //_waiting(false),
            _firstFrame(true),
            _running(false),
            _constructing(true),
            _frameCount(0),
            _pauseCount(64)
        {
            this->debug("construction\n");
            std::cout << "using local lib" << std::endl;
            memset(&_frame, 0, sizeof(TxFrame));
            _fcClient = new FlowControlClient(ducChannel, _config_tx, 4, _debug);
            _statusRx = new UdpStatusReceiver(ifname, 65500+ducChannel, _debug, _updatePE);

            setRadioParameters(radioHostName, radioTcpPort);
            setDucInterface(ifname, tenGigIndex);
            setDucParameters(tenGigIndex, ducRate, ducTxChannels,
                    ducFreq, ducAtten, txFreq, txAtten,
                    streamId);
            _constructing = false;
            _delayTime.tv_sec = 0;
            _delayTime.tv_nsec = 100;

        }

        TransmitPacketizer::~TransmitPacketizer()
        {
            // TODO Auto-generated destructor stub

            this->debug("destruction\n");
            if ( _fcClient != NULL )
                delete _fcClient;
            if ( _txSock != NULL )
                delete _txSock;
        }

        bool TransmitPacketizer::setRadioHostName(const std::string& radioHostName)
        {
            return setRadioParameters(radioHostName, _radioTcpPort);
        }

        bool TransmitPacketizer::setRadioTcpPort(int radioTcpPort)
        {
            return setRadioParameters(_radioHostName, radioTcpPort);
        }

        bool TransmitPacketizer::setDucChannel(unsigned int ducChannel)
        {
            _configuring = true;
            this->debug("setting duc channel = %d\n", ducChannel);
            // Sanity check -- there is not much we can do if we
            // failed to make our control objects!
            if ( (_txSock != NULL) && (_fcClient != NULL) )
            {
                // Disable the DUC this object was talking to
                _fcClient->disableDuc();
                // Switch DUCs
                _fcClient->setDucChannel(ducChannel);
                this->debug("duc channel set ok\n");
            }
            else
            {
                this->debug("duc channel set skipped\n");
            }
            _configuring = false;
            return true;
        }

        bool TransmitPacketizer::setDucInterface(const std::string& ifname,
                unsigned int tenGigIndex)
        {
            _configuring = true;
            this->debug("setting duc interface = %s/%d\n", ifname.c_str(),
                    tenGigIndex);
            // Create a new TransmitSocket object if the user wants to
            // use a different interface.
            if ( ifname != _ifname )
            {
                if ( _txSock != NULL ) {
                    delete _txSock;
                    _txSockVec.clear();
                }
                _ifname = ifname;
                //~ _txSock = new TransmitSocket(_ifname, _streamId);
                for (int i=0; i<_numSock; i++) {
                    _txSockVec.push_back(new TransmitSocket(_ifname, _streamId));
                }
                std::cout << "# sockets = " << _txSockVec.size() << std::endl;
                _currentSockIndex = 0;
                _txSock = _txSockVec[_currentSockIndex];
            }
            _tenGigIndex = tenGigIndex;
            this->debug("duc interface set ok\n");
            return setDucParameters(tenGigIndex, _ducRate, _ducTxChannels,
                    _ducFreq, _ducAtten, _txFreq,
                    _txAtten, _streamId);
        }

        bool TransmitPacketizer::setDucRate(unsigned int ducRate)
        {
            bool ret = true;
            _configuring = true;
            _ducRate = ducRate;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucRateIndex(_ducRate, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setDucTxChannels(unsigned int ducTxChannels)
        {
            bool ret = true;
            _configuring = true;
            _ducTxChannels = ducTxChannels;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucTxChannel(_ducTxChannels, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setDucFreq(float ducFreq)
        {
            bool ret = true;
            _configuring = true;
            _ducFreq = ducFreq;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucFrequency((long)_ducFreq, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setDucTxinvMode(unsigned int txinvMode)
        {
            bool ret = true;
            _configuring = true;
            _txinvMode = txinvMode;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucTxinvMode(txinvMode, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setDucAtten(float ducAtten)
        {
            bool ret = true;
            _configuring = true;
            _ducAtten = ducAtten;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucAttenuation(_ducAtten, true);
            }
            _configuring = false;
            return ret;
        }


        void TransmitPacketizer::setDuchsParameters(unsigned int duchsPfThresh, unsigned int duchsPeThresh, unsigned int duchsPeriod, bool updatePE) {
            bool change = false;
            if (_updatePE != updatePE) {
                _updatePE = updatePE;
                if (updatePE) {
                    std::cerr << "setDuchsParameters: Updating on PE packet" << std::endl;
                } else {
                    std::cerr << "setDuchsParameters: Updating on periodic packet" << std::endl;
                }
                _statusRx->setUpdatePE(_updatePE);
            }
            if (_duchsPfThresh != duchsPfThresh) {
                std::cerr << "setDuchsParameters: Modify duchsPfThresh " << _duchsPfThresh << "->" << duchsPfThresh << std::endl;
                _duchsPfThresh = duchsPfThresh;
                change = true;
            }
            if (_duchsPeThresh != duchsPeThresh) {
                std::cerr << "setDuchsParameters: Modify duchsPeThresh " << _duchsPeThresh << "->" << duchsPeThresh << std::endl;
                _duchsPeThresh = duchsPeThresh;
                change = true;
            }
            if (_duchsPeriod != duchsPeriod) {
                std::cerr << "setDuchsParameters: Modify duchsPeriod " << _duchsPeriod << "->" << duchsPeriod << std::endl;
                _duchsPeriod = duchsPeriod;
                change = true;
            }
            if (change && _running) {
                _fcClient->setDuchsParameters(_duchsPfThresh, _duchsPeThresh, _duchsPeriod);
            }
        }

        bool TransmitPacketizer::setTxFreq(double txFreq)
        {
            bool ret = true;
            bool shfChange = (_txFreq != txFreq) && (((_txFreq >= 200.0)&&(txFreq < 200.0))||((_txFreq < 200.0)&&(txFreq >= 200.0)));
            _configuring = true;
            _txFreq = txFreq;
            if (_fcClient != NULL)
            {
                //~ if (shfChange) {
                //~ ret = _fcClient->enableDuc(_ducRate, _ducTxChannels,
                //~ _streamId, _tenGigIndex,
                //~ _ducAtten, _txFreq,
                //~ (long)_ducFreq,
                //~ (unsigned int)_txAtten);
                //~ } else {
                ret = _fcClient->setTxFrequency(_txFreq, true); // Allow double input
                //~ }
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setTxAtten(float txAtten)
        {
            bool ret = true;
            _configuring = true;
            _txAtten = txAtten;
            if (_fcClient != NULL)
            {
                ret = _fcClient->setTxAttenuation((int)_txAtten, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setStreamId(unsigned int streamId)
        {
            bool ret = true;
            _configuring = true;
            _streamId = streamId;
            setUdpHeader(_streamId, _streamId);
            setVitaHeader(_streamId);
            if (_fcClient != NULL)
            {
                ret = _fcClient->setDucStreamId(_streamId, true);
            }
            _configuring = false;
            return ret;
        }

        bool TransmitPacketizer::setDebug(bool debug)
        {
            _debug = debug;
            return true;
        }

        bool TransmitPacketizer::setRadioParameters(
                const std::string& radioHostName,
                int radioTcpPort)
        {
            _configuring = true;
            this->debug("setting radio parameters  host=%s, port=%d\n",
                    radioHostName.c_str(), radioTcpPort);
            // Sanity check -- there is not much we can do if we
            // failed to make our control objects!
            if ( _fcClient != NULL )
            {
                // If we are not in the middle of constructing, then
                // we need to deal with the case where the user is
                // trying to connect to a different radio and/or TCP
                // port on the fly.
                if ( !_constructing )
                {
                    // If changing radio hosts, disable the DUC we are
                    // controlling first.
                    if ( radioHostName != _radioHostName )
                    {
                        _fcClient->disableDuc();
                    }
                    // If changing radio host or TCP port, disconnect
                    // first.
                    if ( (radioHostName != _radioHostName) ||
                            (radioTcpPort != _radioTcpPort) )
                    {
                        _fcClient->disconnect();
                    }
                }
                // Set the new host name and TCP port
                _radioHostName = radioHostName;
                _radioTcpPort = radioTcpPort;
                // Connect to the radio if a hostname was given
                if ( _radioHostName != "" )
                    _fcClient->connectToRadio(_radioHostName, _radioTcpPort);
                this->debug("radio parameters set result = %s\n",
                        BOOL_DEBUG(_fcClient->isConnected()));
            }
            else
            {
                this->debug("radio parameters set skipped\n");
            }
            _configuring = false;
            return true;
        }

        bool TransmitPacketizer::setDucParameters(unsigned int tenGigIndex,
                unsigned int ducRate,
                unsigned int ducTxChannels,
                float ducFreq,
                float ducAtten,
                double txFreq,
                float txAtten,
                unsigned int streamId)
        {
            _configuring = true;
            bool ret = true;
            this->debug("setting duc parameters  index=%d\n", tenGigIndex);
            _tenGigIndex = tenGigIndex;
            _ducRate = ducRate;
            _ducTxChannels = ducTxChannels;
            _ducFreq = ducFreq;
            _ducAtten = ducAtten;
            _txFreq = txFreq;
            _txAtten = txAtten;
            _streamId = streamId;
            this->debug("-- ducRate=%u ducTxChannels=%d ducFreq=%f "
                    "ducAtten=%f txFreq=%f txAtten=%f streamId=%u\n",
                    _ducRate, _ducTxChannels, _ducFreq, _ducAtten,
                    _txFreq, _txAtten, _streamId);
            // Sanity check -- there is not much we can do if we
            // failed to make our control objects!
            if ( (_txSock != NULL) && (_fcClient != NULL) )
            {
                _sMac = _txSock->getMacAddress();
                _sIp = _txSock->getIpAddress();
                if (_txSock->isUsingRawSocket()) {
                    this->debug("-- source mac = %s\n", _sMac.c_str());
                    _dMac = _fcClient->getRadioMac(tenGigIndex);
                    this->debug("-- dest mac = %s\n", _dMac.c_str());
                    setEthernetHeader(_sMac, _dMac);
                    this->debug("-- source ip = %s\n", _sIp.c_str());
                    _dIp = _fcClient->getRadioIp(tenGigIndex);
                    this->debug("-- dest ip = %s\n", _dIp.c_str());
                    setIpHeader(_sIp, _dIp);
                    setUdpHeader(_streamId, _streamId);
                } else {
                    _frameStart = (unsigned char*)(&_frame.v49.frameStart);
                    _frameLength = sizeof(TxFrame)-( sizeof(ethhdr) + sizeof(iphdr) + sizeof(udphdr) );
                }
                setVitaHeader(_streamId);
                this->debug("-- enabling duc\n");
                ret = _fcClient->enableDuc(_ducRate, _ducTxChannels,
                        _streamId, _tenGigIndex,
                        _ducAtten, _txFreq,
                        (long)_ducFreq,
                        (unsigned int)_txAtten);
                this->debug("-- duc enable = %s\n", BOOL_DEBUG(ret));
            }
            else
            {
                this->debug("duc parameters set skipped\n");
            }
            this->debug("duc parameters set result = %s\n", BOOL_DEBUG(ret));
            _configuring = false;
            return ret;
        }

        void TransmitPacketizer::start()
        {
            _running = true;
            //~ if ( _fcClient != NULL )
            //~ _fcClient->start();
            _fcClient->setDucDipStatusEntry(-1, _sIp, _sMac, _statusRx->getUdpPort());
            _statusRx->setUpdatePE(_updatePE);
            _fcClient->setDuchsParameters(_duchsPfThresh, _duchsPeThresh, _duchsPeriod);
            if ( _statusRx != NULL )
                _statusRx->start();
        }

        void TransmitPacketizer::stop()
        {
            std::cerr << "Stopping flow control threads.\n";
            this->setDuchsParameters(0, 0, 0, false);
            if ( _fcClient != NULL ) {
                //~ _fcClient->interrupt();
                _fcClient->setDucTenGbePort(0, false);
                _fcClient->setDucRateIndex(0, false);
                _fcClient->setDucFrequency(0, false);
                _fcClient->setDucStreamId(0, false);
                _fcClient->setDucEnable(false, true);
                delete _fcClient;
                _fcClient = NULL;
            }
            if ( _statusRx != NULL ){
                std::cerr << "_statusRx->interrupt()\n";
                _statusRx->interrupt();
                std::cerr << "delete _statusRx\n";
                delete _statusRx;
                _statusRx = NULL;
            }
            std::cerr << "Stopped flow control threads.\n";
        }

        unsigned int TransmitPacketizer::sendFrame(short * samples)
        {
            _samplesSent = 0;
            // Sanity check -- there is not much we can do if we
            // failed to make our control objects!
            if ( (_txSock != NULL) && (_fcClient != NULL) && (_statusRx != NULL) )
            {
                while (!_statusRx->okToSend(SAMPLES_PER_FRAME,false))
                {
                    usleep(1000);
                }
                memcpy(&_frame.payload.samples, samples, 4*SAMPLES_PER_FRAME);
                if (_txSock->sendFrame(_frameStart, _frameLength))
                {
                    _samplesSent = SAMPLES_PER_FRAME;
                    _incrementVitaHeader();
                    if (_firstFrame) {
                        this->debug("1st frame sent!\n");
                        _firstFrame = false;
                    }

                }
                _currentSockIndex = (_currentSockIndex+1)%_txSockVec.size();
                _txSock = _txSockVec[_currentSockIndex];
                _statusRx->sentNSamples(_samplesSent);
                //~ _frameCount += 1;
                //~ if (_frameCount==_pauseCount) {
                //~ std::cout << "UNPAUSING\n";
                //~ _fcClient->unpause();
                //~ }
                //~ usleep(1);
            }
            return _samplesSent;
        }

        bool TransmitPacketizer::isConnected(void)
        {
            return ( (_fcClient != NULL) &&
                    _fcClient->isConnected() );
        }

        bool TransmitPacketizer::isReadyToReceive(void)
        {
            return ( !_configuring && isConnected() );
        }

        bool TransmitPacketizer::setEthernetHeader(const std::string& sourceMac,
                const std::string& destMac)
        {
            std::vector<std::string> macVec;
            int ind = 0;

            //Destination MAC address
            split(macVec, destMac, is_any_of(":"));
            //std::cout << "header dMAC = ";
            ind = 0;
            for (std::vector<std::string>::iterator i=macVec.begin(); i!=macVec.end(); i++) {
                unsigned char val = strtol((*i).c_str(), NULL, 16);
                //std::cout << "  " << (*i) << " (" << (int)val << ")";
                _frame.eth.h_dest[ind++] = val;
            }
            //std::cout << std::endl;

            //Source MAC address
            split(macVec, sourceMac, is_any_of(":"));
            //std::cout << "header sMAC = ";
            ind = 0;
            for (std::vector<std::string>::iterator i=macVec.begin(); i!=macVec.end(); i++) {
                unsigned char val = strtol((*i).c_str(), NULL, 16);
                //std::cout << "  " << (*i) << " (" << (int)val << ")";
                _frame.eth.h_source[ind++] = val;
            }
            //std::cout << std::endl;

            _frame.eth.h_proto = htons(ETH_P_IP);

            return true;
        }

        bool TransmitPacketizer::setIpHeader(const std::string& sourceIp,
                const std::string& destIp)
        {
            _frame.ip.version = 4;
            _frame.ip.ihl = sizeof(iphdr)/4;
            //_frame.ip.frag_off = htons(0x4000);
            _frame.ip.protocol = 17;
            _frame.ip.tot_len = htons(sizeof(TxFrame)-sizeof(ethhdr));
            _frame.ip.ttl = 255;

            // Destination IP address
            inet_pton(AF_INET, destIp.c_str(), &(_frame.ip.daddr));

            // Source IP address
            inet_pton(AF_INET, sourceIp.c_str(), &(_frame.ip.saddr));

            // IP Header checksum
            _frame.ip.check = 0;
            _frame.ip.check = compute_checksum((unsigned short*)&(_frame.ip), _frame.ip.ihl<<2);

            return true;
        }

        bool TransmitPacketizer::setUdpHeader(unsigned short sourcePort,
                unsigned short destPort)
        {
            _frame.udp.source = htons(sourcePort);
            _frame.udp.dest = htons(destPort);
            _frame.udp.len = htons(sizeof(TxFrame)-sizeof(ethhdr)-sizeof(iphdr));
            return true;
        }

        bool TransmitPacketizer::setVitaHeader(unsigned int streamId)
        {
            //Vita49
            _frame.v49.frameStart = VRLP;
            //~ _frame.v49.frameSize = SAMPLES_PER_FRAME+10;
            _frame.v49.frameSize = _samplesPerFrame+10;
            _frame.v49.streamId = streamId;
            _frame.v49.packetType = 0x1;
            _frame.v49.TSF = 0x1;
            _frame.v49.TSF = 0x1;
            _frame.v49.T = 0;
            _frame.v49.C = 1;
            _frame.v49.classId1 = 0x00fffffa;
            _frame.v49.classId2 = 0x00130000;
            //~ _frame.v49.packetSize = SAMPLES_PER_FRAME+7;
            _frame.v49.packetSize = _samplesPerFrame+7;
            _frame.vend.frameEnd = VEND;
            return true;
        }

        //~ unsigned int TransmitPacketizer::setSamplesPerFrame(unsigned int samplesPerFrame) {
        //~ _samplesPerFrame = samplesPerFrame;
        //~ _frame.v49.packetSize = _samplesPerFrame+7;
        //~ _frame.v49.frameSize = _samplesPerFrame+10;
        //~ }

        void TransmitPacketizer::_incrementVitaHeader()
        {
            //if (_debug && (_frame.v49.frameCount==0)) {
            //std::cout << "Frame 0 " << std::endl;
            //}
            _frame.v49.frameCount = (_frame.v49.frameCount + 1) % 4096;
            _frame.v49.packetCount = (_frame.v49.packetCount + 1) % 16;
        }

    } /* namespace NDR651 */
}
