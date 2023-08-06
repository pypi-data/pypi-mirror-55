/* ---------- pasa mex function ---------- */
/* This file contains the mex function for interfacing pasa with MATLAB */

/* ---------- Include header files ---------- */
#include "pasa_matlab.h"

/* ---------- Declare global variables ---------- */
mxArray *suiteopt_value ;
mxArray *suiteopt_grad ;
mxArray *suiteopt_valgrad ;
mxArray *suiteopt_hprod ;
mxArray *cg_hprod ;

/* mex function */
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) 
{
    /* Initialize input variables */
    double *lambda, *newlambda, *newx, maxits ;
    bool Aexists ;
    int DiffLen ;
    long i, ncol ;
    char *mystr ;
    mxArray *lhs[1], *rhs, *field ;
    const mxArray *options ;

    #if DEBUG_PASA_MEX
    mexPrintf ("Initialized variables\n") ;
    #endif

    /* If the user provided no input then print some options */
    if (nrhs == 0)
    {
        printf("\n\n  PASA (Polyhedral Active Set Algorithm) is designed\n"
               "    to solve problems of the form\n\n              "
               "min f(x)  subject to  bl <= Ax <= bu, lo <= x <= hi\n"); 
        /* Print additional information note for user */
        pasa_matlab_print_info () ;

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
            mexErrMsgIdAndTxt("MATLAB:pasa:inputNotVector",
                    "pasa help keyword must be a row vector.") ;
        }

        /* Copy string from prhs[0] to string in C */
        mystr = mxArrayToString(prhs[0]);
        
        if( mystr == NULL ) 
        {
            mexErrMsgIdAndTxt("MATLAB:pasa:conversionFailed",
                  "Input could not be converted to string.");
        }
    }
    else /* not string input, must be structure */
    {
        /* Check if user provided nonempty struct as input */
        if ( !mxIsClass(prhs[0], "struct") || mxIsEmpty(prhs[0]) )
        {
            mexErrMsgIdAndTxt("MATLAB:pasa:conversionFailed",
                  "Input must be nonempty structure.");
        }
    }

    /* Verify correct number of output arguments provided for PASA */
    if( (nlhs < 1 || nlhs > 3) && !string_input )
    {  
        mexErrMsgIdAndTxt("MyToolbox:pasa:nlhs",
                          "pasa requires at least 1 output "
                          "and allows at most 3 outputs.") ;
    }

    #if DEBUG_PASA_MEX
    mexPrintf ("Finished prhs error messages\n") ;
    #endif

    /*------- Initialize pasa data struct -------- */
    PASAdata *pasadata = pasa_setup () ;

    /* If user provided no inputs then print default parameter values */
    if ( string_input )
    {
        /* check string against valid keywords */
        if (!strcmp(mystr, "readme"))
        {
            /* Print readme information about pasa */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "help") ;
        }
        else if ((!strcmp(mystr, "all")) || (!strcmp(mystr, "allparms")))
        {
            /* Print default pasa parameter values and descriptions */
            pasa_print_parm (pasadata) ;
    
            /* Print default pproj parameter values and descriptions */
            pproj_print_parm (pasadata->ppdata) ;

            /* Print default cg parameter values and descriptions */
            cg_print_parm (pasadata->cgdata) ;

            /* Print default napheap parameter values and descriptions */
            napheap_print_parm (pasadata->napdata) ;
        }
        else if (!strcmp(mystr, "parm"))
        {
            /* Print default pasa parameter values and descriptions */
            pasa_print_parm (pasadata) ;
        }
        else if (!strcmp(mystr, "pproj"))
        {
            /* Print default pproj parameter values and descriptions */
            pproj_print_parm (pasadata->ppdata) ;
        }
        else if (!strcmp(mystr, "cg"))
        {
            /* Print default pproj parameter values and descriptions */
            cg_print_parm (pasadata->cgdata) ;
        }
        else if (!strcmp(mystr, "napheap"))
        {
            /* Print default pproj parameter values and descriptions */
            napheap_print_parm (pasadata->napdata) ;
        }
        else if (!strcmp(mystr, "demo"))
        {
            /* Open demo file for pasa */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to print readme options */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else if (!strcmp(mystr, "demoQP"))
        {
            /* Open demo file for pasa */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to view file */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else if (!strcmp(mystr, "demoOC"))
        {
            /* Open demo file for pasa */
            /* Copy prhs to non const mxArray */
            rhs = (mxArray*) prhs[0] ;
    
            /* Call MATLAB function help to view file */
            mexCallMATLAB(0, lhs, 1, &rhs, "open") ;
        }
        else /* Invalid option string provided for pasa */ 
        {
            printf("\n Invalid keyword entered for pasa information.\n") ;
        }

        /* Print additional information note for user */
        pasa_matlab_print_info () ;
        
        pasa_terminate (&pasadata) ;

        /* Exit program as there is nothing to evaluate */
        return ;
    }

    #if DEBUG_PASA_MEX
    mexPrintf("Loading problem data struct\n") ;
    #endif

    /* Copy input to options */
    options = prhs[0] ;

    /* Initialize counter for number of different length inputs */
    DiffLen = 0 ;

    /* Initialize Aexists to FALSE (no linear inequality constraints) */
    Aexists = FALSE ; 

    /* --------------------- Import parameters ---------------------- */
    /* Import any custom parameters specified by users */

    #if DEBUG_PASA_MEX
    mexPrintf("Loading problem parameters from struct\n") ;
    #endif

    /* PASAparms: Import PASA, PPROJ, CG, and NAPHEAP parameters --- */
    pasa_matlab_get_parms (options, pasadata->Parms) ;

    /* ----------- Import problem options provided in input struct ------- */
    /* Detailed description of input options found in the setup function
       in PASA/Source/pasa.c */

    /* ncol: Problem dimension */
    ncol = (long) -1 ;
    suiteopt_matlab_get_problem_dimension (options, &ncol) ;

    /* nrow, ((Ap, Ai, Ax) or (a)), and (bl, bu): Polyhedral/napsack constr. */
    suiteopt_matlab_get_polyhedral_constraints (options, pasadata) ;

    /* lo, hi: Bound constraints lo <= x <= hi */
    suiteopt_matlab_get_bound_constraints (options, pasadata, &DiffLen) ;

    /* c: Linear term in quadratic cost function */
    pasadata->c = suiteopt_matlab_get_float (options, &(pasadata->ncol),
                                              &DiffLen, "c") ;

    /* d: Diagonal of Hessian in napsack problem (if NAPSACK) --- */
    pasadata->d = suiteopt_matlab_get_float (options, &(pasadata->ncol),
                                              &DiffLen, "d") ;

    /* y: Point to project onto polyhedron (if PROJ) */
    pasadata->y = suiteopt_matlab_get_float (options, &(pasadata->ncol),
                                              &DiffLen, "y") ;

    /* x: Initial guess for solution */
    pasadata->x = suiteopt_matlab_get_float (options, &(pasadata->ncol),
                                              &DiffLen, "x") ;

    if ( pasadata->ncol == EMPTY )
    {
        pasadata->ncol = ncol ;
    }
    if ( ncol > pasadata->ncol )
    {
        mexPrintf("The specified problem dimension ncol = %ld is larger than\n"
                  "the size %ld of at least some of the PASA problem data\n\n",
                  ncol, pasadata->ncol) ;
        mexErrMsgTxt("\n") ;
    }
    else if ( ncol != (long) -1 )
    {
        pasadata->ncol = ncol ;
    }

    /* lambda: Initial guess for multiplier --- */
    if (pasadata->nrow > 0)
    {
        pasadata->lambda = suiteopt_matlab_get_float (options,
                                           &(pasadata->nrow), NULL, "lambda") ;
    }

    /* objective: Function handle for objective */
    suiteopt_value = suiteopt_matlab_get_func (options, 1, 1, "objective") ;
    if (suiteopt_value != NULL) pasadata->value = suiteopt_matlab_value ;

    /* gradient: Function handle for gradient */
    suiteopt_grad = suiteopt_matlab_get_func (options, 1, 1, "gradient") ;
    if (suiteopt_grad != NULL) pasadata->grad = suiteopt_matlab_grad ;

    /* valgrad: Function handle for objective & gradient */
    suiteopt_valgrad = suiteopt_matlab_get_func (options, 1, 2, "valgrad") ;
    if (suiteopt_valgrad != NULL) pasadata->valgrad = suiteopt_matlab_valgrad ;

    /* hprod: Function handle for PASA Hessian times vector */
    suiteopt_hprod = suiteopt_matlab_get_func (options, 2, 1, "hprod") ;
    if (suiteopt_hprod != NULL) pasadata->hprod = suiteopt_matlab_hprod ;

    /* cg_hprod: Function handle for CG Hessian times vector */
    cg_hprod = suiteopt_matlab_get_func (options, 1, 1, "cg_hprod") ;
    if (cg_hprod != NULL) pasadata->cg_hprod = suiteopt_matlab_cghprod ;

/* TODO: hess not available for use in PASA version 1.0.0 */
#if 0
    /* --- hess: Function handle for evaluating Hessian --- */
    hess = suiteopt_matlab_get_func (options, , , "hess") ;
    pasadata->hess = suiteopt_matlab_hess ; 
#endif

    #if DEBUG_PASA_MEX
    mexPrintf("Completed importing all prhs.\n") ;
    #endif

    /* ------- Check if problem dimension was not provided ------- */
    if (pasadata->ncol <= 0)
    {
        mexPrintf ("pasa unable to determine problem dimension based "
                   "on provided input.\n") ;
        mexPrintf (
            "     This can occur if the problem is unconstrained, a starting\n"
            "     guess is not given, and the structure element ncol in\n"
            "     pasadata is not set. A value for pasadata.ncol is needed.\n");
        mexErrMsgTxt("Terminating pasa.\n") ;
    }

    #if DEBUG_PASA_MEX
    /* Print user provided data */
    pasa_matlab_print_data (pasadata) ;
    #endif

    /* -------- Initialize pproj statistics to default -------- */
    pproj_initstat (pasadata->Stats->pproj) ;

    /* -------- Run pasa on problem -------- */
    pasa (pasadata) ;

    #if DEBUG_PASA_MEX
    mexPrintf("Finished running pasa.\n") ;
    #endif

    /* -------- Store output values -------- */
    #if DEBUG_PASA_MEX
    mexPrintf("Storing pasa problem solution.\n") ;
    #endif

    plhs[0] = mxCreateDoubleMatrix(1, pasadata->ncol, mxREAL) ;
    newx = mxGetPr(plhs[0]) ;

    #if DEBUG_PASA_MEX
    mexPrintf("Copying x to output array.\n") ;
    #endif

    pasa_copyx (newx, pasadata->x, pasadata->ncol) ;

    #if DEBUG_PASA_MEX
    mexPrintf("x copied to output successfully.\n") ;
    #endif

    /* -------- Store any remaining output values -------- */
    if (nlhs >= 2)
    {
        #if DEBUG_PASA_MEX
        mexPrintf("Storing pasa statistics for output.\n") ;
        #endif

        #if DEBUG_PASA_MEX
        mexPrintf("upasastats->pproj->maxdepth = %i\n", 
                  pasadata->Stats->pproj->maxdepth) ;
        #endif

        /* Determine value for Aexists */
        Aexists = (pasadata->Ax != NULL) ;

        /* Store pasa statistics in second output */
        pasa_matlab_get_stats (&plhs[1], pasadata->Stats, Aexists) ;

        #if DEBUG_PASA_MEX
        mexPrintf("Stored pasa statistics successfully.\n") ;
        #endif
    }
    /* Store final lambda for third output */
    if (nlhs >= 3)
    {
        if (pasadata->Stats->pproj != NULL) {
            #if DEBUG_PASA_MEX
            mexPrintf("Initializing output for lambda.\n") ;
            #endif
    
            plhs[2] = mxCreateDoubleMatrix(1, pasadata->nrow, mxREAL) ;
            newlambda = mxGetPr(plhs[2]) ;
    
            #if DEBUG_PASA_MEX
            mexPrintf("Copying lambda to output array.\n") ;
            #endif
    
            pasa_copyx (newlambda, pasadata->lambda, pasadata->nrow) ;
    
            #if DEBUG_PASA_MEX
            mexPrintf("Lambda copied to output successfully.\n") ;
            #endif
        }
        else {/* no lambda to return */
            plhs[2] = mxCreateString("NO_LAMBDA_TO_RETURN") ;
        }
    }

    /* -------- Free memory allocated in mex function -------- */
    #if DEBUG_PASA_MEX
    mexPrintf("Freeing memory allocated by pasa_setup.\n") ;
    #endif

    pasa_terminate (&pasadata) ;

    #if DEBUG_PASA_MEX
    mexPrintf("Exiting pasa.\n") ;
    #endif

    return ;
}
