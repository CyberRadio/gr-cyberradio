/* -*- c++ -*- */
/***************************************************************************
 * \file Vita49Packet.cpp
 *
 * \brief VITA 49 packet decoder.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#include "Vita49Packet.h"
#include <volk/volk.h>
#include <string.h>
#include <sstream>
#include <iomanip>
#include <iostream>


namespace gr
{
	namespace CyberRadio
	{

		Vita49Packet::Vita49Packet(int vitaType,
				                   size_t payloadSize,
		                           size_t vitaHeaderSize,
		                           size_t vitaTailSize,
		                           bool byteSwapped,
		                           bool iqSwapped,
		                           unsigned char* rawData,
		                           size_t rawDataLen) :
		    vitaType(vitaType),
		    payloadSize(payloadSize),
		    vitaHeaderSize(vitaHeaderSize),
		    vitaTailSize(vitaTailSize),
		    byteSwapped(byteSwapped),
		    iqSwapped(iqSwapped),
			frameAlignmentWord(0),
			frameCount(0),
			frameSize(0),
			packetType(0),
			hasClassId(false),
			hasTrailer(false),
			timestampIntType(0),
			timestampFracType(0),
			packetCount(0),
			packetSize(0),
			streamId(0),
			organizationallyUniqueId(0),
			informationClassCode(0),
			packetClassCode(0),
			timestampInt(0),
			timestampFrac(0),
			frameTrailerWord(0)
		{
			// Calculate packet size
			_totalPacketSize = vitaType == 0 ? payloadSize : vitaHeaderSize +
					                           payloadSize + vitaTailSize;
			// Allocate buffer for raw data
			_rawData = new unsigned char[_totalPacketSize];
			size_t setSize = rawDataLen < _totalPacketSize ? rawDataLen : _totalPacketSize;
			// Copy data into our buffer
			memset(_rawData, 0, setSize);
			memcpy(_rawData, rawData, setSize);
			// Apply byte-swapping on a word-by-word basis
			if (byteSwapped)
			{
				volk_32u_byteswap((uint32_t*) (_rawData), setSize / sizeof(uint32_t));
			}
			// Start current word counter
			int currentWord = 0;
			// Decode VITA 49 packet header parameters (if applicable)
			if (vitaType == 551 )
			{
				packetType = (int) ((rawDataWord(currentWord) & 0xF0000000) >> 28);
				hasClassId = ((rawDataWord(currentWord) & 0x08000000) >> 27) == 1;
				hasTrailer = ((rawDataWord(currentWord) & 0x04000000) >> 26) == 1;
				timestampIntType = (int) ((rawDataWord(currentWord) & 0x00C00000) >> 22);
				timestampFracType = (int) ((rawDataWord(currentWord) & 0x00300000) >> 20);
				packetCount = (int) ((rawDataWord(currentWord) & 0x000F0000) >> 16);
				packetSize = (int) ((rawDataWord(currentWord) & 0x0000FFFF));
				currentWord++;
				streamId = rawDataWord(currentWord);
				currentWord++;
				if (hasClassId)
				{
					organizationallyUniqueId = (int) (rawDataWord(currentWord) & 0x0FFFFFFF);
					currentWord++;
					informationClassCode = (int) ((rawDataWord(currentWord) & 0xFFFF0000) >> 16);
					packetClassCode = (int) (rawDataWord(currentWord) & 0x0000FFFF);
					currentWord++;
				}
				// Decode integer-seconds timestamp if the type indicates that one is present
				if (timestampIntType > 0)
				{
					timestampInt = rawDataWord(currentWord);
					currentWord++;
				}
				// Decode fractional-seconds timestamp if the type indicates that one is present
				if (timestampFracType > 0)
				{
					timestampFrac = (uint64_t)(rawDataWord(currentWord))
							<< 32 + rawDataWord(currentWord + 1);
					currentWord += 2;
				}
				//Skip context, for now
				currentWord += 5;
			} else if (vitaType > 0)
			{
				frameAlignmentWord = (uint32_t)(rawDataWord(0));
				frameCount = (int) ((rawDataWord(1) & 0xFFF00000) >> 20);
				frameSize = (int) ((rawDataWord(1) & 0x000FFFFF));
				packetType = (int) ((rawDataWord(2) & 0xF0000000) >> 28);
				hasClassId = ((rawDataWord(2) & 0x08000000) >> 27) == 1;
				hasTrailer = ((rawDataWord(2) & 0x04000000) >> 26) == 1;
				timestampIntType = (int) ((rawDataWord(2) & 0x00C00000) >> 22);
				timestampFracType = (int) ((rawDataWord(2) & 0x00300000) >> 20);
				packetCount = (int) ((rawDataWord(2) & 0x000F0000) >> 16);
				packetSize = (int) ((rawDataWord(2) & 0x0000FFFF));
				currentWord = 3;
				// Decode stream ID if the packet type indicates that one is present
				if ((packetType == 1) || (packetType == 3))
				{
					streamId = rawDataWord(currentWord);
					currentWord++;
				}
				// Decode class ID if the "C" bit indicates that one is present
				if (hasClassId)
				{
					organizationallyUniqueId = (int) (rawDataWord(currentWord) & 0x0FFFFFFF);
					currentWord++;
					informationClassCode = (int) ((rawDataWord(currentWord) & 0xFFFF0000) >> 16);
					packetClassCode = (int) (rawDataWord(currentWord) & 0x0000FFFF);
					currentWord++;
				}
				// Decode integer-seconds timestamp if the type indicates that one is present
				if (timestampIntType > 0)
				{
					timestampInt = rawDataWord(currentWord);
					currentWord++;
				}
				// Decode fractional-seconds timestamp if the type indicates that one is present
				if (timestampFracType > 0)
				{
					timestampFrac = (uint64_t)(rawDataWord(currentWord) << 32)
							      + rawDataWord(currentWord + 1);
//					std::cerr << "[DBG] TFRAC"
//							  << " msw=" << rawDataWord(currentWord)
//							  << " lsw=" << rawDataWord(currentWord + 1)
//							  << " comb=" << timestampFrac
//							  << std::endl;
					currentWord += 2;
				}
			}
			// Decode I/Q payload data
			// -- Calculate the number of samples in the payload
			samples = payloadSize / sizeof(int16_t) / 2;
			// -- Allocate buffer for I/Q payload data
			sampleData = new int16_t[samples * 2];
			memset(sampleData, 0, samples * 2);
			// -- Iterate over payload data and unpack it into I and Q data.
			//    Take I/Q swapping settings into account.
			uint16_t tmp;
			for (int sample = 0; sample < samples; sample++)
			{
				if ( iqSwapped )
				{
					tmp = (uint16_t)(rawDataWord(currentWord) & 0x0000FFFF);
					sampleData[sample * 2] = (int16_t)tmp;
					tmp = (uint16_t)((rawDataWord(currentWord) & 0xFFFF0000) >> 16);
					sampleData[sample * 2 + 1] = (int16_t)tmp;
				}
				else
				{
					tmp = (uint16_t)((rawDataWord(currentWord) & 0xFFFF0000) >> 16);
					sampleData[sample * 2] = (int16_t)tmp;
					tmp = (uint16_t)(rawDataWord(currentWord) & 0x0000FFFF);
					sampleData[sample * 2 + 1] = (int16_t)tmp;
				}
				currentWord++;
			}
			// Decode VITA 49 frame trailer (if applicable)
			if ( hasTrailer )
				frameTrailerWord = rawDataWord(currentWord);
		}

		Vita49Packet::~Vita49Packet()
		{
			if (_rawData != NULL)
				delete _rawData;
			if (sampleData != NULL)
				delete sampleData;
		}

		bool Vita49Packet::isVita49() const
		{
			return (vitaType != 0);
		}

		uint32_t Vita49Packet::rawDataWord(int index)
		{
			return *((uint32_t*) ((_rawData + index * sizeof(uint32_t))));
		}

		int16_t Vita49Packet::getSampleI(int sample)
		{
			int16_t ret = 0;
			if ( (sample >= 0) && (sample < samples) )
				ret = sampleData[sample * 2];
			return ret;
		}

		int16_t Vita49Packet::getSampleQ(int sample)
		{
			int16_t ret = 0;
			if ( (sample >= 0) && (sample < samples) )
				ret = sampleData[sample * 2 + 1];
			return ret;
		}

		std::string Vita49Packet::rawDataBufferHex(unsigned char* buf, int length)
		{
			std::ostringstream oss;
			for (int i = 0; i < length; i++)
				oss << std::hex << std::setw(2) << std::setfill('0')
					<< (unsigned int) (buf[i]);
			return oss.str();
		}

		std::string Vita49Packet::dump()
		{
			std::ostringstream oss;
			if ( vitaType == 0 )
			{
				oss << "I/Q PACKET\n";
			} else {
				oss << "VITA 49 PACKET\n"
					<< "    raw=" << rawDataHex() << "\n"
				    << "    type=" << vitaType << "\n"
				    << "    Frame Details\n"
				    << "        count=" << frameCount << "\n"
				    << "        size=" << frameSize << "\n"
				    << "        align word=" << frameAlignmentWord << "\n";
				if ( hasTrailer )
				    oss << "        trail word=" << frameTrailerWord << "\n";
				oss << "    Packet Details\n"
				    << "        type=" << packetType << "\n"
				    << "        count=" << packetCount << "\n"
				    << "        size=" << packetSize << "\n"
				    << "        timestamp types: int=" << timestampIntType
				                                       << " frac=" << timestampFracType
				                                       << "\n";
				if ( (packetType == 1) || (packetType == 3) )
				{
				    oss << "        stream ID=" << streamId << "\n";
				}
				if ( hasClassId )
				{
				    oss << "        class ID: OUI=" << organizationallyUniqueId
				                                    << " ICC=" << informationClassCode
				                                    << " PCC=" << packetClassCode
				                                    << "\n";

				}
				if ( timestampIntType > 0 )
				{
				    oss << "        timestamp: int=" << timestampInt;
					if ( timestampFracType > 0 )
					    oss << " frac=" << timestampFrac;
				    oss << "\n";
				}
			}
		    oss << "    Payload Details\n"
		        << "        samples=" << samples << "\n";
		    for (int sample = 0; sample < 10; sample++)
		    {
		        oss << "        samp" << std::setw(3) << std::setfill('0') << sample
		            << ": i=" << std::hex << std::setw(4) << std::setfill('0') << getSampleI(sample)
		            << " q=" << std::hex << std::setw(4) << std::setfill('0') << getSampleQ(sample)
		            << "\n";
		    }
			oss << "[END PACKET]";
			return oss.str();
		}

	} /* namespace CyberRadio */
} /* namespace gr */
