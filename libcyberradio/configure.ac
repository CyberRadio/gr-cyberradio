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
