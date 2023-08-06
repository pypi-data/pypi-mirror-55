/* ========================================================================= */
/* === checkdiag =========================================================== */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_diag 
(
    PPcom     *I,
    int     chol,
    char  *where
)
{
    PPINT *Ap, *Anz, *Ai, *Lp, *Li, *Lnz, *ir, *ir_old,
          *RowmodList, *ColmodList, *ineq_row,
           nrowadd, nrowdel, ncoladd, ncoldel,
           i, j, p, q, nrow, ncol, row, col, ni  ;
    int status, *ib, *ib_old ;

    PPFLOAT *Ax, *Lx, *D, *E, s, dmax, err, sigma ;

    cholmod_factor *L ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check diag %s\n", where) ;

    Parm = I->Parm ;
    W = I->Work ;
    ib_old = W->ib ;
    ir_old = W->ir ;
    sigma = I->Work->sigma ;

    Prob = I->Prob ;
    Ap  = Prob->Ap ;
    Anz  = Prob->Anz ;
    Ai  = Prob->Ai ;
    Ax  = Prob->Ax ;
    nrow = Prob->nrow ;
    ncol = Prob->ncol ;
    ni = Prob->ni + Prob->nsing ;
    ineq_row = Prob->ineq_row ;

    L = W->L ;
    Lp   = L->p ;
    Lnz  = L->nz ;
    Li   = L->i ;
    Lx   = L->x ;

    /* allocate workspace */
    E = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    D = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    ir = pproj_malloc (&status, nrow, sizeof (PPINT)) ;
    ib = pproj_malloc (&status, ncol, sizeof (int)) ;

    pproj_copyi (ir, ir_old, nrow) ;
    pproj_copyi_int (ib, ib_old, ncol) ;

/* update ir and ib to take into account the row and column
   updates that have been incorporated into the current L matrix */

    nrowadd = W->nrowadd ;
    nrowdel = W->nrowdel ;
    ncoladd = W->ncoladd ;
    ncoldel = W->ncoldel ;

    RowmodList = W->RowmodList ;
    ColmodList = W->ColmodList ;
    for (i = 1; i <= nrowadd; i++)
    {
        row = RowmodList [nrow-i] ;
        /* the row is currently not in the factorization
           (scheduled to be added) */
        ir [row] = ni + 1 ;
    }
    for (i = 0; i < nrowdel; i++)
    {
        row = RowmodList [i] ;
        /* the row is currently in the factorization
           (scheduled to be deleted) */
        ir [row] = 0 ;
    }
    for (i = 1; i <= ncoldel; i++)
    {
        col = ColmodList [ncol-i] ;
        /* the column is currently in the factorization
           (scheduled to be deleted) */
        ib [col] = 0 ;
    }
    for (i = 0; i < ncoladd; i++)
    {
        col = ColmodList [i] ;
        /* the column is currently not in the factorization
           (scheduled to be added) */
        ib [col] = -1 ;
    }

    for (i = 0; i < nrow; i++)
    {
        D [i] = sigma ;
        E [i] = Lx [Lp [i]] ;	/* D(i,i) */
    }

/* printf ("active elements of A:\n") ;*/
    for (j = 0; j < ncol ; j++)
    {
        if ( !ib [j] )
        {
            q = Ap [j] + Anz [j] ;
            for (p = Ap [j]; p < q; p++)
            {
                i = Ai [p] ;
                if ( ir [i] <= ni )
                {
                    D [i] += Ax [p] * Ax [p] ;
/* printf ("%i %i %e\n", i, j, Ax [p]) ;*/
                }
            }
        }
    }

    for (j = 0; j < nrow; j++)
    {
        if ( ir [j] <= ni )
        {
	    p = Lp [j] ;
            q = p + Lnz [j] ;
            s = Lx [p] ;	    /* D(j,j) */
            for (p++ ; p < q; p++)
            {
                E [Li [p]] += s * Lx [p] * Lx [p] ;
            }
        }
    }

    err = 0 ;
    dmax = 0 ;
    for (i = 0; i < nrow; i++)
    {
        if ( ir [i] <= ni )
        {
            err = PPMAX (err, fabs (D [i] - E [i])) ;
            dmax += fabs (D [i]) ;
        }
    }

    if (Parm->PrintLevel > 0 )
    {
        PRINTF ("err in factorization %s: %e, chol: %i\n",
            where, err, chol);
    }
    if ( chol )
    {
        if ( (err/dmax > 1.e-6) && (err > 1.e-8) )
        {
            PRINTF ("factor err %s: %e\n", where, err);
            for (i = 0; i < nrow;i++)
            {
                if ( ir [i] <= ni )
                {
		/*
                    PRINTF ("i: %i D: %e E: %e\n", i, D [i], E [i]) ;
		    */

                    PRINTF ("i: %ld D: %e E: %e err: %e\n",
                           (LONG) i, D [i], E [i], fabs (D [i]-E [i])) ;
                }
            }
            pproj_error (-1, __FILE__, __LINE__, "Stop") ;
        }
    }
    else
    {
        if ( ((err/dmax > 1.e-5) && (err > 1.e-8)) || (err != err) )
        {
            printf ("factor err %s: %e\n", where, err);
            for (i = 0; i < nrow; i++)
            {
                if ( ir [i] <= ni )
                {
                    printf ("i: %ld D: %e E: %e err: %e",
                           (LONG) i, D [i], E [i], fabs (D [i]-E [i])) ;
		    if (fabs (D [i]-E [i]) > 1e-3) printf (" **** ") ;
		    printf ("\n") ;
                }
            }
            pproj_error (-1, __FILE__, __LINE__, "Stop") ;
        }
    }

    /* free workspace */
    pproj_free (E) ;
    pproj_free (D) ;
    pproj_free (ir) ;
    pproj_free (ib) ;
}
