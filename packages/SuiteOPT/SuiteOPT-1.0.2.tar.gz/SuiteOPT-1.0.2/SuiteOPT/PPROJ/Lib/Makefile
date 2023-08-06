#===============================================================================
# PPROJ/Lib/Makefile: for compiling the PPROJ library
#===============================================================================

LIBRARY = libpproj
VERSION = 2.0.0

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
# The PPROJ library is composed of PPROJ and CHECK
#-------------------------------------------------------------------------------

PPROJ = pproj.o \
	pproj_default.o \
	pproj_print.o \
	pproj_init.o \
	pproj_phase1.o \
	pproj_hotchol.o \
	pproj_coor_ascent.o \
	pproj_dasa.o \
	pproj_sparsa.o \
	pproj_ssor0.o \
	pproj_ssor1.o

CHECK = pproj_checkA.o \
	pproj_checkF.o \
	pproj_check_AFT.o \
	pproj_check_AT.o \
	pproj_check_back.o \
	pproj_checkb.o \
	pproj_checkc.o \
	pproj_check_const.o \
	pproj_checkD.o \
	pproj_check_diag3.o \
	pproj_check_diag.o \
	pproj_check_dual.o \
	pproj_check_eqn5.o \
	pproj_check_forward.o \
	pproj_check_line.o \
	pproj_check_link.o \
	pproj_check_minheap.o \
	pproj_check_modlist.o \
	pproj_check_deriv.o \
	pproj_check_order.o

OBJ = $(PPROJ) $(CHECK)

$(AR_TARGET): $(OBJ)
	$(ARCHIVE) $@ $^
	- $(RANLIB) $@

$(OBJ): $(INCLUDE)

#-------------------------------------
# PPROJ Object files
#-------------------------------------

pproj.o: ../Source/pproj.c
	$(C) -c $(I) $<

pproj_default.o: ../Source/pproj_default.c
	$(C) -c $(I) $<

pproj_print.o: ../Source/pproj_print.c
	$(C) -c $(I) $<

pproj_init.o: ../Source/pproj_init.c
	$(C) -c $(I) $<

pproj_phase1.o: ../Source/pproj_phase1.c
	$(C) -c $(I) $<

pproj_hotchol.o: ../Source/pproj_hotchol.c
	$(C) -c $(I) $<

pproj_coor_ascent.o: ../Source/pproj_coor_ascent.c
	$(C) -c $(I) $<

pproj_dasa.o: ../Source/pproj_dasa.c
	$(C) -c $(I) $<

pproj_sparsa.o: ../Source/pproj_sparsa.c
	$(C) -c $(I) $<

pproj_ssor0.o: ../Source/pproj_ssor0.c
	$(C) -c $(I) $<

pproj_ssor1.o: ../Source/pproj_ssor1.c
	$(C) -c $(I) $<

#-------------------------------------
# Check Object files
#-------------------------------------

pproj_checkA.o: ../Check/pproj_checkA.c
	$(C) -c $(I) $<

pproj_checkF.o: ../Check/pproj_checkF.c
	$(C) -c $(I) $<

pproj_check_AFT.o: ../Check/pproj_check_AFT.c
	$(C) -c $(I) $<

pproj_check_AT.o: ../Check/pproj_check_AT.c
	$(C) -c $(I) $<

pproj_check_back.o: ../Check/pproj_check_back.c
	$(C) -c $(I) $<

pproj_checkb.o: ../Check/pproj_checkb.c
	$(C) -c $(I) $<

pproj_checkc.o: ../Check/pproj_checkc.c
	$(C) -c $(I) $<

pproj_check_const.o: ../Check/pproj_check_const.c
	$(C) -c $(I) $<

pproj_checkD.o: ../Check/pproj_checkD.c
	$(C) -c $(I) $<

pproj_check_diag3.o: ../Check/pproj_check_diag3.c
	$(C) -c $(I) $<

pproj_check_diag.o: ../Check/pproj_check_diag.c
	$(C) -c $(I) $<

pproj_check_dual.o: ../Check/pproj_check_dual.c
	$(C) -c $(I) $<

pproj_check_dualsimple.o: ../Check/pproj_check_dualsimple.c
	$(C) -c $(I) $<

pproj_check_eqn5.o: ../Check/pproj_check_eqn5.c
	$(C) -c $(I) $<

pproj_check_forward.o: ../Check/pproj_check_forward.c
	$(C) -c $(I) $<

pproj_check_line.o: ../Check/pproj_check_line.c
	$(C) -c $(I) $<

pproj_check_link.o: ../Check/pproj_check_link.c
	$(C) -c $(I) $<

pproj_check_minheap.o: ../Check/pproj_check_minheap.c
	$(C) -c $(I) $<

pproj_check_modlist.o: ../Check/pproj_check_modlist.c
	$(C) -c $(I) $<

pproj_check_deriv.o: ../Check/pproj_check_deriv.c
	$(C) -c $(I) $<

pproj_check_order.o: ../Check/pproj_check_order.c
	$(C) -c $(I) $<
