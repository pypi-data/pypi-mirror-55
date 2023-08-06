/* ========================================================================== */
/* === Test/naptest.c ======================================================= */
/* ========================================================================== */

/* exhaustive test for napheap */

#include "napheap.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>

#define MAX(a,b) (((a) > (b)) ? (a) : (b))
#define MIN(a,b) (((a) < (b)) ? (a) : (b))

#define NDIM 53

#define CHECK check_solution(napdata,guess,status,refine,set,method,trial,f);

static void check_status (int status, int should_be)
{
    if (status != should_be)
    {
        printf ("got status %d, should be %d\n", status, should_be) ;
        fprintf (stderr, "TEST FAILURE\n") ;
        exit (0) ;
    }
}

/* portable replacement for rand, for repeatable results */
static unsigned long next = 1 ;
#define MY_RAND_MAX 32767
static int myrand ( void )
{
    next = next * 1103515245 + 12345;
    return ((unsigned) (next / 65536) % (MY_RAND_MAX + 1)) ;
}

/* generate a random number strictly between lower and upper */
static NAPFLOAT rnum
(
    NAPFLOAT lower,
    NAPFLOAT upper
)
{
    NAPFLOAT diff, t ;
    t = ((NAPFLOAT) myrand () + 1) / (MY_RAND_MAX + 2) ;
/*  t = ((NAPFLOAT) rand ()) / RAND_MAX ;*/
    diff = upper - lower ;
    t = t*diff + lower ;
    return (t) ;
}

/* generate a random positive number between 0 and upper */
static NAPFLOAT rnumpos
(
    NAPFLOAT upper
)
{
    NAPFLOAT t ;
    int k = myrand ( ) ;
/*  int k = rand ( ) ;*/
    t = ((NAPFLOAT) k + 1)/((NAPFLOAT) MY_RAND_MAX + 1) ;
/*  t = ((NAPFLOAT) k + 1)/((NAPFLOAT) RAND_MAX + 1) ;*/

    if (t < 1e-6) printf ("myrand k %d t %g t*upper %g\n", k, t, t*upper) ;

    t = t*upper ;
    return (t) ;
}

/* generate a random permutation of the integers 0 through n-1 stored in perm */
static void randperm
(
    NAPINT *perm,
    NAPINT     n
)
{
    NAPINT j, k, l ;
    for (j = n-1; j > 0; j--)
    {
        k = myrand () % (j+1) ;
        l = perm [j] ;
        perm [j] = perm [k] ;
        perm [k] = l ;
    }
    return ;
}

#if 0
static double Timer (void)
{
    struct rusage ru ;
    double user, tsys ;

    (void) getrusage (RUSAGE_SELF, &ru) ;

    user =
    ru.ru_utime.tv_sec                  /* user time (seconds) */
    + 1e-6 * ru.ru_utime.tv_usec ;      /* user time (microseconds) */

    tsys =
    ru.ru_stime.tv_sec                  /* tsys time (seconds) */
    + 1e-6 * ru.ru_stime.tv_usec ;      /* tsys time (microseconds) */

    return (user + tsys) ;
}
#endif

/* -------------------------------------------------------------------------- */
/* check the solution returned by napheap */
/* -------------------------------------------------------------------------- */

static void check_solution
(
    NAPdata *napdata,
    NAPFLOAT   guess, /* initial guess for lambda */
    int       status,         /* napheap return value */
    int       refine,
    int          set,
    int       method,
    int        trial,
    FILE          *f
)
{
    NAPFLOAT blo, bhi, bmin, absbmin, bmax, absbmax, errb, errB, erry, tol, err,
             lambda, n, *a, *d, *lo, *hi, *x, *y ;
    NAPINT j ;
    NAPparm *Parm ;
    NAPstat *Stat ;

    x      = napdata->x ;
    y      = napdata->y ;
    d      = napdata->d ;
    a      = napdata->a ;
    lo     = napdata->lo ;
    hi     = napdata->hi ;
    blo    = napdata->blo ;
    bhi    = napdata->bhi ;
    n      = napdata->n ;
    lambda = napdata->lambda ;
    Parm   = napdata->Parm ;
    Stat   = napdata->Stat ;

    if (status == 1) /* check that the problem is infeasible */
    {
        bmin = NAPZERO ;
        absbmin = NAPZERO ;
        bmax = NAPZERO ;
        absbmax = NAPZERO ;
        for (j = 0; j < n; j++)
        {
            if ( a [j] > NAPZERO )
            {
                bmin += a [j]*lo [j] ;
                absbmin += fabs (a [j]*lo [j]) ;
                bmax += a [j]*hi [j] ;
                absbmax += fabs (a [j]*hi [j]) ;
            }
            else if ( a [j] < NAPZERO )
            {
                bmin += a [j]*hi [j] ;
                absbmin += fabs (a [j]*hi [j]) ;
                bmax += a [j]*lo [j] ;
                absbmax += fabs (a [j]*lo [j]) ;
            }
        }
        if ( (bmin+1.e-10*absbmin > bhi) || (bmax-1.e-10*absbmax < blo) )
        {
            return ; /* yes, infeasible problem */
        }
        else
        {
            err = NAPINF ;                     /* no, it was feasible */
        }
    }
    else
    {
        err = napheap_check (&errb, &errB, &erry, napdata) ;
    }

    if (f != NULL)
    {
        /* diagnostic output */
        fprintf (f, "%2i %g %3i %9.2e %9.2e %9.2e %1i",
             set, (NAPFLOAT) n, trial, errb, errB, erry, status) ;

        if (Stat != NULL)
        {
            fprintf (f, "stats: %ld %ld %ld %ld %ld %ld %ld\n",
                (LONG) (Stat->nfree),
                (LONG) (Stat->nbound),
                (LONG) (Stat->nbrks),
                (LONG) (Stat->nrefine),
                (LONG) (Stat->nvarfix),
                (LONG) (Stat->nnewton),
                (LONG) (Stat->nsecant)) ;
        }

        fprintf (f, "\n") ;
    }

    tol = (refine) ? 2e-6 : 1e-4 ;
    if ( set == 7 ) tol = 1.e-3 ;

    if ( err > tol )
    {
        /* test failure; save the problem to a MATLAB script, and abort */
        FILE *fbug ;
        NAPINT i ;
        fprintf (stderr, "TEST FAILURE\n") ;
        printf ("\n\nTEST FAILURE\n") ;
        printf ("method %d set %d n %ld trial %d refine %d "
            "d_is_zero %d d_is_one %d blo %e bhi %e\n",
            method, set, (LONG) n, trial, refine,
            Parm->d_is_zero, Parm->d_is_one, blo, bhi) ;
        printf ("%d %ld %d err: %9.2e %9.2e %9.2e\n",
             set, (LONG) n, trial, errb, errB, erry) ;

        if (Stat != NULL)
        {
            printf ("stats: %ld %ld %ld %ld %ld %ld %ld\n",
                (LONG) (Stat->nfree),
                (LONG) (Stat->nbound),
                (LONG) (Stat->nbrks),
                (LONG) (Stat->nrefine),
                (LONG) (Stat->nvarfix),
                (LONG) (Stat->nnewton),
                (LONG) (Stat->nsecant)) ;
        }

        fbug = fopen ("bugprob.m", "w") ;
        fprintf (fbug, "%% test failure:\n") ;
        fprintf (fbug, "n = %ld ;\n", (LONG) n) ;
        fprintf (fbug, "blo = %32.18e ;\n", blo) ;
        fprintf (fbug, "bhi = %32.18e ;\n", bhi) ;
        fprintf (fbug, "y = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", y [i]) ;
        fprintf (fbug, "] ;\nd = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", d [i]) ;
        fprintf (fbug, "] ;\na = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", a [i]) ;
        fprintf (fbug, "] ;\nlo = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", lo [i]) ;
        fprintf (fbug, "] ;\nhi = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", hi [i]) ;
        fprintf (fbug, "] ;\nxbad = [\n") ;
        for (i = 0 ; i < n ; i++) fprintf (fbug, "%32.18e\n", x [i]) ;
        fprintf (fbug, "] ;\n") ;
        fprintf (fbug, "lambda_bad = %32.18e ;\n", lambda) ;
        fprintf (fbug, "clear parm ;\n") ;
        fprintf (fbug, "parm.refine = %d ;\n",
            (Parm == NULL) ? FALSE : Parm->refine) ;
        fprintf (fbug, "parm.err = %32.18e ;\n",
            (Parm == NULL) ? NAPZERO : Parm->err) ;
        fprintf (fbug, "parm.newton = %d ;\n",
            (Parm == NULL) ? FALSE : Parm->newton) ;
        fprintf (fbug, "parm.k = %d\n",
            (Parm == NULL) ? 4 : Parm->K) ;
        fprintf (fbug, "guess = %32.18e\n", guess) ;
        fprintf (fbug, "[x lambda stats] = napheap (napdata) ;\n") ;
        fprintf (fbug, "err = napheap_check (&errb, &errB, &erry, napdata) ;") ;
        fclose (fbug) ;

        /*
        fwrite (&n, 4, 1, fbug) ;
        fwrite (&blo, 8, 1, fbug) ;
        fwrite (&bhi, 8, 1, fbug) ;
        fwrite (y, 8, n, fbug) ;
        fwrite (d, 8, n, fbug) ;
        fwrite (a, 8, n, fbug) ;
        fwrite (lo, 8, n, fbug) ;
        fwrite (hi, 8, n, fbug) ;
        */

        if (f != NULL) fclose (f) ;
        exit (0) ;
    }
}

int main (void)
{
    NAPFLOAT d1, y1min, y1max, a1min, a1max, l1min, l1max ;
    NAPFLOAT d2min, d2max, y2min, y2max, a2min, a2max, l2min, l2max ;
    NAPFLOAT y3, a3min, a3max, l3min, l3max ;
    NAPFLOAT d4, y4min, y4max, a4, l4, u4 ;
    NAPFLOAT d5, y5min, y5max, a5min, a5max, l5, u5 ;
    NAPFLOAT d6, y6min, y6max, a6min, a6max, l6, u6 ;
    NAPFLOAT d7, y7min, y7max, a7min, a7max, l7, u7 ;
    NAPFLOAT d8, y8min, y8max, a8min, a8max, l8, u8 ;
    NAPFLOAT guess, lambda, r, s, t, cumlo, cumhi, l, u ;
    NAPFLOAT losave, ysave, dsave, hisave, asave ;
    NAPFLOAT *x, *y, *d, *a, *lo, *hi ;
    NAPINT i, j, n, *perm ;
    int ntries, refine, status, method, d_is_zero,
        set, dim, trial, set_start, set_end, probdim [NDIM+1] ;
    FILE *f = NULL ;
    unsigned int rseed ;
    NAPparm *Parm ;
    NAPstat *Stat ;
    NAPdata *napdata ;

    napdata = napheap_setup () ;
    Parm = napdata->Parm ;
    Stat = napdata->Stat ;

    #ifdef NAPSACK_BRUTAL
    fprintf (stderr, "testing napheap (brutal test), please wait ...\n") ;
    #else
    fprintf (stderr, "testing napheap (normal operation), please wait ...\n") ;
    #endif
    fprintf (stderr, "naptest inf: %g.\n", NAPINF) ;

    for (method = 0; method <= 14; method++)
    {
        printf ("\n---- method: %d\n", method) ;
        fprintf (stderr, "test: %2d ", method) ;

        /* ------------------------------------------------------------------ */
        /* try each variation of the method */
        /* ------------------------------------------------------------------ */

        switch (method)
        {

            case 0:     /* ==> Run/0 <== */
                Parm->newton = FALSE ;
                Parm->K = -1 ;   /* becomes K=0 in napheap */
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_0.txt", "w") ;
                #endif
                break ;

            case 1:     /* ==> Run/1 <== */
                Parm->newton = FALSE ;
                Parm->K = 1 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_1.txt", "w") ;
                #endif
                break ;

            case 2:     /* ==> Run/2 <== */
                Parm->newton = FALSE ;
                Parm->K = 2 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_2.txt", "w") ;
                #endif
                break ;

            case 3:     /* ==> Run/2N <== */
                Parm->newton = TRUE ;
                Parm->K = 2 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_2N.txt", "w") ;
                #endif
                break ;

            case 4:     /* ==> Run/3 <== */
                Parm->newton = FALSE ;
                Parm->K = 3 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_3.txt", "w") ;
                #endif
                break ;

            case 5:     /* ==> Run/3N <== */
                Parm->newton = TRUE ;
                Parm->K = 3 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_3N.txt", "w") ;
                #endif
                break ;

            case 6:     /* ==> Run/4 <== */
                Parm->newton = FALSE ;
                Parm->K = 4 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_4.txt", "w") ;
                #endif
                break ;

            case 7:     /* ==> Run/4N <== */
                Parm->newton = TRUE ;
                Parm->K = 4 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_4N.txt", "w") ;
                #endif
                break ;

            case 8:     /* ==> Run/5 <== */
                Parm->newton = FALSE ;
                Parm->K = 5 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_5.txt", "w") ;
                #endif
                break ;

            case 9:     /* ==> Run/5N <== */
                Parm->newton = TRUE ;
                Parm->K = 5 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_5N.txt", "w") ;
                #endif
                break ;

            case 10:     /* ==> Run/10 <== */
                Parm->newton = FALSE ;
                Parm->K = 10 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_10.txt", "w") ;
                #endif
                break ;

            case 11:     /* ==> Run/10N <== */
                Parm->newton = TRUE ;
                Parm->K = 10 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_11.txt", "w") ;
                #endif
                break ;

            case 12:
                Parm->newton = FALSE ;
                Parm->K = 1000000 ;
                set_end = 18 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_inf.txt", "w") ;
                #endif
                break ;

            case 13:
                Parm->newton = TRUE ;
                Parm->K = 1000000 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_infN.txt", "w") ;
                #endif
                break ;

            case 14:     /* ==> Run/1N <== */
                Parm->newton = TRUE ;
                Parm->K = 1 ;
                set_end = 7 ;
                #ifdef DIAGNOSTIC_OUTPUT
                f = fopen ("output_1N.txt", "w") ;
                #endif
                break ;

        }

        /* ------------------------------------------------------------------ */
        /* test the method on a range of problem sets, sizes, and parameters */
        /* ------------------------------------------------------------------ */

        set_start = 1 ;

        /* problem parameters */

        /* problem set 1 */
        d1 = 25. ;
        y1min = -25. ;
        y1max = +25. ;
        a1min = -25. ;
        a1max = +25. ;
        l1min = -15. ;
        l1max = +15. ;

        /* problem set 2 */
        d2min = .5 ;
        d2max = 1.5 ;
        y2min = -5. ;
        y2max = +5. ;
        a2min = -25. ;
        a2max = +25. ;
        l2min = -15. ;
        l2max = +15. ;

        /* problem set 3 */
        y3 = +5. ;
        a3min = -25. ;
        a3max = +25. ;
        l3min = -15. ;
        l3max = +15. ;

        /* problem set 4 */
        d4 = +1. ;
        y4min = -10. ;
        y4max = +10. ;
        a4 = 1. ;
        l4 = 0. ;
        u4 = 1. ;

        /* problem set 5 */
        d5 = +1. ;
        y5min = -10. ;
        y5max = +10. ;
        a5min = 1. ;
        a5max = 26. ;
        l5 = 0. ;
        u5 = 1. ;

        /* for problem sets 6, and 8 through 11 */
        d6 = +25. ;
        y6min = -25. ;
        y6max = +25. ;
        a6min = -10. ;
        a6max = +10. ;
        l6 = -1 ;
        u6 = NAPINF ;

        /* problem set 7 */
        d7 = 1.e-6 ;
        y7min = -25. ;
        y7max = +25. ;
        a7min = -25. ;
        a7max = +25. ;
        l7 = 0. ;
        u7 = 1. ;

        /* for problem sets 8 through 11 */
        d8 = +25. ;
        y8min = -25. ;
        y8max = +25. ;
        a8min = -25. ;
        a8max = +25. ;
        l8 = -1. ;
        u8 = 1. ;

        /*
        i = 10 ;
        for (j = 0; j < NDIM; j++)
        {
            probdim [j] = i ;
            i *= 5 ;
        }
        */

        for (i = 0; i < 50; i++) probdim [i] = i + 1 ;
        probdim [50] = 250 ;
        probdim [51] = 1250 ;
        probdim [52] = 6250 ;

        ntries = 100 ;

        for (set = set_start; set <= set_end; set++)
        {
            fprintf (stderr, ".") ;

            for (dim = 0; dim < NDIM; dim++)
            {
                /* ---------------------------------------------------------- */
                /* allocate space for solution and problem */
                /* ---------------------------------------------------------- */

                n = probdim [dim] ;          /* problem dimension */
                x  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                d  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                a  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                y  = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                lo = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                hi = (NAPFLOAT *) malloc (n*sizeof (NAPFLOAT)) ;
                perm = (NAPINT *) malloc (n*sizeof (NAPINT)) ;
                napdata->x  = x ;
                napdata->n  = n ;
                napdata->y  = y ;
                napdata->d  = d ;
                napdata->a  = a ;
                napdata->lo = lo;
                napdata->hi = hi;
                Stat = napdata->Stat ;
                Parm = napdata->Parm ;

                /* make ntries instances */
                for (trial = 0; trial < ntries; trial++)
                {
                    rseed = (n*10000) + (set*100) + trial ;

                    /* if ( rseed != 11200 ) continue ;
                    next = 13203020071068733288u ; */

                    printf ("method: %d set: %3d dim %d n: %ld trial: %3d "
                            "seed: %lu\n", method, set, dim, (LONG) n,
                            trial, next) ;
                    fflush (stdout) ;
                    srand (rseed) ;

                    for (j = 0; j < n; j++) perm [j] = j ;
                    cumlo = NAPZERO ;
                    cumhi = NAPZERO ;

                    d_is_zero = FALSE ;
                    Parm->d_is_zero = FALSE ;
                    Parm->d_is_pos = TRUE ;

                    /* ------------------------------------------------------ */
                    /* create the test problem */
                    /* ------------------------------------------------------ */

                    if ( set == 1 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d1) ;
                            y [j] = rnum (y1min, y1max) ;
                            a [j] = rnum (a1min, a1max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            s = rnum (l1min, l1max) ;
                            t = rnum (l1min, l1max) ;
                            lo [j] = MIN (s, t) ;
                            hi [j] = MAX (s, t) ;
                            if (j == 1 && (trial % 5 == 4)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                    }
                    else if ( set == 2 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            a [j] = rnum (a2min, a2max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            y [j] = rnum (a[j]+y2min, a[j]+y2max) ;
                            d [j] = fabs (a [j])*rnum (d2min, d2max) ;
                            if ( !d [j] ) d [j] = rnum (d2min, d2max) ;
                            s = rnum (l2min, l2max) ;
                            t = rnum (l2min, l2max) ;
                            lo [j] = MIN (s, t) ;
                            hi [j] = MAX (s, t) ;
                            if (j == 1 && (trial % 3 == 0)) lo [j] = hi [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                    }
                    else if ( set == 3 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            a [j] = rnum (a3min, a3max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            y [j] = a [j] + y3 ;
                            d [j] = fabs (a [j]) + 1 ;
                            s = rnum (l3min, l3max) ;
                            t = rnum (l3min, l3max) ;
                            lo [j] = MIN (s, t) ;
                            hi [j] = MAX (s, t) ;
                            if (j == 1 && (trial % 3 == 0)) lo [j] = hi [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                    }
                    else if ( set == 4 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            a [j] = a4 ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            y [j] = rnum (y4min, y4max) ;
                            d [j] = d4 ;
                            lo [j] = l4 ;
                            hi [j] = u4 ;
                            if (j == 1 && (trial % 3 == 0)) lo [j] = hi [j] ;
                            if ( j == 2 ) lo [j] = hi [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                    }
                    else if ( set == 5 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            a [j] = floor (rnum (a5min, a5max)) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            y [j] = rnum (y5min, y5max) ;
                            d [j] = d5 ;
                            lo [j] = l5 ;
                            hi [j] = u5 ;
                            if (j == 1 && (trial % 3 == 0)) lo [j] = hi [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        if ( l == NAPZERO )
                        {
                            l = .5*(cumlo+cumhi) ;
                        }
                        u = l ;
                    }
                    else if ( set == 6 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d6) ;
                            y [j] = rnum (y6min, y6max) ;
                            a [j] = rnum (a6min, a6max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = rnum (l6, -l6) ;
                            hi [j] = u6 ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            cumlo += a [j]*lo [j] ;
                        }
                        l = cumlo - 1 ;
                        u = l + 10 ;
                    }
                    else if ( set == 7 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d7) ;
                            y [j] = rnum (y7min, y7max) ;
                            a [j] = rnum (a7min, a7max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l7 ;
                            hi [j] = u7 ;
                            /*
                            if (j == 1 && (trial % 3 == 0)) lo [j] = hi [j] ;
                            */
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l + 1 ;
                    }
                    else if ( set == 8 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d8) ;
                            y [j] = rnum (y8min, y8max) ;
                            a [j] = rnum (a8min, a8max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l8 ;
                            hi [j] = u8 ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l + 10. ;
                        randperm (perm, n) ;
                        i = (NAPINT) (.25*n) ;
                        for (j = 0; j < i; j++) d [perm [j]] = NAPZERO ;
                        Parm->d_is_pos = FALSE ;
                    }
                    else if ( set == 9 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d8) ;
                            y [j] = rnum (y8min, y8max) ;
                            a [j] = rnum (a8min, a8max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l8 ;
                            hi [j] = u8 ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l + 10. ;
                        randperm (perm, n) ;
                        i = (NAPINT) (.50*n) ;
                        for (j = 0; j < i; j++) d [perm [j]] = NAPZERO ;
                        Parm->d_is_pos = FALSE ;
                    }
                    else if ( set == 10 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (d8) ;
                            y [j] = rnum (y8min, y8max) ;
                            a [j] = rnum (a8min, a8max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l8 ;
                            hi [j] = u8 ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l + 10. ;
                        randperm (perm, n) ;
                        i = (NAPINT) (.75*n) ;
                        for (j = 0; j < i; j++) d [perm [j]] = NAPZERO ;
                        Parm->d_is_pos = FALSE ;
                    }
                    else if ( set == 11 ) /* d = 0 */
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = NAPZERO ;
                            y [j] = rnum (y7min, y7max) ;
                            a [j] = rnum (a7min, a7max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l7 ;
                            hi [j] = rnum (l7, u7) ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                        if ( trial % 3 == 0 ) u += 1. ;
                        Parm->d_is_pos = FALSE ;
                        Parm->d_is_zero = TRUE ;
                        d_is_zero = TRUE ;
                    }
                    else if ( set == 12 ) /* d > 0 and lambda = 0 optimal */
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (1.001) ;
                            y [j] = rnum (y1min, y1max) ;
                            a [j] = rnum (a1min, a1max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            t = y [j]/d [j] ;
                            lo [j] = t - rnum (0., 1.) ;
                            hi [j] = t + rnum (0., 1.) ;
                            if (j == 1 && (trial % 5 == 4))
                            {
                                lo [j] = t + 1. ;
                                hi [j] = t + 1. ;
                                cumlo += (t+1)*a [j] ;
                            }
                            else
                            {
                                cumlo += t*a [j] ;
                            }
                        }
                        l = cumlo ;
                        if ( (j/2)*2 == j )
                        {
                            u = l + 1. ;
                        }
                        else
                        {
                            u = l ;
                        }

                        if ( trial % 23 == 0 )
                        {
                            l = -NAPINF ;
                            u =  NAPINF ;
                        }
                    }
                    else if ( set == 13 ) /* d = 0 and lambda = 0 optimal */
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = 0. ;
                            y [j] = rnum (y1min, y1max) ;
                            a [j] = rnum (a1min, a1max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = -rnum (0., 1.) ;
                            hi [j] =  rnum (0., 1.) ;
                            if (j == 3 && (trial % 2 == 0))
                            {
                                y [j] = 0. ;
                            }
                            if (j == 7 && (trial % 3 == 0))
                            {
                                y [j] = 0. ;
                            }
                            if      ( y [j] > 0. ) r = hi [j] ;
                            else if ( y [j] < 0. ) r = lo [j] ;
                            else                   r = 0. ;
                            cumlo += r*a [j] ;
                        }
                        d_is_zero = TRUE ;
                        Parm->d_is_zero = TRUE ;
                        l = rnum (cumlo-1, cumlo) ;
                        u = rnum (cumlo, cumlo+1) ;
                        if ( trial == 15 )
                        {
                            l = -NAPINF ;
                            u =  NAPINF ;
                        }
                    }
                    /* d has 0 and nonzeros, lambda = 0 optimal */
                    else if ( set == 14 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = rnumpos (.001) ;
                            y [j] = rnum (y1min, y1max) ;
                            a [j] = rnum (a1min, a1max) ;
                            if (j == 5 && (trial % 2 == 0)) a [j] = 0 ;
                            t = y [j]/d [j] ;
                            lo [j] = t - rnum (0., 1.) ;
                            hi [j] = t + rnum (0., 1.) ;
                        }
                        randperm (perm, n) ;
                        i = (NAPINT) (.50*n) ;
                        for (j = 0; j < i; j++) d [perm [j]] = NAPZERO ;
                        Parm->d_is_pos = FALSE ;
                        for (j = 0; j < n; j++)
                        {
                            if ( d [j] == 0. )
                            {
                                if (j == 3 && (trial % 2 == 0))
                                {
                                    y [j] = 0. ;
                                }
                                if (j == 7 && (trial % 3 == 0))
                                {
                                    y [j] = 0. ;
                                }
                                if      ( y [j] > 0. ) r = hi [j] ;
                                else if ( y [j] < 0. ) r = lo [j] ;
                                else                   r = .5*(lo [j] + hi [j]);
                                cumlo += r*a [j] ;
                            }
                            else
                            {
                                cumlo += (y [j]/d [j])*a [j] ;
                            }
                        }
                        l = rnum (cumlo-1, cumlo) ;
                        u = rnum (cumlo, cumlo+1) ;
                        if ( trial == 15 )
                        {
                            l = -NAPINF ;
                            u =  NAPINF ;
                        }
                    }
                    /* d = 0 and domain of dual function is a point */
                    else if ( set == 15 )
                    {
                        for (j = 0; j < n; j++)
                        {
                            d [j] = NAPZERO ;
                            y [j] = rnum (y7min, y7max) ;
                            a [j] = rnum (a7min, a7max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l7 ;
                            hi [j] = rnum (l7, u7) ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        if ( n > 4 )
                        {
                            j = n/2 ;
                            t = y [j]/a [j] ;
                            for (j = 0; j < n; j++)
                            {
                                if ( a [j] != NAPZERO )
                                {
                                    s = y [j]/a [j] ;
                                    if ( s > t+.5 )
                                    {
                                        if ( a [j] > NAPZERO )
                                        {
                                            lo [j] = -NAPINF ;
                                        }
                                        else
                                        {
                                            hi [j] =  NAPINF ;
                                        }
                                    }
                                    else if ( s < t-.5 )
                                    {
                                        if ( a [j] < NAPZERO )
                                        {
                                            lo [j] = -NAPINF ;
                                        }
                                        else
                                        {
                                            hi [j] =  NAPINF ;
                                        }
                                    }
                                }
                            }
                            if ( trial % 7 == 0 )
                            {
                                j = n/2 ;
                                lo [j] = -NAPINF ;
                                hi [j] =  NAPINF ;
                            }
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                        if ( trial % 2 == 0 ) u += 1. ;
                        Parm->d_is_pos = FALSE ;
                        if ( trial % 3 )
                        {
                            d_is_zero = TRUE ;
                            Parm->d_is_zero = TRUE ;
                        }
                    }
                    else if ( set == 16 ) /* run set 1 but duplicate data */
                    {
                        i = (n/2) + 1 ;
                        for (j = 0; j < i; j++)
                        {
                            d [j] = rnumpos (d1) ;
                            y [j] = rnum (y1min, y1max) ;
                            a [j] = rnum (a1min, a1max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            s = rnum (l1min, l1max) ;
                            t = rnum (l1min, l1max) ;
                            lo [j] = MIN (s, t) ;
                            hi [j] = MAX (s, t) ;
                            if (j == 1 && (trial % 5 == 4)) hi [j] = lo [j] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        i = 0 ;
                        for (; j < n; j++)
                        {
                            d [j] = d [i] ;
                            y [j] = y [i] ;
                            a [j] = a [i] ;
                            lo [j] = lo [i] ;
                            hi [j] = hi [i] ;
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                            i++ ;
                        }
                        l = rnum (cumlo, cumhi) ;
                        u = l ;
                    }
                    else if ( set == 17 )
                    {
                        i = (n/2) + 1 ;
                        for (j = 0; j < i; j++)
                        {
                            d [j] = NAPZERO ;
                            y [j] = rnum (y7min, y7max) ;
                            a [j] = rnum (a7min, a7max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l7 ;
                            hi [j] = rnum (l7, u7) ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                        }
                        if ( n > 4 )
                        {
                            j = n/4 ;
                            t = y [j]/a [j] ;
                            for (j = 0; j < i; j++)
                            {
                                if ( trial % 3 == 0 )
                                {
                                    if ( j % 2 ) d [j] = rnumpos (d1) ;
                                }
                                if ( a [j] != NAPZERO )
                                {
                                    s = y [j]/a [j] ;
                                    if ( s > t+.5 )
                                    {
                                        if ( a [j] > NAPZERO )
                                        {
                                            lo [j] = -NAPINF ;
                                        }
                                        else
                                        {
                                            hi [j] =  NAPINF ;
                                        }
                                    }
                                }
                            }
                            if ( trial % 4 == 0 )
                            {
                                lo [n/4] = -NAPINF ;
                                hi [n/4] =  NAPINF ;
                                d [n/4] = NAPZERO ;
                            }
                        }
                        i = 0 ;
                        for (; j < n; j++)
                        {
                            d [j] = d [i] ;
                            y [j] = y [i] ;
                            a [j] = a [i] ;
                            lo [j] = lo [i] ;
                            hi [j] = hi [i] ;
                            i++ ;
                        }
                        if ( (trial % 2 == 0) && (n > 4) )
                        {
                            if ( (trial/2)%3 == 0 )
                            {
                                lo [n/4] = rnum (-1, hi [n/4]) ;
                            }
                            else if ( (trial/2)%3 == 1 )
                            {
                                hi [n/4] = rnum (lo [n/4], +1) ;
                            }
                            else
                            {
                                lo [n/4] = rnum (-1, +1) ;
                                hi [n/4] = rnum (lo [n/4], +1) ;
                            }
                        }
                        for (j = 0; j < n; j++)
                        {
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        if ( (cumlo > -NAPINF) && (cumhi < NAPINF) )
                        {
                            l = rnum (cumlo, cumhi) ;
                            u = rnum (l, cumhi) ;
                        }
                        else if ( cumlo > -NAPINF )
                        {
                            l = cumlo ;
                            u = rnum (l, l+1) ;
                        }
                        else if ( cumhi < NAPINF )
                        {
                            u = cumhi ;
                            l = rnum (u-1, u) ;
                        }
                        else
                        {
                            l = -1 ;
                            u = +1 ;
                        }
                        if ( trial % 3 == 0 ) u += 1. ;
                        Parm->d_is_pos = FALSE ;
                    }
                    else if ( set == 18 )
                    {
                        i = (n/2) + 1 ;
                        for (j = 0; j < i; j++)
                        {
                            d [j] = NAPZERO ;
                            y [j] = rnum (y7min, y7max) ;
                            a [j] = rnum (a7min, a7max) ;
                            if (j == 0 && (trial % 2 == 0)) a [j] = 0 ;
                            lo [j] = l7 ;
                            hi [j] = rnum (l7, u7) ;
                            if (j == 1 && (trial % 3 == 0)) hi [j] = lo [j] ;
                        }
                        if ( n > 4 )
                        {
                            j = n/4 ;
                            t = y [j]/a [j] ;
                            for (j = 0; j < i; j++)
                            {
                                if ( a [j] != NAPZERO )
                                {
                                    s = y [j]/a [j] ;
                                    if ( s > t+.5 )
                                    {
                                        if ( a [j] > NAPZERO )
                                        {
                                            lo [j] = -NAPINF ;
                                        }
                                        else
                                        {
                                            hi [j] =  NAPINF ;
                                        }
                                    }
                                    else if ( s < t-.5 )
                                    {
                                        if ( a [j] < NAPZERO )
                                        {
                                            lo [j] = -NAPINF ;
                                        }
                                        else
                                        {
                                            hi [j] =  NAPINF ;
                                        }
                                    }
                                }
                            }
                            if ( trial % 3 == 0 )
                            {
                                lo [n/4] = -NAPINF ;
                                hi [n/4] =  NAPINF ;
                            }
                        }
                        i = 0 ;
                        for (; j < n; j++)
                        {
                            d [j] = d [i] ;
                            y [j] = y [i] ;
                            a [j] = a [i] ;
                            lo [j] = lo [i] ;
                            hi [j] = hi [i] ;
                            i++ ;
                        }
                        if ( (trial % 3 == 0) && (n > 4) )
                        {
                            if ( (trial/3)%3 == 0 )
                            {
                                lo [n/4] = rnum (-1, +1) ;
                            }
                            else if ( (trial/3)%3 == 1 )
                            {
                                hi [n/4] = rnum (-1, +1) ;
                            }
                            else
                            {
                                lo [n/4] = rnum (-1, +1) ;
                                hi [n/4] = rnum (lo [n/4], +1) ;
                            }
                        }
                        for (j = 0; j < n; j++)
                        {
                            t = a [j]*lo [j] ;
                            s = a [j]*hi [j] ;
                            cumlo += MIN (t, s) ;
                            cumhi += MAX (t, s) ;
                        }
                        if ( (cumlo > -NAPINF) && (cumhi < NAPINF) )
                        {
                            l = rnum (cumlo, cumhi) ;
                            u = rnum (l, cumhi) ;
                        }
                        else if ( cumlo > -NAPINF )
                        {
                            l = cumlo ;
                            u = rnum (l, l+1) ;
                        }
                        else if ( cumhi < NAPINF )
                        {
                            u = cumhi ;
                            l = rnum (u-1, u) ;
                        }
                        else
                        {
                            l = -1 ;
                            u = +1 ;
                        }
                        if ( trial % 2 == 0 ) u += 1. ;
                        Parm->d_is_pos = FALSE ;
                        Parm->d_is_zero = TRUE ;
                        d_is_zero = TRUE ;
                    }

                    /* ------------------------------------------------------ */
                    /* try the test problem 4 times */
                    /* ------------------------------------------------------ */

                    /* with/without refinement, and with/without input lambda */

                    napdata->blo = l ;
                    napdata->bhi = u ;
                    for (refine = 0 ; refine <= 1 ; refine++)
                    {
                        Parm->refine = refine ;

                        int use_lambda ;
                        for (use_lambda = 0 ; use_lambda <= 1 ; use_lambda++)
                        {
                            if ( use_lambda )
                            {
                                 napdata->lambda = rnum (-10., +10.) ;
                            }
                            else
                            {
                                napdata->lambda = NAPINF ;
                            }
                            guess = lambda ;

                            /* ---------------------------------------------- */
                            /* run the code */
                            /* ---------------------------------------------- */

                            status = napheap (napdata) ; CHECK ;

                            Parm->return_data = TRUE ;
                            lambda = rnum (-10., +10.) ;
                            status = napheap (napdata) ; CHECK ;

                            Parm->return_data = FALSE ;
                            Parm->use_prior_data = TRUE ;
                            lambda = rnum (-10., +10.) ;
                            status = napheap (napdata) ; CHECK ;
                            Parm->use_prior_data = FALSE ;

                            /* provide user memory */
                            lambda = rnum (-10., +10.) ;
                            napdata->xWork = (NAPFLOAT *)
                                                malloc (5*n*sizeof (NAPFLOAT)) ;
                            napdata->iWork = (NAPINT *)
                                            malloc ((4*n+2)*sizeof (NAPINT)) ;
                            status = napheap (napdata) ; CHECK ;
                            free (napdata->xWork) ;
                            free (napdata->iWork) ;
                            napdata->xWork = NULL ;
                            napdata->iWork = NULL ;

                            /* if the diagonal is positive, also solve the
                               problem with the diagonal all one */
                            if ( Parm->d_is_pos )
                            {
                                Parm->d_is_one = TRUE ;
                                lambda = rnum (-10., +10.) ;
                                status = napheap (napdata) ; CHECK ;

                                Parm->return_data = TRUE ;
                                lambda = rnum (-10., +10.) ;
                                status = napheap (napdata) ; CHECK ;

                                Parm->return_data = FALSE ;
                                Parm->use_prior_data = TRUE ;
                                lambda = rnum (-10., +10.) ;
                                status = napheap (napdata) ; CHECK ;

                                Parm->use_prior_data = FALSE ;
                                Parm->d_is_one = FALSE ;
                            }

                            int hi_is_inf = TRUE ;
                            for (j = 0; j < n; j++)
                            {
                                if ( hi [j] < NAPINF )
                                {
                                    hi_is_inf = FALSE ;
                                    break ;
                                }
                            }
                            if ( hi_is_inf )
                            {
                                status = napheap (napdata) ; CHECK ;

                                /* also try flipping signs so that lo is -inf */
                                NAPFLOAT *hi2, *lo2, *y2 ;
                                hi2 = napdata->hi ;
                                lo2 = napdata->lo ;
                                y2  = napdata->y ;
                                for (j = 0; j < n; j++)
                                {
                                    t = lo [j] ;
                                    lo [j] = -hi [j] ;
                                    hi [j] = -t ;
                                    y  [j] = -y [j] ;
                                }
                                napdata->blo = -u ;
                                napdata->bhi = -l ;
                                status = napheap (napdata) ; CHECK ;
                                for (j = 0; j < n; j++)
                                {
                                    t = lo [j] ;
                                    lo [j] = -hi [j] ;
                                    hi [j] = -t ;
                                    y  [j] = -y [j] ;
                                }
                                napdata->blo = l ;
                                napdata->bhi = u ;
                            }
                        }
                    }
                    printf ("\n") ;
                }

                /* ---------------------------------------------------------- */
                /* test error handling and alternate methods */
                /* ---------------------------------------------------------- */

                printf ("\n--- Testing error handling and special cases: [\n") ;
                losave = lo [0] ;
                hisave = hi [0] ;
                ysave = y [0] ;
                dsave = d [0] ;
                asave = a [0] ;

                Parm->refine = 0 ;
                Parm->check = TRUE ;

                /* default parameters, no stats  */
                printf ("try messing with arguments:\n") ;

                if (set == 12 || set == 13 || set == 14)
                {

                    /* unbounded case */
                    printf ("set %d, unbounded:\n", set) ;
                    napdata->blo = -NAPINF ;
                    napdata->bhi =  NAPINF ;
                    status = napheap (napdata) ;

                    /* now try mangling the lo and hi */
                    printf ("\nset %d, unbounded, lo/hi mangled:\n", set) ;
                    napdata->lo [0] = napdata->hi [0] + 1 ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_INVALID_BOUNDS) ;

                    /* try mangling the lo and hi, bounded case  */
                    printf ("\nset %d, lo/hi mangled:\n", set) ;
                    napdata->blo = l ;
                    napdata->bhi = u ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_INVALID_BOUNDS) ;

                    /* try b unbounded, lo with INFs, but y zero */
                    printf ("\nset %d, b inf, lo/hi infs:\n", set) ;
                    napdata->lo [0] = -NAPINF ;
                    y [0] = 0 ;
                    napdata->blo = -NAPINF ;
                    napdata->bhi =  NAPINF ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_OK) ;

                    y [0] = ysave ;
                    lo [0] = losave ;
                    hi [0] = hisave ;

                    /* now try mangling d */
                    if (!d_is_zero)
                    {
                        printf ("\nset %d, unbounded, d mangled:\n", set) ;
                        napdata->d [0] = -1 ;
                        status = napheap (napdata) ;
                        check_status (status, NAPHEAP_STATUS_INVALID_D) ;
                        napdata->d [0] = dsave ;

                        if ( set != 8 )
                        {
                            /* try b unbounded, lo with INFs, but y zero */
                            printf ("\nset %d, unbounded, hi infs:\n", set) ;
                            napdata->d [0] = 0 ;
                            napdata->hi [0] = NAPINF ;
                            napdata->y [0] = 1 ;
                            status = napheap (napdata) ;
                            if ( Parm->d_is_pos )
                            {
                                check_status (status, NAPHEAP_STATUS_INVALID_D);
                            }
                            else
                            {
                                check_status (status, NAPHEAP_STATUS_UNBOUNDED);
                            }
                        }

                        napdata->hi [0] = hisave ;

                        /* try b unbounded, lo with INFs, but y zero */
                        printf ("\nset %d, unbounded, lo infs:\n", set) ;
                        napdata->d [0] = 0 ;
                        napdata->lo [0] = -NAPINF ;
                        napdata->y [0] = -1 ;
                        status = napheap (napdata) ;
                        if ( Parm->d_is_pos )
                        {
                            check_status (status, NAPHEAP_STATUS_INVALID_D);
                        }
                        else
                        {
                            check_status (status, NAPHEAP_STATUS_UNBOUNDED);
                        }

                        napdata->y [0] = ysave ;
                        napdata->lo [0] = losave ;
                        napdata->hi [0] = hisave ;
                        napdata->d [0] = dsave ;
                    }
                }

                /* n is invalid */
                printf ("check n\n") ;
                napdata->blo = l ;
                napdata->bhi = u ;
                napdata->n = -1 ;
                status = napheap (napdata) ;
                check_status (status, NAPHEAP_STATUS_INVALID_N) ;

                /* n is 0, which is OK */
                printf ("n is zero\n") ;
                napdata->n = 0 ;
                status = napheap (napdata) ;
                check_status (status, NAPHEAP_STATUS_OK) ;
                napdata->n = n ;

                /* test invalid Newton parameters */
                if (!(Parm->d_is_pos) && Parm->K > 1)
                {
                    printf ("check newton\n") ;
                    int newt = Parm->newton ;
                    Parm->newton = TRUE ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_INVALID_NEWTON) ;
                    Parm->newton = newt ;
                }

                /* mangle the problem: d is invalid */
                if (!d_is_zero)
                {
                    printf ("d negative: %d %d\n", d_is_zero, Parm->d_is_pos) ;
                    napdata->d [0] = -1 ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_INVALID_D) ;

                    if ( set != 8 )
                    {
                        status = napheap (napdata) ;
                        check_status (status, NAPHEAP_STATUS_INVALID_D) ;
                    }

                    if (Parm->d_is_pos)
                    {
                        printf ("d said to be positive but d < 0:\n") ;
                        napdata->d [0] = 0 ;
                        status = napheap (napdata) ;
                        check_status (status, NAPHEAP_STATUS_INVALID_D) ;
                        napdata->d [0] = dsave ;
                    }
                    else
                    {
                        if ( set != 8 )
                        {
                            printf ("d general, d = 0, unbounded hi:\n") ;
                            napdata->d [0] = 0 ;
                            napdata->a [0] = 0 ;
                            napdata->y [0] = 1 ;
                            napdata->hi [0] = NAPINF ;
                            status = napheap (napdata) ;
                            check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;

                            printf ("d general, d = 0, unbounded lo:\n") ;
                            napdata->d [0] = 0 ;
                            napdata->a [0] = 0 ;
                            napdata->y [0] = -1 ;
                            napdata->lo [0] = -NAPINF ;
                            status = napheap (napdata) ;
                            check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;
                        }

                        napdata->d [0] = dsave ;
                        napdata->y [0] = ysave ;
                        napdata->lo [0] = losave ;
                        napdata->hi [0] = hisave ;
                        napdata->a [0] = asave ;
                    }
                }

                /* check d = 0 case, using Parm->d_is_zero parameter */
                if (d_is_zero)
                {
                    int d0save = Parm->d_is_zero ;
                    printf ("d zero:\n") ;
                    Parm->d_is_zero = TRUE ;
                    status = napheap (napdata) ; CHECK ;
                    Parm->d_is_zero = d0save ;
                    napdata->blo = -NAPINF ;
                    napdata->bhi =  NAPINF ;

                    /* try b unbounded, lo with INFs, but y zero */
                    printf ("\nd zero, set %d, unbounded, hi infs:\n", set) ;
                    napdata->hi [0] = NAPINF ;
                    napdata->y [0] = 1 ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;

                    napdata->y [0] = ysave ;
                    napdata->lo [0] = losave ;
                    napdata->hi [0] = hisave ;

                    /* try b unbounded, lo with INFs, but y zero */
                    printf ("\nd zero, set %d, unbounded, lo infs:\n", set) ;
                    napdata->lo [0] = -NAPINF ;
                    napdata->y [0] = -1 ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;

                    napdata->y [0] = ysave ;
                    napdata->lo [0] = losave ;
                    napdata->hi [0] = hisave ;

                    /* try b unbounded, lo with INFs, but y zero */
                    printf ("\nd zero, set %d, unbounded, lo inf hi<0:\n",set) ;
                    napdata->lo [0] = -NAPINF ;
                    napdata->y [0] = 0 ;
                    napdata->hi [0] = -1 ;
                    status = napheap (napdata) ;
                    if (! (status == NAPHEAP_STATUS_UNBOUNDED ||
                           status == NAPHEAP_STATUS_OK) )
                    {
                        printf ("got status %d, should be %d or %d\n",
                            status, NAPHEAP_STATUS_UNBOUNDED,
                            NAPHEAP_STATUS_OK) ;
                        fprintf (stderr, "TEST FAILURE\n") ;
                        exit (0) ;
                    }

                    napdata->y [0] = ysave ;
                    napdata->lo [0] = losave ;
                    napdata->hi [0] = hisave ;

                    /* try b bounded, a zero, hi unbounded */
                    printf ("\nd zero, set %d, bounded, a zero, hi inf:\n",set);
                    napdata->a [0] = 0 ;
                    napdata->y [0] = 1 ;
                    napdata->hi [0] = NAPINF ;
                    napdata->blo = l ;
                    napdata->bhi = u ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;

                    /* try b bounded, a zero, lo unbounded */
                    printf ("\nd zero, set %d, bounded, a zero, lo inf:\n",set);
                    napdata->a [0] = 0 ;
                    napdata->y [0] = -1 ;
                    napdata->lo [0] = -NAPINF ;
                    status = napheap (napdata) ;
                    check_status (status, NAPHEAP_STATUS_UNBOUNDED) ;

                    napdata->y [0] = ysave ;
                    napdata->lo [0] = losave ;
                    napdata->hi [0] = hisave ;
                    napdata->a [0] = asave ;

                }

                printf ("\ndone Testing error handling and special cases ]\n") ;

                /* ---------------------------------------------------------- */
                /* free the problem */
                /* ---------------------------------------------------------- */

                free (x) ;
                free (d) ;
                free (a) ;
                free (y) ;
                free (lo) ;
                free (hi) ;
                free (perm) ;
            }
        }
        fprintf (stderr, " OK\n") ;
        if (f != NULL) fclose (f) ;
        f = NULL ;
    }

    napheap_terminate (&napdata) ;

    printf ("\nnapheap default parameters:\n") ;
    napheap_print_parm (NULL) ;

    fprintf (stderr, "All tests passed\n") ;
    printf ("All tests passed\n") ;
    return (0) ;
}
