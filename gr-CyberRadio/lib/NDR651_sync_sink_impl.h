

#ifndef INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_IMPL_H
#define INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_IMPL_H

//#include <LibCyberRadio/NDR651/SyncTXClient.h>


#include <LibCyberRadio/NDR651/SyncTXClient.h>
#include <vector>

#include "CyberRadio/NDR651_sync_sink.h"

namespace gr {
namespace CyberRadio {

#define NUM_CH 2
#define ETH_PACKET_SIZE 1024

/**
* This grc block is used to transmit data synchrnously to the NDR651
* It takes in 2 complex IQ streams and sends data out via syncTXClient (some sort of ethernet thing)
* It sends data out in sizes of ETH_PACKET_SIZE (1024), so this block was made to be decimating. By being decimating, GNU radio won't call it untill it has multiples of ETH_PACKET_SIZE
*/
class NDR651_sync_sink_impl : public NDR651_sync_sink {
  private:
	// Variables that are shared between channels
	const char* radioHostname; int num_inputs; int debug;  int groupIndex; int channelRate; int tenGbeIndex;
	// Variables present in both groups
	double centerFreqMHz[NUM_CH];  int txChannel[NUM_CH]; double rf_attenuationDB[NUM_CH]; const char* eth_index[NUM_CH]; long upd_port[NUM_CH]; double frequencyOffsetMHz[NUM_CH]; double digital_attenuationDB[NUM_CH]; float mult[NUM_CH]; int ducChannel[NUM_CH];

	std::vector<LibCyberRadio::NDR651::TXClient *> txClients;
	LibCyberRadio::NDR651::SyncTXClient * syncTXClient;
	// These buffers contain the gr_complex data that's been converted into int16_t IQ data.
	std::vector<int16_t> iqBuffers[NUM_CH];

  public:
	NDR651_sync_sink_impl(INPUT_ARGUMENTS_TYPE);
	~NDR651_sync_sink_impl();

	int work(int noutput_items,
	         gr_vector_const_void_star &input_items,
	         gr_vector_void_star &output_items);

	bool stop();

	// Callbacks
	//bool doCallBacks(INPUT_ARGUMENTS_TYPE);

	void mult_callback(float mult1, float mult2);

bool setDUCFreq_callback(double frequencyOffsetMHz1, double frequencyOffsetMHz2);
bool setDUCAtten_callback(double digital_attenuationDB1, double digital_attenuationDB2);
bool setTxFreq_callback(double centerFreqMHz1, double centerFreqMHz2);
bool setTxAtten_callback(double rf_attenuationDB1, double rf_attenuationDB2);
bool setDUCParameters(int ducChannel1, int ducChannel2, int channelRate, int txChannel1, int txChannel2);
bool setEthernetInterface(unsigned int tenGbeIndex, const char *eth_index1, const char *eth_index2, long upd_port1, long upd_port2);


};


} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_IMPL_H */

