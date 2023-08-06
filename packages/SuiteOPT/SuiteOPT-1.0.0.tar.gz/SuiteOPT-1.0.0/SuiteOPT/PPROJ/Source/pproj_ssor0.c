/* ========================================================================= */
/* === pproj_ssor0 ========================================================= */
/* ========================================================================= */

/*
    Apply an SSOR Gauss-Seidel preconditioned gradient ascent iteration to
    the dual problem. The iterate is used to generate a search direction
    along which a line search is performed. If one or more variables is
    freed during the line search, then the iteration continues up to a
    maximum of W->ssor0_max iterations.  The goal in this routine is to
    free as many variables and drop as many rows as possible, while performing
    a relatively cheap gradient ascent iteration. If no variable is freed
    or no rows dropped in an iteration, then it is viewed as too expensive,
    so we terminate. ssor1 performs a preconditioned, limited memory conjugate
    gradient iteration, which has a better convergence rate when the
    active indices are not changing. ssor1 also uses update/downdate
    techniques to account for the effect of changes in the free set on
    the dual objective function.  To explain the SSOR preconditioned
    iteration used in the ssor0 code, consider a quadratic optimization
    problem of the form
 
    max -.5x'Qx + b'x
 
    Substitute x = inv (S)'y where S = (D+L) inv (sqrt(D)) and L+D+L' = Q.
    The gradient of the transformed objective at x_k = inv (S)' y_k is
 
    gbar_k = -inv (S) Q inv (S)'y_k + inv (S) b
 
    In y the steepest ascent iteration is
 
    y_k+1 = y_k + alpha_k gbar_k ,
 
    where alpha_k is chosen to minimize the objective in the search
    direction gbar_k. In x, the corresponding iteration is
 
    x_k+1 = x_k + alpha_k inv (S)' gbar_k
 
          = x_k + alpha_k inv (S)' inv (S) g_k,

          = x_k + alpha_k P g_k,
 
    where
 
    g_k = b - Q x_k is the gradient and P =  inv (S)' inv (S) is
    the preconditioner. Observe that
 
    inv (S)' inv (S) = inv (D+L)' D inv (D+L) .
 
    If d_k =  P g_k is the search direction in x, then
 
    alpha_k = g_k'd_k / d_k' Q d_k.
 
    In our case, Q = A_F A_F' + sigma I. Hence,
 
    alpha_k = g_k'd_k / (||A_F'd_k||^2 + sigma ||d_k||^2).
 
    Due to the special structure of Q, the computation of P g_k and
    A_F'd_k = A_F' P g_k can be substantially streamlined. The relation
    between the variables in the description above and the variables in the
    code below is the following:
 
    fd  = g_k'd_k   (the first  derivative in the search direction)
    sd  = d_k'Qd_k  (the second derivative in the search direction)
    pA  = A'd_k     (product between the search direction dk and A')
 
    Note: Differences between the use of the SSOR preconditioned iteration
          in phase1 and in ssor0 include the following:
 
    1. In phase1 we do a fixed number of iterations while in ssor0 we stop if
       no variables are freed. In phase1 we proceed each ssor preconditioned
       iteration with a dual coordinate ascent iteration. In phase1, we
       bind variables and add rows after each iteration, while in ssor0
       we only free variables and drop rows.  In ssor0 there is
       no dual coordinate ascent iteration, although pproj_dasa could perform
       a dual coordinate ascent iteration before calling ssor.
 
    2. Since ssor0 only frees variables, we record the bound variables
       at the start, and in the line search, we only check these variables
       to see if any became free. In phase1, variables are both free and
       bound in each iteration, so we do not store a bound list.
 
    3. In ssor0 we keep track of freed variables and dropped rows since this
       information is needed for the updates and downdates. We also keep
       track of the first variable in a block. These operations involve a
       small unnecessary overhead in the event that updates and downdates are
       not performed or the multilevel scheme is not used.
 
    4. In ssor0 the active bounds are zero due to the transformation
       previously performed, either at the end of phase1 or in the
       check error routine. This transformation is explained in the
       comments provided in the pproj code. In phase1 the active bounds
       are given by their values in lo and hi.
*/

#include "pproj.h"

void pproj_ssor0
(
    PPcom *I
)
{
    int     blk, lineflag, ibj, *ib ;
    PPINT   it, i, j, k, first, last, nup, chg, l, m, p, p1, q, col,
            nbrk, nb, nf, nrowdel, nrowadd, ncoladd, ncoldel,
           *AFTi, *AFTnz, *AFTp, *Heap, *F, *bound, *RLinkDn, *RLinkUp,
           *uLinkUp, *uLinkDn, *lLinkUp, *lLinkDn, *lstart, *ustart,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList,
           *ir, *ns, *worki ;

    PPFLOAT Br, ax, cj,
            s, t, st, st0, fd, fn, sd, tic, dknew, snew,
           *AFTx, *b, *c, *lambda, *shift_l,
           *Br_value, *D, *dk, *pA, *gk, *workd ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;

    tic = pproj_timer () ;

#ifndef NDEBUG
    char   *where ;
    I->Check->location = 3 ; /* code operates in ssor0 */
#endif

    /* extract the problem, statistics, and work structures from I */
    Prob = I->Prob ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    W = I->Work ;

    int const PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 2 )
    {
        printf ("start ssor0\n") ;
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
    PPINT   const    nsingni  = nsing + ni ;
    PPINT   const    nsingni1 = nsingni + 1 ;
    PPINT   const    nsingni2 = nsingni + 2 ;
    PPINT   const        ntot = nsingni1 + ncol ;
    PPINT                *slo = W->slo ;
    PPINT                *shi = W->shi ;
    PPINT   const   *ineq_row = Prob->ineq_row ;
    PPFLOAT const         *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const         *bu = (nsing) ? Prob->singhi : Prob->bu ;
    int     const *sol_to_blk = W->sol_to_blk ; 
    PPFLOAT const       sigma = W->sigma ;

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

    /* working arrays */
    lambda  = W->lambda ;
    shift_l = W->shift_l ;
    ib      = W->ib ;
    ir      = W->ir ;
    b       = W->b ; /* the part of grad L associated with bound variables */
    c       = W->c ; /* y + A'lambda */
    F       = W->F ;
    D       = W->D ;
    ns      = W->ns ;

    nf      = W->nf ;
    nrowdel = W->nrowdel ;
    nrowadd = W->nrowadd ;
    ncoladd = W->ncoladd ;
    ncoldel = W->ncoldel ;
    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;

    lstart = W->lstart ;
    ustart = W->ustart ;

    /* ======== start allocations ========
    -> work arrays in ssor step:

       Heap     - int    ntot, line search
       bound    - int    ncol, line search
       pA       - double ncol, A'lambda
       dk       - double nrow, search direction
       Br_value - double ncol + nsingni + 1
       gk       - double nrow, used in ssor iteration */

    /* ssor step */
    worki = W->arrayi ;
    Heap     = worki ; worki += ntot ;
    bound    = worki ; worki += ncol ;

    workd = W->arrayd ;
    pA       = workd ; workd += ncol ;
    dk       = workd ; workd += nrow ;
    Br_value = workd ; workd += ncol + nsingni1 ;
    gk       = workd ; workd += nrow ; /* grad L (lambda) */

    /* ======== end of allocations ======== */

    nb = 0 ;
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] )
        {
            bound [nb] = j ;
            nb++ ;
        }
    }
    nup = 1 ;
    it = 0 ;
    chg = 0 ; /* count the number of variables freed and rows dropped */

#ifndef NDEBUG
    where = "at very start of ssor0" ;
    pproj_checkF (I, where) ;
    pproj_checkc (I, where) ;
    pproj_checkb (I, where) ;
    pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
    pproj_checkD (I, where) ;
    pproj_check_AT (I, where) ;
    pproj_check_AFT (I, TRUE, where) ;
    pproj_check_link (I, (int *) NULL, 0, where) ;
#endif

    /* nup counts number of freed variables and dropped rows in line search */
    while ( nup > 0 )
    {
        it++ ;
        first = RLinkUp [nrow] ;
        if ( first == nrow ) /* all equations have been dropped */
        {
            break ;
        }

        /* compute objective gradient at the current iterate */
        for (i = first; i < nrow; i = RLinkUp [i])
        {
            t = b [i] ; /* includes -sigma*lambda [i] and bound variables */
            ASSERT (ir [i] <= nsingni) ;
            p = AFTp [i] ;
            q = p + AFTnz [i] ;
            for ( ; p < q ; p++)
            {
                t -= AFTx [p]*c [AFTi [p]] ;
            }
            gk [i] = t ; /* gk = grad L_R (lambda) for active rows */
        }

        pproj_initFx (pA, PPZERO, F, nf) ; /* set pA [F [k]] = 0 */

        i = first ;
        t = dk [i] = gk [i]/D [i] ;

        last = RLinkDn [nrow] ;

        /* compute inv(D+L) * gk (initializations above) */
        while (i < last)
        {

            ASSERT (ir [i] <= nsingni) ;

            p = AFTp [i] ;
            p1 = p + AFTnz [i] ;
            for ( ; p < p1 ; p++)
            {
                pA [AFTi [p]] += AFTx [p]*t ;
            }

            i = RLinkUp [i] ;

            ASSERT (ir [i] <= nsingni) ;

            t = PPZERO ;

            p = AFTp [i] ;
            p1 = p + AFTnz [i] ;
            for ( ; p < p1 ; p++)
            {
                t += AFTx [p]*pA [AFTi [p]] ;
            }
            t = dk [i] = (gk [i] - t)/D [i] ;
        }

        /* start computation of dk and pA = A'*dk */
        pproj_initx (pA, PPZERO, ncol) ;
        fd = t*gk [i] ;
        sd = t*t ;

        for (; i > first;)
        {
            p1 = ATp [i+1] ;
            for (p = ATp [i] ; p < p1 ; p++)
            {
                pA [ATi [p]] += ATx [p]*t ;
            }

            i = RLinkDn [i] ;

            ASSERT (ir [i] <= nsingni) ;

            t = PPZERO ;

            p = AFTp [i] ;
            p1 = p + AFTnz [i] ;
            for ( ; p < p1 ; p++)
            {
                t += AFTx [p]*pA [AFTi [p]] ;
            }
            t = dk [i] = dk [i] - t/D [i] ;
            fd += t*gk [i] ;
            sd += t*t ;
        }

        p1 = ATp [i+1] ;
        for (p = ATp [i] ; p < p1 ; p++)
        {
            pA [ATi [p]] += ATx [p]*t ;
        }
        /* end computation of dk and pA = A'*dk */

        sd *= sigma ;
        for (k = 0; k < nf; k++)
        {
            j = F [k] ;
            sd += pA [j]*pA [j] ;
        }

        if ( sd > PPZERO )
        {
            /* If there are only bounds and no linear inequalities, then
               st0 is an upper bound on the largest possible step size.
               Restricting the break points to be <= st0 reduces the
               number of break points that we need to deal with. */
            st0 = st = fd/sd ;
        }
        else
        {
            st = PPZERO ;
        }
        if ( PrintLevel > 2 )
        {
            printf ("initial ssor st: %25.15e\n", st) ;
        }

        nup = 0 ;
        if ( st != PPZERO )
        {
            nbrk = 0 ;
            for (k = 0; k < nb; k++)
            {
                j = bound [k] ;
                if ( (ibj = ib [j]) < 0 )
                {
                    if ( pA [j] > PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < st )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;        /* add to heap  */
                        }
                    }
                }
                else if ( ibj > 0 )
                {
                    if ( pA [j] < PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < st )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;        /* add to heap */
                        }
                    }
                }
            }

            if ( W->shiftl_is_zero )
            {
                for (j = lLinkUp [nsingni1]; j <= nsingni; j = lLinkUp [j])
                {
                    PPINT const row = ineq_row [j] ;
                    if ( (t = dk [row]) < PPZERO )
                    {
                        /* lambda > 0 for lLinkUp */
                        if ( ni ) s = -lambda [row]/t ;
                        else      s = (singc [j] - lambda [row])/t ;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
                for (j = uLinkUp [nsingni2]; j <= nsingni; j = uLinkUp [j])
                {
                    PPINT const row = ineq_row [j] ;
                    if ( (t = dk [row]) > PPZERO )
                    {
                        /* lambda < 0 for uLinkUp */
                        if ( ni ) s = -lambda [row]/t ;
                        else      s = (singc [j] - lambda [row])/t ;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
            }
            else /* shift_l != 0 */
            {
                for (j = lLinkUp [nsingni1]; j <= nsingni; j = lLinkUp [j])
                {
                    PPINT const row = ineq_row [j] ;
                    if ( (t = dk [row]) < PPZERO )
                    {
                        /* lambda > 0 for lLinkUp */
                        if ( ni ) s = -(lambda [row]+shift_l [row])/t ;
                        else      s = (singc[j]-(lambda [row]+shift_l [row]))/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
                for (j = uLinkUp [nsingni2]; j <= nsingni; j = uLinkUp [j])
                {
                    PPINT const row = ineq_row [j] ;
                    if ( (t = dk [row]) > PPZERO )
                    {
                        /* lambda < 0 for uLinkUp */
                        if ( ni ) s = -(lambda [row]+shift_l [row])/t ;
                        else      s = (singc[j]-(lambda [row]+shift_l [row]))/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
            }

            /* ============================================================== */
            /* sort break points, do a line search */
            /* ============================================================== */

            lineflag = 0 ;
            if ( nbrk > 0 )
            {
                pproj_minheap_build (Heap, Br_value, nbrk) ;
                for (k = 1; k <= nbrk; k++)
                {
                    ns [Heap [k]] = k ;
                }

#ifndef NDEBUG
                pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                    "build Heap, ssor0") ;
#endif

                st = PPZERO ;
                while ( nbrk > 0 )
                {
                    if ( sd > PPZERO )
                    {
                        col = Heap [1] ;
                        Br = PPMAX (Br_value [col], PPZERO) ;
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
                        pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1) ;
                        fn = fd - sd * (Br - st) ;

#ifndef NDEBUG
                        pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                "Heap delete, ssor0") ;
                        if ( PrintLevel > 2 )
                        {
                            PRINTF("    brk: %ld col: %ld fn: %9.3e fd: %9.3e"
                                   " sd: %9.3e st: %9.3e Br_value: %9.3e\n",
                                  (LONG) nbrk, (LONG) col, fn, fd, sd, st, Br) ;
                        }
#endif

                        if ( fn <= PPZERO )
                        {
                            if ( fd != fn )
                            {
                                st += (fd/(fd-fn))*(Br - st);
                            }
                            fd = PPZERO ;
                            break ;
                        }
                        else
                        {
                            fd = fn ;
                        }
                        nup++ ;
                    }
                    else
                    {
                        break ;
                    }

                    st = Br ;

                    if ( col < ncol ) /* free column */
                    {
                        F [nf++] = col ;
                        s = pA [col] ;
                        sd += s*s ;
                        ib [col] = 0 ;
                        k = ColmodFlag [col] ;
                        if ( k != EMPTY )
                        {
                            l = ColmodList [ncol-ncoldel] ;
                            ColmodList [k] = l ;
                            ColmodFlag [l] = k ;
                            ColmodFlag [col] = EMPTY ;
                            ncoldel-- ;
                        }
                        else
                        {
                            ColmodList [ncoladd] = col ;
                            ColmodFlag [col] = ncoladd ;
                            ncoladd++ ;
                        }
                        q = Ap [col+1] ;
                        for (p = Ap [col]; p < q; p++)
                        {
                            i = Ai [p] ;
                            if ( ir [i] <= nsingni )
                            {
                                ax = Ax [p] ;
                                D [i] += ax*ax ;
                                l = AFTp [i] + AFTnz [i]++ ;
                                AFTx [l] = ax ;
                                AFTi [l] = col ;
                            }
                        }
#ifndef NDEBUG
                        if ( PrintLevel > 2 )
                        {
                            PRINTF ("    free: %ld\n", (LONG) col) ;
                        }
#endif
                    }
                    else              /* drop row */
                    {
                        Stat->ssor0_drop++ ;
                        PPINT const sing = col - ncol ;
                        PPINT const row  = ineq_row [sing] ;

#ifndef NDEBUG
                        if ( PrintLevel > 2 )
                        {
                            PRINTF("    jsing: %ld row: %ld ir: %ld\n",
                                    (LONG) sing, (LONG) row, (LONG) ir [row]) ;
                        }
                        if ( ir [row] > nsingni )
                        {
                            PRINTF ("row: %ld ir: %ld was already deleted "
                                    "in ssor0\n", (LONG) row, (LONG) ir [row]) ;
                            pproj_error (-1, __FILE__, __LINE__, "stop") ;
                        }
#endif
                        ASSERT ((ir [row] != 0) && (ir [row] <= nsingni)) ;
                        /* row dropped due to singleton sing */ 
                        ir [row] = sing + nsingni ;
                        i = RLinkDn [row] ;
                        k = RLinkUp [row] ;
                        RLinkUp [i] = k ;
                        RLinkDn [k] = i ;

                        k = RowmodFlag [row] ;
                        if ( k != EMPTY ) /* row set to be added, remove it */
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

                        if ( W->shiftl_is_zero )
                        {
                            if ( ni )
                            {
                                dknew = -lambda [row] ;
                                lambda [row] = PPZERO ;
                            }
                            else /* nsing */
                            {
                                dknew = singc [sing] - lambda [row] ;
                                lambda [row] = singc [sing] ;
                            }
                        }
                        else
                        {
                            if ( ni )
                            {
                                dknew = -(lambda [row]+shift_l [row]) ;
                                lambda [row] = -shift_l [row] ;
                            }
                            else /* nsing */
                            {
                                t = singc [sing] - shift_l [row] ;
                                dknew = t - lambda [row] ;
                                lambda [row] = t ;
                            }
                        }

                        b [row] -= sigma*dknew ;
                        PPFLOAT const dk_row = dk [row] ;
                        /* fd += dk_row*(Dsigma*dknew-b [row]) ;*/
                        fd -= dk_row*b [row] ;
                        sd -= sigma*dk_row*dk_row ;
                        if ( dk_row > PPZERO ) /* drop upper bound bu */
                        {
                            b [row] -= bu [sing] ;
                            m = uLinkUp [sing] ;
                            l = uLinkDn [sing] ;
                            uLinkUp [l] = m ;
                            uLinkDn [m] = l ;
                            if ( Parm->cholmod == TRUE )
                            {
                                blk = sol_to_blk [sing] ;
                                if ( sing == ustart [blk] )
                                {
                                    ustart [blk] = m ;
                                }
                            }
                            if ( nsing )
                            {
                                shi [row] = 0 ;
                                j = slo [row] ;
                                if ( j )
                                {
                                    m = lLinkUp [j] ;
                                    l = lLinkDn [j] ;
                                    lLinkUp [l] = m ;
                                    lLinkDn [m] = l ;
                                    slo [row] = 0 ;
                                    if ( Parm->cholmod == TRUE )
                                    {
                                        if ( j == lstart [blk] )
                                        {   
                                            lstart [blk] = m ;
                                        }
                                    }
                                }
                            }
                        }
                        else /* drop lower bound bl */
                        {
                            b [row] -= bl [sing] ;
                            m = lLinkUp [sing] ;
                            l = lLinkDn [sing] ;
                            lLinkUp [l] = m ;
                            lLinkDn [m] = l ;
                            if ( Parm->cholmod == TRUE )
                            {
                                blk = sol_to_blk [sing] ;
                                if ( sing == lstart [blk] )
                                {
                                    lstart [blk] = m ;
                                }
                            }
                            if ( nsing )
                            {
                                slo [row] = 0 ;
                                j = shi [row] ;
                                if ( j )
                                {
                                    m = uLinkUp [j] ;
                                    l = uLinkDn [j] ;
                                    uLinkUp [l] = m ;
                                    uLinkDn [m] = l ;
                                    shi [row] = 0 ;
                                    if ( Parm->cholmod == TRUE )
                                    {
                                        if ( j == ustart [blk] )
                                        {
                                            ustart [blk] = m ;
                                        }
                                    }
                                }
                            }
                        }

                        q = ATp [row+1] ;
                        for (p = ATp [row] ; p < q ; p++)
                        {
                            j = ATi [p] ;
                            ax = ATx [p] ;
                            s = pA [j] ;
                            /* cj = c after taking the step */
                            cj = c [j] + st*s ;
                            /* Modify c to account for later update. That is,
                               when we drop row i, the contribution of the
                               elements in row i to c need to be removed.
                               The previous contribution of row i to c was
                               a_{ij}lambda_i. So now we need to subtract this
                               term from c. Note that dknew = -lambda_i. */
                            c [j] += dknew*ax ;
                            t = dk_row*ax ;
                            snew = pA [j] = s - t ;
                            /* update c, pA, sd, fd */
                            if ( !ib [j] ) /* variable is free */
                            {
                                fd += cj*t ;
                                sd -= t*(s + snew) ;
                            }
                            else
                            {
                                if ( ib [j] < 0 ) /* cj < 0 */
                                {
                                    if ( snew > PPZERO )
                                    {
                                        Br_value [j] = st - cj/snew ;
                                        if ( ns [j] != EMPTY )
                                        {
                                            pproj_minheap_update (Heap,
                                               ns, Br_value, nbrk, ns [j]) ;
                                        }
                                        else
                                        {
                                           pproj_minheap_add (j, Heap,
                                               ns, Br_value, &nbrk) ;
                                        }
                                    }
                                    else /* this variable remains bound */
                                    {
                                        if ( ns [j] != EMPTY )
                                        {
                                            pproj_minheap_delete (Heap,
                                               ns, Br_value, &nbrk, ns [j]);
                                        }
                                    }
                                }
                                else /* ib [j] > 0 and cj > 0 */
                                {
                                    if ( snew < PPZERO )
                                    {
                                        Br_value [j] = st - cj/snew ;
                                        if ( ns [j] != EMPTY )
                                        {
                                            pproj_minheap_update (Heap,
                                               ns, Br_value, nbrk, ns [j]) ;
                                        }
                                        else
                                        {
                                            pproj_minheap_add (j, Heap,
                                                ns, Br_value, &nbrk) ;
                                        }
                                    }
                                    else /* this variable remains bound */
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
#ifndef NDEBUG
                        if ( PrintLevel > 2 )
                        {
                            PRINTF ("    drop row: %ld\n", (LONG) row) ;
                        }
#endif
                    }

#ifndef NDEBUG
                    pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                        "line search of ssor, ssor0") ;
#endif

                    if ( fd <= PPZERO )
                    {

#ifndef NDEBUG
                        if ( PrintLevel > 2 )
                        {
                            PRINTF("    premature break from line search\n") ;
                        }
#endif

                        lineflag = 1 ;
                        fd = PPZERO ;
                        break ;
                    }
                }
                if ( sd > PPZERO )
                {
                    st += fd/sd ;
                }
                if ( st > st0 )
                {
                    st = st0 ;
                    lineflag = -1 ;
                }

                for (k = 1; k <= nbrk; k++)
                {
                    ns [Heap [k]] = EMPTY ;
                }
            }
            if ( st > PPZERO )
            {
                for (i = RLinkUp [nrow]; i < nrow; i = RLinkUp [i])
                {
                    t = st*dk [i] ;
                    lambda [i] += t ;
                    b [i] -= sigma*t ;
                }
                pproj_saxpy (c, pA, st, ncol) ;
            }
        }
        chg += nup ;
#ifndef NDEBUG
        where = "end of ssor0 line search" ;
        pproj_check_line (I, lineflag, W->blks - 1, nup, dk, st) ;
        pproj_checkb (I, where) ;
        pproj_checkc (I, where) ;
        pproj_check_const (NULL, PPZERO, ns, EMPTY, ntot, where) ;
        pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif
    }
    W->ncoladd = ncoladd ;
    W->ncoldel = ncoldel ;
    W->nrowdel = nrowdel ;
    W->nrowadd = nrowadd ;
    Stat->ssor0_free += nf - W->nf ;
    W->chg_ssor0 = chg ;
    W->nf = nf ;
    Stat->ssor0 += pproj_timer () - tic ;
    Stat->ssor0_its += it ;
    if ( PrintLevel > 1 )
    {
        PRINTF ("SSOR0 complete, it: %ld\n", (LONG) it) ;
    }
}
