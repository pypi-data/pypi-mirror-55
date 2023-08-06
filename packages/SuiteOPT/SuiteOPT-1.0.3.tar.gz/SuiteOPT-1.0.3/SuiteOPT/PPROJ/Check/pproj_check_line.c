/* ========================================================================= */
/* === check_line ========================================================== */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_line
(
    PPcom        *I,
    int        flag, /* flag = 1 if line search terminates at nondiff point
                        flag = 2 if sd <= 0
                        flag =-1 if stepsize truncated to st = 1 */
    int      botblk,
    int     updates, /* number of updates to be performed */
    PPFLOAT     *dl, /* direction vector */
    PPFLOAT      st  /* stepsize */
)
{
    PPINT topblk, toprow, botrow, topcol, botcol, i, j, p, q, nrow, ncol, ni,
         *col_start, *row_start, *Ap, *Anz, *Ai, *ATp, *ATi, *ir, *RLinkUp ;
    int status, location, *ib, *leftdesc ;
    PPFLOAT *Ax, *b, *lambda, *dlambda, *rhs, *c, *pA, mx, s, t, norm_l, sigma ;
    PPwork    *W ;
    PPprob *Prob ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    W = I->Work ;
    location = I->Check->location ;
    /* location = 1 (phase 1)
                = 2 (dasa)
                = 3 (ssor0)
                = 4 (ssor1) */
    if ( location == 1 )
    {
        printf ("check line in phase1\n") ;
    }
    else if ( location == 2 )
    {
        printf ("check line in dasa\n") ;
    }
    else if ( location == 3 )
    {
        printf ("check line in ssor0\n") ;
    }
    else if ( location == 4 )
    {
        printf ("check line in ssor1\n") ;
    }
    
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
            else if ( (location == 3) || (location == 4) )
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
    else if ( (location == 3) || (location == 4) )
    {
        for (j = 0; j < ncol; j++)
        {
            if ( ib [j] == 0 )
            {
                t = c [j] ;
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

    t = PPZERO ;
    s = PPZERO ;
    norm_l = PPZERO ;
    if ( location < 4 )
    {
        for (i = toprow; i < botrow; i++)
        {
            if ( ir [i] <= ni )
            {
                t += fabs (rhs [i]) ;
                s += rhs [i]*dl [i] ;
                norm_l = PPMAX (norm_l, fabs (dl [i])) ;
            }
        }
    }
    /* In ssor1, ir has a dummy value for dropped rows, need to use
       RLinkUp in this case. */
    else /* location = 4, ssor1 */
    {
        RLinkUp = W->RLinkUp ;
        for (i = RLinkUp [nrow]; i < nrow; i = RLinkUp [i])
        {
            t += fabs (rhs [i]) ;
            s += rhs [i]*dl [i] ;
            norm_l = PPMAX (norm_l, fabs (dl [i])) ;
        }
    }
    mx = PPMAX (mx, norm_l) ;
    mx = PPMAX (mx, t) ;

    if ( (norm_l != 0) )
    {
	if ( flag == 2 ) /* sd <= 0 */
        {
            if ( s < -1.e-6 )
            {
                printf ("line err: %e flag: %i (deriv wrong sign)\n", s, flag);
                pproj_error (-1, __FILE__, __LINE__, "in check_line") ;
            }
        }
        else if ( flag == 1 ) /* line search terminates at nondiff point */
        {
            if ( s/((updates+1)*norm_l*mx) > 1.e-6 )
            {
                printf ("line err: %e flag: %i (deriv wrong sign)\n", s, flag);
                printf ("Excessive line error, norm_l: %e mx: %e updates: %i\n",
                    norm_l, mx, updates) ;
                pproj_error (-1, __FILE__, __LINE__, "in check_line") ;
            }
        }
        else if ( flag < 0 )
        {
            if ( s/((updates+1)*norm_l*mx) < -1.e-6 )
            {
                printf ("line err: %e flag: %i (deriv wrong sign)\n", s, flag);
                printf ("Excessive line error, norm_l: %e mx: %e updates: %i\n",
                    norm_l, mx, updates) ;
                pproj_error (-1, __FILE__, __LINE__, "in check_line") ;
            }
        }
        else
        {
            s = fabs (s) /((updates+1)*norm_l*mx) ;
	    if ( I->Parm->PrintLevel > 2 ) printf ("line err: %e\n", s);
            if ( s > 1.e-5 )
            {
                printf ("line err: %e \n", s);
                printf ("Excessive line error, norm_l: %e mx: %e updates: %i\n",
                    norm_l, mx, updates) ;
                pproj_error (-1, __FILE__, __LINE__, "in check_line") ;
            }
        }
    }

    /* free workspace */
    pproj_free (rhs) ;
    pproj_free (ib) ;
}
