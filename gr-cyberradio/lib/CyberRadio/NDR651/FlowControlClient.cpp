/***************************************************************************
 * \file FlowControlClient.cpp
 *
 * \brief NDR651 flow control client.
 *
 * \author NH
 * \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.
 *
 */

#include "FlowControlClient.h"
#include "boost/format.hpp"
#include <boost/algorithm/string.hpp>
#include <math.h>
#include <stdlib.h>
#include <stdarg.h>

#define BOOL_DEBUG(x) (x ? "true" : "false")

using namespace boost::algorithm;


namespace gr
{
	namespace CyberRadio
	{
		namespace NDR651
		{
			FlowControlClient::FlowControlClient(unsigned int ducChannel,
													bool config_tx,
													unsigned int updatesPerSecond,
													bool debug) :
				_config_tx(config_tx),
				_ducChannel(0),
				_ducRateIndex(0),
				_ducStreamId(0),
				_ducTxChannel(0),
				_ducTenGbePort(0),
				_ducAttenuation(0),
				_txAttenuation(0),
				_txFreq(0.0),
				_ducFreq(0),
				_debug(debug)
			{
				this->debug("construction\n");
				_firstUpdate = true;
				_tbsQuery = std::string("\n");
				_651freeSpace = 0;
				_multiChannel = (ducChannel==0);
				_mySocket = NULL;
				for (int i=0; i<=8; i++) {
					_651freeSpaceArray[i] = 0;
					_fcMutexVector.push_back(new boost::mutex);
					_freeSpaceVector.push_back(0);
				}
				setDucChannel( ducChannel );
				setUpdateRate( updatesPerSecond );
			}

			FlowControlClient::~FlowControlClient() {
				this->debug("destruction\n");
				if (_mySocket->isConnected()) {
					_mySocket->disconnect();
				}
				this->interrupt();
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
				if (_multiChannel) {
					_tbsQuery = std::string("TBS?\n");
				} else {
					_tbsQuery = (boost::format("TBS? %d\n") % _ducChannel).str();
				}
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

			bool FlowControlClient::enableDuc(unsigned int rateIndex,
												unsigned int txChannel,
												unsigned int streamId,
												unsigned int tenGbeIndex,
												float attenuation,
												float txFreq,
												long ducFreq,
												unsigned int txAtten ) {
				_ducTenGbePort = tenGbeIndex;
				setDucRateIndex(rateIndex, false);
				setDucStreamId(streamId, false);
				setDucFrequency(ducFreq, false);
				setTxFrequency(txFreq, false);
				setTxAttenuation(txAtten, false);
				setDucAttenuation(attenuation, false);
				return setDucTxChannel(txChannel, true);
			}

			//Optional method to set _txFreq and
			bool FlowControlClient::setTxFrequency(int txFreq, bool applySetting) {
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
					cmdError |= _sendWbduc();
				}
				return cmdError;
			}

			bool FlowControlClient::setDucRateIndex(unsigned int rateIndex, bool applySetting) {
				_ducRateIndex = rateIndex;
				_samplesPerUpdate = _getDucSampleRate() / _fcUpdateRate;
				return applySetting?_sendWbduc():false;
			}

			bool FlowControlClient::setDucStreamId(unsigned int streamId, bool applySetting) {
				_ducStreamId = streamId;
				return applySetting?_sendWbduc():false;
			}

			bool FlowControlClient::setDucAttenuation(float attenuation, bool applySetting) {
				_ducAttenuation = attenuation;
				return applySetting?_sendWbduc():false;
			}

			bool FlowControlClient::setDucFrequency(long ducFreq, bool applySetting) {
				_ducFreq = ducFreq;
				return applySetting?_sendWbf():false;
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
			
			bool FlowControlClient::_sendTxf() {
				bool cmdError = false;
				if (_config_tx) {
					std::string cmd, qry;
					for (int chan=1; chan<=2; chan++) {
						if ((_ducTxChannel&chan)>0) {
							cmd = (boost::format("TXF %d, %f\n") % chan % _txFreq ).str();
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
									//		    (*rspIter).c_str());
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
			
			bool FlowControlClient::_sendWbduc(bool enable) {
				std::string cmd = (boost::format("WBDUC %d, %d, %d, %f, %d, %d, 0, %d\n") % _ducChannel % _ducTenGbePort % _ducFreq % _ducAttenuation % _ducRateIndex % (enable ? _ducTxChannel : 0) % _ducStreamId ).str();
				std::string qry = (boost::format("WBDUC? %d\n") % _ducChannel ).str();
				return _sendCmdAndQry(cmd, qry);
			}
			
			bool FlowControlClient::_sendWba() {
				std::string cmd = (boost::format("WBA %d, %f\n") % _ducChannel % _ducAttenuation ).str();
				std::string qry = (boost::format("WBA? %d\n") % _ducChannel ).str();
				return _sendCmdAndQry(cmd, qry);
			}
			
			bool FlowControlClient::_sendWbf() {
				std::string cmd = (boost::format("WBF %d, %d\n") % _ducChannel % _ducFreq ).str();
				std::string qry = (boost::format("WBF? %d\n") % _ducChannel ).str();
				return _sendCmdAndQry(cmd, qry);
			}
			

			void FlowControlClient::_queryBufferState()
			{
				BasicStringList rspVec, splitRes;
				BasicStringList::iterator rspIter;
				unsigned int channel, space, underrun, overrun;
				if ( (_mySocket != NULL) &&
					 !_mySocket->sendCmdAndGetRsp(_tbsQuery, rspVec, 100, false))
				{
					_651freeSpaceLast = _651freeSpace;
					for (rspIter = rspVec.begin();
						 rspIter != rspVec.end();
						 rspIter++)
					{
						if (strstr((*rspIter).c_str(),"TBS ") != NULL)
						{
							//this->debug("buffer state response = %s\n",
							//		    (*rspIter).c_str());
							split(splitRes, *rspIter, is_any_of(", "));
							// Sanity check -- make sure response is long enough
							// to parse
							if ( splitRes.size() >= 16 )
							{
								// Index 1 -- DUC channel
								// Index 7 -- Sample space available
								// Index 9 -- Underrun event happened
								// Index 13 -- Overrun event happened
								channel = strtol( splitRes.at(1).c_str(), NULL, 10 );
								space = strtol( splitRes.at(7).c_str(), NULL, 10 );
								underrun = strtol( splitRes.at(9).c_str(), NULL, 10 );
								overrun = strtol( splitRes.at(13).c_str(), NULL, 10 );
								_651freeSpaceArray[channel-1] = space;
								if (channel == _ducChannel)
								{
									_651freeSpace = space;
									if (overrun)
									{
										//~ this->debug(" O_%d@%lu_O\n", _ducChannel, _utc);
										//~ std::cerr << (boost::format(" O_%d@%lu_O\n") % _ducChannel % _utc).str();
										std::cerr << "O" << _ducChannel << "@" << _utc << "o " << std::flush;
									}
									if (underrun) {
										//~ this->debug(" U_%d@%lu_U\n", _ducChannel, _utc);
										//~ std::cerr << (boost::format(" U_%d@%lu_U\n") % _ducChannel % _utc).str();
										std::cerr << "U" << _ducChannel << "@" << _utc << "u " << std::flush;
									}
								}
							}
							_firstUpdate = false;
						}
					}
				} else {
				}
			}

			void FlowControlClient::_queryUtc() {
				BasicStringList rspVec, splitRes;
				BasicStringList::iterator rspIter;
				if ( (_mySocket != NULL) &&
					 !_mySocket->sendCmdAndGetRsp("UTC?\n", rspVec, 100, false)) {
					for (rspIter=rspVec.begin(); rspIter!=rspVec.end(); rspIter++) {
						if (strstr((*rspIter).c_str(),"UTC ")!=NULL) {
							split(splitRes, *rspIter, is_any_of(", "));
							_utc = strtol( splitRes.back().c_str(), NULL, 10 );
						}
					}
				} else {
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

			int FlowControlClient::debug(const char *format, ...)
			{
				int ret = 0;
				if (_debug)
				{
					ret = fprintf(stderr, "[%lu][FlowControlClient] ",
							      time(NULL));
					if (ret >= 0)
					{
						va_list ap;
						va_start(ap, format);
						ret = vfprintf(stderr, format, ap);
						va_end(ap);
					}
				}
				return ret;
			}

		}  /* namespace NDR651 */
	}
}

