/* =========================================================================
   ============================== pproj_coor_ascent ========================
   =========================================================================
    Apply one iteration of coordinate ascent to the dual function.
    This is mainly used to handle the situation where all the variables
    associated with nonzeros in a row of A are bound. In this case, the
    corresponding row of AF*AF' vanishes and the dual function depends
    linearly on the multiplier associated with this row. The code is
    very similar to the dual coordinate ascent scheme appearing in the
    top half of phase1. The main differences are the following:

        1. In coor_ascent, we determine the number of active rows in A
           (this is used to decide whether to perform ssor0 or ssor1).
        2. In coor_ascent, we save the rowmod and colmod list for the
           update/downdate routines.
        3. In coor_ascent, the bounds are always 0 due to the x-translation
           described in the code pproj.c
        4. In coor_ascent, we only evaluate elements of D or
           AFT for active rows.
   ========================================================================== */
#include "pproj.h"

void pproj_coor_ascent
(
    PPcom *I
)
{
    int     blk, *ib ;
    PPINT   i, j, k, l, kk, p, p1, q, row,
            ncoladd, ncoldel, nrowadd, nrowdel, coor_ascent_drop,
            maxrow, brk, nbrk, nf, ineqflag,
           *AFTi, *AFTnz, *AFTp,
           *Br_index, *Br_order, *F, *RLinkDn, *RLinkUp,
           *uLinkUp, *uLinkDn, *lLinkUp, *lLinkDn, *lstart, *ustart,
           *ir, *worki, *iwork,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList ;

    PPFLOAT Br, ax, s, t, st, st0, fd, fd0, fn, sd, tic,
           *AFTx, *b, *c, *lambda,
           *shift_l, *Br_value, *D, *workd ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;

    tic = pproj_timer () ;

    /* extract the problem, statistics, and work structures from I */
    Prob = I->Prob ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    W = I->Work ;

    int     const  PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 2 )
    {
        printf ("start coor_ascent\n") ;
    }

    /* Problem data */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPFLOAT const      *singc = Prob->singc ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const          ni = Prob->ni ;
    PPINT   const       nsing = Prob->nsing ;
    PPINT   const     nsingni = nsing + ni ;
    PPFLOAT const         *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const         *bu = (nsing) ? Prob->singhi : Prob->bu ;
    int     const *sol_to_blk = W->sol_to_blk ;
    PPINT                *slo = W->slo ;
    PPINT                *shi = W->shi ;

    PPFLOAT const       sigma = W->sigma ;
    int     const       debug = Parm->debug ;

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
       inequalities with b_i = bl_i while uLinkUp points to the strict
       inequalities with b_i = bu_i. Since only one of these can hold for
       each i, lLinkUp and uLinkUp can be stored in the same array */
    lLinkUp = W->SLinkUp ; 
    lLinkDn = W->SLinkDn ;
    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;

    lstart = W->lstart ;
    ustart = W->ustart ;

    /* working arrays */
    lambda  = W->lambda ;
    shift_l = W->shift_l ;
    ib      = W->ib ;
    ir      = W->ir ;
    b       = W->b ;         /* part of grad L associated with bound variables*/
    c       = W->c ;         /* y + A'lambda */
    maxrow  = Prob->maxrow ; /* max number of nonzeros in a row of A */
    F       = W->F ;
    nf      = W->nf ;
    D       = W->D ;
   
    /* ======== start allocations ========
    -> work arrays in coordinate ascent step
 
       Br_index  - INT maxrow
       Br_order  - INT maxrow
       iwork     - INT maxrow
       Br_value  - double maxrow (maxrow <= ncol) */

    /* coordinate ascent step before ssor step */
    worki = W->arrayi ;
    Br_index  = worki ; worki += maxrow ;
    Br_order  = worki ; worki += maxrow ;
    iwork     = worki ; worki += maxrow ;

    workd    = W->arrayd ;
    Br_value = workd ; workd += maxrow ;
    /* ======== end of allocations ======== */

    /* some parameters */
    ncoladd    = W->ncoladd ;
    ncoldel    = W->ncoldel ;
    nrowadd    = W->nrowadd ;
    nrowdel    = W->nrowdel ;
    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;
    coor_ascent_drop = Stat->coor_ascent_drop ;

    for (row = RLinkUp [nrow]; row < nrow; row = RLinkUp [row])
    {
        fd = b [row] ; /* b includes the sigma*lambda term */
        ASSERT (ir [row] <= nsingni) ;
        PPINT const ir_row = ir [row] ;

        p = AFTp [row] ;
        p1 = p + AFTnz [row] ;
        for (; p < p1; p++)
        {
            fd -= c [AFTi [p]]*AFTx [p] ;
        }

        /* -------------------------------------------------------------- */
        /* Evaluate break points as we search in direction of + deriv. */
        /* -------------------------------------------------------------- */

        nbrk = 0 ;
        fd0 = fd ;
        sd = D [row] ;

        st = fd/sd ;
        ineqflag = 0 ;

        fd = fabs (fd) ;

        if ( fd0 > PPZERO ) /* lambda [row] increases */
        {
            if ( ni )
            {
                /* ir_row > 0 => current lambda < 0 and row may drop when
                   lambda grows */
                if ( ir_row > 0 )
                {
                    if ( W->shiftl_is_zero )
                    {
                        t = -lambda [row] ;
                    }
                    else
                    {
                        t = -(lambda [row] + shift_l [row]) ;
                    }
                    if ( t < st )
                    {
                        ineqflag = ir_row ;
                        st = t ;
                    }
                }
            }
            else if ( ir_row ) /* the row contains singletons, all at bounds */
            {
                /* when lambda increase, hi could switch to lo */
                if ( j = shi [row] ) /* lambda < max singc*/
                {
                    if ( W->shiftl_is_zero )
                    {
                        t = singc [j] - lambda [row] ;
                    }
                    else
                    {
                        t = singc [j] - (lambda [row] + shift_l [row]) ;
                    }
                    if ( t < st )
                    {
                        ineqflag = j ;
                        st = t ;
                    }
                }
            }
            st0 = st ;
 
            /* find all break points < st */
            q = ATp [row+1] ;
            for (p = ATp [row] ; p < q; p++)
            {
                j = ATi [p] ;
                if ( ib [j] )
                {
                    ax = ATx [p] ;
                    if ( ax  > PPZERO )
                    {
                        if ( ib [j] < 0 )
                        {
                            t = -c [j]/ax ;
                            if ( t < st )
                            {
                                Br_value [nbrk] = t ;
                                Br_index [nbrk] = p ;
                                nbrk++ ;
                            }
                        }
                    }
                    else
                    {
                        if ( ib [j] > 0 )
                        {
                            t = -c [j]/ax ;
                            if ( t < st )
                            {
                                Br_value [nbrk] = t ;
                                Br_index [nbrk] = p ;
                                nbrk++ ;
                            }
                        }
                    }
                }
            }
        }
        else if ( fd0 < PPZERO ) /* lambda [row] decreases */
        {
            if ( ni )
            {
                /* ir_row < 0 => current lambda > 0 and row may drop
                   when lambda decreases due to fd0 < 0 */
                if ( ir_row < 0 )
                {
                    if ( W->shiftl_is_zero )
                    {
                        t = -lambda [row] ;
                    }
                    else
                    {
                        t = -(lambda [row] + shift_l [row]) ;
                    }
                    if ( t > st )
                    {
                        ineqflag = ir_row ;
                        st = t ;
                    }
                }
            }
            else if ( ir_row ) /* the row contains singletons, all at bounds */
            {
                /* when lambda decreases, lo could switch to hi */
                if ( j = slo [row] ) /* lambda < max singc*/
                {
                    if ( W->shiftl_is_zero )
                    {
                        t = singc [j] - lambda [row] ;
                    }
                    else
                    {
                        t = singc [j] - (lambda [row] + shift_l [row]) ;
                    }
                    if ( t > st )
                    {
                        ineqflag = -j ;
                        st = t ;
                    }
                }
            }
            st0 = st = -st ;

            /* find all break points < st */
            q = ATp [row+1] ;
            for (p = ATp [row] ; p < q; p++)
            {
                j = ATi [p] ;
                if ( ib [j] )
                {
                    ax = ATx [p] ;
                    if ( ax > PPZERO )
                    {
                        if ( ib [j] > 0 )
                        {
                            t = c [j]/ax ;
                            if ( t < st )
                            {
                                Br_value [nbrk] = t ;
                                Br_index [nbrk] = p ;
                                nbrk++ ;
                            }
                        }
                    }
                    else
                    {
                        if ( ib [j] < 0 )
                        {
                            t = c [j]/ax ;
                            if ( t < st )
                            {
                                Br_value [nbrk] = t ;
                                Br_index [nbrk] = p ;
                                nbrk++ ;
                            }
                        }
                    }
                } /* bound variable, check for break */
            }     /* end of loop over the row */
        }         /* find breaks */

        if ( nbrk > 0 )
        {
            pproj_xminsort (Br_order, Br_value, iwork, nbrk) ;

#ifndef NDEBUG
            if ( debug > 1 )
            {
                pproj_check_order (Br_value, Br_order, nbrk,
                             "in coordinate ascent in DASA") ;
            }
#endif

            st = 0 ;
            for (brk = 0; brk < nbrk; brk++)
            {
                kk = Br_order [brk] ;
                Br = PPMAX (PPZERO, Br_value [kk]) ;
                fn = fd - sd * (Br - st) ;
                p = Br_index [kk] ;
                s = ATx [p] ;
                j = ATi [p] ;

                if ( fn <= PPZERO )
                {
                    if ( fd != fn )
                    {
                        st += (fd/(fd-fn))*(Br - st);
                        fd = PPZERO ;
                    }
                    break ;
                }
                else
                {
                    fd = fn ;
                }

                /* x_j changes from bound to free */
                p1 = Ap [j+1] ;
                for (p = Ap [j]; p < p1; p++)
                {
                    i = Ai [p] ;
                    if ( ir [i] <= nsingni )
                    {
                        ax = Ax [p] ;
                        D [i] += ax*ax ;
                        l = AFTp [i] + AFTnz [i]++ ;
                        AFTx [l] = ax ;
                        AFTi [l] = j ;
                    }
                }
                sd += s*s ;

#ifndef NDEBUG
                if ( PrintLevel > 2 )
                {
                    if ( ib [j] > 0 )
                    {
                        PRINTF("row: %ld free: %ld hi: %e\n",
                               (LONG) row, (LONG) j, W->hi [j]);
                    }
                    else
                    {
                        PRINTF("row: %ld free: %ld lo: %e\n",
                               (LONG) row, (LONG) j, W->lo [j]);
                    }
                }
#endif

                ib [j] = 0 ;
                F [nf++] = j ;
                st = Br ;
                k = ColmodFlag [j] ;
                if ( k != EMPTY )
                {
                    l = ColmodList [ncol-ncoldel] ;
                    ColmodList [k] = l ;
                    ColmodFlag [l] = k ;
                    ColmodFlag [j] = EMPTY ;
                    ncoldel-- ;
                }
                else
                {
                    ColmodList [ncoladd] = j ;
                    ColmodFlag [j] = ncoladd ;
                    ncoladd++ ;
                }
            }

            st += fd/sd ;

            if ( st >= st0 )
            {
                st = st0 ;
            }
            else
            {
                ineqflag = 0 ; /* the row did not drop */
            }
        }

        if ( fd0 < 0 )
        {
            st = -st ;
        }

        if ( ineqflag ) /* drop row */
        {
            Stat->coor_ascent_drop++ ;
            k = RLinkDn [row] ;
            j = RLinkUp [k] = RLinkUp [row] ;
            RLinkDn [j] = k ;
            ASSERT (ir [row] <= nsingni) ;

            if ( ineqflag > 0 ) /* remove from uLink */
            {
                k = uLinkDn [ineqflag] ;
                j = uLinkUp [k] = uLinkUp [ineqflag] ;
                uLinkDn [j] = k ;
                b [row] -= bu [ineqflag] ;
                if ( Parm->cholmod == TRUE )
                {
                    blk = sol_to_blk [ineqflag] ;
                    if ( ineqflag == ustart [blk] )
                    {
                        ustart [blk] = j ;
                    }
                }
                if ( nsing )
                {
                    lambda [row] = singc [ineqflag] - shift_l [row] ;
                    shi [row] = 0 ;
                    /* also remove from lLink is it exists */
                    j = slo [row] ;
                    if ( j )
                    {
                        slo [row] = 0 ;
                        k = lLinkDn [j] ;
                        l = lLinkUp [k] = lLinkUp [j] ;
                        lLinkDn [l] = k ;
                        if ( Parm->cholmod == TRUE )
                        {
                            if ( j == lstart [blk] )
                            {
                                lstart [blk] = l ;
                            }
                        }
                    }
                }
                else /* ni */
                {
                    lambda [row] = -shift_l [row] ;
                }
            }
            else                /* remove from lLink */
            {
                ineqflag = -ineqflag ;
                k = lLinkDn [ineqflag] ;
                j = lLinkUp [k] = lLinkUp [ineqflag] ;
                lLinkDn [j] = k ;
                b [row] -= bl [ineqflag] ;
                if ( Parm->cholmod == TRUE )
                {
                    blk = sol_to_blk [ineqflag] ;
                    if ( ineqflag == lstart [blk] )
                    {
                        lstart [blk] = j ;
                    }
                }
                if ( nsing )
                {
                    lambda [row] = singc [ineqflag] - shift_l [row] ;
                    slo [row] = 0 ;
                    /* also remove from uLink is it exists */
                    j = shi [row] ;
                    if ( j )
                    {
                        shi [row] = 0 ;
                        k = uLinkDn [j] ;
                        l = uLinkUp [k] = uLinkUp [j] ;
                        uLinkDn [l] = k ;
                        if ( Parm->cholmod == TRUE )
                        {
                            if ( j == ustart [blk] )
                            {
                                ustart [blk] = l ;
                            }
                        }
                    }
                }
                else /* ni */
                {
                    lambda [row] = -shift_l [row] ;
                }
            }

            k = RowmodFlag [row] ;
            if ( k != EMPTY ) /* the row was set to be added, remove it */
            {
                AFTnz [row] = 0 ;
                /* move last added row to replace new dropped row */
                l = RowmodList [nrow-nrowadd] ;
                RowmodList [k] = l ;
                RowmodFlag [l] = k ;
                RowmodFlag [row] = EMPTY ;
                nrowadd-- ; /* one less row to add */
            }
            else /* add row to the delete list */
            {
                RowmodList [nrowdel] = row ;
                RowmodFlag [row] = nrowdel ;
                nrowdel++ ;
            }
            ir [row] = ineqflag + nsingni ;  /* Drop row */

#ifndef NDEBUG
            if ( PrintLevel > 2 )
            {
                PRINTF ("dasa coordinate ascent drop row: %ld", (LONG) row) ;
                PRINTF (" inequality index: %ld\n", (LONG) ineqflag) ;
            }
#endif
        }                /* end of row drop */
        else
        {
            lambda [row] += st ;
        }
        if ( st != PPZERO )
        {
            b [row] -= sigma*st ;
            q = ATp [row+1] ;
            for (p = ATp [row] ; p < q; p++)
            {
                c [ATi [p]] += ATx [p]*st ;
            }
        }
    } /* end of coordinate ascent iteration */
#ifndef NDEBUG
    pproj_check_dual (I, NULL, "end of dasa coordinate ascent", TRUE, TRUE) ;
#endif

    W->ncoladd = ncoladd ;
    W->ncoldel = ncoldel ;
    W->nrowadd = nrowadd ;
    W->nrowdel = nrowdel ;
    k = nf - W->nf ;
    W->nf = nf ;
    Stat->coor_ascent_free += k ;
    W->chg_coor = k + (Stat->coor_ascent_drop - coor_ascent_drop) ;
    Stat->coor_ascent_its++ ;
    Stat->coor_ascent += pproj_timer () - tic ;
}
