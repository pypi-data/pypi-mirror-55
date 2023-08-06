/* ========================================================================== */
/* ==== checkb ============================================================== */
/* ========================================================================== */

#include "pproj.h"
void pproj_checkb
(
    PPcom *I,
    char  *where
)
{
    int status, location, *ib ;
    PPINT  *Ai, *Ap, *ir, *ineq_row, *temp, *Heap,
            ni, i, ineqindex, j, p, q, ncol, nrow, row ;
    PPFLOAT zmax, t, err, bmax,
           *x, *Ax, *b, *hi, *lo, *lambda ;
    PPcheck   *C ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif

    printf ("checkb %s\n", where) ;
    W = I->Work ;
    C = I->Check ;
    location = C->location ;
    Prob = I->Prob ;
    Parm = I->Parm ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    Ap = Prob->Ap ;
    Ai = Prob->Ai ;
    Ax = Prob->Ax ;
    ni = Prob->ni ;
    ineq_row = Prob->ineq_row ;

    PPINT   const      nsing = Prob->nsing ;
    PPINT   const    nsingni = ni + nsing ;
    PPINT   const  *row_sing = Prob->row_sing ;
    PPINT   const *row_sing1 = row_sing+1 ;
    PPINT   const       *slo = W->slo ;
    PPFLOAT const        *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const        *bu = (nsing) ? Prob->singhi : Prob->bu ;

    ib = W->ib ;
    ir = W->ir ;
    lo = W->lo ;
    hi = W->hi ;
    lambda = W->lambda ;
    x = W->x ;
    b = (PPFLOAT *) pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    if ( I->Check->b == NULL ) pproj_copyx (b, Prob->b, nrow) ;
    else                       pproj_copyx (b, I->Check->b, nrow) ;
    lambda = (PPFLOAT *) pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    /* LP's need to account for shift_x */
    bmax = PPZERO ;
    for (i = 0; i < nrow; i++)
    {
        lambda [i] = W->dlambda [i] + W->lambda [i] + W->shift_l [i] ;
        if ( fabs (b [i]) > bmax )
        {
            bmax = fabs (b [i]) ;
        }
    }
    if ( location == 4 ) /* in ssor1, ir fudged, fix it */
    {
        temp = (PPINT *) pproj_malloc (&status, nrow, sizeof (PPINT)) ;
        pproj_copyi (temp, ir, nrow) ;
        i = ncol + nsingni ;
        Heap = W->arrayi ;
        while ( Heap [i] != EMPTY )
        {
            ineqindex = Heap [i] ;
            row = ineq_row [ineqindex] ;
            temp [row] = nsingni + ineqindex ;
            i-- ;
        }
        ir = temp ;
    }

    for (i = 1; i <= ni; i++)
    {
        row = ineq_row [i] ;
        if ( ir [row] < 0 )
        {
            b [row] += bl [i] ;
            if ( fabs (bl [i]) > bmax )
            {
                bmax = fabs (bl [i]) ;
            }
            if ( (ir [row] != -i) || (lambda [row] < PPZERO) )
            {
                printf ("checkb error %s, row: %ld ir: %ld should be %ld lambda"
                        ": %e\n",
                        where, (LONG) row, (LONG) ir [row], (LONG) -i,
                        lambda [row]) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else if ( (ir [row] > 0) && (ir [row] <= ni) )
        {
            b [row] += bu [i] ;
            if ( fabs (bu [i]) > bmax )
            {
                bmax = fabs (bu [i]) ;
            }
            if ( (ir [row] != i) || (lambda [row] > PPZERO) )
            {
                printf ("checkb error %s, row: %ld ir: %ld should be "
                        "%ld lambda: %e\n",
                        where, (LONG) row, (LONG) ir [row], (LONG) i,
                        lambda [row]) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else /* the row is dropped */
        {
            if ( ir [row] == 0 )
            {
                printf ("checkb error %s, equation %ld is inequality "
                        "but ir = 0", where, (LONG) row) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
    }

    /* add the singleton bounds into b */
    for (i = 1; i <= nsing; )
    {
        row = ineq_row [i] ;
        if ( ir [row] > nsing ) /* row is dropped */
        {
            /* include all the bounds in b except for the singleton itself */
            PPINT const jsing = ir [row] - nsing ;
            for (i = row_sing [row]; i < jsing; i++)
            {
                b [row] += bl [i] ;
            }
            for (i++; i < row_sing1 [row]; i++)
            {
                b [row] += bu [i] ;
            }
            continue ;
        }
        else if ( ir [row] <= 0 )
        {
            printf ("checkb error %s, equation %ld is singleton inequality "
                    "but ir = %ld", where, (LONG) row, (LONG) ir [row]) ;
            pproj_error (-1, __FILE__, __LINE__, "stop") ;
        }
        else if ( slo [row] ) /* active row */
        {
            for (; i <= slo [row]; i++)
            {
                b [row] += bl [i] ;
            }
        }
        for (; i < row_sing1 [row]; i++)
        {
            b [row] += bu [i] ;
        }
    }

    for (j = 0; j < ncol; j++)
    {
        t = x [j] ;
        if ( t != PPZERO )
        {
            q = Ap [j+1] ;
            for (p = Ap [j]; p < q; p++)
            {
                b [Ai [p]] -= t*Ax [p] ;
            }
        }
    }

    /* In sparsa, x is not updated in each iteration, but b includes current
       bound variables. Need to return to ib to adjust b. */
    if ( location == 6 )
    {
        for (j = 0; j < ncol; j++)
        {
            if ( ib [j] > 0 )
            {
                t = hi [j] ;
            }
            else if ( ib [j] < 0 )
            {
                t = lo [j] ;
            }
            else
            {
                t = PPZERO ;
            }
            if ( t != PPZERO )
            {
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    b [Ai [p]] -= t*Ax [p] ;
                }
            }
        }
    }

    /* for all location except location 1 (phase 1) we also subtract
       sigma*lambda from b */
    if ( location != 1 )
    {
        pproj_saxpy (b, W->lambda, -I->Work->sigma, nrow) ;
    }
    bmax = PPMAX (bmax, PPONE) ;
    bmax = PPMAX (bmax, pproj_max (b, nrow)) ;
    zmax = C->zmax ;
    if ( zmax <= PPONE ) zmax = PPONE ;
    err = PPZERO ;
    for (i = 0; i < nrow; i++)
    {
        t = fabs (b [i] - W->b [i])/(zmax+bmax+C->lmax) ;
        if ( t > Parm->checktol )
        {
            printf ("checkb error %s, row: %ld b: %e should be: %e\n",
                     where, (LONG) i, W->b [i], b [i]) ;
            pproj_error (-1, __FILE__, __LINE__, "stop") ;
        }
        if ( err < t ) err = t ;
    }
    if ( Parm->PrintLevel > 0 ) PRINTF("b error: %e\n", err) ;
    pproj_free (b) ;
    pproj_free (lambda) ;
    if ( location == 4 )
    {
        pproj_free (temp) ;
    }
}
