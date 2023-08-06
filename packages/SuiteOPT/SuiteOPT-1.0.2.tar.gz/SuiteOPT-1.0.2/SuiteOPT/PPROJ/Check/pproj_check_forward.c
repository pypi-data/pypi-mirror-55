/* ========================================================================= */
/* === check_forward  ====================================================== */
/* ========================================================================= */

#include "pproj.h"
#define ISNAN(x) ((x) != (x))
void pproj_check_forward
(
    PPcom         *I,
    PPFLOAT *forward,
    PPFLOAT       *r,
    int     *joblist,
    int           nj,
    char      *where
)
{
    PPINT *row_start, *Ap, *Anz, *Ai, *Lp, *Li, *Lnz, *ir,
           botblk, topblk, toprow, botrow, i, j, p, q, nrow, ncol, ni, jobnum ;
    int status, *ib, *leftdesc ;
    PPFLOAT *Ax, *Lx, *rhs, *cold, *dlambda, mx, mxr, t ;
    cholmod_factor *L ;
    PPwork         *W ;
    PPprob      *Prob ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif

    printf ("check forward solve %s\n", where) ;
    if ( nj == 0 ) return ;
    botrow = 0 ;
    W = I->Work ;
    ib = W->ib ;
    ir = W->ir ;
    cold = W->cold ;
    dlambda = W->dlambda ;

    Prob = I->Prob ;
    Ap   = Prob->Ap ;
    Anz  = Prob->Anz ;
    Ai   = Prob->Ai ;
    Ax   = Prob->Ax ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni   = Prob->ni + Prob->nsing ;

    L = W->L ;
    Lp   = L->p ;
    Lnz  = L->nz ;
    Li   = L->i ;
    Lx   = L->x ;

    leftdesc = W->leftdesc ;
    row_start = W->row_start ;

    /* allocate workspace */
    rhs = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;

    for (i = 0; i < nrow; i++) rhs [i] = r [i] ;
    mx = PPONE ;
    mxr = PPZERO ;
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] == 0 )
        {
            t = cold [j] ;
            mx = PPMAX (mx, fabs (t)) ;
            q = Ap [j] + Anz [j] ;
            for (p = Ap [j]; p < q; p++)
            {
                rhs [Ai [p]] -= Ax [p]*t ;
            }
        }
    }

    i = 0 ;
    for (jobnum = 0; jobnum < nj; jobnum++)
    {
        botblk = joblist [jobnum] ;
        botrow = row_start [botblk+1] ;
        topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
        toprow = row_start [topblk] ;
        for (; i < toprow; i++) rhs [i] = 0 ;
        for (i = toprow; i < botrow; i++)
        {
            if ( ir [i] <= ni )
            {
                mxr = PPMAX (mxr, fabs (rhs [i])) ;
                mx = PPMAX (mx, fabs (forward [i])) ;
                mx = PPMAX (mx, fabs (r [i])) ;
                mx = PPMAX (mx, fabs (dlambda [i])) ;
                t  = forward [i] ;
                rhs [i] -= t ;
                p = Lp [i] ;
                q = p + Lnz [i] ;
                for (p++ ; p < q ; p++)
                {
                    rhs [Li [p]] -= Lx [p]*t ;
                }
            }
        }
    }

    for (i = botrow; i < nrow; i++) rhs [i] = PPZERO ;
    t = PPZERO ;
    for (i = 0; i < nrow; i++)
    {
        if ( ir [i] <= ni )
        {
            t = PPMAX (t, fabs (rhs [i])) ;
        }
    }

    mx = PPMAX (mx, mxr) ;
    if ( I->Parm->PrintLevel > 1 )
        printf ("err in forward solve: %e mx: %e\n", t, mx);
    if ( mx != PPZERO  || ISNAN (mx) || ISNAN (t))
    {
        t /= mx ;
        if ( t > 1.e-6 || ISNAN (mx) || ISNAN (t))
        {
            printf ("err in forward solve: %e mx: %e\n", t, mx);
            for (jobnum = 0; jobnum < nj; jobnum++)
            {
                botblk = joblist [jobnum] ;
                botrow = row_start [botblk+1] ;
                topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
                toprow = row_start [topblk] ;
                for (i = toprow; i < botrow; i++)
                {
                    if ( ir [i] <= ni )
                    {
                        printf("i: %ld rhs: %e\n", (LONG) i , rhs [i]) ;
                    }
                }
            }
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    /* free workspace */
    pproj_free (rhs) ;
}
