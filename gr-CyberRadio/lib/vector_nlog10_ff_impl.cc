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

#include "vector_nlog10_ff_impl.h"
#include <gnuradio/io_signature.h>
#include <volk/volk.h>

namespace gr {
namespace CyberRadio {

vector_nlog10_ff::sptr vector_nlog10_ff::make(float n, size_t vlen, float k) {
  return gnuradio::get_initial_sptr(new vector_nlog10_ff_impl(n, vlen, k));
}

/*
 * The private constructor
 */
vector_nlog10_ff_impl::vector_nlog10_ff_impl(float n, size_t vlen, float k)
    : gr::sync_block("vector_nlog10_ff",
                     io_signature::make(1, 1, sizeof(float) * vlen),
                     io_signature::make(1, 1, sizeof(float) * vlen)),
      //~ d_n(n/log2(10)),
      d_n(log2(10) / n), d_vlen(vlen), d_k(k) {}

/*
 * Our virtual destructor.
 */
vector_nlog10_ff_impl::~vector_nlog10_ff_impl() {}

int vector_nlog10_ff_impl::work(int noutput_items,
                                gr_vector_const_void_star &input_items,
                                gr_vector_void_star &output_items) {
  const float *in = (const float *)input_items[0];
  float *out = (float *)output_items[0];
  int noi = noutput_items * d_vlen;
  int size = noutput_items * d_vlen;
  float n = d_n;
  float k = d_k;

  volk_32f_log2_32f(out, in, noi);
  volk_32f_s32f_normalize(out, d_n, noi);
  return noutput_items;
}

} /* namespace CyberRadio */
} /* namespace gr */
