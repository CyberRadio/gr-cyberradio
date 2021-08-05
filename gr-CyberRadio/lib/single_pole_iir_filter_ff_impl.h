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

#ifndef INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H
#define INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H

#include <CyberRadio/single_pole_iir.h>
#include <CyberRadio/single_pole_iir_filter_ff.h>

namespace gr {
namespace CyberRadio {

class single_pole_iir_filter_ff_impl : public single_pole_iir_filter_ff {
private:
  bool d_resetOnAlphaChange;
  unsigned int d_vlen;
  std::vector<single_pole_iir<float, float, double>> d_iir;
  void rxResetMsg(pmt::pmt_t msg);

public:
  single_pole_iir_filter_ff_impl(INPUT_ARGS_TYPE);
  ~single_pole_iir_filter_ff_impl();

  void set_taps(double alpha);
  void reset(bool reset);

  // Where all the action really happens
  int work(int noutput_items, gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_IMPL_H */
