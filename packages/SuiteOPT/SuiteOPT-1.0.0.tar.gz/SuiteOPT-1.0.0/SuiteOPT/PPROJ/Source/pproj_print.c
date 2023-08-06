/* ==========================================================================
   === pproj_print_status ====================================================
   ==========================================================================
    Print the status at termination of the run
   ========================================================================== */
#include "pproj.h"
#ifdef MATLAB_MEX_FILE
#define LPAREN "("
#define RPAREN ")"
#define OFFSET 1
#else
#define LPAREN "["
#define RPAREN "]"
#define OFFSET 0
#endif

void pproj_print_status
(
    PPdata *Data /* pproj data structure */
)
{
    PPstat *Stat = Data->Stat ;
    int status = Stat->status ;
    printf ("\nPPROJ run status (Version %d.%d, %s):\n\n",
        PPROJ_MAIN_VERSION, PPROJ_SUB_VERSION, PPROJ_DATE) ;

    if ( status == PPROJ_SOLUTION_FOUND )
    {
            printf ("PPROJ success: Error %e satisfies error "
                    "tolerance %e\n", Stat->errdual, Stat->grad_tol) ;
    }
    else if ( status == PPROJ_ERROR_DECAY_STAGNATES )
    {
        printf ("PPROJ did not converge after %i proximal iterations; ",
                Stat->parm_nprox) ;
        printf ("the error decay stagnated.\n") ;
    }
    else if ( status == PPROJ_OUT_OF_MEMORY )
    {
        printf ("PPROJ ran out of memory.\n") ;
    }
    else if ( status == PPROJ_SSOR_NONASCENT )
    {
        printf ("The SSOR method in PPROJ did not generate an ascent "
                "direction\n") ;
    }
    else if ( status == PPROJ_SSOR_MAX_ITS )
    {
        printf ("The SSOR method in PPROJ did not converge after %ld "
                "iterations\n", (LONG) Stat->ssormaxits) ;
    }
    else if ( status == PPROJ_MISSING_PRIOR_DATA)
    {
        printf ("In PPROJ, the parameter use_prior_data was TRUE, however,\n"
                "the priordata argument of ppdata was NULL\n") ;
    }
    else if ( status == PPROJ_START_GUESS_NEEDS_PRIOR_DATA )
    {
         printf ("In PPROJ, the start_guess parameter is 2 or 4 which\n"
                 "requires use of data from a prior run, but either\n"
                 "parameter use_prior_data is FALSE, or the priordata\n"
                 "argument of ppdata is NULL\n") ;
    }
    else if ( status == PPROJ_INVALID_LINEAR_CONSTRAINT_BOUNDS )
    {
        printf ("In PPROJ, the linear inequality bounds are invalid since "
                "Bl %s%ld%s = %e > Bu %s%ld%s = %e.\n", 
            LPAREN, (LONG) Stat->ibad + OFFSET, RPAREN, Stat->lobad, 
            LPAREN, (LONG) Stat->ibad + OFFSET, RPAREN, Stat->hibad) ;
    }
    else if ( status == PPROJ_DUAL_SOLVE_ERROR )
    {
        printf ("In PPROJ, an accurate solution of the dual linear system\n"
                "was not achieved in %i (parameter badFactorCutoff)\n"
                "consecutive iterations\n", Stat->badFactorCutoff) ;
    }
    else if ( status == PPROJ_START_GUESS_IS_1_BUT_LAMBDA_NULL )
    {
        printf ("In PPROJ, the start_guess parameter is 1, which\n"
                "implies that the ppdata input parameter lambda\n"
                "is employed as a starting guess for the dual\n"
                "multiplier, however, lambda is NULL\n") ;
    }
    else if ( status == PPROJ_START_GUESS_IS_2_BUT_CHOLMOD_FALSE )
    {
        printf ("In PPROJ, it is currently required that CHOLMOD\n"
                "was used when the start_guess parameter is 2\n") ;
    }
    else if ( status == PPROJ_START_GUESS_IS_3_BUT_LAMBDA_NULL )
    {
        printf ("In PPROJ, the start_guess parameter is 3, which\n"
                "implies that the ppdata input parameter lambda\n"
                "is employed as a starting guess for the dual\n"
                "multiplier, however, lambda is NULL\n") ;
    }
    else if ( status == PPROJ_BOTH_NI_AND_NSING_POSITIVE )
    {
        printf ("In PPROJ, it was found that parameter nsing is\n"
                "positive and there are one or more strict linear\n"
                "inequalities. Currently, the code does not handle\n"
                "this case. Convert the strict linear inequalities\n"
                "to equalities by introducing slack variables with\n"
                "bounds. Note that each slack variable increases\n"
                "the value of nsing by one.\n") ;
    }
    else if ( status == PPROJ_OPTIMAL_COST_IS_MINUS_INFINITY )
    {
        printf ("In PPROJ, the optimal objective is minus infinity\n"
                "if the problem is feasible. If PPROJ was invoked by\n"
                "PASA, then the problem is an LP whose optimal objective\n"
                "is minus infinity if the problem is feasible.\n") ;
    }
    else if ( status == PPROJ_NSING_START_GUESS_PROB )
    {
        printf ("In PPROJ, currently need to have start_guess = 0\n"
                "when the column singleton feature is utilized\n") ;
    }
}

/* ========================================================================== */
/* === pproj_print_stat ===================================================== */
/* ========================================================================== */
/* Print the data stored in the PPstat structure
   NOTE: If Parm->free is TRUE, then Stat->updowns and Stat->solves
         are freed at the end of this routine, after printing their results.  */
/* ========================================================================== */
void pproj_print_stat
(
    PPdata *Data /* pproj data structure */
)
{
    int i, k ;
    double sparsity, n ;

    PPstat *Stat = Data->Stat ;
    if ( Stat == NULL ) return ;

    printf ("\nPPROJ run statistics (Version %d.%d, %s):\n\n",
        PPROJ_MAIN_VERSION, PPROJ_SUB_VERSION, PPROJ_DATE) ;

    printf ("No. blocks in multilevel partition of A . %i\n", Stat->blks) ;
    printf ("Depth of multilevel partition tree ...... %i\n", Stat->maxdepth) ;
    printf ("Phase 1 iterations ...................... %ld\n",
            (LONG) Stat->phase1_its);
    printf ("Coordinate ascent iterations ............ %ld\n",
            (LONG) Stat->coor_ascent_its) ;
    printf ("    variables freed in coordinate ascent  %ld\n",
            (LONG) Stat->coor_ascent_free) ;
    printf ("    rows dropped in coordinate ascent ... %ld\n",
            (LONG) Stat->coor_ascent_drop) ;
    printf ("Gradient ascent iterations .............. %ld\n",
            (LONG) Stat->ssor0_its) ;
    printf ("    variables freed in gradient ascent .. %ld\n",
            (LONG) Stat->ssor0_free) ;
    printf ("    rows dropped in gradient ascent ..... %ld\n",
            (LONG) Stat->ssor0_drop) ;
    printf ("Preconditioned CG iterations ............ %ld\n",
            (LONG) Stat->ssor1_its) ;
    printf ("    variables freed in CG ............... %ld\n",
            (LONG) Stat->ssor1_free) ;
    printf ("    rows dropped in CG .................. %ld\n",
            (LONG) Stat->ssor1_drop) ;
    printf ("SpaRSA iterations ....................... %ld\n",
            (LONG) Stat->sparsa_its) ;
    printf ("    change in column activity ........... %ld\n",
            (LONG) Stat->sparsa_col) ;
    printf ("    change in row activity .............. %ld\n",
            (LONG) Stat->sparsa_row) ;
    printf ("    failures of Armijo step ............. %ld\n",
            (LONG) Stat->sparsa_step_fail) ;
    printf ("Proximal updates ........................ %i\n",
            Stat->nprox) ;
    printf ("Cholesky factorizations ................. %i\n",
            Stat->nchols) ;
    printf ("    nonzeros in final factor ............ %ld",
            (LONG) Stat->lnnz) ;
    n = (double) Stat->nrow ;
    sparsity = 100*(1. - 2.*(double) Stat->lnnz/(n*n + n)) ;
    printf (" %4.1f%% sparse\n", sparsity) ;
    printf ("    rows dropped from L ................. %ld\n",
            (LONG)  Stat->rowdn) ;
    printf ("    rows added to L ..................... %ld\n",
            (LONG)  Stat->rowup) ;
    printf ("    rank 1 downdates to L ............... %ld\n",
            (LONG)  Stat->coldn) ;
    printf ("    rank 1 updates to L ................. %ld\n",
            (LONG)  Stat->colup) ;

    if ( Stat->updowns != NULL )
    {
        printf ("    Size breakdown of the updates ([size]: "
                "number of this size):\n") ;
        k = Stat->size_updowns ;
        for (i = 1; i < k; i++)
        {
            if (Stat->updowns [i] > 0)
            {
                printf ("        updowns [%3d]: %d\n", i, Stat->updowns [i]) ;
            }
        }
        if ( Stat->updowns [k] > 0 )
        {
            printf ("        updowns [>=%3d]: %d\n", k, Stat->updowns [k]) ;
        }
    }
    if ( Stat->blks != EMPTY )
    {
        if ( Stat->blks == 1 )
        {
            printf ("    No. of solves:   %i\n", Stat->solves [0]) ;
        }
        else
        {
            printf ("    No. of solves by depth in the multilevel partition "
                    "tree:\n") ;
            printf ("        (deeper <=> further from root of tree <=> "
                    "fewer flops)\n");
            for (i = 0; i <= Stat->maxdepth; i++)
            {
                printf ("        depth [%2d]: %d\n", i, Stat->solves [i]) ;
            }
        }
    }
    printf ("\n-------- Time spent in routines ---------\n") ;
    printf ("Multilevel partition and reorder A ...... %e\n", Stat->partition) ;
    printf ("Initialization (includes partition) ..... %e\n", Stat->initialize);
    printf ("Phase 1 ................................. %e\n", Stat->phase1) ;
    printf ("Coordinate ascent ....................... %e\n",Stat->coor_ascent);
    printf ("SSOR0 ................................... %e\n", Stat->ssor0);
    printf ("SSOR1 ................................... %e\n", Stat->ssor1);
    printf ("SpaRSA .................................. %e\n", Stat->sparsa);
    printf ("DASA .................................... %e\n", Stat->dasa) ;
    printf ("DASA line search ........................ %e\n", Stat->dasa_line) ;
    printf ("Check error ............................. %e\n", Stat->checkerr) ;
    printf ("Proximal update ......................... %e\n",Stat->prox_update);
    printf ("Invert permutation ...................... %e\n", Stat->invert) ;
    printf ("Row modifications of Cholesky factor .... %e\n", Stat->modrow) ;
    printf ("Column modifications of Cholesky factor . %e\n", Stat->modcol) ;
    printf ("Cholesky factorization .................. %e\n", Stat->chol) ;
    printf ("Partial Cholesky factorization .......... %e\n", Stat->cholinc) ;
    printf ("Back solves ............................. %e\n", Stat->dltsolve) ;
    printf ("Forward solves .......................... %e\n", Stat->lsolve) ;

    printf ("\n") ;

    /* NOTE: user can free Stat->updowns and Stat->solves if no longer needed */
}

/* =========================================================================
   ============================== pproj_print_parm =========================
   =========================================================================  */
/* Print data in the PPparm structure                                       */
/* ========================================================================== */
void pproj_print_parm
(
    PPdata *Data /* pproj data structure */
)
{
    PPparm *Parm = Data->Parm ;
    printf ("\nPPROJ parameter settings (Version %d.%d, %s):\n",
        PPROJ_MAIN_VERSION, PPROJ_SUB_VERSION, PPROJ_DATE) ;
    printf ("(see pproj_default for definitions)\n\n") ;

    printf ("grad_tol ...........: ") ;
    printf("%e\n", Parm->grad_tol) ;
    printf ("PrintLevel .........: ") ;
    printf ("%i\n", Parm->PrintLevel) ;
    printf ("PrintStatus ........: ") ;
    pproj_print_TF (Parm->PrintStatus) ;
    printf ("PrintStat ..........: ") ;
    pproj_print_TF (Parm->PrintStat) ;
    printf ("PrintParm ..........: ") ;
    pproj_print_TF (Parm->PrintParm) ;
    printf ("return_data ........: ") ;
    pproj_print_TF (Parm->return_data) ;
    printf ("use_prior_data .....: ") ;
    pproj_print_TF (Parm->use_prior_data) ;
    printf ("loExists ...........: ") ;
    pproj_print_TF (Parm->loExists) ;
    printf ("hiExists ...........: ") ;
    pproj_print_TF (Parm->hiExists) ;
    printf ("getfactor ..........: ") ;
    pproj_print_TF (Parm->getfactor) ;
    printf ("debug ..............: ") ;
    printf ("%i\n", Parm->debug) ;
    printf ("checktol ...........: ") ;
    printf("%e\n", Parm->checktol) ;
    printf ("start_guess ..........: ") ;
    printf("%i\n", Parm->start_guess) ;
    printf ("permute ..............: ") ;
    pproj_print_TF (Parm->permute) ;
    printf ("phase1 .............: ") ;
    printf("%e\n", Parm->phase1) ;
    printf ("cholmod ............: ") ;
    pproj_print_TF (Parm->cholmod) ;
    printf ("multilevel .........: ") ;
    pproj_print_TF (Parm->multilevel) ;
    printf ("stop_condition .....: ") ;
    printf ("%i\n", Parm->stop_condition) ;
    printf ("nprox ..............: ") ;
    printf("%i\n", Parm->nprox) ;
    printf ("sigma ..............: ") ;
    printf("%e\n", Parm->sigma) ;
    printf ("Asigma .............: ") ;
    printf("%e\n", Parm->Asigma) ;
    printf ("ScaleSigma .........: ") ;
    pproj_print_TF (Parm->ScaleSigma) ;
    printf ("sigma_decay ........: ") ;
    printf("%e\n", Parm->sigma_decay) ;
    printf ("armijo_grow ........: ") ;
    printf("%e\n", Parm->armijo_grow) ;
    printf ("narmijo ............: ") ;
    printf ("%i\n", Parm->narmijo) ;
    printf ("mem ................: ") ;
    printf ("%i\n", Parm->mem) ;
    printf ("nsparsa ............: ") ;
    printf ("%i\n", Parm->nsparsa) ;
    printf ("gamma ..............: ") ;
    printf("%e\n", Parm->gamma) ;
    printf ("tau ................: ") ;
    printf("%e\n", Parm->tau) ;
    printf ("beta ...............: ") ;
    printf("%e\n", Parm->beta) ;
    printf ("grad_decay .........: ") ;
    printf("%e\n", Parm->grad_decay) ;
    printf ("gamma_decay ........: ") ;
    printf("%e\n", Parm->gamma_decay) ;
    printf ("use_coor_ascent ....: ") ;
    pproj_print_TF (Parm->use_coor_ascent) ;
    printf ("coorcost ...........: ") ;
    printf("%e\n", Parm->coorcost) ;
    printf ("use_ssor0 ..........: ") ;
    pproj_print_TF (Parm->use_ssor0) ;
    printf ("use_ssor1 ..........: ") ;
    pproj_print_TF (Parm->use_ssor1) ;
    printf ("use_sparsa .........: ") ;
    pproj_print_TF (Parm->use_sparsa) ;
    printf ("use_startup ........: ") ;
    pproj_print_TF (Parm->use_startup) ;
    printf ("ssordecay ..........: ") ;
    printf("%e\n", Parm->ssordecay) ;
    printf ("ssormem ............: ") ;
    printf ("%i\n", Parm->ssormem) ;
    printf ("ssorcost ...........: ") ;
    printf("%e\n", Parm->ssorcost) ;
    printf ("ssormaxits .........: ") ;
    printf("%ld\n", (LONG) Parm->ssormaxits) ;
    printf ("cutfactor ..........: ") ;
    printf("%e\n", Parm->cutfactor) ;
    printf ("tolssor ............: ") ;
    printf("%e\n", Parm->tolssor) ;
    printf ("tolprox ............: ") ;
    printf("%e\n", Parm->tolprox) ;
    printf ("tolrefactor ........: ") ;
    printf("%e\n", Parm->tolrefactor) ;
    printf ("badFactorCutoff ....: ") ;
    printf("%i\n", Parm->badFactorCutoff) ;
    printf ("LP .................: ") ;
    pproj_print_TF (Parm->LP) ;
    printf ("LinGrad_tol ........: ") ;
    printf("%e\n", Parm->LinGrad_tol) ;
    printf ("LinFactor ..........: ") ;
    printf("%e\n", Parm->LinFactor) ;
}

void pproj_print_TF 
(
    int TF /* TRUE or FALSE */
)
{
    if ( TF == TRUE )
    {
        printf ("TRUE\n") ;
    }
    else
    {
        printf ("FALSE\n") ;
    }
}

/* print a packed matrix */
void pproj_printA
(
    PPINT   ncol,   /* number of cols in A */
    PPINT    *Ap,   /* size ncol+1, column pointers */
    PPINT    *Ai,   /* size Ap [ncol], row indices for A in increasing
                            order in each column */
    PPFLOAT  *Ax    /* size Ap [ncol], numerical entries of A */
)
{
    PPINT j, p, q ;
    p = 0 ;
    for (j = 1; j <= ncol; j++)
    {
        q = Ap [j] ;
        for (; p < q; p++)
        {
            printf ("%ld %ld %e\n", (LONG) Ai [p], (LONG) (j-1), Ax [p]) ;
        }
    } 
}

void pproj_printL
(
    PPINT   const ncol,   /* number of cols in A */
    PPINT   const  *Ap,   /* size ncol+1, column pointers */
    PPINT   const  *Ai,   /* size Ap [ncol], row indices for A in increasing
                        order in each column */
    PPINT   const *Anz,
    PPFLOAT const  *Ax,   /* size Ap [ncol], numerical entries of A */
    char         *what
)
{
    PPINT j, p, q ;
    printf ("A = [\n") ;
    if ( Anz != NULL )
    {
        for (j = 0; j < ncol; j++)
        {
            p = Ap [j] ;
            q = Ap [j] + Anz [j] ;
            for (; p < q; p++)
            {
                printf ("%ld %ld %25.15e\n",
                        (LONG) Ai [p]+1, (LONG) j+1, Ax [p]) ;
            }
        }
    }
    else
    {
        for (j = 0; j < ncol; j++)
        {
            p = Ap [j] ;
            q = Ap [j+1] ;
            for (; p < q; p++)
            {
                printf ("%ld %ld %25.15e\n",
                        (LONG) Ai [p]+1, (LONG) (j+1), Ax [p]) ;
            }
        }
    }
    printf ("] ;\n") ;
    printf ("%s = sparse (A (:, 1), A (:, 2), A (:, 3)) ;\n", what) ;
}

void pproj_printX
(
    PPFLOAT *x,
    PPINT    n,
    char *what
)
{
    PPINT j ;
    printf ("%s = [\n", what) ;
    for (j = 0; j < n; j++)
    {
        printf ("%25.15e\n", x [j]) ;
    }
    printf ("] ;\n") ;
}

void pproj_printi
(
    int    *i,
    PPINT   n,
    char *what
)
{
    PPINT j ;
    printf ("%s = [\n", what) ;
    for (j = 0; j < n; j++)
    {
        printf ("%i\n", i [j]) ;
    }
    printf ("] ;\n") ;
}

void pproj_printx
(
    PPFLOAT const *x,
    PPINT   const  n,
    char *what
)
{
    PPINT i ;
    printf ("%s\n", what) ;
    for (i = 0; i < n; i++)
    {
        printf ("%ld %25.15e\n", (LONG) i, x [i]) ;
    }
}

void pproj_printI
(
    PPINT const *x,
    PPINT const  n,
    char *what
)
{
    PPINT i ;
    printf ("%s\n", what) ;
    for (i = 0; i < n; i++)
    {
        printf ("%ld %ld\n", (LONG) i, (LONG) x [i]) ;
    }
}
