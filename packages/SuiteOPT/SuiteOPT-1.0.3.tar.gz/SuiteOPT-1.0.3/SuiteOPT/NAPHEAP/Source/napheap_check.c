/* ========================================================================== */
/* === Source/napheap_check.c =============================================== */
/* ========================================================================== */

#include "napheap.h"

#include <math.h>
#include <stdlib.h>

#define MAX(a,b) (((a) > (b)) ? (a) : (b))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))

/*  Determine KKT error in a solution to the separable convex quadratic
    knapsack problem:

    min .5x'Dx - y'x  subject to  lo <= x <= hi, blo <= b <= bhi, a'x = b

    Here D is a diagonal matrix with nonnegative diagonal entries.
    Input is the solution x and the Lagrange multiplier lambda associated
    with the constraint a'x = b. The code determines the smallest perturbations
    in b, y, lo, hi, and lambda with the property that x and lambda satisfy
    the KKT conditions for the perturbed problem. The KKT conditions are the
    following:

    1. If b = a'x, then b = bhi if lambda > 0
                        b = blo if lambda < 0
                        b in [blo, bhi] if lambda = 0

    2. lo [j] <= x [j] <= hi [j]

    3. If D [j,j] = 0, then x [j] = hi [j] if a [j]*lambda - y [j] < 0
                            x [j] = lo [j] if a [j]*lambda - y [j] > 0
       If D [j,j] > 0, then

        x [j] = mid {lo [j], (y [j] - a [j]*lambda)/D [j,j], hi [j]}

       Here `mid' denotes the mean (or middle) of the three quantities.

    The code returns the relative 1-norm of the minimum perturbations
    in b, y, lo, hi, and lambda that are needed to satisfy these conditions.
    These are output in 3 arguments:

    errb: (|pert b|+|pert lambda|)/ sum |a [j]*x [j]|

    errB: ||pert lo||_1 + ||pert hi||_1 over the 1-norm of the corresponding
          original components

    erry: ||pert y||_1 over the 1-norm of the corresponding original components

    This function does not check to see if the input problem is valid or not.
    In particular, all entries in D must be >= 0, and lo [j] <= hi [j] must
    also hold for all j.  Napheap checks these conditions if Parm->check is
    true.  However, in this function, any d[j]<0 is treated as zero.
    If lo [j] > hi [j] for any j, the result of this function is undefined.
*/

NAPFLOAT napheap_check /* returns largest of the 3 error values */
(
    NAPFLOAT     *errb, /* relative error in b (only return if not NULL) */
    NAPFLOAT     *errB, /* relative error in bounds (only return if not NULL) */
    NAPFLOAT     *erry, /* relative error in y (only return if not NULL) */
    NAPdata   *napdata
)
{
    NAPINT j ;
    NAPFLOAT ax, loj, hij, t, s, err, normB, normy,
             pertb, pertB, perty, dj ;

    NAPFLOAT const  *x = napdata->x ;      /* size n, solution */
    NAPFLOAT    lambda = napdata->lambda ; /* multiplier (scalar) */
    NAPINT           n = napdata->n ;      /* problem dimension */
    NAPFLOAT const  *y = napdata->y ;      /* size n, linear term in objective*/
    NAPFLOAT const  *d = napdata->d ;      /* size n, diagonal of cost Hessian*/
    NAPFLOAT const  *a = napdata->a ;      /* size n, linear constraint vector*/
    NAPFLOAT       blo = napdata->blo ;    /* lower bound for a'x */
    NAPFLOAT       bhi = napdata->bhi ;    /* upper bound for a'x */
    NAPFLOAT const *lo = napdata->lo ;     /* size n, lower bounds for x */
    NAPFLOAT const *hi = napdata->hi ;     /* size n, upper bounds for x */
    NAPparm      *Parm = napdata->Parm ;   /* parameter structure */

    /* get the bounds on b, and swap blo and bhi to ensure blo <= bhi */
    int const d_is_zero = (d == NULL) ? TRUE : Parm->d_is_zero ;
    int const d_is_one  = Parm->d_is_one ;
    int const y_is_zero = (y == NULL) ;
    int const loExists  = (lo == NULL) ? FALSE : Parm->loExists ;
    int const hiExists  = (hi == NULL) ? FALSE : Parm->hiExists ;
    if ( blo > bhi )
    {
        t = blo ;
        blo = bhi ;
        bhi = t ;
    }

    /* determine b perturbation */
    t = NAPZERO ;
    ax = NAPZERO ;
    for (j = 0; j < n; j++)
    {
        s = a [j]*x [j] ;
        t += s ;
        ax += fabs (s) ;
    }

/*printf ("blo: %e a'x: %e bhi: %e lambda: %e\n", blo, t, bhi, lambda) ;*/
    if ( lambda > NAPZERO )
    {
        pertb = fabs (t-bhi) ;
        if ( lambda < pertb ) /* less change if lambda is perturbed */
        {
            pertb = lambda ;
        }
    }
    else if ( lambda < NAPZERO )
    {
        pertb = fabs (t-blo) ;
        if ( -lambda < pertb ) /* less change if lambda is perturbed */
        {
            pertb = -lambda ;
        }
    }
    else
    {
        pertb = MAX (blo-t, NAPZERO) ;
        pertb = MAX (t-bhi, pertb) ;
    }
    /* error relative to sum |aj*xj| */
    if ( ax > NAPZERO ) pertb /= ax ;

    /* determine perturbations in bounds and in y */
    pertB = NAPZERO ;
    normB = NAPZERO ;
    perty = NAPZERO ;
    normy = NAPZERO ;
    dj = NAPZERO ;
    for (j = 0; j < n; j++)
    {
        NAPFLOAT const LOj = (loExists) ? lo [j] : -NAPINF ;
        NAPFLOAT const HIj = (hiExists) ? hi [j] :  NAPINF ;
        loj = LOj ;
        hij = HIj ;
        if      ( x [j] < loj ) loj = x [j] ;
        else if ( x [j] > hij ) hij = x [j] ;
        if      ( d_is_zero ) dj = NAPZERO ;
        else if ( d_is_one )  dj = (NAPFLOAT) 1 ;
        else                  dj = d [j] ;
        NAPFLOAT const yj = ( y_is_zero ) ? NAPZERO : y [j] ;
        if ( dj > NAPZERO )
        {
            t = dj*x [j] + a [j]*lambda ; /* yj that yields x [j] */
            s = fabs (t - yj) ;           /* perturbation in y */
            /* we have the choice of perturbing y, lo, or hi */
             /*can eliminate y pert by moving hij to x [j]*/
            if ( yj > t )
            {
                if ( hij - x [j] < s ) /* pert in hi < pert in y */
                {
                    hij = x [j] ;
                    s = NAPZERO ;
                }
            }
            else /* yj <= t, can move loj to x [j] */
            {
                if ( x [j] - loj < s ) /* pert in lo < pert in y */
                {
                    loj = x [j] ;
                    s = NAPZERO ;
                }
            }
        }
        else /* d [j] assumed to be 0 */
        {
            /*  x [j] = hi [j] if a [j]*lambda - yj < 0
                x [j] = lo [j] if a [j]*lambda - yj > 0
                we have the choice of perturbing y, lo, or hi */
            t = a [j]*lambda - yj ;
            s = fabs (t) ;
            if ( t < NAPZERO )
            {
                if ( hij - x [j] < s ) /* pert hi < pert y */
                {
                    hij = x [j] ;
                    s = NAPZERO ;
                }
            }
            else /* t <= 0 */
            {
                if ( x [j] - loj < s ) /* pert lo < pert y */
                {
                    loj = x [j] ;
                    s = NAPZERO ;
                }
            }
        }

        /* accumulate the errors */
        normy += fabs (yj) ;
        if ( s > NAPZERO )
        {
            perty += s ;
        }
        if ( loj != LOj )
        {
            pertB += fabs (loj-LOj) ;
            normB += fabs (LOj) ;
        }
        if ( hij != HIj )
        {
            pertB += fabs (hij-HIj) ;
            normB += fabs (HIj) ;
        }
    }
    if ( normy > NAPZERO ) perty /= normy ;
    if ( normB > NAPZERO ) pertB /= normB ;

    if ( errb != NULL ) *errb = pertb ;
    if ( errB != NULL ) *errB = pertB ;
    if ( erry != NULL ) *erry = perty ;

    /* return the largest error */
    err = MAX (pertb, perty) ;
    err = MAX (err, pertB) ;
    return (err) ;
}
