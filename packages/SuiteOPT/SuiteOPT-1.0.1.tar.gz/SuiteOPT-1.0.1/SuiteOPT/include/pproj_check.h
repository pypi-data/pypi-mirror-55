#ifndef _PPROJ_CHECK_H_
#define _PPROJ_CHECK_H_

void pproj_checkA
(
    PPcom     *I,
    int location, /* = 1 if dead rows are still present, = 0 otherwise */
    char  *where
) ;

void pproj_check_AFT
(
    PPcom    *I,
    int  use_ir,  /* TRUE means skip deleted rows */
    char *where
) ;

void pproj_check_AT
(
    PPcom    *I,
    char *where
) ;

void pproj_check_back
(
    PPcom         *I,
    PPFLOAT *forward,
    PPFLOAT      *dl,
    int       botblk,
    char      *where
) ;

void pproj_checkb
(   
    PPcom     *I,
    char  *where
) ;

void pproj_checkc
(   
    PPcom *Parm,
    char  *where
) ;

void pproj_check_const
(   
    PPFLOAT  *x,
    PPFLOAT  cx,
    PPINT    *y,
    PPINT    cy,
    PPINT     n,
    char *where
) ;

void pproj_checkD
(   
    PPcom     *I,
    char  *where
) ;

void pproj_check_diag3
(   
    PPcom     *I,
    PPINT toprow,
    PPINT botrow,
    int   chol  /* T => the matrix was factorized, otherwise updates */
) ;

void pproj_check_diag 
(
    PPcom     *I,
    int     chol,
    char  *where
) ;

void pproj_check_dual /* return dual objective at current point */
(   
    PPcom     *I,
    PPFLOAT  *dl,
    char  *where,
    int     save, /* TRUE => saves dual objective value */
    int    check  /* TRUE => check for increase in dual objective */
) ;

void pproj_check_eqn5
(
    PPcom         *I,
    int       botblk,
    PPFLOAT      *dl,
    PPFLOAT *forward,
    PPFLOAT       *r,
    char     *where
) ;

void pproj_check_forward
(
    PPcom         *I,
    PPFLOAT *forward,
    PPFLOAT       *r,
    int     *joblist,
    int           nj,
    char      *where
) ;

void pproj_check_line
(
    PPcom        *I,
    int        flag, /* flag = 1 if line search terminates at nondiff point
                        flag = 2 if sd <= 0
                        flag =-1 if stepsize truncated to st = 1 */
    int      botblk,
    int     updates, /* number of updates to be performed */
    PPFLOAT     *dl, /* direction vector */
    PPFLOAT      st  /* stepsize */
) ;

void pproj_check_link
(   
    PPcom     *I,
    int *joblist,
    int       nj,
    char  *where
) ;

void pproj_check_minheap
(
    PPINT   *heap,
    PPFLOAT    *x,
    PPINT     *ns,
    PPINT   nheap,
    PPINT    ntot,
    char   *where
) ;

void pproj_check_modlist
(   
    PPcom    *I,
    char *where
) ;

void pproj_check_order
(   
    double    *x,
    PPINT     *I,
    PPINT length,
    char  *where
) ;

void pproj_checkF
(
    PPcom     *I,
    char  *where
) ;

void pproj_check_deriv
(
    PPcom        *I,
    PPINT    botblk,
    double      *dl, /* direction vector */
    double       st  /* stepsize */
) ;

#endif
