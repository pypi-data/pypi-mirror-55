/* ========================================================================= */
/* === checkF ============================================================== */
/* ========================================================================= */
/* Check that the ib array with entries -1, +1, or 0 depending on whether
   the variable is at lower bound, upper bound, or free, and the F array
   (list of free variables) are consistent. */
/* ========================================================================= */

#include "pproj.h"
void pproj_checkF
(
    PPcom    *I,
    char *where
)
{
    PPINT j, k, ncol, nf, *F, *temp ;
    int status, *ib ;
    PPwork    *W ;
    PPprob *Prob ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check F %s\n", where) ;

    W = I->Work ;
    ib = W->ib ;
    F = W->F ;
    nf = W->nf ;

    Prob = I->Prob ;
    ncol = Prob->ncol ;

    k = 0 ;
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] == 0 ) k++ ;
    }
    if ( k != nf )
    {
        printf ("free indices in ib = %ld != nf: %ld\n", (LONG) k, (LONG) nf) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    temp = (PPINT *) pproj_malloc (&status, ncol, sizeof (PPINT)) ;
    pproj_initi(temp, EMPTY, ncol) ;
    for (k = 0; k < nf; k++)
    {
        j = F [k] ;
        if ( (j < 0) || (j >= ncol) )
        {
            printf("column index %ld in array F out of range 0 to ncol = %ld\n",
                   (LONG) j, (LONG) ncol) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( temp [j] == EMPTY )
        {
            temp [j] = 0 ;
        }
        else
        {
            printf ("column index %ld repeats in F array\n", (LONG) j) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    for (k = 0; k < nf; k++)
    {
        j = F [k] ;
        if ( ib [j] != 0 )
        {
            printf ("column index %ld in F but ib = %i, not 0\n",
                    (LONG) j, ib [j]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    /* free workspace */
    pproj_free (temp) ;
}
