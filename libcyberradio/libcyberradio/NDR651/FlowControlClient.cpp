/***************************************************************************
 * \file FlowControlClient.cpp
 *
 * \brief NDR651 flow control client.
 *
 * \author NH
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#include "LibCyberRadio/NDR651/FlowControlClient.h"
#include "boost/format.hpp"
#include <boost/algorithm/string.hpp>
#include <math.h>
#include <stdlib.h>
#include <stdarg.h>

#define BOOL_DEBUG(x) (x ? "true" : "false")

using namespace boost::algorithm;


namespace LibCyberRadio
{
    namespace NDR651
    {
        FlowControlClient::FlowControlClient(unsigned int ducChannel,
                bool config_tx,
                unsigned int updatesPerSecond,
                bool debug) :
            Thread("FlowControlClient", "FlowControlClient"),
            Debuggable(debug, "FlowControlClient"),
            _config_tx(config_tx),
            _ducEnable(false),
            _ducChannel(0),
            _ducRateIndex(0),
            _ducStreamId(0),
            _ducTxChannel(0),
            _ducTenGbePort(0),
            _ducAttenuation(0),
            _txAttenuation(0),
            _txFreq(0.0),
            _shfMode(-1),
            _ducFreq(0),
            _statusSockfd(-1)
        {
            this->debug("construction\n");
            _firstUpdate = true;
            _tbsQuery = std::string("\n");
            _651freeSpace = 0;
            _multiChannel = false;
            _mySocket = NULL;
            _initStatusFrame();
            _statusSockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
            _initStatusAddress();
            setDucChannel( ducChannel );
            setUpdateRate( updatesPerSecond );
            //~ _clearDucSettingsInRadio();
        }

        FlowControlClient::~FlowControlClient() {
            this->debug("destruction\n");
            if (_mySocket->isConnected()) {
                _mySocket->disconnect();
            }
            if (this->isRunning()) {
                this->interrupt();
            }
            this->debug("Goodbye.\n");
        }

        void FlowControlClient::_initStatusFrame() {
            memset(&_statusFrame, 0, sizeof(TxStatusFrame));
            _statusFrame.v49.frameStart = VRLP;
            _statusFrame.v49.frameSize = 14;
            _statusFrame.v49.C = 1;
            _statusFrame.v49.packetSize = 11;
            _statusFrame.v49.TSI = 1;
            _statusFrame.v49.TSF = 0;
            _statusFrame.vend.frameEnd = VEND;
        }

        void FlowControlClient::_initStatusAddress() {
            _statusDestLen = sizeof(_statusDestAddr);
            memset(&_statusDestAddr, 0, _statusDestLen);
            _statusDestAddr.sin_family = AF_INET;
            _statusDestAddr.sin_addr.s_addr = htonl( INADDR_LOOPBACK );
            _statusDestAddr.sin_port = htons(_ducStreamId);

            memset(&_statusCopyAddr, 0, _statusDestLen);
            _statusCopyAddr.sin_family = AF_INET;
            _statusCopyAddr.sin_addr.s_addr = htonl( INADDR_LOOPBACK );
            _statusCopyAddr.sin_port = htons(0xfff0);
        }

        void FlowControlClient::_sendStatusFrame() {
            _statusFrame.status.emptyFlag = _tbsEmptyFlag;
            _statusFrame.status.fullFlag = _tbsFullFlag;
            _statusFrame.status.spaceAvailable = _tbsSpace;
            _statusFrame.status.underrunFlag = _tbsUnderrunFlag;
            _statusFrame.status.underrunCount = _tbsUnderrunCount;
            _statusFrame.status.overrunFlag = _tbsOverrunFlag;
            _statusFrame.status.overrunCount = _tbsOverrunCount;
            _statusFrame.v49.timeSeconds = _utc;
            _statusFrame.v49.frameCount = (_statusFrame.v49.frameCount+1)%4096;
            _statusFrame.v49.packetCount = (_statusFrame.v49.packetCount+1)%4096;
            if (_statusSockfd>=0) {
                sendto(_statusSockfd, (char *) &_statusFrame, sizeof(TxStatusFrame), 0, (struct sockaddr *) &_statusDestAddr, _statusDestLen);
                sendto(_statusSockfd, (char *) &_statusFrame, sizeof(TxStatusFrame), 0, (struct sockaddr *) &_statusCopyAddr, _statusDestLen);
            } else {
                std::cerr << "No socket to send status?" << std::endl;
            }
        }

        void FlowControlClient::run() {
            this->debug("entering run loop\n");
            _firstUpdate = true;
            while(true)
            {
                if ( (_mySocket != NULL) && _mySocket->isConnected())
                {
                    _queryUtc();
                    update();
                }
                this->sleep( ((double)_fcUpdateDelay)/1e6 );
            }
            this->debug("exiting run loop\n");
        }

        void FlowControlClient::update() {
            _queryBufferState();
        }

        bool FlowControlClient::connectToRadio(const std::string& hostname, unsigned int port) {
            bool ret;
            this->debug("connecting\n");
            _radioHostname = hostname;
            _radioTcpPort = port;
            if ( _mySocket != NULL )
            {
                delete _mySocket;
                _mySocket = NULL;
            }
            _mySocket = new ClientSocket(hostname, port, _debug);
            if ( _mySocket != NULL )
            {
                _mySocket->connectToServer();
                if (_mySocket->isConnected()) {
                    disableDuc();
                }
            }
            ret = (_mySocket != NULL) && _mySocket->isConnected();
            this->debug("connect = %s\n", BOOL_DEBUG(ret));
            return ret;
        }

        unsigned int FlowControlClient::setUpdateRate(unsigned int updatesPerSecond) {
            _fcUpdateRate = updatesPerSecond<=20?updatesPerSecond:20;
            _fcUpdateDelay = 1000000/_fcUpdateRate;
            _samplesPerUpdate = _getDucSampleRate() / _fcUpdateRate;
            return _fcUpdateRate;
        }

        void FlowControlClient::setDucChannel(unsigned int ducChannel) {
            this->debug("setting duc channel = %d\n", ducChannel);
            _ducChannel = ducChannel;
            _tbsQuery = (boost::format("TBS? %d\n") % _ducChannel).str();
            this->debug("duc channel ok\n");
        }

        bool FlowControlClient::disconnect() {
            this->debug("disconnecting\n");
            return _mySocket->disconnect();
        }

        void FlowControlClient::testQueries() {
            _queryBufferState();
        }

        std::string FlowControlClient::getRadioMac(unsigned int tenGbeIndex) {
            //this->debug("query radio mac\n");
            std::string dmac;
            std::string cmd = (boost::format("#MAC? %d\n") % tenGbeIndex).str();
            BasicStringList rspVec, splitRes;
            BasicStringList::iterator rspIter;
            if ( _mySocket != NULL )
            {
                if (!_mySocket->sendCmdAndGetRsp(cmd, rspVec, 100)) {
                    //std::cout << "...success!\n";
                } else {
                    //std::cout << "...ERROR?\n";
                }
                for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
                    if (strstr((*rspIter).c_str(),"#MAC ")!=NULL) {
                        //std::cout << "MAC ADDRESS!!!!" << *rspIter << std::endl;
                        split(splitRes, *rspIter, is_any_of(", "));
                        dmac = splitRes.back();
                    }
                }
                //this->debug("radio mac = %s\n", dmac.c_str());
            }
            else
            {
                //this->debug("radio mac skipped\n");
            }
            return dmac;
        }

        std::string FlowControlClient::getRadioIp(unsigned int tenGbeIndex) {
            std::string dip;
            std::string cmd = (boost::format("SIP? %d\n") % tenGbeIndex).str();
            BasicStringList rspVec, splitRes;
            BasicStringList::iterator rspIter;
            if ( _mySocket != NULL )
            {
                if (!_mySocket->sendCmdAndGetRsp(cmd, rspVec, 100)) {
                    //std::cout << "...success!\n";
                } else {
                    //std::cout << "...ERROR?\n";
                }
                for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
                    if (strstr((*rspIter).c_str(),"SIP ")!=NULL) {
                        //std::cout << "IP ADDRESS!!!!" << *rspIter << std::endl;
                        split(splitRes, *rspIter, is_any_of(", "));
                        dip = splitRes.back();
                    }
                    //this->debug("radio ip = %s\n", dip.c_str());
                }
            }
            else
            {
                //this->debug("radio ip skipped\n");
            }
            return dip;
        }

        bool FlowControlClient::disableDuc() {
            _ducEnable = false;
            std::string cmd = (boost::format("DUCHS %d, 0, 0, 0, 0, 0, 0, 0\n") % _ducChannel).str();
            std::string qry = (boost::format("DUCHS? %d\n") % _ducChannel ).str();
            _sendCmdAndQry(cmd, qry);
            return _sendDuc();
        }

        bool FlowControlClient::enableDuc(unsigned int rateIndex,
                unsigned int txChannel,
                unsigned int streamId,
                unsigned int tenGbeIndex,
                float attenuation,
                double txFreq,
                long ducFreq,
                unsigned int txAtten,
                bool ducEnable ) {
            setDucTenGbePort(tenGbeIndex, false);
            setDucEnable(ducEnable, false);
            setDucRateIndex(rateIndex, false);
            setDucStreamId(streamId, false);
            setDucFrequency(ducFreq, false);
            setTxFrequency(txFreq, false);
            setTxAttenuation(txAtten, false);
            setDucAttenuation(attenuation, false);
            return setDucTxChannel(txChannel, true);
        }

        //Optional method to set _txFreq and
        bool FlowControlClient::setTxFrequency(double txFreq, bool applySetting) {
            _txFreq = txFreq;
            return applySetting?_sendTxf():false;
        }

        /* _setTxAttenuation(unsigned int)
         *
         * sets internal variable _txAttenuation and then sends commands
         *
         */
        bool FlowControlClient::setTxAttenuation(unsigned int txAttenuation, bool applySetting) {
            _txAttenuation = txAttenuation;
            return applySetting?_sendTxa():false;
        }


        bool FlowControlClient::setDucTenGbePort(unsigned int ducTenGbePort, bool applySetting) {
            _ducTenGbePort = ducTenGbePort;
            return applySetting?_sendDuc():false;
        }

        bool FlowControlClient::setDucEnable(bool ducEnable, bool applySetting) {
            _ducEnable = ducEnable;
            return applySetting?_sendDuc():false;
        }

        /* _setDucTxChannel(unsigned int, bool)
         *
         * setter for _ducTxChannel; boolean flag controls application
         * of frequency and
         *
         */
        bool FlowControlClient::setDucTxChannel(unsigned int txChannel, bool applySetting) {
            bool cmdError = false;
            _ducTxChannel = txChannel;
            if (applySetting) {
                cmdError |= _sendTxp();
                cmdError |= _sendTxf();
                cmdError |= _sendTxa();
                cmdError |= _sendDuc();
            }
            return cmdError;
        }

        bool FlowControlClient::setDucRateIndex(unsigned int rateIndex, bool applySetting) {
            _ducRateIndex = rateIndex;
            _samplesPerUpdate = _getDucSampleRate() / _fcUpdateRate;
            return applySetting?_sendDuc():false;
        }

        bool FlowControlClient::setDucStreamId(unsigned int streamId, bool applySetting) {
            _ducStreamId = streamId;
            _statusFrame.v49.streamId = _ducStreamId;
            _initStatusAddress();
            return applySetting?_sendDuc():false;
        }

        bool FlowControlClient::setDucAttenuation(float attenuation, bool applySetting) {
            _ducAttenuation = attenuation;
            return applySetting?_sendWba():false;
        }

        bool FlowControlClient::setDucFrequency(long ducFreq, bool applySetting) {
            _ducFreq = ducFreq;
            return applySetting?_sendWbf():false;
        }

        bool FlowControlClient::setDucTxinvMode(unsigned int txinvMode, bool applySetting) {
            _txinvMode = txinvMode;
            return applySetting?_sendTxinv():false;
        }

        bool FlowControlClient::okToSend(long int numSamples, bool lockIfOk) {
            _fcMutex.lock();
            bool ok = _651freeSpace>numSamples;
            if (!(ok&&lockIfOk)) {
                _fcMutex.unlock();
            } else {
                _sendLock = true;
            }
            return ok;
        }

        long int FlowControlClient::getFreeSpace(void) {
            boost::mutex::scoped_lock lock(_fcMutex);
            return _651freeSpace;
        }

        bool FlowControlClient::sentNSamples(long int samplesSent) {
            if (!_sendLock) {
                _fcMutex.lock();
            }
            _651freeSpace -= samplesSent;
            _fcMutex.unlock();
            return _651freeSpace>TX_BUFFER_MIN_SIZE;
        }

        bool FlowControlClient::_sendCmdAndQry(const std::string& cmd, const std::string& qry) {
            bool cmdError = false;
            _rspVec.clear();
            cmdError |= _mySocket->sendCmdAndGetRsp(cmd, _rspVec, 10000);
            if (!cmdError) {
                _rspVec.clear();
                cmdError |= _mySocket->sendCmdAndGetRsp(qry, _rspVec, 10000);
            }
            this->debug("cmd = \"%s\"  rsp = \"%s\"  err = %s\n",
                    cmd.c_str(), _rspVec[0].c_str(),
                    BOOL_DEBUG(cmdError));
            return cmdError;
        }

        bool FlowControlClient::_sendShf() {
            bool cmdError = false;
            if (_config_tx&&(_shfMode>=0)) {
                for (int chan=1; chan<=2; chan++) {
                    if ((_ducTxChannel&chan)>0)
                    {
                        this->debug("_sendShf: txf=%f and shfMode=%d\n", _txFreq, _shfMode);
                        int currentShfMode;
                        BasicStringList::iterator rspIter;
                        BasicStringList splitRes;
                        std::string cmd, qry;
                        cmd = (boost::format("SHF %d, 1, %d\n") % chan %_shfMode ).str();
                        qry = (boost::format("SHF? %d, 1\n") % chan ).str();
                        _rspVec.clear();
                        cmdError = _mySocket->sendCmdAndGetRsp(qry, _rspVec, 10000);
                        for (rspIter = _rspVec.begin();
                                rspIter != _rspVec.end();
                                rspIter++)
                        {
                            if (strstr((*rspIter).c_str(),"SHF ") != NULL)
                            {
                                //this->debug("buffer state response = %s\n",
                                //   (*rspIter).c_str());
                                split(splitRes, *rspIter, is_any_of(", "));
                                // Sanity check -- make sure response is long enough
                                // to parse
                                if ( splitRes.size() >= 2 )
                                {
                                    for (int ii=0; ii<splitRes.size(); ii++) {
                                        std::cout << "splitRes.at(" << ii << ") = " << splitRes.at(ii).c_str() << std::endl;
                                    }
                                    currentShfMode = strtol( splitRes.at(5).c_str(), NULL, 10 );
                                    this->debug("currentShfMode = %d\n", currentShfMode);
                                    if (currentShfMode!=_shfMode)
                                    {
                                        cmdError = _sendCmdAndQry(cmd, qry);
                                    } else {
                                        std::cout << "NOT sending SHF" << std::endl;
                                    }
                                    break;
                                }
                            }
                        }
                    }
                }
            }
            return cmdError;
        }

        bool FlowControlClient::_sendTxf() {
            bool cmdError = false;
            bool shfChange = false;
            if (_config_tx) {
                std::string cmd, qry;
                if (_ducTxChannel!=0) {
                    _shfMode = (_txFreq<200.0)?1:0;
                    _sendShf();
                }
                //~ if ((_txFreq<200.0)&&(_shfMode!=1)) {
                //~ _shfMode = 1;
                //~ shfChange = true;
                //~ } else if ((_txFreq>=200.0)&&(_shfMode!=0)) {
                //~ _shfMode = 0;
                //~ shfChange = true;
                //~ }
                //~ if (shfChange) {
                //~ cmdError |= _sendShf();
                //~ }
                for (int chan=1; chan<=2; chan++) {
                    if ((_ducTxChannel&chan)>0) {
                        cmd = (boost::format("TXF %d, %f\n") % chan %  _txFreq ).str();
                        qry = (boost::format("TXF? %d\n") % chan ).str();
                        cmdError |= _sendCmdAndQry(cmd, qry);
                    }
                }
            }
            return cmdError;
        }

        /* _sendTxa()
         *
         * using internal variable _txAttenuation to formulate radio commands
         *
         */
        bool FlowControlClient::_sendTxa() {
            bool cmdError = false;
            if (_config_tx) {
                std::string cmd, qry;
                for (int chan=1; chan<=2; chan++) {
                    if ((_ducTxChannel&chan)>0) {
                        cmd = (boost::format("TXA %d, %d\n") % chan % _txAttenuation ).str();
                        qry = (boost::format("TXA? %d\n") % chan ).str();
                        cmdError |= _sendCmdAndQry(cmd, qry);
                    }
                }
            }
            return cmdError;
        }

        bool FlowControlClient::_sendTxp() {
            bool cmdError = false;
            if (_config_tx) {
                std::string cmd, qry;
                BasicStringList::iterator rspIter;
                BasicStringList splitRes;
                unsigned int channel, txstate;
                for (int chan=1; chan<=2; chan++) {
                    if ((_ducTxChannel&chan)>0) {
                        cmd = (boost::format("TXP %d, 1\n") % chan ).str();
                        qry = (boost::format("TXP? %d\n") % chan ).str();
                        _rspVec.clear();
                        cmdError = _mySocket->sendCmdAndGetRsp(qry, _rspVec, 10000);
                        for (rspIter = _rspVec.begin();
                                rspIter != _rspVec.end();
                                rspIter++)
                        {
                            if (strstr((*rspIter).c_str(),"TXP ") != NULL)
                            {
                                //this->debug("buffer state response = %s\n",
                                //    (*rspIter).c_str());
                                split(splitRes, *rspIter, is_any_of(", "));
                                // Sanity check -- make sure response is long enough
                                // to parse
                                if ( splitRes.size() >= 2 )
                                {
                                    channel = strtol( splitRes.at(1).c_str(), NULL, 10 );
                                    txstate = strtol( splitRes.at(3).c_str(), NULL, 10 );
                                    if ((channel==chan) && (txstate==0))
                                    {
                                        cmdError = _sendCmdAndQry(cmd, qry);
                                        break;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            return cmdError;
        }

        bool FlowControlClient::_sendTxinv() {
            bool cmdError = false;
            if (_config_tx) {
                std::string cmd, qry;
                cmd = (boost::format("TXINV %d, %d\n") % _ducChannel % _txinvMode ).str();
                qry = (boost::format("TXINV? %d\n") % _ducChannel ).str();
                cmdError |= _sendCmdAndQry(cmd, qry);
            }
            return cmdError;
        }

        bool FlowControlClient::_sendWbduc() {
            std::string cmd = (boost::format("WBDUC %d, %d, %d, %f, %d, %d, 0, %d\n") % _ducChannel % _ducTenGbePort % _ducFreq % _ducAttenuation % _ducRateIndex % (_ducEnable ? _ducTxChannel : 0) % _ducStreamId ).str();
            std::string qry = (boost::format("WBDUC? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_sendDucp() {
            std::string cmd = (boost::format("DUCP %d, %d\n") % _ducChannel % (_ducEnable ? 1 : 0) ).str();
            std::string qry = (boost::format("DUCP? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_sendDuc() {
            std::string cmd = (boost::format("DUC %d, %d, %d, %f, %d, %d, %d, %d\n")
            % _ducChannel
            % _ducTenGbePort
            % _ducFreq
            % _ducAttenuation
            % _ducRateIndex
            % (_ducEnable ? _ducTxChannel : 0)
            % (_ducEnable ? 0 : 1)
            % _ducStreamId ).str();
            std::string qry = (boost::format("DUC? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_sendWba() {
            std::string cmd = (boost::format("DUCA %d, %f\n") % _ducChannel % _ducAttenuation ).str();
            std::string qry = (boost::format("DUCA? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_sendWbf() {
            std::string cmd = (boost::format("DUCF %d, %d\n") % _ducChannel % _ducFreq ).str();
            std::string qry = (boost::format("DUCF? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_sendDip() {
            return true;
        }

        bool FlowControlClient::_sendDuchs() {
            return true;
        }

        bool FlowControlClient::unpause() {
            return _sendDucp();
        }

        bool FlowControlClient::setDucDipStatusEntry(int dipIndex, std::string dip, std::string dmac, unsigned int ducStatusPort) {
            if (dipIndex<0) {
                _ducDipIndex = 32-_ducChannel;
            } else {
                _ducDipIndex = dipIndex;
            }
            std::cout << "dIP = " << dip << " & dMAC = " << dmac << std::endl;
            std::string cmd = (boost::format("DIP %d, %d, %s, %s, %d, %d\n") % _ducTenGbePort % _ducDipIndex % dip % dmac % ducStatusPort % ducStatusPort ).str();
            std::string qry = (boost::format("DIP? %d, %d\n") % _ducTenGbePort % _ducDipIndex ).str();
            _sendCmdAndQry(cmd, qry);
            return false;
        }

        bool FlowControlClient::setDuchsParameters(unsigned int duchsFullThresh, unsigned int duchsEmptyThresh, unsigned int duchsPeriod) {
            _duchsFullThresh = duchsFullThresh;
            _duchsEmptyThresh = duchsEmptyThresh;
            _duchsPeriod = duchsPeriod;
            std::string cmd = (boost::format("DUCHS %d, %d, %d, %d, %d, %d, 0, %d\n") % _ducChannel % _ducTenGbePort % _duchsFullThresh % _duchsEmptyThresh % _duchsPeriod % _ducDipIndex % _ducStreamId ).str();
            std::string qry = (boost::format("DUCHS? %d\n") % _ducChannel ).str();
            return _sendCmdAndQry(cmd, qry);
        }

        bool FlowControlClient::_clearDucSettingsInRadio() {
            bool rv = false;
            std::string cmd = (boost::format("DUC %d, 0, 0, 0, 0, 0, 0, 0\n") % _ducChannel).str();
            std::string qry = (boost::format("DUC? %d\n") % _ducChannel ).str();
            rv = rv||_sendCmdAndQry(cmd, qry);

            cmd = (boost::format("DUCHS %d, 0, 0, 0, 0, 0, 0, 0\n") % _ducChannel).str();
            qry = (boost::format("DUCHS? %d\n") % _ducChannel ).str();
            rv = rv||_sendCmdAndQry(cmd, qry);
            return rv;
        }



        void FlowControlClient::_queryBufferState()
        {
            BasicStringList rspVec, splitRes;
            BasicStringList::iterator rspIter;
            _fcMutex.lock();
            if ( (_mySocket != NULL) &&
                    !_mySocket->sendCmdAndGetRsp(_tbsQuery, rspVec, 100, _debug))
            {
                _651freeSpaceLast = _651freeSpace;
                for (rspIter = rspVec.begin();
                        rspIter != rspVec.end();
                        rspIter++)
                {
                    if (strstr((*rspIter).c_str(),"TBS ") != NULL)
                    {
                        //this->debug("buffer state response = %s\n",
                        //    (*rspIter).c_str());
                        split(splitRes, *rspIter, is_any_of(", "));
                        // Sanity check -- make sure response is long enough
                        // to parse
                        if ( splitRes.size() >= 16 )
                        {
                            // Index 1 -- DUC channel
                            // Index 7 -- Sample space available
                            // Index 9 -- Underrun event happened
                            // Index 13 -- Overrun event happened
                            _tbsChannel = strtol( splitRes.at(1).c_str(), NULL, 10 );
                            if (_tbsChannel == _ducChannel)
                            {
                                _tbsEmptyFlag = strtol( splitRes.at(3).c_str(), NULL, 10 );
                                _tbsFullFlag = strtol( splitRes.at(5).c_str(), NULL, 10 );
                                _tbsSpace = strtol( splitRes.at(7).c_str(), NULL, 10 );
                                _tbsUnderrunFlag = strtol( splitRes.at(9).c_str(), NULL, 10 );
                                _tbsUnderrunCount = strtol( splitRes.at(11).c_str(), NULL, 10 );
                                _tbsOverrunFlag = strtol( splitRes.at(13).c_str(), NULL, 10 );
                                _tbsOverrunCount = strtol( splitRes.at(15).c_str(), NULL, 10 );

                                _651freeSpace = _tbsSpace;
                                _fcMutex.unlock();
                                //~ if (_tbsOverrunFlag || _tbsFullFlag)
                                //~ {
                                //~ this->debug(" O_%d@%lu_O\n", _ducChannel, _utc);
                                //~ std::cerr << (boost::format(" O_%d@%lu_O\n") % _ducChannel % _utc).str();
                                //~ std::cerr << "O" << _ducChannel << "@" << _utc << "o " << std::flush;
                                //~ }
                                //~ if (_tbsUnderrunFlag || _tbsEmptyFlag) {
                                //~ std::cerr << "U" << _ducChannel << "@" << _utc << "u " << std::flush;
                                //~ }
                                _sendStatusFrame();
                                break;
                            }
                        }
                        _firstUpdate = false;
                    }
                }
            } else {
                std::cerr << "FC Query Error." << std::endl;
            }
            _fcMutex.unlock();
        }

        void FlowControlClient::_queryUtc() {
            BasicStringList rspVec, splitRes;
            BasicStringList::iterator rspIter;
            if ( (_mySocket != NULL) &&
                    !_mySocket->sendCmdAndGetRsp("UTC?\n", rspVec, 100, _debug)) {
                for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
                    if (strstr((*rspIter).c_str(),"UTC ")!=NULL) {
                        split(splitRes, *rspIter, is_any_of(", "));
                        _utc = strtol( splitRes.back().c_str(), NULL, 10 );
                        _statusFrame.v49.timeSeconds = _utc;
                    }
                }
            } else {
            }
        }

        void FlowControlClient::_queryStatus() {
            BasicStringList rspVec, splitRes;
            BasicStringList::iterator rspIter;
            if ( (_mySocket != NULL) ) {
                _mySocket->sendCmdAndGetRsp("STAT?\n", rspVec, 100, _debug);
                //~ for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
                //~ if (strstr((*rspIter).c_str(),"STAT ")!=NULL) {
                //~ split(splitRes, *rspIter, is_any_of(", "));
                //~ _stat = strtol( splitRes.back().c_str(), NULL, 10 );
                //~ }
                //~ }
                _mySocket->sendCmdAndGetRsp("TSTAT?\n", rspVec, 100, _debug);
                //~ for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
                //~ if (strstr((*rspIter).c_str(),"TSTAT ")!=NULL) {
                //~ split(splitRes, *rspIter, is_any_of(", "));
                //~ _tstat = strtol( splitRes.back().c_str(), NULL, 10 );
                //~ }
                //~ }
            }
        }

        long FlowControlClient::_getDucSampleRate(void) const
        {
            long ret = 0;
            if ( _ducRateIndex == 16 )
                ret = 270833;
            else
                ret = (long)(102.4e6 / pow(2, _ducRateIndex));
            return ret;
        }

    }  /* namespace NDR651 */
}

