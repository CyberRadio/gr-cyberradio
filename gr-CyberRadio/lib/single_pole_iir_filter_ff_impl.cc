/* -*- c++ -*- */
/*
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
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

#include "single_pole_iir_filter_ff_impl.h"
#include <gnuradio/io_signature.h>

namespace gr {
namespace CyberRadio {

single_pole_iir_filter_ff::sptr
single_pole_iir_filter_ff::make(INPUT_ARGS_TYPE) {
  return gnuradio::get_initial_sptr(
      new single_pole_iir_filter_ff_impl(INPUT_ARGS_NO_TYPE));
}

/*
 * The private constructor
 */
single_pole_iir_filter_ff_impl::single_pole_iir_filter_ff_impl(INPUT_ARGS_TYPE)
    : gr::sync_block("single_pole_iir_filter_ff",
                     io_signature::make(1, 1, sizeof(float) * vlen),
                     io_signature::make(1, 1, sizeof(float) * vlen)),
      d_vlen(vlen), d_resetOnAlphaChange(resetOnAlphaChange), d_iir(vlen) {
  set_taps(alpha);
  // Create input port
  message_port_register_in(pmt::mp("reset"));
  set_msg_handler(
      pmt::mp("reset"),
      boost::bind(&single_pole_iir_filter_ff_impl::rxResetMsg, this, _1));
}

single_pole_iir_filter_ff_impl::~single_pole_iir_filter_ff_impl() {}

void single_pole_iir_filter_ff_impl::set_taps(double alpha) {
  for (unsigned int i = 0; i < d_vlen; i++) {
    d_iir[i].set_taps(alpha);
    if (d_resetOnAlphaChange) {
      d_iir[i].reset();
    }
  }
}

void single_pole_iir_filter_ff_impl::reset(bool reset) {
  if (reset) {
    for (unsigned int i = 0; i < d_vlen; i++) {
      d_iir[i].reset();
    }
  }
}

void single_pole_iir_filter_ff_impl::rxResetMsg(pmt::pmt_t msg) {
  pmt::pmt_t tag = pmt::car(msg);
  pmt::pmt_t value = pmt::cdr(msg);
  this->reset(true);
}

int single_pole_iir_filter_ff_impl::work(int noutput_items,
                                         gr_vector_const_void_star &input_items,
                                         gr_vector_void_star &output_items) {
  const float *in = (const float *)input_items[0];
  float *out = (float *)output_items[0];
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
};

} /* namespace CyberRadio */
} /* namespace gr */
