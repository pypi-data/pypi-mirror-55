/* --- CGDESCENT functions required by more than one mex function --- */
/* This file contains function definitions associated with CGDESCENT 
   with calls in multiple MATLAB MEX functions found within SuiteOPT */

/* ---------- Include header files ---------- */
#include "cg_descent_matlab.h"

/* --- Function to print additional info for user --- */
void cg_matlab_print_info () {
    /* Print info for cg_descent */
    printf("\n  CGDESCENT (Conjugate Gradient with guaranteed DESCENT) is "
           "designed to solve\n  unconstrained optimization problems.\n");
    /* Print help info for cg_descent */
    printf("\n  ======================  CG_DESCENT Additional Info  ");
    printf("=========================\n");
    printf("    - For more detailed information on cg_descent type ");
    printf(       "'cg_descent readme'\n");
    printf("    - For a list of default parameter values type ");
    printf("'cg_descent parm'\n");
    printf("    - For detailed examples showing how to set up and ");
    printf(       "call cg_descent in\n      MATLAB, type ");
    printf(       "'cg_descent demo' or 'cg_descent demoQP'\n");
    printf("    - Type 'demo' or 'demoQP' to solve a sample problem\n");
    printf("    - For all available help options type 'cg_descent'\n");
    printf("  =================================================");
    printf("============================\n\n");

    /* Exit program */ 
    return ;
}

/* --- Extract parameter values for CGDESCENT from user struct --- */
void cg_matlab_get_parm (const mxArray *options, CGparm *Parm) {
    /* Initialize variables */
    double maxits ;
    mxArray *field ;

    #ifdef DEBUG_SUITEOPT_MEX
    mexPrintf("Importing CGDESCENT parameters.\n") ;
    #endif

    /* -------------------- CGDESCENT parameters -------------------- */
    /* Detailed description of parm in CGDESCENT/Include/cg_descent.h */
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
    if ((field = mxGetField(options, 0, "fadjust")) != NULL)
    {
        Parm->fadjust = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "QPshift")) != NULL)
    {
        Parm->QPshift = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "grad_tol")) != NULL)
    {
        Parm->grad_tol = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "StopFac")) != NULL)
    {
        Parm->StopFac = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "debug")) != NULL)
    {
        Parm->debug = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "debugtol")) != NULL)
    {
        Parm->debugtol = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "step")) != NULL)
    {
        Parm->step = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "LBFGS")) != NULL)
    {
        Parm->LBFGS = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "LBFGSmemory")) != NULL)
    {
        Parm->LBFGSmemory = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "maxit")) != NULL)    
    {
        maxits = mxGetScalar(field) ; 
    
        if ( maxits = CGINF )
        {
            Parm->maxit = CGINFINT ;
        }
        else
        {
            Parm->maxit = (CGINT) maxits ;
        }
    }
    if ((field = mxGetField(options, 0, "restart_fac")) != NULL)
    {
        Parm->restart_fac = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "Qdecay")) != NULL)
    {
        Parm->Qdecay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "nslow")) != NULL)
    {
        Parm->nslow = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "egrow")) != NULL)
    {
        Parm->egrow = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "QuadStep")) != NULL)
    {
        Parm->QuadStep = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "QuadCutOff")) != NULL)
    {
        Parm->QuadCutOff = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "QuadSafe")) != NULL)
    {
        Parm->QuadSafe = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "psi_lo")) != NULL)
    {
        Parm->psi_lo = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "psi_hi")) != NULL)
    {
        Parm->psi_hi = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "psi1")) != NULL)
    {
        Parm->psi1 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "qeps")) != NULL)
    {
        Parm->qeps = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "qrule")) != NULL)
    {
        Parm->qrule = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "qrestart")) != NULL)
    {
        Parm->qrestart = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "UseCubic")) != NULL)
    {
        Parm->UseCubic = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "CubicCutOff")) != NULL)
    {
        Parm->CubicCutOff = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "SmallCost")) != NULL)
    {
        Parm->SmallCost = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "ExpandSafe")) != NULL)
    {
        Parm->ExpandSafe = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "SecantAmp")) != NULL)
    {
        Parm->SecantAmp = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "RhoGrow")) != NULL)
    {
        Parm->RhoGrow = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "approxstep")) != NULL)
    {
        Parm->approxstep = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "ApproxSwitchFactor")) != NULL)
    {
        Parm->ApproxSwitchFactor = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "CostConverge")) != NULL)
    {
        Parm->CostConverge = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "FuncGradSwitchFactor")) != NULL)
    {
        Parm->FuncGradSwitchFactor = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "PertRule")) != NULL)
    {
        Parm->PertRule = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "pert_eps")) != NULL)
    {
        Parm->pert_eps = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "ncontract")) != NULL)
    {
        Parm->ncontract = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "eps_grow")) != NULL)
    {
        Parm->eps_grow = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "neps")) != NULL)
    {
        Parm->neps = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "cgdelta")) != NULL)
    {
        Parm->cgdelta = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "cgsigma")) != NULL)
    {
        Parm->cgsigma = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "maxsteps")) != NULL)
    {
        Parm->maxsteps = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "stepdecay")) != NULL)
    {
        Parm->stepdecay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "rho")) != NULL)
    {
        Parm->rho = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "psi0")) != NULL)
    {
        Parm->psi0 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "psi2")) != NULL)
    {
        Parm->psi2 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "BetaLower")) != NULL)
    {
        Parm->BetaLower = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "theta")) != NULL)
    {
        Parm->theta = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "AdaptiveTheta")) != NULL)
    {
        Parm->AdaptiveTheta = (int) mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "cg_infdecay")) != NULL)
    {
        Parm->cg_infdecay = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "cg_infdecay_rate")) != NULL)
    {
        Parm->cg_infdecay_rate = mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "cg_ninf_tries")) != NULL)
    {
        Parm->cg_ninf_tries = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "SubCheck")) != NULL)
    {
        Parm->SubCheck = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "SubSkip")) != NULL)
    {
        Parm->SubSkip = (int) mxGetScalar(field) ;
    }
    if ((field = mxGetField(options, 0, "eta0")) != NULL)
    {
        Parm->eta0 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "eta1")) != NULL)
    {
        Parm->eta1 = mxGetScalar(field) ; 
    }
    if ((field = mxGetField(options, 0, "eta2")) != NULL)
    {
        Parm->eta2 = mxGetScalar(field) ; 
    }

    #ifdef DEBUG_SUITEOPT_MEX
    mexPrintf("Finished importing CGDESCENT parameters.\n") ;
    #endif
}

/* --- Extract problem statistics for CGDESCENT to return to user --- */
void cg_matlab_get_stat (mxArray **out, CGstat *Stat)
{
    /* Initialize variables */
    mxArray *fout ;
    int ifield ;
    long *ldata ;
    double *pdata ;
    const char *cg_fnames[17] = {/* cg_descent statistics are listed here */
                                 "status", "f", "err", "grad_tol", "gnorm", 
                                 "tol", "maxit", "cg_ninf_tries", "oldf", 
                                 "newf", "maxsteps", "NegDiag", "iter", 
                                 "nfunc", "ngrad", "IterSub", "NumSub"};

    *out = mxCreateStructMatrix(1, 1, 17, cg_fnames) ;

    /* Cycle through fnames and store stats in pdata */
    for (ifield = 0; ifield < 17; ifield++)
    {
        /* Set fout as double */
        fout = mxCreateNumericMatrix(1, 1, mxDOUBLE_CLASS, mxREAL) ;
        /* Set pdata as pointer to double fout */
        pdata = (double *) mxGetData (fout) ;

        /* Set pdata to point to stat for case ifield */
        switch (ifield)
        {
            case 0: *pdata = Stat->status ; break ;
            case 1: *pdata = Stat->f ; break ;
            case 2: *pdata = Stat->err ; break ;
            case 3: *pdata = Stat->grad_tol ; break ;
            case 4: *pdata = Stat->gnorm ; break ;
            case 5: *pdata = Stat->tol ; break ;
            case 6: *pdata = Stat->maxit ; break ;
            case 7: *pdata = Stat->cg_ninf_tries ; break ;
            case 8: *pdata = Stat->oldf ; break ;
            case 9: *pdata = Stat->newf ; break ;
            case 10: *pdata = Stat->maxsteps ; break ;
            case 11: *pdata = Stat->NegDiag ; break ;
            case 12: *pdata = Stat->iter ; break ;
            case 13: *pdata = Stat->nfunc ; break ;
            case 14: *pdata = Stat->ngrad ; break ;
            case 15: *pdata = Stat->IterSub ; break ;
            case 16: *pdata = Stat->NumSub ; break ;
        }
        /* Set the ifieldth component of out to fout */
        mxSetFieldByNumber(*out, 0, ifield, fout) ;
    }
}
