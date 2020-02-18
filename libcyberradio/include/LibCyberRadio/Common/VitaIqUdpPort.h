/* -*- c++ -*- */
/***************************************************************************
 * \file VitaIqUdpPort.h
 *
 * \brief UDP port for handling incoming VITA 49 or I/Q data.
 *
 * \author DA
 * \copyright 2016 CyberRadio Solutions, Inc.
 */

#ifndef INCLUDED_LIBCYBERRADIO_VITAIQUDPPORT_H_
#define INCLUDED_LIBCYBERRADIO_VITAIQUDPPORT_H_

#include "LibCyberRadio/Common/Debuggable.h"
#include <boost/asio.hpp>
#include <boost/format.hpp>
#include <string>

/*!
 * \brief Provides programming elements for controlling CyberRadio Solutions products.
 */
namespace LibCyberRadio
{
    /*
     * Class that grabs channel I/Q data from a UDP port.
     */
    class VitaIqUdpPort : public Debuggable
    {
        public:
            VitaIqUdpPort(const std::string& host = "0.0.0.0",
                    int port = 40001,
                    int packet_size = 8192,
                    bool debug = false);
            ~VitaIqUdpPort();
            void read_data();
            void clear_buffer();
            bool is_packet_ready() const;

        public:
            std::string host;
            int port;
            int packet_size;
            bool connected;    // are we connected?
            boost::asio::ip::udp::socket *socket;
            boost::asio::ip::udp::endpoint endpoint;
            boost::asio::io_service io_service;
            unsigned char* recv_buffer;
            int bytes_recvd;
    };

} /* namespace LibCyberRadio */

#endif /* INCLUDED_LIBCYBERRADIO_VITAIQUDPPORT_H_ */
