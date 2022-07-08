/* -*- c++ -*- */
/*
 * Copyright 2022 g3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "single_pole_iir_filter_ff_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace CyberRadio {
  using input_type = float;
  using output_type = float;
  single_pole_iir_filter_ff::sptr
  single_pole_iir_filter_ff::make(double alpha, unsigned int vlen, bool resetOnAlphaChange)
  {
      return gnuradio::make_block_sptr<single_pole_iir_filter_ff_impl>(
          alpha, vlen, resetOnAlphaChange);
  }


  /*
  * The private constructor
  */
  single_pole_iir_filter_ff_impl::single_pole_iir_filter_ff_impl(double alpha,
                                                                unsigned int vlen,
                                                                bool resetOnAlphaChange)
      : gr::sync_block("single_pole_iir_filter_ff",
                      gr::io_signature::make(
                          1, 1, sizeof(input_type) * vlen),
                      gr::io_signature::make(
                          1, 1, sizeof(output_type) * vlen)),
      d_vlen(vlen), 
      d_resetOnAlphaChange(resetOnAlphaChange), 
      d_iir(vlen)
  {
    set_taps(alpha);
    //Create input port
    message_port_register_in(pmt::mp("reset"));
    set_msg_handler(pmt::mp("reset"), boost::bind(&single_pole_iir_filter_ff_impl::rxResetMsg, this, _1));
  }

  void
  single_pole_iir_filter_ff_impl::set_taps(double alpha)
  {
    for(unsigned int i = 0; i < d_vlen; i++) {
      d_iir[i].set_taps(alpha);
      if (d_resetOnAlphaChange) {
        d_iir[i].reset();
      }
    }
  }

  void
  single_pole_iir_filter_ff_impl::reset(bool reset)
  {
    if (reset) {
      for(unsigned int i = 0; i < d_vlen; i++) {
        d_iir[i].reset();
      }
    }
  }

  void
  single_pole_iir_filter_ff_impl::rxResetMsg(pmt::pmt_t msg)
  {
    pmt::pmt_t tag = pmt::car(msg);
    pmt::pmt_t value = pmt::cdr(msg);
    this->reset(true);
  }

  /*
  * Our virtual destructor.
  */
  single_pole_iir_filter_ff_impl::~single_pole_iir_filter_ff_impl() {}

  int single_pole_iir_filter_ff_impl::work(int noutput_items,
                                          gr_vector_const_void_star& input_items,
                                          gr_vector_void_star& output_items)
  {
      const float* in = (const float*)input_items[0];
      float* out = (float*)output_items[0];
      unsigned int vlen = d_vlen;

      if (d_vlen == 1) {
          for (int i = 0; i < noutput_items; i++) {
              out[i] = d_iir[0].filter(in[i]);
          }
      } else {
          for (int i = 0; i < noutput_items; i++) {
              for (unsigned int j = 0; j < vlen; j++) {
                  *out++ = d_iir[j].filter(*in++);
              }
          }
      }
      return noutput_items;
  }

} /* namespace CyberRadio */
} /* namespace gr */
