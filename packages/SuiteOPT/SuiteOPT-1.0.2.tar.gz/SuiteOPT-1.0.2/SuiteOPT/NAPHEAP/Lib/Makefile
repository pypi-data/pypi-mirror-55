#===============================================================================
# NAPHEAP/Lib/Makefile: for compiling the NAPHEAP library
#===============================================================================

LIBRARY = libnapheap
VERSION = 3.0.0

default: library

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

library: $(AR_TARGET)

#-------------------------------------------------------------------------------

I = -I$(SUITEOPT)/include -I$(SUITEOPT)/NAPHEAP/Include
	
#-------------------------------------------------------------------------------

C = $(CC) $(CF)

purge: distclean

distclean: clean
	- $(RM) -r $(PURGE)

clean:
	- $(RM) -r $(CLEAN)

#-------------------------------------------------------------------------------
# SuiteOPT/include directory contains all include files:
#-------------------------------------------------------------------------------
INCLUDE = Makefile \
	$(SUITEOPT)/SuiteOPTconfig/Userconfig.mk \
	$(SUITEOPT)/SuiteOPTconfig/SuiteOPTconfig.mk \
	$(SUITEOPT)/NAPHEAP/Include/napheap_internal.h \
	$(SUITEOPT)/include/napheap.h \
	$(SUITEOPT)/include/SuiteOPTconfig.h

OBJ = napheap.o \
	napheap_default.o \
	napheap_print.o \
	napheap_check.o

$(AR_TARGET): $(OBJ)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OBJ): $(INCLUDE)

#-------------------------------------
# NAPHEAP Object files
#-------------------------------------
napheap.o: ../Source/napheap.c ../Source/napminmaxheap.c
	$(C) -c $(I) $<

napheap_default.o: ../Source/napheap_default.c
	$(C) -c $(I) $<

napheap_check.o: ../Source/napheap_check.c
	$(C) -c $(I) $<

napheap_print.o: ../Source/napheap_print.c
	$(C) -c $(I) $<
