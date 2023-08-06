#include "cg_descent.h"

/* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       Utility Routines
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! */

/* =========================================================================
   ==== cg_scale ===========================================================
   =========================================================================
   compute y = s*x where s is a scalar
   ========================================================================= */
void cg_scale
(
    CGFLOAT *y, /* output vector */
    CGFLOAT *x, /* input vector */
    CGFLOAT  s, /* scalar */
    CGINT    n  /* length of vector */
)
{
    CGINT i, n5 ;
    n5 = n % 5 ;
    if ( y == x)
    {
#ifdef NOBLAS
        for (i = 0; i < n5; i++) y [i] *= s ;
        for (; i < n;)
        {
            y [i] *= s ;
            i++ ;
            y [i] *= s ;
            i++ ;
            y [i] *= s ;
            i++ ;
            y [i] *= s ;
            i++ ;
            y [i] *= s ;
            i++ ;
        }
#else
        if ( n < DSCAL_START )
        {
            for (i = 0; i < n5; i++) y [i] *= s ;
            for (; i < n;)
            {
                y [i] *= s ;
                i++ ;
                y [i] *= s ;
                i++ ;
                y [i] *= s ;
                i++ ;
                y [i] *= s ;
                i++ ;
                y [i] *= s ;
                i++ ;
            }
        }
        else
        {
            BLAS_INT int_one = 1 ;
            BLAS_INT N ;
            N = (BLAS_INT) n ;
            CG_DSCAL (&N, &s, x, &int_one) ;
        }
#endif
    }
    else
    {
        if ( s == -CGONE )
        {
            for (i = 0; i < n5; i++) y [i] = -x [i] ;
            for (; i < n;)
            {
                y [i] = -x [i] ;
                i++ ;
                y [i] = -x [i] ;
                i++ ;
                y [i] = -x [i] ;
                i++ ;
                y [i] = -x [i] ;
                i++ ;
                y [i] = -x [i] ;
                i++ ;
            }
        }
        else
        {
            for (i = 0; i < n5; i++) y [i] = s*x [i] ;
            for (; i < n;)
            {
                y [i] = s*x [i] ;
                i++ ;
                y [i] = s*x [i] ;
                i++ ;
                y [i] = s*x [i] ;
                i++ ;
                y [i] = s*x [i] ;
                i++ ;
                y [i] = s*x [i] ;
                i++ ;
            }
        }
    }
    return ;
}

/* =========================================================================
   ==== cg_daxpy ===========================================================
   =========================================================================
   Compute x = x + alpha d
   ========================================================================= */
void cg_daxpy
(
    CGFLOAT    *x, /* input and output vector */
    CGFLOAT    *d, /* direction */
    CGFLOAT alpha, /* stepsize */
    CGINT       n  /* length of the vectors */
)
{
#ifdef NOBLAS
    CGINT i, n5 ;
    n5 = n % 5 ;
    if (alpha == -CGONE)
    {
        for (i = 0; i < n5; i++) x [i] -= d[i] ;
        for (; i < n; i += 5)
        {
            x [i]   -= d [i] ;
            x [i+1] -= d [i+1] ;
            x [i+2] -= d [i+2] ;
            x [i+3] -= d [i+3] ;
            x [i+4] -= d [i+4] ;
        }
    }
    else
    {
        for (i = 0; i < n5; i++) x [i] += alpha*d[i] ;
        for (; i < n; i += 5)
        {
            x [i]   += alpha*d [i] ;
            x [i+1] += alpha*d [i+1] ;
            x [i+2] += alpha*d [i+2] ;
            x [i+3] += alpha*d [i+3] ;
            x [i+4] += alpha*d [i+4] ;
        }
    }
#else
    CGINT i, n5 ;
    if ( n < DAXPY_START )
    {
        n5 = n % 5 ;
        if (alpha == -CGONE)
        {
            for (i = 0; i < n5; i++) x [i] -= d[i] ;
            for (; i < n; i += 5)
            {
                x [i]   -= d [i] ;
                x [i+1] -= d [i+1] ;
                x [i+2] -= d [i+2] ;
                x [i+3] -= d [i+3] ;
                x [i+4] -= d [i+4] ;
            }
        }
        else
        {
            for (i = 0; i < n5; i++) x [i] += alpha*d[i] ;
            for (; i < n; i += 5)
            {
                x [i]   += alpha*d [i] ;
                x [i+1] += alpha*d [i+1] ;
                x [i+2] += alpha*d [i+2] ;
                x [i+3] += alpha*d [i+3] ;
                x [i+4] += alpha*d [i+4] ;
            }
        }
    }
    else
    {
        BLAS_INT N ;
        BLAS_INT int_one = 1 ;
        N = (BLAS_INT) n ;
        CG_DAXPY (&N, &alpha, d, &int_one, x, &int_one) ;
    }
#endif

    return ;
}

/* =========================================================================
   ==== cg_dot =============================================================
   =========================================================================
   Compute dot product of x and y, vectors of length n
   ========================================================================= */
CGFLOAT cg_dot
(
    CGFLOAT       *x, /* first vector */
    CGFLOAT       *y, /* second vector */
    CGINT   const  n  /* length of vectors */
)
{
#ifdef NOBLAS
    CGINT i, n5 ;
    CGFLOAT t ;
    t = CGZERO ;
    if ( n <= 0 ) return (t) ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) t += x [i]*y [i] ;
    for (; i < n; i += 5)
    {
        t += x [i]*y[i] + x [i+1]*y [i+1] + x [i+2]*y [i+2]
                        + x [i+3]*y [i+3] + x [i+4]*y [i+4] ;
    }
    return (t) ;
#else
    CGINT i, n5 ;
    CGFLOAT t ;
    if ( n < DDOT_START )
    {
        t = CGZERO ;
        if ( n <= 0 ) return (t) ;
        n5 = n % 5 ;
        for (i = 0; i < n5; i++) t += x [i]*y [i] ;
        for (; i < n; i += 5)
        {
            t += x [i]*y[i] + x [i+1]*y [i+1] + x [i+2]*y [i+2]
                            + x [i+3]*y [i+3] + x [i+4]*y [i+4] ;
        }
        return (t) ;
    }
    else
    {
        BLAS_INT N ;
        BLAS_INT int_one = 1 ;
        N = (BLAS_INT) n ;
        return (CG_DDOT (&N, x, &int_one, y, &int_one)) ;
    }
#endif
}

/* =========================================================================
   === cg_copy =============================================================
   =========================================================================
   Copy vector x into vector y
   ========================================================================= */
void cg_copy
(
    CGFLOAT       *y, /* output of copy */
    CGFLOAT       *x, /* input of copy */
    CGINT   const  n  /* length of vectors */
)
{
#ifdef NOBLAS
    CGINT i, n5 ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; )
    {
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
    }
#else
    CGINT i, n5 ;
    BLAS_INT N ;
    if ( n < DCOPY_START )
    {
        n5 = n % 5 ;
        for (i = 0; i < n5; i++) y [i] = x [i] ;
        for (; i < n; )
        {
            y [i] = x [i] ;
            i++ ;
            y [i] = x [i] ;
            i++ ;
            y [i] = x [i] ;
            i++ ;
            y [i] = x [i] ;
            i++ ;
            y [i] = x [i] ;
            i++ ;
        }
    }
    else
    {
        BLAS_INT int_one  = 1 ;
        N = (BLAS_INT) n ;
        CG_DCOPY (&N, x, &int_one, y, &int_one) ;
    }
#endif

    return ;
}

/* =========================================================================
   ==== cg_matvec ==========================================================
   =========================================================================
   Compute y = A*x or A'*x where A is a dense rectangular matrix
   ========================================================================= */
void cg_matvec
(
    CGFLOAT *y, /* product vector */
    CGFLOAT *A, /* dense matrix */
    CGFLOAT *x, /* input vector */
    CGINT    n, /* number of columns of A */
    CGINT    m, /* number of rows of A */
    int      w  /* T => y = A*x, F => y = A'*x */
)
{
/* if the blas have not been installed, then hand code the product */
#ifdef NOBLAS
    CGINT j, l ;
    l = 0 ;
    if ( w )
    {
        cg_scale0 (y, A, x [0], (int) m) ;
        for (j = 1; j < n; j++)
        {
            l += m ;
            cg_daxpy0 (y, A+l, x [j], (int) m) ;
        }
    }
    else
    {
        for (j = 0; j < n; j++)
        {
            y [j] = cg_dot0 (A+l, x, (int) m) ;
            l += m ;
        }
    }
#else

/* if the blas have been installed, then possibly call gdemv */
    if ( w || (!w && (m*n < MATVEC_START)) )
    {
        CGINT j, l ;
        l = 0 ;
        if ( w )
        {
            cg_scale (y, A, x [0], m) ;
            for (j = 1; j < n; j++)
            {
                l += m ;
                cg_daxpy (y, A+l, x [j], m) ;
            }
        }
        else
        {
            for (j = 0; j < n; j++)
            {
                y [j] = cg_dot0 (A+l, x, (int) m) ;
                l += m ;
            }
        }
    }
    else
    {
        BLAS_INT int_one = 1 ;
        BLAS_INT M, N ;
        CGFLOAT float_one, float_zero ;
        M = (BLAS_INT) m ;
        N = (BLAS_INT) n ;
        float_zero = (CGFLOAT) 0 ;
        float_one = (CGFLOAT) 1 ;
        /* only use transpose mult with blas
          CG_DGEMV ("n", &M, &N, one, A, &M, x, blas_one, zero, y, blas_one) ;*/
        CG_DGEMV ("t", &M, &N, &float_one , A, &M, x, &int_one, &float_zero,
                   y, &int_one) ;
    }
#endif

    return ;
}

/* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       End of routines that could use the BLAS
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! */

/* =========================================================================
   ==== cg_step ============================================================
   =========================================================================
   Compute xnew = x + alpha d
   ========================================================================= */
void cg_step
(
    CGFLOAT  *xnew, /*output vector */
    CGFLOAT     *x, /* initial vector */
    CGFLOAT     *d, /* search direction */
    CGFLOAT  alpha, /* stepsize */
    CGINT        n  /* length of the vectors */
)
{
    CGINT n5, i ;
    n5 = n % 5 ;
    if (alpha == -CGONE)
    {
        for (i = 0; i < n5; i++)
        {
            xnew [i] = x [i] - d [i] ;
        }
        for (; i < n; i += 5)
        {
            xnew [i]   = x [i]   - d [i] ;
            xnew [i+1] = x [i+1] - d [i+1] ;
            xnew [i+2] = x [i+2] - d [i+2] ;
            xnew [i+3] = x [i+3] - d [i+3] ;
            xnew [i+4] = x [i+4] - d [i+4] ;
        }
    }
    else if ( alpha == CGONE )
    {
        for (i = 0; i < n5; i++)
        {
            xnew [i] = x [i] + d [i] ;
        }
        for (; i < n; i += 5)
        {
            xnew [i]   = x [i]   + d [i] ;
            xnew [i+1] = x [i+1] + d [i+1] ;
            xnew [i+2] = x [i+2] + d [i+2] ;
            xnew [i+3] = x [i+3] + d [i+3] ;
            xnew [i+4] = x [i+4] + d [i+4] ;
        }
    }
    else
    {
        for (i = 0; i < n5; i++)
        {
            xnew [i] = x[i] + alpha*d[i] ;
        }
        for (; i < n; i += 5)
        {
            xnew [i]   = x [i]   + alpha*d [i] ;
            xnew [i+1] = x [i+1] + alpha*d [i+1] ;
            xnew [i+2] = x [i+2] + alpha*d [i+2] ;
            xnew [i+3] = x [i+3] + alpha*d [i+3] ;
            xnew [i+4] = x [i+4] + alpha*d [i+4] ;
        }
    }
    return ;
}

/* =========================================================================
   ===================== cg_initi ==========================================
   =========================================================================
   Initialize a CGINT array
   ========================================================================= */
void cg_initi
(
    CGINT *x,  /* array to be initialized */
    CGINT  s,  /* scalar */
    CGINT  n   /* length of x */
)
{
    CGINT j, n5 ;
    CGINT *xj ;
    n5 = n % 5 ;
    for (j = 0; j < n5; j++) x [j] = s ;
    xj = x+j ;
    for (; j < n; j += 5)
    {
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
    }
}

/* =========================================================================
   ==== cg_initx ===========================================================
   =========================================================================
   initialize x to a given scalar value
   ========================================================================= */
void cg_initx
(
    CGFLOAT *x, /* input and output vector */
    CGFLOAT  s, /* scalar */
    CGINT    n  /* length of vector */
)
{
    CGINT i, n5 ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) x [i] = s ;
    for (; i < n;)
    {
        x [i] = s ;
        i++ ;
        x [i] = s ;
        i++ ;
        x [i] = s ;
        i++ ;
        x [i] = s ;
        i++ ;
        x [i] = s ;
        i++ ;
    }
    return ;
}

/* =========================================================================
   ==== cg_update_2 ========================================================
   =========================================================================
   Set gold = gnew (if not equal), compute 2-norm^2 of gnew, and optionally
      set d = -gnew
   ========================================================================= */
CGFLOAT cg_update_2
(
    CGFLOAT *gold, /* old g */
    CGFLOAT *gnew, /* new g */
    CGFLOAT    *d, /* d */
    CGINT       n  /* length of vectors */
)
{
    CGINT i, n5 ;
    CGFLOAT s, t ;
    t = CGZERO ;
    n5 = n % 5 ;

    if ( gold != NULL )
    {
        for (i = 0; i < n5; i++)
        {
            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
        }
        for (; i < n; )
        {
            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            gold [i] = s ;
            d [i] = -s ;
            i++ ;
        }
    }
    else
    {
        for (i = 0; i < n5; i++)
        {
            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
        }
        for (; i < n; )
        {
            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
            i++ ;

            s = gnew [i] ;
            t += s*s ;
            d [i] = -s ;
            i++ ;
        }
    }
    return (t) ;
}

/* =========================================================================
   ==== cg_update_beta =====================================================
   =========================================================================
   compute: ykPyk  = (newproj - oldproj)*(newproj - oldproj),
            gkPyk  =  newproj           *(newproj - oldproj)
   update: oldproj = newproj
   ========================================================================= */
void cg_update_beta
(
    CGFLOAT *oldproj,
    CGFLOAT *newproj,
    CGFLOAT   *GkPyk,
    CGFLOAT   *YkPyk,
    CGINT          n  /* length of vectors */
)
{
    CGINT i, n5 ;
    CGFLOAT gkPyk, ykPyk ;
    gkPyk = CGZERO ;
    ykPyk = CGZERO ;
    n5 = n % 5 ;

    for (i = 0; i < n5; i++)
    {
        CGFLOAT t, p ;

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
    }
    for (; i < n; )
    {
        CGFLOAT t, p ;

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
        i++ ;
        /* 1 ------------------------- */

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
        i++ ;
        /* 2 ------------------------- */

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
        i++ ;
        /* 3 ------------------------- */

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
        i++ ;
        /* 4 ------------------------- */

        t = newproj [i] ;
        p = t - oldproj [i] ;
        oldproj [i] = t ;

        gkPyk +=  t*p ;
        ykPyk +=  p*p ;
        i++ ;
        /* 5 --------------------------- */
    }
    *GkPyk = gkPyk ;
    *YkPyk = ykPyk ;
    return ;
}

/* =========================================================================
   ==== cg_update_d ========================================================
   =========================================================================
   Set d = -gproj + beta*d
   ========================================================================= */
void cg_update_d
(
    CGFLOAT      *d,
    CGFLOAT  *gproj,
    CGFLOAT    beta,
    CGINT         n  /* length of vectors */
)
{
    CGINT i, n5 ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++)
    {
        d [i] = -gproj [i] + beta*d [i] ;
    }
    for (; i < n; )
    {
        d [i] = -gproj [i] + beta*d [i] ;
        i++ ;

        d [i] = -gproj [i] + beta*d [i] ;
        i++ ;

        d [i] = -gproj [i] + beta*d [i] ;
        i++ ;

        d [i] = -gproj [i] + beta*d [i] ;
        i++ ;

        d [i] = -gproj [i] + beta*d [i] ;
        i++ ;
    }
}

/* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       Start of limited memory CG routines  (+ matvec above)
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! */
/* =========================================================================
   ==== cg_trisolve ========================================================
   =========================================================================
   Solve Rx = y or R'x = y where R is a dense upper triangular matrix
   ========================================================================= */
void cg_trisolve
(
    CGFLOAT *x, /* right side on input, solution on output */
    CGFLOAT *R, /* dense matrix */
    int      m, /* leading dimension of R */
    int      n, /* dimension of triangular system */
    int      w  /* T => Rx = y, F => R'x = y */
)
{
    int i, l ;
    if ( w )
    {
        l = m*n ;
        for (i = n; i > 0; )
        {
            i-- ;
            l -= (m-i) ;
            x [i] /= R [l] ;
            l -= i ;
            cg_daxpy0 (x, R+l, -x [i], i) ;
        }
    }
    else
    {
        l = 0 ;
        for (i = 0; i < n; i++)
        {
            x [i] = (x [i] - cg_dot0 (x, R+l, i))/R [l+i] ;
            l += m ;
        }
    }

/* equivalent to:
    BLAS_INT M, N ;
    M = (BLAS_INT) m ;
    N = (BLAS_INT) n ;
    if ( w ) CG_DTRSV ("u", "n", "n", &N, R, &M, x, blas_one) ;
    else     CG_DTRSV ("u", "t", "n", &N, R, &M, x, blas_one) ; */

    return ;
}

/* =========================================================================
   ==== cg_scale0 ==========================================================
   =========================================================================
   compute y = s*x where s is a scalar
   ========================================================================= */
void cg_scale0
(
    CGFLOAT *y, /* output vector */
    CGFLOAT *x, /* input vector */
    CGFLOAT  s, /* scalar */
    int      n  /* length of vector */
)
{
    int i, n5 ;
    n5 = n % 5 ;
    if ( s == -CGONE)
    {
       for (i = 0; i < n5; i++) y [i] = -x [i] ;
       for (; i < n;)
       {
           y [i] = -x [i] ;
           i++ ;
           y [i] = -x [i] ;
           i++ ;
           y [i] = -x [i] ;
           i++ ;
           y [i] = -x [i] ;
           i++ ;
           y [i] = -x [i] ;
           i++ ;
       }
    }
    else
    {
        for (i = 0; i < n5; i++) y [i] = s*x [i] ;
        for (; i < n;)
        {
            y [i] = s*x [i] ;
            i++ ;
            y [i] = s*x [i] ;
            i++ ;
            y [i] = s*x [i] ;
            i++ ;
            y [i] = s*x [i] ;
            i++ ;
            y [i] = s*x [i] ;
            i++ ;
        }
    }
    return ;
}

/* =========================================================================
   ==== cg_daxpy0 ==========================================================
   =========================================================================
   Compute x = x + alpha d
   ========================================================================= */
void cg_daxpy0
(
    CGFLOAT    *x, /* input and output vector */
    CGFLOAT    *d, /* direction */
    CGFLOAT alpha, /* stepsize */
    int         n  /* length of the vectors */
)
{
    CGINT i, n5 ;
    n5 = n % 5 ;
    if (alpha == -CGONE)
    {
        for (i = 0; i < n5; i++) x [i] -= d[i] ;
        for (; i < n; i += 5)
        {
            x [i]   -= d [i] ;
            x [i+1] -= d [i+1] ;
            x [i+2] -= d [i+2] ;
            x [i+3] -= d [i+3] ;
            x [i+4] -= d [i+4] ;
        }
    }
    else
    {
        for (i = 0; i < n5; i++) x [i] += alpha*d[i] ;
        for (; i < n; i += 5)
        {
            x [i]   += alpha*d [i] ;
            x [i+1] += alpha*d [i+1] ;
            x [i+2] += alpha*d [i+2] ;
            x [i+3] += alpha*d [i+3] ;
            x [i+4] += alpha*d [i+4] ;
        }
    }
    return ;
}

/* =========================================================================
   ==== cg_dot0 ============================================================
   =========================================================================
   Compute dot product of x and y, vectors of length n
   ========================================================================= */
CGFLOAT cg_dot0
(
    CGFLOAT *x, /* first vector */
    CGFLOAT *y, /* second vector */
    int      n  /* length of vectors */
)
{
    CGINT i, n5 ;
    CGFLOAT t ;
    t = CGZERO ;
    if ( n <= 0 ) return (t) ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) t += x [i]*y [i] ;
    for (; i < n; i += 5)
    {
        t += x [i]*y[i] + x [i+1]*y [i+1] + x [i+2]*y [i+2]
                        + x [i+3]*y [i+3] + x [i+4]*y [i+4] ;
    }
    return (t) ;
}

/* =========================================================================
   === cg_copy0 ============================================================
   =========================================================================
   Copy vector x into vector y
   ========================================================================= */
void cg_copy0
(
    CGFLOAT *y, /* output of copy */
    CGFLOAT *x, /* input of copy */
    int      n  /* length of vectors */
)
{
    int i, n5 ;
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; )
    {
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
        y [i] = x [i] ;
        i++ ;
    }
    return ;
}

/* =========================================================================
   ==== cg_Yk ==============================================================
   =========================================================================
   Compute y = gnew - gold, set gold = gnew, compute y'y
   ========================================================================= */
void cg_Yk
(
    CGFLOAT    *y, /*output vector */
    CGFLOAT *gold, /* initial vector */
    CGFLOAT *gnew, /* search direction */
    CGFLOAT  *yty, /* y'y */
    CGINT       n  /* length of the vectors */
)
{
    CGINT n5, i ;
    CGFLOAT s, t ;
    n5 = n % 5 ;
    if ( (y != NULL) && (yty == NULL) )
    {
        for (i = 0; i < n5; i++)
        {
            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
        }
        for (; i < n; )
        {
            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            i++ ;

            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            i++ ;

            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            i++ ;

            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            i++ ;

            y [i] = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            i++ ;
        }
    }
    else if ( (y == NULL) && (yty != NULL) )
    {
        s = CGZERO ;
        for (i = 0; i < n5; i++)
        {
            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
        }
        for (; i < n; )
        {
            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            s += t*t ;
            i++ ;
        }
        *yty = s ;
    }
    else
    {
        s = CGZERO ;
        for (i = 0; i < n5; i++)
        {
            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
        }
        for (; i < n; )
        {
            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
            i++ ;

            t = gnew [i] - gold [i] ;
            gold [i] = gnew [i] ;
            y [i] = t ;
            s += t*t ;
            i++ ;
        }
        *yty = s ;
    }
    return ;
}

/* =========================================================================
   ==== cg_update_inf2 =====================================================
   =========================================================================
   Set gold = gnew, compute inf-norm of gnew & 2-norm of gnew, set d = -gnew
   ========================================================================= */
CGFLOAT cg_update_inf2
(
    CGFLOAT   *gold, /* old g */
    CGFLOAT   *gnew, /* new g */
    CGFLOAT      *d, /* d */
    CGFLOAT *gnorm2, /* 2-norm of g */
    CGINT         n  /* length of vectors */
)
{
    CGINT i, n5 ;
    CGFLOAT gnorm, s, t ;
    gnorm = CGZERO ;
    s = CGZERO ;
    n5 = n % 5 ;

    for (i = 0; i < n5; i++)
    {
        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ; 
        gold [i] = t ;
        d [i] = -t ;
    }
    for (; i < n; )
    {
        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ; 
        gold [i] = t ;
        d [i] = -t ;
        i++ ;

        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ; 
        gold [i] = t ;
        d [i] = -t ;
        i++ ;

        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ;
        gold [i] = t ;
        d [i] = -t ;
        i++ ;

        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ;
        gold [i] = t ;
        d [i] = -t ;
        i++ ;

        t = gnew [i] ;
        if ( gnorm < fabs (t) ) gnorm = fabs (t) ;
        s += t*t ;
        gold [i] = t ;
        d [i] = -t ;
        i++ ;
    }
    *gnorm2 = s ;
    return (gnorm) ;
}

/* =========================================================================
   ==== cg_inf =============================================================
   =========================================================================
   Compute infinity norm of vector
   ========================================================================= */
CGFLOAT cg_inf
(
    CGFLOAT *x, /* vector */
    CGINT    n /* length of vector */
)
{
#ifdef NOBLAS
    CGINT i, n5 ;
    CGFLOAT t ;
    t = CGZERO ;
    n5 = n % 5 ;

    for (i = 0; i < n5; i++) if ( t < fabs (x [i]) ) t = fabs (x [i]) ;
    for (; i < n; i += 5)
    {
        if ( t < fabs (x [i]  ) ) t = fabs (x [i]  ) ;
        if ( t < fabs (x [i+1]) ) t = fabs (x [i+1]) ;
        if ( t < fabs (x [i+2]) ) t = fabs (x [i+2]) ;
        if ( t < fabs (x [i+3]) ) t = fabs (x [i+3]) ;
        if ( t < fabs (x [i+4]) ) t = fabs (x [i+4]) ;
    }
    return (t) ;
#endif

#ifndef NOBLAS
    CGINT i, n5 ;
    CGFLOAT t ;
    BLAS_INT N ;
    BLAS_INT int_one = 1 ;
    if ( n < IDAMAX_START )
    {
        t = CGZERO ;
        n5 = n % 5 ;

        for (i = 0; i < n5; i++) if ( t < fabs (x [i]) ) t = fabs (x [i]) ;
        for (; i < n; i += 5)
        {
            if ( t < fabs (x [i]  ) ) t = fabs (x [i]  ) ;
            if ( t < fabs (x [i+1]) ) t = fabs (x [i+1]) ;
            if ( t < fabs (x [i+2]) ) t = fabs (x [i+2]) ;
            if ( t < fabs (x [i+3]) ) t = fabs (x [i+3]) ;
            if ( t < fabs (x [i+4]) ) t = fabs (x [i+4]) ;
        }
        return (t) ;
    }
    else
    {
        N = (BLAS_INT) n ;
        i = (CGINT) CG_IDAMAX (&N, x, &int_one) ;
        return (fabs (x [i-1])) ; /* adjust for fortran indexing */
    }
#endif
}

/* ========================================================================== */
/* ====== cg_error ========================================================== */
/* ========================================================================== */
/* when -g compiler option is used, prints line number of error */
void cg_error
(
    int          status,
    const char    *file,
    int            line,
    const char *message
)
{
    if (status < 0)
    {
        printf ("file: %s line: %d status: %d %s\n",
                 file, line, status, message) ;
#ifdef MATLAB_MEX_FILE
        mexErrMsgTxt (message) ;
#else
        ASSERT (0) ;
        abort ( ) ;
#endif
    }
}

/* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       End of limited memory CG routines
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! */
