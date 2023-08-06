/* ========================================================================== */
/* ==== check_error in c ==================================================== */
/* ========================================================================== */

#include "pproj.h"
void pproj_checkc
(
    PPcom     *I,
    char  *where
)
{
    int status ;
    PPINT *ATp, *ATi, *ir, i, j, p, nrow, ncol, ni, nsing, nsingni ;
    PPFLOAT *ATx, *c, t, s, err, norm_l ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif

    printf ("checkc %s\n", where) ;
    Prob = I->Prob ;
    Parm = I->Parm ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni = Prob->ni ;
    nsing = Prob->nsing ;
    nsingni = nsing + ni ;
    W = I->Work ;
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;
    ir = W->ir ;

    /* allocate workspace */
    c = (PPFLOAT *) pproj_malloc (&status, ncol, sizeof (PPFLOAT)) ;
    pproj_copyx (c, Prob->y, ncol) ;
    /* outside of phase1, x is subtracted from c */
    if ( I->Check->location != 1 )
    {
        pproj_saxpy (c, W->x, -PPONE, ncol) ;
    }
    norm_l = PPZERO ;
    for (i = 0; i < nrow; i++)
    {
        t = W->dlambda [i] + W->lambda [i] + W->shift_l [i] ;
        if ( ir [i] > nsingni ) /* the row has been dropped */
        {
            if ( ni )
            {
                s = PPZERO ;
            }
            else /* dropped row singleton */
            {
                s = Prob->singc [ir [i] - nsing] ;
                norm_l += fabs (W->dlambda [i]) + fabs (W->lambda [i]) +
                          fabs (W->shift_l [i]) ;
                if ( t != PPZERO )
                {
                    for (p = ATp [i]; p < ATp [i+1]; p++)
                    {
                        c [ATi [p]] += ATx [p]*t ; /* c = y + A'lambda */
                    }
                }
            }
            if ( t != s )
            {
                printf ("row %ld has ir = %ld and lambda = %e != %e\n",
                        (LONG) i, (LONG) ir [i], t, s) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        else
        {
            norm_l += fabs (W->dlambda [i]) + fabs (W->lambda [i]) +
                      fabs (W->shift_l [i]) ;
            for (p = ATp [i]; p < ATp [i+1]; p++)
            {
                c [ATi [p]] += ATx [p]*t ; /* c = y + A'lambda */
            }
        }
    }

    if ( norm_l == PPZERO )
    {
        norm_l = 1. ;
    }

    t = PPZERO ;
    err = PPZERO ;
    for (j = 0; j < ncol; j++)
    {
/* printf ("j: %i cerr: %e c: %e W->c: %e\n",
j, fabs(c [j] - W->c [j]), c [j], W->c [j]) ;*/
        err = PPMAX (err, fabs (c [j] - W->c [j])) ;
        t = PPMAX (t, fabs (c [j])) ;
    }

    if ( (err/(t+norm_l) > Parm->checktol) && (err > Parm->checktol) )
    {
        printf ("err in c: %e norm_l: %e\n", err, norm_l) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }

    /* free workspace */
    pproj_free (c) ;
}
