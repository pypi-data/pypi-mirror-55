/* ========================================================================= */
/* === check_back ========================================================== */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_back
(
    PPcom         *I,
    PPFLOAT *forward,
    PPFLOAT      *dl,
    int       botblk,
    char      *where
)
{
    int topblk, *leftdesc ;
    PPINT *row_start, *Lp, *Li, *Lnz, *ir, toprow, botrow, i, j, p, q ;
    PPINT ni ;
    PPFLOAT *Lx, *dlambda, mx, t, s ;
    cholmod_factor *L ;
    PPparm      *Parm ;
    PPwork         *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check back %s\n", where) ;

    Parm = I->Parm ;
    W = I->Work ;
    dlambda = W->dlambda;
    ir = W->ir ;

    ni = I->Prob->ni + I->Prob->nsing ;

    L    = W->L ;
    Lp   = L->p ;
    Lnz  = L->nz ;
    Li   = L->i ;
    Lx   = L->x ;
    /* nrow = L->n ; */

    leftdesc = W->leftdesc ;
    row_start = W->row_start ;
    botrow = row_start [botblk+1] ;
    topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
    toprow = row_start [topblk] ;

    s = mx = PPZERO ;
    for (j = toprow; j < botrow; j++)
    {
        if ( ir [j] <= ni )
        {
            p = Lp [j] ;
            q = p + Lnz [j] ;
            t = forward [j] / Lx [p] ;	/* divide by D(j,j) */
            mx = PPMAX (mx, fabs (t)) ;
            mx = PPMAX (mx, fabs (dlambda [j])) ;
            t -= dl [j] ;
            for (p++ ; p < q ; p++)
            {
                i = Li [p] ;
                if ( i >= botrow ) break ;
                t -= dl [i] * Lx [p] ;
            }
            s += fabs (t) ;
        }
    }

    if ( mx != PPZERO )
    {
        s /= mx ;
        if ( Parm->PrintLevel > 1 )
        {
            PRINTF ("err in backsolve: %e mx: %e\n", s, mx);
        }
        if ( s > 1.e-5 )
        {
            PRINTF ("err in backsolve: %e mx: %e\n", s, mx);
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
}
