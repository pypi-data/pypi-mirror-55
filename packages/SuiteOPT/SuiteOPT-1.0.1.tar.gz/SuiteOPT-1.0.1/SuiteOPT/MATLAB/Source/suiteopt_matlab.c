/* --- Routines required by more than one mex function --- */
/* This file contains function definitions associated with 
   calls in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Include header files ---------- */
#include "suiteopt_matlab.h"

/* --- Wrappers for function handles to pass to C functions ----------------- */
#ifdef SUITEOPT_MATLAB_OBJ
/* Wrapper to evaluate user's objective function */
/* The arguments are converted to MATLAB's format, the user's function stored 
   in a global variable, suiteopt_matlab_value, and is evaluated using the  
   mxCallMATLAB statement. The output is converted back to correct type. */
void suiteopt_matlab_value
(
    SuiteOPTfloat *val, /* Final (scalar) function value stored in val */
    SuiteOPTfloat *x,   /* Evaluate objective function at x */
    SuiteOPTint n       /* Length of x */
)
{
    /* Initialize variables */
    mxArray *F, *ppFevalRhs [2], *X ;
    double *xcopy ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Evaluating suiteopt_matlab_value\n") ;
    #endif

    /* make copy of x */
    xcopy = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
    suiteopt_matlab_copy_arr (xcopy, x, n) ; 

    /* Set initial values */
    X = mxCreateDoubleMatrix(0,0,mxREAL) ;
    mxFree(mxGetPr(X)) ;
    mxSetPr(X, xcopy) ;
    mxSetN(X, 1) ;
    mxSetM(X, n) ;
   
    /* Evaluate function in MATLAB */
    ppFevalRhs[0] = suiteopt_value ;
    ppFevalRhs[1] = X ;
    /* This statement uses MATLAB's feval to evaluate cg_value (X) and
       return the single output in F */
    mexCallMATLAB(1, &F, 2, ppFevalRhs, "feval") ;

    /* Copy F into val */ 
    memcpy(val, mxGetPr(F), sizeof(SuiteOPTfloat)) ;

    /* Free memory */
    mxSetPr(X, NULL) ;
    mxFree(mxGetPr(X)) ;
    mxFree (xcopy) ;

    /* Exit function */
    return ; 
}

/* Wrapper to evaluate user's gradient function */
void suiteopt_matlab_grad
(
    SuiteOPTfloat *g, /* Final gradient stored in g */
    SuiteOPTfloat *x, /* Evaluate gradient at x */
    SuiteOPTint n     /* Length of x */
)
{
    /* Initialize variables */
    mxArray *G, *ppFevalRhs [2], *X ;
    double *xcopy ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Evaluating suiteopt_matlab_grad\n") ;
    #endif

    /* make copy of x */
    xcopy = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
    suiteopt_matlab_copy_arr (xcopy, x, n) ;

    /* Set initial values */
    X = mxCreateDoubleMatrix(0,0,mxREAL) ;
    mxFree(mxGetPr(X)) ;
    mxSetPr(X, xcopy) ;
    mxSetN(X, 1) ;
    mxSetM(X, n) ;
   
    /* Evaluate function in MATLAB */
    ppFevalRhs[0] = suiteopt_grad ;
    ppFevalRhs[1] = X ;
    mexCallMATLAB(1, &G, 2, ppFevalRhs, "feval") ;

    /* Copy values from G into g */ 
    memcpy(g, mxGetPr(G), sizeof(SuiteOPTfloat)*n) ;

    /* Free memory */
    mxSetPr(X, NULL) ;
    mxFree(mxGetPr(X)) ;
    mxFree (xcopy) ;

    /* Exit function */
    return ; 
}

/* Wrapper to evaluate user's valgrad function */
void suiteopt_matlab_valgrad
(
    SuiteOPTfloat *val, /* Final (scalar) function value stored in val */
    SuiteOPTfloat *g,   /* Final gradient stored in g */
    SuiteOPTfloat *x,   /* Evaluate objective function at x */
    SuiteOPTint n       /* Length of x */
)
{
    /* Initialize variables */
    mxArray *FG[2], *ppFevalRhs[2], *X ;
    double *xcopy ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Evaluating suiteopt_matlab_valgrad\n") ;
    #endif

    /* make copy of x */
    xcopy = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
    suiteopt_matlab_copy_arr (xcopy, x, n) ;

    /* Convert x to MATLAB's mxArray format */
    X = mxCreateDoubleMatrix(0,0,mxREAL) ;
    mxFree(mxGetPr(X)) ;
    mxSetPr(X, xcopy) ;
    mxSetN(X, 1) ;
    mxSetM(X, n) ;

    /* Evaluate function */
    ppFevalRhs[0] = suiteopt_valgrad ;
    ppFevalRhs[1] = X ;
    mexCallMATLAB(2, FG, 2, ppFevalRhs, "feval") ; 

    /* Copy values from FG into val and g */
    memcpy(val, mxGetPr(FG[0]), sizeof(SuiteOPTfloat)) ;
    memcpy(g, mxGetPr(FG[1]), sizeof(SuiteOPTfloat)*n) ;

    /* Free memory */
    mxSetPr(X, NULL) ;
    mxFree(mxGetPr(X)) ;
    mxFree (xcopy) ;

    /* Exit function */
    return ;
}
#endif

#ifdef SUITEOPT_MATLAB_HPROD
/* Routine for computing hessian (with free indices) times vector (for PASA) */
void suiteopt_matlab_hprod
(
    SuiteOPTfloat *p,   /* Product Hx stored in p */
    SuiteOPTfloat *x,   /* Multiply hessian times x */
    SuiteOPTint *ifree, /* Indices of free components */
    SuiteOPTint n,      /* Length of x */
    SuiteOPTint nf      /* Number of free components */
)
{
    /* Initialize variables */
    mxArray *I, *P, *X, *ppFevalRhs[3] ;
    double *xcopy, *nzIndices ;
    long i ;

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("Evaluating suiteopt_matlab_hprod in matlab\n") ;
    #endif

    /* make copy of x */
    xcopy = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
    pasa_copyx (xcopy, x, n) ;

    /* Set initial values */
    X = mxCreateDoubleMatrix(0, 0, mxREAL) ;
    mxFree(mxGetPr(X)) ;
    mxSetPr(X, xcopy) ;
    mxSetN(X, 1) ;
    mxSetM(X, n) ;

    /* Initialize nzIndices */
    I = mxCreateDoubleMatrix(0, 0, mxREAL) ;
    mxFree(mxGetPr(I)) ;
    mxSetN(I, 1) ;
    if ( ifree == NULL ) /* means all element of x are nonzero */
    {
        nzIndices = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
        mxSetPr(I, nzIndices) ;
        mxSetM(I,n) ;
        for (i = 0; i < n; i++)
        {
            nzIndices [i] = i + 1 ; /* +1 to convert C indices to MATLAB */
        }
    }
    else
    {
        nzIndices = mxMalloc (nf * sizeof(SuiteOPTfloat)) ;
        mxSetPr(I, nzIndices) ;
        mxSetM(I,nf) ;
        for (i = 0; i < nf; i++)
        {
            /* +1 to convert C indices to MATLAB */
            nzIndices [i] = ifree [i] + 1 ;
        }
    }

    /* Set initial values */
    ppFevalRhs [0] = suiteopt_hprod ;
    ppFevalRhs [1] = X ;
    ppFevalRhs [2] = I ;

    /* Evaluate function */
    mexCallMATLAB(1, &P, 3, ppFevalRhs, "feval") ; 

    /* Copy values from P into p */ 
    memcpy(p, mxGetPr(P), sizeof(SuiteOPTfloat)*n) ;

    /* Free memory */
    mxSetPr(X, NULL) ;
    mxFree(mxGetPr(X)) ;
    mxFree (xcopy) ;

    mxSetPr(I, NULL) ;
    mxFree(mxGetPr(I)) ;
    mxFree(nzIndices) ;

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("Finished evaluating suiteopt_matlab_hprod in matlab\n") ;
    #endif

    /* Exit function */
    return ; 
}
#endif

#ifdef SUITEOPT_MATLAB_CGHPROD
/* Routine for computing CGDESCENT hessian times vector */
void suiteopt_matlab_cghprod
(
    SuiteOPTfloat *p, /* Product Hx stored in p */
    SuiteOPTfloat *x, /* Multiply hessian times x */
    SuiteOPTint n     /* Length of x */
)
{
    /* Initialize variables */
    mxArray *P, *X, *ppFevalRhs[3] ;
    double *xcopy ;
    long i ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Evaluating suiteopt_matlab_cghprod\n") ;
    #endif

    /* make copy of x */
    xcopy = mxMalloc (n * sizeof(SuiteOPTfloat)) ;
    suiteopt_matlab_copy_arr (xcopy, x, n) ;

    /* Set initial values */
    X = mxCreateDoubleMatrix(0, 0, mxREAL) ;
    mxFree(mxGetPr(X)) ;
    mxSetPr(X, xcopy) ;
    mxSetN(X, 1) ;
    mxSetM(X, n) ;

    /* Set initial values */
    ppFevalRhs [0] = cg_hprod ;
    ppFevalRhs [1] = X ;

    /* Evaluate function */
    mexCallMATLAB(1, &P, 2, ppFevalRhs, "feval") ; 

    /* Copy values from P into p */ 
    memcpy(p, mxGetPr(P), sizeof(SuiteOPTfloat)*n) ;

    /* Free memory */
    mxSetPr(X, NULL) ;
    mxFree(mxGetPr(X)) ;
    mxFree (xcopy) ;

    /* Exit function */
    return ; 
}
#endif

/* --- Routines for importing problem data to MEX functions ----------------- */
/* Returns pointer to float with data_name if found in user struct,
   Otherwise returns NULL */
SuiteOPTfloat * suiteopt_matlab_get_float
(
    const mxArray *options, /* User provided struct to mex function */
    long int *n,            /* Pointer to current problem dimension */
    int *DiffLen,           /* Increment DiffLen[0] by 1 if len(data) != n,
                               Provide DiffLen = NULL to bypass this check */
    char *data_name         /* String for name of element to set pointer for */
)
{
    /* Initialize variables */
    long len ;
    mxArray *field ;

    if ((field = mxGetField(options, 0, data_name)) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            #ifdef DEBUG_SUITEOPT_MEX
            mexPrintf("%s::User provided data for %s.\n", 
                      SUITEOPT_MATLAB_SOLVER, data_name) ;
            #endif

            /* Determine if length of data and problem dimension should
               be compared */
            if (DiffLen != NULL)
            {
                /* Number of components of data */
                len = SUITEOPTMAX(mxGetM(field), mxGetN(field)) ;
                /* Check if problem dimension has been determined */
                if (n[0] <= 0)
                {
                    #ifdef DEBUG_SUITEOPT_MEX
                    mexPrintf("%s::Length of %s is %d and problem dimension"
                              " is %d.\n", SUITEOPT_MATLAB_SOLVER, data_name, 
                              len, n[0]) ;
                    mexPrintf("%s::Setting problem dimension equal to "
                              "%d.\n", SUITEOPT_MATLAB_SOLVER, len) ;
                    #endif
                    /* Set value of n to length of data */
                    n[0] = (long) len ;
                }
                else if (len < n[0])
                {
                    /* -- Set value of n to be min of len(data_name) and n -- */
                    mexPrintf("%s::Warning:Length of %s is %d and problem "
                              "dimension is %d.\n", SUITEOPT_MATLAB_SOLVER,  
                              data_name, len, n[0]) ;
                    mexPrintf("Setting problem dimension = length of %s.\n",
                              data_name) ;
    
                    /* Update prob dim and indicate diff lengths provided */
                    /* Set value of n */
                    n[0] = (long) len ;
    
                    #ifdef DEBUG_SUITEOPT_MEX
                    mexPrintf("%s::Updated problem dimension n = %ld.\n", 
                              SUITEOPT_MATLAB_SOLVER, n[0]) ;
                    #endif
    
                    /* Increment DiffLen by one */
                    DiffLen[0]++ ;
                }
                else if (len > n[0] )
                {
                    DiffLen[0]++ ;
                }
            }
            /* Return pointer to data */
            return mxGetPr (field) ;
        }
        else /* data must be of type double, Print error message */
        {
            mexPrintf("%s::Input data provided for %s must be of type double.\n"
                      ,SUITEOPT_MATLAB_SOLVER, data_name) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }
    }
    else /* data not provided to solver */
    {
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::Input data for %s not provided.\n", 
                  SUITEOPT_MATLAB_SOLVER, data_name) ;
        #endif
    }
    /* Data not provided. Return NULL pointer */
    return NULL ;
}

/* Sets scalar with data_name to output[0] if found in user struct */
void suiteopt_matlab_get_scalar
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTfloat *output,  /* Ptr to var to set equal to usr data (if given) */
    char *data_name         /* String for name of element to set pointer for */
)
{
    /* Initialize variables */
    mxArray *field ;

    if ((field = mxGetField(options, 0, data_name)) != NULL)
    {/* Copy value from field to output */
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::User provided data for %s.\n", 
                  SUITEOPT_MATLAB_SOLVER, data_name) ;
        #endif

        if (mxIsClass(field, "double")) {
            /* Copy value for user data */
            output[0] = mxGetScalar (field) ;  

            #ifdef DEBUG_SUITEOPT_MEX
            mexPrintf("%s::Successfully stored value of %f for %s.\n", 
                      SUITEOPT_MATLAB_SOLVER, output[0], data_name) ;
            #endif
        }
        else {/* blo must be of type double */
            /* Print error message */
            mexPrintf("%s::Input data provided for %s must be of type double.\n",
                      SUITEOPT_MATLAB_SOLVER, data_name) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }
    }
    else {/* Print error message */
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::Input data for %s not provided.\n", 
                  SUITEOPT_MATLAB_SOLVER, data_name) ;
        #endif
    }
}

/* Sets int with data_name to output[0] if found in user struct */
void suiteopt_matlab_get_int
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTint *output,    /* Ptr to var to set equal to usr data (if given) */
    char *data_name         /* String for name of element to set pointer for */
)
{
    /* Initialize variables */
    mxArray *field ;

    if ((field = mxGetField(options, 0, data_name)) != NULL)
    {/* Copy value from field to output */
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::User provided data for %s.\n", 
                  SUITEOPT_MATLAB_SOLVER, data_name) ;
        #endif

        if (mxIsClass(field, "double"))
        {
            /* Copy value for user data */
            output[0] = (SuiteOPTint) mxGetScalar (field) ;  

            #ifdef DEBUG_SUITEOPT_MEX
            mexPrintf("%s::Successfully stored value of %d for %s.\n", 
                      SUITEOPT_MATLAB_SOLVER, output[0], data_name) ;
            #endif
        }
        else /* blo must be of type double */
        {
            /* Print error message */
            mexPrintf("%s::Input data provided for %s must be of type double.\n"
                      ,SUITEOPT_MATLAB_SOLVER, data_name) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }
    }
    else /* Print error message */
    {
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::Input data for %s not provided.\n", 
                  SUITEOPT_MATLAB_SOLVER, data_name) ;
        #endif
    }
}


/* Import problem dimension (n) */
void suiteopt_matlab_get_problem_dimension
(
    const mxArray *options, /* User provided struct to mex function */
    SuiteOPTint         *n  /* Pointer to problem dimension variable */
)
{
    #if defined(NAPHEAP_MATLAB) || defined(CGDESCENT_MATLAB)
    /* n: Problem dimension (if provided) */
    suiteopt_matlab_get_int (options, n, "n") ;
    #else
    /* ncol: Problem dimension (if provided) */
    suiteopt_matlab_get_int (options, n, "ncol") ;
    #endif

    /* Exit function */
    return ;
}


#ifdef SUITEOPT_MATLAB_BOUND_CONSTRAINTS
/* Sets data associated w/ bound constraints of the form lo <= x <= hi */
/* Imports lo and hi */
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
)
{
    /* Initialize variables */
    mxArray *field ;

    /* lo: Bound constraint lo <= x */
    data->lo = suiteopt_matlab_get_float (options, &(data->SUITEOPT_MATLAB_N), 
                                          DiffLen, "lo") ;
    /* Check if lo not provided */
    if (data->lo == NULL)
    {
        /* Set parameter loExists to FALSE */
        #ifdef PASA_MATLAB
        data->Parms->pasa->loExists = FALSE ;
        #else
        data->Parm->loExists = FALSE ;
        #endif
    }

    /* hi: Bound constraint x <= hi */
    data->hi = suiteopt_matlab_get_float (options, &(data->SUITEOPT_MATLAB_N), 
                                          DiffLen, "hi") ;
    /* Check if hi not provided */
    if (data->hi == NULL)
    {
        /* Set parameter hiExists to FALSE */
        #ifdef PASA_MATLAB
        data->Parms->pasa->hiExists = FALSE ;
        #else
        data->Parm->hiExists = FALSE ;
        #endif
    }
}
#endif


#ifdef SUITEOPT_MATLAB_POLYHEDRAL_CONSTRAINTS
/* Sets data associated w/ polyhedral constraints of the form bl <= Ax <= bu */
/* Imports nrow, Ap, Ai, Ax, bl, and bu */
/* If PPROJ: Also imports nsing, row_sing singlo, singhi, singc */
void suiteopt_matlab_get_polyhedral_constraints
(
    const mxArray *options  /* User provided struct to mex function */
#ifdef PPROJ_MATLAB
    ,PPdata * data          /* Struct in which to store pproj problem data */
#elif PASA_MATLAB
    ,PASAdata * data        /* Struct in which to store pasa problem data */
#endif
)
{
    /* Initialize variables */
    mxArray *field ;
    int DiffLen ;
    /* Initialize DiffLen to 0 */
    DiffLen = 0 ;

    /* Verify that user provided polyhedral constraint matrix A */
    if ((field = mxGetField(options, 0, "A")) != NULL)
    {
        if (mxIsSparse(field)) 
        {
            #if DEBUG_SUITEOPT_MEX
            mexPrintf("%s::About to load matrix A\n", SUITEOPT_MATLAB_SOLVER) ;
            #endif

            /* Number of rows in A */
            data->nrow = mxGetM (field) ;
            /* Number of cols in A */
            data->ncol = mxGetN (field) ;
            /* Column pointers for A */
            data->Ap = mxGetJc (field) ; 
            /* Row indices for A */
            data->Ai = mxGetIr (field) ; 
            /* Matrix values for A */
            data->Ax = mxGetPr (field) ; 
            
            #if DEBUG_SUITEOPT_MEX
            mexPrintf("%s::Loaded A successfully\n", SUITEOPT_MATLAB_SOLVER) ;
            #endif
        }
        else
        {
            /* Print error message */
            mexPrintf("%s::Matrix for polyhedral constraint set provided must "
                      "be in sparse format.\n", SUITEOPT_MATLAB_SOLVER) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }

        /* Since A provided, user must provide at least one of bl and bu. */
        /* bl: Polyhedral lower bound bl <= Ax */
        long nrow ;
        nrow = (long) -1 ;
        data->bl = suiteopt_matlab_get_float (options, &nrow, 
                                              &DiffLen, "bl");
        /* bu: Polyhedral upper bound Ax <= bu */
        data->bu = suiteopt_matlab_get_float (options, &nrow, 
                                              &DiffLen, "bu");
        /* Check if user provided at least one of bl and bu */
        if ((data->bl == NULL) && (data->bu == NULL))
        {
            /* Print error message and terminate */
            mexPrintf("%s::Matrix for polyhedral constraint set provided "
                      "but bl or bu not provided.\n", SUITEOPT_MATLAB_SOLVER) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }

        if ( nrow < data->nrow )
        {
            mexPrintf("\n%s::Number of rows %ld in polyhedral constraint "
                      "matrix is more than the\n"
                      "number of components %ld in a constraint vector "
                      "bl or bu\n",
                      SUITEOPT_MATLAB_SOLVER, nrow, data->nrow) ;
            mexErrMsgTxt("\n") ;
        }

        /* --- Additional polyhedral data associated exclusively with PPROJ */
        #ifdef PPROJ_MATLAB
            /* Since A provided, user may provide nsing. Check and import */
            if ((field = mxGetField(options, 0, "nsing")) != NULL)
            {/* Copy pointer from field to nsing */
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Value provided for nsing.\n") ;
                #endif
    
                data->nsing = (long) mxGetScalar (field) ;  
    
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Successfully imported value for nsing.\n") ;
                #endif
            }
    
            /* Since A provided, user may provide row_sing. Check and import */
            if ((field = mxGetField(options, 0, "row_sing")) != NULL)
            {/* Copy pointer from field to row_sing */
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::User provided row_sing.\n") ;
                #endif
    
                data->row_sing = mxGetIr (field) ;  
    
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Successfully imported row_sing.\n") ;
                #endif
            }
    
            /* Since A provided, user may provide singlo. Check and import */
            if ((field = mxGetField(options, 0, "singlo")) != NULL)
            {/* Copy pointer from field to singlo */
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::User provided singlo.\n") ;
                #endif
    
                data->singlo = mxGetPr (field) ;  
    
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Successfully imported singlo.\n") ;
                #endif
            }
    
            /* Since A provided, user may provide singhi. Check and import */
            if ((field = mxGetField(options, 0, "singhi")) != NULL)
            {/* Copy pointer from field to singhi */
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::User provided singhi.\n") ;
                #endif
    
                data->singhi = mxGetPr (field) ;  
    
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Successfully imported singhi.\n") ;
                #endif
            }
    
            /* Since A provided, user may provide singc. Check and import */
            if ((field = mxGetField(options, 0, "singc")) != NULL)
            {/* Copy pointer from field to singc */
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::User provided singc.\n") ;
                #endif
    
                data->singc = mxGetPr (field) ;  
    
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj::Successfully imported singc.\n") ;
                #endif
            }
        #endif
    }
    #ifdef PASA_MATLAB
    else if ((field = mxGetField(options, 0, "a")) != NULL)
    {/* User provided vector a instead of matrix */
        /* Setting nrow = 1 */
        data->nrow = 1 ;

        /* a: Linear constraint vector */
        data->a = suiteopt_matlab_get_float (options, &(data->ncol), NULL, "a");
        data->ncol = SUITEOPTMAX(mxGetM(field), mxGetN(field)) ;

        /* bl (scalar in this case): Lower bound on linear constraint a'*x */
        suiteopt_matlab_get_scalar (options, data->bl, "bl") ;

        /* bu (scalar in this case): Upper bound on linear constraint a'*x */
        suiteopt_matlab_get_scalar (options, data->bu, "bu") ;

        /* If user did not provide bl and bu terminate program */ 
        if ((data->bl == NULL) && (data->bu == NULL))
        {
            /* Print error message */
            mexPrintf("%s::Vector a for napsack constraints provided "
                      "but bl and bu not provided.\n", SUITEOPT_MATLAB_SOLVER) ;
            mexErrMsgTxt("Terminating program.\n") ;
        }
    }
    #endif
    else /* Neither A nor a provided. Set Ap, Ai, Ax, a, bl, and bu to NULL */
    {
        /* Setting nrow = 0 */
        data->nrow = 0 ;

        /* Print warning message */
        #if DEBUG_SUITEOPT_MEX
            #ifdef PPROJ_MATLAB
            mexPrintf("%s::Matrix A not provided. Ap, Ai, Ax, bl, bu, "
                      "set to NULL.\n", SUITEOPT_MATLAB_SOLVER) ;
            mexPrintf("pproj::row_sing, singlo, "
                      "singhi, and singc set to NULL.\n") ;
            mexPrintf("pproj::ni and nsing set to default values.\n");
            #elif PASA_MATLAB
            mexPrintf("%s::Matrix A and vector a not provided. Ap, Ai, Ax, a, "
                      "bl, bu, set to NULL.\n", SUITEOPT_MATLAB_SOLVER) ;
            mexPrintf("%s::Set nrow = 0.\n", SUITEOPT_MATLAB_SOLVER) ;
            #endif
        #endif
    }
}
#endif

/* Returns pointer to function handle with data_name if found in user struct,
   Otherwise returns NULL pointer */
mxArray* suiteopt_matlab_get_func
(
    const mxArray *options, /* User provided struct to mex function */
    int inputs,             /* Correct number of input args for function */
    int outputs,            /* Correct number of output args for function */
    char *data_name         /* String for name of element to set pointer for */
)
{
    /* --- Initialize variables --- */
    int nargsin, nargsout ;
    mxArray *lhs[1], *rhs, *field ;

    /* --- Function handle for objective --- */
    if ((field = mxGetField(options, 0, data_name)) != NULL)
    {
        if (mxIsClass(field, "function_handle")) {
            /* ----- Check number of input and output arguments ----- */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) field ;
            /* Call MATLAB function nargin and store output in lhs[0] */
            mexCallMATLAB(1, lhs, 1, &rhs, "nargin") ;
            /* Cast lhs[0] to integer nargsin */
            nargsin = (int) mxGetScalar (lhs[0]) ;
            /* Call MATLAB function nargout and store output in lhs[0] */
            mexCallMATLAB(1, lhs, 1, &rhs, "nargout") ;
            /* Cast lhs[0] to integer nargsout */
            nargsout = (int) mxGetScalar (lhs[0]) ;

            #ifdef DEBUG_SUITEOPT_MEX
            mexPrintf("%s::Number of input arguments for %s: %i\n", 
                      SUITEOPT_MATLAB_SOLVER, data_name, nargsin) ;
            mexPrintf("%s::Number of output arguments for %s: %i\n", 
                      SUITEOPT_MATLAB_SOLVER, data_name, nargsout) ;
            #endif

            if ((nargsin == inputs) && 
                ((nargsout == outputs) || (nargsout == -outputs))) 
            {
                #ifdef DEBUG_SUITEOPT_MEX
                mexPrintf("%s::Successfully imported function handle '%s'.\n",
                          SUITEOPT_MATLAB_SOLVER, data_name) ;
                #endif

                /* Return handle for function evaluation */
                return (mxArray*) field ;
            }
            else {/* Incorrect number of input and output args */
                mexPrintf("%s::Function handle for %s provided to pasa "
                          "has incorrect number of arguments.\n", 
                          SUITEOPT_MATLAB_SOLVER, data_name) ;
                mexPrintf("%s::Function handle for %s must have %d input "
                          "argument(s) and %d output argument(s).\n",
                          SUITEOPT_MATLAB_SOLVER, data_name, inputs, outputs) ;
                mexErrMsgTxt("Terminating program.") ;
            }
        }
        else {/* objective must be a function handle */
            /* Print error message */
            mexPrintf("%s::Function handle for %s must have %d input "
                      "argument(s) and %d output argument(s).\n",
                      SUITEOPT_MATLAB_SOLVER, data_name, inputs, outputs) ;
            mexErrMsgTxt("Terminating cg_descent.") ;
        }
    }
    else {/* objective not provided to pasa */
        #ifdef DEBUG_SUITEOPT_MEX
        mexPrintf("%s::Function handle for %s not provided. Returning NULL "
                  "pointer.\n", SUITEOPT_MATLAB_SOLVER, data_name);
        #endif
    }

    /* Function handle not found. Returning NULL */
    return NULL ;
}

/* --- Utility functions used in SuiteOPT MEX functions --- */
/* Copy vector x into vector y */
void suiteopt_matlab_copy_arr
(
    SuiteOPTfloat *y, /* output of copy */
    SuiteOPTfloat *x, /* input of copy */
    int            n  /* length of vectors */
)
{
    int i, n5 ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; )
    {
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
    }
    return ;
}
