/* ========================================================================= */
/* === pproj_sparsa ======================================================== */
/* ========================================================================= */

/*  NOTE: does not account for column singletons
    An implementation of the SpaRSA algorithm. First, perform an optimization
    along the gradient to obtain the stepsize. For a quadratic, the optimal
    stepsize along the gradient is ||g_k||^2/(g_k' Q g_k), which gives an
    estimate for 1/Hessian. We do not perform the gradient step, but instead
    use alpha0 = 1/stepsize as the starting alpha in SpaRSA.

    In SpaRSA, the new iterate lambda_k+1 is chosen to satisfy the condition

                  new L_R >= L_ref + alpha * beta * ||lambda_k+1 - lambda_k||^2

    where 0 < beta < 1, L_ref is the reference function value at lambda_k
    (explained below), and lambda_k+1 is chosen to maximize

               gs' * lambda - 0.5*sigma ||lambda - lambda_k||^2 + psi (lambda)

    Here gs is the gradient of the smooth part of the dual function
    evaluated at the current iterate lambda_k and psi is the nonsmooth
    part of the dual function:

                     psi_i (lambda) = bl_i * lambda_i if lambda_i > 0
                                      bu_i * lambda_i if lambda_i < 0

    In the code, gk is the total gradient, including both smooth and
    nonsmooth parts. From the formula above for psi, we have

                     gs_i = g_ki - bl_i if lambda_i > 0
                     gs_i = g_ki - bu_i if lambda_i < 0
                     gs_i = g_ki        otherwise

    Throughout the code, our current estimate of lambda is the code's lambda
    plus shift_l. To compute the increment from the current lambda,
    we need to solve the problem

           max gs_i v - 0.5 alpha v^2 + psi (v + lambda_i + shift_li)

    Let "a" be a free parameter whose value will be either bl_i or
    bu_i. Using "a" for the slope of psi, the maximizer over v is

           v (a) = (g_i + a)/alpha

    Hence, the optimal v in the SpaRSA subproblem is given by:

                         -
                        | v (bl_i) if v (bl_i) + lambda_i + shift_li > 0
               v_opt =  | v (bu_i) if v (bu_i) + lambda_i + shift_li < 0
                        | -(lambda_i+shift_li) otherwise
                         -

    lambda_(k+1)i = lambda_ki + v_opt.  At the same time that v_opt is
    computed, we also get set to compute the change in the function
    associated with moving to lambda_k+1. This is done in a way similar to the
    line search procedure in order to ensure accuracy in the computed change.
    Since the dual function is piecewise quadratic, the change in the
    dual objective can be computed by adding up the change in each of
    the quadratics as we move from lambda_k to lambda_k+1.

    Currently, the reference value L_ref is the GLL reference value; that is,
    if mem denotes the memory, then

        L_ref = max {L_R (lambda_k-j): j = 0, 1, ... , mem-1 } */

#include "pproj.h"

int pproj_sparsa /* return status:
                        (0) PPROJ_SOLUTION_FOUND
                        (9) PPROJ_STATUS_OK */
(
    PPcom *I
)
{
    int     blk, lambda_update, mem, ml, rp, ibj, iboldj, status,
           *ib, *ibold ;
    const int loExists = I->Work->loExists ;
    const int hiExists = I->Work->hiExists ;
    PPINT   itsparsa, itarm, i, iri, iri0, iroldi, j, k,
            l, m, p, p0, q, col, row,
            nmod, nbrk, nf, ineqindex,
            nrowdel, nrowadd, ncoladd, ncoldel, stat_col, stat_row,
            Ll, Ul, Rl, prevblkL, prevblkU,
           *AFTi, *AFTnz, *AFTp,
           *Heap, *F, *RLinkDn, *RLinkUp,
           *uLinkUp, *uLinkDn, *lLinkUp, *lLinkDn, *lstart, *ustart,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList,
           *ir, *irold, *ns, *worki ;

    PPFLOAT alpha, ax, Br, d, dl_sq, gmax, gmax0, smax,
            cost_change, g, s, t, st, fd, sd, tic, Lref,
            gki, shift_li, pAj, dlambda_i,
           *AFTx, *b, *c, *hi, *lo,
           *dlambda, *lambda, *shift_l,
           *Br_value, *D, *pA, *gk, *workd, *x, *obj ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;

    tic = pproj_timer () ;
#ifndef NDEBUG
    char   *where ;
    I->Check->location = 6 ; /* code operates in sparsa */
#endif

    /* extract the problem, statistics, and work structures from I */
    Prob = I->Prob ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    W = I->Work ;
    mem = Parm->mem ;

    int const PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 2 )
    {
        printf ("start sparsa\n") ;
    }

    /* Problem matrix */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const          ni = Prob->ni ;
    PPINT   const         ni1 = ni + 1 ;
    PPINT   const         ni2 = ni + 2 ;
    PPINT   const        ntot = ni1 + ncol ;
    PPINT   const   *ineq_row = Prob->ineq_row ;
    PPFLOAT const         *bl = Prob->bl ;
    PPFLOAT const         *bu = Prob->bu ;
    int     const *sol_to_blk = W->sol_to_blk ;
    PPFLOAT const       sigma = W->sigma ;
    int     const        blks = W->blks ;

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
    dlambda = W->dlambda ;
    lambda = W->lambda ;
    shift_l = W->shift_l ;
    x = W->x ;
    ib = W->ib ;
    ir = W->ir ;
    b = W->b ; /* the part of grad L (lambda) associated with bound variables */
    c = W->c ; /* y + A'lambda */
    F = W->F ;
    D = W->D ;
    ns = W->ns ;
    lo = W->lo ;
    hi = W->hi ;

    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;

    lstart = W->lstart ;
    ustart = W->ustart ;

    /* ======== start allocations ========
    -> work arrays:

       Heap     - int ntot, line search
       irold    - int nrow, for determining change in ir
       ibold    - int ncol, for determining change in ib
       pA       - double ncol, A'lambda
       Br_value - double ncol + nsingni + 1
       gk       - double nrow, gradient at current iterate
       obj      - double mem, storage for objective values */

    worki = W->arrayi ;
    Heap  = worki ;         worki += ntot ;
    irold = worki ;         worki += nrow ;
    ibold = (int *) worki ; worki += ncol ;

    workd = W->arrayd ;
    pA       = workd ; workd += ncol ;
    Br_value = workd ; workd += ntot ;
    gk       = workd ; workd += nrow ; /* grad L (lambda) */
    obj      = workd ; workd += mem ;

    /* ======== end of allocations ======== */
#ifndef NDEBUG
    where = "at very start of sparsa" ;
    pproj_checkF (I, where) ;
    pproj_checkc (I, where) ;
    pproj_checkb (I, where) ;
    pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
    pproj_checkD (I, where) ;
    pproj_check_AT (I, where) ;
    pproj_check_AFT (I, TRUE, where) ;
    pproj_check_link (I, (int *) NULL, 0, where) ;
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    pproj_copyi_int (ibold, ib, ncol) ;
    pproj_copyi (irold, ir, nrow) ;
    lambda_update = FALSE ; /* switch to TRUE when lambda is updated */
    stat_col = Stat->sparsa_col ;
    stat_row = Stat->sparsa_row ;
    status = PPROJ_STATUS_OK ;

    /* rp points to location of current function value, it increments
       from 0 to mem - 1 and then resets to 0 */
    rp = 0 ;

    /* function memory increments from 1 to mem and then stays fixed at mem */
    ml = 1 ;

    /* Object values are all expressed relative to the current iterate.
       Since the first iteration is monotone, objective value is initialized
       to 0. */
    obj [0] = PPZERO ;

    if ( W->shiftl_is_zero == TRUE )
    {
        shift_li = PPZERO ;
    }

    /* start the sparse iteration */
    for (itsparsa = 0; itsparsa < Parm->nsparsa; itsparsa++)
    {
        /* compute gradient of dual function */
        nf = 0 ;
        pproj_copyx (gk, b, nrow) ;
        for (j = 0; j < ncol; j++)
        {
            if ( ib [j] == 0 )
            {
                F [nf++] = j ;
                t = c [j] ;
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    gk [Ai [p]] -= Ax [p]*t ;
                }
            }
        }

        /* Compute the stepsize corresponding to a gradient step
           (Cauchy step) from the current iterate. Cauchy step st = fd/sd */
        sd = PPZERO ;
        for (k = 0; k < nf; k++)
        {
            j = F [k] ;
            q = Ap [j+1] ;
            t = PPZERO ;
            for (p = Ap [j]; p < q; p++)
            {
                i = Ai [p] ;
                if ( ir [i] <= ni )
                {
                    t += gk [i]*Ax [p] ; /* A'*gk */
                }
            }
            sd += t*t ;
        }
        fd = PPZERO ;
        for (i = 0; i < nrow; i++)
        {
            if ( ir [i] <= ni )
            {
                fd += gk [i]*gk [i] ;
            }
        }
        sd += sigma*fd ;

        /* Starting alpha in SpaRSA = sd/fd */
        if ( fd > PPZERO )
        {
            alpha = sd/fd ;
        }
        else
        {
            status = PPROJ_SOLUTION_FOUND ;
            break ; /* gradient vanishes at the current iterate */
        }
 
        /* reference function value is minimum of recent values */
        Lref = PPZERO ;
        for (k = 0; k < ml; k++)
        {
            if ( obj [k] < Lref )
            {
                Lref = obj [k] ;
            }
        }
#ifndef NDEBUG
        /* save the value of the dual function for checking cost_change */
        pproj_check_dual (I, NULL, "before the sparsa loop", FALSE, FALSE) ;
#endif

        /* Armijo line search */
        for (itarm = 0; itarm < Parm->narmijo; itarm++)
        {
            d = PPONE/alpha ;
            pproj_initx (pA, PPZERO, ncol) ;
            p = 0 ;
            nbrk = 0 ;
            nmod = ntot ; /* store modifications to constraints at end of Heap*/
            fd = PPZERO ;
            sd = PPZERO ;
            gmax = PPZERO ; /* max gradient for lambda_i != 0 */
            gmax0 = PPZERO ;/* max gradient for lambda_i == 0 */
            smax = PPZERO ; /* max -sign(lambda_i) grad_i L_R for inequalities*/
            for (i = 0; i < nrow; i++)
            {
                iri = ir [i] ;
                iri0 = iri ;
                gki = gk [i] ;
                if ( W->shiftl_is_zero == FALSE )
                {
                    shift_li = shift_l [i] ;
                }
                if ( iri <= ni )
                {
                    if ( fabs (gki) > gmax )
                    {
                        gmax = fabs (gki) ;
                    }
                    if ( iri != 0 ) /* skip the equality constraints */
                    {
                        if ( lambda [i] + shift_li > PPZERO )
                        {
                            if ( smax < -gki )
                            {
                                smax = -gki ;
                            }
                        }
                        else
                        {
                            if ( smax < gki )
                            {
                                smax = gki ;
                            }
                        }
                        /* form smooth part of the gradient */
                        if ( iri < 0 ) /* at lower bound */
                        {
                            iri = -iri ;
                            g = gki - bl [iri] ;
                        }
                        else
                        {
                            g = gki - bu [iri] ;
                        }
                    }
                    else
                    {
                        g = gki ;
                    }
                }
                else /* evaluate max gradient for lambda_i == 0 */
                {
                    g = gki ;
                    iri -= ni ;
                    t = bl [iri] + g ;
                    if ( t < PPZERO )
                    {
                        t = -(bu [iri] + g) ;
                    }
                    if ( t > gmax0 )
                    {
                        gmax0 = t ;
                    }
                }
                ineqindex = iri ;
                t = d*g ;
                if ( iri == 0 ) /* equality constraint */
                {
                    dlambda_i = t ;
                }
                else            /* inequality constraint */
                {
                    s = t ;
                    t += lambda [i] + shift_li ;
                    if ( t + bl [iri]*d > PPZERO )      /* lower bound active */
                    {
                        dlambda_i = s + bl [iri]*d ;
                        iri = -iri ;
                    }
                    else if ( t + bu [iri]*d < PPZERO ) /* upper bound active */
                    {
                        dlambda_i = s + bu [iri]*d ;
                    }
                    else                              /* inactive inequality*/
                    {
                        dlambda_i = -(lambda [i] + shift_li) ;
                        iri += ni ;
                    }
                }
                sd += dlambda_i*dlambda_i ;
                dlambda [i] = dlambda_i ;

                /* iri now corresponds to equation activity at new lambda */
                if ( iri != iri0 ) /* equation activity changes */
                {
                    k = ineqindex + ncol ;
                    if ( iri > ni ) /* active initially, terminally inactive */
                    {
                        fd += gk [i]*dlambda_i ;
                        nmod-- ;
                        Heap [nmod] = -k ; /* inactive */
                    }
                    else if ( iri0 > ni ) /* initially inactive, then active */
                    {
                        /* activate immediately */
                        if ( iri < 0 )
                        {
                            fd += (bl [ineqindex] + gk [i])*dlambda_i ;
                        }
                        else
                        {
                            fd += (bu [ineqindex] + gk [i])*dlambda_i ;
                        }
                        nmod-- ;
                        Heap [nmod] = k ; /* active at end */
                    }
                    else /* always active, but activity changes */
                    {
                        /* solve for the point where multiplier vanishes
                           (discontinuity in slope at this point) */
                        t = -(lambda [i] + shift_li)/dlambda_i ;
                        if ( t != PPZERO )
                        {
                            ASSERT (t >= PPZERO) ;
                            fd += gk [i]*dlambda_i ;
                            Br_value [k] = t ;
                            nbrk++ ;
                            Heap [nbrk] = k ;
                        }
                        else /* immediately switch activity */
                        {
                            if ( iri < 0 )
                            {
                                fd += (g + bl [ineqindex])*dlambda_i ;
                            }
                            else
                            {
                                fd += (g + bu [ineqindex])*dlambda_i ;
                            }
                            nmod-- ;
                            Heap [nmod] = k ;
                        }
                    }
                }
                else /* always the same constraint activity */
                {
                    if ( iri <= ni ) /* active constraints contribute to fd */
                    {
                        fd += gk [i]*dlambda_i ;
                    }
                }

                /* evaluate the change in c associate with change in lambda */
                q = ATp [i+1] ;
                for (; p < q; p++)
                {
                    pA [ATi [p]] += ATx [p]*dlambda_i ;
                }
            }
            dl_sq = sd ; /* square of dlambda needed for Armijo test */
            sd *= sigma ;

            /* compute any additional break points associate with the
               bound constraints */
            for (j = 0; j < ncol; j++)
            {
                pAj = pA [j] ;
                if ( ib [j] == 0 )
                {
                    sd += pAj*pAj ;
                    if ( pAj > PPZERO )      /* could hit upper bound */
                    {
                        if ( hiExists == FALSE )
                        {
                            continue ;       /* does not hit a bound */
                        }
                        t = hi [j] ;
                    }
                    else if ( pAj < PPZERO ) /* could hit lower bound */
                    {
                        if ( loExists == FALSE )
                        {
                            continue ;       /* does not hit a bound */
                        }
                        t = lo [j] ;
                    }
                    else                     /* does not hit a bound */
                    {
                        continue ;
                    }
                }
                else if ( ib [j] < 0 )       /* at lower bound */
                {
                    if ( pAj > PPZERO ) /* may become free */
                    {
                        t = lo [j] ;
                        /* second possible break point handled in line search */
                    }
                    else
                    {
                        continue ;
                    }
                }
                else                    /* at upper bound */
                {
                    if ( pAj < PPZERO ) /* may become free */
                    {
                        t = hi [j] ;
                        /* second possible break point handled in line search */
                    }
                    else
                    {
                        continue ;
                    }
                }
                t = (t - c [j])/pAj ;
                if ( t < PPONE )
                {
                    if ( t < PPZERO )
                    {
                        t = PPZERO ;
                    }
                    Br_value [j] = t ;
                    nbrk++ ;
                    Heap [nbrk] = j ;      /* add to heap  */
                }
            }

            /* compute the function change associated with replacing
               lambda by lambda + dlambda */
            if ( nbrk > 0 )
            {
                pproj_minheap_build (Heap, Br_value, nbrk) ;
                for (k = 1; k <= nbrk; k++)
                {
                    ns [Heap [k]] = k ;
                }
#ifndef NDEBUG
                pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                    "in sparsa");
#endif
            }
            cost_change = PPZERO ;
            st = PPZERO ;
            while ( nbrk > 0 )
            {
                j = Heap [1] ;
                Br = Br_value [j] ;
                t = Br - st ;
                cost_change += fd*t - .5*sd*t*t ;
                fd -= sd * (Br - st) ;
                st = Br ;
                if ( j > ncol ) /* discontinuity in fd */
                {
                    pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1) ;
                    nmod-- ;
                    Heap [nmod] = j ;
                    ineqindex = j - ncol ;
                    row = ineq_row [ineqindex] ;
                    if ( dlambda [row] > PPZERO ) /* slope must decrease */
                    {
                        fd -= (bu [ineqindex] - bl [ineqindex])*dlambda [row] ;
                    }
                    else                        /* slope must increase */
                    {
                        fd += (bu [ineqindex] - bl [ineqindex])*dlambda [row] ;
                    }
                }
                else
                {
                    pAj = pA [j] ;
                    if ( ib [j] == 0 ) /* currently free, becomes bound */
                    {
                        sd -= pAj*pAj ;
                        pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1) ;
                        nmod-- ;
                        Heap [nmod] = j ;
                    }
                    else /*currently bound, becomes free or free becomes bound*/
                    {
                        if ( ib [j] < 0 ) /* check upper bound */
                        {
                            if ( hiExists == TRUE )
                            {
                                t = (hi [j] - c [j])/pAj ;
                            }
                            else
                            {
                                t = PPINF ;
                            }
                        }
                        else
                        {
                            if ( loExists == TRUE )
                            {
                                t = (lo [j] - c [j])/pAj ;
                            }
                            else
                            {
                                t = PPINF ;
                            }
                        }
                        if ( t >= PPONE ) /* bound became free */
                        {
                            sd += pAj*pAj ;
                            pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1);
                            nmod-- ;
                            Heap [nmod] = j ;
                            continue ;
                        }
                        if ( Br == t ) /* free became bound */
                        {
                            sd -= pAj*pAj ;
                            pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1);
                            nmod-- ;
                            Heap [nmod] = j ;
                        }
                        else /* new break point and bound became free */
                        {
                            sd += pAj*pAj ;
                            Br_value [j] = t ;
                            pproj_minheap_update (Heap, ns, Br_value, nbrk,
                                                        ns [j]) ;
                        }
                    }
                }
            }
            ASSERT (st <= PPONE) ;
            if ( st < PPONE )
            {
                t = PPONE - st ;
                cost_change += fd*t - 0.5*sd*t*t ;
            }
            /* if stepsize accepted, update variables and start next iteration*/
            if  ( cost_change >= Lref + Parm->beta*alpha*dl_sq )
            {
                lambda_update = TRUE ;
                ml++ ;
                if ( ml > mem )
                {
                    ml = mem ;
                }
                rp++ ;
                if ( rp >= mem )
                {
                    rp = 0 ;
                }
                /* the objective values are relative to the current objective
                   value */
                for (k = 0; k < ml; k++)
                {
                    obj [k] -= cost_change ;
                }
                obj [rp] = PPZERO ;
                pproj_saxpy (c, pA, PPONE, ncol) ;
                pproj_saxpy (lambda, dlambda, PPONE, nrow) ;
                pproj_saxpy (b, dlambda, -sigma, nrow) ;
                for (k = nmod; k < ntot; k++)
                {
                    col = Heap [k] ;
                    if ( col < 0 ) /* inequality that becomes inactive */
                    {
                        ineqindex = -(col + ncol) ;
                        row = ineq_row [ineqindex] ;
                        if ( ir [row] < PPZERO )
                        {
                            b [row] -= bl [ineqindex] ;
                        }
                        else
                        {
                            b [row] -= bu [ineqindex] ;
                        }
                        ir [row] = ineqindex + ni ;
                        lambda [row] = -shift_l [row] ;
                    }
                    else if ( col > ncol ) /* inequality changes its activity */
                    {
                        ineqindex = col - ncol ;
                        row = ineq_row [ineqindex] ;
                        if ( ir [row] > ni ) /* change from inactive to active*/
                        {
                            if ( dlambda [row] > PPZERO ) /* lower bound */
                            {
                                ir [row] = -ineqindex ;
                                b [row] += bl [ineqindex] ;
                            }
                            else
                            {
                                ir [row] = ineqindex ;
                                b [row] += bu [ineqindex] ;
                            }
                        }
                        else                    /* reverses its activity */
                        {
                            if ( ir [row] > 0 ) /* upper bound goes to lower */
                            {
                                b [row] += bl [ineqindex] - bu [ineqindex] ;
                            }
                            else                /* lower bound goes to upper */
                            {
                                b [row] += bu [ineqindex] - bl [ineqindex] ;
                            }
                            ir [row] = -ir [row] ;
                        }
                    }
                    else /* a constraint on a variable changes its activity */
                    {
                        if ( ib [col] == 0 ) /* variable moves to a bound */
                        {
                            if ( pA [col] > PPZERO ) /* moves to upper bound */
                            {
                                t = -hi [col] ;
                                ib [col] = +1 ;
                            }
                            else                     /* moves to lower bound */
                            {
                                t = -lo [col] ;
                                ib [col] = -1 ;
                            }
                        }
                        else if ( ib [col] < 0 )     /* free or upper bound */
                        {
                            if ( hiExists == TRUE )
                            {
                                if ( c [col] <= hi [col] ) /* becomes free */
                                {
                                    t = lo [col] ;
                                    ib [col] = 0 ;
                                }
                                else                 /* moves to upper bound */
                                {
                                    t = lo [col] - hi [col] ;
                                    ib [col] = +1 ;
                                }
                            }
                            else
                            {
                                t = lo [col] ;
                                ib [col] = 0 ;
                            }
                        }
                        else   /* ib [col > 0 => becomes free or lower bound */
                        {
                            if ( loExists == TRUE )
                            {
                                if ( c [col] >= lo [col] ) /* becomes free */
                                {
                                    t = hi [col] ;
                                    ib [col] = 0 ;
                                }
                                else                 /* moves to lower bound */
                                {
                                    t = hi [col] - lo [col] ;
                                    ib [col] = -1 ;
                                }
                            }
                            else
                            {
                                t = hi [col] ;
                                ib [col] = 0 ;
                            }
                        }
                        q = Ap [col+1] ;
                        for (p = Ap [col]; p < q; p++)
                        {
                            b [Ai [p]] += t*Ax [p] ;
                        }
                    }
                }
#ifndef NDEBUG
                where = "after sparsa update" ;
                pproj_initx (dlambda, PPZERO, nrow) ;
                pproj_checkc (I, where) ;
                pproj_checkb (I, where) ;
                pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
                t = cost_change + I->Check->mark ;
                pproj_check_dual (I, NULL, where, FALSE, FALSE) ;
                s = I->Check->mark ;
                printf ("cost estimate: %25.15e cost: %25.15e\n", t, s) ;
                if ( fabs (s-t) > Parm->checktol*fabs (s) )
                {
                    printf ("relatively poor cost estimate!!\n") ;
                }
#endif
                break ; /* line search condition satisfied */
            }
            else        /* see if Armijo condition holds with a larger alpha */
            {
                Stat->sparsa_step_fail++ ;
                alpha *= Parm->armijo_grow ;
            }
        }   /* continue Armijo line search */

        /* If the line search fails or the gradient associated with
           nonvanishing multipliers is large enough, then stop. */
        if ( (gmax >= W->gamma*gmax0) || (itarm == Parm->narmijo) )
        {
            break ;
        }
        else /* if ( gmax < W->gamma*gmax0 )*/
        {   /* Check the undecided index set and whether gamma decreases.
               Only check undecided indices if gradient is small enough
               relative to starting gradient grad0 evaluated at end of phase1 */
            if ( PPMAX (gmax, gmax0) <= W->grad0 )
            {
                if ( smax < Parm->tau*pow(gmax, Parm->beta) )
                {
                    W->gamma *= Parm->gamma_decay ;
                }
            }
        }
    }
    /* SpaRSA has completed, if lambda has changed, then perform updates */
    if ( lambda_update == TRUE )
    {
        ncoldel = W->ncoldel ;
        ncoladd = W->ncoladd ;
        nrowdel = W->nrowdel ;
        nrowadd = W->nrowadd ;
        nf = 0 ;
        for (j = 0; j < ncol; j++)
        {
            ibj = ib [j] ;
            iboldj = ibold [j] ;
            if( ibj != iboldj )
            {
                /* count number of changes in bound constraints */
                Stat->sparsa_col++ ;
                if ( PrintLevel > 2 )
                {
                    printf ("sparsa column %ld flips from %i to %i\n",
                            (LONG) j, iboldj, ibj) ;
                }
            }
            /* check if both at upper bound or both at lower bound or both free
               or one at upper bound and one at lower bound */
            if ( (iboldj == ibj) || (iboldj == -ibj) )
            {
                if ( ibj == 0 )
                {
                    F [nf++] = j ; /* j stays in the free list */
                }
                else /* a variable flipped to the opposite bound */
                {
                    if ( ibj > 0 ) /* lo [j] = 0 */
                    {
                        t = hi [j] ;
                    }
                    else            /* hi [j] = 0 */
                    {
                        t = lo [j] ;
                    }
                    if ( loExists == TRUE )
                    {
                        lo [j] -= t ;
                    }
                    if ( hiExists == TRUE )
                    {
                        hi [j] -= t ;
                    }
                    x [j] += t ;
                    c [j] -= t ;
                }
                continue ; /* no change between bound and free */
            }
            if ( ibj == 0 ) /* bound became free */
            {
                F [nf++] = j ;
                /* add column to free list if not in the delete list */
                if ( ColmodFlag [j] == EMPTY )
                {
                    ColmodList [ncoladd] = j ;
                    ColmodFlag [j] = ncoladd ;
                    ncoladd++ ;
                }
                else /* column was in the delete list, remove */
                {
                    l = ColmodFlag [j] ;
                    m = ColmodList [ncol-ncoldel] ;
                    ColmodList [l] = m ;
                    ColmodFlag [m] = l ;
                    ColmodFlag [j] = EMPTY ;
                    ncoldel-- ;
                }

                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( (ir [i] <= ni) && (irold [i] <= ni) )
                    {
                        ax = Ax [p] ;
                        D [i] += ax*ax ;
                        l = AFTp [i] + AFTnz [i]++ ;
                        AFTi [l] = j ;
                        AFTx [l] = ax ;
                    }
                }
            }
            else   /* free became bound */
            {
                /* add column to the delete list if not in the add list */
                if ( ColmodFlag [j] == EMPTY )
                {
                    ncoldel++ ;
                    W->ColmodList [ncol-ncoldel] = j ;
                    ColmodFlag [j] = ncol-ncoldel ;
                }
                else /* column was in the add list, remove it */
                {
                    l = ColmodFlag [j] ;
                    ncoladd-- ;
                    m = ColmodList [ncoladd] ;
                    ColmodList [l] = m ;
                    ColmodFlag [m] = l ;
                    ColmodFlag [j] = EMPTY ;
                }
                if ( ib [j] < 0 ) /* free went to lower bound */
                {
                    t = lo [j] ;
                }
                else
                {
                    t = hi [j] ;
                }
                q = Ap [j+1] ;
                if ( t == PPZERO )
                {
                    for (p = Ap [j]; p < q; p++)
                    {
                        i = Ai [p] ;
                        if ( (ir [i] <= ni) && (irold [i] <= ni) )
                        {
                            D [i] -= Ax [p]*Ax [p] ;
                            ns [i] = 0 ;
                        }
                    }
                }
                else
                {
                    if ( loExists == TRUE )
                    {
                        lo [j] -= t ;
                    }
                    if ( hiExists == TRUE )
                    {
                        hi [j] -= t ;
                    }
                    x [j] += t ;
                    c [j] -= t ;
                    for (p = Ap [j]; p < q; p++)
                    {
                        i = Ai [p] ;
                        if ( (ir [i] <= ni) && (irold [i] <= ni) )
                        {
                            D [i] -= Ax [p]*Ax [p] ;
                            ns [i] = 0 ;
                        }
                    }
                }
            }
        }

        if ( Parm->cholmod ) /* start of the blocks is saved */
        {
            for (k = 0; k < blks; k++)
            {
                lstart [k] = ni1 ;
                ustart [k] = ni2 ;
            }
        }
        Ll = ni1 ;
        Ul = ni2 ;
        Rl = nrow ;
        prevblkL = prevblkU = EMPTY ;
        for (i = 0; i < nrow; i++)
        {
            iri = ir [i] ;
            iroldi = irold [i] ;
            if ( iri != iroldi )
            {
                /* count number of changes in equation inequality activity */
                Stat->sparsa_row++ ;
                if ( PrintLevel > 2 )
                {
                    printf ("sparsa row %ld flips from ir = %ld to ir = %ld\n",
                            (LONG) i, (LONG) iroldi, (LONG) iri) ;
                }
            }
            if ( iri <= ni ) /* the row is active */
            {
                RLinkDn [i] = Rl ;
                RLinkUp [Rl] = i ;
                Rl = i ;

                /* add active inequality at lower bound to llinks */
                if ( iri < 0 )
                {
                    ineqindex = -iri ;
                    lLinkDn [ineqindex] = Ll ;
                    lLinkUp [Ll] = ineqindex ;
                    Ll = ineqindex ;
                    if ( Parm->cholmod == TRUE ) /* update start of blocks */
                    {
                        blk = sol_to_blk [ineqindex] ;
                        if ( blk > prevblkL )
                        {
                            lstart [blk] = ineqindex ;
                            prevblkL = blk ;
                        }
                    }
                }
                /* add active inequality at upper bound to ulinks */
                else if ( iri > 0 )
                {
                    ineqindex = iri ;
                    uLinkDn [ineqindex] = Ul ;
                    uLinkUp [Ul] = ineqindex ;
                    Ul = ineqindex ;
                    if ( Parm->cholmod == TRUE ) /* update start of blocks */
                    {
                        blk = sol_to_blk [ineqindex] ;
                        if ( blk > prevblkU )
                        {
                            ustart [blk] = ineqindex ;
                            prevblkU = blk ;
                        }
                    }
                }
                /* for previously inactive row, update modlist, AFT, and D */
                if ( iroldi > ni )
                {
                    /* if the row not in the delete list, then add it */
                    if ( RowmodFlag [i] == EMPTY )
                    {
                        nrowadd++ ;
                        RowmodList [nrow-nrowadd] = i ;
                        RowmodFlag [i] = nrow-nrowadd ;
                    }
                    else /* remove row from the delete list */
                    {
                        l = RowmodFlag [i] ;
                        nrowdel-- ;
                        m = RowmodList [nrowdel] ;
                        RowmodList [l] = m ;
                        RowmodFlag [m] = l ;
                        RowmodFlag [i] = EMPTY ;
                    }

                    /* update AFT and D */
                    t = sigma ;
                    q = ATp [i+1] ;
                    p = ATp [i] ;
                    l = AFTp [i] ;
                    for (; p < q; p++)
                    {
                        j = ATi [p] ;
                        if ( !ib [j] ) /* the column is free */
                        {
                            ax = ATx [p] ;
                            t += ax*ax ;
                            AFTx [l] = ax ;
                            AFTi [l] = j ;
                            l++ ;
                        }
                    }
                    D [i] = t ;            /* new diagonal element for SSOR */
                    AFTnz [i] = l - AFTp [i] ;
                }
                else /* the row is active both now and before */
                {
                    /* if there are new bound variables in row, compress AFT */
                    if ( ns [i] == 0 )
                    {
                        if ( D [i] < sigma ) /* D updated already above */
                        {
                            D [i] = sigma ;
                        }
                        p0 = l = p = AFTp [i] ;
                        q = p + AFTnz [i] ;
                        for (; p < q; p++)
                        {
                            if ( ib [AFTi [p]] == 0 ) /* column is free */
                            {
                                AFTi [l] = AFTi [p] ;
                                AFTx [l] = AFTx [p] ;
                                l++ ;
                            }
                        }
                        AFTnz [i] = l - p0 ;
                        ns [i] = EMPTY ;
                    }
                }
            }
            else /* the row is now inactive */
            {
                /* if the row was previously active, update modlists */
                if ( iroldi <= ni )
                {
                    AFTnz [i] = 0 ;
                    ineqindex = iri - ni ;
                    k = RowmodFlag [i] ;
                    if ( k != EMPTY ) /* row was set to be added */
                    {
                        /* move last added row to replace new dropped row */
                        l = RowmodList [nrow-nrowadd] ;
                        RowmodList [k] = l ;
                        RowmodFlag [l] = k ;
                        RowmodFlag [i] = EMPTY ;
                        nrowadd-- ; /* one less row to add */
                    }
                    else /* add row to the delete list */
                    {
                        RowmodList [nrowdel] = i ;
                        RowmodFlag [i] = nrowdel ;
                        nrowdel++ ;
                    }
                }
            }
        }
        /* terminate the links */
        lLinkUp [Ll] = ni1 ;
        uLinkUp [Ul] = ni2 ;
        lLinkDn [ni1] = Ll ;
        uLinkDn [ni2] = Ul ;
        RLinkDn [nrow] = Rl ;
        RLinkUp [Rl] = nrow ;
        /* store the adds and deletes */
        W->nrowadd = nrowadd ;
        W->ncoladd = ncoladd ;
        W->nrowdel = nrowdel ;
        W->ncoldel = ncoldel ;
        W->nf = nf ;
    }
    pproj_initx (dlambda, PPZERO, nrow) ;

    /* number of changes in both bound variable and in row constraints */
    W->chg_sparsa = (Stat->sparsa_row-stat_row) + (Stat->sparsa_col-stat_col) ;

    /* iterations in sparsa */
    Stat->sparsa_its += itsparsa + 1 ;

    /* time in sparsa */
    Stat->sparsa = pproj_timer () - tic ;
#ifndef NDEBUG
    where = "at very end of sparsa" ;
    pproj_checkF (I, where) ;
    pproj_checkc (I, where) ;
    pproj_checkb (I, where) ;
    pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
    pproj_checkD (I, where) ;
    pproj_check_AT (I, where) ;
    pproj_check_AFT (I, TRUE, where) ;
    pproj_check_link (I, (int *) NULL, 0, where) ;
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif
    return (status) ;
}
