


#ifndef INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_H
#define INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_H

#include <CyberRadio/api.h>
//#include <gnuradio/sync_block.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace CyberRadio {

    #define INPUT_ARGUMENTS_TYPE const char* radioHostname, int num_inputs, int debug, int groupIndex, int channelRate, int tenGbeIndex, \
    double centerFreqMHz1, int txChannel1, double rf_attenuationDB1, const char* eth_index1, long upd_port1, double frequencyOffsetMHz1, double digital_attenuationDB1, float mult1, int ducChannel1, \
    double centerFreqMHz2, int txChannel2, double rf_attenuationDB2, const char* eth_index2, long upd_port2, double frequencyOffsetMHz2, double digital_attenuationDB2, float mult2, int ducChannel2
    
    #define INPUT_ARGUMENTS_NO_TYPE radioHostname, num_inputs, debug, groupIndex, channelRate, tenGbeIndex, \
    centerFreqMHz1, txChannel1, rf_attenuationDB1, eth_index1, upd_port1, frequencyOffsetMHz1, digital_attenuationDB1, mult1, ducChannel1, \
    centerFreqMHz2, txChannel2, rf_attenuationDB2, eth_index2, upd_port2, frequencyOffsetMHz2, digital_attenuationDB2, mult2, ducChannel2

    class CYBERRADIO_API NDR651_sync_sink : virtual public sync_decimator
    {
     public:
      typedef boost::shared_ptr<NDR651_sync_sink> sptr;
      static sptr make(INPUT_ARGUMENTS_TYPE);
 virtual void mult_callback(float mult1, float mult2) = 0;
 virtual bool setDUCFreq_callback(double frequencyOffsetMHz1, double frequencyOffsetMHz2)= 0;
 virtual bool setDUCAtten_callback(double digital_attenuationDB1, double digital_attenuationDB2)= 0;
 virtual bool setTxFreq_callback(double centerFreqMHz1, double centerFreqMHz2)= 0;
virtual bool setTxAtten_callback(double rf_attenuationDB1, double rf_attenuationDB2)= 0;
 virtual bool setDUCParameters(int ducChannel1, int ducChannel2, int channelRate, int txChannel1, int txChannel2)= 0;
 virtual bool setEthernetInterface(unsigned int tenGbeIndex, const char *eth_index1, const char *eth_index2, long upd_port1, long upd_port2)= 0;

//bool doCallBacks(INPUT_ARGUMENTS_TYPE);
          };

  } // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIO_NDR651_SYNC_SINK_H */

