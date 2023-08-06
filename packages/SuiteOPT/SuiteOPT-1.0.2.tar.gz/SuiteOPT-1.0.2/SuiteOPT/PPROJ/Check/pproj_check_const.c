/* ========================================================================= */
/* === check_const ========================================================= */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_const
(
    PPFLOAT  *x,
    PPFLOAT  cx,
    PPINT    *y,
    PPINT    cy,
    PPINT     n,
    char *where
)
{
    PPINT i ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check for constant value %s\n", where) ;

    if ( x != NULL )
    for (i = 0; i < n; i++)
    {
        if ( x [i] != cx )
        {
            printf ("x [%ld] = %e != %e\n", (LONG) i, x [i], cx) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    if ( y != NULL )
    for (i = 0; i < n; i++)
    {
        if ( y [i] != cy )
        {
            printf ("y [%ld] = %ld != %ld\n",
                   (LONG) i, (LONG) y [i], (LONG) cy) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
}
