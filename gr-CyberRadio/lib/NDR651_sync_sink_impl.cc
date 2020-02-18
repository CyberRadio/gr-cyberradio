/* -*- c++ -*- */
/*
 * Copyright 2017 G3
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <complex>
using std::complex;
#include <iostream>
using std::cout;
using std::endl;
using std::cerr;

#include <gnuradio/io_signature.h>
#include <volk/volk.h>

#include <iomanip>
//! Prints the variables name and value. For example, if "int x = 9", this would print "x:9"
#define PRINT_VAR(x) std::cout << std::setw(25)  << #x << ": " << x << '\n'


#include "NDR651_sync_sink_impl.h"


namespace gr {
namespace CyberRadio {

NDR651_sync_sink::sptr NDR651_sync_sink::make(INPUT_ARGUMENTS_TYPE) {
	return gnuradio::get_initial_sptr
	       (new NDR651_sync_sink_impl(INPUT_ARGUMENTS_NO_TYPE));
}

//! JOIN(a,1) would give a1
#define JOIN(x,n) x##n
//! This macro makes assigning class variables to the many imput variables easier
#define THIS_ASSIGN(x) this->x[0] = JOIN(x,1); this->x[1] = JOIN(x,2);

NDR651_sync_sink_impl::NDR651_sync_sink_impl(INPUT_ARGUMENTS_TYPE)
	: sync_decimator("NDR651_sync_sink",	 gr::io_signature::make(1, 2, sizeof(std::complex<float>)),	 gr::io_signature::make(0, 0, 0), ETH_PACKET_SIZE) {
	// Set shared variables
	this->radioHostname = radioHostname; this->num_inputs = num_inputs; this->debug = debug; this->groupIndex = groupIndex; this->channelRate = channelRate; this->tenGbeIndex = tenGbeIndex;
	// Set channel specific variables
	THIS_ASSIGN(centerFreqMHz); THIS_ASSIGN(txChannel); THIS_ASSIGN(rf_attenuationDB); THIS_ASSIGN(eth_index); THIS_ASSIGN(upd_port); THIS_ASSIGN(frequencyOffsetMHz); THIS_ASSIGN(digital_attenuationDB); THIS_ASSIGN(mult); THIS_ASSIGN(ducChannel);

	// Debug that prints all the variables passed in
	if(debug) {
		cout << "NDR651 sync sink last compiled " << __TIME__ << ", " <<  __DATE__ << endl << endl;

		PRINT_VAR(this->radioHostname);
		PRINT_VAR(this->num_inputs);
		PRINT_VAR(this->debug);
		PRINT_VAR(this->groupIndex);
		PRINT_VAR(this->channelRate);

		cout << endl;
		for(int i = 0; i < num_inputs; i++) {
			cout << "i = " << i << endl;
			PRINT_VAR(centerFreqMHz[i]);
			PRINT_VAR(txChannel[i]);
			PRINT_VAR(rf_attenuationDB[i]);
			PRINT_VAR(eth_index[i]);
			PRINT_VAR(upd_port[i]);
			PRINT_VAR(frequencyOffsetMHz[i]);
			PRINT_VAR(digital_attenuationDB[i]);
			cout << endl;
		}
	}

	// Sets variables for the two transmiters that are started synchronously by syncTXClient
	{
		unsigned int tenGbeIndex  = 1;

		for( int i = 0; i < num_inputs; i++) {
			txClients.push_back(new LibCyberRadio::NDR651::TXClient(radioHostname, debug) );
			txClients[i]->setDUCParameters(ducChannel[i], channelRate, txChannel[i]); // DUC
			txClients[i]->setEthernetInterface(tenGbeIndex + i, eth_index[i], upd_port[i]); // COM
			txClients[i]->setTxFreq(centerFreqMHz[i]);
			txClients[i]->setDUCFreq(frequencyOffsetMHz[i] * 1e6);
		}
	}

	syncTXClient = new LibCyberRadio::NDR651::SyncTXClient(txClients, radioHostname, debug);
	syncTXClient->setDucGroup(groupIndex);
	syncTXClient->start();
}


bool NDR651_sync_sink_impl::stop() {
	if( debug)
		cout << "stop called" << endl;
	syncTXClient->stop();
	// Cleanup (SyncTX Constructor deletes TXClients)
	delete syncTXClient;
}


NDR651_sync_sink_impl::~NDR651_sync_sink_impl() {
}

#define DEBUG_PRINT_FUNC if(debug){ cout << __FUNCTION__ << endl; }

void NDR651_sync_sink_impl::mult_callback(float mult1, float mult2) {
DEBUG_PRINT_FUNC
	THIS_ASSIGN(mult);
}

bool NDR651_sync_sink_impl::setDUCFreq_callback(double frequencyOffsetMHz1, double frequencyOffsetMHz2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(frequencyOffsetMHz);
	for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setDUCFreq(frequencyOffsetMHz[i]);
}


bool NDR651_sync_sink_impl::setDUCAtten_callback(double digital_attenuationDB1, double digital_attenuationDB2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(digital_attenuationDB);
		for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setDUCAtten(digital_attenuationDB[i]);
}

bool NDR651_sync_sink_impl::setTxFreq_callback(double centerFreqMHz1, double centerFreqMHz2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(centerFreqMHz);
	for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setTxFreq(centerFreqMHz[i]);
}


bool NDR651_sync_sink_impl::setTxAtten_callback(double rf_attenuationDB1, double rf_attenuationDB2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(rf_attenuationDB);
	for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setTxAtten(rf_attenuationDB[i]);
}


bool NDR651_sync_sink_impl::setDUCParameters(int ducChannel1, int ducChannel2, int channelRate, int txChannel1, int txChannel2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(ducChannel);
THIS_ASSIGN(txChannel);
this->channelRate = channelRate;
	for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setDUCParameters(ducChannel[i], channelRate, txChannel[i]);
}

bool NDR651_sync_sink_impl::setEthernetInterface(unsigned int tenGbeIndex, const char *eth_index1, const char *eth_index2, long upd_port1, long upd_port2) {
DEBUG_PRINT_FUNC
THIS_ASSIGN(eth_index);
this->tenGbeIndex = tenGbeIndex;
THIS_ASSIGN(upd_port);
	for(int i = 0; i < NUM_CH; i++)
		this->txClients[i]->setEthernetInterface(tenGbeIndex + i, eth_index[i], upd_port[i]);
}

#if 0
#define IF_THIS_VAR_NEQ_VAR(x,i,j,function) if (this->x[i] != JOIN(x,j)){ this->x[i] = JOIN(x,j); function;}

bool NDR651_sync_sink_impl::doCallBacks(INPUT_ARGUMENTS_TYPE) {
	bool used = false;
	bool sucess = true;

	IF_THIS_VAR_NEQ_VAR(mult, 0, 1, ;)
	IF_THIS_VAR_NEQ_VAR(mult, 1, 2, ;)




	IF_THIS_VAR_NEQ_VAR(centerFreqMHz, 0, 1, this->txClients[0]->setTxFreq(centerFreqMHz[0]) )
	IF_THIS_VAR_NEQ_VAR(centerFreqMHz, 1, 2, this->txClients[1]->setTxFreq(centerFreqMHz[1]) )






	//SET_PAIR_PIECE_IF_DIFF(centerFreqMHz, this->txClient, ->setTxFreq(centerFreqMHz))


	//		THIS_ASSIGN(centerFreqMHz); THIS_ASSIGN(txChannel); THIS_ASSIGN(rf_attenuationDB); THIS_ASSIGN(eth_index); THIS_ASSIGN(upd_port); THIS_ASSIGN(frequencyOffsetMHz); THIS_ASSIGN(digital_attenuationDB); THIS_ASSIGN(mult);
}

#endif




int NDR651_sync_sink_impl::work(int noutput_items, gr_vector_const_void_star &input_items, gr_vector_void_star &output_items) {
	size_t numInputs = input_items.size();
	// The number of output items is expected to be much less than the input items since this is a decimating block
	// This block does not actually output anything though.
	noutput_items *= ETH_PACKET_SIZE;


	// Convert the input data to IQ
	{
		complex<float> *streams[numInputs];
		for(size_t i = 0; i < numInputs; i++)
			streams[i] = (complex<float> *) input_items[i];

		for( size_t i = 0; i < NUM_CH; i++) {
			// Each complex data sample has an I and Q component
			int16_t *start = &iqBuffers[0][0];
			// Make sure that the buffer will be large enough to hold the items
			// Fun fact: resize() will never re allocate memory to make the vector smaller (this is good for performance such as in this case)
			// Each complex sample results in 2 int16_t pairs (hence the times 2)
			iqBuffers[i].resize(noutput_items * 2);
			int16_t *end = &iqBuffers[0][0];
			// Little endian. Uses Volk to speed up conversion process from complex<float> to complex int16_t
#if 1
			//volk_64u_byteswap((uint64_t*)(&streams[i][0]), noutput_items);
			volk_32f_s32f_convert_16i(&iqBuffers[i][0], (const float *)&streams[i][0], mult[i], noutput_items * 2);
			// Shh, it's fine.
			volk_32u_byteswap((uint32_t*)(&iqBuffers[i][0]), noutput_items);
			volk_16u_byteswap((uint16_t*)(&iqBuffers[i][0]), noutput_items * 2);
#else
			for( int j = 0; j < noutput_items; j++) {
				iqBuffers[i][j * 2 + 1] = streams[i][j].real();
				iqBuffers[i][j * 2 + 0] = streams[i][j].imag();
			}
#endif
		}
	}

	// Send the converted data via the syncTXClient
	{
		// Should really be int16_t, but syncTXClient expects a short. This contains both streams of int16_t IQ data
		short *samples[2];
		int sent = 0;
		// Sends data ETH_PACKET_SIZE IQ samples at a time
		for(; sent + ETH_PACKET_SIZE <= noutput_items; sent += ETH_PACKET_SIZE) {
			// Since each buffer is of short IQ, it increments twice as fast to get the IQ pairs
			for(int i = 0; i < NUM_CH; i++)
				samples[i] = &iqBuffers[i][sent * 2];
			syncTXClient->sendFrames(samples, ETH_PACKET_SIZE);
		}
		return sent / ETH_PACKET_SIZE;
	}

}

} /* namespace CyberRadio */
} /* namespace gr */

