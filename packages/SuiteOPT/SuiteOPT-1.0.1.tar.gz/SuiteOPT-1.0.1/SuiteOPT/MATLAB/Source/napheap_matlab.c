/* --- NAPHEAP functions required by more than one mex function --- */
/* This file contains function definitions associated with NAPHEAP 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Include header files ---------- */
#include "napheap_matlab.h"

/* --- Function to print additional info for user --- */
void napheap_matlab_print_info () {
    /* Print info for napheap */
    printf("\n  NAPHEAP is designed to "
           "solve a separable convex quadratic knapsack problem\n\n"
           "                min             0.5 * x'*D*x - y'*x\n"
           "            subject to    lo <= x <= hi, blo <= a'*x <= bhi\n\n  "
           "where lo and hi are vectors, blo and bhi are scalars, "
           "and D is a diagonal\n  matrix with nonnegative diagonal.\n");
    /* Print help info for napheap */
    printf ("\n  ========================== NAPHEAP Additional Info  ");
    printf ("==========================\n");
    printf ("    - For more detailed information on napheap type ");
    printf (       "'napheap readme'\n");
    printf ("    - For a list of all default parameter values ");
    printf ("type 'napheap parm'\n");
    printf ("    - For detailed information on napheap_check ");
    printf ("type 'napheap_check'\n");
    printf ("    - For a detailed example showing how to set up and ");
    printf (       "call napheap and\n      napheap_check in MATLAB, ");
    printf (       "type 'napheap demo'\n");
    printf ("    - Type 'demo' to solve a ");
    printf ("sample problem\n");
    printf ("    - For all available help options type 'napheap'\n");
    printf ("  ============================================");
    printf ("==================================\n\n");

    /* Exit program */ 
    return ;
}

/* Print information about napheap_check */
void napheap_check_matlab_print_info ()
{
    printf (
"\n NAPHEAP_CHECK checks the knapsack solution found by napheap\n"
"\n"
"   Usage: [err, errb, errB, erry] = napheap_check (napdata)\n"
"\n"
"   Determines KKT error in a solution to the separable convex quadratic\n"
"   knapsack problem:\n"
"\n"
"   min .5*x'*D*x - y'*x  subject to lo <= x <= hi, blo <= b <= bhi, a'*x = b\n"
"\n"
"   Input is a struct containing the napheap problem data with solution\n" 
"   x and the Lagrange multiplier lambda associated with the constraint\n"
"   a'*x = b. napheap_check determines the smallest perturbations in b,\n" 
"   y, lo, hi, and lambda with the property that x and lambda satisfy the\n"
"   KKT conditions for the perturbed problem. The KKT conditions are the\n"
"   following:\n"
"\n"
"   1. If b = a'*x, then b = bhi if lambda > 0\n"
"                        b = blo if lambda < 0\n"
"                        b in [blo, bhi] if lambda = 0\n"
"\n"
"   2. lo (j) <= x (j) <= hi (j)\n"
"\n"
"   3. If d (j) = 0, then x (j) = hi (j) if a (j)*lambda - y (j) < 0\n"
"                         x (j) = lo (j) if a (j)*lambda - y (j) > 0\n"
"      If d (j) > 0, then\n"
"      x (j) = mid {lo (j), (y (j) - a (j)*lambda)/d (j), hi (j)}\n"
"      Here 'mid' denotes the mean (or middle) of the three quantities.\n"
"\n"
"   If not present on input, defaults are d=ones(n,1), a=ones(n,1), blo=0,\n"
"   bhi=inf lo=zeros(n,1), and hi=inf(n,1)\n"
"\n"
"   The code returns the relative 1-norm of the minimum perturbations\n"
"   in b, y, lo, hi, and lambda that are needed to satisfy these conditions.\n"
"   These three terms are computed, and the overall error is the largest of\n"
"   the three:\n"
"\n"
"   errb: (|pert b|+|pert lambda|)/ sum |a (j)*x (j)|\n"
"   errB: ||pert lo||_1 + ||pert hi||_1 over the 1-norm of the corresponding\n"
"       original components\n"
"   erry: ||pert y||_1 over the 1-norm of the corresponding original\n"
"       components\n"
"\n"
"   Example:\n"
"       [x lambda] = napheap (napdata) ;\n"
"       napdata.x = x ;\n"
"       napdata.lambda = lambda ;\n"
"       [err, errb, errB, erry] = napheap_check (napdata)\n"
"\n"
"   See also NAPHEAP, NAPHEAP_INSTALL, NAPHEAP_TEST\n"
"\n"
"   Copyright 2015, T. A. Davis, W. W. Hager, and J. T. Hungerford\n"
"   http://www.suitesparse.com\n"
"   For a paper on napheap, see napheap/Doc/napheap.pdf\n\n\n") ;
}


/* Import cost function data (d and y) */
void napheap_matlab_get_objective
(
    const mxArray *options, /* User provided struct to mex function */
    NAPdata *data,          /* Struct in which to store pproj problem data */
    int *DiffLen            /* Increment DiffLen each time len(data) != n */
)
{
    /* d: Diagonal Hessain in cost function */
    data->d = suiteopt_matlab_get_float (options, &(data->n), DiffLen, "d") ;
    /* Check if d was provided */
    if (data->d == NULL)
    {
        /* d not provided; set d_is_zero to true and d_is_pos to false */
        data->Parm->d_is_zero = TRUE ;
        data->Parm->d_is_pos = FALSE ;
    }
    else
    {
        /* d provided; set d_is_zero to false and d_is_pos to true */
        data->Parm->d_is_zero = FALSE ;
        data->Parm->d_is_pos = TRUE ;
    }

    /* y: Linear term in cost function */
    data->y = suiteopt_matlab_get_float (options, &(data->n), DiffLen, "y") ;

    /* Exit program */
    return ;
}


/* Import napsack constraint data (blo, bhi, and a) */
void napheap_matlab_get_napsack_constraints
(
    const mxArray *options, /* User provided struct to mex function */
    NAPdata *data,          /* Struct in which to store pproj problem data */
    int *DiffLen            /* Increment DiffLen each time len(data) != n */
)
{
    /* a: Linear constraint vector */
    data->a = suiteopt_matlab_get_float (options, &(data->n), DiffLen, "a") ;

    /* blo: Lower bound on linear constraint a'*x */
    suiteopt_matlab_get_scalar (options, &(data->blo), "blo") ;

    /* bhi: Upper bound on linear constraint a'*x */
    suiteopt_matlab_get_scalar (options, &(data->bhi), "bhi") ;

    /* Exit program */
    return ;
}


/* --- Extract parameter values for NAPHEAP from user struct --- */
void napheap_matlab_get_parm (const mxArray *options, NAPparm *Parm)
{
    /* Initialize variables */
    mxArray *field ;

    /* --------------------- NAPHEAP parameters --------------------- */
    /* Detailed description of parm in NAPHEAP/Include/napheap.h */
    if ((field = mxGetField(options, 0, "PrintStatus")) != NULL)
    {
        Parm->PrintStatus = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "PrintStat")) != NULL)
    {
        Parm->PrintStat = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "PrintParm")) != NULL)
    {
        Parm->PrintParm = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_prior_data")) != NULL)
    {
        Parm->use_prior_data = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "return_data")) != NULL)
    {
        Parm->return_data = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "loExists")) != NULL)
    {
        Parm->loExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "hiExists")) != NULL)
    {
        Parm->hiExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "Aexists")) != NULL)
    {
        Parm->Aexists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "d_is_pos")) != NULL)
    {
        Parm->d_is_pos = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "d_is_zero")) != NULL)
    {
        Parm->d_is_zero = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "d_is_one")) != NULL)
    {
        Parm->d_is_one = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "K")) != NULL)
    {
        Parm->K = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "newton")) != NULL)
    {
        Parm->newton = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "newton_scale")) != NULL)
    {
        Parm->newton_scale = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "decay")) != NULL)
    {
        Parm->decay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "refine")) != NULL)
    {
        Parm->refine = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "err")) != NULL)
    {
        Parm->err = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "check")) != NULL)
    {
        Parm->check = (int) mxGetScalar(field) ;
    }
}

/* --- Extract problem statistics for NAPHEAP to return to user --- */
void napheap_matlab_get_stat (mxArray **out, NAPstat *Stat)
{
    /* Initialize variables */
    mxArray *fout, *sout ;
    int ifield, *idata ;
    double *pdata ;
    const char *nap_fnames[13] = {/* napheap statistics are listed here */
                                  "nkf", "nfree", "nbound", "nbrks", 
                                  "nrefine", "nvarfix", "nnewton", 
                                  "nsecant", "status", "kerror", 
                                  "lobad", "hibad", "dbad"} ;
    /* Create struct matrix with napheap statistic names */
    *out = mxCreateStructMatrix(1, 1, 13, nap_fnames) ;

    /* Cycle through fnames and store stats in idata or pdata */
    for(ifield = 0; ifield < 13; ifield++)
    {
        if ( ifield  > 9 )
        {
            /* Set fout to 1 by 1 number matrix of doubles */
            fout = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL) ;
            /* Set pdata as pointer to double fout */
            pdata = (double *) mxGetData (fout) ;
        }
        else
        {
            /* Set fout as 1 by 1 matrix of type int */
            fout = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL) ;
            /* Set idata as pointer to int fout */
            idata = (int *) mxGetData (fout) ;
        }

        /* Set pdata to point to stat for case ifield */
        switch (ifield)
        {
            case 0: *idata = Stat->nkf ; break ;
            case 1: *idata = Stat->nfree ; break ;
            case 2: *idata = Stat->nbound ; break ;
            case 3: *idata = Stat->nbrks ; break ;
            case 4: *idata = Stat->nrefine ; break ;
            case 5: *idata = Stat->nvarfix ; break ;
            case 6: *idata = Stat->nnewton ; break ;
            case 7: *idata = Stat->nsecant ; break ;
            case 8: *idata = Stat->status ; break ;
            case 9: *idata = Stat->kerror ; break ;
            case 10: *pdata = Stat->lobad ; break ;
            case 11: *pdata = Stat->hibad ; break ;
            case 12: *pdata = Stat->dbad ; break ;
        }
        /* Set the ifieldth component of *out to fout */
        mxSetFieldByNumber(*out, 0, ifield, fout) ;
    }
}

/* --- Routine to print all elements imported to napheap data struct --- */
void napheap_matlab_print_data
(
    NAPdata *data   /* Pointer to napheap data struct with problem data */ 
)
{
    /* Initialize variables */
    int i ;

    mexPrintf("\nInput Variables:\n") ;
    /* Print dimension */
    mexPrintf("n = %i\n", data->n) ;
    /* Print linear term in cost function */
    if (data->y != NULL) {
        for (i = 0; i < data->n; i++)
        {
            mexPrintf("y[%i] = %g\n", i, data->y[i]) ;
        }
    }
    else
    {
        mexPrintf("y not provided.\n") ;
    }
    /* Print diagonal of Hessian */
    if (data->d != NULL)
    {
        for (i = 0; i < data->n; i++)
        {
            mexPrintf("d[%i] = %g\n", i, data->d[i]) ;
        }
    }
    else
    {
        mexPrintf("d not provided.\n") ;
    }
    /* Print constraint vector a */
    for (i = 0; i < data->n; i++)
    {
        mexPrintf("a[%i] = %g\n", i, data->a[i]) ;
    }
    /* Print solution x */
    if (data->x != NULL)
    {
        for (i = 0; i < data->n; i++)
        {
            mexPrintf("x[%i] = %g\n", i, data->x[i]) ;
        }
    }
    /* Print multiplier lambda */
    mexPrintf("lambda = %g\n", data->lambda) ;
    /* Print lo vector */
    if (data->lo != NULL)
    {
        for (i = 0; i < data->n; i++)
        {
            mexPrintf("lo[%i] = %g\n", i, data->lo[i]) ;
        }
    }
    else
    {
        mexPrintf("lo not provided.\n") ;
    }
    /* Print hi vector */
    if (data->hi != NULL)
    {
        for (i = 0; i < data->n; i++)
        {
            mexPrintf("hi[%i] = %g\n", i, data->hi[i]) ;
        }
    }
    else
    {
        mexPrintf("hi not provided.\n") ;
    }
    /* Print lower bound on napsack constraint */
    mexPrintf("blo = %g\n", data->blo) ;
    /* Print upper bound on napsack constraint */
    mexPrintf("bhi = %g\n", data->bhi) ;
    mexPrintf("\n") ;

    mexPrintf("Completed printing all prhs.\n") ;

}

/* --- Wrapup routine for NAPHEAP MATLAB MEX functions --- */
void napheap_matlab_wrapup
(
    NAPdata *data,  /* Pointer to napheap data struct with problem data */ 
    bool Malloc_a   /* TRUE if mex function malloc'd a, FALSE otherwise */
) {
    /* Free memory allocated for a (if necessary) */
    if (Malloc_a) {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Freeing memory for a.\n") ;
        #endif

        mxFree(data->a) ;

        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Successfully freed memory for a.\n") ;
        #endif
    }

    /* Free memory allocated by napheap_setup */
    napheap_terminate (&data) ;

    /* Exit */
    return ;
}
