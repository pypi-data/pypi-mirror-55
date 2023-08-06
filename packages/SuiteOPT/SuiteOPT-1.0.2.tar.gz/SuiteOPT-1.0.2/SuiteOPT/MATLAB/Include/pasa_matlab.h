/* --- PASA functions required by more than one mex function --- */
/* This file contains function prototypes associated with PASA 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* --- Include header files --- */
#include "suiteopt_matlab.h"
#include "cg_descent_matlab.h"
#include "napheap_matlab.h"
#include "pproj_matlab.h"
#include "pasa.h"

/* --- Function prototypes for PASA in SuiteOPT MEX functions --- */
void pasa_matlab_print_info () ;

void pasa_matlab_get_parm (
    const mxArray *options, /* Pointer to struct containing user problem data */
    PASAparm *Parm          /* Pointer to pasa parm struct */
) ;

void pasa_matlab_get_parms (
    const mxArray *options, /* Pointer to struct containing user problem data */
    PASAparms *Parms        /* Pointer to PASAparms struct */
) ;

void pasa_matlab_get_stat (
    mxArray **out, /* mxArray in which pasa statistics will be stored */
    PASAstat *Stat /* Pointer to pasa stats struct with all solver stats */
) ;

void pasa_matlab_get_stats (
    mxArray **out,    /* mxArray in which pasa statistics will be stored */
    PASAstats *Stats, /* Pointer to pasa stats struct with all solver stats */
    int Aexists       /* 0 if no constraint matrix A; 1 otherwise */
) ;

void pasa_matlab_print_data (
    PASAdata *data   /* Pointer to pasa data struct with problem data */ 
) ;
