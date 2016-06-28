dnl Process this file with autoconf to produce a configure script.

AC_PREREQ(2.59)
AC_INIT(libcyberradio, 16.06.20)

AC_CANONICAL_SYSTEM

AC_CONFIG_MACRO_DIR([m4])

AX_CHECK_ENABLE_DEBUG()
AC_PROG_CC
AC_PROG_CXX

dnl Initialize automake
AM_INIT_AUTOMAKE

dnl this allows us specify individual liking flags for each target
AM_PROG_CC_C_O 

dnl Initialize Libtool
LT_INIT

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

dnl Doxygen support
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

AC_CONFIG_FILES(Makefile
                include/Makefile
                libcyberradio/Makefile
                testvitaiq/Makefile
                )
AC_OUTPUT
