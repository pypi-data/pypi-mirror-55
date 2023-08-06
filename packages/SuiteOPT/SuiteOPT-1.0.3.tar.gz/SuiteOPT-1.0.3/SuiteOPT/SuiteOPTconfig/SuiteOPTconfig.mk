# it is assumed that this file will be included in a Makefile found
# in either a Demo or Lib or CUTEst directory
include ../../SuiteOPTconfig/Userconfig.mk

# For python configuration, add flags to LDLIBS
LDLIBS += $(PYSUITEOPT_RPATH)
# End customization for python configuration

# the math library is needed
LDLIBS += -lm

# full path to SuiteSparseX and SuiteOPT
SUITESPARSE ?= $(realpath $(CURDIR)/../../SuiteSparseX)
SUITEOPT    ?= $(realpath $(CURDIR)/../..)

# basic settings for all levels of optimization
CFLAGS = -std=c99

RANLIB ?= ranlib
ARCHIVE ?= $(AR) $(ARFLAGS)

# remove object files, but keep compiled libraries via 'make clean'
CLEAN = *.o *.obj *.ln *.bb *.bbg *.da *.tcov *.gcov gmon.out *.bak *.d \
        *.gcda *.gcno *.aux *.bbl *.blg *.log *.toc *.dvi *.lof *.lot

# also remove compiled libraries, via 'make distclean'
PURGE = *.so* *.a *.dll *.dylib *.dSYM


# Following is an abbreviated version of Tim Davis' SuiteSparse config file

    #---------------------------------------------------------------------------
    # installation location
    #---------------------------------------------------------------------------

    # For "make install" and "make uninstall", the default location is
    # SuiteOPT/lib and SuiteOPT/include
    INSTALL ?= $(SUITEOPT)
    INSTALL_LIB ?= $(INSTALL)/lib

    #---------------------------------------------------------------------------
    # parallel make
    #---------------------------------------------------------------------------

    # sequential make's by default
    JOBS ?= 1

    #---------------------------------------------------------------------------
    # OpenMP is used in SUITEOPT
    #---------------------------------------------------------------------------

    # with gcc, enable OpenMP directives via -fopenmp
    # This is not supported on Darwin, so this string is cleared, below.
    CFOPENMP ?= -fopenmp

    #---------------------------------------------------------------------------
    # CFLAGS for the C/C++ compiler
    #---------------------------------------------------------------------------

    # The CF macro is used by SuiteOPT Makefiles as a combination of
    # CFLAGS, CPPFLAGS, TARGET_ARCH, and system-dependent settings.
    CF ?= $(CFLAGS) $(CPPFLAGS) $(TARGET_ARCH) $(OPTFLAGS) -fexceptions

    #---------------------------------------------------------------------------
    # required libraries
    #---------------------------------------------------------------------------

    # SuiteOPT requires the BLAS, LAPACK, and -lm (Math) libraries.
    # It places its shared *.so libraries in SuiteOPT/lib.
    # Linux also requires the -lrt library (see below)
    LDFLAGS = -L$(SUITESPARSE)/lib -L$(SUITEOPT)/lib

    #---------------------------------------------------------------------------
    # shell commands
    #---------------------------------------------------------------------------

    # ranlib, and ar, for generating libraries.  If you don't need ranlib,
    # just change it to RANLAB = echo
    RANLIB ?= ranlib
    ARCHIVE ?= $(AR) $(ARFLAGS)
    CP ?= cp -f
    MV ?= mv -f

#===============================================================================
# System-dependent configurations
#===============================================================================

    #---------------------------------------------------------------------------
    # determine what system we are on
    #---------------------------------------------------------------------------

    # To disable these auto configurations, use 'make UNAME=custom'

    ifndef UNAME
        ifeq ($(OS),Windows_NT)
            # Cygwin Make on Windows has an $(OS) variable, but not uname.
            # Note that this option is untested.
            UNAME = Windows
        else
            # Linux and Darwin (Mac OSX) have been tested.
            UNAME := $(shell uname)
        endif
    endif

    #---------------------------------------------------------------------------
    # Linux
    #---------------------------------------------------------------------------

    ifeq ($(UNAME),Linux)
        # add the realtime library, librt, and SuiteSparse/lib
        LDLIBS += -lrt -Wl,-rpath=$(INSTALL_LIB) -Wl,-rpath=$(SUITESPARSE)/lib
    endif

    #---------------------------------------------------------------------------
    # Mac
    #---------------------------------------------------------------------------

    ifeq ($(UNAME), Darwin)
        # To compile on the Mac, you must install Xcode.  Then do this at the
        # command line in the Terminal, before doing 'make':
        # xcode-select --install
        CF += -fno-common
        BLAS = -framework Accelerate
        LAPACK = -framework Accelerate
        # OpenMP is not yet supported by default in clang
        CFOPENMP =
    endif

    #---------------------------------------------------------------------------
    # Solaris
    #---------------------------------------------------------------------------

    ifeq ($(UNAME), SunOS)
        # Using the Sun compiler and the Sun Performance Library
        # This hasn't been tested recently.
        # I leave it here in case you need it.  It likely needs updating.
        CF += -fast -KPIC -xc99=%none -xlibmieee -xlibmil -m64 -Xc
        F77FLAGS = -O -fast -KPIC -dalign -xlibmil -m64
        BLAS = -xlic_lib=sunperf
        LAPACK =
        # Using the GCC compiler and the reference BLAS
        ## CC = gcc
        ## CXX = g++
        ## MAKE = gmake
        ## BLAS = -lrefblas -lgfortran
        ## LAPACK = -llapack
    endif

    #---------------------------------------------------------------------------
    # IBM AIX
    #---------------------------------------------------------------------------

    ifeq ($(UNAME), AIX)
        # hasn't been tested for a very long time...
        # I leave it here in case you need it.  It likely needs updating.
        CF += -O4 -qipa -qmaxmem=16384 -q64 -qproto -DBLAS_NO_UNDERSCORE
        F77FLAGS =  -O4 -qipa -qmaxmem=16384 -q64
        BLAS = -lessl
        LAPACK =
    endif

#===============================================================================
# finalize the CF compiler flags
#===============================================================================

    CF += $(CFOPENMP)

#===============================================================================
# internal configuration
#===============================================================================

    # The user should not have to change these definitions, and they are
    # not displayed by 'make config'

    #---------------------------------------------------------------------------
    # for removing files not in the distribution
    #---------------------------------------------------------------------------

    # remove object files, but keep compiled libraries via 'make clean'
    CLEAN = *.o *.obj *.ln *.bb *.bbg *.da *.tcov *.gcov gmon.out *.bak *.d \
        *.gcda *.gcno *.aux *.bbl *.blg *.log *.toc *.dvi *.lof *.lot

    # also remove compiled libraries, via 'make distclean'
    PURGE = *.so* *.a *.dll *.dylib *.dSYM

#===============================================================================
# Building the shared and static libraries
#===============================================================================

# How to build/install shared and static libraries for Mac and Linux/Unix.
# This assumes that LIBRARY and VERSION have already been defined by the
# Makefile that includes this file.

SO_OPTS = $(LDFLAGS)

ifeq ($(UNAME),Windows)
    # Cygwin Make on Windows (untested)
    AR_TARGET = $(LIBRARY).lib
    SO_PLAIN  = $(LIBRARY).dll
    SO_MAIN   = $(LIBRARY).$(SO_VERSION).dll
    SO_TARGET = $(LIBRARY).$(VERSION).dll
    SO_INSTALL_NAME = echo
else
    # Mac or Linux/Unix
    AR_TARGET = $(LIBRARY).a
    ifeq ($(UNAME),Darwin)
        # Mac
        SO_PLAIN  = $(LIBRARY).dylib
        SO_MAIN   = $(LIBRARY).$(SO_VERSION).dylib
        SO_TARGET = $(LIBRARY).$(VERSION).dylib
        SO_OPTS  += -dynamiclib -compatibility_version $(SO_VERSION) \
                    -current_version $(VERSION) \
                    -shared -undefined dynamic_lookup
        # When a Mac *.dylib file is moved, this command is required
        # to change its internal name to match its location in the filesystem:
        SO_INSTALL_NAME = install_name_tool -id
    else
        # Linux and other variants of Unix
        SO_PLAIN  = $(LIBRARY).so
        SO_MAIN   = $(LIBRARY).so.$(SO_VERSION)
        SO_TARGET = $(LIBRARY).so.$(VERSION)
        SO_OPTS  += -shared -Wl,-soname -Wl,$(SO_MAIN) # -Wl,--no-undefined
        # Linux/Unix *.so files can be moved without modification:
        SO_INSTALL_NAME = echo
    endif
endif

