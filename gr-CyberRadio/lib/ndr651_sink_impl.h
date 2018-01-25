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

#ifndef INCLUDED_CYBERRADIO_NDR651_SINK_IMPL_H
#define INCLUDED_CYBERRADIO_NDR651_SINK_IMPL_H

#include <CyberRadio/ndr651_sink.h>
#include "LibCyberRadio/NDR651/TXClient.h"
#include <volk/volk.h>

#define SAPMLES_PER_FRAME 1024

namespace gr
{
	namespace CyberRadio
	{

		class ndr651_sink_impl : public ndr651_sink
		{
			private:
				LibCyberRadio::NDR651::TXClient * txClient;
				bool d_firstFrame;
				int16_t *txBuffer;
				unsigned int d_vlen;

			public:
				ndr651_sink_impl(std::string hostname, unsigned int vlen, bool debug);
				~ndr651_sink_impl();

				bool start();
				bool stop();

				// Where all the action really happens
				int work(int noutput_items,
				    gr_vector_const_void_star &input_items,
				    gr_vector_void_star &output_items);

				bool setDUCParameters(
					unsigned int ducChannel,
					unsigned int ducRateIndex,
					unsigned int txChannel
						);
				bool setEthernetInterface(
					unsigned int tenGbeIndex,
					const std::string &txInterfaceName,
					unsigned short port
						);
				bool setDUCRateIndex(unsigned int ducRateIndex);
				bool setDUCFreq(double ducFreq);
				bool setDUCAtten(double ducAtten);
				bool setTxFreq(double txFreq);
				bool setTxAtten(double txAttenuation);
				//bool setTxInversion(bool txInversion) { return true; };
				bool setTxInversion(bool txInversion);
			//			void disableRF();
				bool pauseDUC(bool paused = true);

			protected:
				void handleMsgFreq( pmt::pmt_t msg );

		};

	} // namespace CyberRadio

} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_SINK_IMPL_H */

