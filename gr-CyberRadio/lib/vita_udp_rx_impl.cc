/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vita_udp_rx_impl.h"
#include <iostream>
#include <iomanip>

namespace gr {
  namespace CyberRadio {

    vita_udp_rx::sptr
    vita_udp_rx::make(const std::string &src_ip, unsigned short port, unsigned int header_byte_offset, int samples_per_packet, int bytes_per_packet, bool swap_bytes, bool swap_iq, bool tag_packets, bool vector_output, bool uses_v491, bool narrowband, bool debug)
    {
      return gnuradio::get_initial_sptr
        (new vita_udp_rx_impl(src_ip, port, header_byte_offset, samples_per_packet, bytes_per_packet, swap_bytes, swap_iq, tag_packets, vector_output, uses_v491, narrowband, debug));
    }

    /*
     * The private constructor
     */
    vita_udp_rx_impl::vita_udp_rx_impl(const std::string &src_ip, unsigned short port, unsigned int header_byte_offset, int samples_per_packet, int bytes_per_packet, bool swap_bytes, bool swap_iq, bool tag_packets, bool vector_output, bool uses_v491, bool narrowband, bool debug)
      : gr::sync_interpolator("vita_udp_rx",
              gr::io_signature::make(0, 0, 0),
//              gr::io_signature::make(1, 1, sizeof(gr_complex)), samples_per_packet),
			  gr::io_signature::make(0, 0, 0), 1),
		samples_per_packet(samples_per_packet),
		bytes_per_packet(bytes_per_packet),
		uses_v491(uses_v491),
    is_narrowband(narrowband),
		src_ip(src_ip),
		port(port),
		header_byte_offset(header_byte_offset),
		swap_bytes(swap_bytes),
		swap_iq(swap_iq),
		tag_packets(tag_packets),
		debug(debug),
		vector_output(vector_output)
    {
    	if (this->vector_output) {
    		this->set_output_signature(gr::io_signature::make(1, 1, this->samples_per_packet*sizeof(gr_complex)));
    		this->set_interpolation(1);
    	} else {
    		this->set_output_signature(gr::io_signature::make(1, 1, sizeof(gr_complex)));
    		this->set_interpolation(this->samples_per_packet);
    	}
      
		//Create input port
		message_port_register_in(pmt::mp("control"));
		set_msg_handler(pmt::mp("control"), boost::bind(&vita_udp_rx_impl::rxControlMsg, this, _1));

		//Create output ports
		message_port_register_out(pmt::mp("status"));

      // Create RX Buffer
      this->buffer = new uint8_t[this->bytes_per_packet];
   
    }

	void vita_udp_rx_impl::rxControlMsg(pmt::pmt_t msg) {
		std::cout << "****    vita_udp_rx_impl::rxControlMsg    ****" << std::endl;
		// What did we receive?
		pmt::pmt_t msgId = pmt::car(msg);
		pmt::pmt_t content = pmt::cdr(msg);
	}

    bool vita_udp_rx_impl::start()
    {
      // Init RX Socket
      std::cout << "Socket opening" << std::endl;
      this->sock_fd = this->initSocket(); // create recv socket
      if (this->sock_fd < 0) {
          perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max is set to 268435456");
          throw "Socket Creation Error";
      }
      bool ret = true;
      return ret;  
    }

    bool vita_udp_rx_impl::stop()
    {
      std::cout << "Socket closing" << std::endl;
      close(this->sock_fd);
      bool ret = true;
      return ret;
    }

    void vita_udp_rx_impl::tag_packet()
    {
      // Load stream offset and current packet header
      uint64_t tag_offset = nitems_written(0);
      pmt::pmt_t timestamp;
      pmt::pmt_t stream_id;
      if (this->uses_v491)
      {
          V49_308_Header *hdr = (V49_308_Header *)(this->buffer);
          // Create polymorphic type for timestamp
          timestamp = pmt::cons(pmt::from_long(hdr->int_timestamp),pmt::from_long(hdr->frac_timestamp_lsw));
          // Create polymorphic type for stream id
          stream_id = pmt::from_long(hdr->stream_id);
      }
      else
      {
          V49_No491_Header *hdr = (V49_No491_Header *)(this->buffer);
//          std::cout << "****    vita_udp_rx_impl::tag_packet packet_info = "
//                    << std::hex << std::setw(8) << std::setfill('0')
//                    << hdr->packet_info << "    ****" << std::endl;
          // Create polymorphic type for timestamp
          timestamp = pmt::cons(pmt::from_long(hdr->int_timestamp),pmt::from_long(hdr->frac_timestamp_lsw));
          // Create polymorphic type for stream id
          stream_id = pmt::from_long(hdr->stream_id);
      }

      // Hook the tag into the stream
      add_item_tag(0, tag_offset, pmt::intern("timestamp"), timestamp);
      add_item_tag(0, tag_offset, pmt::intern("stream_id"), stream_id);
    }


    int vita_udp_rx_impl::initSocket()
    {

        // /proc/sys/net/core/rmem_max holds this value must be >= recv_buffer_size
        // linux kernel receiver buffer size. this is not to be confused with the size of this class' ring buffer.
        unsigned long recv_buffer_size = 268435456; // 256 MB

        int sockfd;
        struct sockaddr_in myaddr;
        memset((char *)&myaddr, 0, sizeof(myaddr));
        myaddr.sin_family = AF_INET;
        myaddr.sin_addr.s_addr = inet_addr(this->src_ip.c_str());
        myaddr.sin_port = htons(this->port);

        /* Create a UDP Socket*/
        if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
            perror("cannot create socket\n");
            return -1;
        }

        /* Set socket to reuse address */
        int enable = 1;
        if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0) {
            perror("setsockopt SO_REUSEADDR call failed");
            return -1;
        }

        if (!is_narrowband) {
          /* Set recv buffer size */
          if (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size, sizeof(unsigned long long)) == -1) {
              perror("couldn't set recv buf size.");
              return -1;
          }
          /* Verify this sock opt took */
          unsigned long long check_size = 0;
          unsigned int arg_len = sizeof(check_size);
          getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &check_size, &arg_len);
          if (check_size != 2*recv_buffer_size) {
              fprintf(stderr, "ERROR: set recv buf size, but it is incorrect in kernel. check max limit in /proc/sys/net/core/rmem_max\n");
              return -1;
          }
        }

        /* Bind the socket */
        if (bind(sockfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
            perror("bind failed");
            return -1;
        }

        /* Our socket was correctly created */
        return sockfd;

    }

    /*
     * Our virtual destructor.
     */
    vita_udp_rx_impl::~vita_udp_rx_impl()
    {
      delete [] this->buffer;
    }

    int
    vita_udp_rx_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {

    	int noutput = 0;
      int nbytesRx = 0;
    	// Declare complex output buffer
      gr_complex *out = (gr_complex *) output_items[0];
      int numRx = 0;
      int maxNumRx=0;
      if (this->vector_output) {
    	  maxNumRx = noutput_items;
      } else {
    	  maxNumRx = noutput_items/this->samples_per_packet;
      }



//		while (noutput<=(noutput_items-this->samples_per_packet)) {
		for (numRx=0; numRx<maxNumRx; numRx++) {
			// Recv a packet
			memset(&pfd, 0, sizeof(pfd));
			pfd.fd = this->sock_fd;
			pfd.events = POLLIN | POLLERR;
			pfd.revents = 0;
			int poll_res = poll(&pfd, 1, RECV_TIMEOUT);

			if (poll_res > 0){
				// We've got some data
				nbytesRx = recv(this->sock_fd, this->buffer, this->bytes_per_packet, 0);
				if (nbytesRx==this->bytes_per_packet) {
                    // Byte-swap the header if needed so we can read it
                    if (this->swap_bytes)
                    {
                        volk_32u_byteswap((uint32_t*)(this->buffer), this->header_byte_offset / 4);
                    }
                    if (this->uses_v491)
                    {
                        V49_308_Header *hdr = (V49_308_Header *)(this->buffer);
//                        std::cout << "****    vita_udp_rx_impl::work() "
//                                  << "PACKET/491 p_i = "
//                                  << std::hex << std::setw(8) << std::setfill('0')
//                                  << hdr->packet_info << "    ****" << std::endl;
                    }
                    else
                    {
                        V49_No491_Header *hdr = (V49_No491_Header *)(this->buffer);
                        if (this->debug)
                            std::cout << "**** vita_udp_rx_impl("
                                      << this->src_ip << ","
                                      << this->port << ")::work() "
                                      << "PACKET/N491 p_i = "
                                      << std::hex << std::setw(8) << std::setfill('0')
                                      << hdr->packet_info << "    ****" << std::endl;
                    }
					// Copy IQ data to output
					short * IQ = (short *)((uint8_t *)buffer + this->header_byte_offset);
					// Swap bytes if requested
					if (this->swap_iq) {
						volk_32u_byteswap((uint32_t*)(IQ), this->samples_per_packet);
					}
					if (this->swap_bytes^this->swap_iq) {
						volk_16u_byteswap((uint16_t*)(IQ), 2*this->samples_per_packet);
					}
//					if (this->swap_bytes) {
//					  if (this->swap_iq) {
//						volk_32u_byteswap((uint32_t*)(IQ), this->samples_per_packet);
//					  } else {
//						volk_16u_byteswap((uint16_t*)(IQ), 2*this->samples_per_packet);
//					  }
//					} else if (this->swap_iq) {
//					  volk_32u_byteswap((uint32_t*)(IQ), this->samples_per_packet);
//					  volk_16u_byteswap((uint16_t*)(IQ), 2*this->samples_per_packet);
//					}

					volk_16i_s32f_convert_32f((float *)(out+noutput), IQ, 32768.0, 2*this->samples_per_packet);

					// Tag the incoming packet (ONLY FOR 308 and 651)
					if (this->tag_packets) {
					  this->tag_packet();
					}

					noutput += this->samples_per_packet;
//					break;
				} else {
//					std::cout << "received " << nbytesRx << " but expected " << this->bytes_per_packet << std::endl;
					break;
				}
			} else {
//				std::cout << "RECV TIMEOUT" << std::endl;
				break;
			}
		}

//		std::cout << (this->vector_output?numRx:noutput) << " " << noutput_items << std::endl;
		return this->vector_output?numRx:noutput;
		}
	} /* namespace CyberRadio */
} /* namespace gr */

