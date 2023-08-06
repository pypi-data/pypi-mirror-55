/* ========================================================================== */
/* === check_minheap ======================================================== */
/* ========================================================================== */

#include "pproj.h"
void pproj_check_minheap
(
    PPINT   *heap,
    PPFLOAT   *x,
    PPINT     *ns,
    PPINT   nheap,
    PPINT    ntot,
    char *where
)
{
    PPINT j, k ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check minheap %s\n", where) ;

    for (k = 1; k <= nheap; k++)
    {
        if ( (heap [k] < 0) || (heap [k] >= ntot) )
        {
            PRINTF ("heap [%ld]: %ld, out of range 0 to ntot = %ld\n",
                   (LONG) k, (LONG) heap [k], (LONG) ntot) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    for (k = 1; k <= nheap; k++)
    {
        j = heap [k] ;
        if ( ns [j] != k )
        {
            PRINTF ("ns [%ld]: %ld, heap [%ld]: %ld\n",
                   (LONG) j, (LONG) ns [j], (LONG) k, (LONG) heap [k]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    j = 1 ;
    for (;;)
    {
        k = 2*j ;
        if ( k > nheap ) break ;
        if ( x [heap [k]] < x [heap [j]] )
        {
            PRINTF ("messed up at: j: %ld (heap: %ld x: %e) k: %ld "
                    "(heap: %ld x: %e)\n",
                    (LONG) j, (LONG) heap [j], x [heap [j]], (LONG) k,
                    (LONG) heap [k], x [heap [k]]) ;
     
            for (j = 0; j <= 27; j++)
            {
                PRINTF ("j: %ld heap: %ld x: %e\n",
                       (LONG) j, (LONG) heap [j], x [j]) ;
            }
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        k = 2*j + 1 ;
        if ( k > nheap ) break ;
        if ( x [heap [k]] < x [heap [j]] )
        {
            PRINTF ("messed up at: j: %ld (heap: %ld x: %e) k: %ld "
                    "(heap: %ld x: %e)\n",
                    (LONG) j, (LONG) heap [j], x [heap [j]], (LONG) k,
                    (LONG) heap [k], x [heap [k]]) ;
     
            for (j = 0; j <= 27; j++)
            {
                PRINTF ("j: %ld heap: %ld x: %e\n",
                       (LONG) j, (LONG) heap [j], x [j]) ;
            }
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        j++ ;
    }
}
