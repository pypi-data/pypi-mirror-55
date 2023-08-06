/* ========================================================================= */
/* === check_deriv ========================================================= */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_deriv
(
    PPcom        *I,
    PPINT    botblk,
    PPFLOAT     *dl, /* direction vector */
    PPFLOAT      st  /* stepsize */
)
{
    int status, location, *ib, *leftdesc ;
    PPINT *col_start, *row_start, *Ap, *Anz, *Ai, *ATp, *ATi, *ir,
           topblk, toprow, botrow, topcol, botcol, i, j, p, q, nrow, ncol, ni ;
    PPFLOAT *Ax, *b, *lambda, *dlambda, *rhs, *c, *pA,
            normg, normd, mx, s, t, sigma ;
    PPwork    *W ;
    PPprob *Prob ;

    W = I->Work ;
    location = I->Check->location ;
    /* location = 1 (phase 1)
                = 2 (dasa)
                = 3 (ssor0) */
    Prob = I->Prob ;
    lambda = W->lambda ;
    dlambda = W->dlambda ;
    b = W->b ;
    c = W->c ;
    ir = W->ir ;
    pA = W->arrayd ;
    sigma = I->Work->sigma ;

    Ap   = Prob->Ap ;
    Anz  = Prob->Anz ;
    Ai   = Prob->Ai ;
    Ax   = Prob->Ax ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni   = Prob->ni + Prob->nsing ;

    ATp  = W->ATp ;
    ATi  = W->ATi ;

    leftdesc = W->leftdesc ;
    row_start = W->row_start ;
    col_start = W->col_start ;

    topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
    toprow = row_start [topblk] ;
    botrow = row_start [botblk+1] ;
    topcol = col_start [topblk] ;
    botcol = col_start [botblk+1] ;

    /* allocate workspace */
    rhs = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    ib  = pproj_malloc (&status, ncol, sizeof (int)) ;

    for (j = topcol; j < botcol; j++) ib [j] = W->ib [j] ;

    mx = 0 ;
    p = ATp [toprow] ;
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            if ( location == 1 )
            {
                rhs [i] = b [i] - sigma*(lambda [i]+st*dl [i]) ;
            }
            else if ( location == 2 )
            {
                rhs [i] = b [i] - dlambda [i]*sigma ;
                mx = PPMAX (mx, fabs (dlambda [i])) ;
            }
            else if ( location == 3 )
            {
                rhs [i] = b [i] ;
            }
            mx = PPMAX (mx, fabs (b [i])) ;
            mx = PPMAX (mx, fabs (lambda [i])) ;
            q = ATp [i+1] ;
            for (; p < q; p++)
            {
                j = ATi [p] ;
                if ( (j < topcol) || (j >= botcol) )
                {
                    printf ("in line, col %ld out of range %ld to %ld\n",
                           (LONG) j, (LONG) topcol, (LONG) botcol) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
            }
        }
    }

    if ( location == 1 )
    {
        for (j = 0; j < ncol; j++)
        {
            if ( ib [j] == 0 )
            {
                t = c [j] + st*pA [j] ;
                mx = PPMAX (mx, fabs (t)) ;
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( ir [i] <= ni )
                    {
                        rhs [i] -= t*Ax [p] ;
                    }
                }
            }
        }
    }
    else if ( location == 2 )
    {
        for (j = topcol; j < botcol; j++)
        {
            if ( ib [j] == 0 )
            {
                t = c [j] ;
                mx = PPMAX (mx, fabs (t)) ;
                q = Ap [j] + Anz [j] ;
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( i >= botrow ) break ;
    
                    if ( ir [i] <= ni )
                    {
                        if ( i >= toprow )
                        {
                            rhs [i] -= t*Ax [p] ;
                        }
                    }
                }
            }
        }
    }
    else if ( location == 3 )
    {
        for (j = 0; j < ncol; j++)
        {
            if ( ib [j] == 0 )
            {
                t = c [j] + st*pA [j] ;
                mx = PPMAX (mx, fabs (t)) ;
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( ir [i] <= ni )
                    {
                        if ( i >= toprow )
                        {
                            rhs [i] -= t*Ax [p] ;
                        }
                    }
                }
            }
        }
    }

    s = PPZERO ;
    normg = PPZERO ;
    normd = PPZERO ;
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            s += rhs [i]*dl [i] ;
            normg += fabs (rhs [i]) ;
            normd += fabs (dl [i]) ;
        }
    }
    printf ("deriv: %25.15e normg: %e normd: %e\n", s, normg, normd) ;

    /* free workspace */
    pproj_free (rhs) ;
    pproj_free (ib) ;
}
