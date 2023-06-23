
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <string.h>

#include <gnuradio/io_signature.h>
#include "mux_impl.h"


namespace gr {
namespace CyberRadio {

mux::sptr
mux::make(INPUT_ARGS_TYPE) {
	return gnuradio::get_initial_sptr
	       (new mux_impl(INPUT_ARGS_NO_TYPE));
}


mux_impl::mux_impl(INPUT_ARGS_TYPE)
	: gr::sync_block("mux",
	                 gr::io_signature::make( numInputs, numInputs, typeSize * vlen),
	                 gr::io_signature::make( 1, 1, typeSize * vlen)) {
	this->vlen = vlen;
	this->numInputs = numInputs;
	this->typeSize = typeSize;
	this->input_index = input_index;
	
	set_tag_propagation_policy( gr::block::TPP_DONT );
	
	//Create input port
	message_port_register_in(pmt::mp("control"));
	set_msg_handler(pmt::mp("control"), boost::bind(&mux_impl::rxControlMsg, this, _1));

	//Create output ports
	message_port_register_out(pmt::mp("status"));

}


mux_impl::~mux_impl() {}

bool mux_impl::set_input_index(int input_index) {
	bool rv = false;
	if ((input_index>=0)&&(input_index<this->numInputs)) {
		this->input_index = input_index;
		rv = true;
	} else {
		std::cerr << "Cannot set input_index to " << input_index << "; max value " << (this->numInputs-1) << "!" << std::endl;
	}
	this->txStatusMsg();
	return rv;
}

int mux_impl::get_input_index(void) {
	return this->input_index;
}

void mux_impl::rxControlMsg(pmt::pmt_t msg) {
	pmt::pmt_t tag = pmt::car(msg);
	pmt::pmt_t value = pmt::cdr(msg);
	//~ std::cout << "tag = " << tag << std::endl;
	//~ std::cout << "value = " << value << std::endl;
	this->set_input_index(pmt::to_long(value));
}

void mux_impl::txStatusMsg(void) {
	pmt::pmt_t msg = pmt::cons(pmt::intern("mux_input"), pmt::from_long(this->get_input_index()));
	message_port_pub(pmt::mp("status"), msg);
}

int
mux_impl::work(int noutput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items) {

	memcpy(output_items[0], input_items[input_index], vlen * typeSize * noutput_items);
	
	uint64_t abs_N, end_N;
	abs_N = nitems_read(input_index);
	end_N = abs_N + (uint64_t)(noutput_items);
	d_tags.clear();
	get_tags_in_range(d_tags, input_index, abs_N, end_N);
	 for(d_tags_itr = d_tags.begin(); d_tags_itr != d_tags.end(); d_tags_itr++) {
		add_item_tag(0, d_tags_itr->offset, d_tags_itr->key, d_tags_itr->value);
		
		//~ sout << std::setw(10) << "Offset: " << d_tags_itr->offset
		//~ << std::setw(10) << "Source: "
		//~ << (pmt::is_symbol(d_tags_itr->srcid) ? pmt::symbol_to_string(d_tags_itr->srcid) : "n/a")
		//~ << std::setw(10) << "Key: " << pmt::symbol_to_string(d_tags_itr->key)
		//~ << std::setw(10) << "Value: ";
		//~ sout << d_tags_itr->value << std::endl;
	}
	
	return noutput_items;
}

} /* namespace CyberRadio */
} /* namespace gr */

