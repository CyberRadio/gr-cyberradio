#!/usr/bin/env python
###############################################################
# \package CyberRadio
# 
# \brief The CyberRadio Solutions GNU Radio module (\link CyberRadio 
# CyberRadio\endlink) provides users with GNU Radio blocks for 
# controlling and using CyberRadio Solutions NDR-class radios.
#
# \author NH
# \author DA
# \copyright Copyright (c) 2015 CyberRadio Solutions, Inc.  All 
# rights reserved.
#
###############################################################

###############################################################
# \mainpage CyberRadio Solutions GNU Radio module for Python
#
# \section Description
#
# The CyberRadio Solutions GNU Radio module (\link CyberRadio 
# CyberRadio\endlink) provides users with GNU Radio blocks for 
# controlling and using CyberRadio Solutions NDR-class radios.
#
###############################################################

###############################################################
# \defgroup CyberRadioBase Base Blocks
# GNU Radio blocks that act as bases for other CyberRadio blocks
# \defgroup CyberRadioNDR304 NDR304 Blocks
# GNU Radio blocks for operating NDR304 radios
# \defgroup CyberRadioNDR308 NDR308 Blocks
# GNU Radio blocks for operating NDR308 radios
# \defgroup CyberRadioNDR651 NDR651 Blocks
# GNU Radio blocks for operating NDR651 radios
###############################################################

##
# \brief Driver module name (string).
name = "CyberRadio"
##
# \brief Driver module description (string).
description = "CyberRadio Solutions GNU Radio module for Python"
##
# \brief Driver version number (string).
version = "15.12.09"

# ----------------------------------------------------------------
# Temporary workaround for ticket:181 (swig+python problem)
import sys
_RTLD_GLOBAL = 0
try:
    from dl import RTLD_GLOBAL as _RTLD_GLOBAL
except ImportError:
    try:
	from DLFCN import RTLD_GLOBAL as _RTLD_GLOBAL
    except ImportError:
	pass

if _RTLD_GLOBAL != 0:
    _dlopenflags = sys.getdlopenflags()
    sys.setdlopenflags(_dlopenflags|_RTLD_GLOBAL)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Import SWIG and Python code elements into the CyberRadio namespace.
#
# Each import is wrapped in a try-except block so that only the
# components that the user has installed actually get imported.  This
# allows the user to install only the components he/she wants -- or
# CRS to distribute only the components that the customer needs.
#
# When importing SWIG-generated objects, performing a wildcard import
# is generally safe.  This may or may not be the case for pure Python
# modules, so in the blocks below, we import symbols explicitly.

# BASE Group
# Objects in this group MUST be built and installed correctly for 
# the module to work.  We need to crash out with an exception if
# that is not the case. 
from .CyberRadio_base_swig import *
from .file_like_object_source import file_like_object_source
from .NDR_driver_interface import NDR_driver_interface

# NDR304 Group
try:
    from .NDR304_source import NDR304_source
except:
    pass

# NDR308 Group
try:
    from .NDR308_source import NDR308_source
except:
    pass

# NDR651 Group
try:
    from .CyberRadio_NDR651_swig import *
except:
    pass
try:
    from .NDR651_source import NDR651_source
except:
    pass
try:
    from .NDR651_sink import NDR651_sink
except:
    pass


# ----------------------------------------------------------------
# Tail of workaround
if _RTLD_GLOBAL != 0:
    sys.setdlopenflags(_dlopenflags)      # Restore original flags
# ----------------------------------------------------------------
