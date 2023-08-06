/* ---------- napheap_check mex function ---------- */
/* This file contains a mex function for using napheap_check with MATLAB */

/* ---------- Include header files ---------- */
#include "napheap_matlab.h"

/* mex function */
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    /* Initialize input variables */
    double *lambda ;
    double inf = mxGetInf ( ) ;
    NAPFLOAT err, errb, errB, erry ;
    bool Malloc_a ;
    int DiffLen ;
    long i ;
    NAPdata *napdata ; 
    mxArray *field ;
    const mxArray *options ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf ("Initialized variables\n") ;
    #endif

    /* If the user provided no input then print some options */
    if (nrhs == 0)
    {
        /* Print additional information note for user */
        napheap_check_matlab_print_info () ;

        /* Nothing to solve, terminate program */
        return ;
    }

    /* Check if user provided nonempty struct as input */
    if ((nrhs >= 1) && (mxIsClass(prhs[0], "struct")) && !mxIsEmpty(prhs[0]))
    {
        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Loading problem data struct\n") ;
        #endif

        /* Copy input to options */
        options = prhs[0] ;
    }

    /* Verify correct number of input arguments provided for napheap_check */
    if(nrhs > 1)
    {
        mexErrMsgIdAndTxt("MyToolbox:napheap_check:nrhs",
                          "napheap_check requires exactly 1 struct as "
                          "an input.");
    }

    /* Verify correct number of output arguments provided for napheap_check */
    if(nlhs < 1 || nlhs > 4)
    {
        mexErrMsgIdAndTxt("MyToolbox:napheap_check:nlhs",
                          "napheap_check requires at least 1 output "
                          "and allows at most 4 outputs.");
    }

    #if DEBUG_NAPHEAP_MEX
    mexPrintf ("napheap_check: Finished prhs error messages\n") ;
    #endif

    /*------- Initialize napheap data struct -------- */
    napdata = napheap_setup () ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Loading problem parameters from struct\n") ;
    #endif

    /* Call external function to import parameters */
    napheap_matlab_get_parm (options, napdata->Parm) ;
    
    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Imported user NAPHEAP parameters\n") ;
    #endif

    /* Initialize checks for internal control */
    Malloc_a = FALSE ;
    DiffLen = 0 ;

    /* ----------- Import problem options provided in input struct ------- */
    /* n: Problem dimension */
    suiteopt_matlab_get_problem_dimension (options, &(napdata->n)) ;

    /* d, y: Objective function data */
    napheap_matlab_get_objective (options, napdata, &DiffLen) ;

    /* blo, bhi, a: Napsack constraints blo <= a'*x <= bhi */
    napheap_matlab_get_napsack_constraints (options, napdata, &DiffLen) ;

    /* lo, hi: Bound constraints lo <= x <= hi */
    suiteopt_matlab_get_bound_constraints (options, napdata, &DiffLen) ;
                                    
    /* lambda: Scalar multiplier for linear constraint a'*x */
    suiteopt_matlab_get_scalar (options, &(napdata->lambda), "lambda") ;
                                
    /* Print warning message if vectors have different lengths */
    if (DiffLen)
    {
        mexPrintf("Problem dimension is assumed to be %i based on the "
                  "provided data.\n", napdata->n) ;
    }

    /* --- a (linear constraint): Initialize to ones if not provided --- */
    if (napdata->a == NULL)
    {
        /* a not provided, allocate memory for a */
        #if DEBUG_NAPHEAP_MEX
        mexPrintf("a not provided. Setting a to default of ones(%d,1).\n", 
                  napdata->n) ;
        #endif

        /* Allocate memory for a */
        napdata->a = (double *) mxMalloc ((napdata->n) * sizeof(double)) ;
        Malloc_a = TRUE ;

        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Allocated memory for a.\n") ;
        #endif

        /* Fill a with ones */
        for (i = 0; i < napdata->n; i++)
        {
            napdata->a[i] = 1 ;
        }

        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Initialized a to ones(%d,1).\n", napdata->n);
        #endif
    }

    /* --- x (Solution) --- */
    if ((field = mxGetField(options, 0, "x")) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            /* -------- Configure initial output values  -------- */
            /* Copy initial guess for x */
            napdata->x = mxGetPr(field) ;

            #if DEBUG_NAPHEAP_MEX
            mexPrintf("Successfully imported initial guess x.\n") ;
            #endif
        }
        else /* x must be of type double Print error message */
        {
            mexPrintf("Solution x provided to napheap_check "
                      "must be of type double.\n") ;
            mexErrMsgTxt("Terminating napheap_check.\n") ;
        }
    }
    else /* x not provided to napheap_check */
    {
        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Solution x not provided.\n");
        #endif

        mexPrintf("Solution x not provided to napheap_check "
                  "but is required.\n") ;
        mexErrMsgTxt("Terminating napheap_check.\n") ;
    }

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Completed importing all prhs.\n") ;
    #endif

    #if DEBUG_NAPHEAP_MEX
    /* Print all elements imported from user's data */
    napheap_matlab_print_data (napdata) ;
    mexPrintf("Completed printing all prhs.\n") ;
    #endif

    /* -------- Run napheap_check on problem -------- */
    err = napheap_check (&errb, &errB, &erry, napdata) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Finished running napheap_check.\n") ;
    #endif

    /* -------- Store output values -------- */
    plhs [0] = mxCreateDoubleScalar (err) ;
    if (nlhs > 1) plhs [1] = mxCreateDoubleScalar (errb) ;
    if (nlhs > 2) plhs [2] = mxCreateDoubleScalar (errB) ;
    if (nlhs > 3) plhs [3] = mxCreateDoubleScalar (erry) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Set output variables successfully\n") ;
    #endif

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Wrapping up and preparing to exit.\n") ;
    #endif

    napheap_matlab_wrapup (napdata, Malloc_a) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Exiting napheap_check.\n") ;
    #endif

    return ;
}
