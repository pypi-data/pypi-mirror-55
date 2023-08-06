/* ========================================================================= */
/* === checkdiag3 ========================================================== */
/* ========================================================================= */
/* check the diagonal of LDL' between toprow and botrow */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_diag3
(
    PPcom     *I,
    PPINT toprow,
    PPINT botrow,
    int     chol  /* T => the matrix was factorized, otherwise updates */
)
{
    int status, *ib ;
    PPINT i, p, q, nrow, ni, *ATp, *ATi, *Lp, *Li, *Lnz, *ir ;
    PPFLOAT *ATx, *Lx, *D, *E, t, dmax, err, sigma, di ;
    cholmod_factor *L ;
    PPparm *Parm ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif

    Parm = I->Parm ;
    W = I->Work ;
    ir = W->ir ;
    ib = W->ib ;
    sigma = I->Work->sigma ;

    ATp   = W->ATp ;
    ATi   = W->ATi ;
    ATx   = W->ATx ;
    nrow = I->Prob->nrow ;
    ni = I->Prob->ni + I->Prob->nsing ;

    L = W->L ;
    Lp   = L->p ;
    Lnz  = L->nz ;
    Li   = L->i ;
    Lx   = L->x ;

    /* allocate workspace */
    E = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
    D = pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;

    pproj_initx (D, PPZERO, nrow) ;
    pproj_initx (E, PPZERO, nrow) ;
    err = 0 ;
    dmax = 0 ;
/*printf ("active elements of A:\n") ;*/
    for (i = toprow; i < botrow; i++)
    {
        if ( ir [i] <= ni )
        {
            t = sigma ;
            q = ATp [i+1] ;
            for (p = ATp [i]; p < q; p++)
            {
                if ( ib [ATi [p]] == 0 )
                {
                    t += ATx [p]*ATx [p] ;
/* printf ("%i %i %e\n", i, ATi [p], ATx [p]) ;*/
                }
            }
            p = Lp [i] ;
	    di = Lx [p] ;   	/* D(i,i) */
            D [i] = t ;
            dmax += fabs (t) ;
            E [i] += di ;
            err = PPMAX (err, fabs (t - E [i])) ;
            q = p + Lnz [i] ;
            t = di ;
            for (p++ ; p < q ; p++)
            {
                E [Li [p]] += t * Lx [p] * Lx [p] ;
            }
        }
    }

    if ( Parm->PrintLevel > 1 )
        printf ("diag3, err in factorization: %e chol: %i\n", err, chol);
    if ( chol )
    {
        if ( (err/dmax > 1.e-6) && (err > 1.e-10) )
        {
            printf ("err in chol: %e\n", err);
            for (i = toprow; i < botrow;i++)
            {
                if ( ir [i] < 0 )
                {
                    printf ("i: %ld D: %e E: %e err: %e\n",
                           (LONG) i, D [i], E [i], fabs (D [i] - E [i])) ;
                }
            }
            pproj_error (-1, __FILE__, __LINE__, "partial chol failure") ;
        }
    }
    else
    {
        if ( (err/dmax > 1.e-5) && (err > 1.e-10) )
        {
            printf ("err in chol update: %e\n", err);
            for (i = toprow; i < botrow;i++)
            {
                if ( ir [i] <= ni )
                {
                    printf ("i: %ld D: %e E: %e err: %e\n",
                           (LONG) i, D [i], E [i], fabs (D [i] - E [i])) ;
                }
            }
            pproj_error (-1, __FILE__, __LINE__, "partial chol failure") ;
        }
    }

    /* free workspace */
    pproj_free (E) ;
    pproj_free (D) ;
}
