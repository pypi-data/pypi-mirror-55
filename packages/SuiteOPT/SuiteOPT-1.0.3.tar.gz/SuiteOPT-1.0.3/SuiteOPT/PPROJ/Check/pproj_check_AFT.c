/* ========================================================================= */
/* === check_AFT =========================================================== */
/* ========================================================================= */

#include "pproj.h"

void pproj_check_AFT
(
    PPcom    *I,
    int  use_ir,  /* TRUE means skip deleted rows */
    char *where
)
{
    PPINT *ATp, *ATi, *AFTp, *AFTi, *AFTnz, *J, *ir,
           i, j, p, q, nrow, ncol, ni ;
    int status, *ib ;
    PPFLOAT *X, *ATx, *AFTx ;
    PPprob *Prob ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check AFT %s\n", where) ;

    Prob = I->Prob ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni = Prob->ni + Prob->nsing ;

    W = I->Work ;
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;
    AFTp = W->AFTp ;
    AFTi = W->AFTi ;
    AFTx = W->AFTx ;
    AFTnz = W->AFTnz ;
    ib = W->ib ;
    ir = W->ir ;

    for (i = 0; i <= nrow; i++) ASSERT (AFTp [i] == ATp [i]) ;

    /* allocate workspace */
    J = (PPINT *) pproj_malloc (&status, ncol, sizeof (PPINT)) ;
    X = (PPFLOAT *) pproj_malloc (&status, ncol, sizeof (PPFLOAT)) ;

    for (j = 0; j < ncol; j++) J [j] = 0 ;
    for (i = 0; i < nrow; i++)
    {
        /* skip deleted rows if use_ir is TRUE and the row has been deleted */
        if ( use_ir && (ir [i] <= ni) || !use_ir )
        {
            p = AFTp [i] ;
            q = p + AFTnz [i] ;
            for (; p < q; p++)
            {
                j = AFTi [p];
                if ( (j < 0) || (j > ncol) )
                {
                    PRINTF ("AFT error %s, col: %ld in AFT out of range "
                            "(%i to %ld)\n",
                            where, (LONG) j, 0, (LONG) (ncol-1)) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
                if ( J [j] )
                {
                    PRINTF ("AFT error %s, row: %ld col: "
                            "%ld repeats in AFT\n", where, (LONG) i, (LONG) j) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
                if ( ib [j] )
                {
                    PRINTF ("AFT error %s, row: %ld col: %ld in AFT "
                            "but ib not zero: %i\n",
                            where, (LONG) i, (LONG) j, ib [j]) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
                J [j] = 1 ;
                X [j] = AFTx [p] ;
            }
            p = ATp [i] ;
            q = ATp [i+1] ;
            for (; p < q; p++)
            {
                j = ATi [p];
                if ( (j < 0) || (j >= ncol) )
                {
                    PRINTF ("AFT error %s, col: %ld in AT out of range "
                            "(%i to %ld)\n",
                            where, (LONG) j, 0, (LONG) (ncol-1)) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
                if ( !ib [j] )
                {
                    if ( !J [j] )
                    {
                        PRINTF ("AFT error %s, row: %ld col: %ld in AT and "
                                "ib zero, but not in AFT\n",
                                where, (LONG) i, (LONG) j) ;
                        pproj_error (-1, __FILE__, __LINE__, "stop") ;
                    }
                    J [j] = 0 ;
                    if ( ATx [p] != X [j] )
                    {
                        PRINTF ("AFT error %s, row: %ld col: %ld "
                                "val in  AT (%e) != AFT (%e)\n",
                                where, (LONG) i, (LONG) j, ATx [p], X [j]) ;
                        pproj_error (-1, __FILE__, __LINE__, "stop") ;
                    }
                }
            }
            p = AFTp [i] ;
            q = p + AFTnz [i] ;
            for (; p < q; p++)
            {
                j = AFTi [p];
                if ( J [j] )
                {
                    PRINTF ("AFT error %s, row: %ld col: %ld "
                            "in AFT but not in AT\n",
                            where, (LONG) i, (LONG) j) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
                J [j] = 0 ;
            }
        }
    }

#if 0
    for (i = 0; i < nrow; i++)
    {
        if ( (AFTnz [i] > 0) && (ir [i] > ni) && use_ir )
        {
     
            PRINTF ("in %s AFTnz [%i] > 0 but ir = %i (row dropped, ni: %i)\n",
                     where, (LONG) i, (LONG) ir [i], (LONG) ni) ;
            pproj_error (-1, __FILE__, __LINE__, "stop") ;
        }
    }
#endif

    /* free workspace */
    pproj_free (J) ;
    pproj_free (X) ;
}
