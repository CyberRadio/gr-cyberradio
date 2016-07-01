dnl Process this file with autoconf to produce a configure script.

dnl Initialize autoconf.  Version 2.64 is the minimum required, due to the 
dnl AX_CHECK_ENABLE_DEBUG macro we are using.
AC_PREREQ(2.64)
AC_INIT(libcyberradio, 16.06.20)
: ${CFLAGS="-g -O2"}
: ${CXXFLAGS="-g -O2"}
AC_CANONICAL_SYSTEM
AC_CONFIG_MACRO_DIR([m4])

dnl Initialize automake
AM_INIT_AUTOMAKE

dnl Enable debugging if desired
AX_CHECK_ENABLE_DEBUG

dnl Configure C and C++ compilers
AC_PROG_CC
AC_PROG_CXX
AM_PROG_CC_C_O 

dnl Check for Boost and required components of Boost that we need.  Since we depend
dnl on the Boost::Chrono library, Boost must be at least version 1.47.
AX_BOOST_BASE([1.47], [], [AC_MSG_ERROR([Boost libraries (1.47 or newer) are required but could not be found])])
AX_BOOST_ASIO
test "x$BOOST_ASIO_LIB" = "x" && AC_MSG_ERROR([Boost::ASIO library is required but could not be found])
AX_BOOST_CHRONO
test "x$BOOST_CHRONO_LIB" = "x" && AC_MSG_ERROR([Boost::Chrono library is required but could not be found])
AX_BOOST_SYSTEM
test "x$BOOST_SYSTEM_LIB" = "x" && AC_MSG_ERROR([Boost::System library is required but could not be found])
AX_BOOST_THREAD
test "x$BOOST_THREAD_LIB" = "x" && AC_MSG_ERROR([Boost::Thread library is required but could not be found])

dnl Enable Doxygen support
dnl NOTE: Automake files that need Doxygen support must include doxygen.am
dnl       to get the appropriate build rules.
DX_HTML_FEATURE(ON)
DX_CHM_FEATURE(OFF)
DX_CHI_FEATURE(OFF)
DX_MAN_FEATURE(OFF)
DX_RTF_FEATURE(OFF)
DX_XML_FEATURE(OFF)
DX_PDF_FEATURE(OFF)
DX_PS_FEATURE(OFF)
DX_INIT_DOXYGEN($PACKAGE_NAME, $PACKAGE_NAME.doxyfile, docs)

dnl Initialize Libtool
LT_INIT

AC_CONFIG_FILES(Makefile
                include/Makefile
                libcyberradio/Makefile
                testvitaiq/Makefile
                )
AC_OUTPUT
