/* --- PASA functions required by more than one mex function --- */
/* This file contains function definitions associated with PASA 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Include header files ---------- */
#include "pasa_matlab.h"

/* --- Function to print additional info for user --- */
void pasa_matlab_print_info ()
{
    /* Print help info for pasa */
    printf ("\n  =========================== PASA Additional Info  ") ;
    printf ("============================\n") ;
    printf ("    - For more detailed information on pasa type ") ;
    printf (       "'pasa readme'\n") ;
    printf ("    - For a list of all default parameter values, ") ;
    printf ("type 'pasa all' or\n      'pasa allparms'.\n") ;
    printf ("    - For a list of default parameter values for ") ;
    printf ("pasa, type 'pasa parm'\n") ;
    printf ("    - For a list of default parameter values for ") ;
    printf ("pproj, type 'pasa pproj'\n") ;
    printf ("    - For a list of default parameter values for ") ;
    printf ("cg, type 'pasa cg'\n") ;
    printf ("    - For a list of default parameter values for ") ;
    printf ("napheap, type 'pasa napheap'\n") ;
    printf ("    - For detailed examples showing how to set up and ") ;
    printf (       "call pasa in MATLAB,\n      type 'pasa demo', ") ;
    printf (       "'pasa demoQP', or 'pasa demoOC'\n") ;
    printf ("    - Type 'demo', 'demoQP', or 'demoOC' to solve a ") ;
    printf ("sample problem\n") ;
    printf ("    - For all available help options type 'pasa'\n") ;
    printf ("  ============================================") ;
    printf ("==================================\n\n") ;

    /* Exit program */ 
    return ;
}

/* --- Extract parameter values for PASA from user struct --- */
void pasa_matlab_get_parm
(
    const mxArray *options, /* Pointer to struct containing user problem data */
    PASAparm *Parm          /* Pointer to pasa parm struct */
)
{
    /* Initialize variables */
    double maxits ;
    mxArray *field ;

    /* ---------------------- PASA parameters ---------------------- */
    /* Detailed description of parameters found in PASA/Source/pasa.c */
    if ((field = mxGetField(options, 0, "UNC")) != NULL)
    {
        Parm->UNC = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "BNC")) != NULL)
    {
        Parm->BNC = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "LP")) != NULL)
    {
        Parm->LP = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "QP")) != NULL)
    {
        Parm->QP = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "NL")) != NULL)
    {
        Parm->NL = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "NAPSACK")) != NULL)
    {
        Parm->NAPSACK = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "PROJ")) != NULL)
    {
        Parm->PROJ = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "grad_tol")) != NULL)
    {
        Parm->grad_tol = mxGetScalar(field) ;
    }
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
    if ((field = mxGetField(options, 0, "PrintLevel")) != NULL)
    {
        Parm->PrintLevel = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "GradProjOnly")) != NULL)
    {
        Parm->GradProjOnly = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "use_activeGP")) != NULL)
    {
        Parm->use_activeGP = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "use_napheap")) != NULL)
    {
        Parm->use_napheap = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "use_hessian")) != NULL)
    {
        Parm->use_hessian = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "loExists")) != NULL)
    {
        Parm->loExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "hiExists")) != NULL)
    {
        Parm->hiExists = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "updateorder")) != NULL)
    {
        Parm->updateorder = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "epsilon")) != NULL)
    {
        Parm->epsilon = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "cerr_decay")) != NULL)
    {
        Parm->cerr_decay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "EpsilonGrow")) != NULL)
    {
        Parm->EpsilonGrow = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "EpsilonDecay")) != NULL)
    {
        Parm->EpsilonDecay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "fadjust")) != NULL)
    {
        Parm->fadjust = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "use_lambda")) != NULL)
    {
        Parm->use_lambda = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "pproj_start_guess")) != NULL)
    {
        Parm->pproj_start_guess = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "use_penalty")) != NULL)
    {
        Parm->use_penalty = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "penalty")) != NULL)
    {
        Parm->penalty = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "debug")) != NULL)
    {
        Parm->debug = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "debugtol")) != NULL)
    {
        Parm->debugtol = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "switchfactor")) != NULL)
    {
        Parm->switchfactor = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "switchdecay")) != NULL)
    {
        Parm->switchdecay =  mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "terminate_agp")) != NULL)
    {
        Parm->terminate_agp = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "testit")) != NULL)
    {
        Parm->testit = (PASAINT) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "GPtol")) != NULL)
    {
        Parm->GPtol = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "gpmaxit")) != NULL)    
    {
        maxits = mxGetScalar(field) ; 
    
        if ( maxits = PASAINF )
        {
            Parm->gpmaxit = PASAINFINT ;
        }
        else
        {
            Parm->gpmaxit = (PASAINT) maxits ;
        }
    }
    if ((field = mxGetField(options, 0, "restart_fac")) != NULL)
    {
        Parm->restart_fac =  mxGetScalar(field) ;
    }
    
    if ((field = mxGetField(options, 0, "L")) != NULL)
    {
        Parm->L = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "M")) != NULL)
    {
        Parm->M = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "P")) != NULL)
    {
        Parm->P = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "gamma1")) != NULL)
    {
        Parm->gamma1 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "gamma2")) != NULL)
    {
        Parm->gamma2 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "gamma3")) != NULL)
    {
        Parm->gamma3 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "lambda0")) != NULL)
    {
        Parm->lambda0 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "lambda0Factor")) != NULL)
    {
        Parm->lambda0Factor = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "bbk")) != NULL)
    {
        Parm->bbk = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "bbexpand")) != NULL)
    {
        Parm->bbexpand = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "bbSwitchFactor")) != NULL)
    {
        Parm->bbSwitchFactor = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "MaximumCycle")) != NULL)
    {
        Parm->MaximumCycle = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "NominalCycle")) != NULL)
    {
        Parm->NominalCycle = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "approxstep")) != NULL)
    {
        Parm->approxstep = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "ArmijoSwitchFactor")) != NULL)
    {
        Parm->ArmijoSwitchFactor = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "PertRule")) != NULL)
    {
        Parm->PertRule = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "pert_eps")) != NULL)
    {
        Parm->pert_eps = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "neps")) != NULL)
    {
        Parm->neps = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "Armijo_delta")) != NULL)
    {
        Parm->Armijo_delta = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "Wolfe_delta")) != NULL)
    {
        Parm->Wolfe_delta = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "Wolfe_sigma")) != NULL)
    {
        Parm->Wolfe_sigma =  mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "maxsteps")) != NULL)
    {
        Parm->maxsteps = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "stepdecay")) != NULL)
    {
        Parm->stepdecay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "safe0")) != NULL)
    {
        Parm->safe0 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "safe1")) != NULL)
    {
        Parm->safe1 = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "infdecay")) != NULL)
    {
        Parm->infdecay = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "infdecay_rate")) != NULL)
    {
        Parm->infdecay_rate = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "ninf_tries")) != NULL)
    {
        Parm->ninf_tries = (int) mxGetScalar(field) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("Imported user PASA parameters\n") ;
    #endif
}

/* --- Extract parameter values for PASA from user struct --- */
void pasa_matlab_get_parms (
    const mxArray *options, /* Pointer to struct containing user problem data */
    PASAparms *Parms        /* Pointer to PASAparms struct */
) {
    /* Initialize variables */
    mxArray *field ;

    /* --- PASA parameters --- */
    if ((field = mxGetField(options, 0, "pasa")) != NULL)
    {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Importing pasa parms \n") ;
        #endif

        pasa_matlab_get_parm (field, Parms->pasa) ;
    }

    /* --- PPROJ parameters --- */
    if ((field = mxGetField(options, 0, "pproj")) != NULL)
    {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Importing pproj parms \n") ;
        #endif

        pproj_matlab_get_parm (field, Parms->pproj) ;
    }

    /* --- CGDESCENT parameters --- */
    if ((field = mxGetField(options, 0, "cg")) != NULL)
    {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Importing cg parms \n") ;
        #endif

        cg_matlab_get_parm (field, Parms->cg) ;
    }

    /* --- NAPHEAP parameters --- */
    if ((field = mxGetField(options, 0, "napheap")) != NULL)
    {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Importing napheap parms \n") ;
        #endif

        napheap_matlab_get_parm (field, Parms->napheap) ;
    }
    
    /* --- Exit function --- */
    return ;
}

/* --- Extract problem statistics for PASA to return to user --- */
void pasa_matlab_get_stat (
    mxArray **out, /* mxArray in which pasa statistics will be stored */
    PASAstat *Stat /* Pointer to pasa stats struct with all solver stats */
) {
    /* Initialize variables */
    mxArray *fout, *sout ;
    int ifield, *idata, j ;
    double *pdata ;
    const char *pasa_fnames[12] = {/* pasa statistics are listed here */
                                  "status", "err", "f", "mcnf", "mcng",  
                                  "gpit", "gpnf", "gpng", "agpit", "agpnf", 
                                  "agpng", "nproject"} ; 

    /* Create struct matrix with pasa statistic names for output */
    *out = mxCreateStructMatrix(1, 1, 12, pasa_fnames) ;

    /* ------------------ Store pasa statistics -------------------- */
    /* Cycle through fnames and store stats in pdata */
    for (ifield = 0; ifield < 12; ifield++)
    {
        if ( ifield  > 0 )
        {
            /* Set fout to 1 by 1 number matrix of doubles */
            fout = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL) ;
            /* Set pdata as pointer to double fout */
            pdata = (double *) mxGetData (fout) ;
        }
        else
        {
            /* Set fout to 1 by 1 number matrix of integers */
            fout = mxCreateNumericMatrix(1, 1, mxINT32_CLASS, mxREAL) ;
            /* Set pdata as pointer to double fout */
            idata = (int *) mxGetData (fout) ;
        }

        /* Set pdata to point to stat for case ifield */
        switch (ifield)
        {
            case 0: *idata = Stat->status ; break ; 
            case 1: *pdata = Stat->err ; break ; 
            case 2: *pdata = Stat->f ; break ; 
            case 3: *pdata = Stat->mcnf ; break ; 
            case 4: *pdata = Stat->mcng ; break ; 
            case 5: *pdata = Stat->gpit ; break ; 
            case 6: *pdata = Stat->gpnf ; break ; 
            case 7: *pdata = Stat->gpng ; break ; 
            case 8: *pdata = Stat->agpit ; break ; 
            case 9: *pdata = Stat->agpnf ; break ; 
            case 10: *pdata = Stat->agpng ; break ; 
            case 11: *pdata = Stat->nproject ; break ; 
        }
        /* Set the ifieldth component of out to fout */
        mxSetFieldByNumber(*out, 0, ifield, fout) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("pasa statistics copied to stats struct\n") ;
    #endif

    /* Exit program */ 
    return ;
}

/* --- Extract problem stats for all solvers PASA used and return to user --- */
void pasa_matlab_get_stats
(
    mxArray **out,    /* mxArray in which pasa statistics will be stored */
    PASAstats *Stats, /* Pointer to pasa stats struct with all solver stats */
    int Aexists       /* 0 if no constraint matrix A; 1 otherwise */
)
{
    /* Initialize variables */
    mxArray *tout[4] ;
    /* Names of all solvers that generate statistics within PASA */
    const char *stats_fnames[4] = {"pasa", "pproj", "cg", "napheap"} ;
    /* Indicators when statistics not generated by solvers within PASA */
    const char *pprojunused_fnames[1] = {"PPROJ_NOT_USED"} ;
    const char *cgunused_fnames[1] = {"CGDESCENT_NOT_USED"} ;
    const char *napunused_fnames[1] = {"NAPHEAP_NOT_USED"} ;

    /* Create struct matrix for output */
    *out = mxCreateStructMatrix(1, 1, 4, stats_fnames) ;

    /* ------------------ Store pasa statistics -------------------- */
    #if DEBUG_SUITEOPT_MEX
    mexPrintf("Extracting pasa statistics\n") ;
    #endif

    /* Copy pasa statistics */
    pasa_matlab_get_stat (&tout[0], Stats->pasa) ;

    /* Write pasa statistics to output array */
    mxSetFieldByNumber(*out, 0, 0, tout[0]) ;

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("pasa statistics copied to stats struct\n") ;
    #endif

    /* ------------------ Store pproj statistics -------------------- */
    /* Check if pproj statistics were generated */
    if (Aexists == TRUE) {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("pproj statistics generated. Copying to struct.\n") ;
        mexPrintf("maxdepth = %i\n", Stats->pproj->maxdepth) ;
        mexPrintf("size_updowns = %i\n", Stats->pproj->size_updowns) ;
        mexPrintf("Extracting pproj statistics\n") ;
        #endif

        /* Copy pproj statistics */
        pproj_matlab_get_stat (&tout[1], Stats->pproj) ;

        /* Write pproj statistics to output array */
        mxSetFieldByNumber(*out, 0, 1, tout[1]) ;
    }
    else {/* pproj not used in computing solution, indicate to user */ 
        /* Write unused indicator for pproj statistics to output array */
        tout[1] = mxCreateStructMatrix(1, 1, 1, pprojunused_fnames) ;
        mxSetFieldByNumber(tout[1], 0, 0, mxCreateString("TRUE")) ;
        mxSetFieldByNumber(*out, 0, 1, tout[1]) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("pproj statistics copied to stats struct\n") ;
    #endif

    /* ------------------ Store cg statistics -------------------- */
    /* Check if cg statistics were generated */
    if (Stats->cg != NULL) {
        /* Check if number of cg iterations is nonzero */
        if (Stats->cg->iter != 0) {
            #if DEBUG_SUITEOPT_MEX
            mexPrintf("Extracting cg statistics\n") ;
            #endif

            /* Copy cg statistics */
            cg_matlab_get_stat (&tout[2], Stats->cg) ;

            /* Write cg statistics to output array */
            mxSetFieldByNumber(*out, 0, 2, tout[2]) ;
        }
        else {/* cg_descent not used in computing solution, indicate to user */
            /* Write unused indicator for cg statistics to output array */
            tout[2] = mxCreateStructMatrix(1, 1, 1, cgunused_fnames) ;
            mxSetFieldByNumber(tout[2], 0, 0, mxCreateString("TRUE")) ;
            mxSetFieldByNumber(*out, 0, 2, tout[2]) ;
        }
    }
    else {/* cg_descent not used in computing solution, indicate to user */
        /* Write unused indicator for cg statistics to output array */
        tout[2] = mxCreateStructMatrix(1, 1, 1, cgunused_fnames) ;
        mxSetFieldByNumber(tout[2], 0, 0, mxCreateString("TRUE")) ;
        mxSetFieldByNumber(*out, 0, 2, tout[2]) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("cg statistics copied to stats struct\n") ;
    #endif

    /* ------------------ Store napheap statistics -------------------- */
    /* Check if napheap statistics were generated */
    if (Stats->napheap != NULL) {
        #if DEBUG_SUITEOPT_MEX
        mexPrintf("Extracting napheap statistics\n") ;
        #endif

        /* Copy napheap statistics */
        napheap_matlab_get_stat (&tout[3], Stats->napheap) ;

        /* Write napheap statistics to output array */
        mxSetFieldByNumber(*out, 0, 3, tout[3]) ;
    }
    else {/* napheap not used in computing solution, indicate to user */ 
        /* Write unused indicator for napheap statistics to output array */
        tout[3] = mxCreateStructMatrix(1, 1, 1, napunused_fnames) ;
        mxSetFieldByNumber(tout[3], 0, 0, mxCreateString("TRUE")) ;
        mxSetFieldByNumber(*out, 0, 3, tout[3]) ;
    }

    #if DEBUG_SUITEOPT_MEX
    mexPrintf("napheap statistics copied to stats struct\n") ;
    #endif

    /* Exit program */ 
    return ;
}


/* --- Routine to print all elements imported to PASA data struct --- */
void pasa_matlab_print_data (
    PASAdata *data /* Pointer to pasa data struct with problem data */ 
) {
    /* Initialize variables */
    int i ;

    mexPrintf("\nInput Variables:\n") ;
    mexPrintf("ncol = %i\n", data->ncol) ;
    mexPrintf("nrow = %i\n", data->nrow) ;
    mexPrintf("grad_tol = %g\n", data->Parms->pasa->grad_tol) ;
    /* Print x */
    if (data->x != NULL) {
        mexPrintf("\nPrinting the first 10 components of x:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++) {
            mexPrintf("x[%i] = %g\n", i, data->x[i]) ;
        }
    }
    else {
        mexPrintf("x not provided.\n") ;
    }
    /* Print lambda */
    if (data->lambda != NULL) {
        mexPrintf("\nPrinting the first 10 components of lambda:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++) {
            mexPrintf("lambda[%i] = %g\n", i, data->lambda[i]) ;
        }
    }
    else {
        mexPrintf("lambda not provided. lambda set to default.\n") ;
    }
    /* Print lo and hi */
    if (data->lo != NULL) {
        mexPrintf("\nPrinting the first 10 components of lo:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++) {
            mexPrintf("lo[%i] = %g\n", i, data->lo[i]) ;
        }
    }
    else {
        mexPrintf("lo not provided.\n") ;
    }
    if (data->hi != NULL) {
        mexPrintf("\nPrinting the first 10 components of hi:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++) {
            mexPrintf("hi[%i] = %g\n", i, data->hi[i]) ;
        }
    }
    else {
        mexPrintf("hi not provided.\n") ;
    }
    /* Print matrix A in sparse format */
    if (data->ncol != 0) {
        if (data->Ap != NULL) {
            mexPrintf("\nPrinting the first 10 components of Ap:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++) {
                mexPrintf("Ap[%i] = %i\n", i, data->Ap[i]) ;
            }
        }
        if (data->Ai != NULL) {
            mexPrintf("\nPrinting the first 10 components of Ai:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->Ap[data->ncol], 10); i++) {
                mexPrintf("Ai[%i] = %i\n", i, data->Ai[i]) ;
            }
        }
        if (data->Ax != NULL) {
            mexPrintf("\nPrinting the first 10 components of Ax:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->Ap[data->ncol], 10); i++) {
                mexPrintf("Ax[%i] = %g\n", i, data->Ax[i]) ;
            }
        }
    }
    /* Print bl and bu */
    if (data->nrow != 0) {
        if (data->bl != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of bl:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++) {
                mexPrintf("bl[%i] = %g\n", i, data->bl[i]) ;
            }
        }
        if (data->bu != NULL)
        {
            mexPrintf("\nPrinting the first 10 components of bu:\n") ;
            for (i = 0; i < SUITEOPTMIN(data->nrow, 10); i++) {
                mexPrintf("bu[%i] = %g\n", i, data->bu[i]) ;
            }
        }
    }
    /* Print c */
    if (data->c != NULL)
    {
        mexPrintf("\nPrinting the first 10 components of c:\n") ;
        for (i = 0; i < SUITEOPTMIN(data->ncol, 10); i++)
        {
            mexPrintf("c[%i] = %g\n", i, data->c[i]) ;
        }
    }
    else
    {
        mexPrintf("c not provided.\n") ;
    }
    mexPrintf("\n") ;

    mexPrintf("Completed printing all user data for pasa.\n") ;

    /* Exit function */
    return ;
}
