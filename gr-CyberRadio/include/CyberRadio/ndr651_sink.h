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


#ifndef INCLUDED_CYBERRADIO_NDR651_SINK_H
#define INCLUDED_CYBERRADIO_NDR651_SINK_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

namespace gr
{
	namespace CyberRadio
	{

		/*!
		 * \brief <+description of block+>
		 * \ingroup CyberRadio
		 *
		 */
		class CYBERRADIO_API ndr651_sink : virtual public gr::sync_block
		{
			public:
				typedef boost::shared_ptr<ndr651_sink> sptr;

				/*!
				* \brief Return a shared_ptr to a new instance of CyberRadio::ndr651_sink.
				*
				* To avoid accidental use of raw pointers, CyberRadio::ndr651_sink's
				* constructor is in a private implementation
				* class. CyberRadio::ndr651_sink::make is the public interface for
				* creating new instances.
				*/
				static sptr make(std::string hostname, unsigned int vlen, bool debug);

				virtual bool setDUCParameters(unsigned int ducChannel, unsigned int ducRateIndex, unsigned int txChannel) = 0;
				virtual bool setEthernetInterface(unsigned int tenGbeIndex, const std::string &txInterfaceName, unsigned short port) = 0;
				virtual bool setDUCRateIndex(unsigned int ducRateIndex) = 0;
				virtual bool setDUCFreq(double ducFreq) = 0;
				virtual bool setDUCAtten(double ducAtten) = 0;
				virtual bool setTxFreq(double txFreq) = 0;
				virtual bool setTxAtten(double txAttenuation) = 0;
				virtual bool setTxInversion(bool txInversion) = 0;
				virtual bool pauseDUC(bool paused = true) = 0;

				bool start() = 0;
				bool stop() = 0;
		};

	} // namespace CyberRadio

} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_SINK_H */

