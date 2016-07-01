
SUBDIRS=include \
        libcyberradio \
        testvitaiq
        
ACLOCAL_AMFLAGS=-I m4

## Include rules for Doxygen support

include $(top_srcdir)/doxygen.am

## Define a "dummy" data file rule that has no recipe.
## This is needed because make executes the data file rule 
## prior to executing target all-local (which runs Doxygen
## to create the target data files).  

$(DATA): ;

## Define rules to automatically rebuild documentation each time
## we do a build.

clean-local:
	$(RM) $(DX_CLEANFILES)
	
all-local: clean-local doxygen-doc

## HTML files that Doxygen creates for us.  These will be installed 
## (or placed in an installation package).  But since they don't need 
## to be included in our source distribution, we don't put the "dist_" 
## prefix on the variable name.
## NOTE: The wildcard used here goes against standard Automake protocol
## (which wants us to enumerate the list of files to install).  However,
## since Doxygen can potentially generate a completely different list of
## files depending on which version of Doxygen is installed, this protects 
## us from make errors caused by a slight version difference.
html_DATA = docs/html/*

## Add DX_CLEANFILES to MOSTLYCLEANFILES so that the documentation 
## directory that gets created during the build process is eliminated 
## during "make clean".

MOSTLYCLEANFILES = $(DX_CLEANFILES)

## Add files that should be included in the source distribution 
## (created with "make dist") but aren't included by default:
## * Doxygen configuration file

EXTRA_DIST = $(DX_CONFIG)
