/* ========================================================================= */
/* === checkA ============================================================== */
/* ========================================================================= */
/* Check that the columns of A are arranged so that the active entries
   are before the inactive entries. Also, check that the active rows and
   free columns of A correspond to AFT. */
/* ========================================================================= */

#include "pproj.h"
void pproj_checkA
(
    PPcom     *I,
    int location, /* = 1 if dead rows are still present
                     = 0 otherwise
                     = 2 to check that A' = AT */
    char  *where
)
{
    PPINT *Ap, *Ai, *Anz, *Ti, *Tp, *AFTp, *AFTnz, *AFTi, *ir, *J,
           i, j, p, q, pp, p1, p2, iprev, nrow, ncol, ni, nmax, tnz ;
    int status, *ib ;
    PPFLOAT *Ax, *Tx, *AFTx, *X ;
    PPwork    *W ;
    PPprob *Prob ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check A %s\n", where) ;

    W = I->Work ;
    ir = W->ir ;
    ib = W->ib ;

    Prob = I->Prob ;
    Ap = Prob->Ap ;
    Anz = Prob->Anz ;
    Ai = Prob->Ai ;
    Ax = Prob->Ax ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni = Prob->ni + Prob->nsing ;
    nmax = PPMAX (nrow, ncol) ;
    if ( location == 2 )
    {
        PPINT *ATp, *ATi, *Work ;
        PPFLOAT *ATx ;
        ATp = (PPINT *) pproj_malloc (&status, (nrow+1), sizeof (PPINT)) ;
        ATi = (PPINT *) pproj_malloc (&status, Ap [ncol], sizeof (PPINT)) ;
        Work= (PPINT *) pproj_malloc (&status, nrow, sizeof (PPINT)) ;
        ATx = (PPFLOAT *) pproj_malloc (&status, Ap [ncol], sizeof (PPFLOAT)) ;
        pproj_transpose (ATp, ATi, ATx, Ap, Ai, Ax, nrow, ncol, Work) ;
        for (i = 0; i <= nrow; i++)
        {
            if ( ATp [i] != W->ATp [i] )
            {
                printf ("ATp [%ld] = %ld != W->ATp [%ld] = %ld\n",
                        (LONG) i, (LONG) ATp [i], (LONG) i, (LONG) W->ATp [i]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        for (i = 0; i < Ap [ncol]; i++)
        {
            if ( ATi [i] != W->ATi [i] )
            {
                printf ("ATi [%ld] = %ld != W->ATi [%ld] = %ld\n",
                        (LONG) i, (LONG) ATi [i], (LONG) i, (LONG) W->ATi [i]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        for (i = 0; i < Ap [ncol]; i++)
        {
            if ( ATx [i] != W->ATx [i] )
            {
                printf ("ATx [%ld] = %e != W->ATx [%ld] = %e\n",
                         (LONG) i, ATx [i], (LONG) i, W->ATx [i]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        pproj_free (ATp) ;
        pproj_free (ATi) ;
        pproj_free (ATx) ;
        pproj_free (Work) ;
        return ;
    }

    AFTp = W->AFTp ;
    AFTi = W->AFTi ;
    AFTnz = W->AFTnz ;
    AFTx = W->AFTx ;

    for (i = 0 ; i <= nrow ; i++) ASSERT (AFTp [i] == W->ATp [i]) ;

    /* allocate workspace */
    J = pproj_malloc (&status, nmax, sizeof (PPINT)) ;
    X = pproj_malloc (&status, nmax, sizeof (PPFLOAT)) ;

    /* check for sorted columns */
    for (j = 0 ; j < ncol ; j++)
    {
        if ( Anz [j] < 0 )
        {
            printf ("Anz [%ld] = %ld < 0\n", (LONG) j, (LONG) Anz [j]) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        p1 = Ap [j] ;
        p2 = Ap [j] + Anz [j] ;
        iprev = -1 ;
        for (p = p1; p < p2; p++)
        {
            i = Ai [p] ;
            if (i >= nrow || i < 0)
            {
                printf("i: %ld j: %ld nrow: %ld ncol: %ld\n",
                       (LONG) i, (LONG) j, (LONG) nrow, (LONG) ncol) ;
                pproj_error (-1, __FILE__, __LINE__, where);
            }
            if (i <= iprev)
            {
                printf("col: %ld (entries in column not increasing)\n",
                       (LONG) j) ;
                for (p = p1 ; p < p2 ; p++)
                {
                    printf ("p: %ld i: %ld\n", (LONG) p, (LONG) Ai [p]) ;
                }
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            iprev = i ;
            /* if ( (ir [i] > ni) || (ir [i] < -ni) )
            {
                printf ("col: %i has active row %i, "
                        "but it is dropped ir: %i\n", j, i, ir [i]) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            } */
        }
        for (; p < Ap [j+1]; p++)
        {
            i = Ai [p] ;
            if ( ir [i] <= ni )
            {
                printf ("col: %ld row: %ld inactive, but ir: %ld\n",
                        (LONG) j, (LONG) i, (LONG) ir [i]);
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }

/* check that each entry in A is the transpose of AFT */
/* compute transpose of A */
   
    for (i = 0; i < nrow; i++)
    {
        J [i] = 0 ;
    }

    for (j = 0 ; j < ncol ; j++)
    {
        if ( !ib [j] )
        {
            p1 = Ap [j] + Anz [j] ;
            for (p = Ap [j]; p < p1; p++)
            {
                if ( ir [Ai [p]] <= ni ) J [Ai [p]]++ ;
            }
        }
    }

    Tp = pproj_malloc (&status, (nrow+1), sizeof (PPINT)) ;
    Tp [0] = 0 ;
    for (i = 0 ; i < nrow ; i++)
    {
        Tp [i+1] = Tp [i] + J [i] ;
        J [i] = Tp [i] ;
    }
    tnz = Tp [nrow] ; 
    if (tnz == 0)
    {
	/* nothing to do; free workspace and return */
	pproj_free (J) ;
	pproj_free (X) ;
	pproj_free (Tp) ;
        return ;
    }

    Ti = pproj_malloc (&status, tnz, sizeof (PPINT)) ;
    Tx = pproj_malloc (&status, tnz, sizeof (PPFLOAT)) ;

    /* ====================================================================== */
    /* === T = A' =========================================================== */
    /* ====================================================================== */

    for (j = 0 ; j < ncol ; j++)
    {
        if ( !ib [j] )
        {
            p1 = Ap [j] + Anz [j] ;
            for (p = Ap [j] ; p < p1 ; p++)
            {
                if ( ir [Ai [p]] <= ni )
                {
                    pp = J [Ai [p]]++ ;
                    Ti [pp] = j ;
                    Tx [pp] = Ax [p] ;
                }
            }
        }
    }

/* check that each row of T agree with the corresponding row of AFT */

    for (j = 0; j < ncol; j++) J [j] = 0 ;
    for (i = 0; i < nrow; i++)
    {
        if ( ir [i] <= ni )
        {
            p1 = Tp [i+1] ;
            if ( AFTnz [i] != p1 - Tp [i] )
            {
                printf ("row: %ld AFTnz (%ld) != Tp (%ld+1) - Tp (%ld)\n",
                        (LONG) i, (LONG) AFTnz [i], (LONG) p1, (LONG) Tp [i]) ;
                for (p = AFTp [i]; p < AFTp [i] + AFTnz [i]; p++)
                {
                    printf ("AFT matrix: row: %ld col: %ld x: %e\n",
                            (LONG) i, (LONG) AFTi [p], AFTx [p]) ;
                }
                for (p = Tp [i]; p < p1; p++)
                {
                    printf ("A matrix, row: %ld col: %ld x: %e\n",
                           (LONG) i, (LONG) Ti [p], Tx [p]) ;
                }
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            for (p = Tp [i]; p < p1; p++)
            {
                j = Ti [p] ;
                J [j] = 1 ;
                X [j] = Tx [p] ;
            }
            p = AFTp [i] ;
            p1 = p + AFTnz [i] ;
            for (; p < p1; p++)
            {
                j = AFTi [p] ;
                if ( !J [j] )
                {
                    printf("row: %ld col: %ld in AFT, but not in A transpose\n",
                           (LONG) i, (LONG) j) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
                J [j] = 0 ;
                if ( AFTx [p] != X [j] )
                {
                    printf ("row: %ld col: %ld AFTx(%e) != Ax (%e)\n",
                            (LONG) i, (LONG) j, AFTx [p], X [j]) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
        }
    }

    /* In dasa check that all rows in the active part of A are active rows.
       In one location in the code, cannot make this test since dead
       rows are still present. */
    if ( location == 0 )
    {
        for (j = 0; j < ncol; j++)
        {
            q = Ap [j] + Anz [j] ;
            for (p = Ap [j]; p < q; p++)
            {
                if ( ir [Ai [p]] > ni ) /* row is dropped */
                {
                    printf ("row: %ld col: %ld in active part of A, but "
                            "row is dropped since ir = %ld > ni = %ld\n",
                            (LONG) Ai [p], (LONG) j, (LONG) ir [Ai [p]],
                            (LONG) ni) ;
                    pproj_error (-1, __FILE__, __LINE__, where) ;
                }
            }
        }
    }

    /* free workspace */
    pproj_free (J) ;
    pproj_free (X) ;
    pproj_free (Tp) ;
    pproj_free (Ti) ;
    pproj_free (Tx) ;
}
