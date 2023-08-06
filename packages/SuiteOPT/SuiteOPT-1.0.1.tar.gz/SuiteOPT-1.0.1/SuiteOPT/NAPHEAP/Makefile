#-------------------------------------------------------------------------------
# napheap makefile
#-------------------------------------------------------------------------------

default: all

# compile the C-callable library and the Demo program
all:
	( cd Demo ; $(MAKE) )

# compile the C-callable library only
lib: 
	( cd Lib ; $(MAKE) )

libpy: 
	( cd LibPy ; $(MAKE) )

# remove all but the distributed files
purge:
	( cd Demo ; $(MAKE) purge )
	( cd Lib  ; $(MAKE) purge )
	( cd LibPy  ; $(MAKE) purge )
	( cd Test ; $(MAKE) purge )
	( cd MATLAB ; $(RM) *.mex* *.o *.obj )

distclean: purge

# remove all files not in the original distribution, except keep the
# compiled libraries and programs
clean:
	( cd Demo ; $(MAKE) clean )
	( cd Lib  ; $(MAKE) clean )
	( cd LibPy  ; $(MAKE) clean )
	( cd Test ; $(MAKE) clean )
	- $(RM) MATLAB/*.mex* MATLAB/*.o MATLAB/*.obj

# run the exhaustive test suite
tests:
	( cd Test ; $(MAKE) )

# run the exhaustive test suite with statement coverage
cov:
	( cd Test ; $(MAKE) cov )

# run the exhaustive test suite with valgrind (requires Linux)
valgrind:
	( cd Demo ; $(MAKE) valgrind )
	( cd Test ; $(MAKE) valgrind )
