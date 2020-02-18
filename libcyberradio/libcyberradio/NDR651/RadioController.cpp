#include "LibCyberRadio/NDR651/RadioController.h"

namespace LibCyberRadio
{
    namespace NDR651
    {
        /* Constructors and Destructors */
        RadioController::RadioController(const std::string& radioHostname, unsigned short radioPort, bool debug):
            Debuggable(debug, "RadioController"),
            radioHostname(radioHostname),
            radioPort(radioPort)
        {
            // Init and connect Client Socket right away
            this->clientSocket = new ClientSocket(radioHostname, radioPort);
        }

        RadioController::~RadioController()
        {
            if (this->clientSocket != NULL)
            {
                delete this->clientSocket;
            }
        }

        /* Private Methods ****************************************************/
        void RadioController::dumpRspVec()
        {
            for (int i = 0; i < this->rspVec.size(); i++)
            {
                std::cout << "Val: " << this->rspVec.at(i) << " Ind: " << i << std::endl;
            }
        }

        bool RadioController::sendCmd(const std::string& cmd, bool splitResponse)
        {
            // Create a TCP Connection to radio
            if (!this->clientSocket->connectToServer())
            {
                throw std::runtime_error("ClientSocket could not connect to radio");
            }

            if (this->clientSocket != NULL && this->clientSocket->isConnected())
            {
                bool cmdError = false;
                this->rspVec.clear(); // Clear whatever was in the buffer before

                // Send the command, returning success/fail as the result
                cmdError = this->clientSocket->sendCmdAndGetRsp(cmd, this->rspVec, CMD_TIMEOUT);

                // Split the response vector by commas and whitespace (if requested)
                if (splitResponse)
                {
                    boost::split(this->rspVec, this->rspVec.at(0), boost::algorithm::is_any_of(" ,"));
                }

                // Disconnect
                this->clientSocket->disconnect();

                return !cmdError;
            }
            this->debug("clientSocket is NULL or not connected\n");
            return false;
        }

        bool RadioController::sendCmdAndQry(const std::string& cmd, const std::string& qry, bool splitResponse)
        {
            // Create a TCP Connection to radio
            if (!this->clientSocket->connectToServer())
            {
                throw std::runtime_error("ClientSocket could not connect to radio");
            }

            if (this->clientSocket != NULL && this->clientSocket->isConnected())
            {
                bool cmdError = false;
                this->rspVec.clear(); // Clear whatever was in the buffer before

                // Send the command
                cmdError = this->clientSocket->sendCmdAndGetRsp(cmd, this->rspVec, CMD_TIMEOUT);

                // Only send the query to check status if the command had no error
                if (!cmdError)
                {
                    this->rspVec.clear();
                    cmdError |= this->clientSocket->sendCmdAndGetRsp(qry, this->rspVec, CMD_TIMEOUT);

                    // Split the response vector by commas and whitespace (if requested)
                    if (splitResponse)
                    {
                        boost::split(this->rspVec, this->rspVec.at(0), boost::algorithm::is_any_of(" ,"));
                    }
                }
                // Disconnect
                this->clientSocket->disconnect();

                return !cmdError;
            }
            this->debug("clientSocket is NULL or not connected\n");
            return false;
        }

        /* Public Methods ****************************************************/
        std::string RadioController::getRadioMac(unsigned int tenGbeIndex)
        {
            std::string cmd = (boost::format("#MAC? %d\n") % tenGbeIndex).str();
            return this->sendCmd(cmd) ? this->rspVec.at(1) : "";
        }

        std::string RadioController::getRadioIP(unsigned int tenGbeIndex)
        {
            std::string cmd = (boost::format("SIP? %d\n") % tenGbeIndex).str();
            return this->sendCmd(cmd) ? this->rspVec.at(3) : "";
        }

        bool RadioController::setTXF(unsigned int rfTxChannel, double freq)
        {
            // 1) Query SHF Setting
            // 2) Query TXF
            // If TXF > 200 && freq <= 200 && shf disabled , enable shf
            // If TXF <= 200 && freq > 200 && shf enabled, disable shf

            if (rfTxChannel==3) {
                bool rv[2];
                int i=0;
                while (i<2) {
                    rv[i] = this->setTXF(++i, freq);
                }
                return rv[0]&&rv[1];
            } else {
                std::string cmd, qry;
                double epsilon = 0.000001; // This is the smallest double that would be 1Hz difference between tuned value and requested value

                // Query SHF Setting
                qry = (boost::format("SHF? %d, 1\n") % rfTxChannel).str();
                if (!this->sendCmd(qry)) return false;
                unsigned int currentShf = atoi(this->rspVec.at(5).c_str());

                // Query TXF Setting
                qry = (boost::format("TXF? %d\n") % rfTxChannel).str();
                if (!this->sendCmd(qry)) return false;
                double setFreq = atof(this->rspVec.at(3).c_str());

                // Set SHF if needed
                if ((currentShf == 1) && (setFreq <= 200) && (freq > 200))
                {
                    // Disable SHF
                    this->setSHF(rfTxChannel, 0);
                }
                else if ((currentShf == 0) && ((setFreq > 200) || (setFreq < epsilon)) && (freq <= 200))
                {
                    // Enable SHF
                    this->setSHF(rfTxChannel, 1);
                }

                // Send TXF, and make sure it took
                cmd = (boost::format("TXF %d, %f\n") % rfTxChannel % freq).str();
                qry = (boost::format("TXF? %d\n") % rfTxChannel).str();
                if (this->sendCmdAndQry(cmd, qry))
                {
                    setFreq = atof(this->rspVec.at(3).c_str());
                    return (std::abs(setFreq - freq) < epsilon);
                }
            }
            return false;
        }

        double RadioController::getTXA(unsigned int channel)
        {
            double ret = 0.0;
            std::string qry = (boost::format("TXA? %d\n") % channel).str();
            if (this->sendCmd(qry))
            {
                ret = atof(this->rspVec.at(3).c_str());
            }
            return ret;
        }

        bool RadioController::setTXA(unsigned int channel, double attenuation)
        {
            if (channel==3) {
                bool rv[2];
                int i=0;
                while (i<2) {
                    rv[i] = this->setTXA(++i, attenuation);
                }
                return rv[0]&&rv[1];
            } else {
                std::string cmd = (boost::format("TXA %d, %f\n") % channel % attenuation).str();
                std::string qry = (boost::format("TXA? %d\n") % channel).str();
                if (this->sendCmdAndQry(cmd, qry))
                {
                    double setAttenuation = atof(this->rspVec.at(3).c_str());
                    double epsilon = 1.0;
                    return (std::fabs(setAttenuation - attenuation) < epsilon);
                }
            }
        }

        bool RadioController::setTXP(unsigned int channel, bool enable)
        {
            if (channel==3) {
                bool rv[2];
                int i=0;
                while (i<2) {
                    rv[i] = this->setTXP(++i, enable);
                }
                return rv[0]&&rv[1];
            } else {
                std::string cmd = (boost::format("TXP %d, %d\n") % channel % (int)(enable)).str();
                std::string qry = (boost::format("TXP? %d\n") % channel).str();

                // Query TXP first, because it takes a long time and might mess radio state up if it's set twice
                if (!this->sendCmd(qry)) return false;
                bool setEnable = atof(this->rspVec.at(3).c_str());
                if (setEnable == enable) return false;

                if (this->sendCmdAndQry(cmd, qry))
                {
                    setEnable = (bool)(atoi(this->rspVec.at(3).c_str()));
                    return setEnable == enable;
                }
            }
            return false;
        }

        bool RadioController::setTXINV(unsigned int ducChannel, bool invert)
        {
            std::string cmd = (boost::format("TXINV %d, %d\n") % ducChannel % (int)(invert)).str();
            std::string qry = (boost::format("TXINV? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool setInvert = (bool)(atoi(this->rspVec.at(3).c_str()));
                return setInvert == invert;
            }
            return false;
        }

        bool RadioController::setDUCP(unsigned int ducChannel, bool pause)
        {
            std::string cmd = (boost::format("DUCP %d, %d\n") % ducChannel % (int)(pause)).str();
            std::string qry = (boost::format("DUCP? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool setPause = (bool)(atoi(this->rspVec.at(3).c_str()));
                return setPause == pause;
            }
            return false;
        }

        bool RadioController::setDUCA(unsigned int ducChannel, double attenuation)
        {
            std::string cmd = (boost::format("DUCA %d, %f\n") % ducChannel % attenuation).str();
            std::string qry = (boost::format("DUCA? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                double setAttenuation = atof(this->rspVec.at(3).c_str());
                double epsilon = 0.2;
                return (std::fabs(setAttenuation - attenuation) <= epsilon);
            }
            return false;
        }

        bool RadioController::setDUCF(unsigned int ducChannel, double freq)
        {
            std::string cmd = (boost::format("DUCF %d, %f\n") % ducChannel % freq).str();
            std::string qry = (boost::format("DUCF? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                double setFreq = atof(this->rspVec.at(3).c_str());
                return setFreq == freq;
            }
            return false;
        }

        bool RadioController::clearDUCG(unsigned int ducGroup)
        {
            std::string cmd, qry;
            bool success = true;
            for (int i = 1; i <= 8; i++)
            {
                cmd = (boost::format("DUCG %d, %d, 0\n") % ducGroup % i).str();
                qry = (boost::format("DUCG? %d, %d\n") % ducGroup % i).str();
                if (this->sendCmdAndQry(cmd, qry))
                {
                    unsigned int setEnable = (unsigned int)(atoi(this->rspVec.at(5).c_str()));
                    success &= (setEnable == 0);
                }
            }
            return success;
        }

        bool RadioController::setDUCG(unsigned int ducGroup, unsigned int ducChannel, bool enable)
        {
            std::string cmd = (boost::format("DUCG %d, %d, %d\n") % ducGroup % ducChannel % enable).str();
            std::string qry = (boost::format("DUCG? %d, %d\n") % ducGroup % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool setEnable = (bool)(atoi(this->rspVec.at(5).c_str()));
                return (setEnable == enable);
            }
        }

        bool RadioController::setDUCGE(unsigned ducGroup, bool enable)
        {
            std::string cmd = (boost::format("DUCGE %d, %d\n") % ducGroup % enable).str();
            std::string qry = (boost::format("DUCGE? %d\n") % ducGroup).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool setEnable = (bool)(atoi(this->rspVec.at(3).c_str()));
                return (setEnable == enable);
            }
        }

        bool RadioController::setSHF(unsigned int rfTxChannel, bool enable)
        {
            std::string cmd = (boost::format("SHF %d, 1, %d\n") % rfTxChannel % (int)(enable)).str();
            std::string qry = (boost::format("SHF? %d, 1\n") % rfTxChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool shfEnable = (bool)(atoi(this->rspVec.at(5).c_str()));
                return shfEnable == enable;
            }
            return false;
        }

        bool RadioController::setSIP(unsigned int tenGbeIndex, const std::string& sourceIP)
        {
            std::string cmd = (boost::format("SIP %d, %s\n") % tenGbeIndex % sourceIP).str();
            std::string qry = (boost::format("SIP? %d\n") % tenGbeIndex).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                std::string setSIP = this->rspVec.at(3);
                return setSIP == sourceIP;
            }
            return false;
        }

        bool RadioController::setDIP(
                unsigned int ducChannel,
                unsigned int tenGbeIndex,
                const std::string& destIP,
                const std::string& destMAC,
                unsigned short ducStatusPort
        )
        {
            // Conventionally, we start status receivers at DIP index 32 - ducChannel
            unsigned int ducDipIndex = 32 - ducChannel;
            std::string cmd = (boost::format("DIP %d, %d, %s, %s, %d, %d\n") % tenGbeIndex % ducDipIndex % destIP % destMAC % ducStatusPort % ducStatusPort ).str();
            std::string qry = (boost::format("DIP? %d, %d\n") % tenGbeIndex % ducDipIndex ).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                // We need to check that the IP, MAC, port, and stream ID were all set correctly
                bool success = true;
                success &= (this->rspVec.at(11) == destIP);
                success &= (this->rspVec.at(13) == destMAC);
                success &= (atoi(this->rspVec.at(15).c_str()) == ducStatusPort);
                success &= (atoi(this->rspVec.at(17).c_str()) == ducStatusPort);
                return success;
            }
            return false;
        }

        bool RadioController::setDUC(
                unsigned ducChannel,
                unsigned int tenGbeIndex,
                double ducFreq,
                double attenuation,
                unsigned int ducRateIndex,
                unsigned int rfTxChannel, // Note 3 is TX on RF1 and RF2
                unsigned int mode,
                unsigned int streamID
        )
        {
            std::string cmd = (boost::format("DUC %d, %d, %d, %f, %d, %d, %d, %d\n") % ducChannel % tenGbeIndex % ducFreq % attenuation % ducRateIndex % rfTxChannel % mode % streamID ).str();
            std::string qry = (boost::format("DUC? %d\n") % ducChannel ).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool success = true;
                success &= (atoi(this->rspVec.at(3).c_str()) == tenGbeIndex);
                success &= (atof(this->rspVec.at(5).c_str()) == ducFreq);

                double setAttenuation = atof(this->rspVec.at(7).c_str());
                double epsilon = 0.1;
                success &= (std::abs(setAttenuation - attenuation) < epsilon);

                success &= (atoi(this->rspVec.at(9).c_str()) == ducRateIndex);
                success &= (atoi(this->rspVec.at(11).c_str()) == rfTxChannel);
                success &= (atoi(this->rspVec.at(13).c_str()) == mode);
                success &= (atoi(this->rspVec.at(15).c_str()) == streamID);
                return success;
            }
            return false;
        }

        bool RadioController::setDUCHS(
                unsigned int ducChannel,
                unsigned int tenGbeIndex,
                unsigned int fullThresh,
                unsigned int emptyThresh,
                unsigned int duchsPeriod,
                unsigned int ducStreamID
        )
        {
            unsigned int ducDipIndex = 32 - ducChannel;
            std::string cmd = (boost::format("DUCHS %d, %d, %d, %d, %d, %d, 0, %d\n") % ducChannel % tenGbeIndex % fullThresh % emptyThresh % duchsPeriod % ducDipIndex % ducStreamID ).str();
            std::string qry = (boost::format("DUCHS? %d\n") % ducChannel ).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool success = true;
                success &= (atoi(this->rspVec.at(3).c_str()) == tenGbeIndex);
                success &= (atoi(this->rspVec.at(5).c_str()) == fullThresh);
                success &= (atoi(this->rspVec.at(7).c_str()) == emptyThresh);
                success &= (atoi(this->rspVec.at(9).c_str()) == duchsPeriod);
                success &= (atoi(this->rspVec.at(11).c_str()) == ducDipIndex);
                success &= (atoi(this->rspVec.at(15).c_str()) == ducStreamID);
                return success;
            }
            return false;
        }

        /*
             Alternate version of setDUCHS
             thresholdPercents will be calculated to the nearest 4 samples.
         */
        bool RadioController::setDUCHSPercent(
                unsigned int ducChannel,
                unsigned int tenGbeIndex,
                double fullThreshPercent,
                double emptyThreshPercent,
                unsigned int updatesPerSecond,
                unsigned int ducStreamID
        )
        {
            unsigned int ducDipIndex = 32 - ducChannel;
            unsigned int fullThresh, emptyThresh, duchsPeriod;
            // Round the number of samples to a factor of 4. (This is what the radio does anyway)
            fullThresh = ((unsigned int )(fullThreshPercent * 67108860)) - ((unsigned int )(fullThreshPercent * 67108860)%4);
            emptyThresh = ((unsigned int )(emptyThreshPercent * 67108860)) - ((unsigned int )(emptyThreshPercent * 67108860)%4);
            if ((updatesPerSecond > 0) && (updatesPerSecond <= 200))
            {
                duchsPeriod = 1000/5/updatesPerSecond;
            }
            else
            {
                // periodic flow control
                duchsPeriod = 0;
            }

            std::string cmd = (boost::format("DUCHS %d, %d, %d, %d, %d, %d, 0, %d\n") % ducChannel % tenGbeIndex % fullThresh % emptyThresh % duchsPeriod % ducDipIndex % ducStreamID ).str();
            std::string qry = (boost::format("DUCHS? %d\n") % ducChannel ).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool success = true;
                success &= (atoi(this->rspVec.at(3).c_str()) == tenGbeIndex);
                success &= (atoi(this->rspVec.at(5).c_str()) == fullThresh);
                success &= (atoi(this->rspVec.at(7).c_str()) == emptyThresh);
                success &= (atoi(this->rspVec.at(9).c_str()) == duchsPeriod);
                success &= (atoi(this->rspVec.at(11).c_str()) == ducDipIndex);
                success &= (atoi(this->rspVec.at(15).c_str()) == ducStreamID);
                return success;
            }
            return false;
        }

        bool RadioController::clearDUC(unsigned int ducChannel)
        {
            std::string cmd = (boost::format("DUC %d, 0, 0, 0, 0, 0, 0, 0\n") % ducChannel).str();
            std::string qry = (boost::format("DUC? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool success = true;
                success &= (atoi(this->rspVec.at(3).c_str()) == 0);
                success &= (atoi(this->rspVec.at(5).c_str()) == 0);
                success &= (atoi(this->rspVec.at(7).c_str()) == 0);
                success &= (atoi(this->rspVec.at(9).c_str()) == 0);
                success &= (atoi(this->rspVec.at(11).c_str()) == 0);
                success &= (atoi(this->rspVec.at(13).c_str()) == 0);
                success &= (atoi(this->rspVec.at(15).c_str()) == 0);
                return success;
            }
            return false;
        }

        bool RadioController::clearDUCHS(unsigned int ducChannel)
        {
            std::string cmd = (boost::format("DUCHS %d, 0, 0, 0, 0, 0, 0, 0\n") % ducChannel).str();
            std::string qry = (boost::format("DUCHS? %d\n") % ducChannel).str();
            if (this->sendCmdAndQry(cmd, qry))
            {
                bool success = true;
                success &= (atoi(this->rspVec.at(3).c_str()) == 0);
                success &= (atoi(this->rspVec.at(5).c_str()) == 0);
                success &= (atoi(this->rspVec.at(7).c_str()) == 0);
                success &= (atoi(this->rspVec.at(9).c_str()) == 0);
                success &= (atoi(this->rspVec.at(11).c_str()) == 0);
                success &= (atoi(this->rspVec.at(13).c_str()) == 0);
                success &= (atoi(this->rspVec.at(15).c_str()) == 0);
                return success;
            }
            return false;
        }

        bool RadioController::querySTAT(bool verbose)
        {
            std::string cmd = (boost::format("STAT?%s\n") % (verbose?" v":"") ).str();
            this->sendCmd(cmd, true);
            return false;
        }

        bool RadioController::queryTSTAT(bool verbose)
        {
            std::string cmd = (boost::format("TSTAT?%s\n") % (verbose?" v":"") ).str();
            this->sendCmd(cmd, true);
            return false;
        }


    }
}
