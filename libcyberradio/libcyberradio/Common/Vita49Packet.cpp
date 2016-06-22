/* -*- c++ -*- */
/***************************************************************************
 * \file Vita49Packet.cpp
 *
 * \brief VITA 49 packet decoder.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#include <LibCyberRadio/Common/Vita49Packet.h>
#include <string.h>
#include <sstream>
#include <iomanip>
#include <iostream>


namespace LibCyberRadio
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
		_rawData = new uint8_t[_totalPacketSize];
		size_t setSize = rawDataLen < _totalPacketSize ? rawDataLen : _totalPacketSize;
		// Copy data into our buffer
		memset(_rawData, 0, setSize);
		memcpy(_rawData, rawData, setSize);
		// Apply byte-swapping on a word-by-word basis
		if (byteSwapped)
		{
			byteswapRawData();
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
				timestampFrac = ((uint64_t)rawDataWord(currentWord) << 32)
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

	Vita49Packet::Vita49Packet(const Vita49Packet& src)
	{
		vitaType = src.vitaType;
		payloadSize = src.payloadSize;
		vitaHeaderSize = src.vitaHeaderSize;
		vitaTailSize = src.vitaTailSize;
		byteSwapped = src.byteSwapped;
		iqSwapped = src.iqSwapped;
		samples = src.samples;
		frameAlignmentWord = src.frameAlignmentWord;
		frameCount = src.frameCount;
		frameSize = src.frameSize;
		packetType = src.packetType;
		hasClassId = src.hasClassId;
		hasTrailer = src.hasTrailer;
		timestampIntType = src.timestampIntType;
		timestampFracType = src.timestampFracType;
		packetCount = src.packetCount;
		packetSize = src.packetSize;
		streamId = src.streamId;
		organizationallyUniqueId = src.organizationallyUniqueId;
		informationClassCode = src.informationClassCode;
		packetClassCode = src.packetClassCode;
		timestampInt = src.timestampInt;
		timestampFrac = src.timestampFrac;
		frameTrailerWord = src.frameTrailerWord;
		_totalPacketSize = src._totalPacketSize;
		_rawData = new uint8_t[_totalPacketSize];
		memcpy(_rawData, src._rawData, _totalPacketSize);
		sampleData = new int16_t[samples * 2];
		memcpy(sampleData, src.sampleData, samples * 2 * sizeof(int16_t));
	}

	Vita49Packet& Vita49Packet::operator=(const Vita49Packet& src)
	{
		if ( this != &src )
		{
			vitaType = src.vitaType;
			payloadSize = src.payloadSize;
			vitaHeaderSize = src.vitaHeaderSize;
			vitaTailSize = src.vitaTailSize;
			byteSwapped = src.byteSwapped;
			iqSwapped = src.iqSwapped;
			samples = src.samples;
			frameAlignmentWord = src.frameAlignmentWord;
			frameCount = src.frameCount;
			frameSize = src.frameSize;
			packetType = src.packetType;
			hasClassId = src.hasClassId;
			hasTrailer = src.hasTrailer;
			timestampIntType = src.timestampIntType;
			timestampFracType = src.timestampFracType;
			packetCount = src.packetCount;
			packetSize = src.packetSize;
			streamId = src.streamId;
			organizationallyUniqueId = src.organizationallyUniqueId;
			informationClassCode = src.informationClassCode;
			packetClassCode = src.packetClassCode;
			timestampInt = src.timestampInt;
			timestampFrac = src.timestampFrac;
			frameTrailerWord = src.frameTrailerWord;
			_totalPacketSize = src._totalPacketSize;
			if ( sampleData != NULL )
				delete sampleData;
			sampleData = new int16_t[samples * 2];
			memcpy(sampleData, src.sampleData, samples * 2 * sizeof(int16_t));
			if ( _rawData != NULL )
				delete _rawData;
			_rawData = new uint8_t[_totalPacketSize];
			memcpy(_rawData, src._rawData, _totalPacketSize);
		}
		return *this;
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

	void Vita49Packet::byteswapRawData(void)
	{
		uint32_t tmp;
		for (int i = 0; i < (int)_totalPacketSize; i += sizeof(uint32_t) )
		{
			tmp = (uint32_t)__builtin_bswap32(*((int32_t*)(_rawData + i)));
			memcpy((uint32_t*)(_rawData + i), &tmp, sizeof(uint32_t));
		}
	}

#define VALUE_DEC(val) std::dec << val
#define VALUE_HEX(val,bits) "0x" << std::hex << std::setw(bits/4) << std::setfill('0') << val
#define VALUE_DEC_HEX(val,bits) VALUE_DEC(val) << " (" << VALUE_HEX(val,bits) << ")"

	std::string Vita49Packet::dump()
	{
		std::ostringstream oss;
		if ( vitaType == 0 )
		{
			oss << "I/Q PACKET\n";
		} else if ( vitaType == 551 ) {
			oss << "NDR551 Packet\n";
		} else {
			oss << "VITA 49 PACKET\n"
//				<< "    raw=" << rawDataHex() << "\n"
				<< "    type=" << vitaType << "\n"
				<< "    Frame Details\n"
				<< "        count=" << VALUE_DEC_HEX(frameCount, 32) << "\n"
				<< "        size=" << VALUE_DEC_HEX(frameSize, 32) << "\n"
				<< "        align word=" << VALUE_DEC_HEX(frameAlignmentWord, 32) << "\n";
			if ( hasTrailer )
				oss << "        trail word=" << VALUE_DEC_HEX(frameTrailerWord, 32) << "\n";
			oss << "    Packet Details\n"
				<< "        type=" << VALUE_DEC_HEX(packetType, 32) << "\n"
				<< "        count=" << VALUE_DEC_HEX(packetCount, 32) << "\n"
				<< "        size=" << VALUE_DEC_HEX(packetSize, 32) << "\n"
				<< "        timestamp types: int=" << VALUE_DEC_HEX(timestampIntType, 32)
												   << " frac=" << VALUE_DEC_HEX(timestampFracType, 32)
												   << "\n";
			if ( (packetType == 1) || (packetType == 3) )
			{
				oss << "        stream ID=" << VALUE_DEC_HEX(streamId, 32) << "\n";
			}
			if ( hasClassId )
			{
				oss << "        class ID: OUI=" << VALUE_DEC_HEX(organizationallyUniqueId, 32)
												<< " ICC=" << VALUE_DEC_HEX(informationClassCode, 32)
												<< " PCC=" << VALUE_DEC_HEX(packetClassCode, 32)
												<< "\n";

			}
			if ( timestampIntType > 0 )
			{
				oss << "        timestamp: int=" << VALUE_DEC_HEX(timestampInt, 32);
				if ( timestampFracType > 0 )
					oss << " frac=" << VALUE_DEC_HEX(timestampFrac, 64);
				oss << "\n";
			}
		}
		oss << "    Payload Details\n"
			<< "        samples=" << VALUE_DEC(samples) << "\n";
		for (int sample = 0; sample < 10; sample++)
		{
			oss << "        samp" << std::setw(3) << std::setfill('0') << sample
				<< ": i=" << VALUE_HEX(getSampleI(sample), 16)
				<< " q=" << VALUE_HEX(getSampleQ(sample), 16)
				<< "\n";
		}
		oss << "[END PACKET]";
		return oss.str();
	}

} /* namespace CyberRadio */
