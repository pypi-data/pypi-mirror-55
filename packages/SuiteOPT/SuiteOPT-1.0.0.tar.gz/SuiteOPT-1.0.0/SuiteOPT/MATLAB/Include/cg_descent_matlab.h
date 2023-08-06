/* --- CGDESCENT functions required by more than one mex function --- */
/* This file contains function prototypes associated with CGDESCENT 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* --- Include header files --- */
#include "suiteopt_matlab.h"
#include "cg_descent.h"

/* --- Function prototypes for CGDESCENT in SuiteOPT MEX functions --- */
void cg_matlab_print_info () ;

void cg_matlab_get_parm (
    const mxArray *options, /* Pointer to struct containing user problem data */
    CGparm *Parm            /* Pointer to cg parameter struct */
) ;

void cg_matlab_get_stat (
    mxArray **out, /* mxArray in which cg statistics will be stored */
    CGstat *Stat   /* Pointer to cg stats struct with problem statistics */
) ;
