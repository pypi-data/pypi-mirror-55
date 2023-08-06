#===============================================================================
# NAPHEAP/Lib/Makefile: for compiling the NAPHEAP shared object library
#===============================================================================

LIBRARY = libnapheap
VERSION = 3.0.0
SO_VERSION = 3

default: library

ccode: all

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

SO_OPTS += $(CFOPENMP)

# compile and install in SuiteOPT/lib
library:
	$(MAKE) install INSTALL=$(SUITEOPT)

#-------------------------------------------------------------------------------

I = -I$(SUITEOPT)/include -I$(SUITEOPT)/NAPHEAP/Include
	
#-------------------------------------------------------------------------------

C = $(CC) $(CF) -fPIC

all: library

purge: distclean

distclean: clean
	- $(RM) -r $(PURGE)

clean:
	- $(RM) -r $(CLEAN)

#-------------------------------------------------------------------------------
# SuiteOPT/include directory contains all include files except internal files
#-------------------------------------------------------------------------------
INCLUDE = Makefile \
	$(SUITEOPT)/SuiteOPTconfig/SuiteOPTconfig.mk \
	$(SUITEOPT)/NAPHEAP/Include/napheap_internal.h \
	$(SUITEOPT)/include/napheap.h \
	$(SUITEOPT)/include/SuiteOPTconfig.h

OBJ = napheap.o \
	napheap_default.o \
	napheap_print.o \
	napheap_check.o

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
#-------------------------------------------------------------------------------

# install NAPHEAP
install: $(INSTALL_LIB)/$(SO_TARGET)

$(INSTALL_LIB)/$(SO_TARGET): $(OBJ)
	@mkdir -p $(INSTALL_LIB)
	$(CC) $(SO_OPTS) $^ -o $@ $(LDLIBS)
	( cd $(INSTALL_LIB) ; ln -sf $(SO_TARGET) $(SO_PLAIN) )
	( cd $(INSTALL_LIB) ; ln -sf $(SO_TARGET) $(SO_MAIN) )

# uninstall NAPHEAP
uninstall:
	$(RM) $(INSTALL_LIB)/$(SO_TARGET)
	$(RM) $(INSTALL_LIB)/$(SO_PLAIN)
	$(RM) $(INSTALL_LIB)/$(SO_MAIN)
