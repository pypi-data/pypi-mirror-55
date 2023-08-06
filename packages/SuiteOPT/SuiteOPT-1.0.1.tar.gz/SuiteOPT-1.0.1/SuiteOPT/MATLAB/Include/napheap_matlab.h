/* --- NAPHEAP functions required by more than one mex function --- */
/* This file contains function prototypes associated with NAPHEAP 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* --- Include header files --- */
#include "suiteopt_matlab.h"
#include "napheap.h"

/* --- Function prototypes for NAPHEAP in SuiteOPT MEX functions --- */
void napheap_matlab_print_info () ;

void napheap_check_matlab_print_info () ;

void napheap_matlab_get_objective (
    const mxArray *options, /* User provided struct to mex function */
    NAPdata *data,          /* Struct in which to store pproj problem data */
    int *DiffLen            /* Increment DiffLen each time len(data) != n */
) ;

void napheap_matlab_get_napsack_constraints (
    const mxArray *options, /* User provided struct to mex function */
    NAPdata *data,          /* Struct in which to store pproj problem data */
    int *DiffLen            /* Increment DiffLen each time len(data) != n */
) ;

void napheap_matlab_get_parm (
    const mxArray *options, /* Pointer to struct containing user problem data */
    NAPparm *Parm           /* Pointer to napheap parm struct */
) ;

void napheap_matlab_get_stat (
    mxArray **out, /* mxArray in which napheap statistics will be stored */
    NAPstat *Stat  /* Pointer to napheap stats struct with problem stats */
) ;

void napheap_matlab_print_data (
    NAPdata *data   /* Pointer to napheap data struct with problem data */ 
) ;

void napheap_matlab_wrapup (
    NAPdata *data,  /* Pointer to napheap data struct with problem data */ 
    bool Malloc_a   /* TRUE if mex function malloc'd a, FALSE otherwise */
) ;
