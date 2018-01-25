/*
*	RadioContoller - Class to send radio configuration to the NDR651
* 	Author: Nathan Harter
*	Author: Joseph Martin
*	Date: 5/24/2017
*/

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_RADIOCONTROLLER_H
#define INCLUDED_LIBCYBERRADIO_NDR651_RADIOCONTROLLER_H

#include "LibCyberRadio/Common/Debuggable.h"
#include "LibCyberRadio/NDR651/ClientSocket.h"
#include "LibCyberRadio/Common/BasicList.h"
#include <boost/algorithm/string.hpp>
#include <boost/format.hpp>
#include <cmath>

#define CMD_TIMEOUT 10000 // How long to wait for a response from radio

namespace LibCyberRadio
{
	namespace NDR651
	{
		class RadioController : public Debuggable
		{
			private:
				/* Member Variables */
				ClientSocket *clientSocket; // Handles communication to NDR651
				std::string radioHostname;
				unsigned short radioPort;
				BasicStringList rspVec;

				/* Private Methods */
				bool sendCmd(const std::string& cmd, bool splitResponse = true);
				bool sendCmdAndQry(const std::string& cmd, const std::string& qry, bool splitResponse = true);
				void dumpRspVec();
				
			public:
				/* Constructors and Destructors */
				RadioController(const std::string& radioHostname, unsigned short radioPort, bool debug = false);
				~RadioController();

				/* Public Methods */
				std::string getRadioMac(unsigned int tenGbeIndex);
				std::string getRadioIP(unsigned int tenGbeIndex);
				bool setTXF(unsigned int channel, double freq);
				double getTXA(unsigned int channel);
				bool setTXA(unsigned int channel, double attenuation);
				bool setTXP(unsigned int channel, bool enable);
				bool setTXINV(unsigned int ducChannel, bool invert);
				bool setDUCP(unsigned int ducChannel, bool pause);
				bool setDUCA(unsigned int ducChannel, double attenuation);
				bool setDUCF(unsigned int ducChannel, double freq);
				bool setSHF(unsigned int channel, bool enable);
				bool setSIP(unsigned int tenGbeIndex, const std::string& sourceIP);
				bool setDIP(
					unsigned int ducChannel, 
					unsigned int tenGbeIndex, 
					const std::string& destIP, 
					const std::string& destMAC, 
					unsigned short ducStatusPort
				);
				bool setDUC(
					unsigned int ducChannel,
					unsigned int tenGbeIndex,
					double ducFreq,
					double attenuation, 
					unsigned int ducRateIndex,
					unsigned int rfTxChannel, // Note 3 is TX on RF1 and RF2
					unsigned int mode,
					unsigned int streamID
				);
				bool setDUCHS(
					unsigned int ducChannel,
					unsigned int tenGbeIndex,
					unsigned int fullThresh,
					unsigned int emptyThresh,
					unsigned int duchsPeriod,
					unsigned int ducStreamID
				);
				bool setDUCHSPercent(
					unsigned int ducChannel,
					unsigned int tenGbeIndex,
					double fullThreshPercent,
					double emptyThreshPercent,
					unsigned int updatesPerSecond,
					unsigned int ducStreamID
				);
				bool clearDUC(unsigned int ducChannel);
				bool clearDUCHS(unsigned int ducChannel);
				bool clearDUCG(unsigned int ducGroup);
				bool setDUCG(unsigned int ducGroup, unsigned int ducChannel, bool enable);
				bool setDUCGE(unsigned int ducGroup, bool enable);
				bool querySTAT(bool verbose);
				bool queryTSTAT(bool verbose);
		};
	}
}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_RADIOCONTROLLER_H */
