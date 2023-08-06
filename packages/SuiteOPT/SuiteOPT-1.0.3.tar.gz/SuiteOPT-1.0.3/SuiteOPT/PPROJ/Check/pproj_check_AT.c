/* ========================================================================= */
/* === check_AT ============================================================ */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_AT
(
    PPcom    *I,
    char *where
)
{
    int status ;
    PPINT i, n, nrow, ncol, p, *Tp, *Ti, *Ap, *Ai, *ATp, *ATi, *Wi ;
    PPFLOAT *Tx, *Ax, *ATx ;

    PPprob *Prob ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check AT %s\n", where) ;

    Prob = I->Prob ;
    nrow = Prob->nrow ;
    ncol = Prob->ncol ;
    Ap   = Prob->Ap ;
    Ai   = Prob->Ai ;
    Ax   = Prob->Ax ;

    W = I->Work ;
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;

    /* allocate temporary workspace */
    Tp = (PPINT *) pproj_malloc (&status, (nrow+1), sizeof (PPINT)) ;
    n = Ap [ncol] ;
    Ti = (PPINT *) pproj_malloc (&status, n, sizeof (PPINT)) ;
    Tx = (PPFLOAT *) pproj_malloc (&status, n, sizeof (PPFLOAT)) ;
    Wi = (PPINT *) pproj_malloc (&status, nrow, sizeof (PPINT)) ;

    pproj_transpose (Tp, Ti, Tx, Ap, Ai, Ax, nrow, ncol, Wi) ;

    /* Check Tp */
    for (i = 0; i <= nrow; i++)
    {
        if ( Tp [i] != ATp [i] )
        {
            PRINTF ("Column pointers wrong, i: %ld, Tp: %ld, ATp: %ld\n",
                    (LONG) i, (LONG) Tp [i], (LONG) ATp [i]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    /* Check Tx and Ti */
    for (p = 0; p < n; p++)
    {
        if ( Tx [p] != ATx [p] )
        {
            PRINTF ("ATx != transpose Ax p: %ld, Tx: %e, ATx: %e\n",
                    (LONG) p, Tx [p], ATx [p]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( Ti [p] != ATi [p] )
        {
            PRINTF ("ATi != transpose Ai p: %ld, Ti: %ld, ATi: %ld\n",
                (LONG) p, (LONG) Ti [p], (LONG) ATi [p]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    pproj_free (Tp) ;
    pproj_free (Ti) ;
    pproj_free (Tx) ;
    pproj_free (Wi) ;
}
