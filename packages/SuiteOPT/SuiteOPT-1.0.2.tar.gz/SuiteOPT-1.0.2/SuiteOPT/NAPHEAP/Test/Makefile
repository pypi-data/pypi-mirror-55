#-------------------------------------------------------------------------------
# Test/Makefile for napheap exhaustive test
#-------------------------------------------------------------------------------

# include napheap.mk: use SuiteOPTconfig.mk instead
include ../../SuiteOPTconfig/SuiteOPTconfig.mk

# compile and run the tests (both normal and brutal)
all: naptest naptest_brutal
	./naptest > /tmp/output_naptest.txt
	./naptest_brutal > /tmp/output_naptest_brutal.txt

tests: all

test: all

SRC = ../Source/napheap.c ../Source/napheap_default.c \
	../Source/napheap_print.c ../Source/napheap_check.c naptest.c
INC = Makefile ../Include/napheap.h ../Include/napheap_internal.h \
	../../SuiteOPTconfig/SuiteOPTconfig.h \
	../../SuiteOPTconfig/SuiteOPTconfig.mk
LIB = -lm
I = -I../Include -I../../SuiteOPTconfig

C = $(CC) $(CFLAGS) $(OPTFLAGS) $(I)

naptest: $(SRC) $(INC)
	$(C) -o naptest $(SRC) $(LIB)

naptest_brutal: $(SRC) $(INC)
	$(C) $(I) -DNAPSACK_BRUTAL -o naptest_brutal $(SRC) $(LIB)

# run the brutal test with statement coverage
cov:
	gcc -DNAPSACK_BRUTAL -g -W -Wall -pedantic -Wmissing-prototypes \
	    -Wredundant-decls -Wnested-externs -Wdisabled-optimization \
	    -std=c99 -fexceptions -Wno-parentheses -Wshadow -Wcast-align \
            -Winline -Wstrict-prototypes -Wno-unknown-pragmas \
            -fprofile-arcs -ftest-coverage $(I) \
            -o cov_naptest $(SRC) $(LIB)
	./cov_naptest > /tmp/output_naptest_brutal_cov.txt
	gcov -f ../Source/napheap.c
	gcov -f ../Source/napheap_print.c
	gcov -f ../Source/napheap_check.c

# valgrind requires Linux
valgrind: naptest naptest_brutal
	valgrind --vgdb-error=1 ./naptest > /tmp/output_naptest_valgrind.txt
	valgrind --vgdb-error=1 ./naptest_brutal > /tmp/output_naptest_brutal_valgrind.txt

# remove all but the distributed files
purge: clean
	- $(RM) naptest naptest_brutal cov_naptest
	- $(RM) *.gcov /tmp/output_naptest*.txt
	- $(RM) -rf *.dSYM

distclean: purge

# remove all files not in the original distribution, except keep the
# compiled libraries and programs
clean:
	- $(RM) *.o *.gcno *.gcda bugprob.txt bugprob.m *.obj
