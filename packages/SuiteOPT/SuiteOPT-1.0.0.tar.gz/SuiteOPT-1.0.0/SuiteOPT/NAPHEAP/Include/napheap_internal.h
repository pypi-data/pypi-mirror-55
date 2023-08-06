/* ========================================================================== */
/* === napheap_internal.h =================================================== */
/* ========================================================================== */

/* prototypes and definitions not visible to the caller */

#ifndef _NAPHEAP_INTERNAL_H_
#define _NAPHEAP_INTERNAL_H_

#include "napheap.h"

#define NONE    0
#define SECANT1 1
#define SECANT2 2
#define VARFIX  3
#define NEWTON  4

/* true infinity (ANSI C99) or DBL_MAX (ANSI C90) */

#define PRIVATE static
#define MAX(a,b) (((a) > (b)) ? (a) : (b))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))

/* additional status value, not returned to the user */
#define NAPHEAP_STATUS_KEEP_LOOKING     (-1)

/* -------------------------------------------------------------------------- */
/* macros for bounding a variable */
/* -------------------------------------------------------------------------- */

#define LOOP_OVER_UNFIXED \
nk = nuf ; \
nuf = 0 ; \
for (k = 0; k < nk; k++) \
{ \
    const NAPINT j = uf [k] ;

#define END_UNFIXED_LOOP \
    uf [nuf] = j ; \
    nuf++ ; \
}

#define LOOP_OVER_UNFIXED_NO_UF_UPDATE \
for (k = 0; k < nuf; k++) \
{ \
    const NAPINT j = uf [k] ;


#define END_LOOP \
}

#define FIX_LO \
const NAPFLOAT loj = (loExists) ? lo [j] : -NAPINF ; \
if ( x [j] == loj ) \
{ \
    b -= aj*loj ; \
    continue ; \
}

#define FIX_HI \
const NAPFLOAT hij = (hiExists) ? hi [j] : NAPINF ; \
if ( x [j] == hij ) \
{ \
    b -= aj*hij ; \
    continue ; \
}

#define VAR_FIX_LO \
if ( loExists && (x [j] == lo [j]) ) \
{ \
    b -= aj*lo [j] ; \
    const NAPFLOAT t = (d_is_one) ? aj*aj : aj*ad [j] ; \
    den -= t ; \
    num -= t*ay [j] ; \
    continue ; \
}

#define VAR_FIX_HI \
if ( hiExists && (x [j] == hi [j]) ) \
{ \
    b -= aj*hi [j] ; \
    const NAPFLOAT t = (d_is_one) ? aj*aj : aj*ad [j] ; \
    den -= t ; \
    num -= t*ay [j] ; \
    continue ; \
}

#define SLOPE_UPDATE_LO_NO_DEN \
const NAPFLOAT t = (d_is_one) ? y [j] - lambda*aj : \
                                (ay [j] - lambda)*ad [j] ; \
if ( t < loj ) \
{ \
    x [j] = loj ; \
    slope += aj*loj ; \
} \
else \
{ \
    if ( hiExists && (t > hi [j]) ) \
    { \
        x [j] = hi [j] ; \
        slope +=aj*hi [j] ; \
    } \
    else \
    { \
        x [j] = t ; \
        slope += aj*t ;

#define SLOPE_UPDATE_HI_NO_DEN \
const NAPFLOAT t = (d_is_one) ? y [j] - lambda*aj : \
                                (ay [j] - lambda)*ad [j] ; \
if ( t > hij) \
{ \
    x [j] = hij ; \
    slope +=aj*hij ; \
} \
else \
{ \
    if ( loExists && (t < lo [j]) ) \
    { \
        x [j] = lo [j] ; \
        slope += aj*lo [j] ; \
    } \
    else \
    { \
        x [j] = t ; \
        slope += aj*t ;

#define SLOPE_UPDATE_LO \
SLOPE_UPDATE_LO_NO_DEN \
    } \
}

#define SLOPE_UPDATE_LO_DEN \
SLOPE_UPDATE_LO_NO_DEN \
        den += (d_is_one) ? aj*aj : aj*ad [j] ; \
    } \
}

#define SLOPE_UPDATE_HI \
SLOPE_UPDATE_HI_NO_DEN \
    } \
}

#define SLOPE_UPDATE_HI_DEN \
SLOPE_UPDATE_HI_NO_DEN \
        den += (d_is_one) ? aj*aj : aj*ad [j] ; \
    } \
}

#define BRACKET \
lambdaL = -NAPINF ; \
lambdaR = NAPINF ; \
if ( slope0 < blo ) /* optimal multiplier < 0 */ \
{ \
     b = blo ; \
     slope0 -= b ; \
     dL = NAPINF ; \
     dR = slope0 ; \
     lambdaR = NAPZERO ; \
} \
else if ( slope0 > bhi ) /* optimal multiplier > 0 */ \
{ \
    b = bhi ; \
    slope0 -= b ; \
    dL = slope0 ; \
    dR = -NAPINF ; \
    lambdaL = NAPZERO ; \
} \
else /* lambda = 0 is optimal, blo <= a'x <= bhi */ \
{ \
    lambda = NAPZERO ; \
    for (k = 0; k < n; k++) \
    { \
        const NAPFLOAT t = (d_is_one) ? y [k] : y [k]/d [k] ; \
        if ( loExists && (t < lo [k]) ) \
        { \
            x [k] = lo [k] ; \
        } \
        else if ( hiExists && (t > hi [k]) ) \
        { \
            x [k] = hi [k] ; \
        } \
        else \
        { \
            x [k] = t ; \
        } \
    } \
    status = NAPHEAP_STATUS_OK ; \
    return (nap_wrapup (status, napdata, lambda)) ; \
}

/* -------------------------------------------------------------------------- */
/* prototypes of non-user callable functions */
/* -------------------------------------------------------------------------- */
PRIVATE int nap_wrapup
(
    int         status,
    NAPdata   *napdata,
    NAPFLOAT    lambda
) ;

PRIVATE int napsearch   /* return status of solution process */
(
    NAPFLOAT        *x, /* size n. solution (output) */
    NAPFLOAT   *lambda, /* optimal multiplier (input = guess, output = sol)*/
    NAPFLOAT   lambdaL, /* optimal multiplier lies on [lambdaL, lambdaR] */
    NAPFLOAT   lambdaR, /* optimal multiplier lies on [lambdaL, lambdaR] */
    NAPFLOAT         B, /* a'x = B */
    NAPFLOAT     slope, /* derivative of dual function */
    NAPFLOAT const *ay, /* size n. linear term in objective function yj/aj */
    NAPFLOAT const *ad, /* size n, diagonal of objective Hessian aj/dj */
    NAPFLOAT const  *a, /* size n, linear constraint vector */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPINT   const   n, /* problem dimension */
    NAPFLOAT *breakpts, /* size n, breakpts [j] is br_hi[j] or br_lo[j] */
    NAPFLOAT *breaknext,/* size n, TRUE if 2 break points in search dir. */
    NAPINT         nuf, /* number of unfixed variables */
    NAPINT *known_free, /* location of first known free variable in uf */
    NAPINT     *n_free, /* number of indices in free heap */
    NAPINT    *n_bound, /* number of indices in bound heap */
    NAPINT         *uf, /* size n, list of unfixed variables */
    NAPINT         *kf, /* size n, list of known free variables */
    NAPINT  *free_heap, /* size n+1, heap of free variables */
    NAPINT *bound_heap, /* size n+1, heap of bound variables */
    NAPstat      *Stat, /* solution statistics */
    NAPparm      *Parm, /* parameters */
    int const loExists, /* TRUE when there are lower bound for x */
    int const hiExists  /* TRUE when there are upper bound for x */
) ;

PRIVATE void napsearch0
(
    NAPFLOAT              *x, /* size n. solution (output) */
    NAPFLOAT         *lambda, /* optimal multiplier (in = guess, out = sol) */
    NAPFLOAT         lambdaL, /* optimal multiplier lies on [lambdaL, lambdaR]*/
    NAPFLOAT         lambdaR, /* optimal multiplier lies on [lambdaL, lambdaR]*/
    NAPFLOAT              *b, /* a'x = b */
    NAPFLOAT          *slope, /* slope (exclude break point term) */
    NAPFLOAT        *slopelo, /* lower subdifferential associated with break */
    NAPFLOAT        *slopehi, /* upper subdifferential associated with break */
    NAPINT   const         n, /* problem dimension */
    NAPFLOAT const        *a, /* size n, linear constraint vector */
    NAPFLOAT const       *lo, /* size n, lower bounds on x */
    NAPFLOAT const       *hi, /* size n, upper bounds on x */
    NAPFLOAT const *breakpts, /* size n, breakpts [j] is br_hi[j] or br_lo[j] */
    NAPINT               *uf, /* size n, list of unfixed variables */
    NAPINT         *nunfixed, /* number of unfixed variables */
    NAPINT       *bound_heap, /* size n+1, heap of bound variables */
    int              goright, /* if true, move right, else move left */
    NAPstat            *Stat, /* solution statistics */
    int      recompute_slope, /* if true, then recompute slope */
    NAPparm            *Parm, /* parameters */
    int      const  loExists, /* TRUE when there are lower bound for x */
    int      const  hiExists  /* TRUE when there are upper bound for x */

) ;

PRIVATE void napsearch1
(
    NAPFLOAT           *x,/* size n. solution (output) */
    NAPFLOAT      *lambda,/* optimal multiplier (input = guess, output = sol) */
    NAPFLOAT      lambdaL,/* optimal multiplier lies on [lambdaL, lambdaR] */
    NAPFLOAT      lambdaR,/* optimal multiplier lies on [lambdaL, lambdaR] */
    NAPFLOAT           *b,/* a'x = b */
    NAPFLOAT       *slope,/*  slope excluding term associated with break point*/
    NAPFLOAT     *slopelo,/* lower subdifferential associated with break point*/
    NAPFLOAT     *slopehi,/* upper subdifferential associated with break point*/
    NAPFLOAT const     *y,/* size n. linear term in objective function */
    NAPFLOAT const     *d,/* size n, diagonal of objective Hessian */
    NAPFLOAT const     *a,/* size n, linear constraint vector */
    NAPFLOAT const    *lo,/* size n, lower bounds on x */
    NAPFLOAT const    *hi,/* size n, upper bounds on x */
    NAPINT   const      n,/* problem dimension */
    NAPINT              K,/* number iterations in variable fixing method */
    NAPFLOAT    *breakpts,/* size n, breakpts [j] is br_hi[j] or br_lo[j] */
    NAPINT            *uf,/* size n, list of unfixed variables */
    NAPINT      *nunfixed,/* number of unfixed variables */
    NAPINT     *free_heap,/* size n+1, heap of free variables */
    NAPINT    *bound_heap,/* size n+1, heap of bound variables */
    int           goright,/* if true, move right, else move left */
    NAPstat         *Stat,/* solution statistics */
    NAPFLOAT const *br_lo,/* size n, br_lo[j] lo break pt for x[j] */
    NAPFLOAT const *br_hi,/* size n. br_hi[j] hi break pt for x[j] */
    int   recompute_slope,/* if true, then recompute slope */
    NAPparm         *Parm,/* parameters */
    int   const  loExists,/* TRUE when there are lower bound for x */
    int   const  hiExists /* TRUE when there are upper bound for x */
) ;

PRIVATE void napfix0
(
    NAPFLOAT        *x, /* size n. solution (output) */
    NAPFLOAT const  *a, /* size n, linear constraint vector */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPFLOAT        *b, /* b - ai*xi for fixed variables */
    NAPFLOAT    lambda, /* optimal multiplier */
    NAPINT         *uf, /* size n, list of unfixed variables */
    NAPINT   *nunfixed, /* number of unfixed variables */
    NAPFLOAT const *breakpts /* break points */
) ;

PRIVATE void napfix1
(
    NAPFLOAT        *x, /* size n. solution (output) */
    NAPFLOAT const  *a, /* size n, linear constraint vector */
    NAPFLOAT const  *y, /* size n. linear term in objective function */
    NAPFLOAT const  *d, /* size n, diagonal of objective Hessian */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPFLOAT        *b, /* b - ai*xi for fixed variables */
    NAPFLOAT    lambda, /* optimal multiplier */
    NAPINT         *uf, /* size n, list of unfixed variables */
    NAPINT   *nunfixed, /* number of unfixed variables */
    int const loExists, /* TRUE when there are lower bound for x */
    int const hiExists, /* TRUE when there are upper bound for x */
    NAPFLOAT const *breakpts /* break points */
) ;

PRIVATE void napsolution
(
    NAPFLOAT        *x, /* size n, solution (output) */
    NAPFLOAT const  *a, /* size n, coefficient of linear constraint */
    NAPFLOAT const  *y, /* size n, linear term in objective */
    NAPFLOAT const *ay, /* size n, linear term y in objective over a */
    NAPFLOAT const *ad, /* size n, coefficient of linear constraint over d */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPFLOAT    lambda, /* optimal multiplier */
    NAPINT   const *uf, /* size n, unfixed variables */
    NAPINT   const *kf, /* size n, known free variables */
    NAPINT         nuf, /* number of unfixed variables */
    NAPINT         nkf, /* number of known free variables */
    int const loExists, /* TRUE when there are lower bound for x */
    int const hiExists, /* TRUE when there are upper bound for x */
    int const d_is_one  /* TRUE when diagonal is identically one */
) ;

PRIVATE void napsolution0
(
    NAPFLOAT        *x, /* size n. solution (output) */
    NAPFLOAT const  *a, /* size n, linear constraint vector */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPFLOAT         B, /* the constraint is A'X = B */
    NAPFLOAT *breakpts, /* size n, breakpts [j] is br_hi[j] or br_lo[j] */
    NAPINT         *uf, /* size n, list of unfixed variables */
    NAPINT         nuf, /* number of unfixed variables */
    NAPINT  *free_heap, /* size n+1, heap of free variables */
    NAPINT *bound_heap, /* size n+1, heap of bound variables */
    int const loExists, /* TRUE when there are lower bound for x */
    int const hiExists  /* TRUE when there are upper bound for x */
) ;

PRIVATE void napsolution1
(
    NAPFLOAT        *x,  /* size n. solution (output) */
    NAPFLOAT const  *y,  /* size n. linear term in objective function */
    NAPFLOAT const  *d,  /* size n, diagonal of objective Hessian */
    NAPFLOAT const  *a,  /* size n, linear constraint vector */
    NAPFLOAT const *lo, /* size n, lower bounds on x */
    NAPFLOAT const *hi, /* size n, upper bounds on x */
    NAPFLOAT    lambda, /* optimal multiplier */
    NAPFLOAT     slope, /* slope of dual function determines search direction */
    NAPINT   const *kf,/* size n, known free variables */
    NAPINT         nkf, /* number of known free variables */
    NAPINT  *free_heap,
    NAPINT *bound_heap,
    NAPINT      n_free,
    NAPINT     n_bound,
    int const d_is_one
) ;

PRIVATE void napminheap_build
(
    NAPINT      *heap,  /* on input, unsorted set of indices.  size nheap+1 */
    NAPFLOAT const *X,  /* numbers to sort */
    NAPINT      nheap   /* number of elements to build into the heap */
) ;

PRIVATE NAPINT napminheap_delete  /* return new size of heap */
(
    NAPINT      *heap,  /* indices into X, 1..n on input.  size nheap+1 */
    NAPFLOAT const *X,  /* not modified */
    NAPINT      nheap   /* number of items in heap */
) ;

PRIVATE NAPINT napminheap_add
(
    NAPINT      *heap,  /* size n, containing indices into X.  size nheap+2 */
    NAPFLOAT const *X,  /* not modified */
    NAPINT       leaf,  /* the new leaf */
    NAPINT      nheap   /* number of elements in heap not counting new one */
) ;

PRIVATE void napminheapify
(
    NAPINT      *heap,  /* size nheap+1, containing indices into X */
    NAPFLOAT const *X,  /* not modified */
    NAPINT          p,  /* start at node p in the heap */
    NAPINT      nheap   /* heap [1 ... n] is in use */
) ;

PRIVATE void napmaxheap_build
(
    NAPINT      *heap,  /* on input, unsorted set of elements. size nheap+1 */
    NAPFLOAT const *X,  /* not modified */
    NAPINT      nheap   /* number of elements to build into the heap */
) ;

PRIVATE NAPINT napmaxheap_delete  /* return new size of heap */
(
    NAPINT      *heap,  /* containing indices into X, size nheap+1 */
    NAPFLOAT const *X,  /* not modified */
    NAPINT      nheap   /* number of items in heap */
) ;

PRIVATE NAPINT napmaxheap_add
(
    NAPINT      *heap,  /* size nheap+2, containing indices into X */
    NAPFLOAT const *X,  /* not modified */
    NAPINT       leaf,  /* the new leaf */
    NAPINT      nheap   /* number of elements in heap not counting new one */
) ;

PRIVATE void napmaxheapify
(
    NAPINT      *heap,  /* size nheap+1, containing indices into X */
    NAPFLOAT const *X,  /* not modified */
    NAPINT          p,  /* start at node p in the heap */
    NAPINT      nheap   /* heap [1 ... nheap] is in use */
) ;

PRIVATE void nap_infeasible
(
    NAPFLOAT        *x, /* size n. solution (output) */
    NAPFLOAT const  *a, /* size n. linear constraint vector */
    NAPFLOAT const *lo, /* size n. lower bounds for x */
    NAPFLOAT const *hi, /* size n. upper bounds for x */
    NAPINT         *uf, /* size n, list of unfixed variables */
    NAPINT         nuf, /* number of unfixed variables */
    NAPFLOAT     minax,
    NAPFLOAT     maxax,
    NAPFLOAT       blo, /* lower bound for a'x */
    NAPFLOAT       bhi  /* upper bound for a'x */
) ;

PRIVATE int nap_work
(
    NAPINT  const      n,
    NAPFLOAT      *xWork,     /* user-provide workspace */
    NAPFLOAT       **xw2,     /* return malloc'ed space */

    /* the 6 work arrays, each of size n */
    NAPFLOAT        **ad,
    NAPFLOAT        **ay,
    NAPFLOAT     **br_hi,
    NAPFLOAT     **br_lo,
    NAPFLOAT  **breakpts,
    NAPFLOAT **breaknext
) ;

PRIVATE NAPFLOAT nap_dot
(
    const NAPFLOAT *x, /* first vector */
    const NAPFLOAT *y, /* second vector */
    const NAPINT    n  /* length of vectors */
) ;

#endif
