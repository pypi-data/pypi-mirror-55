#---------------------------------------------------------------------------
# specify the compiler
#---------------------------------------------------------------------------
CC = gcc

#---------------------------------------------------------------------------
# set the optimization level
#---------------------------------------------------------------------------

# optimization level 3 and no debugging:
OPTFLAGS = -O3 -DNDEBUG

# when debugging code, comment out the line above, uncomment the following line
#OPTFLAGS = -W -Wall -pedantic -Wmissing-prototypes \
	-Wredundant-decls -Wnested-externs -Wdisabled-optimization \
	-fexceptions -Wno-parentheses -Wshadow -Wcast-align \
	-Winline -Wstrict-prototypes -Wno-unknown-pragmas -g -DNSUPER

#---------------------------------------------------------------------------
# specify the BLAS, LAPACK, and LDLIBS
#---------------------------------------------------------------------------

# For openblas, use something like the following:
BLAS = -lopenblas -lgfortran -lpthread
LAPACK = -llapack
LDLIBS =
OPTFLAGS += -DNSUPER

# For Intel's mkl BLAS, use something like the following:
#BLAS = -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -liomp5 -lpthread
#LAPACK = -lmkl_lapack95_lp64
#LDLIBS = -L/opt/intel/mkl/lib/intel64 \
#    -L/opt/intel/compilers_and_libraries_2019.4.243/linux/compiler/lib/intel64
