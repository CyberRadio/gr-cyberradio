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

#include "boost/bind.hpp"
#include "ndr651_sink_impl.h"
#include <gnuradio/io_signature.h>
#include <iostream>

using std::cout;
using std::endl;

namespace gr {
namespace CyberRadio {

ndr651_sink::sptr ndr651_sink::make(std::string hostname, unsigned int vlen,
                                    bool debug) {
  return gnuradio::get_initial_sptr(
      new ndr651_sink_impl(hostname, vlen, debug));
}

/*
 * The private constructor
 */
ndr651_sink_impl::ndr651_sink_impl(std::string hostname, unsigned int vlen,
                                   bool debug)
    : gr::sync_block("ndr651_sink",
                     gr::io_signature::make(1, 1, sizeof(gr_complex) * vlen),
                     gr::io_signature::make(0, 0, 0)),
      d_firstFrame(true), d_vlen(vlen) {
  this->txClient = new LibCyberRadio::NDR651::TXClient(hostname, debug);
  // this->txClient = NULL;
  // Create space for a TX Buffer
  this->txBuffer = new int16_t[2 * SAMPLES_PER_FRAME];
  // this->txBuffer = NULL;
  // cout << "\e[91m" << " Welcomes!" << __TIME__ << "\e[39m" << endl;
  // Create messaging port(s)
  // -- "freq" (input)
  message_port_register_in(pmt::mp("freq"));
  set_msg_handler(pmt::mp("freq"),
                  boost::bind(&ndr651_sink_impl::handleMsgFreq, this, _1));
  // message_port_register_out(pmt::mp("status"));
}

bool ndr651_sink_impl::setDUCParameters(unsigned int ducChannel,
                                        unsigned int ducRateIndex,
                                        unsigned int txChannel) {
  // cout << "\e[91m" << __FUNCTION__ << "  " << ducRateIndex << "\e[39m" <<
  // endl;
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setDUCParameters(ducChannel, ducRateIndex, txChannel);
  }
  return ret;
}

bool ndr651_sink_impl::setEthernetInterface(unsigned int tenGbeIndex,
                                            const std::string &txInterfaceName,
                                            unsigned short port) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setEthernetInterface(tenGbeIndex, txInterfaceName,
                                               port);
  }
  return ret;
}

bool ndr651_sink_impl::setDUCRateIndex(unsigned int ducRateIndex) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setDUCRateIndex(ducRateIndex);
  }
  return ret;
}

bool ndr651_sink_impl::setDUCFreq(double ducFreq) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setDUCFreq(ducFreq);
  }
  return ret;
}

bool ndr651_sink_impl::setDUCAtten(double ducAtten) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setDUCAtten(ducAtten);
  }
  return ret;
}

bool ndr651_sink_impl::setTxFreq(double txFreq) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setTxFreq(txFreq);
  }
  return ret;
}

bool ndr651_sink_impl::setTxAtten(double txAttenuation) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setTxAtten(txAttenuation);
  }
  return ret;
}

// bool setTxInversion(bool txInversion) { return true; };
bool ndr651_sink_impl::setTxInversion(bool txInversion) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->setTxInversion(txInversion);
  }
  return ret;
}

//	void ndr651_sink_impl::disableRF();

bool ndr651_sink_impl::pauseDUC(bool paused) {
  bool ret = false;
  if (this->txClient != NULL) {
    ret = this->txClient->pauseDUC(paused);
  }
  return ret;
}

/*
 * Our virtual destructor.
 */
ndr651_sink_impl::~ndr651_sink_impl() {
  // Why doesn't this actually get called
  if (this->txClient != NULL)
    delete this->txClient;
  if (this->txBuffer != NULL)
    delete[] this->txBuffer;
}

bool ndr651_sink_impl::start() {
  // Call the base-class start() method to ensure that this
  // block is ready to be part of a flowgraph
  bool ret = gr::sync_block::start();
  if (ret && (this->txClient != NULL)) {
    // Start the TX Client IFF block init was successful
    this->txClient->start();
  }
  return ret;
}

bool ndr651_sink_impl::stop() {
  // Stop the TX client
  if (this->txClient != NULL) {
    this->txClient->stop();
  }
  // Call the base-class stop() method
  bool ret = gr::sync_block::stop();
  return ret;
}

int ndr651_sink_impl::work(int noutput_items,
                           gr_vector_const_void_star &input_items,
                           gr_vector_void_star &output_items) {
  if (d_firstFrame) {
    d_firstFrame = false;
    std::cout << "noutput_items = " << noutput_items << std::endl;
    std::cout << "input_items.size() = " << input_items.size() << std::endl;
    std::cout << "noutput_items*d_vlen = " << noutput_items * d_vlen
              << std::endl;
  }

  int noi = input_items.size();
  gr_complex *floatSamples = (gr_complex *)input_items[0];

  for (int i = 0; i < noutput_items; i++) {
    // Sanity-check: Do this only if we have a buffer and a TX client!
    if ((this->txClient != NULL) && (this->txBuffer != NULL)) {
      // From gr_complex vector to short array
      volk_32f_s32f_convert_16i(this->txBuffer,
                                (const float *)(floatSamples + (i * d_vlen)),
                                32767, 2 * SAMPLES_PER_FRAME);
      // Shh, it's fine.
      volk_32u_byteswap((uint32_t *)(this->txBuffer), SAMPLES_PER_FRAME);
      volk_16u_byteswap((uint16_t *)(this->txBuffer), 2 * SAMPLES_PER_FRAME);
      // Fwoop
      this->txClient->sendFrame(this->txBuffer, SAMPLES_PER_FRAME);
    }
  }

  // I processed 1 gr_complex*SAMPLES_PER_FRAME vector
  return noutput_items;
}

/**
 * \internal
 * \brief Handles messages from the input port "freq".
 * \param msg Incoming message.  For this message to have any
 *    effect, this should be a pmt::cons object, where the key
 *    (car) is the string "freq" and the value (cdr) is the new
 *    frequency setting in Hz.
 */
void ndr651_sink_impl::handleMsgFreq(pmt::pmt_t msg) {
  //			std::cerr << "[ndr651_sink_impl::handleMsgFreq] "
  //					  << "ACTIVATED\n"
  //					  << "-- msg = " << msg
  //					  << std::endl;
  // Sanity check: Make sure that the incoming message is
  // a "pair" type.
  if (pmt::is_pair(msg)) {
    // Unpack the incoming message
    // * The key (setting) is the "car" of the incoming object,
    //   converted to a string.
    std::string setting = pmt::symbol_to_string(pmt::car(msg));
    // [DEBUG]
    //				std::cerr << "[ndr651_sink_impl::handleMsgFreq]
    //"
    //						  << "New Message\n"
    //						  << "-- Key: " << setting
    //						  << std::endl;
    // Handle this message only if it is a "freq" message
    if (setting == "freq") {
      // * The value (newValue) is the "cdr" of the incoming object,
      //   converted to a floating-point value.
      float newValue = pmt::to_float(pmt::cdr(msg));
      // * This value is in Hz, but the underlying radio control
      //   code needs transmit frequency in MHz
      newValue /= 1.0e6;
      //					std::cerr << "-- Freq Value: "
      //<< newValue << " MHz"
      //							  << std::endl;
      // * Set the transmit frequency.
      if (this->txClient != NULL) {
        //						std::cerr <<
        //"[ndr651_sink_impl::handleMsgFreq] "
        //								  << "Setting
        //TX Freq"
        //								  <<
        // std::endl;
        this->txClient->setTxFreq(newValue);
      }
    }
  }
}

} /* namespace CyberRadio */

} /* namespace gr */
