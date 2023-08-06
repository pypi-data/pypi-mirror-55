/* ---------- pproj mex function ---------- */
/* This file contains the mex function for interfacing pproj with MATLAB */

/* ---------- Include header files ---------- */
#include "pproj_matlab.h"

/* mex function */
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    /* Initialize input variables */
    double *lambda ; 
    int status, n_temp, DiffLen ;
    bool Malloc_lambda ;
    long i ;
    long long *ppcom_ptr ;
    char *mystr, *outstr ;
    size_t  buflen ;
    PPdata *pprojdata ; 
    mxArray *lhs[1], *rhs, *field ;
    const mxArray *options ;
    union {long long theint; void *theptr;} void_com ; 

    #if DEBUG_PPROJ_MEX
    mexPrintf ("Initialized variables\n") ;
    #endif

    /* If the user provided no input then print some options */
    if (nrhs == 0) {
        /* Print additional information note for user */
        pproj_matlab_print_info () ;

        /* Nothing to solve, terminate program */
        return ;
    }

    /* If user provided one input then print default parameter values */
    if ((nrhs == 1) && mxIsChar(prhs[0]))
    {
        /* String must be input as row vector */
        if (mxGetM(prhs[0])!=1)
          mexErrMsgIdAndTxt("MATLAB:pproj:inputNotVector",
                  "pproj help keyword must be a row vector.") ;

        /* Set length of string */
        buflen = (mxGetM(prhs[0]) * mxGetN(prhs[0])) + 1;
    
        /* Allocate memory for output string */
        outstr = mxCalloc(buflen, sizeof(char));
    
        /* Copy string from prhs[0] to string in C */
        mystr = mxArrayToString(prhs[0]);
        
        if(mystr == NULL) 
          mexErrMsgIdAndTxt("MATLAB:pproj:conversionFailed",
                  "Input could not be converted to string.");

        /* Initialize variables needed for printing parameters */
        PPparm *UPPparm, PPparmStruc ;
        
        /* Set initial values */
        UPPparm = &PPparmStruc ;

        /* check string against valid keywords */
        if (!strcmp(mystr, "readme"))
        {
            /* Print readme information about pproj */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "help") ;
        }
        else if (!strcmp(mystr, "parm"))
        {
            /* Print default pproj parameter values and descriptions */
            pprojdata = pproj_setup () ;
            pproj_print_parm (pprojdata) ;
            pproj_terminate (&pprojdata) ;
        }
        else if (!strcmp(mystr, "demo"))
        {
            /* Open demo file for pproj */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else /* Invalid option string provided for pproj */ 
        {
            printf("\n Invalid keyword enetered for pproj information.\n") ;
        }

        /* Print additional information note for user */
        pproj_matlab_print_info () ;

        /* Exit program as there is no problem to solve */
        return ;
    }

    /* Check if user provided nonempty struct as input */
    if ((nrhs == 1) && (mxIsClass(prhs[0], "struct")) && !mxIsEmpty(prhs[0]))
    {
        #if DEBUG_PPROJ_MEX
        mexPrintf("Loading problem data struct\n") ;
        #endif

        /* Copy input to options */
        options = prhs[0] ;
    }

    /* Verify correct number of input arguments provided for PPROJ */
    if(nrhs > 2)
    {
        mexErrMsgIdAndTxt("MyToolbox:pproj:nrhs",
                          "pproj requires at least 1 struct "
                          "as an input and accepts at most two "
                          "structs.");
    }

    /* Verify correct number of output arguments provided for PPROJ */
    if(nlhs < 1 || nlhs > 3)
    {
        mexErrMsgIdAndTxt("MyToolbox:pproj:nlhs",
                          "pproj requires at least 1 output "
                          "and allows at most 3 outputs.");
    }

    #if DEBUG_PPROJ_MEX
    mexPrintf ("Finished prhs error messages\n") ;
    #endif

    /*------- Initialize pproj data struct -------- */
    pprojdata = pproj_setup () ;

    #if DEBUG_PPROJ_MEX
    mexPrintf("Loading problem parameters from struct\n") ;
    #endif

    /* Import user parameter values */
    pproj_matlab_get_parm (options, pprojdata->Parm) ;

    #if DEBUG_PPROJ_MEX
    mexPrintf("Imported user PPROJ parameters\n") ;
    #endif

    /* Initialize counter for number of different length inputs */
    DiffLen = 0 ;
    /* Initialize check for whether or not user provided parameters */
    Malloc_lambda = FALSE ;

    /* ----------- Import problem options provided in input struct ------- */
    /* Detailed description of input options found in PPROJ/Source/pproj.c */

    /* ncol: Problem dimension */
    suiteopt_matlab_get_problem_dimension (options, &(pprojdata->ncol)) ;

    /* y: Point to project onto polyhedron */
    if ((field = mxGetField(options, 0, "y")) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            /* Copy value for y */
            pprojdata->y = mxGetPr (field) ;

            #if DEBUG_PPROJ_MEX
            mexPrintf("Successfully imported point to project.\n") ;
            #endif

            /* -------- Set value of ncol if it was not provided -------- */
            /* Number of components of y */
            n_temp = (long) PPMAX(mxGetM(field), mxGetN(field)) ;
            /* If current ncol is 0 or larger than length of y, set ncol 
               equal to the length of y */
            if((pprojdata->ncol <= 0) || (pprojdata->ncol > n_temp))
            {
                pprojdata->ncol = n_temp ;
            }
            else if (pprojdata->ncol < n_temp)
            {
                /* Print warning message */
                mexPrintf("pproj::Warning::Input y (point to project onto "
                          "polyhedron) provided to pproj is of length %d but "
                          "provided ncol is %d.\n", n_temp, pprojdata->ncol) ;
                mexPrintf("pproj::Warning::Using ncol = %d for problem "
                          "dimension.\n", pprojdata->ncol) ;
            }
        }
        else /* y must be of type double, Print error message */
        {
            mexPrintf("pproj::Input y (point to project onto polyhedron) "
                      "provided to pproj must be of type double.\n") ;
            mexErrMsgTxt("Terminating pproj.\n") ;
        }
    }
    else /* y not provided to pproj, Print error message */
    {
        mexPrintf("pproj::Input y (point to project onto polyhedron) "
                  "not provided but is required input.\n") ;
        mexErrMsgTxt("Terminating pproj.\n") ;
    }

    /* Initialize pointer for the first output of plhs */
    plhs[0] = mxCreateDoubleMatrix (pprojdata->ncol, 1, mxREAL) ;
    /* Copy value for x */
    pprojdata->x = mxGetPr(plhs[0]) ;  

    #if DEBUG_PPROJ_MEX
    mexPrintf("Allocated memory for x.\n");
    #endif

    /* grad_tol: Stopping tolerance */
    suiteopt_matlab_get_scalar (options, &(pprojdata->Parm->grad_tol),
                                "grad_tol") ;

    /* nrow, Ap, Ai, Ax, bl, bu, nsing, ...: Polyhedral constraints */
    suiteopt_matlab_get_polyhedral_constraints (options, pprojdata) ;

    /* lo, hi: Bound constraints lo <= x <= hi */
    suiteopt_matlab_get_bound_constraints (options, pprojdata, &DiffLen) ;

    /* lambda: Initial guess for constraint multiplier --- */
    if ((field = mxGetField(options, 0, "lambda")) != NULL)
    {
        if (mxIsClass(field, "double"))
        {
            #if DEBUG_PPROJ_MEX
            mexPrintf("User provided lambda.\n");
            #endif

            /* use the provided lambda as a starting guess for the
               solution of the dual problem */
            pprojdata->Parm->start_guess = 3 ;

            /* Check if user requested lambda as output */
            if (nlhs >= 3)
            {
                /* Copy initial guess for lambda into output plhs[2] */
                plhs[2] = mxDuplicateArray(field) ;
        
                #if DEBUG_PPROJ_MEX
                mexPrintf("Successfully set plhs[2].\n") ;
                #endif

                /* Copy pointer for lambda */
                pprojdata->lambda = mxGetPr(plhs[2]) ;  
            }
            else
            {
                /* Copy pointer for lambda */
                pprojdata->lambda = mxGetPr(mxDuplicateArray(field)) ;
            }

            #if DEBUG_PPROJ_MEX
            mexPrintf("Successfully imported value to pproj.\n");
            #endif
        }
        else
        {/* lambda must be of type double, print error message */
            mexErrMsgTxt("Multiplier lambda provided to pproj "
                         "must be of type double.\n") ;
            mexErrMsgTxt("Terminating pproj.\n") ;
        }
    }
    else /* lambda not provided to pproj */
    {
        #if DEBUG_PPROJ_MEX
        mexPrintf("lambda not provided. Setting lambda to default.\n");
        #endif

        /* Check if user requested lambda as output */
        if (nlhs >= 3)
        {
            /* Initialize pointer for the first output of plhs */
            plhs[2] = mxCreateDoubleMatrix (pprojdata->nrow, 1, mxREAL) ;
        
            #if DEBUG_PPROJ_MEX
            mexPrintf("Successfully set plhs[2].\n") ;
            #endif

            /* Copy pointer for lambda */
            pprojdata->lambda = mxGetPr(plhs[2]) ;  

            #if DEBUG_PPROJ_MEX
            mexPrintf("Set lambda to default.\n");
            #endif
        }
    }

    #if DEBUG_PPROJ_MEX
    mexPrintf("Completed importing all prhs.\n") ;
    #endif

    #if DEBUG_PPROJ_MEX
    /* Print user provided data */
    pproj_matlab_print_data (pprojdata) ;
    #endif

    /* -------- Initialize pproj statistics to default -------- */
    pproj_initstat (pprojdata->Stat) ;

    /* -------- Run pproj on problem -------- */
    status = pproj (pprojdata) ;

    #if DEBUG_PPROJ_MEX
    mexPrintf("Finished running pproj.\n") ;
    #endif

    /* -------- Store any remaining output values -------- */
    if (nlhs >= 2)
    {
        #if DEBUG_PPROJ_MEX
        mexPrintf("Storing pproj statistics for output.\n") ;
        #endif

        #if DEBUG_PPROJ_MEX
        mexPrintf("upprojstats->maxdepth = %i\n", pprojdata->Stat->maxdepth) ;
        #endif

        /* Store pproj statistics in second output */
        pproj_matlab_get_stat (&plhs[1], pprojdata->Stat) ;

        #if DEBUG_PPROJ_MEX
        mexPrintf("Stored pproj statistics successfully.\n") ;
        #endif
    }

    #if DEBUG_PPROJ_MEX
    mexPrintf("Set output variables successfully\n") ;
    #endif

    /* -------- Free memory allocated in mex function -------- */
    #if DEBUG_PPROJ_MEX
    mexPrintf("Checking and freeing memory for lambda (if necessary).\n") ;
    #endif

    /* Wrapup and free memory */
    pproj_terminate (&pprojdata) ;

    #if DEBUG_PPROJ_MEX
    mexPrintf("Exiting pproj.\n") ;
    #endif

    return ;
}
