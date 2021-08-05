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

#ifndef INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H
#define INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H

#include <CyberRadio/vector_nlog10_ff.h>

namespace gr {
namespace CyberRadio {

class vector_nlog10_ff_impl : public vector_nlog10_ff {
private:
  float d_n;
  size_t d_vlen;
  float d_k;

public:
  vector_nlog10_ff_impl(float n, size_t vlen, float k);
  ~vector_nlog10_ff_impl();

  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_VECTOR_NLOG10_FF_IMPL_H */
