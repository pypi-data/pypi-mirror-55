/* ---------- napheap mex function ---------- */
/* This file contains the mex function for interfacing napheap with MATLAB */

/* ---------- Include header files ---------- */
#include "napheap_matlab.h"

/* mex function */
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    /* Initialize input variables */
    double *lambda ;
    int status, DiffLen ;
    bool Malloc_a ;
    long i ;
    char *mystr, *outstr ;
    size_t  buflen ;
    NAPdata *napdata ; 
    mxArray *lhs[1], *rhs, *field ;
    const mxArray *options ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf ("Initialized variables\n") ;
    #endif

    /* If the user provided no input then print some options */
    if (nrhs == 0)
    {
        /* Print additional information note for user */
        napheap_matlab_print_info () ;

        /* Nothing to solve, terminate program */
        return ;
    }

    /*------- Initialize napheap data struct -------- */
    napdata = napheap_setup () ;

    /* If user provided one input then print default parameter values */
    if ((nrhs == 1) && mxIsChar(prhs[0]))
    {
        /* String must be input as row vector */
        if (mxGetM(prhs[0])!=1)
          mexErrMsgIdAndTxt( "MATLAB:napheap:inputNotVector",
                  "napheap help keyword must be a row vector.") ;

        /* Set length of string */
        buflen = (mxGetM(prhs[0]) * mxGetN(prhs[0])) + 1;
    
        /* Allocate memory for output string */
        outstr = mxCalloc(buflen, sizeof(char));
    
        /* Copy string from prhs[0] to string in C */
        mystr = mxArrayToString(prhs[0]);
        
        if(mystr == NULL) 
          mexErrMsgIdAndTxt("MATLAB:napheap:conversionFailed",
                  "Input could not be converted to string.");

        /* check string against valid keywords */
        if (!strcmp(mystr, "readme"))
        {
            /* Print readme information about napheap */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "help") ;
        }
        else if (!strcmp(mystr, "parm"))
        {
            /* Print default napheap parameter values and descriptions */
            napheap_print_parm (napdata) ;
        }
        else if (!strcmp(mystr, "demo"))
        {
            /* Open demo file for napheap */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else{/* Invalid option string provided for napheap */ 
            printf("\n Invalid keyword enetered for napheap information.\n") ;
        }

        /* Print additional information note for user */
        napheap_matlab_print_info () ;

        napheap_terminate (&napdata) ;

        /* Exit program as there is nothing to evaluate */
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

    /* Verify correct number of input arguments provided for NAPHEAP */
    if(nrhs > 1)
    {
        mexErrMsgIdAndTxt("MyToolbox:napheap:nrhs",
                          "napheap requires exactly 1 struct as an input.");
    }

    /* Verify correct number of output arguments provided for NAPHEAP */
    if(nlhs < 1 || nlhs > 3)
    {
        mexErrMsgIdAndTxt("MyToolbox:napheap:nlhs",
                          "napheap requires at least 1 output "
                          "and allows at most 3 outputs.");
    }

    #if DEBUG_NAPHEAP_MEX
    mexPrintf ("Finished prhs error messages\n") ;
    #endif

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Loading problem parameters from struct\n") ;
    #endif

    /* Call external function to import parameters */
    napheap_matlab_get_parm(options, napdata->Parm) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Imported user napheap parameters\n") ;
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
    if ( napdata->n == EMPTY )
    {
        if ( napdata->Parm->d_is_one == TRUE )
        {
            mexPrintf("napheap could not determine the problem dimension "
                      "from the provided data.\n") ;
            mexErrMsgTxt("Terminating napheap.\n") ;
 
        }
        mexErrMsgTxt("User did not provide napheap an objective.\n") ;
        mexErrMsgTxt("Terminating napheap.\n") ;
    }
                                
    /* Print warning message if vectors have different lengths */
    if (DiffLen)
    {
        mexPrintf("Problem dimension is assumed to be %i based on the "
                  "provided data.\n", napdata->n) ;
    }

    /* lambda: Scalar multiplier for linear constraint a'*x */
    suiteopt_matlab_get_scalar (options, &(napdata->lambda), "lambda") ;

    /* --- a (linear constraint): Initialize to ones if not provided --- */
    if (napdata->a == NULL)
    {
        /* a not provided, allocate memory for a */
        mexPrintf("a not provided. Setting a to default of ones(%d,1).\n", 
                  napdata->n);

        /* Allocate memory for a */
        napdata->a = (double *) mxMalloc ((napdata->n) * sizeof(double)) ;
        Malloc_a = TRUE ;

        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Allocated memory for a.\n");
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

    /* --- x (Solution): Can now allocate memory since n has been set --- */
    if ((field = mxGetField(options, 0, "x")) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            /* -------- Configure initial output values  -------- */
            /* Copy initial guess for x into first output plhs[0] */
            plhs[0] = mxDuplicateArray(field) ;
        
            #if DEBUG_NAPHEAP_MEX
            mexPrintf("Successfully set plhs[0].\n") ;
            #endif

            /* Copy value for x */
            napdata->x = mxGetPr(plhs[0]) ;  

            #if DEBUG_NAPHEAP_MEX
            mexPrintf("Successfully imported initial guess x.\n") ;
            #endif
        }
        else /* x must be of type double, print error message */
        {
            mexPrintf("Initial guess x provided to napheap "
                      "must be of type double.\n") ;
            mexErrMsgTxt("Terminating napheap.\n") ;
        }
    }
    else
    {/* x not provided to napheap */
        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Initial guess x not provided.\n");
        #endif

        /* Initialize pointer for the first output of plhs */
        plhs[0] = mxCreateDoubleMatrix (napdata->n, 1, mxREAL) ;
        /* Copy value for x */
        napdata->x = mxGetPr(plhs[0]) ;  

        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Allocated memory for x.\n");
        #endif
    }

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Completed importing all prhs.\n") ;
    #endif

    #if DEBUG_NAPHEAP_MEX
    /* Print all elements imported from user's data */
    napheap_matlab_print_data (napdata) ;
    mexPrintf("Completed printing all prhs.\n") ;
    #endif

    /* -------- Run napheap on problem -------- */
    status = napheap (napdata) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Finished running napheap.\n") ;
    #endif

    /* -------- Store any remaining output values -------- */
    if (nlhs > 1)
    {
        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Storing napheap statistics for output.\n") ;
        #endif

        /* Store napheap statistics in second output */
        napheap_matlab_get_stat(&plhs[1], napdata->Stat) ;

        #if DEBUG_NAPHEAP_MEX
        mexPrintf("Stored napheap statistics successfully.\n") ;
        #endif
    }
    if (nlhs > 2)
    {
        plhs [2] = mxCreateDoubleScalar (napdata->lambda) ;
    }

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Set additional output variables successfully\n") ;
    #endif

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Wrapping up and preparing to exit.\n") ;
    #endif

    napheap_matlab_wrapup (napdata, Malloc_a) ;

    #if DEBUG_NAPHEAP_MEX
    mexPrintf("Exiting napheap.\n") ;
    #endif

    return ;
}
