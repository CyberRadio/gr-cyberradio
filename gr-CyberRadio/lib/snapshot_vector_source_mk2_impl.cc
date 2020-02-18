/* -*- c++ -*- */
/*
 * Copyright 2019 gr-CyberRadio author.
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
#include "snapshot_vector_source_mk2_impl.h"
#include <sys/uio.h>


namespace gr {
  namespace CyberRadio {

    snapshot_vector_source_mk2::sptr
    snapshot_vector_source_mk2::make(const std::string radio_type, const std::string &ip, unsigned int port, unsigned int block_size, unsigned int block_rate,bool demod)
    {
      return gnuradio::get_initial_sptr
        (new snapshot_vector_source_mk2_impl(radio_type, ip, port, block_size, block_rate, demod));
    }

    /*
     * The private constructor
     */
    snapshot_vector_source_mk2_impl::snapshot_vector_source_mk2_impl(const std::string radio_type, const std::string &ip, unsigned int port, unsigned int block_size, unsigned int block_rate, bool demod)
      : gr::sync_block("snapshot_vector_source_mk2",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(float)*block_size)),
    d_radio_type(radio_type),
    d_ip(ip),
    d_port(port),
    d_block_size(block_size),
    d_block_rate(block_rate),
    d_tag_frame(false),
    thisCount(0),
    lastCount(0),
    d_byte_swap(false),
    d_iq_swap(true),
    initializing(true),
    running(false),
    d_demod(demod),
    _parseHeader(_parseHeaderNull)
    {
      if ( (d_radio_type.compare("ndr308")==0) ||
  		     (d_radio_type.compare("ndr308-ts")==0) ||
               (d_radio_type.compare("ndr651")==0) ||
               (d_radio_type.compare("ndr804")==0) ||
               (d_radio_type.compare("ndr804-ptt")==0) ||
               (d_radio_type.compare("ndr810")==0) ) {
  			this->set_iqSwap(true);
  			this->set_byteSwap(false);
  			this->d_samples_per_frame = 1024;

  			if (this->d_tag_frame) {
  				this->_parseHeader = this->_parseHeaderNdr308;
  			}
  			this->rxVec[0].iov_base = new char[ sizeof(struct Vita49Header) ];
  			this->rxVec[0].iov_len = sizeof(struct Vita49Header);

  			this->rxVec[2].iov_base = new char[ sizeof(struct Vita49Trailer) ];
  			this->rxVec[2].iov_len = sizeof(struct Vita49Trailer);
  		} else if ( (d_radio_type.compare("ndr301")==0) ||
  				(d_radio_type.compare("ndr301-ptt")==0) ) {
  			this->set_iqSwap(true);
  			this->set_byteSwap(false);
  			this->d_samples_per_frame = 2048;

  			if (this->d_tag_frame) {
  				this->_parseHeader = this->_parseHeaderNdr308;
  			}

  			this->rxVec[0].iov_base = new char[ sizeof(struct Vita49Header) ];
  			this->rxVec[0].iov_len = sizeof(struct Vita49Header);

  			this->rxVec[2].iov_base = new char[ sizeof(struct Vita49Trailer) ];
  			this->rxVec[2].iov_len = sizeof(struct Vita49Trailer);
  		} else if ((d_radio_type.compare("ndr364")==0)||(d_radio_type.compare("ndr354")==0)) {
  			this->set_iqSwap(false);
  			this->set_byteSwap(true);

  			this->d_samples_per_frame = 1024;

  			this->rxVec[0].iov_base = new char[ 4*5 ];
  			this->rxVec[0].iov_len = 4*5;

  			this->rxVec[2].iov_base = new char[ 1 ];
  			this->rxVec[2].iov_len = 1;
  		} else if ((d_radio_type.compare("ndr551")==0)||(d_radio_type.compare("ndr358")==0)||(d_radio_type.compare("ndr357")==0)) {
  			this->set_iqSwap(false);
  			this->set_byteSwap(true);
        if (this->d_demod){
          this->d_samples_per_frame = 256;
        }
        else {
           this->d_samples_per_frame = 1024;
        }
  			//~ this->_parseHeader = this->_parseHeaderNdr551;

  			this->rxVec[0].iov_base = new char[ 48 ];
  			this->rxVec[0].iov_len = 48;

  			this->rxVec[2].iov_base = new char[ sizeof(struct Vita49Trailer) ];
  			this->rxVec[2].iov_len = sizeof(struct Vita49Trailer);
  		} else {
  			perror("Unknown radio type");
  			throw "Unknown radio type";
  		}

  		this->rxVec[1].iov_base = new int16_t[2*this->d_samples_per_frame];
  		this->rxVec[1].iov_len = sizeof(int16_t)*2*this->d_samples_per_frame;

  		for (int i=0; i<3; i++) {
  			std::cout << "rxVec[" << i << "].iov_len = " << rxVec[i].iov_len << std::endl;
  			this->expectedRxSize += rxVec[i].iov_len;
  		}
  		this->set_bswap_flags();

  		// Save GRC Paramters
  		this->ip = std::string(ip);
  		this->port = port;
  		this->block_size = block_size;
  		this->block_rate = block_rate;
  		this->packets_per_block = this->block_size/this->d_samples_per_frame;
      if(this->packets_per_block <= 0)
      {
        perror("Packets per block less than zero");
  			throw "Packets per block less than zero";
      }
  		// Init a huge vector that will hold all the samples
      this->sampleVector = std::vector<float> (block_size);
      // if(this->d_demod)
      // {
      //   this->sampleVector = std::vector<float> (block_size);
      // }
      // else
      // {
  		//     this->sampleVector = std::vector<gr_complex> (block_size);
      // }
  		//Create input port
  		message_port_register_in(pmt::mp("control"));
  		set_msg_handler(pmt::mp("control"), boost::bind(&snapshot_vector_source_mk2_impl::rxControlMsg, this, _1));

  		//Create output ports
  		message_port_register_out(pmt::mp("status"));
    }

    void snapshot_vector_source_mk2_impl::rxControlMsg(pmt::pmt_t msg) {
    	pmt::pmt_t tag = pmt::car(msg);
    	pmt::pmt_t value = pmt::cdr(msg);
    	std::cout << "tag = " << tag << std::endl;
    	std::cout << "value = " << value << std::endl;
    	txStatusMsg();
    }

    void snapshot_vector_source_mk2_impl::txStatusMsg(void) {
    	pmt::pmt_t msg = pmt::cons(pmt::intern("status"), pmt::PMT_NIL);
    	message_port_pub(pmt::mp("status"), msg);
    }

    bool snapshot_vector_source_mk2_impl::start(void) {
  		this->initializing = false;
  		this->running = true;

  		// Init block counting and prebuffering state
  		this->stream_counter = 0;
  		this->program_starting = true; // We have to pre buffer some data for gnuradio
  		this->sock_fd = this->initSocket("0.0.0.0", port); // create recv socket
  		if (this->sock_fd < 0) {
  			perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max is set to 268435456");
  			throw "Socket Creation Error";
  		}

  		return true;
  	}

      bool snapshot_vector_source_mk2_impl::stop(void) {
  		this->running = false;
  		return true;
  	}

    int snapshot_vector_source_mk2_impl::initSocket(const std::string ip, unsigned short port)
    {

        // /proc/sys/net/core/rmem_max holds this value must be >= recv_buffer_size
        // linux kernel receiver buffer size. this is not to be confused with the size of this class' ring buffer.
        unsigned long recv_buffer_size = 268435456; // 256 MB

        int sockfd;
        struct sockaddr_in myaddr;
        memset((char *)&myaddr, 0, sizeof(myaddr));
        myaddr.sin_family = AF_INET;
        myaddr.sin_addr.s_addr = inet_addr(ip.c_str());
        myaddr.sin_port = htons(port);

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

        /* Set recv buffer size */
        //~ if (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size, sizeof(unsigned long long)) == -1) {
            //~ perror("couldn't set recv buf size.");
            //~ return -1;
        //~ }

        while (setsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &recv_buffer_size, sizeof(unsigned long long)) == -1) {
            std::cerr << "Couldn't set recv buf size = " << recv_buffer_size << "." << std::endl;
            recv_buffer_size <<= 1;
        }

        /* Verify this sock opt took */
        unsigned long long check_size = 0;
        unsigned int arg_len = sizeof(check_size);
        getsockopt(sockfd, SOL_SOCKET, SO_RCVBUF, &check_size, &arg_len);
        if (check_size != 2*recv_buffer_size) {
            fprintf(stderr, "ERROR: set recv buf size, but it is incorrect in kernel. check max limit in /proc/sys/net/core/rmem_max\n");
            return -1;
        }

        /* Bind the socket */
        if (bind(sockfd, (struct sockaddr *)&myaddr, sizeof(myaddr)) < 0) {
            perror("bind failed");
            return -1;
        }

        /* Our socket was correctly created */
        return sockfd;

    }

    void snapshot_vector_source_mk2_impl::pause()
    {
        // Close our recv socket
        close(this->sock_fd);
        //~ printf("\n");

        // Sleep
        if (this->block_rate>0) {
          usleep(950000/this->block_rate);
        }

        // Open a new socket
        this->sock_fd = this->initSocket(this->ip, this->port);
        if (this->sock_fd < 0) {
            perror("Could not create socket.  Check that /proc/sys/net/core/rmem_max is set to 268435456");
            throw "Socket Creation Error";
        }
    }

    /*
     * Our virtual destructor.
     */
    snapshot_vector_source_mk2_impl::~snapshot_vector_source_mk2_impl()
    {
    }

    int
    snapshot_vector_source_mk2_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      // Declare complex output buffer
      // if (this->d_demod)
      // {
      //   float *out = (float *) output_items[0];
      // }
      // else
      // {
      //   gr_complex *out = (gr_complex *) output_items[0];
      // }
      float *out = (float *) output_items[0];
      // Recv a packet
      //~ recv(this->sock_fd, rxbuff, sizeof(Ndr308Frame), 0);
      int rxSize = readv(this->sock_fd, this->rxVec, 3);
      // make sure the packet was big enough to be a data packet.
      // Ignore Context Packets
      if (rxSize > 1000){
          // Copy IQ data to output
          if (this->d_bswap32) {
              volk_32u_byteswap((uint32_t*)(this->rxVec[1].iov_base), this->d_samples_per_frame);
          }
          if (this->d_bswap16) {
              volk_16u_byteswap((uint16_t*)(this->rxVec[1].iov_base), 2*this->d_samples_per_frame);
          }
          volk_16i_s32f_convert_32f((float *)((uint8_t*)this->sampleVector.data() +  this->stream_counter*this->d_samples_per_frame*sizeof(gr_complex)), (int16_t *)(this->rxVec[1].iov_base), 32768.0, 2*this->d_samples_per_frame);

          if (this->d_tag_frame) {
          //Decode the Vita49 header
              _parseHeader((char *)(this->rxVec[0].iov_base), this->rxVec[0].iov_len);
          }

          // Increment our counter of packets received
          this->stream_counter++;

          // Check to see if it's time to sleep
          if (this->stream_counter >= this->packets_per_block) {
              this->stream_counter = 0;
              if (this->block_rate>0) {
              this->pause();
          }

              // Copy Sample Vector to output vector
              memcpy(out, this->sampleVector.data(), this->block_size*sizeof(float));

              return 1;
          }
      }
      else
      {
         // std::cout << "Detected smaller packet!" << std::endl;
         if (this->d_bswap32) {
             volk_32u_byteswap((uint32_t*)(this->rxVec[1].iov_base), this->d_samples_per_frame);
         }
         if (this->d_bswap16) {
             volk_16u_byteswap((uint16_t*)(this->rxVec[1].iov_base), 2*this->d_samples_per_frame);
         }

         volk_16i_s32f_convert_32f((float *)((uint8_t*)this->sampleVector.data() +  this->stream_counter*this->d_samples_per_frame*sizeof(float)), (int16_t *)(this->rxVec[1].iov_base), 16384.0, this->d_samples_per_frame);

         this->stream_counter++;
         if (this->stream_counter >= this->packets_per_block) {
             this->stream_counter = 0;
             if (this->block_rate>0) {
             this->pause();
           }
         memcpy(out, this->sampleVector.data(), this->block_size*sizeof(float));

         return 1;
         }
      // We need more samples
      }
      return 0;
    }

    void snapshot_vector_source_mk2_impl::set_iqSwap(bool iqSwap) {
      if (this->d_iqSwap != iqSwap) {
        this->d_iqSwap = iqSwap;
        this->set_bswap_flags();
      }
    }

    void snapshot_vector_source_mk2_impl::set_byteSwap(bool byteSwap) {
    if (this->d_byteSwap != byteSwap) {
      this->d_byteSwap = byteSwap;
      this->set_bswap_flags();
      }
    }

  /*
   * if (byteSwap and iqSwap)
   *     volk_32u_byteswap
   * elif (byteswap and (not iqSwap))
   *     volk_16u_byteswap
   * elif ((not byteswap) and iqSwap)
   *     volk_32u_byteswap
   *     volk_16u_byteswap
   *
   *  byteSwap | iqSwap | volk_32u_byteswap | volk_16u_byteswap
   * ----------|--------|-------------------|-------------------
   *     0     |   0    |        0          |        0
   *     0     |   1    |        1          |        1
   *     1     |   0    |        0          |        1
   *     1     |   1    |        1          |        0
   *
   * volk_32u_byteswap = iqSwap
   * volk_16u_byteswap = byteSwap XOR iqSwap
   */
    void snapshot_vector_source_mk2_impl::set_bswap_flags(void) {
      this->d_bswap32 = this->d_iqSwap;
      this->d_bswap16 = this->d_byteSwap ^ this->d_iqSwap;
    }










  } /* namespace CyberRadio */
} /* namespace gr */
