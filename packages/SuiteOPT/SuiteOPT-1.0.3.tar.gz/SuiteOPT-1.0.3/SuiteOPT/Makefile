#===============================================================================
# SuitOPT/Makefile:
#===============================================================================
USERCONFIG = $(realpath $(CURDIR))/SuiteOPTconfig/Userconfig.mk
export USERCONFIG
# For python configuration, add flags to LDLIBS
PYSUITEOPT_RPATH ?=
export PYSUITEOPT_RPATH
# End customization for python configuration

default: all

all:
	( cd SuiteSparseX ; $(MAKE) purge )
	( cd SuiteSparseX ; $(MAKE) install )
	( cd NAPHEAP/Demo ; $(MAKE) )
	( cd PPROJ/Demo ; $(MAKE) )
	( cd CGDESCENT/Demo ; $(MAKE) )
	( cd PASA/Demo  ; $(MAKE) )

#-------------------------------------
# Python - Makes shared libraries
#-------------------------------------

py:
	( cd SuiteSparseX ; $(MAKE) install )
	( cd NAPHEAP/LibPy ; $(MAKE) )
	( cd PPROJ/LibPy ; $(MAKE) )
	( cd CGDESCENT/LibPy ; $(MAKE) )
	( cd PASA/LibPy  ; $(MAKE) )

#-------------------------------------------------------------------------
# Lib - SuiteSparseX dynamic & static libraries + SuiteOPT static libraries
#-------------------------------------------------------------------------

lib:
	( cd SuiteSparseX ; $(MAKE) purge )
	( cd SuiteSparseX ; $(MAKE) install )
	( cd NAPHEAP/Lib ; $(MAKE) )
	( cd PPROJ/Lib ; $(MAKE) )
	( cd CGDESCENT/Lib  ; $(MAKE) )
	( cd PASA/Lib  ; $(MAKE) )

#-------------------------------------------------
# SuiteSparseX - Makes dynamic and static libraries
#-------------------------------------------------
suitesparse:
	( cd SuiteSparseX ; $(MAKE) purge )
	( cd SuiteSparseX ; $(MAKE) install )

#-------------------------------------
# pasacute - CUTEst interface to pasa
#-------------------------------------
pasacute:
	( cd PASA/CUTEst  ; $(MAKE) )

#----------------------------------------
# cgcute - CUTEst interface to cg_descent
#----------------------------------------
cgcute:
	( cd CGDESCENT/CUTEst  ; $(MAKE) )

#-----------------------------------------------
# cute - CUTEst interface to cg_descent and pasa
#-----------------------------------------------
cute:
	( cd PASA/CUTEst  ; $(MAKE) )
	( cd CGDESCENT/CUTEst  ; $(MAKE) )

#-------------------------------------
# Purge
#-------------------------------------

purge:
	( cd PPROJ ; $(MAKE) purge )
	( cd PASA  ; $(MAKE) purge )
	( cd NAPHEAP ; $(MAKE) purge )
	( cd CGDESCENT ; $(MAKE) purge )
	( cd SuiteSparseX ; $(MAKE) purge )
	- $(RM) lib/*

#-------------------------------------
# Clean
#-------------------------------------

clean:
	( cd PPROJ ; $(MAKE) clean )
	( cd PASA  ; $(MAKE) clean )
	( cd NAPHEAP ; $(MAKE) clean )
	( cd CGDESCENT ; $(MAKE) clean )
	( cd SuiteSparseX ; $(MAKE) clean )
