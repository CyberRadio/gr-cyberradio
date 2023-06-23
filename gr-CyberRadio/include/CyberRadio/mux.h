

#ifndef INCLUDED_CYBERRADIOTEST_MUX_H
#define INCLUDED_CYBERRADIOTEST_MUX_H

#include <CyberRadio/api.h>
#include <gnuradio/sync_block.h>

#undef INPUT_ARGS_TYPE
#undef INPUT_ARGS_DECLARATION
#undef INPUT_ARGS_NO_TYPE

#define INPUT_ARGS_TYPE        int vlen, int numInputs, int typeSize, int input_index
#define INPUT_ARGS_NO_TYPE     vlen, numInputs,typeSize, input_index
#define INPUT_ARGS_DECLARATION int vlen; int numInputs; int typeSize; int input_index;

namespace gr {
namespace CyberRadio {


class CYBERRADIO_API mux : virtual public gr::sync_block {
  public:
	typedef boost::shared_ptr<mux> sptr;

	virtual bool set_input_index(int input_index)=0;
	virtual int get_input_index(void)=0;
	static sptr make(INPUT_ARGS_TYPE);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CYBERRADIOTEST_MUX_H */

