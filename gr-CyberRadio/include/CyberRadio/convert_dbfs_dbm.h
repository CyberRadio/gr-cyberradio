/* -*- c++ -*- */
/* 
 * Copyright 2023 G3.
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


#ifndef INCLUDED_CYBERRADIO_CONVERT_DBFS_DBM_H
#define INCLUDED_CYBERRADIO_CONVERT_DBFS_DBM_H

#include <CyberRadio/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace CyberRadio {

    /*!
     * \brief <+description of block+>
     * \ingroup CyberRadio
     *
     */
    class CYBERRADIO_API convert_dbfs_dbm : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<convert_dbfs_dbm> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of CyberRadio::convert_dbfs_dbm.
       *
       * To avoid accidental use of raw pointers, CyberRadio::convert_dbfs_dbm's
       * constructor is in a private implementation
       * class. CyberRadio::convert_dbfs_dbm::make is the public interface for
       * creating new instances.
       */
      static sptr make(int vec_len, float user_atten, float factory_cal);
    };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_CONVERT_DBFS_DBM_H */

