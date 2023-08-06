/* ========================================================================= */
/* === check_eqn5 ========================================================== */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_eqn5
(
    PPcom         *I,
    int       botblk,
    PPFLOAT      *dl,
    PPFLOAT *forward,
    PPFLOAT       *r,
    char     *where
)
{
    PPINT *row_start, *col_start, *Ap, *Anz, *Ai, *ATp, *ATi, *ir,
           topblk, toprow, botrow, topcol, botcol,
           i, j, p, q, nrow, ncol, ni ;
    int status, *ib, *leftdesc ;
    PPFLOAT *Ax, *ATx, *pA, *rhs, *cold, *lambda, mx, s, t, sigma ;
    PPwork    *W ;
    PPprob *Prob ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check eqn5 %s\n", where) ;

    W = I->Work ;
    Prob = I->Prob ;
    ib = W->ib ;
    ir = W->ir ;
    cold = W->cold ;
    sigma = I->Work->sigma ;
    lambda = W->lambda ;
    Ap   = Prob->Ap ;
    Anz  = Prob->Anz ;
    Ai   = Prob->Ai ;
    Ax   = Prob->Ax ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni   = Prob->ni + Prob->nsing ;

    ATp  = W->ATp ;
    ATi  = W->ATi ;
    ATx  = W->ATx ;

    leftdesc = W->leftdesc ;
    row_start = W->row_start ;
    col_start = W->col_start ;

    topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
    toprow = row_start [topblk] ;
    topcol = col_start [topblk] ;

    botrow = row_start [botblk+1] ;
    botcol = col_start [botblk+1] ;

    /* allocate workspace */
    pA  = pproj_malloc (&status, ncol, sizeof (PPFLOAT)) ;
    rhs = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;

    mx = 0 ;
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            mx = PPMAX (mx, fabs (r [i])) ;
            mx = PPMAX (mx, fabs (dl [i])) ;
            mx = PPMAX (mx, fabs (lambda [i])) ;
            mx = PPMAX (mx, fabs (forward [i])) ;
            t  = r [i] ;
            q = ATp [i+1] ;
            for (p = ATp [i]; p < q; p++)
            {
                j = ATi [p] ;
                if ( ib [j] == 0 )
                {
                    t -= ATx [p]*cold [j] ;
                }
            }
            rhs [i] = t ;
        }
    }

    for (j = topcol; j < botcol; j++)
    {
        pA [j] = 0 ;
        if ( ib [j] == 0 )
        {
            mx = PPMAX (mx, fabs (cold [j])) ;
        }
    }

    p = ATp [toprow] ;
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            t = dl [i] ;
            rhs [i] -= t*sigma ;
            q = ATp [i+1] ;
            for (p = ATp [i]; p < q; p++)
            {
                j = ATi [p] ;
                if ( (j < topcol) || (j >= botcol) )
                {
                    printf ("in check_eqn5, col %ld out of range %ld to %ld\n",
                           (LONG) j, (LONG) topcol, (LONG) botcol) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
                pA [j] += t*ATx [p] ;
            }
        }
    }

    for (j = topcol; j < botcol; j++)
    {
        if ( ib [j] == 0 )
        {
            t = pA [j] ;
            q = Ap [j] + Anz [j] ;
            for (p = Ap [j]; p < q; p++)
            {
                i = Ai [p] ;
                if ( i < toprow )
                {
                    printf ("in eqn5, row %ld below toprow %ld\n",
                           (LONG) i, (LONG) toprow) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
                if ( i >= botrow )
                {
                    break ;
                }
                if ( ir [i] <= ni ) rhs [i]  -= t * Ax [p] ;
            }
        }
    }

    s = 0 ;
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            s = PPMAX (s, fabs (rhs [i])) ;
        }
    }

    if ( mx > 1.e-15 )
    {
        s /= (mx*sqrt ((PPFLOAT) nrow));
        if ( I->Parm->PrintLevel > 1)
        {
            printf ("equation err: %e mx: %e\n", s, mx);
        }
        if ( s > 1.e-5 )
        {
            printf ("equation err: %e mx: %e\n", s, mx);
            for (i = toprow; i < botrow; i++)
            {
                if ( ir [i] <= ni )
                {
                    printf ("i: %ld err: %e r: %e dl: %e lambda: %e for: %e\n",
                           (LONG) i, rhs [i], r[i], dl [i], lambda [i],
                           forward [i]) ;
                }
            }
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    /* free workspace */
    pproj_free (pA) ;
    pproj_free (rhs) ;
}
