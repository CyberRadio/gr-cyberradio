#######################################
# Generic build information for all executables.

ACLOCAL_AMFLAGS = -I ../m4

# The directory where example programs will be installed
exampledir = $(pkgdatadir)/examples

# The list of executables we are building separated by spaces.
# The 'example_' indicates that these build products will be 
# installed in the $(exampledir) directory, defined above.
example_PROGRAMS = testvitaiq

# The list of example source files separated by spaces.
# The 'example_' indicates that these build products will be 
# installed in the $(exampledir) directory, defined above.
example_DATA = testvitaiq.cpp


#######################################
# Build information for each executable. Variable names are derived
# from the name of the executable, with each non alpha-numeric character
# replaced by '_'.
# To add additional example programs:
# (1) Add the executable name to the example_PROGRAMS list above.
# (2) Add example source files to the example_DATA list above.
# (3) Add build variables <executable>_SOURCES, <executable>_LDADD, 
#    <executable>_LDFLAGS, and <executable>_CPPFLAGS below.

# testvitaiq
# -- Sources
testvitaiq_SOURCES = testvitaiq.cpp
# -- Libraries
testvitaiq_LDADD = ../libcyberradio/libcyberradio.la
# -- Compiler options
testvitaiq_CPPFLAGS = -I$(top_srcdir)/include
# -- Linker options
testvitaiq_LDFLAGS = -rpath `cd ..;pwd`/libcyberradio/.libs $(BOOST_SYSTEM_LIB)

