/* ========================================================================== */
/* check_dual (based on the current ib, only enforce bounds when ib [j] != 0) */
/* ========================================================================== */

#include "pproj.h"
void pproj_check_dual /* return dual objective at current point */
(
    PPcom      *I,
    PPFLOAT   *dl,
    char   *where,
    int      save, /* TRUE  => saves dual objective value for next comparison
                      FALSE => put dual value in C->mark but do not compare */
    int     check  /* TRUE => check for increase in dual objective */
)
{
    int loExists, hiExists, status, *ib ;
    PPINT    i, j, k, p, q, ncol, nrow, row, *ATi, *ATp, *ir, *temp ;
    PPFLOAT cost, lmax, loj, hij, t, s, tol, zerr, zmax,
           *ATx, *b, *hi, *lo, *y, *z, *lambda ;
    PPcheck   *C ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check dual value %s\n", where) ;

    W = I->Work ;
    C = I->Check ;
    int const location = C->location ;
    Parm = I->Parm ;
    Prob = I->Prob ;
    y = Prob->y ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    if ( I->Check->lo == NULL ) lo = Prob->lo ;
    else                        lo = I->Check->lo ; /* LP's include shift_x */
    if ( I->Check->hi == NULL ) hi = Prob->hi ;
    else                        hi = I->Check->hi ;
    if ( I->Check->b  == NULL ) b  = Prob->b ;
    else                        b  = I->Check->b ;

    PPINT   const         ni = Prob->ni ;
    PPINT   const      nsing = Prob->nsing ;
    PPINT   const  *row_sing = Prob->row_sing ;
    PPINT   const *row_sing1 = row_sing+1 ;
    PPFLOAT const     *singc = Prob->singc ;
    PPFLOAT const        *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const        *bu = (nsing) ? Prob->singhi : Prob->bu ;
    PPINT   const       *slo = W->slo ;
    PPINT   const       *shi = W->shi ;

    loExists = W->loExists ;
    hiExists = W->hiExists ;
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;
    ib  = W->ib ;
    ir  = W->ir ;

    if ( location == 4 ) /* in ssor1, ir fudged, fix it */
    {
        temp = (PPINT *) pproj_malloc (&status, nrow, sizeof (PPINT)) ;
        pproj_copyi (temp, ir, nrow) ;
        PPINT const nsingni = nsing + ni ;
        i = ncol + nsingni ;
        PPINT const *Heap = W->arrayi ;
        while ( Heap [i] != EMPTY )
        {
            PPINT const ineqindex = Heap [i] ;
            row = Prob->ineq_row [ineqindex] ;
            temp [row] = nsingni + ineqindex ;
            i-- ;
        }
        ir = temp ;
    }

    /* allocate workspace */
    z = pproj_malloc (&status, ncol, sizeof (PPFLOAT)) ;
    lambda = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;

    if ( dl == NULL )
    {
        for (i = 0; i < nrow; i++)
        {
            lambda [i] = W->dlambda [i] + W->lambda [i] + W->shift_l [i] ;
        }
    }
    else
    {
        pproj_copyx (lambda, dl, nrow) ;
        for (i = 0; i < nrow; i++)
        {
            lambda [i] += W->dlambda [i] + W->lambda [i] + W->shift_l [i] ;
        }
    }

    pproj_copyx (z, y, ncol) ;
    p = 0 ;
    lmax = PPZERO ;
    s = PPZERO ;
    /* compute z = y + A'*lambda and |lambda - shift_l|^2 */
    for (i = 0; i < nrow; i++)
    {
        t = lambda [i] ;
        if ( fabs (t) > lmax ) lmax = fabs (t) ;
        q = ATp [i+1] ;
        for (; p < q; p++)
        {
            z [ATi [p]] += t*ATx [p] ;
        }
        t -= W->shift_l [i] ;
        s += t*t ;
    }
    /* the proximal part of the objective */
    cost = -0.5*I->Work->sigma*s ;
    C->lmax = lmax ;

    /* check sign of lambda for inequalities */
    tol = Parm->checktol*lmax ;
    if ( ni )
    {
        for (i = 0; i < nrow; i++)
        {
            if ( ir [i] == 0 )
            {
                continue ;
            }
            if ( ir [i] < 0 ) /* should have lambda_i >= 0 */
            {
                if ( lambda [i] < -tol )
                {
                    printf ("i: %ld ir: %ld lambda: %e\n",
                           (LONG) i, (LONG) ir [i], lambda [i]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
            else if ( ir [i] > ni ) /* should have lambda_i = 0 */
            {
                if ( fabs (lambda [i]) > tol )
                {
                    printf ("i: %ld ir: %ld lambda: %e\n",
                           (LONG) i, (LONG) ir [i], lambda [i]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
            else /* should have lambda_i <= 0 */
            {
                if ( lambda [i] > tol )
                {
                    printf ("i: %ld ir: %ld lambda: %e\n",
                           (LONG) i, (LONG) ir [i], lambda [i]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
        }
    }
    for (i = 1; i <= nsing; )
    {
        row = Prob->ineq_row [i] ;
        if ( ir [row] > nsing ) /* row is dropped */
        {
            j = ir [row] - nsing ;
            if ( lambda [row] != singc [j] )
            {
                printf ("row: %ld is dropped, sing: %ld, lambda: %e "
                        "!= singc: %e\n",
                       (LONG) row, (LONG) j, lambda [row], singc [j]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            i = row_sing1 [row] ;
            continue ;
        }
        /* the row is active */
        if ( slo [row] )
        {
            for (; i <= slo [row]; i++)
            {
                if ( singc [i] > lambda [row] )
                {
                    printf ("row: %ld is active, sing: %ld, lambda: %e "
                            "< singc: %e slo: %ld\n", (LONG) row, (LONG) i,
                            lambda [row], singc [i], (LONG) slo [row]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
        }
        if ( shi [row] )
        {
            for (; i < row_sing1 [row]; i++)
            {
                if ( singc [i] < lambda [row] )
                {   
                    printf ("row: %ld is active, sing: %ld, lambda: %e " 
                            "> singc: %e shi: %ld\n", (LONG) row, (LONG) i,
                            lambda [row], singc [i], (LONG) shi [row]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
        }
        else i = row_sing1 [row] ;
    }
    zmax = PPZERO ;
    s = PPZERO ;
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] )
        {
            if      ( (loExists == TRUE) && (z [j] < lo [j]) ) z [j] = lo [j] ;
            else if ( (hiExists == TRUE) && (z [j] > hi [j]) ) z [j] = hi [j] ;
        }
        if ( fabs (z [j]) > zmax ) zmax = fabs (z [j]) ;
        s += (z [j] - y [j])*(z [j] - y [j]) ;
    }
    cost += 0.5*s ;
    if ( zmax < PPONE )
    {
        zmax = PPONE ;
    }
    C->zmax = zmax ;
    for (j = 0; j < ncol; j++)
    {
        zerr = PPZERO ;
        if      ( ib [j] < 0 ) zerr = fabs (z [j] - lo [j]) ;
        else if ( ib [j] > 0 ) zerr = fabs (z [j] - hi [j]) ;
        if ( zerr != PPZERO )
        {
            if ( zmax != PPZERO ) zerr /= zmax ;
            if ( zerr > Parm->checktol )
            {
                loj = -PPINF ;
                hij =  PPINF ;
                if ( loExists == TRUE )
                {
                    loj = lo [j] ;
                }
                if ( hiExists == TRUE )
                {
                    hij = hi [j] ;
                }
                printf ("j: %ld z: %e lo: %e hi: %e ib: %i\n",
                       (LONG) j, z [j], loj, hij, ib [j]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }

    /* there is a term in the dual cost of the form lambda_i * (b-Ax)_i
       we start the formation of this term by evaluating b_i */
    k = 1 ;
    for (i = 0; i < nrow; i++)
    {
        t = b [i] ; /* right side, 0 for strict inequality */
        if ( ir [i] != 0 ) /* strict inequality or column singleton */
        {
            if ( ni ) /* strict inequality */
            {
                if ( ir [i] < 0 )
                {
                    t += bl [k] ;
                }
                else if ( ir [i] <= ni )
                {
                    t += bu [k] ;
                }
                /* if ir [i] > ni, then lambda_i should be 0 */
                k++ ;
            }
            /* when there is a column singletons, need to compute the
               singleton cost terms, which depend on the x's and also
               compute b_i */
            else if ( nsing )
            {
                /* when a row is dropped, need to account for all the
                   singletons that are at their bounds */
                if ( ir [i] > nsing ) /* row is dropped */
                {
                    j = ir [i] - nsing ; /* singleton causing drop */
                    for (; k < j; k++)
                    {
                        t += bl [k] ;
                        cost -= singc [k]*bl [k] ;
                    }
                    /* skip the singleton causing drop */
                    for (k++; k < row_sing1 [i]; k++)
                    {
                        t += bu [k] ;
                        cost -= singc [k]*bu [k] ;
                    }
                }
                else if ( ir [i] == 1 ) /* row is active, but with singletons */
                {
                    if ( slo [i] )
                    {
                        for (; k <= slo [i]; k++)
                        {
                            t += bl [k] ;
                            cost -= singc [k]*bl [k] ;
                        }
                    }
                    for (; k < row_sing1 [i]; k++)
                    {
                        t += bu [k] ;
                        cost -= singc [k]*bu [k] ;
                    }
                }
if ( cost > 1.e20 )
{
    printf ("lambda [%i] = %e\n", i, lambda [i]) ;
    printf ("row: %i ir: %i nsing: %i slo: %i shi: %i "
            "row_sing: %i row_sing1: %i\n",
             i, ir [i], nsing, slo [i], shi [i], row_sing [i], row_sing1 [i]) ;
    for (k = row_sing [i]; k < row_sing1 [i]; k++)
    {
        printf ("bl [%i] = %e\n", k, bl [k]) ;
    }
    for (k = row_sing [i]; k < row_sing1 [i]; k++)
    {
        printf ("bu [%i] = %e\n", k, bu [k]) ;
    }
    for (k = row_sing [i]; k < row_sing1 [i]; k++)
    {
        printf ("singc[%i] = %e\n", k, singc[k]) ;
    }
    pproj_error (-1, __FILE__, __LINE__, where) ;
}
            }
        }
        /* now evaluate the (Ax)_i term */
        q = ATp [i+1] ;
        for (p = ATp [i]; p < q; p++)
        {
            t -= ATx [p]*z [ATi [p]] ;
        }
        cost += t*lambda [i] ;
    }
    if ( Parm->PrintLevel > 0 ) printf("VAL: %25.15e\n",cost) ;
    if ( check == TRUE )
    {
        if ( C->prior > cost + Parm->checktol*(C->zmax+C->lmax) +
                        fabs(cost)*Parm->checktol )
        {
            PRINTF ("new cost %25.15e  < old cost %25.15e\n", cost, C->prior) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    if ( save == TRUE )
    {
        C->prior = cost ;
    }
    else
    {
        C->mark = cost ;
    }

    /* free workspace */
    pproj_free (z) ;
    pproj_free (lambda) ;
    if ( location == 4 )
    {
        pproj_free (temp) ;
    }

    return ;
}
