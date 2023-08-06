/* --- PPROJ functions required by more than one mex function --- */
/* This file contains function prototypes associated with PPROJ 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* --- Include header files --- */
#include "suiteopt_matlab.h"
#include "pproj.h"

/* --- Function prototypes for PPROJ in SuiteOPT MEX functions --- */
void pproj_matlab_print_info () ;

void pproj_matlab_get_parm
(
    const mxArray *options, /* Pointer to struct containing user problem data */
    PPparm *Parm            /* Pointer to pproj parm struct */
) ;

void pproj_matlab_get_stat
(
    mxArray **out, /* mxArray in which pproj statistics will be stored */
    PPstat *Stat   /* Pointer to pproj stats struct with problem stats */
) ;

void pproj_matlab_print_data
(
    PPdata *data   /* Pointer to pproj data struct with problem data */ 
) ;
