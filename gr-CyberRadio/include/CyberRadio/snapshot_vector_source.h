/* -*- c++ -*- */
/*
 * Copyright 2022 G3.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_CYBERRADIO_SNAPSHOT_VECTOR_SOURCE_H
#define INCLUDED_CYBERRADIO_SNAPSHOT_VECTOR_SOURCE_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API snapshot_vector_source : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<snapshot_vector_source> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::snapshot_vector_source.
       *
       * To avoid accidental use of raw pointers, CyberRadio::snapshot_vector_source's
       * constructor is in a private implementation
       * class. CyberRadio::snapshot_vector_source::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string radio_type, const std::string &ip, unsigned int port,unsigned int block_size, unsigned int block_rate);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_SNAPSHOT_VECTOR_SOURCE_H */
