#===============================================================================
# NAPHEAP/Demo/Makefile: For compiling the NAPHEAP demo
#===============================================================================

default: ccode

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

# C code only:
ccode: run_napheap

I = -I$(SUITEOPT)/include -I$(SUITEOPT)/NAPHEAP/Include

C = $(CC) $(CF) $(I)

LIB = ../Lib/libnapheap.a -lm

#-------------------------------------------------------------------------------
# SuiteOPT/include directory contains all include files except internal ones:
#-------------------------------------------------------------------------------
INCLUDE = Makefile \
	$(SUITEOPT)/SuiteOPTconfig/Userconfig.mk \
	$(SUITEOPT)/SuiteOPTconfig/SuiteOPTconfig.mk \
	$(SUITEOPT)/NAPHEAP/Include/napheap_internal.h \
	$(SUITEOPT)/include/napheap.h \
	$(SUITEOPT)/include/SuiteOPTconfig.h

#-------------------------------------
# run_napheap
#-------------------------------------

run_napheap: lib $(INCLUDE) run_napheap.c
	$(C) -o run_napheap run_napheap.c $(LDLIBS) $(LIB)

#-------------------------------------
# Purge
#-------------------------------------

purge:
	- $(RM) run_napheap

#-------------------------------------
# Lib
#-------------------------------------
lib:
	( cd ../Lib ; $(MAKE) )
