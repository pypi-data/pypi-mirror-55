#===============================================================================
# CG_DESCENT/Demo/Makefile: For compiling the CG_DESCENT demo
#===============================================================================

default: ccode

include ../../SuiteOPTconfig/SuiteOPTconfig.mk

# C code only:
ccode: run_cg_descent run_cg_descentQP

I = -I$(SUITEOPT)/include

C = $(CC) $(CFLAGS) $(OPTFLAGS) $(I)

LIB = ../Lib/libcg_descent.a -lm $(BLAS) $(LAPACK)

INCLUDE = Makefile \
	$(SUITEOPT)/include/cg_descent.h \
	$(SUITEOPT)/include/pasa.h \
	$(SUITEOPT)/include/SuiteOPTconfig.h \
	$(SUITEOPT)/SuiteOPTconfig/Userconfig.mk \
	$(SUITEOPT)/SuiteOPTconfig/SuiteOPTconfig.mk

#-------------------------------------
# run_cg_descent
#-------------------------------------

run_cg_descent: lib $(INCLUDE) run_cg_descent.c
	$(C) -o run_cg_descent run_cg_descent.c $(LDLIBS) $(LIB)

#-------------------------------------
# run_cg_descentQP
#-------------------------------------

run_cg_descentQP: lib $(INCLUDE) run_cg_descentQP.c
	$(C) -o run_cg_descentQP run_cg_descentQP.c $(LDLIBS) $(LIB)

#-------------------------------------
# Purge
#-------------------------------------

purge:
	- $(RM) run_cg_descent
	- $(RM) run_cg_descentQP

#-------------------------------------
# Clean
#-------------------------------------

clean:
	- $(RM) $(CLEAN)

#-------------------------------------
# Lib
#-------------------------------------

lib:
	( cd ../Lib ; $(MAKE) )
