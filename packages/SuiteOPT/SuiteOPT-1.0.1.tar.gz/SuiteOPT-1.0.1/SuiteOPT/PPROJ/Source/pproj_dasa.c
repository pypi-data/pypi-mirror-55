/* ========================================================================= */
/* ================== pproj_dasa =========================================== */
/* ========================================================================= */
#include "pproj.h"

int pproj_dasa /* error status returned:
                      PPROJ_SOLUTION_FOUND
                      PPROJ_SSOR_NONASCENT
                      PPROJ_SSOR_MAX_ITS

                  flow control:
                      PPROJ_STATUS_OK
                      PPROJ_ALL_ROWS_DROPPED
                      PPROJ_SWITCH_TO_UPDOWN */
(
    PPcom *I
)
{
    PPINT   nrowdel, nrowadd, ncoldel, ncoladd, col, Cncol,
            colp, rowp, NextColp, NextRowp, rstart,
            toprow, botrow, seprow, topcol, botcol, botsol, nf,
            row, i, istart, j, k, l, m, p, p0, q, p2,
            Rl, MarkedForward, nup, ndrop, nd, nbrk,
           *AFTp, *AFTi, *AFTnz, *AF_nz,
           *Cp, *Cnz, *Lnz, *colmark, *ir, *ns,
           *RLinkUp, *RLinkDn, *lLinkUp, *lLinkDn, *uLinkUp, *uLinkDn,
           *lstart, *ustart, *Rstart, *Rend,
           *col_start, *col_start1, *row_start,
           *sol_start, *sol_start1, *jobcols, *jobrows, 
           *Heap, *F, *worki, *updatework,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList ;

    int     chol, status, root, blks,
            pprevblk, prevblk, topblk, botblk, jobnum, lineflag, do_rechol,
            blk, nj, new_nj, ibj, pa, qa,
           *parent, *nkids, *Kids, *leftdesc,
           *depth, *Kp, *ib, *joblist, *kidsleft ;
    const int loExists = I->Work->loExists ;
    const int hiExists = I->Work->hiExists ;

    PPFLOAT Br, tic, cj, ax, fd, fn, sd, st, st0,
            dlambda_new, s, t, u, snew, dlnew, dl_row,
            *AFTx, *x, *hi, *lo, *b, *c, *cold,
            *pA, *D, *workd, *Br_value, *changeRHS,
            *forward, *lambda, *dlambda, *lambda_tot, *shift_l, *dl ;

    cholmod_common *cmm ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;
    PPFLOAT beta [2] ;

#ifndef NDEBUG
    char *where ;
    where = "at very start of DASA" ;
    pproj_checkF (I, where) ;
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif
    Stat = I->Stat ;
    Prob = I->Prob ;
    Parm = I->Parm ;
    W = I->Work ;
    /* return_chol is set to FALSE since we are in the iterative part of
       the code. return_chol is set to TRUE when the iterations are
       complete and the factorization is updated. */
    W->return_chol = FALSE ;
    int const PrintLevel = Parm->PrintLevel ;

    /* use sparsa if the active set changed during previous usage and
       the condition for using sparsa, which was checked in the check_error
       routine, is satisfied (sparsaOK = TRUE) */
    if ( (Parm->use_sparsa == TRUE) && (W->chg_sparsa > 0)
                                    && (!Prob->nsing)
                                    && (W->sparsaOK == TRUE) )
    {
        status = pproj_sparsa (I) ;
        if ( (status == PPROJ_SOLUTION_FOUND) && (W->getfactor == FALSE) )
        {
            return (status) ;
        }
    }

    if ( PrintLevel > 2 )
    {
        printf ("sparsa max norm lambda: %e\n",pproj_max(W->lambda,Prob->nrow));
    }
#ifndef NDEBUG
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    /* determine whether to perform coordinate ascent or ssor iterations */
    pproj_iterquery (I) ;

    if ( (!Parm->cholmod && (W->chg_coor > 0)) ||
      ((Parm->use_coor_ascent == TRUE) && (W->do_coor == TRUE)
                                       && (W->chg_coor > 0)) )
    {
        pproj_coor_ascent (I) ;
    }
    if ( PrintLevel > 2 )
    {
        printf ("coor max norm lambda: %e\n", pproj_max(W->lambda, Prob->nrow));
    }
#ifndef NDEBUG
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    if ( (!Parm->cholmod && (W->chg_ssor0 > 0)) ||
     ((Parm->use_ssor0 == TRUE) && (W->do_ssor == TRUE) && (W->chg_ssor0 > 0)))
    {
        pproj_ssor0 (I) ;
    }
    if ( PrintLevel > 2 )
    {
        printf ("ssor0 max norm lambda: %e\n", pproj_max(W->lambda,Prob->nrow));
    }
#ifndef NDEBUG
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    if ( !Parm->cholmod ) /* an iterative method will use ssor1 and return */
    {
        status = pproj_ssor1 (I) ;
        return (status) ;
    }

    /* if doing update/downdate then will still use ssor1 in certain cases */
    if ( (Parm->use_ssor1 == TRUE) && (W->do_ssor == TRUE) &&
         (W->chg_ssor1 > 0) )
    {
        status = pproj_ssor1 (I) ;
        /* if an error occurred, then return */
        if ( (status == PPROJ_SSOR_NONASCENT) ||
             (status == PPROJ_SSOR_MAX_ITS) )
        {
            return (status) ;
        }
        /* if not required to factor the matrix, return in certain cases */
        if ( W->getfactor == FALSE )
        {
            if ( (status == PPROJ_SOLUTION_FOUND) ||
                 (status == PPROJ_STATUS_OK) )
            {
                return (status) ;
            }
        }
    }
    if ( PrintLevel > 2 )
    {
        printf ("max norm lambda: %e\n", pproj_max(W->lambda, Prob->nrow)) ;
    }
#ifndef NDEBUG
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    /* empty if row not modified, otherwise points into Rowmodlist
       which contains list of rows to modify*/
    RowmodFlag = W->RowmodFlag ;

    /* first part of this list contains the rows to delete
       the tail contains the rows to add */
    RowmodList = W->RowmodList ;

    /* empty if column not modified, otherwise points into Colmodlist
       which contains list of columns to modify*/
    ColmodFlag = W->ColmodFlag ;

    /* first part of this list contains the columns to delete
       the tail contains the columns to add */
    ColmodList = W->ColmodList ;

    /* If all the rows have dropped, then return to check error.
       No need to factor the matrix since it is empty. */
    PPINT   const      ncol = Prob->ncol ;
    PPINT   const      nrow = Prob->nrow ;
    PPINT   const *ineq_row = Prob->ineq_row ;

    nrowadd = W->nrowadd ;
    nrowdel = W->nrowdel ;
    ncoladd = W->ncoladd ;
    ncoldel = W->ncoldel ;
    if ( nrow == W->RLinkUp [nrow] )
    {
        if ( PrintLevel > 0 )
        {
            printf ("all rows have dropped\n") ;
        }
        W->fac = FALSE ;
        W->ncoladd = 0 ;
        W->nrowdel = 0 ;
        W->ncoldel = 0 ;
        pproj_initi (W->AFTnz, 0, nrow) ;
        pproj_initi (RowmodFlag, EMPTY, nrow) ;
        for (i = 0; i < ncoladd; i++)
        {
            ColmodFlag [ColmodList [i]] = EMPTY ;
        }
        for (i = 1; i <= ncoldel; i++)
        {
            ColmodFlag [ColmodList [ncol-i]] = EMPTY ;
        }
        pproj_initi (Prob->Anz, (PPINT) 0, ncol) ;
        return (PPROJ_ALL_ROWS_DROPPED) ;
    }

    status = PPROJ_STATUS_OK ;
    W->return_chol = TRUE ;

#ifndef NDEBUG
    I->Check->location = 2 ;                     /* code operates in dasa */
    pproj_checkA (I, 2, "after ssor1 in dasa") ; /* check that A' = AT */
fflush (stdout) ;
#endif

    /* Problem data */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPINT   const        *Anz = Prob->Anz ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPFLOAT const      *singc = Prob->singc ;
    PPINT   const          ni = Prob->ni ;
    PPINT   const       nsing = Prob->nsing ;
    PPINT   const    nsingni  = nsing + ni ;
    PPINT   const    nsingni1 = nsingni + 1 ;
    PPINT                *slo = W->slo ;
    PPINT                *shi = W->shi ;
    PPINT   const        ntot = nsingni1 + ncol ;
    PPFLOAT const         *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const         *bu = (nsing) ? Prob->singhi : Prob->bu ;
    PPFLOAT const       sigma = W->sigma ;

    /* initializations */
    beta [0] = W->Totsigma ;
    beta [1] = PPZERO ;

    /* dual variables: total multiplier = dlambda + lambda + shift_l */
    dlambda = W->dlambda ;
    lambda = W->lambda ;
    shift_l = W->shift_l ;

    if ( W->shiftl_is_zero )
    {
        lambda_tot = lambda ;
    }
    else
    {
        lambda_tot = W->lambda_tot ;
    }
    x = W->x ;
    cmm = W->cmm ;

    /* Transpose of A */
    PPINT   const *ATp = W->ATp ;
    PPINT   const *ATi = W->ATi ;
    PPFLOAT const *ATx = W->ATx ;

    /* Transpose of AF */
    AFTp = W->AFTp ;
    AFTx = W->AFTx ;
    AFTi = W->AFTi ;
    AFTnz = W->AFTnz ;

    /* ib [col] = +1 if column at upper bound
                  -1 if column at lower bound
                   0 if column is free */
    ib = W->ib ;

    /* ir [row] = 0         for an equality constraint
                = 1         for an active singleton row
                =  ineq # for an active inequality at upper bound
                = -ineq # for an active inequality at lower bound
                =  ineq # or singleton # + nsingni for a dropped constraint */
    ir = W->ir ;
    b = W->b ; /* the part of grad L (lambda) associated with bound variables */
    c = W->c ; /* y + A'lambda */
    cold = W->cold ; /* initial y + A'lambda */
    F = W->F ; /* free indices */
    D = W->D ; /* diag of AF*AF' */
    ns = W->ns ; /* used in line search, points from index to break point # */
    lo = W->lo ; /* lower bounds on x */
    hi = W->hi ; /* upper bounds on x */
    /* entries in changeRHS are all zero except for the entries that change */
    changeRHS = W->changeRHS ;

    /* pointers into Ai or Ax of columns to add or delete */
    Cp = W->Cp ;
    Cnz = W->Cnz ;

    /* Links for active inequalities. lLinkUp points to the strict
       inequalities with b_i = bl_i while uLinkUp points to the strict
       inequalities with b_i = bu_i. Since only one of these can hold for
       each i, lLinkUp and uLinkUp can be stored in the same array */
    lLinkUp = W->SLinkUp ;
    lLinkDn = W->SLinkDn ;
    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;

    /* Links for the active rows */
    RLinkUp = W->RLinkUp ;
    RLinkDn = W->RLinkDn ;

    /* Multilevel information */
    blks = W->blks ;     /* number of nodes (blocks) in the multilevel tree */
    root = blks - 1 ;    /* the root node is labeled blks - 1. */
    parent = W->parent ; /* parent [k] is the parent of node k */
    nkids = W->nkids ;   /* nkids [k] is the number of children of node k */
    Kids = W->Kids ;     /* list of children */
    Kp = W->Kp ;         /* Kp [k] points to the first child of node k */
    leftdesc = W->leftdesc ; /* in the multilevel tree, leftdesc [k] is the node
                            beneath k in the tree that is left most descendant*/
    row_start = W->row_start ;   /* first row associated with each block */
    col_start = W->col_start ;   /* first column associated with each block */
    sol_start = W->sol_start ;   /* index 1st singleton associated with block */
    depth = W->depth ;           /* depth of each node in tree, used for stats*/
    col_start1 = col_start+1 ;
    sol_start1 = sol_start+1 ;

    /* Arrays joblist and kidsleft are used in the multilevel implementation.
       joblist contain the blocks that are solved to generate the current
       search direction. For each block in the list, we treat all the
       variables as being fixed except for the variables associated with
       the block. The variables in the blocks, with the variables
       outside these blocks fixed, are completely uncoupled in the
       dual problem, so we can perform a DASA step by solving for these
       variables in an uncoupled fashion. We start at the leaves of the
       tree and work up to the root. Once all the children of a node
       are optimized, we move up to the parent. */
    joblist = W->joblist ;

    /* For each node in the multilevel tree, we keep a list of the number
       of children that have not yet been optimized over. When all the
       children of a node have been optimized over (that is, the
       variables associated with the blocks that are children of the
       node), then we move up to the node itself and start to optimize
       over the associated variables. We cannot move up to the parent of
       a node until kidsleft for this node reaches 0. */
    kidsleft = W->kidsleft ;

    /* jobcols is the number of columns associated with this each block
       that have been added while jobrows is the number of rows in this
       block that have been deleted. */
    jobcols = W->jobcols ;
    jobrows = W->jobrows ;

    /* Rstart and Rend contain the first and last active row of each block. */
    Rstart = W->Rstart ;
    Rend = W->Rend ;

    /* pointers to the starting column in each block of the multilevel
       decomposition. lstart is associated with the equations at lower
       bounds and ustart is associated with the equations at upper bound */
    lstart = W->lstart ;
    ustart = W->ustart ;

    /* phase1, coor_ascent, ssor0, ssor1, modcol, and modrow all get their
       allocated space from W->arrayi and and W->arrayd, the same as the
       DASA algorithm.  The workspace for all these routines can overwrite
       each other.  At the end of pproj_init, we make sure that
       there is enough space allocated for all these routines.
       The DASA variables are listed below.

    -> work arrays for multilevel solves and line search:

       forward    - double nrow, forward solve
       dl         - double nrow, search direction
       pA         - double ncol, A'lambda
       Br_value   - double ntot, break points for line search
       Heap       - int ntot, line search heap

    -> work array after line search for update/downdate:

       colmark    - int ncol, bottom row of block associated with added columns
       updatework - int nrow, needed by modrow */
       
    /* |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| */
    /* assign work variables to double (workd) and int (worki) work space */

    /* for multilevel solves and line search */
    workd = W->arrayd ;
    forward  = workd ; workd += nrow ;
    dl       = workd ; workd += nrow ;
    pA       = workd ; workd += ncol ; /* W in modrow_prep used here */
    Br_value = workd ; workd += ntot ;

#ifndef NDEBUG
pproj_initx (forward, PPZERO, nrow) ;
#endif

    worki = W->arrayi ;
    Heap     = worki ; worki += ntot ;

    /* update/downdate after line search */
    worki = W->arrayi ;
    colmark    = worki ; worki += ncol ;
    updatework = worki ; worki += nrow ;
 
    /* end of assignments to workspace */
    /* |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| */

    botblk = 0 ;
    st = PPZERO ;
    W->npup_cur = 0 ; /* number of partial updates */
    W->npup_old = 0 ;
    nf = W->nf ;

    /* Evaluate the first (Rstart) and last (Rend) active row in
       each active block. For the dead blocks, with all rows inactive,
       Rstart is empty */
    row = nrow ;
    Rl = nrow ;
    pprevblk = blks ;
    prevblk = 0 ;
    blk = 0 ;
    while ( (row = RLinkUp [row]) < nrow ) /* the active rows */
    {
        if ( !W->shiftl_is_zero )
        {
            lambda_tot [row] = lambda [row] + shift_l [row] ;
        }
        /* else lambda_tot = lambda */
        while ( row >= row_start [blk] )
        {
            Rstart [blk++] = EMPTY ; /* Rstart = EMPTY for inactive blocks */
        }
        if ( blk > prevblk )
        {
            Rend [pprevblk] = Rl ;
            pprevblk = blk - 1 ;
            Rstart [pprevblk] = row ;
            prevblk = blk ;
        }
        Rl = row ;
    }
    Rend [pprevblk] = Rl ;
    while ( blk < blks )
    {
        Rstart [blk++] = EMPTY ;
    }

    /* The change of variables described in pproj.  It is assumed
       that the part of the change of variables associated with the
       bound variables has already been performed. Hence, only the
       part associated with the free variables is done here.
       The current estimate of x is always x + the minimizer of the
       dual function. cold is used in the linear systems while c is
       used in the computation of the directional derivative of the
       dual function. c is updated by A'*dlambda */
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] ) /* variable at bound */
        {
            cold [j] = c [j] ;
        }
        else          /* variable is free */
        {
            PPFLOAT const tc = c [j] ;
            c [j] = PPZERO ;
            if ( loExists ) lo [j] -= tc ;
            if ( hiExists ) hi [j] -= tc ;
            x [j] += tc ;
            cold [j] = PPZERO ;
            if ( tc )
            {
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    b [Ai [p]] -= Ax [p]*tc ;
                }
            }
        }
    }
#ifndef NDEBUG
    where = "at start of DASA" ;
    pproj_checkc (I, where);
    pproj_checkb (I, where) ;
    pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
    pproj_check_const (dlambda, PPZERO, NULL, 0, nrow, where) ;
#endif

   /* Factor or update the matrix.
      If the matrix is factored, compare update to factorization.
      W->fac = TRUE (matrix has been factored), = FALSE (matrix not factored)*/
    if ( W->fac == TRUE )
    {

        /* ------------------------------------------------------------------ */
        /* The matrix has already been factorized.
           We now check to see if we want to update/downdate/rowadd/rowdel it,
           OR factorize it from scratch. */
        /* ------------------------------------------------------------------ */
        chol = pproj_cholquery (I) ; /* TRUE => do chol, FALSE means update*/
    }
    else
    {
        /* ------------------------------------------------------------------ */
        /* The matrix has never been factorized.
           Get ready to factorize it for the very first time. */
        /* ------------------------------------------------------------------ */
        W->fac = TRUE ;
        chol = TRUE ; /* do a chol, not an update */
    }

    if ( PrintLevel > 0 )
    {
        if ( chol )
        {
            printf ("Factor the matrix ") ;
        }
        else
        {
            printf ("Update the matrix ") ;
        }
       
        printf (" (colup: %ld coldn: %ld rowup: %ld rowdn: %ld nf: %ld)\n",
            (LONG) ncoladd, (LONG) ncoldel, (LONG) nrowadd, (LONG) nrowdel,
            (LONG) nf) ;
    }

    if ( chol )
    {
        /* matrix recholed, also sets AFTnz to zero for dead rows */
        Stat->nchols++ ;
        pproj_updateAnz (I, 1) ;
    }
    else
    {

        /* ------------------------------------------------------------------ */
        /* update the matrix */
        /* ------------------------------------------------------------------ */

        /*
           1. Delete inactive rows
           2. Add active rows
           3. Delete bound columns
           4. Resymbol
           5. Add free columns
        */
#ifndef NDEBUG
        pproj_check_diag (I, chol,
                          "before call of modrow delete at start of DASA") ;
#endif
        if ( nrowdel > 0 )
        {
            pproj_modrow (I, 0, TRUE, FALSE, -1, NULL, NULL, dl, NULL) ;
        }
#ifndef NDEBUG
        pproj_check_diag (I, chol,
                          "after call of modrow delete at start of DASA") ;
#endif
        pproj_updateAnz (I, 0) ;
        if ( nrowadd > 0 )
        {
            pproj_modrow (I, 0, TRUE, FALSE, +1, NULL, NULL, dl, NULL) ;
        }
#ifndef NDEBUG
        pproj_check_diag (I, chol,
                          "after call of modrow add at start of DASA");
#endif

        l = 0 ;
        for (k = 1; k <= ncoldel; k++)
        {
            j = ColmodList [ncol-k] ;
            if ( Anz [j] > 0 )
            {
                Cp [l] = Ap [j] ;
                Cnz [l] = Anz [j] ;
                l++ ;
            }
            else /* update the list of deletion columns by removing j */
            {
                col = ColmodList [ncol-ncoldel] ;   /* last col in list*/
                ColmodList [ncol-k] = col ;         /* replace j by col*/
                ColmodFlag [col] = ncol - k ;       /* new location for col */
                ncoldel-- ;                         /* one less update */
                W->ncoldel = ncoldel ;              /* store it in W */
                k-- ;                               /* adjust k */
                ColmodFlag [j] = EMPTY ;            /* col j is done */
            }
        }
        pproj_modcol (I, 0, 0, -1, colmark, Cp, Cnz, NULL, NULL, l) ;
#ifndef NDEBUG
        where = "after modcol at start of DASA" ;
        pproj_check_diag (I, chol, where);
        pproj_checkF (I, where) ;
#endif

        /* Resymbol to exploit the zeros created by deleting columns */
        CHOLMOD (resymbol) (W->A, F, nf, FALSE, W->L, cmm) ;
#ifndef NDEBUG
        pproj_check_diag (I, chol, "after resymbol at start of DASA") ;
#endif
        l = 0 ;
        for (k = 0; k < ncoladd; k++)
        {
            j = ColmodList [k] ;
            if ( Anz [j] > 0 )
            {
                Cp [l] = Ap [j] ;
                Cnz [l] = Anz [j] ;
                l++ ;
            }
            else /* update the list of addition columns by removing j */
            {
                ncoladd-- ;                         /* one less update */
                col = ColmodList [ncoladd] ;        /* last col in list*/
                ColmodList [k] = col ;              /* replace j by col*/
                ColmodFlag [col] = k ;              /* new location for col */
                W->ncoladd = ncoladd ;              /* store it in W */
                k-- ;                               /* adjust k */
                ColmodFlag [j] = EMPTY ;            /* col j is done */
            }
        }
        pproj_modcol (I, 0, 0, +1, colmark, Cp, Cnz, NULL, NULL, l) ;
    }

#ifndef NDEBUG
    where = "at top of DASA after initial updates" ;
    pproj_checkA (I, 0, where) ;
    pproj_check_AT (I, where) ;
    pproj_checkF (I, where) ;
    pproj_check_AFT (I, TRUE, where) ;
    pproj_check_link (I, (int *) NULL, 0, where) ;
    if ( chol )
    {
        for (i = 0; i < nrow; i++)
        {
            if ( (ir [i] > nsingni) && (AFTnz [i] != 0) )
            {
                printf ("row %ld ir = %ld > nsingni = %ld but AFTnz = %ld "
                        "!= 0\n", (LONG) i, (LONG) ir [i], (LONG) nsingni,
                         (LONG) AFTnz [i]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }
#endif


    /* ---------------------------------------------------------------------- */
    /* Setup the initial job queue containing the leaves */
    /* ---------------------------------------------------------------------- */

    /*
        row_start [blk] = first row    in block blk       (blks+1 elements)
        col_start [blk] = first column in block blk       (blks+1 elements)
        Lstart [blk]    = 1st lower bound column in block blk (blks+1 elements)
        LLinkUp [j]     = next lower bound column
        LLinkDn [j]     = previous lower bound column
    */

    for (blk = 0; blk < blks; blk++)
    {
        kidsleft [blk] = nkids [blk] ;
    }

    AF_nz = NULL ;        /* [ */
    if (chol && blks > 1) /* doing factorization with more than 1 block */
    {
        /* AF_nz [j] will be the number of active rows in the leaves of
         * column j of AF, where j is in the range 0 to ncol-1 */
        AF_nz = CHOLMOD (calloc) (ncol, sizeof (PPINT), cmm) ;
    }

    nj = 0 ;
    for (blk = 0; blk < blks; blk++)
    {
        if ( kidsleft [blk] == 0 )
        {
            /* blk is now a leaf */
            if ( Rstart [blk] == EMPTY )
            {
                if (W->L != NULL)
                {
                    Lnz = W->L->nz ;
                    /* all rows in blk inactive */
                    /* zero out Lnz since the block will be skipped */
                    q = row_start [blk+1] ;
                    for (i = row_start [blk]; i < q; i++)
                    {
                        Lnz [i] = 1 ;        /* only diagonal left */
                    }
                }

                pa = parent [blk] ;
                kidsleft [pa]-- ;
            }
            else
            {
                joblist [nj++] = blk ;

                if ( chol && blks > 1)
                {

                    /* multilevel chol of the leaf node blk */
                    /* Aleaf = copy of AF but containing just the leaves */

                    botrow = row_start [blk+1] ;
                    i = Rstart [blk] ;
                    for (; i < botrow ; i = RLinkUp [i])
                    {
                        /* Aleaf (i,:) = AFT(:,i) where AFT is in column form,
                         * will be done below.  Just compute the column counts
                         * of Aleaf only */
                        p = AFTp [i] ;
                        q = p + AFTnz [i] ;
                        for ( ; p < q ; p++)
                        {
                            AF_nz [AFTi [p]]++ ;
                        }
                    }
                }
            }
        }
    }

    if ( chol )
    {
        /* factor the matrix AF*AF' + beta*I, either all of it or just the
         * leaves of the separator tree (with dead blocks removed). */
        cholmod_sparse *Aleaf = NULL ;

        if (blks != 1)
        {
            PPFLOAT *Aleafx ;
            PPINT *Aleaf_nz, *Finv, *Aleafp2, *Aleafi ;
            PPINT *Aleafp ;
            PPINT nz, jnz ;

            /* build the Aleaf matrix.  Aleaf consists of all active rows in
             * the leaves to be factorized.  */
            Finv = CHOLMOD (malloc) (ncol, sizeof (PPINT), cmm) ;        /* [ */
            Aleaf_nz = CHOLMOD (malloc) (nf, sizeof (PPINT), cmm) ;      /* [ */
            nz = 0 ;
            for (k = 0 ; k < nf ; k++)
            {
                j = F [k] ;
                Finv [j] = k ;
                jnz = AF_nz [j] ;
                Aleaf_nz [k] = jnz ;
                nz += jnz ;
            }

            /* allocate Aleaf */
            Aleaf = CHOLMOD (allocate_sparse) (nrow, nf, nz, TRUE, TRUE, 0,
                    CHOLMOD_REAL, cmm) ;
            Aleafp = Aleaf->p ;
            Aleafi = Aleaf->i ;
            Aleafx = Aleaf->x ;

            nz = 0 ;
            for (k = 0 ; k < nf ; k++)
            {
                Aleafp [k] = nz ;
                nz += Aleaf_nz [k] ;
            }
            Aleafp [nf] = nz ;

            Aleafp2 = Aleaf_nz ;        /* [ use Aleaf_nz as workspace */
            for (k = 0 ; k < nf ; k++)
            {
                Aleafp2 [k] = Aleafp [k] ;
            }

            /* Aleaf = transpose of AFT, active leaf rows only  */
            for (jobnum = 0 ; jobnum < nj ; jobnum++)
            {
                blk = joblist [jobnum] ;

                /* multilevel chol of the leaf node blk */
                botrow = row_start [blk+1] ;
                i = Rstart [blk] ;
                for (; i < botrow ; i = RLinkUp [i])
                {
                    p = AFTp [i] ;
                    q = p + AFTnz [i] ;
                    for ( ; p < q ; p++)
                    {
                        /* Aleaf (i, Finv(j)) = AFT (j,i) */
                        j = AFTi [p] ;
                        k = Finv [j] ;
                        p2 = Aleafp2 [k]++ ;
                        Aleafi [p2] = i ;
                        Aleafx [p2] = AFTx [p] ;
                    }
                }
            }

            CHOLMOD (free) (nf, sizeof (PPINT), Aleaf_nz, cmm) ; /* ] ] */
            CHOLMOD (free) (ncol, sizeof (PPINT), Finv, cmm) ;   /* ] */
        }

        cmm->nmethods = 1 ;
        cmm->method [0].ordering = CHOLMOD_NATURAL ;
        cmm->postorder = FALSE ;

        CHOLMOD (free_factor) (&(W->L), cmm) ;

        tic = pproj_timer () ;

        if (blks == 1)
        {
            W->L = pproj_rechol (W->A, W->AFT, F, nf, beta, RLinkUp, W, cmm) ;

#ifndef NDEBUG
            pproj_check_diag (I, chol,
                              "after initial factorization in DASA") ;
#endif
        }
        else
        {

            W->L = pproj_rechol (Aleaf, NULL, NULL, 0, beta, RLinkUp, W, cmm) ;

            CHOLMOD (free_sparse) (&Aleaf, cmm) ;
            CHOLMOD (free) (ncol, sizeof (PPINT), AF_nz, cmm) ; /* ] */
        }

        I->Stat->chol += pproj_timer () - tic ;
    }

    /* MarkedForward solves are only used in the case of a multilevel
       implementation (blks > 1) where the matrix is updated. In this case,
       L stores a factorization of the entire matrix, and we are partially
       updating the factorization and the forward solve (up to botrow).
       The bottom row of the block associated with an added column is stored
       in the array colmark.  When we chol the matrix in a multilevel
       implementation, we update the forward solve over the entire existing
       L so there is no need to mark where the forward solves end. */
    if ( blks == 1 ) MarkedForward = FALSE ;
    else             MarkedForward = !chol ;

    /* Initial forward solve over each block */
    tic = pproj_timer () ;        /* [ */
    if ( MarkedForward )
    {
        if ( PrintLevel > 1 ) printf ("MarkedForward\n") ;
        row = RLinkUp [nrow] ;
        for (jobnum = 0; jobnum < nj; jobnum++)
        {
            botblk = joblist [jobnum] ;
            botrow = row_start [botblk+1] ;
            topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
            toprow = row_start [topblk] ;

#ifndef NDEBUG
            if ( PrintLevel > 1 )
            {
                printf ("\nforward solve, jobnum: %i botblk: %i"
                        " topblk: %i toprow: %ld botrow: %ld\n",
                        jobnum, botblk, topblk, (LONG) toprow, (LONG) botrow) ;
            }
#endif

            /* For a marked forward solve, we also zero out
               all the element of forward associated with active rows
               that are outside the blocks being optimized over in
               this iteration. We need to zero out these elements for
               the subsequent updates. Note that row = RLinkUp [nrow]
               initially, and hence, it iterates over all the active rows. */
            rstart = Rstart [botblk] ;
            for (; row < rstart; row = RLinkUp [row])
            {
                forward [row] = PPZERO ;
            }

            /* The rows from Rstart [botblk] to botrow are set to b [row] */
            for (; row < botrow; row = RLinkUp [row])
            {
                forward [row] = b [row] ;
            }

            pproj_lsolve (W, forward, RLinkUp, Rstart [botblk],
                           botrow, MarkedForward) ;
        }
        for (; row < nrow; row = RLinkUp [row])
        {
            forward [row] = PPZERO ;
        }
    }
    else /* else not MarkedForward */
    {
        if ( PrintLevel > 1 ) printf ("Not MarkedForward\n") ;
        for (jobnum = 0; jobnum < nj; jobnum++)
        {
            botblk = joblist [jobnum] ;
            botrow = row_start [botblk+1] ;
            topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
            toprow = row_start [topblk] ;

            if (PrintLevel > 1 )
            {
                printf ("forward solve, jobnum: %i botblk: %i"
                        " topblk: %i toprow: %ld botrow: %ld\n",
                         jobnum, botblk, topblk, (LONG) toprow, (LONG) botrow) ;
            }

            for (row = Rstart [botblk]; row < botrow; row = RLinkUp [row])
            {
                forward [row] = b [row] ;
            }

            pproj_lsolve (W, forward, RLinkUp, Rstart [botblk], botrow,
                    MarkedForward) ;
        }
    }
    Stat->lsolve += pproj_timer () - tic ;

    /* ---------------------------------------------------------------------- */
    /* PPwork from leaves to root, until no change in free set */
    /* ---------------------------------------------------------------------- */

#ifndef NDEBUG
    where = "after initial forward solve in DASA" ;
    pproj_check_link (I, joblist, nj, where) ;
    pproj_checkA (I, 0, where) ;
    pproj_check_AT (I, where) ;
    pproj_check_forward (I, forward, b, joblist, nj, where) ;
#endif

    while ( nj > 0 )
    {
        nrowdel = 0 ;
        ncoladd = 0 ;

        for (jobnum = 0; jobnum < nj; jobnum++)
        {
            botblk = joblist [jobnum] ;
            botrow = row_start [botblk+1] ;

            topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
            toprow = row_start [topblk] ;
            seprow = row_start [botblk] ;

            topcol = col_start [topblk] ;
            botcol = col_start1[botblk] ;
            botsol = sol_start1[botblk] ; /*singular column */

            Stat->solves [depth [botblk]]++ ;

            if ( PrintLevel > 1 )
            {
                printf ("jobnum: %i botblk: %i topblk: %i toprow: %ld"
                    " botrow: %ld seprow: %ld topcol: %ld botcol: %ld\n",
                    jobnum, botblk, topblk, (LONG) toprow,
                    (LONG) botrow, (LONG) seprow, (LONG) topcol, (LONG) botcol);
                fflush (stdout) ;
            }
#ifndef NDEBUG
            pproj_check_diag3 (I, toprow, botrow, chol) ;
            pproj_check_link (I, joblist, nj, "before start of job in DASA");
#endif


            /* momentarily set the initial RLinkDn to -1, this simplifies
               indexing in dltsolve */
            k = RLinkUp [nrow] ;
            RLinkDn [k] = -1 ;
            tic = pproj_timer () ;/* time the back solve */
            pproj_dltsolve (W, dl, forward, RLinkDn,
                             toprow, Rend [botblk], MarkedForward, botrow) ;
            Stat->dltsolve += pproj_timer () - tic ;
            RLinkDn [k] = nrow ; /* restore RLinkDn */

#ifndef NDEBUG
            where = "before line search" ;
            pproj_check_back (I, forward, dl, botblk, where) ;
            pproj_check_eqn5 (I, botblk, dl, forward, b, where) ;
#endif
            /* start of line search */
            tic = pproj_timer () ;

            /* zero out pA [topcol:botcol-1] */
            pproj_initx (pA+topcol, PPZERO, botcol - topcol) ;
            sd = fd = PPZERO ;

            /* multiply dl [toprow:botrow] by A [toprow:botrow, :] */

            for (row = Rstart [botblk]; row < botrow; row = RLinkUp [row])
            {
                PPFLOAT dlambda_row = dlambda [row] ;
                u = dl [row] ;
                t = u - dlambda_row ; /* maximizer - current lambda */
                sd += t*t ;
                dl [row] = t ;
                fd += (b [row] - sigma*dlambda_row)*t ;
                q = ATp [row+1] ;
                p = ATp [row] ;
                for (; p < q; p++)
                {
                    pA [ATi [p]] += t*ATx [p] ;
                }
            }

            sd = sigma*sd ;
            st = PPONE ;
            nbrk = 0 ;

            for (j = topcol; j < botcol; j++)
            {
                ibj = ib [j] ;
                if ( ibj == 0 )
                {
                    t = pA [j] ;
                    sd += t*t ;
                    fd -= c [j]*t ;
                }
                else if ( ibj < 0 ) /* check for lower bound becoming free */
                {
                    if ( pA [j] > PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < PPONE )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;
                        }
                    }
                }
                else                /* check for upper bound becoming free */
                {
                    if ( pA [j] < PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < PPONE )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;
                        }
                    }
                }
            }

#ifndef NDEBUG
            if ( fd < PPZERO )
            {
                t = PPZERO ;
                for (row = Rstart [botblk]; row < botrow;
                     row = RLinkUp [row])
                {
                    t = PPMAX (t, fabs (dl [row])) ;
                    t = PPMAX (t, fabs (dlambda [row])) ;
                    t = PPMAX (t, fabs (b [row])) ;
                }
                if ( fd < -t*1.e-10 )
                {
                    printf ("bad search direction, fd = %e sd: %e\n",
                             fd, sd) ;
                    printf ("(fd should be -sd)\n") ;
                    /* to stop at bad search direction, uncomment next line */
                    /*  pproj_error (-1, __FILE__, __LINE__, "stop") ;*/
                }
            }
#endif

            if ( fd > PPZERO )
            {
                /* factor error can yield a bad step, could take a step
                   of length st1 = MIN (fd/sd, 1.), however, would need to
                   pass over the Br_value computed above and remove any
                   which exceed st1 */

                for (j = lstart [botblk]; j < botsol; j = lLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) < PPZERO )
                    {
                        if ( ni ) s = -(dlambda [row] + lambda_tot [row])/t ;
                        else      s = (singc[j]-dlambda[row]-lambda_tot[row])/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = PPMAX (PPZERO, s) ;
                            nbrk++ ;
                            Heap [nbrk] = k ;
                        }
                    }
                }

                for (j = ustart [botblk]; j < botsol; j = uLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) > PPZERO )
                    {
                        if ( ni ) s = -(dlambda [row] + lambda_tot [row])/t ;
                        else      s = (singc[j]-dlambda[row]-lambda_tot[row])/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = PPMAX (PPZERO, s) ;
                            nbrk++ ;
                            Heap [nbrk] = k ;  /* add to heap */
                        }
                    }
                }
            }
            else /* step was poor, don't move */
            {
                st = 0 ;
                nbrk = 0 ;
            }

#ifndef NDEBUG
            pproj_checkc (I, "before line search in DASA") ;
#endif
            if ( PrintLevel > 1 )
            {
                printf("nbrk: %ld st: %e\n", (LONG) nbrk, st) ;
                fflush (stdout) ;
            }

            /* ============================================================== */
            /* sort break points, do a line search */
            /* ============================================================== */

            lineflag = 0 ;
            if ( nbrk > 0 )
            {
                st0 = st ; /* st0 = 1 */
                pproj_minheap_build (Heap, Br_value, nbrk) ;
                for (k = 1; k <= nbrk; k++)
                {
                    ns [Heap [k]] = k ;
                }

#ifndef NDEBUG
                pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot, "in DASA");
#endif

                st = PPZERO ;
                while ( nbrk > 0 )
                {
                    if ( sd > PPZERO )
                    {
                        col = Heap [1] ;
                        Br_value [col] = Br = PPMAX (PPZERO, Br_value [col]) ;
                        /* If current break point is beyond the stepsize st0
                           for which we extracted break points, then terminate,
                           either at the global minimum in the search direction,
                           or at st0. */
                        if ( Br >= st0 )
                        {
                            Br = st + fd/sd ;
                            if ( Br < st0 )
                            {
                                st = Br ; 
                            }
                            else
                            {
                                st = st0 ;
                                /* lineflag = -2 means that in the debugger,
                                    we should only check that slope >= 0 */
                                lineflag = -2 ;
                            }
                            fd = PPZERO ;
                            break ;
                        }

                        /* nbrk decreased by 1 inside minheap_delete */
                        pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1) ;
                        fn = fd - sd*(Br - st) ;

#ifndef NDEBUG
                        pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                "at initial Heap delete") ;
                        if ( PrintLevel > 1 )
                        {
                            printf("    brk: %ld col: %ld fn: %9.3e fd: %9.3e"
                                   " sd: %9.3e st: %9.3e Br_value: %9.3e\n",
                                  (LONG) nbrk, (LONG) col, fn, fd, sd, st, Br) ;
                            fflush (stdout) ;
                        }
#endif

                        if ( fn <= 0 )
                        {
                            if ( fd != fn )
                            {
                                st += (fd/(fd-fn))*(Br - st);
                            }
                            fd = 0 ;
                            break ;
                        }
                        else
                        {
                            fd = fn ;
                        }
                    }
                    else /* sd <= 0, only happens if all rows drop */
                    {

#ifndef NDEBUG
                        if ( PrintLevel > 2 )
                        {
                            printf("    break from line search due to sd "
                                   "(%e) <= 0\n", sd) ;
                            fflush (stdout) ;
                        }
#endif
                        lineflag = 2 ;
                        break ;
                    }

                    st = Br ;

                    if ( col < ncol ) /* free column */
                    {
                        F [nf++] = col ;
                        s = pA [col] ;
                        sd += s*s ;
                        ib [col] = 0 ;
                        ColmodList [ncoladd] = col ; /* use 1st part for add */
                        ASSERT (ColmodFlag [col] == EMPTY) ;
                        ColmodFlag [col] = ncoladd ;
                        ncoladd++ ;
                    }
                    else            /* drop row */
                    {
                        PPINT const sing = col - ncol ;
                        row = ineq_row [sing] ;

#ifndef NDEBUG
                        if ( PrintLevel > 1 )
                        {
                            printf("     drop row: %ld ir: %ld\n",
                                   (LONG) row, (LONG) ir [row]);
                            fflush (stdout) ;
                        }
                        if ( ir [row] > nsingni )
                        {
                            printf ("row: %ld ir: %ld was already deleted\n",
                                    (LONG) row, (LONG) ir [row]) ;
                            pproj_error (-1, __FILE__, __LINE__, "stop") ;
                        }
#endif

                        ir [row] = sing + nsingni ;    /* Drop row */
                        RowmodList [nrowdel] = row ;
                        ASSERT (RowmodFlag [row] == EMPTY) ;
                        RowmodFlag [row] = nrowdel ;
                        nrowdel++ ;
                        i = RLinkDn [row] ;
                        k = RLinkUp [row] ;
                        RLinkUp [i] = k ;
                        RLinkDn [k] = i ;
                        if ( Rstart [botblk] == row )
                        {
                            Rstart [botblk] = k ;
                            if ( Rend [botblk] == row ) Rend [botblk] = k ;
                        }
                        else if ( Rend [botblk] == row )
                        {
                            Rend [botblk] = i ;
                        }

                        dl_row = dl [row] ;
                        dlnew = st*dl_row ;
                        dlambda_new = dlambda [row] + dlnew ;
                        /* dl [row] used in row delete for update*/
                        dl [row] = -dlambda_new ;
                        dlambda [row] = PPZERO ;
                        if ( ni )
                        {
                            lambda [row] = -shift_l [row] ;
                        }
                        else /* nsing */
                        {
                            lambda [row] = singc [sing] - shift_l [row] ;
                        }
                        b [row] -= sigma*dlambda_new ;
                        fd -= dl_row*b [row] ;
                        sd -= sigma*dl_row*dl_row ;

                        if ( dl_row > PPZERO )
                        {
                            /* drop upper bound on col */
                            b [row] -= bu [sing] ;
                            m = uLinkUp [sing] ;
                            l = uLinkDn [sing] ;
                            uLinkUp [l] = m ;
                            uLinkDn [m] = l ;
                            if ( sing == ustart [botblk] )
                            {
                                ustart [botblk] = m ;
                            }
                            if ( nsing )
                            {
                                shi [row] = 0 ;
                                PPINT const sloj = slo [row] ;
                                if ( sloj )
                                {
                                    m = lLinkUp [sloj] ;
                                    l = lLinkDn [sloj] ;
                                    lLinkUp [l] = m ;
                                    lLinkDn [m] = l ;
                                    slo [row] = 0 ;
                                    if ( sloj == lstart [botblk] )
                                    {   
                                        lstart [botblk] = m ;
                                    }
                                }
                            }
                        }
                        else
                        {
                            /* drop lower bound on col */
                            b [row] -= bl [sing] ;
                            m = lLinkUp [sing] ;
                            l = lLinkDn [sing] ;
                            lLinkUp [l] = m ;
                            lLinkDn [m] = l ;
                            if ( sing == lstart [botblk] )
                            {
                                lstart [botblk] = m ;
                            }
                            if ( nsing )
                            {
                                slo [row] = 0 ;
                                PPINT const shij = shi [row] ;
                                if ( shij )
                                {
                                    m = uLinkUp [shij] ;
                                    l = uLinkDn [shij] ;
                                    uLinkUp [l] = m ;
                                    uLinkDn [m] = l ;
                                    shi [row] = 0 ;
                                    if ( shij == ustart [botblk] )
                                    {
                                        ustart [botblk] = m ;
                                    }
                                }
                            }
                        }

                        /* since a component of lambda is now kept fixed,
                           it is moved to the right side of the equation
                           which is equivalent to a change in cold */
                        q = ATp [row+1] ;
                        for (p = ATp [row]; p < q; p++)
                        {
                            j = ATi [p] ;
                            ax = ATx [p] ;
                            cold [j] += ax*dlambda_new ;

                            /* cj after taking the step */
                            s = pA [j] ;
                            cj = c [j] + st*s ;
                            /* modify c to account for later update, with
                               these changes to pA and c, the subsequent
                               update c [j] += st*pA [j] works */
                            c [j] += dlnew*ax ;
                            t = dl_row*ax ;
                            snew = pA [j] = s - t ;
                            /* if ( fabs (snew) < 1.e-4*fabs (s) )
                            {
                                lineflag = 2 ;
                            } */

                            /* update c, pA, sd, fd */
                            if ( !ib [j] )
                            {
                                fd += cj*t ;
                                sd -= t*(s + snew) ;
                            }
                            else
                            {
                                if ( ib [j] < 0 )
                                {
                                    if ( snew > PPZERO )
                                    {
                                        t = Br_value [j] = st - cj/snew ;
                                        if ( ns [j] != EMPTY )
                                        {
                                            if ( t <= st0 )
                                            {
                                                pproj_minheap_update (Heap,
                                                   ns, Br_value, nbrk, ns [j]) ;
                                            }
                                            else
                                            {
                                                pproj_minheap_delete (Heap,
                                                   ns, Br_value, &nbrk, ns [j]);
                                            }
                                        }
                                        else
                                        {
                                           if ( t <= st0 )
                                           {
                                               pproj_minheap_add (j, Heap,
                                                   ns, Br_value, &nbrk) ;
                                           }
                                        }
                                    }
                                    else
                                    {
                                        if ( ns [j] != EMPTY )
                                        {
                                            pproj_minheap_delete (Heap,
                                               ns, Br_value, &nbrk, ns [j]);
                                        }
                                    }
                                }
                                else
                                {
                                    if ( snew < PPZERO )
                                    {
                                        t = Br_value [j] = st - cj/snew ;
                                        if ( ns [j] != EMPTY )
                                        {
                                            if ( t <= st0 )
                                            {
                                                pproj_minheap_update (Heap,
                                                   ns, Br_value, nbrk, ns [j]) ;
                                            }
                                            else
                                            {
                                                pproj_minheap_delete (Heap,
                                                   ns, Br_value, &nbrk, ns [j]);
                                            }
                                        }
                                        else
                                        {
                                            if ( t <= st0 )
                                            {
                                                pproj_minheap_add (j, Heap,
                                                    ns, Br_value, &nbrk) ;
                                            }
                                        }
                                    }
                                    else
                                    {
                                        if ( ns [j] != EMPTY )
                                        {
                                            pproj_minheap_delete (Heap,
                                               ns, Br_value, &nbrk, ns [j]);
                                        }
                                    }
                                }
                            }
                        }
                    }

                    /* fd <= 0 only happens if a row drops and the current
                       step is optimal. The optimum occurred at a point
                       where the dual function was not differentiable */
                    if ( fd <= PPZERO )
                    {

                        if ( PrintLevel > 1 )
                        {
                            printf("    premature break from line search\n") ;
                            fflush (stdout) ;
                        }

                        lineflag = 1 ;
                        fd = PPZERO ;
                        break ;
                    }
                    if ( PrintLevel > 1 )
                    {
                        if ( col < ncol )
                        {
                            printf ("    free: %ld blk: %i nbrk: %ld\n",
                                    (LONG) col, botblk, (LONG) nbrk);
                        }
                        else
                        {
                            printf ("    drop row: %ld, nbrk: %ld\n",
                                    (LONG) row, (LONG) nbrk) ;
                        }
                        fflush (stdout) ;
                    }

#ifndef NDEBUG
                    pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                        "in line search") ;
                    pproj_check_link (I, joblist, nj, "inside line") ;
#endif
                }

                /* lineflag = 2 if sd <= 0
                   lineflag = 1 if line search terminates at nondiff point */
                   
                if ( (sd > PPZERO) && (!lineflag) )
                {
                    st += fd/sd ; /* fd != 0 only if no break points */
                }
                if ( st > st0 ) /* st0 = 1 */
                {
                    st = st0 ;
                    lineflag = -1 ;
                }
                for (row = Rstart [botblk]; row < botrow; row = RLinkUp [row])
                {
                    dlambda [row] += st*dl [row] ;
                }
                for (j = topcol; j < botcol; j++)
                {
                    c [j] += st*pA [j] ;
                }

                /* save dropped rows factors in components of dl */
            }
            else if ( st > 0 ) /* st = 0 only if step so poor fd < 0 initially*/
            {
                for (row = Rstart [botblk]; row < botrow; row = RLinkUp [row])
                {
                    dlambda [row] += st*dl [row] ;
                }
                for (j = topcol; j < botcol; j++)
                {
                    c [j] += st*pA [j] ;
                }
            }

            for (k = 1; k <= nbrk; k++)
            {
                ns [Heap [k]] = EMPTY ;
            }

            jobcols [jobnum] = ncoladd ; /* number of cols added so far */
            jobrows [jobnum] = nrowdel ; /* number of rows deleted so far */
            W->nf = nf ;

            /* end of line search */
            Stat->dasa_line += pproj_timer () - tic ;
            if ( PrintLevel > 1 )
            {
                printf("line search complete, st: %22.16e\n",st) ;
                fflush (stdout) ;
            }
#ifndef NDEBUG

            W->nrowdel = nrowdel ;
            W->ncoladd = ncoladd ;
            where = "end of line search in DASA" ;
            pproj_check_modlist (I, where) ;
            pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
            pproj_check_link (I, joblist, nj, where) ;
            pproj_checkc (I, where) ;
            /* lineflag = 2 if sd <= 0
               lineflag = 1 if line search terminates at nondifferentiable point
               lineflag =-1 if stepsize truncated to st = 1 */
            pproj_check_line (I, lineflag, botblk, ncoladd+nrowdel, dl, st) ;
            pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
            pproj_checkF (I, where) ;
#endif
        }

        ndrop = nrowdel ;
        W->nrowdel = nrowdel ;
        W->ncoladd = ncoladd ;
        W->nf = nf ;
        ASSERT (W->nrowadd == 0) ; /* do not add rows in this section */
        ASSERT (W->ncoldel == 0) ; /* do not delete columns in this section */

        if ( (botblk == root) && (nrowdel + ncoladd == 0) )
        {
            return (status) ;
        }

        /* ------------------------------------------------------------------ */
        /* update forward, update factorization for deleted rows and new cols */
        /* can either rechol the matrix or update the matrix                  */
        /* ------------------------------------------------------------------ */

        do_rechol = 0 ;
        if ( blks == 1 )
        {
            ASSERT (W->npup == 0 && W->npup_old == 0) ;
            do_rechol = pproj_cholquery (I) ;
        }

        if ( PrintLevel > 1 )
        {
            printf ("rechol: %i\n", do_rechol) ; 
        }
        colp = 0 ;
        rowp = 0 ;
        if ( !do_rechol ) /* use update and downdate */
        {

            /* -------------------------------------------------------------- */
            /* update */
            /* -------------------------------------------------------------- */

            /* delete rows */
            pproj_modrow (I, nj, MarkedForward, TRUE, -1, forward, changeRHS,
                          dl, updatework) ;
            Cncol = new_nj = nup = 0 ;
            for (jobnum = 0; jobnum < nj; jobnum++)
            {
                botblk = joblist [jobnum] ;
                topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
                botrow = row_start [botblk+1] ;
                toprow = row_start [topblk] ;
                NextColp = jobcols [jobnum] ;
                NextRowp = jobrows [jobnum] ;
                if ( PrintLevel > 1 )
                { 
                    if ( (colp == NextColp) &&
                         ((rowp == NextRowp) ||
                          (Rstart [botblk] >= row_start [botblk+1])) )
                    {
                        /* block done */
                        if ( botblk < root )
                        printf ("jobnum: %i botblk: %i done! parent: %i "
                                "kidsleft: %i\n", jobnum, botblk,
                                parent [botblk], kidsleft [parent [botblk]]-1) ;
                    }
                    else
                    {
                        printf ("jobnum: %i botblk: %i"
                                " col start: %ld row start: %ld\n",
                                jobnum, botblk, (LONG) colp, (LONG) rowp) ;
                    }
                    fflush (stdout) ;
                }

                if ( (colp == NextColp) &&
                     ((rowp == NextRowp) ||
                      (Rstart [botblk] >= row_start [botblk+1])) )
                {
                    /* block done */
                    if ( botblk == root )
                    {
                        return (status) ;
                    }
                    pa = parent [botblk] ;
                    l = --kidsleft [pa] ;
                    if ( l == 0 )
                    {
                        if ( PrintLevel > 1 )
                        {
                            printf ("l == 0\n") ;
                        }
                        while ( l == 0 )
                        {
                            /* all children done, move up to parent */
                            row = Rstart [pa] ;
                            if ( row == EMPTY )
                            {
                                /* block done */
                                if (W->L != NULL)
                                {
                                    /* zero out Lnz, block will be skipped */
                                    Lnz = W->L->nz ;
                                    q = row_start [pa+1] ;
                                    for (i = row_start [pa]; i < q; i++)
                                    {
                                        Lnz [i] = 1 ;   /* was 0 */
                                    }
                                }
                                if ( pa == root )
                                {
                                    return (status) ;
                                }

                                blk = pa ; /* else set starts for this block */
                                pa = Kp [blk] ;
                                qa = pa + nkids [blk] ;
                                for (; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    i = Rstart [k] ;
                                    if ( (i != EMPTY) && (i < row_start [k+1]) )
                                    {
                                        break ;
                                    }
                                }
                                if ( i == EMPTY ) i = nrow ;
                                Rstart [blk] = i ;

                                /* set the starting singleton for blk */
                                for (pa = Kp [blk]; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    if ( (j = lstart [k]) < sol_start1 [k] )
                                    {
                                        lstart [blk] = j ;
                                        break ;
                                    }
                                }

                                for (pa = Kp [blk]; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    if ( (j = ustart [k]) < sol_start1 [k] )
                                    {
                                        ustart [blk] = j ;
                                        break ;
                                    }
                                }
                                pa = parent [blk] ;
                                l = --kidsleft [pa] ;
                            }
                            else
                            {
                                break ;
                            }
                        }
                        if ( l == 0 )
                        {

#ifndef NDEBUG
                            if ( PrintLevel > 1 )
                            { 
                                printf("    add %i to job que\n", pa) ;
                            }
#endif

                            jobcols [new_nj] = EMPTY ;
                            joblist [new_nj++] = pa ;  /* move up to parent*/
                        }
                    }
                }
                else
                {
                    joblist [new_nj++] = botblk ;
                    for (; colp < NextColp; colp++)
                    {
                        j = ColmodList [colp] ;

                        if ( PrintLevel > 1 )
                        { 
                            printf ("    update col: %ld\n", (LONG) j) ;
                        }

                        q = Ap [j] + Anz [j] ;
                        Cp [Cncol] = p0 = p = Ap [j] ;
                        if ( q > p )
                        {
                            t = cold [j] ;
                            if ( Ai [q-1] < botrow )
                            {
                                for (; p < q; p++)
                                {
                                    i = Ai [p] ;
                                    if ( ir [i] <= nsingni )
                                    {
                                        ax = Ax [p] ;
                                        changeRHS [i] -= t*ax ;
                                        D [i] += ax*ax ; /* diag of AF*AF' */
                                        l = AFTp [i] + AFTnz [i]++ ;
                                        AFTx [l] = ax ;
                                        AFTi [l] = j ;
                                    }
                                }

                                Cnz [Cncol] = Anz [j] ;

                                /* colmark gives the botrow of the block
                                 * associated with added column */
                                colmark [Cncol] = botrow ;
                                Cncol++ ;
                            }
                            else
                            {
                                /* find botrow */
                                for (; p < q; p++)
                                {
                                    i = Ai [p] ;
                                    if ( i < botrow )
                                    {
                                        if ( ir [i] <= nsingni )
                                        {
                                            ax = Ax [p] ;
                                            changeRHS [i] -= t*ax ;
                                            D [i] += ax*ax ; /* diag of AF*AF'*/
                                            l = AFTp [i] + AFTnz [i]++ ;
                                            AFTx [l] = ax ;
                                            AFTi [l] = j ;
                                        }
                                    }
                                    else
                                    {
                                        if ( MarkedForward )
                                        {/*update entire matrix, part of solve,
                                          * colmark gives botrow of the block
                                          * associated with added column */

                                            colmark [Cncol] = botrow ; 
                                            Cnz [Cncol] = Anz [j] ;
                                            Cncol++ ;
                                        }
                                        else /* update part of matrix */
                                        {
                                            if ( p > p0 ) /* column nonempty */
                                            {
                                                colmark [Cncol] = botrow ;
                                                Cnz [Cncol] = p - p0 ;
                                                Cncol++ ;
                                            }
                                        }
                            
                                        if ( ir [i] <= nsingni )
                                        {
                                            l = AFTp [i] + AFTnz [i]++ ;
                                            ax = Ax [p] ;
                                            AFTx [l] = ax ;
                                            AFTi [l] = j ;
                                            D [i] += ax*ax ;
                                        }
                                        for (p++; p < q; p++)
                                        {
                                            i = Ai [p] ;
                                            if ( ir [i] <= nsingni )
                                            {
                                                l = AFTp [i] + AFTnz [i]++ ;
                                                ax = Ax [p] ;
                                                AFTx [l] = ax ;
                                                D [i] += ax*ax ;
                                                AFTi [l] = j ;
                                            }
                                        }
                                    }
                                }
                            } /* find bottom row in block, set r, AFT */
                        }     /* column has active rows */
                    }         /* end of loop over columns in job */
                }             /* end of column setup for modcol */
            }                 /* loop over jobs */


            /* -------------------------------------------------------------- */
            /* update the matrix */
            /* -------------------------------------------------------------- */

#ifndef NDEBUG
            where = "before update/downdate in DASA" ;
            pproj_checkA (I, 1, where) ;
            pproj_check_AT (I, where) ;
#endif
            ASSERT (W->ncoladd == Cncol) ;
            pproj_modcol (I, MarkedForward, +1, +1, colmark, Cp, Cnz,
                         forward, changeRHS, Cncol) ;
        }
        else /* it is better to rechol the matrix rather than update/downdate */
        {
            /* determine the new job list, without evaluating changeRHS,
               refactor the matrix, compute the forward solve */

            Stat->nchols++ ;
            Cncol = new_nj = nup = 0 ;
            for (jobnum = 0; jobnum < nj; jobnum++)
            {
                botblk = joblist [jobnum] ;
                topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
                botrow = row_start [botblk+1] ;
                toprow = row_start [topblk] ;
                NextColp = jobcols [jobnum] ;
                NextRowp = jobrows [jobnum] ;

#ifndef NDEBUG
                if ( PrintLevel > 1 )
                { 
                    if ( (colp == NextColp) &&
                         ((rowp == NextRowp) ||
                          (Rstart [botblk] >= row_start [botblk+1])) )
                    {
                        /* block done */
                        if ( botblk < root )
                        printf ("jobnum: %i botblk: %i done! parent: %i "
                                "kidsleft: %i\n", jobnum, botblk,
                                parent [botblk], kidsleft [parent [botblk]]-1) ;
                    }
                    else
                    {
                        printf ("jobnum: %i botblk: %i"
                                " col start: %ld row start: %ld\n",
                                jobnum, botblk, (LONG) colp, (LONG) rowp) ;
                    }
                }
#endif

                if ( (colp == NextColp) &&
                     ((rowp == NextRowp) ||
                      (Rstart [botblk] >= row_start [botblk+1])) )
                {
                    if ( botblk == root ) /* all rows were dropped */
                    {
                        W->nrowdel = 0 ;
                        nd = W->nd ;
                        for (k = 0; k < nrowdel; k++)
                        {
                            i = RowmodList [k] ;
                            RowmodFlag [i] = EMPTY ;
                            W->dropped [nd] = i ;
                            nd++ ;
                        }
                        W->nd = nd ;
                        return (status) ;
                    }
                    /* block done */
                    pa = parent [botblk] ;
                    l = --kidsleft [pa] ;
                    if ( l == 0 )
                    {
                        while ( l == 0 )
                        {
                            /* all children done, move up to parent */
                            row = Rstart [pa] ;
                            if ( row == EMPTY )
                            {
                                /* block done */
                                if (W->L != NULL)
                                {
                                    /* zero out Lnz, block will be skipped */
                                    Lnz = W->L->nz ;
                                    q = row_start [pa+1] ;
                                    for (i = row_start [pa]; i < q; i++)
                                    {
                                        Lnz [i] = 1 ;   /* was 0 */
                                    }
                                }
                                if ( pa == root )
                                {
                                    return (status) ;
                                }

                                blk = pa ; /* else set starts for this block */
                                pa = Kp [blk] ;
                                qa = pa + nkids [blk] ;
                                for (; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    i = Rstart [k] ;
                                    if ( (i != EMPTY) && (i < row_start [k+1]) )
                                    {
                                        break ;
                                    }
                                }
                                if ( i == EMPTY ) i = nrow ;
                                Rstart [blk] = i ;

                                /* set the starting singleton for blk */
                                for (pa = Kp [blk]; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    if ( (j = lstart [k]) < sol_start1 [k] )
                                    {
                                        lstart [blk] = j ;
                                        break ;
                                    }
                                }

                                for (pa = Kp [blk]; pa < qa; pa++)
                                {
                                    k = Kids [pa] ;
                                    if ( (j = ustart [k]) < sol_start1 [k] )
                                    {
                                        ustart [blk] = j ;
                                        break ;
                                    }
                                }
                                pa = parent [blk] ;
                                l = --kidsleft [pa] ;
                            }
                            else
                            {
                                break ;
                            }
                        }
                        if ( l == 0 )
                        {

                            if ( PrintLevel > 1 )
                            { 
                                printf("    add %i to job que\n", pa) ;
                            }

                            jobcols [new_nj] = EMPTY ;
                            joblist [new_nj++] = pa ;  /* move up to parent*/
                        }
                    }
                }
                else
                {
                    joblist [new_nj++] = botblk ;
                    for (; colp < NextColp; colp++)
                    {
                        j = ColmodList [colp] ;

                        if ( PrintLevel > 1 )
                        {
                            printf ("    update col: %ld, lineflag = 0\n",
                                    (LONG) j) ;
                        }

                        q = Ap [j] + Anz [j] ;
                        p0 = p = Ap [j] ;
                        if ( q > p )
                        {
                            for (; p < q; p++)
                            {
                                i = Ai [p] ;
                                if ( ir [i] <= nsingni )
                                {
                                    ax = Ax [p] ;
                                    D [i] += ax*ax ; /* diag of AF*AF' */
                                    l = AFTp [i] + AFTnz [i]++ ;
                                    AFTx [l] = ax ;
                                    AFTi [l] = j ;
                                }
                            } /* set AFT */
                        }     /* column has active rows */
                    }         /* end of loop over columns in job */
                }             /* end of column setup for modcol */
            }                 /* loop over jobs */

            /* -------------------------------------------------------------- */
            /* re-chol the matrix*/
            /* -------------------------------------------------------------- */

            pproj_updateAnz (I, 2) ; /*also sets AFTnz = 0 for dead rows*/
#ifndef NDEBUG
            where = "after line search and before rechol in DASA" ;
            pproj_checkA (I, 0, where) ;
            pproj_check_AT (I, where) ;
            pproj_check_AFT (I, TRUE, where) ;
#endif
            CHOLMOD (free_factor) (&(W->L), cmm) ;
            tic = pproj_timer () ;
            W->L = pproj_rechol (W->A, W->AFT, F, nf, beta, RLinkUp, W, cmm) ;
            Stat->chol += pproj_timer () - tic ;
#ifndef NDEBUG
            pproj_check_diag (I, chol, where);
#endif

            botblk = 0 ;
            botrow = row_start [botblk+1] ;
            topblk = leftdesc [botblk] ;
            toprow = row_start [topblk] ;

#ifndef NDEBUG
            if ( PrintLevel > 1 )
            {
                printf ("forward solve after rechol\n") ;
            }
#endif

            /* -------------------------------------------------------------- */
            /* forward solve after re-chol */
            /* -------------------------------------------------------------- */

            tic = pproj_timer () ;
            for (row = Rstart [botblk]; row < botrow; row = RLinkUp [row])
            {
                t = b [row] ;
                p = AFTp [row] ;
                q = p + AFTnz [row] ;
                ASSERT (ir [row] <= nsingni) ;
                for (; p < q; p++)
                {
                    t -= cold [AFTi [p]] * AFTx [p] ;
                }
                forward [row] = t ;
            }

            pproj_lsolve (W, forward, RLinkUp, Rstart [botblk], botrow,
                    MarkedForward) ;
            Stat->lsolve += pproj_timer () - tic ;
        }

        if ( PrintLevel > 0 )
        {
            if ( botblk == root )
            {
                printf("nj: %i new_nj: %i nup: %ld ndrop: %ld st: %e UP*\n",
                    nj, new_nj, (LONG) Cncol, (LONG) ndrop, st) ;
            }
            else
            {
                printf("nj: %i new_nj: %i nup: %ld ndrop: %ld st: %e UP\n",
                     nj, new_nj, (LONG) Cncol, (LONG) ndrop, st) ;
            }
            fflush (stdout) ;
        }

        /* ------------------------------------------------------------------ */
        /* do any separator solves */
        /* ------------------------------------------------------------------ */

        for (jobnum = 0; jobnum < new_nj; jobnum++)
        {

            if ( PrintLevel > 1 )
            {
                printf("jobnum: %i botblk: %i\n", jobnum, joblist [jobnum]) ;
            }

            /* above, we set jobcols to EMPTY if we moved up to parent */
            if ( jobcols [jobnum] == EMPTY )
            {
                /* Do a separator solve */
                botblk = joblist [jobnum] ;

                botrow = row_start [botblk+1] ;
                seprow = row_start [botblk] ;
                topblk = leftdesc [botblk] ;
                toprow = row_start [topblk] ;
                istart = Rstart [botblk] ;

                if ( !MarkedForward )
                {
                    /* this is truly an incremental LDL' factorization */

#ifndef NDEBUG
                    if ( PrintLevel > 1 )
                    {
                        printf("chol from %ld to %ld\n",
                               (LONG) toprow, (LONG) botrow-1);
                    }
                    where = "before incremental LDL" ;
                    pproj_check_AFT (I, TRUE, where) ;
                    pproj_checkA (I, 1, where) ;
#endif

                    tic = pproj_timer () ;

                    CHOLMOD (rowfac_mask2) (W->A, W->AFT, beta, istart, botrow,
                                     ir, nsingni1, RLinkUp, W->L, cmm) ;

                    I->Stat->cholinc += pproj_timer () - tic ;
                    W->cholaatflops += cmm->rowfacfl ;
                }

                /* Rstart points to first row in separator */
                tic = pproj_timer () ;
                for (row = istart; row < botrow; row = RLinkUp [row])
                {
                    t = b [row] ;
                    p = AFTp [row] ;
                    ASSERT (ir [row] <= nsingni) ;
                    q = p + AFTnz [row] ;
                    for (; p < q; p++)
                    {
                        t -= cold [AFTi [p]]*AFTx [p] ;
                    }
                    forward [row] = t ;
                }
                Rend [botblk] = RLinkDn [row] ;

                if ( PrintLevel > 1 )
                {
                    printf("    separator! botblk: %i toprow: %ld seprow: %ld"
                           " solve from %ld to %ld\n",
                           botblk, (LONG) toprow, (LONG) seprow,
                           (LONG) istart, (LONG) botrow) ;
                }

                /* Forward solve and update Rstart.
                   Reset Rstart to 1st row in block starting at top row .
                   Temporarily set the initial RLinkDn to -1, this simplifies
                   indexing in the solve routine */
                k = RLinkUp [nrow] ;
                RLinkDn [k] = -1 ;
                pproj_lsolve0 (W, forward, RLinkUp, RLinkDn, Rstart+botblk,
                    istart, toprow, seprow, botrow, MarkedForward) ;
                Stat->lsolve += pproj_timer () - tic ;
                RLinkDn [k] = nrow ; /* restore RLinkDn */

                blk = botblk ;

                /* set the starting singleton for blk */
                p0 = Kp [blk] ;
                q = p0 + nkids [blk] ;
                for (p = p0; p < q; p++)
                {
                    k = Kids [p] ;
                    if ( (j = lstart [k]) < sol_start1 [k] )
                    {
                        lstart [blk] = j ;
                        break ;
                    }
                }

                for (p = p0; p < q; p++)
                {
                    k = Kids [p] ;
                    if ( (j = ustart [k]) < sol_start1 [k] )
                    {
                        ustart [blk] = j ;
                        break ;
                    }
                }
            }
        }
        nj = new_nj ;

#ifndef NDEBUG
        where = "after forward solve at end" ;
        pproj_check_link (I, joblist, nj, where) ;
        if ( (blks == 1) || MarkedForward )
        {
            pproj_check_diag (I, chol, where) ;
        }
        pproj_check_forward (I, forward, b, joblist, nj, where) ;
#endif
    }
    return (status) ;
}

/* ========================================================================= */
/* === pproj_rechol ======================================================== */
/* ========================================================================= */
cholmod_factor *pproj_rechol
(
    cholmod_sparse   *A,
    cholmod_sparse *AFT,    /* A(:,f)' */
    PPINT            *F,    /* the free set f = columns F [0..nf-1] */
    PPINT            nf,
    PPFLOAT    beta [2],
    PPINT      *RLinkUp,
    PPwork           *W,
    cholmod_common *cmm
)
{
    cholmod_factor *L ;
    PPINT nrow, ncol, *First, *Level, *Iwork, *Parent, *Post ;
    int get_aft ;

    get_aft = (AFT == NULL) ;
    if (get_aft)
    {
        AFT = CHOLMOD (transpose) (A, 1, cmm) ;
    }

    nrow = A->nrow ;
    ncol = A->ncol ;

    Iwork = W->arrayi ;
    First  = Iwork ;  Iwork += nrow ;
    Level  = Iwork ;  Iwork += nrow ;
    Post   = Iwork ;  Iwork += nrow ;
    Parent = Iwork ;  Iwork += nrow ;

    /*
    Parent = cholmod_malloc (nrow, sizeof (int), cmm) ;
    First = cholmod_malloc (nrow, sizeof (int), cmm) ;
    Level = cholmod_malloc (nrow, sizeof (int), cmm) ;
    Post = cholmod_malloc (nrow, sizeof (int), cmm) ;
    */

    /* TODO: could pass in a simplicial symbolic L here instead (minor issue) */
    L = CHOLMOD (allocate_factor) (nrow, cmm) ;

    cmm->anz = EMPTY ;

    /* find the etree */
    /* uses Iwork (0..nrow+ncol) */
    CHOLMOD (etree) (AFT, Parent, cmm) ;

    /* postorder the etree (required by cholmod_rowcolcounts) */
    /* uses Iwork (0..2*nrow) */
    CHOLMOD (postorder) (Parent, nrow, NULL, Post, cmm) ;

    /* cholmod_postorder doesn't set cmm->status if it returns < nrow */
    /* cmm->status = (!ok && cmm->status == CHOLMOD_OK) ?
        CHOLMOD_INVALID : cmm->status ; */

    /* analyze LL'=A(:,f)*A(:,f)' */
    /* uses Iwork (0..2*nrow+ncol-1) */
    CHOLMOD (rowcolcounts) (A, F, nf, Parent,
            Post, NULL, L->ColCount, First, Level, cmm) ;

    cmm->method [0].fl  = cmm->fl ;
    cmm->method [0].lnz = cmm->lnz ;

    /* See if we want to do a supernodal factorization.
       The supernodal routine gives a valgrind error in the
       debug mode when the mkl BLAS are used, so we skip this
       if the debugger is being used. Also, openblas has
       problems with the supernodal routine which lead to
       huge solution times, although the numerical results are
       still correct. If openblas are used, then these
       supernodal statements should also be skipped. The NSUPER
       compiler flag is set in SuiteOPTconfig. */
#ifndef NSUPER
    if (cmm->supernodal > CHOLMOD_AUTO
    || (cmm->supernodal == CHOLMOD_AUTO &&
        cmm->lnz > 0 &&
        (cmm->fl / cmm->lnz) >= cmm->supernodal_switch))
    {
        /* uses Iwork (0..5*nrow-1) */
        CHOLMOD (super_symbolic) (A, AFT, Parent, L, cmm) ;
    }
#endif

    /* ---------------------------------------------------------------------- */
    /* factorize */
    /* ---------------------------------------------------------------------- */

    if ( L->is_super )
    {
        CHOLMOD (factorize_p) (A, beta, F, nf, L, cmm) ;
    }
    else
    {
        CHOLMOD (rowfac_mask) (A, AFT, beta, RLinkUp [nrow], nrow,
                         NULL, RLinkUp, L, cmm) ;
    }

    if (get_aft)
    {
        CHOLMOD (free_sparse) (&AFT, cmm) ;
    }

    W->nchols++ ;
    W->cholaatflops += cmm->fl + cmm->aatfl ;
    W->cholflops = cmm->fl ;        /* excl. flops to compute A(:,f)*A(:,f)' */
    W->Lnnz = cmm->lnz ;

    /* insist that diag (L) >= sigma */
    {
        PPINT i, *Lp ; 
        PPFLOAT sigma, *Lx ;
        Lp = L->p ;
        Lx = L->x ;
        sigma = beta [0] ;
        for (i = RLinkUp [nrow]; i < nrow; i = RLinkUp [i])
        {
            if ( Lx [Lp [i]] < sigma )
            {
                Lx [Lp [i]] = sigma ;
            }
        }
    }

    return (L) ;
}

/* ========================================================================== */
/* ======= pproj_modrow ===================================================== */
/* ========================================================================== */
void pproj_modrow
(
    PPcom           *I,
    int             nj, /* number of jobs in multilevel update,
                           ignored if no solve update */
    int  MarkedForward, /* = TRUE (use botrow to update forward solve
                           = FALSE (botrow not needed in forward solve) */
    int    UpdateSolve, /* = TRUE (forward solve update)
                           = FALSE (only update factorization) */
    int          RowOp, /* = +1 (row is added)
                           = -1 (row is deleted) */
    PPFLOAT   *forward, /* forward solve */
    PPFLOAT *changeRHS, /* change in right hand side */
    PPFLOAT        *dl, /* change in lambda */
    PPINT  *updatework  /* nrow int work space needed when UpdateSolve TRUE */
)
{

    PPINT *ATi, *ATp, *AFTp, *AFTi, *AFTnz, Rp [2], Rnz [1],
         *RowmodList, *RowmodFlag, *ColmodFlag,
         colmark [1], *row_start,
         *jobrows, *ati, *afti, *iwork, *worki,
         nchg, nrowadd, nrowdel, blks, j, k, p, q, row, botrow,
         NextRowp, rowp, root, jobnum, nz, nd ;
    int botblk, PrintLevel, *ib, *joblist ;
    PPFLOAT tic, elapsed, flops, *ATx, *atx, *xwork, *workd ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;
    cholmod_sparse *R, Rmatrix ;
    cholmod_dense Xstruc, *X, DeltaBstruc, *DeltaB ;
    cholmod_common *cmm ;
    PPFLOAT yk [2] ;
    cholmod_factor *L ;

    tic = pproj_timer () ;

    Parm = I->Parm ;
    Prob = I->Prob ;
    Stat = I->Stat ;
    W = I->Work ;
    L = W->L ;

    RowmodList = W->RowmodList ;
    RowmodFlag = W->RowmodFlag ;
    ColmodFlag = W->ColmodFlag ;

    PPINT const ncol    = Prob->ncol ;
    PPINT const nrow    = Prob->nrow ;
    PPINT const nsingni = Prob->ni + Prob->nsing ;

    botrow = nrow ;
    botblk = 0 ;
    flops = 0 ;
    PrintLevel = Parm->PrintLevel ;

#ifndef NDEBUG
    if (PrintLevel > 0)
             printf ("modrow Op: %i UpdateSolve: %i MarkedForward: %i\n",
             RowOp, UpdateSolve, MarkedForward) ;
    pproj_check_modlist (I, "inside call_modrow") ;
    if (PrintLevel > 0)
    {
        if ( RowOp > 0 )
        {
            for (k = 1; k <= W->nrowadd; k++)
            {
                printf ("add inequality: %ld\n", (LONG) RowmodList [nrow-k]);
            }
        }
        else
        {
            for (k = 0; k < W->nrowdel; k++)
            {
                printf ("del inequality: %ld\n", (LONG) RowmodList [k]) ;
            }
        }
    }
#endif

    R = &Rmatrix ;

    cmm = W->cmm ;

    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;

    AFTp = W->AFTp ;
    AFTi = W->AFTi ;
    AFTnz = W->AFTnz ;

#ifndef NDEBUG
    for (row = 0 ; row <= nrow ; row++)
    {
        ASSERT (AFTp [row] == ATp [row]) ;
    }
#endif

    nd = W->nd ;
    if ( UpdateSolve )
    {

        if ( RowOp >= 0 )
        {
           printf ("forward solve update with row addition not"
                   "implemented in current code\n") ;
           pproj_error (-1, __FILE__, __LINE__, "stop") ;
        }
        /* In the middle of a big iteration, a row is deleted.
           For an update solve, use the passed down array updatework for the
           integer row index storage in the R array. */
        pproj_cholmod_sparse (R, nrow, 1, nrow, Rp, Rnz, updatework, NULL,
        FALSE, TRUE, CHOLMOD_PATTERN) ;

        /* store the forward solve vector in a CHOLMOD dense matrix */
        X = &Xstruc ;
        pproj_cholmod_dense (X, nrow, forward) ;

        /* store the change in the right side in a CHOLMOD dense matrix */
        DeltaB = &DeltaBstruc ;
        pproj_cholmod_dense (DeltaB, nrow, changeRHS) ;

        blks = W->blks ;
        root = blks - 1 ;
        row_start = W->row_start ;

        joblist = W->joblist ;
        jobrows = W->jobrows ;
        nchg = W->nrowdel ;
        W->nrowdel = 0 ;
        rowp = 0 ;

        for (jobnum = 0; jobnum < nj; jobnum++)
        {
            botblk = joblist [jobnum] ;
            botrow = colmark [0] = row_start [botblk+1] ; /* MARK set colmark */
            NextRowp = jobrows [jobnum] ;
            for (; rowp < NextRowp; rowp++)
            {
                row = RowmodList [rowp] ;
                RowmodFlag [row] = EMPTY ;
                W->dropped [nd] = row ;
                nd++ ;
                afti = AFTi+AFTp [row] ; /* columns for row being deleted */
                nz = AFTnz [row] ;
                AFTnz [row] = 0 ;
                ASSERT (W->ir [row] > nsingni) ;
#ifndef NDEBUG
                if ( PrintLevel > 2 )
                {
                    printf ("    botblk: %i drop row: %ld\n",
                            botblk, (LONG) row) ;
                }
#endif
                yk [0] = -dl [row] ;
                yk [1] = PPZERO ;

                CHOLMOD (row_lsubtree) (W->A, afti, nz, row, L, R, cmm) ;
                CHOLMOD (rowdel_mark) (row, R, yk, colmark, L, X, DeltaB, cmm);

                flops += cmm->modfl ;
                cmm->modfl = 0 ;
            }
        }
    }
    else /* Not an update solve (at the start of a big iteration).
            The allocations are done from the work structure */
    {
        workd = W->arrayd ; /* double */
        atx   = workd ; workd += ncol ;
        xwork = workd ; workd += nrow ;

        worki = W->arrayi ; /* int */
        ati   = worki ; worki += ncol ;
        iwork = worki ; worki += nrow ;

        pproj_cholmod_sparse (R, nrow, 1, nrow, Rp, Rnz, iwork, xwork, FALSE,
                          TRUE, (RowOp < 0) ? CHOLMOD_PATTERN : CHOLMOD_REAL) ;

        ib = W->ib ;
        if ( RowOp < 0 ) /* drop rows */
        {
            nchg = nrowdel = W->nrowdel ;
            W->nrowdel = 0 ;

            for (k = 0; k < nrowdel; k++)
            {
                row = RowmodList [k] ;
                RowmodFlag [row] = EMPTY ;
                W->dropped [nd] = row ;
                nd++ ;
                q = ATp [row+1] ;
                AFTnz [row] = 0 ;
                nz = 0 ;

#ifndef NDEBUG
                if (PrintLevel > 2) printf ("    del row: %ld\n", (LONG) row) ;
#endif

                /* find the superset of the active columns */
                for (p = ATp [row]; p < q; p++)
                {
                    j = ATi [p] ;
                    if ( ib [j] ) /* currently bound */
                    {
                         /* but it was in the L matrix */
                        if ( ColmodFlag [j] != EMPTY ) ati [nz++] = j ;
                    }
                    else           /* currently free */
                    {
                         /* and in the L matrix */
                        if ( ColmodFlag [j] == EMPTY ) ati [nz++] = j ;
                    }
                }

                ASSERT (W->ir [row] > nsingni) ;
                ASSERT (!W->A->packed) ;

                CHOLMOD (row_lsubtree) (W->A, ati, nz, row, L, R, cmm) ;
                CHOLMOD (rowdel) (row, R, L, cmm) ;

                flops += cmm->modfl ;
                cmm->modfl = 0 ;
            }
        }
        else /* add rows */
        {
            nchg = nrowadd = W->nrowadd ;
            W->nrowadd = 0 ;
            for (k = 1; k <= nrowadd; k++)
            {
                row = RowmodList [nrow-k] ;
                RowmodFlag [row] = EMPTY ;
                ASSERT (W->ir [row] <= nsingni) ;
                q = ATp [row+1] ;
                nz = 0 ;

#ifndef NDEBUG
                if (PrintLevel > 2) printf ("    add row: %ld\n", (LONG) row) ;
#endif

                /* find the superset of the active columns */
                for (p = ATp [row]; p < q; p++)
                {
                    j = ATi [p] ;
                    if ( ib [j] ) /* currently bound */
                    {
                        if ( ColmodFlag [j] != EMPTY ) /* but in the L matrix */
                        {
                            ati [nz] = j ;
                            atx [nz] = ATx [p] ;
                            nz++ ;
                        }
                    }
                    else           /* currently free */
                    {
                        if ( ColmodFlag [j] == EMPTY ) /* and in the L matrix */
                        {
                            ati [nz] = j ;
                            atx [nz] = ATx [p] ;
                            nz++ ;
                        }
                    }
                }

                if ( nz > 0)
                {
                    pproj_rowadd_prep (row, I, W->A, ati, atx, nz, R, nrowadd-k,
                                       RowmodList+nrow-nrowadd, cmm) ;
                    CHOLMOD (rowadd) (row, R, L, cmm) ;
                    flops += cmm->modfl ;
                    cmm->modfl = 0 ;
                }
                else /* the row is zero, the diagonal element in L is Totsigma*/
                {
                    PPINT *Lp ;
                    PPFLOAT *Lx ;
                    Lp = L->p ;
                    Lx = L->x ;
                    Lx [Lp [row]] = I->Work->Totsigma ;
                }
            }
        }
        botblk = root = 0 ;
    }

    W->nd = nd ;
    if ( (botblk < root) && !MarkedForward )
    { /* partial update at a node below the root */
        W->npup += nchg ;
        W->pupflops += flops ;
        W->npup_cur += nchg ;
    }
    else
    {
        W->nrup += nchg ;
        W->rupflops += flops ;
        if ( botblk < root )
        {
            W->npup_cur += nchg ;
        }
    }

    elapsed = pproj_timer () - tic ;
    Stat->modrow += elapsed ;
    if ( RowOp > 0 )
    {
        Stat->rowup += nchg ;
    }
    else
    {
        Stat->rowdn += nchg ;
    }

#ifndef NDEBUG
    if ( UpdateSolve )
    {
        pproj_check_const (changeRHS, PPZERO, NULL, 0, nrow,
                           "changeRHS in modrow") ;
    }
    /* NOTE: check_diag only works when the entire matrix is updated */
    if ( (botrow == nrow) || MarkedForward )
    {
        pproj_check_diag (I, FALSE, "in modrow");
    }
#endif
}

/* ========================================================================== */
/* ======= pproj_modcol ===================================================== */
/* ========================================================================== */

void pproj_modcol
(
    PPcom           *I,
    int  MarkedForward, /* = 0 (botrow not needed forward solve)
                           = 1 (use botrow to update forward solve) */
    int    UpdateSolve, /* = 0 (only update factorization)
                           = 1 (forward solve update) */
    int          ColOp, /* = +1 (cols are added)
                           = -1 (cols are deleted) */
    PPINT     *Colmark, /* bottom row of block associated with added columns */
    PPINT          *Cp, /* pointers into Ai or Ax of columns to add or delete */
    PPINT         *Cnz, /* number of nonzeros in columns to add or delete */
    PPFLOAT   *forward, /* forward solve */
    PPFLOAT *changeRHS, /* change in right hand side */
    PPINT           nf  /* number of columns to add */
)
{

    PPINT *colmark, *ColmodList, *ColmodFlag, *ir,
         i, botrow, ncoladd, ncoldel ;
    PPFLOAT tic, elapsed ;
    PPstat *Stat ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;
    cholmod_dense *X, Xstruc, *DeltaB, DeltaBstruc ;
    cholmod_sparse Cstruc, *C ;
    cholmod_common *cmm ;

    if ( nf == 0 ) return ; /* there were no columns */

    tic = pproj_timer () ;

    Parm = I->Parm ;
    W = I->Work ;
    cmm = W->cmm ;
    ir = W->ir ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;
    Prob = I->Prob ;

    PPINT const ncol    = Prob->ncol ;
    PPINT const nrow    = Prob->nrow ;
    PPINT const nsingni = Prob->ni + Prob->nsing ;
/*----------------------------------------------------------------------------*/
#ifndef NDEBUG
    if (Parm->PrintLevel > 1)
        printf ("modcol Op: %i UpdateSolve: %i MarkedForward: %i\n",
                 ColOp, UpdateSolve, MarkedForward) ;
    if ( Colmark != NULL )
    {
        pproj_checkA (I, 1, "before column updates in modcol") ;
    }
    pproj_check_modlist (I, "before column updates in modcol") ;
    if (Parm->PrintLevel > 0)
    {
        if ( ColOp > 0 )
        {
            for (i = 0; i < W->ncoladd; i++)
            {
                printf ("add col: %ld\n", (LONG) ColmodList [i]) ;
            }
        }
        else
        {
            for (i = 1; i <= W->ncoldel; i++)
            {
                printf ("del col: %ld\n", (LONG) ColmodList [ncol-i]) ;
            }
        }
    }
#endif
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

    if ( ColOp > 0 ) /* columns are added */
    {
        ncoladd = W->ncoladd ;
        W->ncoladd = 0 ;
        for (i = 0; i < ncoladd; i++) ColmodFlag [ColmodList [i]] = EMPTY ;
    }
    else             /* columns are deleted */
    {
        ncoldel = W->ncoldel ;
        W->ncoldel = 0 ;
        for (i = 1; i <= ncoldel; i++) ColmodFlag [ColmodList [ncol-i]] = EMPTY;
    }
    Stat = I->Stat ;

    /* store the forward solve vector in a CHOLMOD dense matrix */
    X = &Xstruc ;
    pproj_cholmod_dense (X, nrow, forward) ;

    /* store the change in the right side in a CHOLMOD dense matrix */
    DeltaB = &DeltaBstruc ;
    pproj_cholmod_dense (DeltaB, nrow, changeRHS) ;

    /* store the columns to free in a CHOLMOD sparse matrix */
    C = &Cstruc ;
    pproj_cholmod_sparse (C, nrow, nf, Prob->Ap [ncol], Cp, Cnz,
                          Prob->Ai, Prob->Ax, TRUE, FALSE, CHOLMOD_REAL) ;

    Stat = I->Stat ;
        
    colmark = NULL ;
    if ( UpdateSolve )
    {
        botrow = Colmark [0] ;
        if ( botrow < nrow ) colmark = Colmark ;
    }
    else
    {
        X = NULL ;
        DeltaB = NULL ;
        botrow = nrow ;
    }

    if ( ColOp > 0 )
    {
        CHOLMOD (updown_mask2) (TRUE, C, colmark, ir, nsingni+1, W->L, X,
                                DeltaB, cmm);
    }
    else
    {
        CHOLMOD (updown_mask2) (FALSE, C, colmark, ir, nsingni+1, W->L, X,
                                DeltaB,cmm);
    }

    if ( (botrow < nrow) && !MarkedForward )
    { /* multilevel partial update at a node below root */
        W->npup += nf ;
        W->npup_cur += nf ; /* counts number of updates below root,
                                full or partial */
        W->pupflops += cmm->modfl ;
    }
    else
    {
        W->nrup += nf ;
        if ( botrow < nrow ) W->npup_cur += nf ;
        W->rupflops += cmm->modfl ;
    }

    elapsed = pproj_timer () - tic ;
    Stat->modcol += elapsed ;

    Stat->updowns [PPMIN (nf, Stat->size_updowns)] += 1 ;

    if ( ColOp > 0 ) Stat->colup += nf ;
    else             Stat->coldn += nf ;
/*----------------------------------------------------------------------------*/
#ifndef NDEBUG
    pproj_check_modlist (I, "tail of call_modcol") ;
    if ( UpdateSolve )
    {
        pproj_check_const (changeRHS, PPZERO, NULL, 0, nrow,
                          "changeRHS in modcol") ;
    }
    /* NOTE: check_diag assumes the entire matrix is updated */
    if ( (botrow == nrow) || MarkedForward )
    {
        pproj_check_diag (I, FALSE, "modcol") ;
    }
#endif
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
}

/* ========================================================================== */
/* === pproj_lsolve ========================================================= */
/* ========================================================================== */
/* Solve Lx = b, over the block toprow <= i < botrow */
/* ========================================================================== */

#include "t_pproj_lsolve.c"
#define PARTIAL
#include "t_pproj_lsolve.c"

void pproj_lsolve
(
    PPwork      *W,
    PPFLOAT     *X, /* X [0 .. (L->ncol)-1], right hand side, on input.
                           solution to Lx=b in locations jstart to botrow
                           on output */
    PPINT *RLinkUp,
    PPINT   jstart, /* either toprow or seprow */
    PPINT   botrow,
    int     update
)
{
    /* ====================================================================== */
    /* === local variables ================================================== */
    /* ====================================================================== */

    if (update)
    {
        pproj_lsol_partial (W->L, X, jstart, botrow, RLinkUp) ;
    }
    else
    {
        pproj_lsol (W->L, X, jstart, botrow, RLinkUp) ;
    }
}

/* ========================================================================== */
/* === pproj_dltsolve ======================================================= */
/* ========================================================================== */

/* Solve DL'x = b , over the block toprow <= i < botrow */

/* ========================================================================== */

#include "t_pproj_dltsolve.c"
#define PARTIAL
#include "t_pproj_dltsolve.c"

void pproj_dltsolve
(
    PPwork        *W,
    PPFLOAT       *X, /* X [0 .. (L->ncol)-1], right hand side, on input. */
    PPFLOAT *forward, /* solution to DL'x=b, on output */
    PPINT   *RLinkDn,
    PPINT     toprow,
    PPINT       iend,
    PPINT     update,
    PPINT     botrow
)
{
    if (update)
    {
        pproj_dltsol_partial (W->L, X, forward, iend, toprow, RLinkDn, botrow) ;
    }
    else
    {
        pproj_dltsol (W->L, X, forward, iend, toprow, RLinkDn) ;
    }
}

/* ========================================================================== */
/* === pproj_lsolve0 ======================================================== */
/* ========================================================================== */
/* Separator solve:
   Solve Lx = b, over the block given by seprow <= i < botrow */

/* ========================================================================== */

void pproj_lsolve0
(
    PPwork     *W,
    PPFLOAT    *X, /* X [0 .. (L->ncol)-1], right hand side, on input.
                      solution to Lx=b in locations jstart to botrow
                      on output */
    PPINT *RLinkUp,
    PPINT *RLinkDn,
    PPINT  *Rstart, /* return the new Rstart for botblk */
    PPINT   jstart, /* first row in separator block */
    PPINT   toprow,
    PPINT   seprow,
    PPINT   botrow,
    int     update
)
{
    /* ====================================================================== */
    /* === local variables ================================================== */
    /* ====================================================================== */

    PPINT i, j, jprev, k, p, p2, *Li, *Lp, *Lnz ;
    PPFLOAT xj, *Lx ;
    cholmod_factor *L ;

    L = W->L ;
    if ( L->nzmax == 0 ) return ;
    Li = L->i ;
    Lx = L->x ;
    Lp = L->p ;
    Lnz = L->nz ;

/* ====================================================================== */
/* === solve Lx=b ======================================================= */
/* ====================================================================== */

    /* substitution part of the separator solve
       start at the column corresponding to the separator and work down
       to the column associated with the top row */
    if ( update )
    {

        jprev = jstart ;
        for (j = RLinkDn [jstart]; j >= toprow; j = RLinkDn [j])
        {
            jprev = j ;
            xj = X [j] ;
            p = Lp [j] ;
            p2 = Lp [j] + Lnz [j] ;
            for (p++ ; p < p2 ; p++)
            {
                i = Li [p] ;
                if (i < seprow) continue ;
                if (i >= botrow) break ;
                X [i] -= Lx [p]*xj ;
            }
        }
    }
    else
    {
        for (j = RLinkDn [jstart]; j >= toprow; j = RLinkDn [j])
        {
            jprev = j ;
            xj = X [j] ;
            p = Lp [j] ;
            k = Lnz [j] ;
            p2 = p + k ;
            p++ ;
            if ( k > 1 )
            {
                if ( Li [p] >= seprow )
                {
                    while ( p < p2 )
                    {
                        X [Li [p]] -= Lx [p]*xj ;
                        p++ ;
                    }
                }
                else
                {
                    while ( (i = Li [--p2]) >= seprow )
                    {
                        X [i] -= Lx [p2]*xj ;
                    }
                }
            }
        }
    }
    *Rstart = jprev ;

    /* forward solve part of the separator solve */
    if ( update )
    {
        for (j = jstart; j < botrow; j = RLinkUp [j])
        {
            xj = X [j] ;
            p = Lp [j] ;
            k = Lnz [j] ;
            p2 = p + k ;
            p++ ;
            if ( k > 1 )
            {
                if ( Li [p2-1] < botrow )
                {
                    while ( p < p2 )
                    {
                        X [Li [p]] -= Lx [p]*xj ;
                        p++ ;
                    }
                }
                else
                {
                    while ( (i = Li [p]) < botrow )
                    {
                        X [i] -= Lx [p++]*xj ;
                    }
                }
            }
        }
    }
    else
    {
        for (j = jstart; j < botrow; j = RLinkUp [j])
        {
            xj = X [j] ;
            p = Lp [j] ;
            p2 = p + Lnz [j] ;
            for (p++ ; p < p2; p++)
            {
                X [Li [p]] -= Lx [p]*xj ;
            }
        }
    }
}

/* ========================================================================== */
/* ==== pproj_upspeed ======================================================= */
/* speed of the update code divided by the speed of the chol code */
/* ========================================================================== */
PPFLOAT pproj_upspeed
(
    PPFLOAT  fl, /* flops to perform a chol (excludes AF*AF') */
    PPFLOAT lnz /* nonzeros in cholesky factor */
)
{
    PPFLOAT upspeed ;
    if (lnz <= 0 || fl/lnz < 100)
    {
        upspeed = 1.0 ; /* speed of updates and chols are comparable */
    }
    else if (fl/lnz < 500)
    {
        upspeed = 0.6 ; /* flop rate of chols almost double that of updates */
    }
    else
    {
        upspeed = 0.3333 ; /* flop rate of chols are 3 times that of updates */
    }
    /*printf ("upspeed:  fl %14.0f  lnz  %14.0f  :: %g\n", fl, lnz, upspeed) ;*/
    return (upspeed) ;
}

/* ========================================================================== */
/* ==== pproj_cholquery ===================================================== */
/* ========================================================================== */
int pproj_cholquery /* TRUE  => chol the matrix
                       FALSE => update the matrix */
(
    PPcom *I
)
{
    int nmod ;

    PPFLOAT s, t, upspeed, rupflops, totflops, aatflops ;
    PPwork    *W ;

    W = I->Work ;

    /* if less than 5 rows, then chol the matrix */
    if ( W->nactive <= 5 )
    {
        return (TRUE) ;
    }
    /*nmod = # of updates/downdates/rowmods to be performed */
    nmod = W->nrowadd + W->nrowdel + W->ncoladd + W->ncoldel ;

    if ( W->nrup == 0 )
    {
        rupflops = W->Lnnz ;
    }
    else
    {
        rupflops = W->rupflops/(W->nrup) ;
    }

    /* W->npup : # of partial updates ("pups") done so far */

    /* W->cholflops is the flops to do the prior chol (excl AA') */
    upspeed = pproj_upspeed (W->cholflops, W->Lnnz) ;
    /* upspeed is the speed of the update code divided by the speed
       of the chol code */

    /* factorization also benefits during the partial updates since
       they are done over a part of the matrix, while the update approach
       needs to operate over the entire matrix, add in the cost of the
       partial updates */
                                                                                
    totflops = W->cholaatflops/W->nchols ;
    /* avg flops to do a chol (incl. AA') */
    aatflops = PPMAX (totflops - W->cholflops, 0) ;
    t = 2.*aatflops + upspeed*W->cholflops ;
    
    if ( W->npup > 0.0 )
    {
        t +=  (W->npup_old)                /* # pups in last pass */
           *(W->pupflops)/(W->npup) ;     /* avg flops to do a pup */
    }
 
    /* the cost of updates is (nmod + the number of partial updates)
       times the average number of flops in a full update */
    s = (nmod + (W->npup_old))*rupflops ;

    if ( s < t ) return (FALSE) ;/* do updates */
    else         return (TRUE) ; /* do chol, no update of whole L */

}

/* ========================================================================= */
/* === pproj_iterquery ===================================================== */
/* ========================================================================= */
/*  Determine whether a coordinate ascent, or ssor step should be
    performed.  The decision is based on the number of downdates and row
    additions that are to be performed and on the cost of an update/downdate
    versus the cost of an iteration. */
/* ========================================================================= */
   
void pproj_iterquery
(
    PPcom *I
)
{
    PPFLOAT upflops ;
    PPparm *Parm ;
    PPwork *W ;

    Parm = I->Parm ;
    W = I->Work ;

    /* If cholmod not used, then must use coordinate ascent, sparsa, or
       ssor routines */
    if ( !Parm->cholmod )
    {
        W->do_coor = TRUE ;
        W->do_ssor = TRUE ;
        /* set parameter for deciding when to switch to cholmod to infty */
        W->ssor1_its = INT_MAX ;
        return ;
    }

    /* estimate the flops associated with the update and solve process */
    if ( W->npup > 0 )     /* multilevel with some partial updates completed */
    {
        upflops = W->pupflops/W->npup ;
    }
    else if ( W->nrup > 0 ) /* single level with some full updates completed */
    {
        upflops = W->rupflops/W->nrup ;
    }
    else                    /* no information */
    {
        upflops = 4*W->Lnnz ;
    }
    if ( Parm->coorcost*W->Annz <= upflops )
    {
        W->do_coor = TRUE ;
    }
    else
    {
        W->do_coor = FALSE ;
    }
    if ( Parm->ssorcost*W->Annz <= upflops )
    {
        W->do_ssor = TRUE ;
        if ( W->Annz > 0 )
        {
            W->ssor1_its = ceil (upflops/(Parm->ssorcost*W->Annz)) ;
        }
        else
        {
            W->ssor1_its = upflops/Parm->ssorcost ;
        }
    }
    else
    {
        W->do_ssor = FALSE ;
        W->ssor1_its = 0 ;
    }
    /* if a significant fraction of rows are added, then let
       coordinate ascent and ssor try to drop them, even when the op-count
       above seemed too large, we are thinking that the historical data
       for Lnnz may not be correct since the matrix is changing so much. */
    if ( W->nactive > 10 )
    {
        if ( W->nrowadd / (float) W->nactive >= .1 )
        {
            W->chg_coor = 1 ;
            W->chg_ssor0 = 1 ;
            W->chg_ssor1 = 1 ;
            if ( W->ssor1_its == 0 ) W->ssor1_its = 1 ;
            W->do_coor = TRUE ;
            W->do_ssor = TRUE ;
        }
    }
 
    if ( Parm->PrintLevel > 0 )
    {
        printf ("upflops: %e Annz: %ld\n", upflops, (LONG) W->Annz) ;
        printf ("do_coor: %i do_ssor: %i ssor1_its: %ld\n",
                 W->do_coor, W->do_ssor, (LONG) W->ssor1_its) ;
    }
}

/* ========================================================================== */
/* ======= pproj_updateAnz ================================================== */
/* Find the rows that have changed from active to inactive or vice versa and
   arrange the columns so that the active rows come first and they are sorted.
   dropped stores the list of rows that have been dropped via calls to the
   modrow program. The variables RowmodList and RowmodFlag tell us the
   rows that should be dropped or added to L in order to update the
   current factorization. Based on where the code is invoked (location)
   and the values of these variables, we can prepare a list of columns
   that need to be updated. These are stored in the array mod_col below.
   We also store in the array ns, an integer which tells us how the
   column should be modified. ns = 0 means only delete dropped rows from active
   part of column of A, ns = 1 means only add rows to active part of
   column of A, and ns = 2 means both add and delete rows. We update
   the modlist and flags according to where the program is invoked. We also
   update these arrays inside modcol and modrow; in updateAnz, we only
   need to perform updating if the code is invoked before a factorization.
   For a factorization at the start of the program, we have to update
   everything. For a factorization in the middle of an iteration, we only
   have to update the flags associated with column additions and row
   deletions. Note that the work performed in this code is proportional
   to the change in the active and inactive parts of A */
/* ========================================================================== */

void pproj_updateAnz
(
    PPcom     *I,
    int location    /* = 0 means code called at the top of DASA
                           before adding the new rows to L
                       = 1 means before the factorization at the 
                           top of DASA
                       = 2 means inside the DASA iteration, it
                           was cheaper to refactor than update */
)
{

    PPINT  *AFTnz, *tempi, *ir, *ns,
           *Bi, *order, *w, *mod_col, *dropped, *worki,
           *RowmodList, *RowmodFlag, *ColmodList, *ColmodFlag,
            nrowadd, nrowdel, ncoladd, ncoldel,
            nmod, topi, i, j, k, l, m, n, p, p0, q, ii, ns_j, nd;
    PPFLOAT *workd, *tempx, *Bx, topa ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

    Parm = I->Parm ;
    W = I->Work ;
    dropped = W->dropped ;
    nd = W->nd ;
    W->nd = 0 ;
    RowmodList = W->RowmodList ;
    RowmodFlag = W->RowmodFlag ;
    ColmodList = W->ColmodList ;
    ColmodFlag = W->ColmodFlag ;
    Prob = I->Prob ;
    PPINT   const         *Ap = Prob->Ap ;
    PPINT                 *Ai = Prob->Ai ;
    PPINT                *Anz = Prob->Anz ;
    PPFLOAT               *Ax = Prob->Ax ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const    nsingni  = Prob->nsing + Prob->ni ;

    /* Transpose of A */
    PPINT const *ATp = W->ATp ;
    PPINT const *ATi = W->ATi ;

    AFTnz = W->AFTnz ;

    ir = W->ir ;
    ns = W->ns ;

    workd = W->arrayd ;
    tempx = workd ; workd += nrow ;

    worki   = W->arrayi ;
    tempi   = worki ; worki += nrow ;
    w       = worki ; worki += nrow ;
    order   = worki ; worki += nrow ;
    mod_col = worki ; worki += ncol ; /* columns that were fixed */

    nmod = 0 ;
    if ( Parm->PrintLevel > 1 )
    {
        printf ("updateAnz, nd: %ld\n", (LONG) nd) ;
    }
    for (k = 0; k < nd; k++)
    {
        /* dropped array stores rows that have been removed from L by modrow */
        i = dropped [k] ;
        if ( RowmodFlag [i] == EMPTY ) /* row is dropped */
        {
            q = ATp [i+1] ;
            p = ATp [i] ;
            for (; p < q; p++)
            {
                j = ATi [p] ;
                if ( ns [j] == EMPTY )
                {
                    mod_col [nmod] = j ;
                    ns [j] = 0 ;
                    nmod++ ;
                }
            }
        }
        else  /* row is added, it is currently deleted, hence no
                 change to Anz although L will change, temporarily set
                 RowmodFlag less than EMPTY then reset it below */
        {
            RowmodFlag [i] = EMPTY - RowmodFlag [i] - 1 ;
        }
    }
    nrowadd = W->nrowadd ;
    /* location = 1 or 2 means that the matrix will be refactored,
       not updated. location = 1 is at the top of DASA before starting
       the iteration, while location = 2 is after the line search, inside
       the DASA iteration */
    if ( location > 0 )
    {
        nrowdel = W->nrowdel ;
        W->nrowdel = 0 ;
        /* Check the recently dropped rows. These are rows that are
           scheduled for deletion, but not yet deleted. We can remove
           them from the rowmod list since the matrix will be refactored */
        for (k = 0; k <  nrowdel; k++)
        {
            i = RowmodList [k] ;
            RowmodFlag [i] = EMPTY ;
            AFTnz [i] = 0 ;
            q = ATp [i+1] ;
            p = ATp [i] ;
            for (; p < q; p++)
            {
                j = ATi [p] ;
                if ( ns [j] == EMPTY )
                {
                    mod_col [nmod] = j ;
                    ns [j] = 0 ;
                    nmod++ ;
                }
            }
        }
        ncoladd = W->ncoladd ;
        W->ncoladd = 0 ;
        for (k = 0; k <  ncoladd; k++) ColmodFlag [ColmodList [k]] = EMPTY ;
        if ( location == 1 ) /* check the row add list for new rows and
                                reset ColmodFlag for deleted columns */
        {
            W->nrowadd = 0 ;
            for (k = 1; k <= nrowadd; k++)
            {
                i = RowmodList [nrow-k] ;
                if ( RowmodFlag [i] > EMPTY )
                {
                    p = ATp [i] ;
                    q = ATp [i+1] ;
                    for (; p < q; p++)
                    {
                        j = ATi [p] ;
                        if ( ns [j] == EMPTY )
                        {
                            mod_col [nmod] = j ;
                            ns [j] = 1 ;
                            nmod++ ;
                        }
                        else if ( ns [j] == 0 ) ns [j] = 2 ;
                    }
                }
                RowmodFlag [i] = EMPTY ;
            }
            /* These columns will be handled by refactorization so delete
               them from the column modlist */
            ncoldel = W->ncoldel ;
            W->ncoldel = 0 ;
            for (k = 1; k <= ncoldel; k++)
            {
                ColmodFlag [ColmodList [ncol-k]] = EMPTY ;
            }
        }
    }
    else /* location = 0, the matrix will be updated. We need to retain
            the modlists, we just check the row additions to see how they
            effect the columns of A */
    {
        for (k = 1; k <= nrowadd; k++)
        {
            i = RowmodList [nrow-k] ;
            if ( RowmodFlag [i] > EMPTY )
            {
                p = ATp [i] ;
                q = ATp [i+1] ;
                for (; p < q; p++)
                {
                    j = ATi [p] ;
                    if ( ns [j] == EMPTY )
                    {
                        mod_col [nmod] = j ;
                        ns [j] = 1 ;
                        nmod++ ;
                    }
                    else if ( ns [j] == 0 ) ns [j] = 2 ;
                }
            }
            else
            {
                RowmodFlag [i] = EMPTY - 1 - RowmodFlag [i] ;
            }
        }
    }

    /* The following code is executed for all the locations where updateAnz
       is invoked. The columns of A are arranged so that the active
       rows are first, followed by the inactive rows. Moreover, the
       indices for the active rows in each column are placed in increasing
       order. */
    for (ii = 0; ii < nmod; ii++)
    {
        j = mod_col [ii] ;
        m = nrow ;
        n = 0 ;
        ns_j = ns [j] ;
        p0 = Ap [j] ;
        /* ns_j = 0 means only drop rows from active part of column, while
           ns_j = 2 means both add and drop rows from active part of column */
        if ( (ns_j == 0) || (ns_j == 2 ) )
        {
            q = p0 + Anz [j] ; /* current end of active rows, sorted to here */
            l = p = p0 ;       /* start of column */
            i = Ai [p] ;
            /* find the first dropped row in column */
            while ( ir [i] <= nsingni )
            {
                i = Ai [++p] ;
            }
            tempi [--m] = i ;  /* bottom of temp stores inactive rows */
            tempx [m] = Ax [p] ;
            /* Top rows of A contain active sorted indices,
               bottom of temp has inactive. In this sorted part of
               the column, extract the dropped rows and put them at the
               bottom of temp. Move the active rows forward, they will
               remain sorted. */
            l = p ;
            for (p++; p < q; p++)
            {
                i = Ai [p] ;
                if ( ir [i] <= nsingni )
                {
                    Ai [l] = i ;
                    Ax [l++] = Ax [p] ;
                }
                else
                {
                    tempi [--m] = i ;
                    tempx [m] = Ax [p] ;
                }
            }
        }
        else /* ns_j = 1, only add active rows to the sorted part of column */
        {
            l = p = p0 + Anz [j] ;
        }
        /* l is the end of the sorted part of the column with active rows.
           Starting at Ap [j] + Anz [j], extract active rows and put in
           bottom of temp, while inactive rows are retained in Ai. */
        if ( ns_j > 0 )
        {
            q = p ;  /* q = Ap [j] + Anz [j] = part of column already checked */
            p = Ap [j+1] ; /* p = start of next column */
            i = Ai [--p] ;
            /* start from col end and find first active row */
            while ( ir [i] > nsingni )
            {
                i = Ai [--p] ;
            }
            k = p ;
            /* store index of first active row in temp, this location in
               column can now be used to store inactive rows */
            tempi [n] = i ;
            tempx [n] = Ax [p] ;
            n++ ;
            for (; p > q; )
            {
                p-- ;
                i = Ai [p] ;
                if ( ir [i] <= nsingni )
                {
                    tempi [n] = i ;
                    tempx [n] = Ax [p] ;
                    n++ ;
                }
                else
                {
                    Ai [k] = i ;
                    Ax [k] = Ax [p] ;
                    k-- ;
                }
            }
            k++ ;
        }
        else k = p ;
        /* k stores the start of the inactive rows in column
           n is number of active rows in bottom of column j */
        p = l + n ; /* p is the end of the active rows in the column */
        Anz [j] = p - p0 ;
        Bi = tempi+(nrow-k) ;
        Bx = tempx+(nrow-k) ;
        while ( k > p )  /* put inactive rows in A, they are at end of temp */
        {
            k-- ;
            Ai [k] = Bi [k] ;
            Ax [k] = Bx [k] ;
        }
        if ( n > 0 )
        {
            /* sort the new active rows */
            if ( n > 1 )
            {
                if ( n > 2 ) pproj_iminsort (order, tempi, w, n) ;
                else
                {
                    if ( tempi [1] < tempi [0] )
                    {
                        order [0] = 1 ;
                        order [1] = 0 ;
                    }
                    else
                    {
                        order [0] = 0 ;
                        order [1] = 1 ;
                    }
                }
            }
            else
            {
                order [0] = 0 ;
            }
            l-- ;          /* end of the active stack */
            if ( l < p0 )  /* directly copy temp to A, A is currently empty */
            {
                Bi = order+(n-p) ;
                while ( p > p0 )
                {
                     m = Bi [--p] ;
                     Ai [p] = tempi [m] ;
                     Ax [p] = tempx [m] ;
                 }
            }
            else           /* shuffle together the 2 sorted stacks */
            {
                m = order [--n] ;
                topi = tempi [m] ;
                topa = Ai [l] ;
                while ( 1 )
                {
                    if ( l < p0 )
                    {
                        Ai [--p] = topi ;
                        Ax [p] = tempx [m] ;
                        Bi = order+(n-p) ;
                        while ( p > p0 )
                        {
                            m = Bi [--p] ;
                            Ai [p] = tempi [m] ;
                            Ax [p] = tempx [m] ;
                        }
                            break ;
                    }
                    if ( topi > topa )
                    {
                            Ai [--p] = topi ;
                            Ax [p] = tempx [m] ;
                            --n ;
                            if ( n < 0 ) break ;
                            m = order [n] ;
                            topi = tempi [m] ;
                        }
                        else
                        {
                            Ai [--p] = topa ;
                            Ax [p] = Ax [l--] ;
                            if ( l < p0 )
                            {
                            Ai [--p] = topi ;
                            Ax [p] = tempx [m] ;
                            Bi = order+(n-p) ;
                            while ( p > p0 )
                            {
                                    m = Bi [--p] ;
                                Ai [p] = tempi [m] ;
                                Ax [p] = tempx [m] ;
                            }
                            break ;
                        }
                        else
                        {
                            topa = Ai [l] ;
                        }
                    }
                }
            }
        }
    }
    for (i = 0; i < nmod; i++)
    {
        ns [mod_col [i]] = EMPTY ;  /* restore ns to all EMPTY */
    }
#ifndef NDEBUG
    pproj_checkA (I, 0, "at end of updateAnz") ;
    /* also check that ns is completely empty */
    k = PPMAX (ncol+nsingni+1, nrow) ;
    pproj_check_const (NULL, 0, ns, EMPTY, k, "at end of updateAnz") ;
#endif
}

/* ========================================================================== */
/* ======= pproj_rowadd_prep ================================================ */
/* compute the new row of AF*AF' corresponding to a row added to AF */
/* ========================================================================== */
void pproj_rowadd_prep
(
    PPINT             k, /* number of the row to add */
    PPcom            *I,
    cholmod_sparse   *A, /* the matrix */
    PPINT          *ati, /* column numbers in row */
    PPFLOAT        *atx, /* nonzeros in row */
    PPINT            nz, /* number of nonzeros */
    cholmod_sparse   *R, /* new row of AF*AF' */
    PPINT         ndead, /* number of currently dead rows still to be added */
    PPINT    *dead_rows, /* row numbers of currently dead rows */
    cholmod_common *cmm
)
{
    PPFLOAT a_kj, *Ax, *newrow, *Rx ;
    PPINT *Ap, *Ai, *Anz, *Flag, *Rp, *Ri ;
    PPINT mark, rnz, pf, i, j, l, p, p2 ;
    PPINT nrow = A->nrow ;

    Ap = A->p ;
    Ai = A->i ;
    Ax = A->x ;
    Anz = A->nz ;

    newrow = I->Work->newrow ; /* work space with nrow zeros */
    Flag = cmm->Flag ;    /* nrow array with all elements < mark */
    mark = cmm->mark ;

    Ri = R->i ;
    Rx = R->x ;
    Rp = R->p ;
    Rp [0] = 0 ;

    /* ====================================================================== */
    /* === R = C(:,k) where C = Ir*(Asigma*I + AF*AF')*Ir =================== */
    /* ====================================================================== */

    newrow [k] = I->Work->Totsigma ;

    /* rnz = number of nonzeros in C (:,k) including the diagonal */
    rnz = 0 ;

    /* add the diagonal entry */
    Ri [rnz++] = k ;
    Flag [k] = mark ;

    /* for each nonzero in AFT (:,k) evaluate the new row using the
       outer product rule for AF*AF' */
    for (pf = 0 ; pf < nz ; pf++)
    {
	j = ati [pf] ;
	a_kj = atx [pf] ;
	/* newrow += A (:,j) * a_kj */
	p = Ap [j] ;
	p2 = p + Anz [j] ;
	for ( ; p < p2 ; p++)
	{
	    i = Ai [p] ;
	    newrow [i] += Ax [p] * a_kj ;
	    if (Flag [i] < mark)
	    {
		Ri [rnz++] = i ;
		Flag [i] = mark ;
	    }
	}
    }

    /* At this point, newrow [i] holds C (i,k) */
    /* The nonzero pattern of column C is held in Ri (unsorted). */
    /* Flag [Ri [0:rnz-1]] are all equal to mark, rest < mark. */

    CHOLMOD (clear_flag) (cmm) ;
    /* Now Flag [i] < mark for all i */

    /* Since A was updated to include the nonzeros for the still dead
       (but soon to be added rows), we now need to zero out the elements
       of AF*AF' associated with these still dead rows */
    l = 0 ;
    if ( ndead > 0 )
    {
        mark = cmm->mark ;
        for (i = 0; i < ndead; i++)
        {
            Flag [dead_rows [i]] = mark ;
        }
        CHOLMOD (clear_flag) (cmm) ;
        /* Now Flag [i] < mark for all i */

        for (p = 0 ; p < rnz ; p++)
        {
            i = Ri [p] ;
            if ( Flag [i] < mark )
            {
                Rx [p-l] = newrow [i] ;
                Ri [p-l] = i ;
            }
            else l++ ;
	    newrow [i] = PPZERO ;
        }
    }
    else
    {
        for (p = 0 ; p < rnz ; p++)
        {
            i = Ri [p] ;
            Rx [p] = newrow [i] ;
            newrow [i] = PPZERO ;
        }
    }
    Rp [1] = rnz - l ;
#ifndef NDEBUG
    pproj_check_const (newrow, 0, NULL, EMPTY, nrow, "in rowadd_prep") ;
#endif
    /*  The kth row of C is in R */
}
