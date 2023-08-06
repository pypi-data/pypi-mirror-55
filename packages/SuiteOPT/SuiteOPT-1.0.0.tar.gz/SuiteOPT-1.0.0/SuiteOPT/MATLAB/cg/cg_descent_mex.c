/* ---------- cg_descent mex function ---------- */
/* This file contains the mex function for interfacing cg_descent with MATLAB */

/* ---------- Include header files ---------- */
#include "cg_descent_matlab.h"

/* ---------- Declare global variables ---------- */
mxArray *suiteopt_value ;
mxArray *suiteopt_grad ;
mxArray *suiteopt_valgrad ;
mxArray *cg_hprod ;

/* mex function */
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    /* Initialize input variables */
    double *x, *c ;
    bool FoundValue, FoundGrad, FoundValgrad, FoundHprod, FoundC ;
    long i, n ;
    char *mystr ;
    mxArray *lhs[1], *rhs, *field ;
    const mxArray *options ;

    /* Initialize output variables */
    double *status, status_value ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf ("Initialized variables\n") ;
    #endif

    /* If the user provided no input then print some options */
    if (nrhs == 0)
    {
        /* Print additional information note for user */
        cg_matlab_print_info () ;

        /* Nothing to solve, terminate program */
        return ;
    }

    /* Verify correct number of input arguments provided for PASA */
    if(nrhs > 1)
    {
        mexErrMsgIdAndTxt("MyToolbox:pasa:nrhs",
                          "pasa requires exactly one struct as an input.") ;
    }

    int string_input = mxIsChar(prhs[0]) ;

    /* Any string must be input as row vector */
    if ( string_input )
    {
        if ( mxGetM(prhs[0])!=1 )
        {
            mexErrMsgIdAndTxt("MATLAB:cg_descent:inputNotVector",
                    "cg_descent help keyword must be a row vector.") ;
        }

        /* Copy string from prhs[0] to string in C */
        mystr = mxArrayToString(prhs[0]);

        if( mystr == NULL )
        {
            mexErrMsgIdAndTxt("MATLAB:cg_descent:conversionFailed",
                  "Input could not be converted to string.");
        }
    }
    else /* not string input, must be structure */
    {
        /* Check if user provided nonempty struct as input */
        if ( !mxIsClass(prhs[0], "struct") || mxIsEmpty(prhs[0]) )
        {
            mexErrMsgIdAndTxt("MATLAB:cg_descent:conversionFailed",
                  "Input must be nonempty structure.");
        }
    }

    /* Verify correct number of output arguments provided for PASA */
    if( (nlhs < 1 || nlhs > 3) && !string_input )
    {
        mexErrMsgIdAndTxt("MyToolbox:cg_descent:nlhs",
                          "cg_descent requires at least 1 output "
                          "and allows at most 3 outputs.") ;
    }

    #if DEBUG_CGDESCENT_MEX
    mexPrintf ("Finished prhs error messages\n") ;
    #endif

    /*------- Initialize cg data struct -------- */
    CGdata *cgdata = cg_setup () ;

    if ( string_input )
    {
        /* check string against valid keywords */
        if (!strcmp(mystr, "readme"))
        {
            /* Print readme information about cg_descent */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "help") ;
        }
        else if ((!strcmp(mystr, "all")) || (!strcmp(mystr, "allparms"))
                                         || (!strcmp(mystr, "parm")))
        {
            /* Print default cg_descent parameter values and descriptions */
            cg_print_parm (cgdata) ;
        }
        else if (!strcmp(mystr, "demo"))
        {
            /* Open demo file for cg_descent */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to view file */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else if (!strcmp(mystr, "demoQP"))
        {
            /* Open demo file for cg_descent */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to view file */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else /* Invalid option string provided for cg_descent */ 
        {
            printf("\n Invalid keyword entered for cg_descent information.\n") ;
        }

        /* Print additional information note for user */
        cg_matlab_print_info () ;
        
        cg_terminate (&cgdata) ;

        /* Exit program as there is nothing to evaluate */
        return ;
    }

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Loading problem data struct\n") ;
    #endif

    /* Copy input to options */
    options = prhs[0] ;

    /* Initialize n to 0 */
    n = EMPTY ;

    /* --- n: Problem dimension --- */
    /* Extract problem dimension if provided */
    suiteopt_matlab_get_problem_dimension (options, &n) ;

    /* --- x (Solution): Allocate memory if not provided --- */
    if ((field = mxGetField(options, 0, "x")) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            /* -------- Configure initial output values  -------- */
            /* Copy initial guess for x into first output plhs[0] */
            plhs[0] = mxDuplicateArray(field) ;

            #if DEBUG_CGDESCENT_MEX
            mexPrintf("Successfully set plhs[0].\n") ;
            #endif

            /* Copy value for x */
            cgdata->x = mxGetPr(plhs[0]) ;

            #if DEBUG_CGDESCENT_MEX
            mexPrintf("Successfully imported initial guess x.\n") ;
            #endif

            long xdim = (long) CGMAX(mxGetN (field), mxGetM (field)) ;
            /* Set problem dimension if n not provided */
            if (n <= 0)
            {
                n = xdim ;
            }
            else if ( n > xdim ) /* print error and exit */
            {
                mexPrintf("The dimension of the starting guess is %ld, "
                          "which is inconsistent\n"
                          "with the specified problem "
                          "dimension given by cgdata.n = %ld\n", xdim, n) ;
                mexErrMsgTxt("Terminating cg_descent.\n") ;
            }
        }
        else /* x must be of type double, print error message */
        {
            mexPrintf("Initial guess x provided to cg_descent "
                      "must be of type double.\n") ;
            mexErrMsgTxt("Terminating cg_descent.\n") ;
        }
    }
    else if (n > 0) /* x not provided but n provided so create vector */
    {
        #if DEBUG_CGDESCENT_MEX
        mexPrintf("Initial guess x not provided.\n");
        #endif

        /* Initialize pointer for the first output of plhs */
        plhs[0] = mxCreateDoubleMatrix (n, 1, mxREAL) ;
        /* Copy value for x */
        cgdata->x = mxGetPr(plhs[0]) ;
        cg_initx (cgdata->x, CGZERO, n) ;

        #if DEBUG_CGDESCENT_MEX
        mexPrintf("Allocated memory for x.\n");
        #endif
    }
    else /* x not provided and n not provided, Print error message */
    {
        mexPrintf("Initial guess x and problem dimension n "
                  "not provided to cg_descent.\n") ;
        mexErrMsgTxt("Terminating cg_descent.\n") ;
    }

    cgdata->n = n ;

    /* c: Linear term in quadratic cost function */
    cgdata->c = suiteopt_matlab_get_float (options, &n, NULL, "c") ;
    FoundC = (cgdata->c != NULL) ;

    /* objective: Function handle for objective */
    suiteopt_value = suiteopt_matlab_get_func (options, 1, 1, "objective") ;
    cgdata->value = (suiteopt_value != NULL) ? suiteopt_matlab_value : NULL ;
    FoundValue = (suiteopt_value != NULL) ;

    /* gradient: Function handle for gradient */
    suiteopt_grad = suiteopt_matlab_get_func (options, 1, 1, "gradient") ;
    cgdata->grad = (suiteopt_grad != NULL) ? suiteopt_matlab_grad : NULL ;
    FoundGrad = (suiteopt_grad != NULL) ;

    /* valgrad: Function handle for objective & gradient */
    suiteopt_valgrad = suiteopt_matlab_get_func (options, 1, 2, "valgrad") ;
    cgdata->valgrad = (suiteopt_valgrad != NULL) ? suiteopt_matlab_valgrad:NULL;
    FoundValgrad = (suiteopt_valgrad != NULL) ;

    /* cg_hprod: Function handle for Hessian times vector */
    cg_hprod = suiteopt_matlab_get_func (options, 1, 1, "hprod") ;
    cgdata->hprod = (cg_hprod != NULL) ? suiteopt_matlab_cghprod : NULL ;
    FoundHprod = (cg_hprod != NULL) ;

    /* CGParm: Import custom parameter values */
    cg_matlab_get_parm (options, cgdata->Parm) ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Completed importing all prhs.\n") ;
    #endif

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("\nInput Variables:\n") ;
    mexPrintf("Problem dimension: %d\n", n) ;
    mexPrintf("grad_tol = %g\n", cgdata->Parm->grad_tol) ;
    mexPrintf("\nFirst components of initial guess:\n") ;
    for (i = 0; i < SUITEOPTMIN(n, 10); i++)
    {
        mexPrintf("x[%i] = %g\n", i, cgdata->x[i]) ;
    }
    mexPrintf("\n") ;
    #endif

    /* -------- Configure remaining output values  -------- */
    status = &status_value ;
    if ( nlhs >= 3 )
    {
        plhs[2] = mxCreateDoubleMatrix(1, 1, mxREAL) ;
        status = mxGetPr(plhs[2]) ;
    }

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Set output variables successfully\n") ;
    #endif

    /* If user did not provide enough function handles, print error message */
    if ( !(FoundHprod && FoundC) && !(FoundValue && FoundGrad) )
    {
        mexPrintf("Insufficient function information provided to cg_descent.\n"
                  "Must provide objective value and its gradient or a\n"
                  "quadratic objective (linear cost vector and routine for\n"
                  "multiplying the objective Hessian by a vector).\n") ;
        mexPrintf("  Objective provided: %s\n", FoundValue ? "TRUE" : "FALSE") ;
        mexPrintf("  Gradient provided.: %s\n", FoundGrad ? "TRUE" : "FALSE") ;
        mexPrintf("  Valgrad provided..: %s\n",FoundValgrad ? "TRUE" : "FALSE");
        mexPrintf("  Hprod provided....: %s\n", FoundHprod ? "TRUE" : "FALSE") ;
        mexPrintf("  c provided........: %s\n", FoundC ? "TRUE" : "FALSE") ;
        mexErrMsgTxt("Terminating cg_descent.\n") ;
    }

    *status = cg_descent (cgdata) ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Finished running cg_descent.\n") ;
    #endif

    /* -------- Store any remaining output values -------- */
    if (nlhs >= 2)
    {
        #if DEBUG_CGDESCENT_MEX
        mexPrintf("Storing cg_descent statistics for output.\n") ;
        #endif

        /* Store cg_descent statistics in second output */
        cg_matlab_get_stat (&plhs[1], cgdata->Stat) ;
    }

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Freeing memory allocated by cg_setup.\n") ;
    #endif

    cg_terminate (&cgdata) ;

    #if DEBUG_CGDESCENT_MEX
    mexPrintf("Exiting cg_descent.\n") ;
    #endif

    /* Exit program */
    return ;
}
