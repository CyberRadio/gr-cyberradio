
#ifndef INCLUDED_CYBERRADIO_MUX_IMPL_H
#define INCLUDED_CYBERRADIO_MUX_IMPL_H

#include <CyberRadio/mux.h>

namespace gr {
namespace CyberRadio {

class mux_impl : public mux {
  private:
	INPUT_ARGS_DECLARATION
	
	std::vector<tag_t> d_tags;
	std::vector<tag_t>::iterator d_tags_itr;
	
	void rxControlMsg(pmt::pmt_t msg);
	void txStatusMsg(void);

  public:
	mux_impl(INPUT_ARGS_TYPE);
	~mux_impl();

	bool set_input_index(int input_index);
	int get_input_index(void);

	// Where all the action really happens
	int work(int noutput_items,
	         gr_vector_const_void_star &input_items,
	         gr_vector_void_star &output_items);
};

} // namespace CyberRadio
} // namespace gr

#endif /* INCLUDED_CyberRadio_MUX_IMPL_H */

