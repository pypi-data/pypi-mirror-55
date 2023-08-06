/* ========================================================================== */
/* === Demo/napheap_demo.c ================================================== */
/* ========================================================================== */

/* simple stand-alone demo program for napheap */

#include "napheap.h"
#include <stdlib.h>
#include <stdio.h>

#define MAX(a,b) (((a) > (b)) ? (a) : (b))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))

/* portable replacement for rand, for repeatable results */
static unsigned long next = 1 ;
#define MY_RAND_MAX 32767
static int myrand ( void )
{
    next = next * 1103515245 + 12345;
    return ((unsigned) (next / 65536) % (MY_RAND_MAX + 1)) ;
}


/* generate a random number between lower and upper */
static NAPFLOAT rnum
(
    NAPFLOAT lower,
    NAPFLOAT upper
)
{
    NAPFLOAT diff, t ;
    t = ((NAPFLOAT) myrand ()) / MY_RAND_MAX ;
    diff = upper - lower ;
    t = t*diff + lower ;
    return (t) ;
}

static void print_vector (char *name, NAPFLOAT *x, NAPINT n)
{
    NAPINT j ;
    printf ("\n%s:\n", name) ;
    for (j = 0; j < n; j++)
    {
        /* use ((NAPFLOAT) j) since j could be int (%d) or long (%ld) */
        printf ("%s [%ld] = %g\n", name, (LONG) j, x [j]) ;
    }
}


int main (void)
{
    NAPFLOAT s, t, cumlo, cumhi, l, u, err, err1, *y, *d, *a, *lo, *hi ;
    NAPINT j, n ;
    int status, ok ;
    NAPdata *napdata ;
    NAPparm *Parm ;
    NAPstat *Stat ;

    printf ("\nNAPHEAP demo.  Version %d.%d.%d, %s\n", NAPHEAP_MAIN_VERSION,
        NAPHEAP_SUB_VERSION, NAPHEAP_SUBSUB_VERSION, NAPHEAP_DATE) ;

    /* set up the input data structure */
    napdata = napheap_setup () ;

    /* The setup code also initialized the parameters to their default values.
       Access the parameters using: */
    Parm = napdata->Parm ;
    Stat = napdata->Stat ;

    /* To print the parameters: */
    napheap_print_parm (napdata) ;

    /* ---------------------------------------------------------------------- */
    /* randomly generate a problem and store it in napdata structure */
    /* ---------------------------------------------------------------------- */

    napdata->n  = n  = 20 ;
    napdata->y  = y  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
    napdata->d  = d  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
    napdata->a  = a  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
    napdata->lo = lo = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
    napdata->hi = hi = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
    cumlo = 0 ;
    cumhi = 0 ;
    for (j = 0; j < n; j++)
    {
        /* dj = random number on (5, 10) */
        d [j] = rnum (5, 10) ;
        /* yj = random number on (-10, 10) */
        y [j] = rnum (-10, 10) ;
        a [j] = rnum (-10, 10) ;
        lo [j] = -1 ;
        hi [j] = +1 ;
        t = a [j]*lo [j] ;
        s = a [j]*hi [j] ;
        /* cumlo = min a'x */
        cumlo += MIN (t, s) ;
        /* cumhi = max a'x */
        cumhi += MAX (t, s) ;
    }
    l = rnum (cumlo, cumhi) ;
    u = l + 10 ;
    napdata->blo = l ;
    napdata->bhi = u ;

    printf ("\nminimize 0.5x'Dx - y'x subject to lo <= x <= hi and "
        "blo <= a'x <= bhi\n") ;

    printf ("blo = %g, bhi = %g\n", l, u) ;
    printf ("D is diagonal, with d = diag(D):\n") ;
    print_vector ("d", d, n) ;
    print_vector ("y", y, n) ;
    print_vector ("lo", lo, n) ;
    print_vector ("hi", hi, n) ;
    print_vector ("a", a, n) ;

    /* solve the problem with default parameters */
    status = napheap (napdata) ;
    ok = (status == NAPHEAP_STATUS_OK) ;

    /* print the solution status */
    napheap_print_status (napdata) ;

    /* If there was an error, then the command
           napheap_print_status (napdata) ;
       could provide more information concerning the error. */

    /* print statistics for the run */
    napheap_print_stat (napdata) ;

    /* estimate the error in the solution */
    err = napheap_check (NULL, NULL, NULL, napdata) ;

    printf ("relative error: %g\n", err) ;
    
    printf ("The solution is:\n") ;
    print_vector ("x", napdata->x, n) ;

    /* ---------------------------------------------------------------------- */
    /* resolve the problem using the previously computed multiplier lambda
       as the starting guess. The multiplier was stored in napdata->lambda. */
    /* ---------------------------------------------------------------------- */

    printf ("\n=============================================\n") ;
    printf ("Resolve the problem using the previously computed\n") ;
    printf ("multiplier as the starting guess:\n") ;

    /* solve the problem */
    status = napheap (napdata) ;

    napheap_print_parm (napdata) ;
    napheap_print_status (napdata) ;

    printf ("\nNote that the number of Newton iterations is 1 due to "
            "the good starting guess:\n") ;
    napheap_print_stat (napdata) ;
    ok = ok && (status == NAPHEAP_STATUS_OK) ;
    err1 = napheap_check (NULL, NULL, NULL, napdata) ;
    printf ("relative error: %g\n", err1) ;
    err = MAX (err, err1) ;

    /* ---------------------------------------------------------------------- */
    /* resolve the problem using the previously computed multiplier lambda
       as the starting guess and purely the break point searching algorithm */
    /* ---------------------------------------------------------------------- */

    Parm->K = 0 ;
    printf ("\n=============================================\n") ;
    printf ("Resolve the problem using the previously computed\n") ;
    printf ("multiplier as the starting guess and purely the break point\n") ;
    printf ("searching algorithm. Note that the number of break\n") ;
    printf ("to reach the solution is 0:\n") ;
    status = napheap (napdata) ;

    napheap_print_parm (napdata) ;
    napheap_print_status (napdata) ;
    napheap_print_stat (napdata) ;
    ok = ok && (status == NAPHEAP_STATUS_OK) ;
    err1 = napheap_check (NULL, NULL, NULL, napdata) ;
    printf ("relative error: %g\n", err1) ;
    err = MAX (err, err1) ;

    /* ---------------------------------------------------------------------- */
    /* set a diagonal element to 0 to generate an error message */
    /* ---------------------------------------------------------------------- */

    /* NOTE: To check the input parameters for dj < 0 or hij < loj or
             Bhi < Blo, set Parm->check = TRUE */

    Parm->check = TRUE ;
    printf ("\n=============================================\n") ;
    printf ("Set a diagonal element to 0 to generate an error message\n") ;
    printf ("The default method is Newton, which requires that d > 0.\n") ;
    d [4] = 0 ;
    status = napheap (napdata) ;
    napheap_print_status (napdata) ;
    napheap_print_stat (napdata) ;
    ok = ok && (status != NAPHEAP_STATUS_OK) ;
    if (ok)
    {
        printf ("error expected and properly detected.  Newton's method\n"
                "(the default) can only be used when d is all positive.\n") ;
    }
    else
    {
        printf ("TEST ERROR.  Problem is invalid but this was not detected\n") ;
    }

    /* ---------------------------------------------------------------------- */
    /* use a different method when the diagonal has zeros or is identically 0 */
    /* ---------------------------------------------------------------------- */

    Parm->newton = FALSE ;     /* can use Newton only when all (d>0) */
    Parm->d_is_zero = TRUE ;   /* same as setting napdata->d = NULL */
    printf ("\n=============================================\n") ;
    printf ("Solve with d=0, without using Newton's method\n") ;
    status = napheap (napdata) ;
    napheap_print_parm (napdata) ;
    napheap_print_status (napdata) ;
    napheap_print_stat (napdata) ;
    ok = ok && (status == NAPHEAP_STATUS_OK) ;
    err1 = napheap_check (NULL, NULL, NULL, napdata) ;
    printf ("relative error: %g\n", err1) ;
    err = MAX (err, err1) ;

    /* ---------------------------------------------------------------------- */
    /* repeat, but use work arrays provided by user */
    /* ---------------------------------------------------------------------- */
    napdata->xWork = (NAPFLOAT *) malloc (5*n*sizeof (NAPFLOAT)) ;
    napdata->iWork = (NAPINT *) malloc ((4*n+2)*sizeof (NAPINT)) ;

    printf ("\n=============================================\n") ;
    printf ("Repeat the above solution with user-provided work arrays\n") ; 
    printf ("This will solve very quickly since the prior run stored\n") ; 
    printf ("the multiplier in napdata->lambda, and prior multiplier\n") ; 
    printf ("becomes the starting guess.\n") ; 
    status = napheap (napdata) ;
    napheap_print_parm (napdata) ;
    napheap_print_status (napdata) ;
    napheap_print_stat (napdata) ;
    ok = ok && (status == NAPHEAP_STATUS_OK) ;
    err1 = napheap_check (NULL, NULL, NULL, napdata) ;
    printf ("relative error: %g\n", err1) ;
    err = MAX (err, err1) ;

    /* free memory that the user created */
    free (d) ;
    free (a) ;
    free (y) ;
    free (lo) ;
    free (hi) ;
    free (napdata->xWork) ;
    free (napdata->iWork) ;

    /* free any remaining memory associated with the napdata structure */
    printf ("\nUse napheap_terminate to free any remaining memory associated\n"
            "with the napdata structure. Since the user did not allocate\n"
            "the solution array napdata->x, the memory for this array will\n"
            "also be freed by napheap_terminate.\n") ;
    napheap_terminate (&napdata) ;

    printf ("\n\nOverall results: worst-case relative error: %g\n", err) ;
    if (ok && err < 1e-6)
    {
        printf ("\nAll tests passed.\n") ;
    }
    else
    {
        printf ("\nTEST FAILURE.\n") ;
    }
    
    return (0) ;
}
