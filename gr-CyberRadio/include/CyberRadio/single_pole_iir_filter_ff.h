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


#ifndef INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H
#define INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>
#include "CyberRadio/single_pole_iir.h"

#define INPUT_ARGS_TYPE        double alpha, unsigned int vlen, bool resetOnAlphaChange
#define INPUT_ARGS_NO_TYPE     alpha, vlen, resetOnAlphaChange

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API single_pole_iir_filter_ff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<single_pole_iir_filter_ff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::single_pole_iir_filter_ff.
       *
       * To avoid accidental use of raw pointers, CyberRadio::single_pole_iir_filter_ff's
       * constructor is in a private implementation
       * class. CyberRadio::single_pole_iir_filter_ff::make is the public interface for
       * creating new instances.
       */
      static sptr make(INPUT_ARGS_TYPE);

      virtual void set_taps (double alpha) = 0;
      virtual void reset (bool reset) = 0;
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SINGLE_POLE_IIR_FILTER_FF_H */

