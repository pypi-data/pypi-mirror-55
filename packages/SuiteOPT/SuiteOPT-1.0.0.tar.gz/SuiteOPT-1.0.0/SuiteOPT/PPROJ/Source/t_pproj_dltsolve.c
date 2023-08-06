/* Author: Tim Davis */
/* undefine all prior definitions */
#undef FORM_NAME
#undef DLTSOLVE
#undef SKIP

/* -------------------------------------------------------------------------- */
/* define the method */
/* -------------------------------------------------------------------------- */

#ifdef PARTIAL

/* LDL': solve Lx=b with unit diagonal (partial, uses botrow) */
#define DLTSOLVE pproj_dltsol_partial
#define SKIP if (i >= botrow) break

#else

/* LDL': solve Lx=b with unit diagonal (all rows) */
#define DLTSOLVE pproj_dltsol
#define SKIP

#endif

/* ========================================================================== */
/* === DLTSOLVE ============================================================= */
/* ========================================================================== */

/* Solve L'x=b, where b has 1 column  */

void DLTSOLVE
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPFLOAT *Xforward,
    PPINT        iend,
    PPINT      toprow,
    PPINT    *RLinkDn
#ifdef PARTIAL
    , PPINT botrow
#endif
)
{
    PPFLOAT *Lx = L->x ;
    PPINT *Li = L->i ;
    PPINT *Lp = L->p ;
    PPINT *Lnz = L->nz ;
    PPINT i, j, j1, j2 ;

    X [iend] = Xforward [iend] / Lx [Lp [iend]] ;

    for (j = RLinkDn [iend]; j >= toprow; )
    {
        /* get the start, end, and length of column j */
        PPINT p = Lp [j] ;
        PPINT lnz = Lnz [j] ;
        PPINT pend = p + lnz ;

        j1 = RLinkDn [j] ;
        j2 = (j1 >= 0) ? RLinkDn [j1] : -1 ;

        /* find a chain of supernodes (up to j, j1, and j2) */
        if (j1 < toprow || lnz != Lnz [j1] - 1 || Li [Lp [j1]+1] != j)
        {

            /* -------------------------------------------------------------- */
            /* solve with a single column of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y = Xforward [j] / Lx [p] ;
            for (p++ ; p < pend ; p++)
            {
                i = Li [p] ;
                SKIP ;
                y -= Lx [p] * X [i] ;
            }
            X [j] = y ;
            j = j1 ;

        }
        else if (j2 < toprow || lnz != Lnz [j2]-2 || Li [Lp [j2]+2] != j)
        {

            /* -------------------------------------------------------------- */
            /* solve with a supernode of two columns of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y [2], t ;
            PPINT q = Lp [j1] ;
            t = Lx [q+1] ;
            y [0] = Xforward [j ] / Lx [p] ;
            y [1] = Xforward [j1] / Lx [q] ;
            for (p++, q += 2 ; p < pend ; p++, q++)
            {
                i = Li [p] ;
                SKIP ;
                y [0] -= Lx [p] * X [i] ;
                y [1] -= Lx [q] * X [i] ;
            }
            y [1] -= t * y [0] ;
            X [j ] = y [0] ;
            X [j1] = y [1] ;
            j = j2 ;

        }
        else
        {

            /* -------------------------------------------------------------- */
            /* solve with a supernode of three columns of L */
            /* -------------------------------------------------------------- */

            PPFLOAT y [3], t [3] ;
            PPINT q = Lp [j1] ;
            PPINT r = Lp [j2] ;
            t [0] = Lx [q+1] ;
            t [1] = Lx [r+1] ;
            t [2] = Lx [r+2] ;
            y [0] = Xforward [j]  / Lx [p] ;
            y [1] = Xforward [j1] / Lx [q] ;
            y [2] = Xforward [j2] / Lx [r] ;
            for (p++, q += 2, r += 3 ; p < pend ; p++, q++, r++)
            {
                i = Li [p] ;
                SKIP ;
                y [0] -= Lx [p] * X [i] ;
                y [1] -= Lx [q] * X [i] ;
                y [2] -= Lx [r] * X [i] ;
            }
            q = Lp [j1]  ;
            r = Lp [j2]  ;
            y [1] -= t [0] * y [0] ;
            y [2] -= t [2] * y [0] + t [1] * y [1] ;
            X [j ] = y [0] ;
            X [j1] = y [1] ;
            X [j2] = y [2] ;
            j = RLinkDn [j2] ;
        }
    }
}

#undef PARTIAL
