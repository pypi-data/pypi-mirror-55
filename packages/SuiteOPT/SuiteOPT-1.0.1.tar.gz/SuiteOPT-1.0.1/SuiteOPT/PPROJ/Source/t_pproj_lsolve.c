/* Author: Tim Davis */
/* undefine all prior definitions */
#undef FORM_NAME
#undef LSOLVE
#undef SKIP

/* -------------------------------------------------------------------------- */
/* define the method */
/* -------------------------------------------------------------------------- */

#ifdef PARTIAL

/* LDL': solve Lx=b with unit diagonal (partial, uses botrow) */
#define LSOLVE pproj_lsol_partial
#define SKIP if (i >= botrow) break

#else

/* LDL': solve Lx=b with unit diagonal (all rows) */
#define LSOLVE pproj_lsol
#define SKIP

#endif

/* ========================================================================== */
/* === LSOLVE (1) =========================================================== */
/* ========================================================================== */

/* Solve Lx=b, where b has 1 column  */

void LSOLVE
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPINT      jstart,
    PPINT      botrow,
    PPINT    *RLinkUp
)
{
    PPFLOAT *Lx = L->x ;
    PPINT *Li = L->i ;
    PPINT *Lp = L->p ;
    PPINT *Lnz = L->nz ;
    PPINT i, j, j1, j2, n = L->n ;

    for (j = jstart ; j < botrow ; )
    {
        /* get the start, end, and length of column j */
        PPINT p = Lp [j] ;
        PPINT lnz = Lnz [j] ;
        PPINT pend = p + lnz ;

        j1 = RLinkUp [j] ;
        j2 = (j1 < botrow) ? RLinkUp [j1] : n ;

        /* find a chain of supernodes (up to j, j1, and j2) */
        if (lnz < 4 || j1 >= botrow || lnz != Lnz [j1] + 1 || Li [p+1] != j1)
        {

            /* -------------------------------------------------------------- */
            /* solve with a single column of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y = X [j] ;
            for (p++ ; p < pend ; p++)
            {
                i = Li [p] ;
                SKIP ;
                X [i] -= Lx [p] * y ;
            }
            j = j1 ;

        }
        else if (j2 >= botrow || lnz != Lnz [j2] + 2 || Li [p+2] != j2)
        {

            /* -------------------------------------------------------------- */
            /* solve with a supernode of two columns of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y [2] ;
            PPINT q = Lp [j1] ;
            y [0] = X [j] ;
            y [1] = X [j1] - Lx [p+1] * y [0] ;
            X [j1] = y [1] ;
            for (p += 2, q++ ; p < pend ; p++, q++)
            {
                i = Li [p] ;
                SKIP ;
                X [i] -= Lx [p] * y [0] + Lx [q] * y [1] ;
            }
            j = j2 ;

        }
        else
        {

            /* -------------------------------------------------------------- */
            /* solve with a supernode of three columns of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y [3] ;
            PPINT q = Lp [j1] ;
            PPINT r = Lp [j2] ;
            y [0] = X [j] ;
            y [1] = X [j1] - Lx [p+1] * y [0] ;
            y [2] = X [j2] - Lx [p+2] * y [0] - Lx [q+1] * y [1] ;
            X [j1] = y [1] ;
            X [j2] = y [2] ;
            for (p += 3, q += 2, r++ ; p < pend ; p++, q++, r++)
            {
                i = Li [p] ;
                SKIP ;
                X [i] -= Lx [p] * y [0] + Lx [q] * y [1] + Lx [r] * y [2] ;
            }
            j = RLinkUp [j2] ;
        }
    }
}

#undef PARTIAL
