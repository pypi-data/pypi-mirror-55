#ifndef _PPROJ_PRINT_H_
#define _PPROJ_PRINT_H_

void pproj_printA
(
    PPINT   ncol,   /* number of cols in A */
    PPINT    *Ap,   /* size ncol+1, column pointers */
    PPINT    *Ai,   /* size Ap [ncol], row indices for A in increasing
                            order in each column */
    PPFLOAT  *Ax    /* size Ap [ncol], numerical entries of A */
) ;

void pproj_printL
(
    PPINT   const ncol,   /* number of cols in A */
    PPINT   const  *Ap,   /* size ncol+1, column pointers */
    PPINT   const  *Ai,   /* size Ap [ncol], row indices for A in increasing
                        order in each column */
    PPINT   const *Anz,
    PPFLOAT const  *Ax,   /* size Ap [ncol], numerical entries of A */
    char    *what
) ;

void pproj_printX
(
    PPFLOAT *x,
    PPINT    n,
    char *what
) ;

void pproj_printi
(
    int    *i,
    PPINT   n,
    char *what
) ;

void pproj_printx
(
    PPFLOAT const *x,
    PPINT   const  n,
    char *what
) ;

void pproj_printI
(
    PPINT const *x,
    PPINT const  n,
    char *what
) ;

#endif
