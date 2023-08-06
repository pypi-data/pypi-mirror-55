/* =========================================================================
   ============================== pproj_hotchol ============================
   =========================================================================
    A starting point was previously generated in pproj. It is either the
    solution obtained from a previous problem, or the solution obtained
    from the bound structure for a previous problem. We now update the
    work arrays and the list of updates that should be applied to the
    previously computed factorization. This routine is currently not
    designed to handle the case where nsing > 0. For an LP, this is routine
    is not used; instead pproj goes straight to pproj_dasa by setting the
    parameter use_startup = FALSE.
   ========================================================================== */

#include "pproj.h"

int pproj_hotchol
(
    PPcom *I
)
{
    int     *ib ;
    PPINT   Annz, ATnz, iri, i, j, k, l, m, p, q, row, nactive, nf,
            Rl, Ul, Ll, nrowadd, ncoladd, nrowdel, ncoldel,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList,
           *AFTi, *AFTnz, *AFTp, *F, *RLinkDn, *RLinkUp,
           *uLinkUp, *uLinkDn, *lLinkUp, *lLinkDn, *ir ;

    PPFLOAT errdual, bi, s, t, *AFTx, *b, *c,
           *lambda, *D, *x, *absAx ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;

#ifndef NDEBUG
    char   *where ;
    I->Check->location = 7 ; /* code operates in hotchol */
#endif
    /* extract the problem, statistics, and work structures from I */
    Parm = I->Parm ;
    Prob = I->Prob ;
    Stat = I->Stat ;
    W = I->Work ;
    int const PrintLevel = Parm->PrintLevel ;

    /* Problem data */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPFLOAT const         *lo = Prob->lo ;
    PPFLOAT const         *hi = Prob->hi ;
    PPFLOAT const          *y = Prob->y ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const          ni = Prob->ni ;
    PPINT   const         ni1 = ni + 1 ;
    PPINT   const         ni2 = ni + 2 ;
    PPINT   const   *ineq_row = Prob->ineq_row ;
    PPFLOAT const         *bl = Prob->bl ;
    PPFLOAT const         *bu = Prob->bu ;
    int     const *sol_to_blk = W->sol_to_blk ;
    PPFLOAT const       sigma = W->sigma ;
    int     const    loExists = I->Work->loExists ;
    int     const    hiExists = I->Work->hiExists ;

    /* Transpose of A */
    PPINT   const *ATp = W->ATp ;
    PPINT   const *ATi = W->ATi ;
    PPFLOAT const *ATx = W->ATx ;

    /* Transpose of AF */
    AFTp = W->AFTp ;
    AFTnz = W->AFTnz ;
    AFTi = W->AFTi ;
    AFTx = W->AFTx ;

    /* Links point to active rows */
    RLinkUp = W->RLinkUp ;
    RLinkDn = W->RLinkDn ;

    /* Links point to active singletons. lLinkUp points to the strict
       inequalities at their lower bound bl_i while uLinkUp points to the
       strict inequalities at their upper bound bu_i. Since only one
       of these can hold for each i, lLinkUp and uLinkUp can be stored
       in the same array */
    lLinkUp = W->SLinkUp ; 
    lLinkDn = W->SLinkDn ;
    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;

    /* working arrays */
    x = W->x ;
    ib = W->ib ;
    ir = W->ir ;
    b = W->b ; /* the part of grad L (lambda) associated with bound variables */
    c = W->c ; /* y + A'lambda */
    F = W->F ;
    D = W->D ;

    nrowadd = W->nrowadd ;
    ncoladd = W->ncoladd ;
    nrowdel = W->nrowdel ;
    ncoldel = W->ncoldel ;

    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;

    /* initializations */
    /* ir [row] = 0         for an equality constraint
                =  strict # for an active inequality at upper bound
                = -strict # for an active inequality at lower bound
                =  strict # + ni for a dropped constraint */


    /* ---------------------------------------------------------------------- */
    /* Check that starting guess is feasible. If not, adjust lambda to make
       it feasible. Set b[row] = 0 if constraint inactive, b[row] = bl [row] if
       constraint at lower bound, b[row] = bu[row] if constraint at upper bound.
       Also, ir [row] = i, -i, or i+ni if ith strict constraint is at upper
       bound, at lower bound, or is inactive.  */
    /* ---------------------------------------------------------------------- */
    /* Throughout this routine lambda = W->lambda if shift_l = 0, while
       lambda = W->shift_l otherwise */
    lambda = W->shift_l ;
    if ( W->shiftl_is_zero == TRUE )
    {
        lambda = W->lambda ;
    }

    /* Cycle over the inequalities and make sure that the starting guess
       is feasible. */
    for (i = 1; i <= ni; i++)
    {
        row = ineq_row [i] ;
        t = lambda [row] ;
        /* if lambda infeasible, set it to zero and drop the row */
        if (  (t == PPZERO)                       ||
             ((t > PPZERO) && (bl [i] == -PPINF)) ||
             ((t < PPZERO) && (bu [i] ==  PPINF)) )
        {
            b [row] = PPZERO ;
            if ( t != PPZERO )
            {
                t = lambda [row] = W->shift_l [row] = PPZERO ;
            }
            if ( ir [row] <= ni ) /* row is currently active, drop it */
            {
                ir [row] = i + ni ;
                k = RowmodFlag [row] ;
                if ( k == EMPTY ) /* put row in the delete list */
                {
/*printf("put row %i (%i) in delete list\n", row, i) ;*/
                    RowmodList [nrowdel] = row ;
                    RowmodFlag [row] = nrowdel ;
                    nrowdel++ ;
                }
                else /* row in the to-add list, remove it from the add list */
                {
/*printf("row %i (%i) in add list, remove it\n", row, i) ;*/
                    l = RowmodList [nrow-nrowadd] ;
                    RowmodList [k] = l ;
                    RowmodFlag [l] = k ;
                    RowmodFlag [row] = EMPTY ;
                    nrowadd-- ; /* one less row to add */
                }
            }
            else /* row continues to be inactive */
            {
                ir [row] = i + ni ;
            }
        }
        else /* t != 0 and a bound is active */
        {
            if ( t > PPZERO ) /* at lower bound */
            {
                b [row] = bl [i] ;
                iri = -i ;
            }
            else              /* at upper bound */
            {
                b [row] = bu [i] ;
                iri = i ;
            }
            if ( ir [row] > ni ) /* row currently dropped */
            {
                /* if the row not in the modify list, then add it */
                if ( RowmodFlag [row] == EMPTY )
                {
                    nrowadd++ ;
                    RowmodList [nrow-nrowadd] = row ;
                    RowmodFlag [row] = nrow-nrowadd ;
                }
                else /* do not delete row, it is already in factor */
                {
                    l = RowmodFlag [row] ;
                    nrowdel-- ;
                    m = RowmodList [nrowdel] ;
                    RowmodList [l] = m ;
                    RowmodFlag [m] = l ;
                    RowmodFlag [row] = EMPTY ;
                }
            }
            ir [row] = iri ;
        }
    }

    /* evaluate: c = y + A'lambda */
    pproj_copyx (c, y, ncol) ;
    for (i = 0; i < nrow; i++)
    {
        if ( (t = lambda [i]) != PPZERO )
        {
            q = ATp [i+1] ;
            for (p = ATp [i]; p < q; p++)
            {
                c [ATi [p]] += t*ATx [p] ;
            }
        }
    }

    /* evaluate:
                 b - A_B*x_B - A_F*x_F
                 ib [j] = +1 if x_j at upper bound
                 ib [j] = -1 if x_j at lower bound
                 ib [j] =  0 if x_j is free
                 AFT, diag of AF*AF', F, absAx */
    Annz = 0 ; /* number of nonzeros in active rows and free columns of A */
    nf = 0 ;
    p = 0 ;
    s = PPZERO ; /* stores 1-norm of x */
    absAx = W->arrayd ; /* for sum_j |a_{ij} x_j| */
    pproj_initx (absAx, PPZERO, nrow) ;
    pproj_initi (AFTnz, (PPINT) 0, nrow) ;
    pproj_initx (D, sigma, nrow) ;
    for (j = 0; j < ncol; j++)
    {
        PPFLOAT u ;
        u = c [j] ;

        PPFLOAT const loj = (loExists) ? lo [j] : -PPINF ;
        PPFLOAT const hij = (hiExists) ? hi [j] :  PPINF ;

        if ( (u > hij) || (u < loj) ) /* xj at a bound */
        {
            if ( !ib [j] ) /* ibj = 0, xj was previously free, now it is bound*/
            {
                if ( ColmodFlag [j] == EMPTY ) /* add to bound list */
                {
                    ncoldel++ ;
                    ColmodList [ncol-ncoldel] = j ;
                    ColmodFlag [j] = ncol-ncoldel ;
                }
                else /* do not bind column, it is not included in factor */
                {
                    l = ColmodFlag [j] ;
                    ncoladd-- ;
                    m = ColmodList [ncoladd] ;
                    ColmodList [l] = m ;
                    ColmodFlag [m] = l ;
                    ColmodFlag [j] = EMPTY ;
                    /* else j was in the list to delete, do nothing */
                }
            }
            if ( u > hij )
            {
                ib [j] = 1 ;
                c [j] = u - hij ;
                u = hij ;
                W->hi [j] = PPZERO ;
                if ( loExists == TRUE )
                {
                    W->lo [j] = loj - u ;
                }
            }
            else
            {
                ib [j] = -1 ;
                c [j] = u - loj ;
                u = loj ;
                W->lo [j] = PPZERO ;
                if ( hiExists == TRUE )
                {
                    W->hi [j] = hij - u ;
                }
            }
            if ( u != PPZERO )
            {
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    PPINT ai ;
                    PPFLOAT v ;
                    ai = Ai [p] ;
                    v = u*Ax [p] ;
                    b [ai] -= v ; 
                    absAx [ai] += fabs (v) ;
                }
            }
        }
        else /* xj is free */
        {
            if ( ib [j] ) /* xj was previously bound */
            {
                k = ColmodFlag [j] ;
                /*If j is neither scheduled to be free or bound, then free it.*/
                if ( k == EMPTY )
                {
                    ColmodList [ncoladd] = j ;
                    ColmodFlag [j] = ncoladd ;
                    ncoladd++ ;
                }
                else /* j was previously free, remove it from the bind list */
                {
                    l = ColmodList [ncol-ncoldel] ;
                    ColmodList [k] = l ;
                    ColmodFlag [l] = k ;
                    ColmodFlag [j] = EMPTY ;
                    ncoldel-- ;
                }
            }
            ib [j] = 0 ;
            c [j] = PPZERO ;
            if ( loExists == TRUE )
            {
                W->lo [j] = lo [j] - u ;
            }
            if ( hiExists == TRUE )
            {
                W->hi [j] = hi [j] - u ;
            }
            F [nf++] = j ;
            q = Ap [j+1] ;
            for (p = Ap [j]; p < q; p++)
            {
                PPINT ai ;
                PPFLOAT ax, v ;
                ai = Ai [p] ;
                ax = Ax [p] ;
                v = u*ax ;
                b [ai] -= v ; 
                if ( ir [ai] <= ni ) /* active row */
                {
                    Annz++ ;
                    D [ai] += ax*ax ;
                    absAx [ai] += fabs (ax*u) ;
                    k = AFTp [ai] + AFTnz [ai]++ ;
                    AFTi [k] = j ;
                    AFTx [k] = ax ;
                }
            }
        }
        x [j] = u ;
        s += fabs (u) ; /* 1-norm of x */
    }
    W->nf = nf ;    /* return number of free indices */
    W->normx = s ;  /* L1 norm of x */
    /* compute max (absAx) for the active constraints */
    W->absAx = pproj_max (absAx, nrow) ;

    /* Set up the row links and check whether an inactive row should be
       activated at an upper or lower bound. Estimate dual error. */
    if ( ni == 0 )                /* no strict inequalities */
    {
        errdual = pproj_max (b, nrow) ;
        nactive = nrow ;
        ATnz = ATp [nrow] ;
        if ( W->shiftl_is_zero == TRUE )
        {
            pproj_saxpy (b, lambda, -sigma, nrow) ;
        }
    }
    else                          /* there are strict inequalities */
    {
        ATnz = 0 ; /* number of nonzeros in active rows of full matrix */
        nactive = 0 ; /* number of active rows */
        Ll = ni1 ;
        Ul = ni2 ;
        Rl = nrow ;
        errdual = PPZERO ;
        for (i = 0; i < nrow; i++)
        {
            k = ir [i] ;
            if ( k <= ni )        /* row is active */
            {
                nactive++ ;
                ATnz += ATp [i+1] - ATp [i] ;
                if ( errdual < fabs (b [i]) )
                {
                    errdual = fabs (b [i]) ;
                }
                if ( W->shiftl_is_zero == TRUE )
                {
                    b [i] -= sigma*lambda [i] ;
                }
                RLinkDn [i] = Rl ;
                RLinkUp [Rl] = i ;
                Rl = i ;
                if ( k < 0 )      /* strict inequality at lower bound */
                {
                    k = -k ;
                    lLinkDn [k] = Ll ;
                    lLinkUp [Ll] = k ;
                    Ll = k ;
                }
                else if ( k > 0 ) /* strict inequality at upper bound */
                {
                    uLinkDn [k] = Ul ;
                    uLinkUp [Ul] = k ;
                    Ul = k ;
                }
            }
            else /* row is dropped, it can effect absAx and errdual */
            {
                k -= ni ; /* k = ineqindex */
                bi = b [i] ;
                /* first compute dual derivative without the prox term and
                   update sup-norm of dual gradient */
                if ( (t = bl [k] + bi) > PPZERO )
                {
                    if ( errdual < t )
                    {
                        errdual = t ;
                    }
                }
                else if ( (t = bu [k] + bi) < PPZERO )
                {
                    if ( errdual < -t )
                    {
                        errdual = -t ;
                    }
                }
                
                /* when activating constraints, also need to take into
                   account the proximal term */
                if ( W->shiftl_is_zero == TRUE )
                {
                    /* adjust b for proximal term */
                    bi -= sigma*lambda [i] ;
                }
    
                /* check if lambda_i > 0 increases dual */
                if ( (t = bl [k] + bi) > PPZERO )
                {
                    /* activate lower bound */
                    b [i] = t ;
                    ir [i] = -k ;
                    lLinkDn [k] = Ll ;
                    lLinkUp [Ll] = k ;
                    Ll = k ;
                }
                /* check if lambda_i < 0 increases dual */
                else if ( (t = bu [k] + bi) < PPZERO )
                {
                    /* activate upper bound */
                    b [i] = t ;
                    ir [i] = k ;
                    uLinkDn [k] = Ul ;
                    uLinkUp [Ul] = k ;
                    Ul = k ;
                }
                else /* remains inactive */
                {
                    b [i] = bi ;
                }
                if ( ir [i] <= ni ) /* the constraint is active */
                {
                    nactive++ ;
                    ATnz += ATp [i+1] - ATp [i] ;
                    RLinkDn [i] = Rl ;
                    RLinkUp [Rl] = i ;
                    Rl = i ;
                    l = RowmodFlag [i] ;
                    /* if row missing from factor, add it */
                    if ( l == EMPTY )
                    {
                        nrowadd++ ;
                        RowmodList [nrow-nrowadd] = i ;
                        RowmodFlag [i] = nrow-nrowadd ;
                    }
                    else /* remove row from delete list */
                    {
                        nrowdel-- ;
                        m = RowmodList [nrowdel] ;
                        RowmodList [l] = m ;
                        RowmodFlag [m] = l ;
                        RowmodFlag [i] = EMPTY ;
                    }
                    s = PPZERO ;
                    t = PPZERO ;
                    q = ATp [i+1] ;
                    p = ATp [i] ;
                    l = AFTp [i] ;
                    for (; p < q; p++)
                    {
                        PPFLOAT ax ;
                        ax = ATx [p] ;
                        j = ATi [p] ;
                        if ( !ib [j] ) /* the column is free */
                        {
                            PPFLOAT u ;
                            Annz++ ;
                            t += ax*ax ;
                            AFTx [l] = ax ;
                            AFTi [l] = j ;
                            l++ ;
                            u = fabs (y [j]) + fabs (y [j] - x [j]) ;
                            s += fabs (u*ax) ;
                        }
                        else
                        {
                            s += fabs (x [j]*ax) ;
                        }
                    }
                    D [i] += t ;            /* new diagonal element for SSOR */
                    m =  l - AFTp [i] ;
                    AFTnz [i] = m ;
                    if ( W->absAx < s )
                    {
                        W->absAx = s ;
                    }
                }
                else  /* constraint is inactive */
                {
                    W->shift_l [i] = PPZERO ;
                }
            }
        }
        /* close the linked lists */
        lLinkUp [Ll] = ni1 ;
        uLinkUp [Ul] = ni2 ;
        lLinkDn [ni1] = Ll ;
        uLinkDn [ni2] = Ul ;
        RLinkDn [nrow] = Rl ;
        RLinkUp [Rl] = nrow ;
    }

    W->nrowadd = nrowadd ;
    W->ncoladd = ncoladd ;
    W->nrowdel = nrowdel ;
    W->ncoldel = ncoldel ;

    /* in SpaRSA, only monitor undecided index set when gradient <= grad0 */
    W->grad0 = errdual*Parm->grad_decay ;

    if ( W->absAx == PPZERO )
    {
        W->absAx = PPONE ;
    }

    if ( Parm->stop_condition == 0 )
    {
        errdual /= (W->absAx+W->absAxk) ;
    }
    else if ( Parm->stop_condition == 2 )
    {
        errdual /= (W->absAx + W->ymax) ;
    }
    if ( PrintLevel > 0 )
    {
        printf ("hotchol errdual: %e absAx: %e absAxk: %e\n",
                 errdual, W->absAx, W->absAxk) ;
    }

    if ( errdual <= Parm->grad_tol )
    {
        if ( (Parm->getfactor == FALSE) ||
             (nrowadd + nrowdel + ncoladd + ncoldel == 0) )
        {
            if ( PrintLevel > 0 )
            {
                printf ("!!##xx fast return xx##!!\n") ;
            }

            W->stop_in_hotchol = TRUE ; /* no change in the factorization */
            Stat->errdual = errdual ;
            return (PPROJ_SOLUTION_FOUND) ;
        }
    }

    /* In the case where lambda is nonzero and shift_l is zero, b is
       modified by the proximal term. */
    pproj_initx (W->dlambda, PPZERO, nrow) ;

#ifndef NDEBUG
    /* save dual objective but do not check for increase */
    pproj_check_dual (I, NULL, "at hotchol & initial dual value",
                      TRUE, FALSE);
#endif

    if ( !Parm->cholmod ) /* return if purely iterative method is used */
    {
        pproj_copyx (W->lambda_tot, lambda, nrow) ;
        return (PPROJ_TOLERANCE_NOT_MET) ;
    }

    /* otherwise update/downdate is used */
    {
        int blk, blk1, blks, prevblk ;
        PPINT *lstart, *ustart, *sol_start ;

        W->ATnz = ATnz ;
        W->Annz = Annz ;
        W->nactive = nactive ;
        sol_start = W->sol_start ;
        sol_to_blk = W->sol_to_blk ;
        /* sol_start [k] = first singleton (strict inequality) associated
                           with block k */
        j = 1 ;
        blk1 = sol_to_blk [j] ;
        blk = 0 ;
        /* set sol_start to 1 for all block before first inequality */
        while ( blk < blk1 )
        {
            sol_start [blk] = j ;
            blk++ ;
        }
        blks = W->blks ;

        while ( blk < blks )
        {
            /* blk1 = sol_to_blk [j], j = first strict inequality in block */
            sol_start [blk1] = j ;
            j++ ;
            /* find the first row in the next block */
            while ( sol_to_blk [j] <= blk1 )
            {
                j++ ;
            }
            /* store the block associated with the first row */
            blk1 = sol_to_blk [j] ;
            /* set the start of all blocks before this new block to j */
            while ( blk < blk1 )
            {
                blk++ ;
                sol_start [blk] = j ;
            }
        }
        sol_start [blk] = ni + 1 ;

        lstart = W->lstart ;
        ustart = W->ustart ;

        /* lstart and ustart are associated with the inequalities that are
           strict.  For each block in the multilevel decomposition,
           lstart points to the first singleton at its lower bound while ustart
           points to the first singleton at it upper bound */
        for (blk = 0; blk < blks; blk++)
        {
            lstart [blk] = ni1 ;
            ustart [blk] = ni2 ;
        }

        prevblk = EMPTY ;
        for (j = lLinkUp [ni1]; j <= ni; j = lLinkUp [j])
        {
            blk = sol_to_blk [j] ;
            if ( blk > prevblk )
            {
                lstart [blk] = j ;
                prevblk = blk ;
            }
        }

        prevblk = EMPTY ;
        for (j = uLinkUp [ni2]; j <= ni; j = uLinkUp [j])
        {
            blk = sol_to_blk [j] ;
            if ( blk > prevblk )
            {
                ustart [blk] = j ;
                prevblk = blk ;
            }
        }

#ifndef NDEBUG
        where = "at tail of hotchol" ;
        pproj_check_AT (I, where) ;
        pproj_check_AFT (I, TRUE, where) ; /* TRUE: skip deleted rows */
        pproj_checkb (I, where) ;
        pproj_checkc (I, where) ;
        /* check that dual objective increases */
        pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
        pproj_check_link (I, (int *) NULL, 0, where) ;
#endif
    }

#ifndef NDEBUG
    if ( PrintLevel > 0 )
    {
        PRINTF("hotchol complete\n") ;
    }
    where = "end of hotchol" ;
    pproj_checkb (I, where) ;
#endif

    return (PPROJ_TOLERANCE_NOT_MET) ;
}
