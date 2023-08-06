/* --- PPROJ functions required by more than one mex function --- */
/* This file contains function definitions associated with PPROJ 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Include header files ---------- */
#include "pproj_matlab.h"

/* --- Function to print additional info for user --- */
void pproj_matlab_print_info ()
{
    /* Print info for pproj */
    printf("\n  PPROJ is designed to "
           "solve problems of the form\n\n              "
           "    min         0.5 || x0 - y0 || - y1'x1\n              "
           "subject to    lo <= x <= hi, bl <= Ax <= bu\n") ;
    /* Print help info for pproj */
    printf ("\n  =========================== PPROJ Additional Info  ") ;
    printf ("===========================\n") ;
    printf ("    - For more detailed information on pproj, type ") ;
    printf (       "'pproj readme'.\n") ;
    printf ("    - For a list of all default parameter values, ") ;
    printf ("type 'pproj parm'.\n") ;
    printf ("    - For detailed examples showing how to set up and ") ;
    printf (       "call pproj in MATLAB,\n      type 'pproj demo'\n") ;
    printf ("    - Type 'demo' to solve a sample problem\n") ;
    printf ("    - For all available help options, type 'pproj'\n") ;
    printf ("  ============================================") ;
    printf ("==================================\n\n") ;

    /* Exit program */ 
    return ;
}

/* --- Extract parameter values for PPROJ from user struct --- */
void pproj_matlab_get_parm
(
    const mxArray *options, /* Pointer to struct containing user problem data */
    PPparm *Parm            /* Pointer to pproj parm struct */
)
{
    /* Initialize variables */
    double maxits ;
    mxArray *field ;

    /* ------------------------ PPROJ parameters ------------------------ */
    /* Detailed description of parameters found in PPROJ/Include/pproj.h */
    if ((field = mxGetField(options, 0, "PrintStatus")) != NULL)
    {
        Parm->PrintStatus = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "PrintStat")) != NULL)
    {
        Parm->PrintStat = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "PrintLevel")) != NULL)
    {
        Parm->PrintLevel = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "PrintParm")) != NULL)
    {
        Parm->PrintParm = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_prior_data")) != NULL)
    {
        Parm->use_prior_data = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "loExists")) != NULL)
    {
        Parm->loExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "hiExists")) != NULL)
    {
        Parm->hiExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "getfactor")) != NULL)
    {
        Parm->getfactor = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "debug")) != NULL)
    {
        Parm->debug = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "checktol")) != NULL)
    {
        Parm->checktol = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "start_guess")) != NULL)
    {
        Parm->start_guess = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "permute")) != NULL)
    {
        Parm->permute = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "phase1")) != NULL)
    {
        Parm->phase1 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "cholmod")) != NULL)
    {
        Parm->cholmod = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "multilevel")) != NULL)
    {
        Parm->multilevel = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "stop_condition")) != NULL)
    {
        Parm->stop_condition = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "sigma")) != NULL)
    {
        Parm->sigma = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "Asigma")) != NULL)
    {
        Parm->Asigma = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ScaleSigma")) != NULL)
    {
        Parm->ScaleSigma = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "sigma_decay")) != NULL)
    {
        Parm->sigma_decay = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "nprox")) != NULL)
    {
        Parm->nprox = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "armijo_grow")) != NULL)
    {
        Parm->armijo_grow = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "narmijo")) != NULL)
    {
        Parm->narmijo = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "mem")) != NULL)
    {
        Parm->mem = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "nsparsa")) != NULL)
    {
        Parm->nsparsa = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "gamma")) != NULL)
    {
        Parm->gamma = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "tau")) != NULL)
    {
        Parm->tau = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "beta")) != NULL)
    {
        Parm->beta = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "grad_decay")) != NULL)
    {
        Parm->grad_decay = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "gamma_decay")) != NULL)
    {
        Parm->gamma_decay = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_coor_ascent")) != NULL)
    {
        Parm->use_coor_ascent = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "coorcost")) != NULL)
    {
        Parm->coorcost = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_ssor0")) != NULL)
    {
        Parm->use_ssor0 = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_ssor1")) != NULL)
    {
        Parm->use_ssor1 = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_sparsa")) != NULL)
    {
        Parm->use_sparsa = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "use_startup")) != NULL)
    {
        Parm->use_startup = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ssordecay")) != NULL)
    {
        Parm->ssordecay = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ssorcost")) != NULL)
    {
        Parm->ssorcost = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ssormem")) != NULL)
    {
        Parm->ssormem = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ssormaxits")) != NULL)    
    {
        maxits = mxGetScalar(field) ;
    
        if ( maxits == PPINF )
        {
            Parm->ssormaxits = PPINFINT ;
        }
        else
        {
            Parm->ssormaxits = (PPINT) maxits ; 
        }
    }
    if ((field = mxGetField(options, 0, "cutfactor")) != NULL)
    {
        Parm->cutfactor = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "tolssor")) != NULL)
    {
        Parm->tolssor = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "tolprox")) != NULL)
    {
        Parm->tolprox = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "tolrefactor")) != NULL)
    {
        Parm->tolrefactor = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "badFactorCutoff")) != NULL)
    {
        Parm->badFactorCutoff = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "LP")) != NULL)
    {
        Parm->LP = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "LinFactor")) != NULL)
    {
        Parm->LinFactor = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "LinGrad_tol")) != NULL)
    {
        Parm->LinGrad_tol = mxGetScalar(field) ; 
    }
}

/* --- Extract problem statistics for PPROJ to return to user --- */
void pproj_matlab_get_stat
(
    mxArray **out, /* mxArray in which pproj statistics will be stored */
    PPstat *Stat   /* Pointer to pproj stats struct with problem stats */
)
{
    /* Initialize variables */
    mxArray *fout, *sout ;
    int ifield, *idata, j ;
    double *pdata ;
    const char *pproj_fnames[55] = {/* pproj statistics are listed here */
                                    "updowns", "solves", "status", 
                                    "parm_nprox", "cholmod", 
                                    "badFactorCutoff", "ibad", "ssormaxits",
                                    "nrow", "size_updowns", "maxdepth", 
                                    "blks", "nchols", "nprox", 
                                    "phase1_its", "coor_ascent_its", 
                                    "ssor0_its", "ssor1_its", 
                                    "sparsa_its", "coldn", "colup", 
                                    "rowdn", "rowup", "coor_ascent_free", 
                                    "coor_ascent_drop", "ssor0_free", 
                                    "ssor0_drop", "ssor1_free", 
                                    "ssor1_drop", "sparsa_col", 
                                    "sparsa_row", "sparsa_step_fail", 
                                    "lnnz", "lobad", "hibad", "grad_tol", 
                                    "errdual", "partition", "initialize", 
                                    "phase1", "sparsa", "coor_ascent", 
                                    "ssor0", "ssor1", "dasa", 
                                    "dasa_line", "checkerr", 
                                    "prox_update", "invert", "modrow", 
                                    "modcol", "chol", "cholinc", 
                                    "dltsolve", "lsolve"} ;
    /* Create struct matrix with pproj statistic names */
    *out = mxCreateStructMatrix(1, 1, 55, pproj_fnames) ;

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("pproj_matlab_get_stat::Initialized variables\n") ;
    #endif

    /* Cycle through fnames and store stats in idata or pdata */
    for(ifield = 0; ifield < 55; ifield++)
    {
        #if 0
        mexPrintf("pproj_matlab_get_stat::ifield = %d\n", ifield) ;
        #endif

        if ( ifield  > 32 )
        {
            /* Set fout to 1 by 1 number matrix of doubles */
            fout = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL) ;
            /* Set pdata as pointer to double fout */
            pdata = (double *) mxGetData (fout) ;
        }
        else if ( ifield > 1)
        {
            /* Set fout as 1 by 1 matrix of type int */
            fout = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL) ;
            /* Set idata as pointer to int fout */
            idata = (int *) mxGetData (fout) ;
        }
        else if ( ifield > 0 )
        {
            /* Check if maxdepth is EMPTY */
            if ((Stat->maxdepth == EMPTY) || (Stat->maxdepth == 0))
            {
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj_matlab_get_stat::maxdepth == EMPTY or 0\n") ;
                #endif

                /* Set the solves array to indicate EMPTY */
                mxSetFieldByNumber(*out, 0, ifield, mxCreateString("EMPTY")) ;
                /* Continue to next element in ifield */
                continue ;
            }
            else
            { 
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj_matlab_get_stat::maxdepth != EMPTY\n") ;
                #endif

                /* Set fout as 1 by Stat->maxdepth matrix of type int */
                fout = mxCreateNumericMatrix(1, Stat->maxdepth + 1,
                                             mxINT32_CLASS, mxREAL) ;
                /* Set idata as pointer to int fout */
                idata = (int *) mxGetData (fout) ;
            }
        }
        else
        {
            /* Check if sizeupdowns is zero */
            if (Stat->size_updowns == 0)
            {
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj_matlab_get_stat::size_updowns == 0\n") ;
                #endif

                /* Set the updowns array to indicate EMPTY */
                mxSetFieldByNumber(*out, 0, ifield, mxCreateString("EMPTY")) ;
                /* Continue to next element in ifield */
                continue ;
            }
            else
            { 
                #if DEBUG_SUITEOPT_MEX
                mexPrintf("pproj_matlab_get_stat::size_updowns != 0\n") ;
                #endif

                /* Set fout as 1 by Stat->size_updowns matrix of type int */
                fout = mxCreateNumericMatrix(1, Stat->size_updowns,
                                             mxINT32_CLASS, mxREAL) ;
                /* Set idata as pointer to int fout */
                idata = (int *) mxGetData (fout) ;
            }
        }

        /* Set pdata to point to stat for case ifield */
        switch (ifield)
        {
            case 0: for (j = 0; j < Stat->size_updowns; j++)
                    {
                        idata [j] = Stat->updowns [j] ;
                    }
                    break ;
            case 1: for (j = 0; j < Stat->maxdepth + 1; j++)
                    {
                        idata [j] = Stat->solves [j] ;
                    }
                    break ;
            case 2: *idata = Stat->status ; break ;
            case 3: *idata = Stat->parm_nprox ; break ;
            case 4: *idata = Stat->cholmod ; break ;
            case 5: *idata = Stat->badFactorCutoff ; break ;
            case 6: *idata = Stat->ibad ; break ;
            case 7: *idata = Stat->ssormaxits ; break ;
            case 8: *idata = Stat->nrow ; break ;
            case 9: *idata = Stat->size_updowns ; break ;
            case 10: *idata = Stat->maxdepth ; break ;
            case 11: *idata = Stat->blks ; break ;
            case 12: *idata = Stat->nchols ; break ;
            case 13: *idata = Stat->nprox ; break ;
            case 14: *idata = Stat->phase1_its ; break ;
            case 15: *idata = Stat->coor_ascent_its ; break ;
            case 16: *idata = Stat->ssor0_its ; break ;
            case 17: *idata = Stat->ssor1_its ; break ;
            case 18: *idata = Stat->sparsa_its ; break ;
            case 19: *idata = Stat->coldn ; break ;
            case 20: *idata = Stat->colup ; break ;
            case 21: *idata = Stat->rowdn ; break ;
            case 22: *idata = Stat->rowup ; break ;
            case 23: *idata = Stat->coor_ascent_free ; break ;
            case 24: *idata = Stat->coor_ascent_drop ; break ;
            case 25: *idata = Stat->ssor0_free ; break ;
            case 26: *idata = Stat->ssor0_drop ; break ;
            case 27: *idata = Stat->ssor1_free ; break ;
            case 28: *idata = Stat->ssor1_drop ; break ;
            case 29: *idata = Stat->sparsa_col ; break ;
            case 30: *idata = Stat->sparsa_row ; break ;
            case 31: *idata = Stat->sparsa_step_fail ; break ;
            case 32: *idata = Stat->lnnz ; break ;
            case 33: *pdata = Stat->lobad ; break ;
            case 34: *pdata = Stat->hibad ; break ;
            case 35: *pdata = Stat->grad_tol ; break ;
            case 36: *pdata = Stat->errdual ; break ;
            case 37: *pdata = Stat->partition ; break ;
            case 38: *pdata = Stat->initialize ; break ;
            case 39: *pdata = Stat->phase1 ; break ;
            case 40: *pdata = Stat->sparsa ; break ;
            case 41: *pdata = Stat->coor_ascent ; break ;
            case 42: *pdata = Stat->ssor0 ; break ;
            case 43: *pdata = Stat->ssor1 ; break ;
            case 44: *pdata = Stat->dasa ; break ;
            case 45: *pdata = Stat->dasa_line ; break ;
            case 46: *pdata = Stat->checkerr ; break ;
            case 47: *pdata = Stat->prox_update ; break ;
            case 48: *pdata = Stat->invert ; break ;
            case 49: *pdata = Stat->modrow ; break ;
            case 50: *pdata = Stat->modcol ; break ;
            case 51: *pdata = Stat->chol ; break ;
            case 52: *pdata = Stat->cholinc ; break ;
            case 53: *pdata = Stat->dltsolve ; break ;
            case 54: *pdata = Stat->lsolve ; break ;
        }
        /* Set the ifieldth component of *out to fout */
        mxSetFieldByNumber(*out, 0, ifield, fout) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("pproj statistics copied to stats struct\n") ;
    #endif

    /* Exit program */ 
    return ;
}

/* --- Routine to print all elements imported to PPROJ data struct --- */
void pproj_matlab_print_data
(
    PPdata *data   /* Pointer to pproj data struct with problem data */ 
)
{
    /* Initialize variables */
    int i ;

    mexPrintf("\nInput Variables:\n") ;
    mexPrintf("ncol = %i\n", data->ncol) ;
    mexPrintf("nrow = %i\n", data->nrow) ;
    mexPrintf("grad_tol = %g\n", data->Parm->grad_tol) ;
    /* Print y */
    for (i = 0; i < data->ncol; i++)
    {
        mexPrintf("y[%i] = %g\n", i, data->y[i]) ;
    }
    /* Print x */
    if (data->x != NULL)
    {
        mexPrintf("\nPrinting the first 10 components of x:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++)
        {
            mexPrintf("x[%i] = %g\n", i, data->x[i]) ;
        }
    }
    else
    {
        mexPrintf("x not provided.\n") ;
    }
    /* Print lambda */
    if (data->lambda != NULL)
    {
        mexPrintf("\nPrinting the first 10 components of lambda:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++)
        {
            mexPrintf("lambda[%i] = %g\n", i, data->lambda[i]) ;
        }
    }
    else
    {
        mexPrintf("lambda not provided. lambda set to default.\n") ;
    }
    /* Print lo and hi */
    if (data->lo != NULL)
    {
        mexPrintf("\nPrinting the first 10 components of lo:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++)
        {
            mexPrintf("lo[%i] = %g\n", i, data->lo[i]) ;
        }
    }
    else
    {
        mexPrintf("lo not provided.\n") ;
    }
    if (data->hi != NULL)
    {
        mexPrintf("\nPrinting the first 10 components of hi:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++)
        {
            mexPrintf("hi[%i] = %g\n", i, data->hi[i]) ;
        }
    }
    else
    {
        mexPrintf("hi not provided.\n") ;
    }
    /* Print matrix A in sparse format */
    if (data->ncol != 0)
    {
        if (data->Ap != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of Ap:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++)
            {
                mexPrintf("Ap[%i] = %i\n", i, data->Ap[i]) ;
            }
        }
        if (data->Ai != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of Ai:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->Ap[data->ncol], 10); i++)
            {
                mexPrintf("Ai[%i] = %i\n", i, data->Ai[i]) ;
            }
        }
        if (data->Ax != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of Ax:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->Ap[data->ncol], 10); i++)
            {
                mexPrintf("Ax[%i] = %g\n", i, data->Ax[i]) ;
            }
        }
    }
    /* Print bl, bu, ni, nsing, singlo, singhi, and singc */
    if (data->nrow != 0)
    {
        if (data->bl != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of bl:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++)
            {
                mexPrintf("bl[%i] = %g\n", i, data->bl[i]) ;
            }
        }
        if (data->bu != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of bu:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++)
            {
                mexPrintf("bu[%i] = %g\n", i, data->bu[i]) ;
            }
        }
        mexPrintf("ni = %g\n", data->ni) ;
        mexPrintf("nsing = %g\n", data->nsing) ;
        if (data->row_sing != NULL)
        {
            for (i = 0; i <= data->nrow; i++)
            {
                mexPrintf("row_sing[%i] = %g\n", i, data->row_sing[i]) ;
            }
        }
        if (data->nsing > 0)
        {
            if (data->singlo != NULL)
            {
                for (i = 0; i < data->nsing; i++)
                {
                    mexPrintf("singlo[%i] = %g\n", i, data->singlo[i]) ;
                }
            }
            if (data->singhi != NULL)
            {
                for (i = 0; i < data->nsing; i++)
                {
                    mexPrintf("singhi[%i] = %g\n", i, data->singhi[i]) ;
                }
            }
            if (data->singc != NULL)
            {
                for (i = 0; i < data->nsing; i++)
                {
                    mexPrintf("singc[%i] = %g\n", i, data->singc[i]) ;
                }
            }
        }
    }
    mexPrintf("\n") ;

    mexPrintf("Completed printing all user data for pproj.\n") ;

    /* Exit function */
    return ;
}
