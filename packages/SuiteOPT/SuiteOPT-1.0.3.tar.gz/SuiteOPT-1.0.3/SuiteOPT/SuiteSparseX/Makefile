#-------------------------------------------------------------------------------
# Makefile for all SuiteSparse packages
#-------------------------------------------------------------------------------

SUITESPARSE = $(CURDIR)
export SUITESPARSE

default: go

include SuiteSparse_config/SuiteSparse_config.mk

# Compile the default rules for each package
go: metis
	( cd SuiteSparse_config && $(MAKE) )
	( cd AMD && $(MAKE) )
	( cd CAMD && $(MAKE) )
	( cd CCOLAMD && $(MAKE) )
	( cd COLAMD && $(MAKE) )
	( cd CHOLMOD && $(MAKE) )

# install all packages in /usr/local/lib and /usr/local/include
# (note that CSparse is not installed; CXSparse is installed instead)
install: metisinstall
	( cd SuiteSparse_config && $(MAKE) install )
	( cd AMD && $(MAKE) install )
	( cd CAMD && $(MAKE) install )
	( cd CCOLAMD && $(MAKE) install )
	( cd COLAMD && $(MAKE) install )
	( cd CHOLMOD && $(MAKE) install )
	$(CP) README.txt $(INSTALL_DOC)/SuiteSparse_README.txt
	chmod 644 $(INSTALL_DOC)/SuiteSparse_README.txt

metisinstall: metis
ifeq (,$(MY_METIS_LIB))
        # install METIS from SuiteSparse/metis-5.1.0
	@mkdir -p $(INSTALL_LIB)
	@mkdir -p $(INSTALL_INCLUDE)
	@mkdir -p $(INSTALL_DOC)
	- $(CP) lib/libmetis.* $(INSTALL_LIB)
	- $(CP) metis-5.1.0/manual/manual.pdf $(INSTALL_DOC)/METIS_manual.pdf
	- $(CP) metis-5.1.0/README.txt $(INSTALL_DOC)/METIS_README.txt
        # the following is needed only on the Mac, so *.dylib is hardcoded:
	$(SO_INSTALL_NAME) $(INSTALL_LIB)/libmetis.dylib $(INSTALL_LIB)/libmetis.dylib
	- $(CP) include/metis.h $(INSTALL_INCLUDE)
	chmod 755 $(INSTALL_LIB)/libmetis.*
	chmod 644 $(INSTALL_INCLUDE)/metis.h
	chmod 644 $(INSTALL_DOC)/METIS_manual.pdf
	chmod 644 $(INSTALL_DOC)/METIS_README.txt
endif

# uninstall all packages
uninstall:
	$(RM) $(INSTALL_DOC)/SuiteSparse_README.txt
	( cd SuiteSparse_config && $(MAKE) uninstall )
	- ( cd metis-5.1.0 && $(MAKE) uninstall )
	( cd AMD && $(MAKE) uninstall )
	( cd CAMD && $(MAKE) uninstall )
	( cd COLAMD && $(MAKE) uninstall )
	( cd CCOLAMD && $(MAKE) uninstall )
	( cd CHOLMOD && $(MAKE) uninstall )
ifeq (,$(MY_METIS_LIB))
        # uninstall METIS, which came from SuiteSparse/metis-5.1.0
	$(RM) $(INSTALL_LIB)/libmetis.*
	$(RM) $(INSTALL_INCLUDE)/metis.h
	$(RM) $(INSTALL_DOC)/METIS_manual.pdf
	$(RM) $(INSTALL_DOC)/METIS_README.txt
endif
	$(RM) -r $(INSTALL_DOC)

# compile the dynamic libraries.  For GraphBLAS and Mongoose, this also builds
# the static library
library: metis
	( cd SuiteSparse_config && $(MAKE) )
	( cd AMD && $(MAKE) library )
	( cd CAMD && $(MAKE) library )
	( cd CCOLAMD && $(MAKE) library )
	( cd COLAMD && $(MAKE) library )
	( cd CHOLMOD && $(MAKE) library )

# compile the static libraries (except for metis, GraphBLAS, and Mongoose).
# metis is only dynamic, and the 'make static' for GraphBLAS and Mongoose makes
# both the dynamic and static libraries.
static: metis
	( cd SuiteSparse_config && $(MAKE) static )
	( cd AMD && $(MAKE) static )
	( cd CAMD && $(MAKE) static )
	( cd CCOLAMD && $(MAKE) static )
	( cd COLAMD && $(MAKE) static )
	( cd CHOLMOD && $(MAKE) static )

# Remove all files not in the original distribution
purge:
	- ( cd SuiteSparse_config && $(MAKE) purge )
	- ( cd metis-5.1.0 && $(MAKE) distclean )
	- ( cd AMD && $(MAKE) purge )
	- ( cd CAMD && $(MAKE) purge )
	- ( cd COLAMD && $(MAKE) purge )
	- ( cd CCOLAMD && $(MAKE) purge )
	- ( cd CHOLMOD && $(MAKE) purge )
	- ( cd MATLAB_Tools/SuiteSparseCollection && $(RM) *.mex* )
	- ( cd MATLAB_Tools/SSMULT && $(RM) *.mex* )
	- $(RM) MATLAB_Tools/*/*.mex* MATLAB_Tools/spok/private/*.mex*
	- $(RM) -r include/* bin/* lib/* share/*

# Remove all files not in the original distribution, but keep the libraries
clean:
	- ( cd SuiteSparse_config && $(MAKE) clean )
	- ( cd metis-5.1.0 && $(MAKE) clean )
	- ( cd AMD && $(MAKE) clean )
	- ( cd CAMD && $(MAKE) clean )
	- ( cd COLAMD && $(MAKE) clean )
	- ( cd CCOLAMD && $(MAKE) clean )
	- ( cd CHOLMOD && $(MAKE) clean )

# Create the PDF documentation
docs:
	( cd AMD && $(MAKE) docs )
	( cd CAMD && $(MAKE) docs )
	( cd CHOLMOD && $(MAKE) docs )

distclean: purge

# statement coverage (Linux only); this requires a lot of time.
# The umfpack tcov requires a lot of disk space in /tmp
cov: purge
	( cd CHOLMOD && $(MAKE) cov )

# configure and compile METIS, placing the libmetis.* library in
# SuiteSparse/lib and the metis.h include file in SuiteSparse/include.
metis: include/metis.h

# Install the shared version of METIS in SuiteSparse/lib.
# The SO_INSTALL_NAME commmand is only needed on the Mac, so *.dylib is
# hardcoded below.
include/metis.h:
ifeq (,$(MY_METIS_LIB))
	- ( cd metis-5.1.0 && $(MAKE) config shared=1 prefix=$(SUITESPARSE) cc=$(CC) )
	- ( cd metis-5.1.0 && $(MAKE) )
	- ( cd metis-5.1.0 && $(MAKE) install )
	- $(SO_INSTALL_NAME) $(SUITESPARSE)/lib/libmetis.dylib \
                             $(SUITESPARSE)/lib/libmetis.dylib
else
	@echo 'Using pre-installed METIS 5.1.0 library at ' '[$(MY_METIS_LIB)]'
endif
