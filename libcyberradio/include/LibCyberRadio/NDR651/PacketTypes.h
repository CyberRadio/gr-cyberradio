/***************************************************************************
 * \file PacketTypes.h
 *
 * \brief Defines data structures for handling VITA 49-formatted data packets.
 *
 * \author NH
 * \copyright Copyright (c) 2015-2021 CyberRadio Solutions, Inc.
 *
 */

#ifndef INCLUDED_LIBCYBERRADIO_NDR651_PACKETTYPES_H_
#define INCLUDED_LIBCYBERRADIO_NDR651_PACKETTYPES_H_

#include <linux/if_ether.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <stdint.h>

#define SAMPLES_PER_FRAME 1024

#define VRLP 0x56524c50
#define VEND 0x56454e44

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /*!
     * \brief Provides programming elements for controlling the CyberRadio Solutions
     *    NDR651 radio.
     */
    namespace NDR651
    {

        /*!
         * \brief VITA 49 frame header information.
         */
        struct Vita49Header {
                uint32_t frameStart;     //!< Frame start word (ASCII string "VRLP")
                uint32_t frameSize:20;   //!< Frame size, in 32-bit words
                uint32_t frameCount:12;  //!< Frame Count
                uint16_t packetSize;     //!< Packet size, in 32-bit words
                uint16_t packetCount:4;  //!< Packet counter
                uint16_t TSF:2;          //!< Timestamp fractional field format
                uint16_t TSI:2;          //!< Timestamp integer field format
                uint16_t RSVD:2;         //!< RESERVED
                uint16_t T:1;            //!< Frame trailer present indicator
                uint16_t C:1;            //!< Class ID field present indicator
                uint16_t packetType:4;   //!< Packet type
                uint32_t streamId;       //!< Stream ID
                /*!
                 * \brief Class ID Field Part 1
                 *
                 * Contains the Organizationally Unique Identifier (OUI).
                 */
                uint32_t classId1;
                /*!
                 * \brief Class ID Field Part 2
                 *
                 * Bits 16-31 contain the Information Class Code (ICC).
                 * Bits 0-15 contain the Packet Class Code (PCC).
                 */
                uint32_t classId2;
                uint32_t timeSeconds;    //!< Timestamp integer field
                uint32_t timeFracSecMSB; //!< Timestamp fractional field, MSW
                uint32_t timeFracSecLSB; //!< Timestamp fractional field, LSW
        } __attribute__((packed));

        /*!
         * \brief VITA 49 frame payload information.
         */
        struct Payload {
                int16_t samples[2*SAMPLES_PER_FRAME];  //!< Interleaved I and Q samples
        } __attribute__((packed));

        /*!
         * \brief VITA 49 frame trailer information.
         */
        struct Vita49Trailer {
                uint32_t frameEnd;          //!< Frame end word (ASCII string "VEND")
        } __attribute__((packed));

        /*!
         * \brief VITA 49 transmit-over-UDP frame information.
         */
        struct TxFrame {
                struct ethhdr eth;          //!< Ethernet header
                struct iphdr ip;            //!< IP header
                struct udphdr udp;          //!< UDP header
                struct Vita49Header v49;    //!< VITA 49 frame header
                struct Payload payload;     //!< VITA 49 payload
                struct Vita49Trailer vend;  //!< VITA 49 frame trailer
        } __attribute__((aligned));

        /*!
         * \brief Transmit status information.
         */
        struct TxStatusPayload {
                uint32_t contextIndicator:31;  //!< Context indicator
                uint32_t CI:1;  //!< Change Indicator

                uint32_t spaceAvailable;    //!< Space available

                uint32_t overrunCount:7;    //!< Overrun count
                uint32_t overrunFlag:1;     //!< Overrun flag
                uint32_t underrunCount:7;   //!< Underrun count
                uint32_t underrunFlag:1;    //!< Underrun flag
                uint32_t packetLossCount:7; //!< Packet loss count
                uint32_t packetLossFlag:1;  //!< Packet loss flag
                uint32_t fullFlag:1;        //!< Full flag
                uint32_t emptyFlag:1;       //!< Empty flag
                uint32_t RSVD:6;            //!< RESERVED

                uint32_t PF:1;               //!< Filling trigger
                uint32_t PE:1;               //!< Emptying trigger
                uint32_t PP:1;               //!< Periodic notification
                uint32_t PAD:29;               //!< Padding
        } __attribute__((packed));;

        /*!
         * \brief Transmit status frame information.
         */
        struct TxStatusFrame {
                struct Vita49Header v49;        //!< VITA 49 frame header
                struct TxStatusPayload status;  //!< Transmit status information
                struct Vita49Trailer vend;      //!< VITA 49 frame trailer
        };

    }

}

#endif /* INCLUDED_LIBCYBERRADIO_NDR651_PACKETTYPES_H_ */
