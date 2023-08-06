/* ========================================================================== */
/* ==== check_error in D ==================================================== */
/* ========================================================================== */

#include "pproj.h"
void pproj_checkD
(
    PPcom    *I,
    char *where
)
{
    PPINT *ATp, *ATi, *ir, i, p, q, nrow, ni ;
    int *ib ;
    PPFLOAT *ATx, *D, t, sigma ;
    PPwork *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check D %s\n", where) ;
   
    W = I->Work ;
    nrow = I->Prob->nrow ;
    ni = I->Prob->ni + I->Prob->nsing ;
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;
    ib = W->ib ;
    ir = W->ir ;
    D = W->D ;
    sigma = I->Work->sigma ;

    for (i = 0; i < nrow; i++)
    {
        if ( ir [i] <= ni )
        {
            t = sigma ;
            q = ATp [i+1] ;
            for (p = ATp [i]; p < q; p++)
            {
                if ( !ib [ATi [p]] )
                {
                    t += ATx [p]*ATx [p] ;
                }
            }
            if ( fabs (t-D [i])/PPMAX (1., D [i]) > 1.e-8 )
            {
                PRINTF ("row: %ld D: %e computed: %e err: %e\n",
                       (LONG) i, D [i], t, fabs (t-D [i])) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }
}
