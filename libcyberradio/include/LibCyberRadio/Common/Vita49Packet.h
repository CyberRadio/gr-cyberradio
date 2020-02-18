/* -*- c++ -*- */
/***************************************************************************
 * \file Vita49Packet.h
 *
 * \brief VITA 49 packet decoder.
 *
 * \author DA
 * \copyright 2015 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_LIBCYBERRADIO_VITA49PACKET_H
#define INCLUDED_LIBCYBERRADIO_VITA49PACKET_H

#include <stddef.h>
#include <stdint.h>
#include <string>


/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /*!
     * \ingroup CyberRadio
     *
     * \brief Decodes a VITA 49 or I/Q data packet.
     *
     * \details
     * The Vita49Packet class is used to decode VITA 49 or raw I/Q data
     * coming from an NDR-class radio.
     *
     * This class is designed to be as flexible as possible in dealing
     * with data streams, since each NDR-class radio varies in how it
     * packages data streams.
     */
    class Vita49Packet
    {
        public:
            /*!
             * \brief Constructs a Vita49Packet object.
             *
             * \param vitaType The VITA 49 enable option value.  The range of valid values
             *     depends on the radio, but 0 always disables VITA 49 formatting.  In that
             *     case, the data format is raw I/Q.
             * \param payloadSize The VITA 49 or I/Q payload size for the radio, in bytes.
             *     If VITA 49 output is disabled, then this parameter provides the total
             *     size of all raw I/Q data transmitted in a single packet.
             * \param vitaHeaderSize The VITA 49 header size for the radio, in bytes.
             *     If VITA 49 output is disabled, then this parameter is ignored.
             * \param vitaTailSize The VITA 49 tail size for the radio, in bytes.
             *     If VITA 49 output is disabled, then this parameter is ignored.
             * \param byteSwapped Whether the bytes in the packet are byte-swapped with
             *     respect to the endianness employed by the host operating system.
             * \param iqSwapped Whether I and Q data in the payload are swapped.
             * \param rawData A pointer to the buffer of raw data received from the radio.
             * \param rawDataLen The length of the raw data buffer.
             */
            Vita49Packet(int vitaType,
                    size_t payloadSize,
                    size_t vitaHeaderSize,
                    size_t vitaTailSize,
                    bool byteSwapped,
                    bool iqSwapped,
                    unsigned char* rawData = NULL,
                    size_t rawDataLen = 0);
            /*!
             * \brief Destroys a Vita49Packet object.
             */
            virtual ~Vita49Packet();
            /*!
             * \brief Copy constructor.
             *
             * \param src The object to copy.
             */
            Vita49Packet(const Vita49Packet& src);
            /*!
             * \brief Assignment operator.
             *
             * \param src The object to assign properties from.
             */
            virtual Vita49Packet& operator=(const Vita49Packet& src);
            /*!
             * \brief Indicates whether the packet data is in VITA 49 format.
             *
             * \return True if the data is VITA 49, False otherwise.
             */
            bool isVita49() const;
            /*!
             * \brief Gets the I component of a given data sample.
             *
             * \param sample The sample number (0-based).
             * \return The I component of the sample.  This method will return 0 if the
             *     sample number is out of bounds.
             */
            int16_t getSampleI(int sample);
            /*!
             * \brief Gets the Q component of a given data sample.
             *
             * \param sample The sample number (0-based).
             * \return The Q component of the sample.  This method will return 0 if the
             *     sample number is out of bounds.
             */
            int16_t getSampleQ(int sample);
            /*!
             * \brief Gets the raw data in hex-string format.
             *
             * \return A hex string representing the raw data.
             */
            std::string rawDataHex() { return rawDataBufferHex(_rawData, _totalPacketSize); };
            /*!
             * \brief Gets a string dump of the contents of the data packet.
             *
             * \return A string describing the contents of the packet.
             */
            std::string dump();

        public:
            // Packet structure configuration parameters
            int vitaType;
            size_t payloadSize;
            size_t vitaHeaderSize;
            size_t vitaTailSize;
            bool byteSwapped;
            bool iqSwapped;
            // Decoded from packet structure
            int samples;
            uint32_t frameAlignmentWord;
            int frameCount;
            int frameSize;
            int packetType;
            int hasClassId;
            int hasTrailer;
            int timestampIntType;
            int timestampFracType;
            int packetCount;
            int packetSize;
            uint32_t streamId;
            int organizationallyUniqueId;
            int informationClassCode;
            int packetClassCode;
            uint32_t timestampInt;
            uint64_t timestampFrac;
            uint32_t frameTrailerWord;
            int16_t* sampleData;

        protected:
            uint32_t rawDataWord(int index);
            std::string rawDataBufferHex(unsigned char* buf, int length);
            void byteswapRawData(void);

        protected:
            // Raw data buffer
            uint8_t* _rawData;
            // Calculated quantities
            size_t _totalPacketSize;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_VITA49PACKET_H */
