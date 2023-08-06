#===============================================================================
# CG_DESCENT/Lib/Makefile: for compiling the static CG_DESCENT library
#===============================================================================

LIBRARY = libcg_descent
VERSION = 6.8.0

default: library

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

library: $(AR_TARGET)

#-------------------------------------------------------------------------------

I = -I$(SUITESPARSE)/include -I$(SUITEOPT)/include
	
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
	$(SUITEOPT)/include/pproj.h \
	$(SUITEOPT)/include/pproj_check.h \
	$(SUITEOPT)/include/pproj_print.h \
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
# The CG_DESCENT library
#-------------------------------------------------------------------------------

OBJ = cg_descent.o \
	pasa_cg_descent.o \
	cg_util.o \
	cg_default.o \
	cg_print.o

$(AR_TARGET): $(OBJ)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OBJ): $(INCLUDE)

#-----------------------------------------------------
# CGDESCENT Object files
#-----------------------------------------------------
cg_descent.o: ../Source/cg_descent.c
	$(C) -c $(I) $<

cg_default.o: ../Source/cg_default.c
	$(C) -c $(I) $<

cg_util.o: ../Source/cg_util.c
	$(C) -c $(I) $<

cg_print.o: ../Source/cg_print.c
	$(C) -c $(I) $<

pasa_cg_descent.o: ../Source/cg_descent.c
	$(C) -DPASA -c $(I) $< -o $@
