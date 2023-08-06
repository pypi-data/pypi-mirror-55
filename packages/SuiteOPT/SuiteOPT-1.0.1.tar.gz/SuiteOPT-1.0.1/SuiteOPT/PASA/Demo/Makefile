#===============================================================================
# PASA/Demo/Makefile: For compiling the PASA demo
#===============================================================================

default: ccode

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

# C code only:
ccode: run_pasa

I = -I$(SUITESPARSE)/include -I$(SUITEOPT)/include

C = $(CC) $(CF) $(I)

LIB = ../Lib/libpasa.a \
	$(SUITEOPT)/PPROJ/Lib/libpproj.a \
	$(SUITEOPT)/NAPHEAP/Lib/libnapheap.a \
	$(SUITEOPT)/CGDESCENT/Lib/libcg_descent.a \
	$(SUITESPARSE)/CHOLMOD/Lib/libcholmod.a \
	$(SUITESPARSE)/AMD/Lib/libamd.a \
	$(SUITESPARSE)/CAMD/Lib/libcamd.a \
	$(SUITESPARSE)/CCOLAMD/Lib/libccolamd.a \
	$(SUITESPARSE)/COLAMD/Lib/libcolamd.a \
	$(SUITESPARSE)/lib/libmetis.so \
	$(SUITESPARSE)/SuiteSparse_config/libsuitesparseconfig.a \
	$(LAPACK) $(BLAS) $(XERBLA) -lm

#-------------------------------------------------------------------------------
# SuiteOPT/include directory contains all include files:
#-------------------------------------------------------------------------------
INCLUDE = Makefile \
	$(SUITEOPT)/SuiteOPTconfig/Userconfig.mk \
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

#-------------------------------------
# run_pasa
#-------------------------------------

run_pasa: lib $(INCLUDE) run_pasa.c
	$(C) -g -o run_pasa run_pasa.c $(LDLIBS) $(LIB) 

#-------------------------------------
# Purge
#-------------------------------------

purge:
	- $(RM) run_pasa

#-------------------------------------
# Lib
#-------------------------------------
lib:
	( cd ../Lib ; $(MAKE) )
