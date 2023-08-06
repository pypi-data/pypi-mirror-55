/* ========================================================================== */
/* ======= check_order ====================================================== */
/* ========================================================================== */

#include "pproj.h"
void pproj_check_order
(
    PPFLOAT   *x,
    PPINT     *I,
    PPINT length,
    char  *where
)
{
    PPINT i ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check order %s\n", where) ;

    for (i = 1; i < length; i++)
    {
        if ( x [I [i-1]] > x [I [i]] )
        {
            PRINTF ("Break points not sorted: %s\n", where) ;
            PRINTF ("i: %ld I: %ld value: %e prior: %e\n",
                   (LONG) i, (LONG) I [i], x [I[i-1]], x [I [i]]) ;
            pproj_error (-1, __FILE__, __LINE__, "Stop") ;
        }
    }
/*  PRINTF ("Break points sorted: %s\n", where) ; */
}
