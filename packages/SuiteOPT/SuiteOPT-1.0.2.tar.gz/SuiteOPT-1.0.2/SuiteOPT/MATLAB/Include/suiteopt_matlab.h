/* --- Routines required by more than one mex function in SuiteOPT --- */
/* This file contains function prototypes associated with calls 
   in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Define MIN and MAX for MEX functions ---------- */
#define TRUE SuiteOPTtrue
#define FALSE SuiteOPTfalse
#define SUITEOPTMAX(a,b) (((a) > (b)) ? (a) : (b))
#define SUITEOPTMIN(a,b) (((a) < (b)) ? (a) : (b))

/* --- Include header files and define macros --- */
#include "SuiteOPTconfig.h"
#ifdef CGDESCENT_MATLAB
#define SUITEOPT_MATLAB_SOLVER "cg_descent"
#define SUITEOPT_MATLAB_N n
#elif NAPHEAP_MATLAB
#include "napheap.h"
#define SUITEOPT_MATLAB_SOLVER "napheap"
#define SUITEOPT_MATLAB_N n
#elif PPROJ_MATLAB
#include "pproj.h"
#define SUITEOPT_MATLAB_SOLVER "pproj"
#define SUITEOPT_MATLAB_N ncol
#elif PASA_MATLAB
#include "pasa.h"
#define SUITEOPT_MATLAB_SOLVER "pasa"
#define SUITEOPT_MATLAB_N ncol
#endif

/* --- Function prototypes found in SuiteOPT MEX functions --- */
/* Define external variables used in function evaluation routines */
extern mxArray *suiteopt_value ;
extern mxArray *suiteopt_grad ;
extern mxArray *suiteopt_valgrad ;
extern mxArray *suiteopt_hprod ;
extern mxArray *cg_hprod ;

/* Routine for evalating objective function */
void suiteopt_matlab_value
(
    SuiteOPTfloat *val, /* Final (scalar) function value stored in val */
    SuiteOPTfloat *x,   /* Evaluate objective function at x */
    SuiteOPTint n       /* Length of x */
) ;

/* Routine for evalating gradient of objective function */
void suiteopt_matlab_grad
(
    SuiteOPTfloat *g, /* Final gradient stored in g */
    SuiteOPTfloat *x, /* Evaluate gradient at x */
    SuiteOPTint n     /* Length of x */
) ;

/* Routine for evalating objective and gradient */
void suiteopt_matlab_valgrad
(
    SuiteOPTfloat *val, /* Final (scalar) function value stored in val */
    SuiteOPTfloat *g,   /* Final gradient stored in g */
    SuiteOPTfloat *x,   /* Evaluate objective function at x */
    SuiteOPTint n       /* Length of x */
) ;

/* Routine for computing hessian (with free indices) times vector (for PASA) */
void suiteopt_matlab_hprod
(
    SuiteOPTfloat *p,   /* Product Hx stored in p */
    SuiteOPTfloat *x,   /* Multiply hessian times x */
    SuiteOPTint *ifree, /* Indices of free components */
    SuiteOPTint n,      /* Length of x */
    SuiteOPTint nf      /* Number of free components */
) ;

/* Routine for computing CGDESCENT hessian times vector */
void suiteopt_matlab_cghprod
(
    SuiteOPTfloat *p, /* Product Hx stored in p */
    SuiteOPTfloat *x, /* Multiply hessian times x */
    SuiteOPTint n     /* Length of x */
) ;

/* TODO: Not available for use with PASA version 1.0.0 */
#if 0
/* Routine for evaluating hessian of objective function (for PASA) */
void suiteopt_matlab_hprod(
    PASAhess *val /* Pointer to struct containing objective Hessian values */
) ;
#endif

/* --- Function prototypes found in SuiteOPT MEX functions --- */
SuiteOPTfloat * suiteopt_matlab_get_float
(
    const mxArray *options, /* User provided struct to mex function */
    long int *n,            /* Pointer to current problem dimension */
    int *DiffLen,           /* Increment DiffLen by 1 if len(data) != n */
    char *data_name         /* String for name of element to set pointer for */
) ;

void suiteopt_matlab_get_scalar
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTfloat *output,  /* Ptr to var to set equal to usr data (if given) */
    char *data_name         /* String for name of element to set pointer for */
) ;

void suiteopt_matlab_get_int
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTint *output,    /* Ptr to var to set equal to usr data (if given) */
    char *data_name         /* String for name of element to set pointer for */
) ;

void suiteopt_matlab_get_problem_dimension
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTint *n          /* Pointer to problem dimension variable */
) ;

void suiteopt_matlab_get_bound_constraints
(
    const mxArray *options,  /* User provided struct to mex function */
#ifdef NAPHEAP_MATLAB
    NAPdata *data,           /* Struct in which to store pproj problem data */
#elif PPROJ_MATLAB
    PPdata *data,            /* Struct in which to store pproj problem data */
#elif PASA_MATLAB
    PASAdata *data,          /* Struct in which to store pasa problem data */
#endif
    int *DiffLen             /* Increment DiffLen each time len(data) != n */
) ;

void suiteopt_matlab_get_polyhedral_constraints
(
    const mxArray *options  /* User provided struct to mex function */
#ifdef PPROJ_MATLAB
    ,PPdata * data          /* Struct in which to store pproj problem data */
#elif PASA_MATLAB
    ,PASAdata * data        /* Struct in which to store pasa problem data */
#endif
) ;

mxArray* suiteopt_matlab_get_func
(
    const mxArray *options, /* User provided struct to mex function */
    int inputs,             /* Correct number of input args for function */
    int outputs,            /* Correct number of output args for function */
    char *data_name         /* String for name of element to set pointer for */
) ;

void suiteopt_matlab_copy_arr
(
    SuiteOPTfloat *y, /* output of copy */
    SuiteOPTfloat *x, /* input of copy */
    int            n  /* length of vectors */
) ;
