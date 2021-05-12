#!/usr/bin/env python
###############################################################
# \package CyberRadio.file_like_object_source
# 
# \brief File-Like Object Source
#
# \author DA
# 
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  
#    All rights reserved.
#
###############################################################

from gnuradio import gr
import threading
import numpy
from time import sleep

##
# \class file_like_object_source
# \ingroup CyberRadioBase
# \brief File-like object source block.
#
# The file_like_object_source block acts as a Python file-like
# object for text output from other blocks in the flowgraph.  This text
# is collected and made available for streaming from the block's
# output. 
# 
# To use this block, create a file_like_object_source object, and then
# use that object wherever a Python file-like object could be used to
# write output.
# 
# \note The file_like_object_source object supports only the \c write() and
# \c flush() methods of file-like objects.  It cannot be read from or
# searched.
class file_like_object_source(gr.sync_block):
    
    ##
    # \brief Creates a file_like_object_source object.
    def __init__(self):
        gr.sync_block.__init__(
            self, "[CyberRadio] File-Like Object Source",
            [],
            [numpy.int8],
        )
        self.buffer = ""
        self.buffer_lock = threading.Lock()
        
    # Methods needed for this source to act as a file-like object
    
    ##
    # \brief Write data to this file-like object.
    # \param data Data to write to the object.
    def write(self, data):
        self.buffer_lock.acquire()
        self.buffer += data
        self.buffer_lock.release()
        pass
    
    ##
    # \brief Flush data from this file-like object.
    def flush(self):
        pass
    
    # Methods needed for this source to act as a GNU Radio block
    
    def work(self, input_items, output_items):
        self.buffer_lock.acquire()
        if len(self.buffer)>0:
            noutput_items = len(output_items[0])
            noutput_items_processed = min(noutput_items, len(self.buffer))
            for i in range(0, noutput_items_processed, 1):
                output_items[0][i] = numpy.int8(ord(self.buffer[i]))
            self.buffer = self.buffer[noutput_items_processed:]
        else:
            noutput_items_processed = 0
            sleep(0.001)
        self.buffer_lock.release()
        return noutput_items_processed
    
    
