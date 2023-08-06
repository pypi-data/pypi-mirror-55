#===============================================================================
# PASA/Lib/Makefile: for compiling the PASA shared object library
#===============================================================================

LIBRARY = libpasa
VERSION = 1.0.0
SO_VERSION = 1

default: library

ccode: all

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

LDLIBS += -lpproj -lcg_descent -lnapheap -lcholmod -lamd -lcamd -lcolamd \
	-lccolamd -lmetis -lsuitesparseconfig $(LAPACK) $(BLAS)

SO_OPTS += $(CFOPENMP)

# compile and install in SuiteOPT/lib
library:
	$(MAKE) install INSTALL=$(SUITEOPT)

#-------------------------------------------------------------------------------

I = -I$(SUITESPARSE)/include -I$(SUITEOPT)/include
	
#-------------------------------------------------------------------------------

C = $(CC) $(CF) -fPIC

all: library

purge: distclean

distclean: clean
	- $(RM) -r $(PURGE)

clean:
	- $(RM) -r $(CLEAN)

#-------------------------------------------------------------------------------
# SuiteOPT/include directory contains all include files:
#-------------------------------------------------------------------------------
INCLUDE = Makefile \
	$(SUITEOPT)/SuiteOPTconfig/SuiteOPTconfig.mk \
	$(SUITEOPT)/include/pproj.h \
	$(SUITEOPT)/include/pproj_check.h \
	$(SUITEOPT)/include/pproj_print.h \
	$(SUITEOPT)/include/cg_descent.h \
	$(SUITEOPT)/include/napheap.h \
	$(SUITEOPT)/include/SuiteOPTconfig.h \
	$(SUITESPARSE)/include/cholmod_blas.h \
	$(SUITESPARSE)/include/cholmod_check.h \
	$(SUITESPARSE)/include/cholmod_cholesky.h \
	$(SUITESPARSE)/include/cholmod_complexity.h \
	$(SUITESPARSE)/include/cholmod_config.h \
	$(SUITESPARSE)/include/cholmod_core.h \
	$(SUITESPARSE)/include/cholmod.h \
	$(SUITESPARSE)/include/cholmod_matrixops.h \
	$(SUITESPARSE)/include/cholmod_modify.h \
	$(SUITESPARSE)/include/cholmod_partition.h \
	$(SUITESPARSE)/include/cholmod_supernodal.h \
	$(SUITESPARSE)/include/cholmod_template.h \
	$(SUITESPARSE)/include/amd.h \
	$(SUITESPARSE)/include/ccolamd.h \
	$(SUITESPARSE)/include/SuiteSparse_config.h \
	$(SUITESPARSE)/include/colamd.h \
	$(SUITESPARSE)/include/metis.h

#-------------------------------------------------------------------------------
# The PASA library
#-------------------------------------------------------------------------------

OBJ = pasa.o \
	pasa_default.o \
	pasa_print.o

$(OBJ): $(INCLUDE)

#-------------------------------------
# PPROJ Object files
#-------------------------------------

pasa.o: ../Source/pasa.c \
	../Source/pasa_default.c \
	../Source/pasa_print.c \
	../../CGDESCENT/Source/cg_descent.c \
	../../CGDESCENT/Source/cg_default.c \
	../../CGDESCENT/Source/cg_print.c
	$(C) -c $(I) $<

pasa_default.o: ../Source/pasa_default.c
	$(C) -c $(I) $<

pasa_print.o: ../Source/pasa_print.c
	$(C) -c $(I) $<

#-------------------------------------------------------------------------------

# install PPROJ
install: $(INSTALL_LIB)/$(SO_TARGET)

$(INSTALL_LIB)/$(SO_TARGET): $(OBJ)
	@mkdir -p $(INSTALL_LIB)
	$(CC) $(SO_OPTS) $^ -o $@ $(LDLIBS)
	( cd $(INSTALL_LIB) ; ln -sf $(SO_TARGET) $(SO_PLAIN) )
	( cd $(INSTALL_LIB) ; ln -sf $(SO_TARGET) $(SO_MAIN) )

# uninstall PPROJ
uninstall:
	$(RM) $(INSTALL_LIB)/$(SO_TARGET)
	$(RM) $(INSTALL_LIB)/$(SO_PLAIN)
	$(RM) $(INSTALL_LIB)/$(SO_MAIN)
