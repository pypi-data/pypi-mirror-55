#ifndef _PPROJ_H_
#define _PPROJ_H_
#include "SuiteSparse_config.h"
#include "cholmod.h"
#include "ccolamd.h"
#include "SuiteOPTconfig.h"

#define PPFLOAT SuiteOPTfloat
#define PPINT SuiteOPTint

#define FALSE SuiteOPTfalse
#define TRUE SuiteOPTtrue

#define PPINF SuiteOPTinf
#define PPINFINT SuiteOPTinfint

#ifndef PRINTF
#define PRINTF printf
#endif

#define PPZERO ((PPFLOAT) 0)
#define PPONE ((PPFLOAT) 1)
#define PPMAX(a,b) (((a) > (b)) ? (a) : (b))
#define PPMIN(a,b) (((a) < (b)) ? (a) : (b))

/* -------------------------------------------------------------------------- */
/* status returned by pproj */
/* -------------------------------------------------------------------------- */
#define PPROJ_SOLUTION_FOUND                     (0)
#define PPROJ_ERROR_DECAY_STAGNATES              (100)
#define PPROJ_OUT_OF_MEMORY                      (101)
#define PPROJ_SSOR_NONASCENT                     (102)
#define PPROJ_SSOR_MAX_ITS                       (103)
#define PPROJ_MISSING_PRIOR_DATA                 (104)
#define PPROJ_START_GUESS_NEEDS_PRIOR_DATA       (105)
#define PPROJ_INVALID_LINEAR_CONSTRAINT_BOUNDS   (106)
#define PPROJ_DUAL_SOLVE_ERROR                   (107)
#define PPROJ_START_GUESS_IS_1_BUT_LAMBDA_NULL   (108)
#define PPROJ_START_GUESS_IS_2_BUT_CHOLMOD_FALSE (109)
#define PPROJ_START_GUESS_IS_3_BUT_LAMBDA_NULL   (110)
#define PPROJ_BOTH_NI_AND_NSING_POSITIVE         (111)
#define PPROJ_OPTIMAL_COST_IS_MINUS_INFINITY     (112)
#define PPROJ_NSING_START_GUESS_PROB             (113)

#define PPROJ_START_MESSAGES                     (100)
#define PPROJ_END_MESSAGES                       (199)

/* the following are used for flow control and are not returned to user */
#define PPROJ_STATUS_OK            (-1)
#define PPROJ_PROX_UPDATE          (-2)
#define PPROJ_ALL_ROWS_DROPPED     (-3)
#define PPROJ_SWITCH_TO_UPDOWN     (-4)
#define PPROJ_TOLERANCE_NOT_MET    (-5)
#define PPROJ_DO_LINE_SEARCH       (-6)
#define PPROJ_SSOR1_DIAG_ZERO      (-7)
#define PPROJ_SSOR1_DIAG_OK        (-8)

/* -------------------------------------------------------------------------- */
/* pproj version information */
/* -------------------------------------------------------------------------- */
#define PPROJ_DATE "October 30, 2019"
#define PPROJ_MAIN_VERSION 2
#define PPROJ_SUB_VERSION 0
#define PPROJ_SUBSUB_VERSION 0

#define ADD_SING_IN_LLINK(k) \
l = lLinkUp [Ll] ; \
lLinkUp [k] = l ; \
lLinkDn [l] = k ; \
lLinkUp [Ll] = k ; \
lLinkDn [k] = Ll ; \
Ll = k ;


#define ADD_SING_IN_ULINK(k) \
l = uLinkUp [Ul] ; \
uLinkUp [k] = l ; \
uLinkDn [l] = k ; \
uLinkUp [Ul] = k ; \
uLinkDn [k] = Ul ; \
Ul = k ;

#define ADD_ROW_IN_RLINK(i) \
l = RLinkUp [Rl]  ; \
RLinkUp [i] = l ; \
RLinkDn [l] = i ; \
RLinkUp [Rl] = i ; \
RLinkDn [i] = Rl ; \
Rl = i ;

#define SET_LSTART(k) \
if ( cholmod ) \
{ \
    blk = sol_to_blk [k] ; \
    if ( blk > prevblkL ) \
    { \
        lstart [blk] = k ; \
        prevblkL = blk ; \
    } \
}

#define SET_LSTART0(k) \
blk = sol_to_blk [k] ; \
if ( blk > prevblkL ) \
{ \
    lstart [blk] = k ; \
    prevblkL = blk ; \
}

/* the blk computed above is the correct blk */
#define SET_LSTART_SIMPLE(k) \
if ( cholmod ) \
{ \
    if ( blk > prevblkL ) \
    { \
        lstart [blk] = k ; \
        prevblkL = blk ; \
    } \
}

#define SET_USTART(k) \
if ( cholmod ) \
{ \
    blk = sol_to_blk [k] ; \
    if ( blk > prevblkU ) \
    { \
        ustart [blk] = k ; \
        prevblkU = blk ; \
    } \
}

#define SET_USTART0(k) \
blk = sol_to_blk [k] ; \
if ( blk > prevblkU ) \
{ \
    ustart [blk] = k ; \
    prevblkU = blk ; \
}

/* the blk computed above is the correct blk */
#define SET_USTART_SIMPLE(k) \
if ( cholmod ) \
{ \
    if ( blk > prevblkU ) \
    { \
        ustart [blk] = k ; \
        prevblkU = blk ; \
    } \
}

#define ADD_IN_R_AND_ULINKS(i,j) \
ADD_ROW_IN_RLINK(i) ; \
ADD_SING_IN_ULINK(j) ; \
b [i] += bu [j] ; \
if ( ni ) ir [i] = j ; \
else \
{ \
    ir [i] = 1 ; \
    shi [i] = j ; \
    if ( j > row_sing [i] ) \
    { \
        j-- ; \
        slo [i] = j ; \
        ADD_SING_IN_LLINK(j) ; \
    } \
    else slo [i] = 0 ; \
}

#define ADD_IN_R_AND_LLINKS(i,j) \
ADD_ROW_IN_RLINK(i) ; \
ADD_SING_IN_LLINK(j) ; \
b [i] += bl [j] ; \
if ( ni ) ir [i] = -j ;  \
else \
{ \
    ir [i] = 1 ; \
    slo [i] = j ; \
    j++ ; \
    if ( j < row_sing1 [i] ) \
    { \
        shi [i] = j ; \
        ADD_SING_IN_ULINK(j) ; \
    } \
    else shi [i] = 0 ; \
}

/* ========================================================================== */
/* === PPparm =============================================================== */
/* ========================================================================== */
typedef struct PPparm_struct
{
    PPFLOAT   grad_tol ; /* relative error tolerance */
    int    PrintStatus ; /* T => print status of run */
    int      PrintStat ; /* T => print final statistics */
    int     PrintLevel ; /* = 0(none), = 1(final), = 2(post loop), 3(in-loop) */
    int      PrintParm ; /* T => print the parameters */
    int use_prior_data ; /* T => use the priordata argument of ppdata */
    int    return_data ; /* T => return priordata in ppdata */
    int       loExists ; /* F => treat input argument lo as -infinity */
    int       hiExists ; /* F => treat input argument hi as +infinity */
    int      getfactor ; /* T => do not terminate before matrix is factored */
    int          debug ; /* debug level, 0 = none, 1 = after loop, 2 = in loop*/
    PPFLOAT   checktol ; /* acceptable errors in debug routines */
    int    start_guess ; /* see pproj_default.c for details */
    int        permute ; /* T => permute user's input, and output to user */
    PPFLOAT     phase1 ; /* phase1 iterations = MAX (nrow^{phase1}, 5),
                            phase1 < 0 => no phase1 iterations */
    int        cholmod ; /* T = use cholmod and update/downdates, F = SSOR */
    int     multilevel ; /* T = use multilevel method, F = single level */
    int stop_condition ; /* stopping condition (0, 1, or 2 -see pproj_default)*/
    PPFLOAT      sigma ; /* prox regularization parameter */
    PPFLOAT     Asigma ; /* diagonal offset of A_F A_F' in LDL' factoriza */
    int     ScaleSigma ; /* T = scale sigma by max_ij |a_ij| */
    PPFLOAT sigma_decay; /* decay factor for sigma in the prox iteration */
    int          nprox ; /* max number of proximal updates */
    PPFLOAT armijo_grow; /* growth factor for SpaRSA's Armijo step */
    int        narmijo ; /* maximum number of Armijo expansions */
    int            mem ; /* number of function values stored for SpaRSA */
    int        nsparsa ; /* maximum number of SpaRSA iterations */
    PPFLOAT      gamma ; /* parameter in (0, 1) for terminating SpaRSA */
    PPFLOAT        tau ; /* tau, beta, grad_decay, gamma_decay are (continued)*/
    PPFLOAT       beta ; /* parameters associated with formula for (continued)*/
    PPFLOAT grad_decay ; /* undecided indices -- see default in    (continued)*/
    PPFLOAT gamma_decay; /* pproj for details */
    int use_coor_ascent; /* T = use coordinate ascent, F = do not use */
    PPFLOAT   coorcost ; /* if coorcost*Annz <= Lnnz, use coor_ascent */
    int      use_ssor0 ; /* T = use ssor0 if appropriate, F = never use ssor0 */
    int      use_ssor1 ; /* T = use ssor1 if appropriate, F = never use ssor1 */
    int     use_sparsa ; /* T = use SpaRSA if appropriate, F=never use SpaRSA */
    int    use_startup ; /* T means that the routine hotchol (phase1) is used
                            when use_prior_data is TRUE (FALSE) */
    PPFLOAT  ssordecay ; /* stop ssor1 when errls <= ssordecay * errdual */
    PPFLOAT   ssorcost ; /* if ssorcost*Annz <= Lnnz, use ssor */
    int        ssormem ; /* number of vectors in ssor memory */
    PPINT   ssormaxits ; /* upper bound on number of ssor iterations */
    PPFLOAT  cutfactor ; /* factor used for binding constraints in ascent */
    PPFLOAT    tolssor ; /* stop ssor when err1 <= err/tol2 */
    PPFLOAT    tolprox ; /* prox update when err <= tol2*norm_l */
    PPFLOAT tolrefactor; /* refactorization tolerance for Cholesky factor */
    int badFactorCutoff; /* # consecutive iterations a bad factor is tolerated*/
    /* special parameters related to linear programs */
    int             LP ; /* T => PPROJ is being used to solve an LP */
    PPFLOAT  LinFactor ; /* factor for comparing primal and dual feasibility */
    PPFLOAT LinGrad_tol; /* stopping condition for dual gradient */
} PPparm ;

/* ========================================================================== */
/* === PPstat =============================================================== */
/* ========================================================================== */
typedef struct PPstat_struct
{
    int             status ; /* status of the run */
    int         parm_nprox ; /* max number of proximal updates */
    int            cholmod ; /* TRUE => cholmod is employed */
    int    badFactorCutoff ; /* number attempts to solve dual linear system */
    PPFLOAT          lobad ; /* invalid lower bound for a linear inequality */
    PPFLOAT          hibad ; /* invalid upper bound for a linear inequality */
    PPINT             ibad ; /* index of the bad bound */
    PPFLOAT       grad_tol ; /* relative tolerance for dual function gradient */
    PPINT       ssormaxits ; /* upper bound on number of ssor iterations */
    PPFLOAT        errdual ; /* actual error in the dual function gradient where
                                the error measure is based on the stop condition
                                0 => ||grad L (lambda)||_sup / absAx_sup
                                     where absAx_sup = max_i sum_j |a_{ij}x_j|
                                     x achieves min in dual function
                                1 => ||grad L (lambda)||_sup
                                2 => ||grad L (lambda)||_sup /(absAx_sup + ymax)
                                     where ymax is the sup-norm of the
                                     projection point y */
    PPINT             nrow ; /* number of rows in A */
    int           *updowns ; /* number of updates and downdates of each size */
    int       size_updowns ; /* dimension of updowns array */
    int            *solves ; /* size: maxdepth+1, # of solves by level  */
    int           maxdepth ; /* number of levels in the partition tree */
    int               blks ; /* number of blocks in multilevel partition of A
                                each separator is also counted as a block */
    int             nchols ; /* number of Cholesky factorizations */
    int              nprox ; /* number of proximal updates */
    PPINT       phase1_its ; /* number of iterations in phase 1 */
    PPINT  coor_ascent_its ; /* number of coordinate ascent iterations */
    PPINT        ssor0_its ; /* number of ssor0 iterations */
    PPINT        ssor1_its ; /* number of ssor1 iterations */
    PPINT       sparsa_its ; /* number of SpaRSA iterations */
    PPINT            coldn ; /* number of rank 1 downdates to Cholesky factor */
    PPINT            colup ; /* number of rank 1 updates to Cholesky factor */
    PPINT            rowdn ; /* number of rows dropped from Cholesky factor */
    PPINT            rowup ; /* number of rows added to Cholesky factor */
    PPINT coor_ascent_free ; /* number of variables freed in coordinate ascent*/
    PPINT coor_ascent_drop ; /* number of rows dropped in coordinate ascent */
    PPINT       ssor0_free ; /* number of variables freed in ssor0 */
    PPINT       ssor0_drop ; /* number of rows dropped in ssor0 */
    PPINT       ssor1_free ; /* number of variables freed in ssor1 */
    PPINT       ssor1_drop ; /* number of rows dropped in ssor1 */
    PPINT       sparsa_col ; /* number of bound constraint changes in SpaRSA */
    PPINT       sparsa_row ; /* number of changes in row constraints in SpaRSA*/
    PPINT sparsa_step_fail ; /* number of failures of Armijo step in SpaRSA */
    PPINT           lnnz ; /* number of nonzeros in final Cholesky factor */

    /* timing */
    PPFLOAT    partition ; /* compute reordering of rows of A */
    PPFLOAT   initialize ; /* initialization of variables, includes partition */
    PPFLOAT       phase1 ; /* phase1 */
    PPFLOAT       sparsa ; /* sparsa */
    PPFLOAT  coor_ascent ; /* coor_ascent */
    PPFLOAT        ssor0 ; /* ssor0 */
    PPFLOAT        ssor1 ; /* ssor1 */
    PPFLOAT         dasa ; /* dasa (includes coor_ascent, ssor0, and ssor1) */
    PPFLOAT    dasa_line ; /* dasa line search */
    PPFLOAT     checkerr ; /* check_error */
    PPFLOAT  prox_update ; /* prox_update */
    PPFLOAT       invert ; /* invert permutation of rows and columns */
    PPFLOAT       modrow ; /* modrow (update L by adding or deleting rows) */
    PPFLOAT       modcol ; /* modcol (rank 1 column updates of L) */
    PPFLOAT         chol ; /* cholmod_analyze, cholmod_factorize */
    PPFLOAT      cholinc ; /* incremental cholmod_rowfac */
    PPFLOAT     dltsolve ; /* dltsolve (back solve) */
    PPFLOAT       lsolve ; /* lsolve (forward solve) */
} PPstat ;

/* ========================================================================== */
/* === PPprob =============================================================== */
/* ========================================================================== */
typedef struct PPprob_struct
{
    PPINT         nrow ; /* number of rows in A */
    PPINT         ncol ; /* number of cols in A0 */
    PPINT           ni ; /* number of i s. t. bl_i < bu_i, ni = 0 if nsing > 0*/
    PPINT        nsing ; /* total number of column singletons */
    PPINT          *Ap ; /* size ncol+1, the column pointers */
    PPINT         *Anz ; /* If cholmod is used, then the row indices in each
                            column are reordered so that the active rows are
                            first, followed by the inactive rows. Anz [j]
                            is the number of active rows in column j */
    PPINT          *Ai ; /* size Ap [ncol], the row indices */
    PPFLOAT        *Ax ; /* size Ap [ncol], the numerical values in A */
    PPFLOAT         *y ; /* project y onto polyhedron */
    PPFLOAT         *b ; /* size nrow, right-side, insert 0 for strict ineq. */
    PPINT    *ineq_row ; /* size nsing+ni+2
                            If ni > 0, then ineq_row [1], ...  ineq_row [ni]
                                are the row numbers where bl_i < bu_i,
                                while ineq_row [ni+1] = nrow, a stopper.
                            If nsing > 0, then ineq_row [j] is the row
                                associated with the jth column singleton,
                                while ineq_row [nsing+1] = nrow, a stopper.  */
    PPFLOAT        *bl ; /* size ni+1, bl_i with bl_i < bu_i */
    PPFLOAT        *bu ; /* size ni+1, bu_i with bl_i < bu_i */

    PPFLOAT        *lo ; /* size ncol, Lower bounds for x */
    PPFLOAT        *hi ; /* size ncol, Upper bounds for x */
    PPFLOAT       Amax ; /* absolute maximum element in matrix */
    PPINT       maxrow ; /* maximum number of nonzeros in a row including
                            any singleton. Used in coordinate ascent steps */
    PPINT       maxcol ; /* maximum number of nonzeros in a column.
                            Used in pproj_init */
    PPINT     *colperm ; /* if nonnull, permutation applied to columns of A */
    PPINT     *rowperm ; /* if nonnull, permutation applied to rows of A */
    PPINT    *row_sing ; /* size nrow + 1, sing_row [i] = first index of singc
                            associated with start of row i in A1 */
    PPFLOAT     *singc ; /* size nsing+1, elements of y1 */
    PPFLOAT    *singlo ; /* size nsing+1, -hi1 (for consistency with bl/bu) */
    PPFLOAT    *singhi ; /* size nsing+1, -lo1 */
} PPprob ;

/* ========================================================================== */
/* === PPwork =============================================================== */
/* ========================================================================== */
typedef struct PPwork_struct
{
    int       getfactor ; /* changes to T in check_error if stopping condition
                             holds and Parm->getfactor = T */
    int    size_updowns ; /* dimension of updowns array */
    int        loExists ; /* F => treat input argument lo as -infinity */
    int        hiExists ; /* F => treat input argument hi as +infinity */
    int       ssorquery ; /* TRUE if code should try ssor, FALSE = no ssor*/
    int     return_chol ; /* TRUE if code returns from pproj_dasa with chol */
    int             fac ; /* FALSE (not factored), TRUE (factorization exists)*/
    int  stop_in_hotchol; /* TRUE if we exit in hotchol */
    int            Exit ; /* 1 (terminated in ssor1), 2 (terminated in dasa)*/
    int  shiftl_is_zero ; /* TRUE when the proximal shift_l is zero */
    int   factor_not_OK ; /* # times with large relative error in solution */
    int     return_data ; /* F => free all memory when exiting pproj; otherwise,
                             return the data in the priordata element of the
                             user's ppdata structure. */
    PPINT *user_row_sing; /* user's row_sing */
    PPINT          ATnz ; /* # nonzeros in active rows of full matrix */
    PPINT          Annz ; /* # nonzeros in active rows and free columns of A */
    PPINT          Lnnz ; /* # nonzeros in chol (AF * AF') */

    cholmod_sparse   *A ; /* A   matrix in cholmod sparse format */
    cholmod_sparse *AFT ; /* AFT matrix in cholmod sparse format */

    /* AT is the transpose of the A matrix, compact format */
    PPINT          *ATp ; /* size nrow + 1, the column pointers */
    PPINT          *ATi ; /* size Ap [ncol], the column indices */
    PPFLOAT        *ATx ; /* size Ap [ncol], the numerical values in A */

    /* AFT is the transpose of the AF matrix, the submatrix of A associated
       with the free variables */
    PPINT         *AFTp ; /* size nrow+1, the column pointers */
    PPINT        *AFTnz ; /* size nrow, number of nonzeros in each row */
    PPINT         *AFTi ; /* size Ap [ncol], the column indices */
    PPFLOAT       *AFTx ; /* size Ap [ncol], the numerical values in A */

    PPFLOAT          *x ; /* size: ncol */
    PPFLOAT    *shift_l ; /* The proximal shift in lambda. When a nonzero
                             starting guess is given, set shift_l = lambda */
    PPFLOAT     *lambda ; /* size: nrow */
    PPFLOAT *lambda_tot ; /* size: nrow, lambda + shift_l */
    PPFLOAT    *dlambda ; /* size: nrow, the change in lambda */

    PPFLOAT start_sigma ; /* initial value for sigma, used if use_prio_data =T*/
    PPFLOAT       sigma ; /* current value for prox regularization parameter */
    PPFLOAT      Asigma ; /* offset to diagonal of A_F A_F' in LDL' factoriza */
    PPFLOAT    Totsigma ;  /* sigma + Asigma */

    PPINT           *ns ; /* size: ntot, EMPTY always, used in line search */
    PPINT            *F ; /* size: ncol, free columns */
    int             *ib ; /* size: ntot, ib [j] defines the status of a column:
                             0 : column j is free
                             1 : column j is at the upper bound
                            -1 : column j is at the lower bound */
    PPINT           *ir ; /* size: nrow, nsingni = nsing + ni (ni or nsing = 0).
                             ir gives status of row i:
                     ir [i] =  0 for an equality constraint
                            =  1 for an active singleton row
                            =  ineq # for active inequality at upper bound
                            = -ineq # for active inequality at lower bound
                            =  ineq # or singleton # + nsingni for a dropped
                               constraint */
                                
    PPINT  *RowmodFlag ; /* size: nrow, empty if inequality not modified,
                            otherwise points into RowmodList showing rows
                            to modify*/
    PPINT  *RowmodList ; /* size: nrow, first part of this list contains the
                            rows to delete, the tail contains rows to add */

    PPINT  *ColmodFlag ; /* size: ncol, same as row flag and list, but
                            delete and add indices are flipped */
    PPINT  *ColmodList ; /* size: ncol */

    PPFLOAT         *b ; /* size: nrow, shifted b vector for current level */
    PPFLOAT         *c ; /* size: ntot, shifted cost vector for curr. level */
    PPFLOAT      *cold ; /* size: ncol, c at start of the ascent iteration */
    PPFLOAT        *lo ; /* size: ncol, Lower bounds in translated problem */
    PPFLOAT        *hi ; /* size: ncol, Upper bounds in translated problem */
    PPFLOAT        *bl ; /* size: nrow, user bl except that NULL->-infty */
    PPFLOAT        *bu ; /* size: nrow, user bu except that NULL->+infty */
    PPFLOAT         *D ; /* size: nrow, diagonal of AF*AF' */

    PPINT      *arrayi ; /* int work array (malloc'd in pproj_init) */
    PPFLOAT    *arrayd ; /* double work array (malloc'd pproj_init) */
    PPINT     *RLinkUp ; /* size nrow+1 linked list for active equations */
    PPINT     *RLinkDn ; /* size nrow+1 linked list for active equations */
                         /* numbering of strict inequalities (also referred to
                            as column singletons) starts at 1 instead of 0 */
    PPINT     *SLinkUp ; /* size ni+3 linked list for row active singletons */
    PPINT     *SLinkDn ; /* size ni+3 linked list for row active singletons */
    PPINT     *uLinkUp ; /* size nsing+2,linked list for col active singletons*/
    PPINT     *uLinkDn ; /* size nsing+2, linked list */
    PPINT     *lLinkUp ; /* shares space with uLinkUp */
    PPINT     *lLinkDn ; /* shares space with uLinkDn */
    PPINT         *shi ; /* size nrow, points to 1st singleton at upper bound */
    PPINT         *slo ; /* size nrow, points to 1st singleton at lower bound */
    int        ssormem ; /* number of vector in ssor memory */
    PPINT    ssor1_its ; /* stop ssor1 if no change in active set in ssor1_its*/

    /* ---------------------------------------------------------------------- */
    /* scalars */
    /* ---------------------------------------------------------------------- */

    PPINT      nrowadd ; /* number of rows to add to AF */
    PPINT      nrowdel ; /* number of rows to delete from AF */
    PPINT      ncoladd ; /* number of columns to add to AF */
    PPINT      ncoldel ; /* number of columns to delete from AF */
    PPINT      nactive ; /* number of active rows in upcoming L */
    PPINT           nf ; /* number of currently free variables (zeros in ib)*/
    int        do_coor ; /* T => perform coordinate ascent */
    int        do_ssor ; /* T => perform ssor ascent */
    PPINT     chg_coor ; /* # freed variables and dropped rows in coor_ascent */
    PPINT    chg_ssor0 ; /* # freed variables and dropped rows in ssor0 */
    PPINT    chg_ssor1 ; /* # freed variables and dropped rows in ssor1 */
    PPINT   chg_sparsa ; /* # variables or rows that change status in sparsa */
    PPFLOAT      normx ; /* 1-norm of x */
    PPFLOAT      absAx ; /* stores max_i sum_j |A_{ij}x_j| */
    PPFLOAT     absAxk ; /* stores max_i sum_j |A_{ij}x_{kj}|| */
    PPFLOAT       ymax ; /* stores sup-norm of projection point y */
    PPFLOAT       cerr ; /* multiplier error in LP */
    PPFLOAT       berr ; /* constraint violation error in LP */
    PPFLOAT    epsilon ; /* proximal parameter used for LP's */
    PPFLOAT    errdual ; /* norm of dual gradient (with normalization) */
    PPFLOAT     norm_l ; /* norm of lambda */
    PPFLOAT      grad0 ; /* SpaRSA monitors undecided set when grad <= grad0 */
    PPFLOAT      gamma ; /* SpaRSA stopping parameter */
    int       sparsaOK ; /* T => condition for using sparsa satisfied */

    /* ========== arrays and variable used in update/downdate ========== */
    cholmod_common *cmm; /* Common block for CHOLMOD */
    PPINT     *dropped ; /* list of rows dropped in modrow since last
                            updateAnz */

    /* C and L allocated in lpdasa_initupdate and lpdasa_initrun */
    cholmod_factor  *L ; /* Cholesky factor */

    PPFLOAT *changeRHS ; /* size: nrow, right side change for forward
                            solve update */
    PPFLOAT    *newrow ; /* size: nrow, new row added in rowmod_prep */
    PPINT          *Cp ; /* size ncol, pointers into Ai or Ax of columns
                            to add or delete */
    PPINT         *Cnz ; /* size ncol, number of nonzeros in columns to
                            add or delete */
    PPINT     *colmark ; /* size: ncol, gives botrow for each column */

    /* ---------------------------------------------------------------------- */
    /* scalars */
    /* ---------------------------------------------------------------------- */

    int             nd ; /* total number of dropped rows since updataAnz */
    PPFLOAT       npup ; /* total number of partial updates/downdates */
    PPFLOAT       nrup ; /* total number of rooted updates/downdates */
    int       npup_old ; /* number of partial updates in previous ascent */
    int       npup_cur ; /* number of partial updates in current ascent */
    PPFLOAT   rupflops ; /* total number of flops in a rooted update */
    PPFLOAT   pupflops ; /* total number of flops in a partial update */
    int         nchols ; /* total number of chols */
    PPFLOAT  cholflops ; /* flops in last chol (excl AA') */
    PPFLOAT  cholaatflops ;/* total flops in chols (incl AA'
                              and incremental rowfac) */

    /* ==== arrays and variables used in multilevel implementation ==== */
    int           blks ; /* number of blocks in the multilevel partition */
    int       maxdepth ; /* number of levels in the partition */
    int          *Kids ; /* size: blks, list of children */
    int         *nkids ; /* size: blks, number of children of a node */
    int        *parent ; /* size: blks, defines tree in multilevel partition*/
    int            *Kp ; /* size: blks, points into array Kids. kids of node
                            are in list Kids [Kp [node] ... nkids [node]]*/
    int         *depth ; /* size: blks, depth of each node in tree */
    int      *leftdesc ; /* size: blks, for each block, left descendant */
    PPINT   *col_start ; /* size: blks+1, for each block, first column */
    PPINT   *sol_start ; /* size: blks+1, for each block, first singleton */
    PPINT   *row_start ; /* size: blks+1, for each block, 1st row in matrix */
    int    *sol_to_blk ; /* size: ni+2, for each singleton, 1st block in
                            matrix, set sol_to_blk [ni+1] = blks */

    /* lstart and ustart are associated with the inequalities that are
       strict.  For each block in the multilevel decomposition,
       lstart points to the first singleton at its lower bound while ustart
       points to the first singleton at it upper bound. Rstart and Rend
       contain the first and last active row of each block.
       Arrays joblist and kidsleft are used in the multilevel implementation.
       joblist contain the blocks that are solved to generate the current
       search direction. For each block in the list, we treat all the
       variables as being fixed except for the variables associated with
       the block. The variables in the blocks, with the variables
       outside these blocks fixed, are completely uncoupled in the
       dual problem, so we can perform a DASA step by solving for these
       variables in an uncoupled fashion. We start at the leaves of the
       tree and work up to the root. Once all the childen of a node
       are optimized, we move up to the parent. jobcols is the number
       of columns associated with this each block that have been added
       while jobrows is the number of rows in this block that have
       been deleted.  */
    PPINT      *lstart ; /* size blks + 1 */
    PPINT      *ustart ; /* size blks + 1 */

    int       *joblist ; /* size blks */
    int      *kidsleft ; /* size blks */
    PPINT     *jobcols ; /* size blks + 1 */
    PPINT     *jobrows ; /* size blks + 1 */
    PPINT      *Rstart ; /* size blks + 1 */
    PPINT        *Rend ; /* size blks + 1 */
} PPwork ;

/* ========================================================================== */
/* === PPcheck ============================================================== */
/* ========================================================================== */
typedef struct PPcheck_struct
{

    /* ---------------------------------------------------------------------- */
    /* sizes of allocated blocks */
    /* ---------------------------------------------------------------------- */

    PPFLOAT      prior ; /* prior objective value */
    PPFLOAT       mark ; /* current objective value (not used for comparisons)*/
    PPFLOAT       zmax ; /* max component of the x that minimizes Lagrangian */
    PPFLOAT       lmax ; /* max component of the current lambda */
    int       location ; /* 1 = phase1, 2 = dasa, 3 = ssor0, 4 = ssor1,
                            5 = check_error, 6 = sparsa */
    PPFLOAT         *b ; /* pointer to the right side, used for checking
                            right side when solving an LP */
    PPFLOAT        *lo ; /* pointer to the lo, used for checking
                            lower bounds when solving an LP */
    PPFLOAT        *hi ; /* pointer to the hi, used for checking
                            upper bounds when solving an LP */
} PPcheck ;

/* ========================================================================== */
/* === PPcom ================================================================ */
/* ========================================================================== */
typedef struct PPcom_struct
{
    PPprob    *Prob ; /* Problem */
    PPparm    *Parm ; /* Parameters */
    PPstat    *Stat ; /* Statistics */
    PPwork    *Work ; /* Working arrays and parameters that change */
    PPcheck  *Check ; /* Check structure */
} PPcom ;

/* ========================================================================== */
/* === PPdata =============================================================== */
/* ========================================================================== */
typedef struct PPdata_struct
{
    PPFLOAT         *lambda ; /* size nrow. If parameter start_guess = 3, then
                                 stores the starting guess for the constraint
                                 multiplier.  If NULL, then malloc'd by pproj.
                                 Used to return final multiplier for constraint.
                                 Any allocated memory is freed by
                                 pproj_terminate */
    PPFLOAT              *x ; /* size ncol+nsing, solution (if NULL, then
                                 malloc'd by pproj and freed by running
                                 pproj_terminate). */
    PPcom        *priordata ; /* data from prior run */
    PPparm            *Parm ; /* parameters */
    PPstat            *Stat ; /* statistics */
    PPFLOAT              *y ; /* size ncol, y0 */
    PPINT                ni ; /* # strict inequality (-1 => pproj computes) */
    PPINT             nsing ; /* number of column singletons in A1 */
    PPINT              nrow ; /* number of rows in A0 */
    PPINT              ncol ; /* number of cols in A0 */
    PPINT               *Ap ; /* size ncol+1, column pointers for A0 */
    PPINT               *Ai ; /* size Ap [ncol], row indices for A0,
                                 increasing order in each column */
    PPFLOAT             *Ax ; /* size Ap [ncol], numerical entries A0 */
    PPFLOAT             *lo ; /* size ncol, lower bounds, NULL=>use -infinity */
    PPFLOAT             *hi ; /* size ncol, upper bounds, NULL=>use +infinity */
    PPFLOAT             *bl ; /* size nrow, lower bounds, NULL=>use -infinity */
    PPFLOAT             *bu ; /* size nrow, upper bounds, NULL=>use +infinity
                                 use the same pointers for bl and bu when the
                                 upper and lower bounds on b are the same */
    PPINT         *row_sing ; /* if not NULL, size nrow+1, sing_row [row] =index
                                 of first element of y1 for each row of A1 */
    PPFLOAT         *singlo ; /* if not NULL, size nsing, elements of lo1 */
    PPFLOAT         *singhi ; /* if not NULL, size nsing, elements of hi1 */
    PPFLOAT          *singc ; /* if not NULL, size nsing, elements of y1 */

    /* the following are used internally when the code allocates memory */
    PPFLOAT *lambda_created ; /* pointer to memory created for lambda */
    PPFLOAT      *x_created ; /* pointer to memory created for x */

} PPdata ;

/* ========================================================================== */
/* === Prototypes of PPROJ routines ========================================= */
/* ========================================================================== */
int pproj  /* return status 0 if solution found, see pproj.h for nonzero ints */
(
    PPdata *ppdata /* Structure containing pasa input data. Initialize it
                      using pproj_setup and then modify entries to describe
                      the user's problem */
) ;

void * pproj_malloc
(
    int *status,
    PPINT     n,
    int    size
) ;

void pproj_free
(
    void *p
) ;

PPdata * pproj_setup (void) ;

void pproj_terminate
(
    PPdata **DataHandle
) ;

void pproj_default
(
    PPparm *Parm /* Parameter structure */
) ;

void pproj_print_status
(
    PPdata *Data /* pproj data structure */
) ;

void pproj_print_stat
(
    PPdata *Data /* pproj data structure */
) ;

void pproj_print_parm
(
    PPdata *Data /* pproj data structure */
) ;

void pproj_print_TF
(
    int TF /* TRUE or FALSE */
) ;

PPFLOAT pproj_KKTerror /* returns the largest of the primal and dual errors */
(
    PPFLOAT   *errg, /* sup norm dist of g to 0 relative to sup-norm of absAx
                        (only returned when not NULL) */
    PPFLOAT   *errx, /* 1 norm relative difference of x and x(lamba)
                        (only returned when not NULL) */
    PPFLOAT  *absAx, /* sup norm of absAx (only returned when not NULL) */
    PPdata  *ppdata  /* problem data and computed solution */
) ;

void pproj_error
(
    int status,
    const char *file,
    int line,
    const char *message
) ;

void pproj_wrapup
(
    int      status, /* termination status */
    int  fastreturn, /* T => return after printing status */
    PPdata  *ppdata,
    PPcom **Ihandle
) ;

void pproj_freeAll
(
    PPcom **Ihandle
) ;

int pproj_check_error /* return status:
                                 PPROJ_SOLUTION_FOUND
                                 PPROJ_TOLERANCE_NOT_MET
                                 PPROJ_PROX_UPDATE */
(
    PPcom *I
) ;

int pproj_prox_update
(
    PPcom *I
) ;

void pproj_invert
(
    PPcom *I
) ;

void pproj_cholmod_sparse
(
    cholmod_sparse *A, /* pointer to a cholmod sparse matrix */
    PPINT    nrow, /* number of rows */
    PPINT    ncol, /* number of columns */
    PPINT   nzmax, /* max number of nonzeros */
    PPINT      *p, /* size ncol + 1, the column pointers */
    PPINT     *nz, /* size ncol, # nonzeros in each column, may be NULL */
    PPINT      *i, /* size Ap [ncol], the row indices */
    PPFLOAT    *x, /* size Ap [ncol], the numerical values in A */
    int    sorted, /* TRUE if columns of A are sorted, FALSE otherwise */
    int    packed, /* TRUE if A is packed, FALSE otherwise */
    int     xtype  /* CHOLMOD_PATTERN or CHOLMOD_REAL */
) ;

void pproj_cholmod_dense
(
    cholmod_dense *A, /* pointer to a cholmod dense matrix */
    PPINT       nrow, /* number of rows */
    PPFLOAT       *x  /* size nrow, the numerical values in A */
) ;

void pproj_transpose
(
    PPINT   *Bp,   /* size nrow+1, column pointers (output) */
    PPINT   *Bi,   /* size Ap [ncol], row indices of B (output) */
    PPFLOAT *Bx,   /* size Ap [ncol], numerical entries of B (output) */
    PPINT   *Ap,   /* size ncol+1, column pointers */
    PPINT   *Ai,   /* size Ap [ncol], row indices for A */
    PPFLOAT *Ax,   /* size Ap [ncol], numerical entries of A */
    PPINT  nrow,   /* number of rows in A */
    PPINT  ncol,   /* number of cols in A */
    PPINT    *W    /* work array of size nrow */
) ;

void pproj_iminsort
(
    PPINT  *y, /* n-by-1 (output) */
    PPINT  *x, /* n-by-1 (input not modified) */
    PPINT  *w, /* n-by-1, (input, working array) */
    PPINT   n  /* number of elements to sort */
) ;

void pproj_xminsort
(
    PPINT   *y, /* n-by-1 (output) */
    PPFLOAT *x, /* n-by-1 (input not modified) */
    PPINT   *w, /* n-by-1, (input, working array) */
    PPINT    n  /* number of elements to sort */
) ;

void pproj_copyi
(
    PPINT       *y, /* output of copy */
    PPINT const *x, /* input of copy */
    PPINT const  n  /* length of vectors */
) ;

void pproj_copyi_int
(
    int  *y, /* output of copy */
    int  *x, /* input of copy */
    PPINT n  /* length of vectors */
) ;

void pproj_copyx
(
    PPFLOAT       *y, /* output of copy */
    PPFLOAT const *x, /* input of copy */
    PPINT   const  n  /* length of vectors */
) ;

void pproj_initi
(
    PPINT *x,  /* array to be initialized */
    PPINT  s,  /* scalar */
    PPINT  n   /* length of x */
) ;

void pproj_initx
(
    PPFLOAT *x,  /* array to be initialized */
    PPFLOAT  s,  /* scalar */
    PPINT   n   /* length of x */
) ;

void pproj_initFx
(
    PPFLOAT *x,  /* array to be initialized */
    PPFLOAT  s,  /* scalar */
    PPINT   *F,  /* indices to be initialized */
    PPINT    n   /* length of F */
) ;

void pproj_initstat
(
    PPstat *Stat
) ;

void pproj_scale
(
    PPFLOAT *x,  /* array to be scaled */
    PPFLOAT *y,  /* array used for the scaling */
    PPFLOAT  s,  /* scale */
    PPINT    n   /* length of x */
) ;

PPFLOAT pproj_dot
(
    PPFLOAT *x,
    PPFLOAT *y,
    PPINT    n  /* length of x */
) ;

PPFLOAT pproj_sup_norm
(
    PPFLOAT const *x, /* vector */
    PPINT   const  n  /* length of vector */
) ;

void pproj_minheap_build
(
    PPINT *heap, /* on input, an unsorted set of element numbers */
    PPFLOAT  *x, /* the numerical values to be ordered */
    PPINT nheap  /* number of elements to build into the heap */
) ;

void pproj_minheap_ify
(
    PPINT     p, /* start at node p in the heap */
    PPINT *heap, /* size n, containing indices into x */
    PPFLOAT  *x, /* not modified */
    PPINT nheap  /* heap [1 ... nheap] is in use */
) ;

void pproj_minheap_add
(
    PPINT   leaf, /* the new leaf */
    PPINT  *heap, /* size n, containing indices into x */
    PPINT    *ns, /* pointer from node to store in heap */
    PPFLOAT   *x, /* not modified */
    PPINT *nheap   /* number of elements in heap including new one */
) ;

void pproj_minheap_delete
(
    PPINT  *heap, /* containing indices into x, 1..n on input */
    PPINT    *ns, /* pointer from node to store */
    PPFLOAT   *x, /* not modified */
    PPINT *nheap, /* number of items in heap */
    PPINT      p  /* element to delete from the heap */
) ;

void pproj_minheap_update
(
    PPINT *heap, /* size n, containing indices into x */
    PPINT   *ns, /* pointer from node to store in heap */
    PPFLOAT  *x, /* not modified */
    PPINT nheap, /* number of elements in the heap */
    PPINT     p  /* location of element to update */
) ;

void pproj_minheap_ns
(
    PPINT     p, /* start at node p in the heap */
    PPINT *heap, /* size n, containing indices into x */
    PPINT   *ns, /* pointer from node to store */
    PPFLOAT  *x, /* not modified */
    PPINT nheap  /* heap [1 ... nheap] is in use */
) ;

void pproj_step
(
    PPFLOAT       *xnew, /* updated x vector */
    PPFLOAT const    *x, /* current x */
    PPFLOAT const    *d, /* search direction */
    PPFLOAT const alpha, /* stepsize */
    PPINT   const     n  /* dimension */
) ;

void pproj_saxpy
(
    PPFLOAT *x,
    PPFLOAT *y,
    PPFLOAT  s,
    PPINT    n  /* dimension of the vectors */
) ;

PPFLOAT pproj_max
(
    PPFLOAT *x,
    PPINT    n  /* dimension of x */
) ;

double pproj_timer ( void ) ;

int pproj_init
(
    PPcom       *I, /* pproj's common structure for all the routines */
    PPdata *ppdata  /* user problem description */
) ;

int pproj_phase1
(             
    PPcom *I
) ;

int pproj_hotchol
(
    PPcom *I
) ;

int pproj_sparsa
(
    PPcom *I
) ;

void pproj_coor_ascent
(          
    PPcom *I
) ;

void pproj_ssor0
(
    PPcom *I
) ;

int pproj_ssor1
(
    PPcom *I
) ;

int pproj_updown_dense
(
    PPFLOAT    *L, /* lower triangle of factorization (beneath diagonal) */
    PPFLOAT *diag, /* D in the LDL' factorization */
    PPFLOAT    *w, /* update/downdate matrix */
    int      info, /* +1 = update, -1 = downdate */
    PPINT       n  /* rank of the matrix */
) ;

int pproj_dasa
(
    PPcom *I
) ;

cholmod_factor *pproj_rechol
(
    cholmod_sparse   *A,
    cholmod_sparse *AFT,    /* A(:,f)' */
    PPINT            *F,    /* the free set f = columns F [0..nf-1] */
    PPINT            nf,
    PPFLOAT    beta [2],
    PPINT      *RLinkUp,
    PPwork           *W,
    cholmod_common *cmm
) ;

void pproj_modrow
(
    PPcom            *I,
    int              nj, /* number of jobs in multilevel update,
                          ignored if no solve update */
    int   MarkedForward, /* = TRUE (use botrow to update forward solve
                            = FALSE (botrow not needed in forward solve) */
    int     UpdateSolve, /* = TRUE (forward solve update)
                            = FALSE (only update factorization) */
    int           RowOp, /* = +1 (row is added)
                            = -1 (row is deleted) */
    PPFLOAT    *forward, /* forward solve */
    PPFLOAT  *changeRHS, /* change in right hand side */
    PPFLOAT         *dl, /* change in lambda */
    PPINT   *updatework  /* nrow int work space needed when UpdateSolve TRUE */
) ;

void pproj_modcol
(
    PPcom           *I,
    int  MarkedForward, /* = 0 (botrow not needed forward solve)
                           = 1 (use botrow to update forward solve) */
    int    UpdateSolve, /* = 0 (only update factorization)
                           = 1 (forward solve update) */
    int          ColOp, /* = +1 (cols are added)
                           = -1 (cols are deleted) */
    PPINT     *Colmark, /* bottom row of block associated with added columns */
    PPINT          *Cp, /* pointers into Ai or Ax of columns to add or delete */
    PPINT         *Cnz, /* number of nonzeros in columns to add or delete */
    PPFLOAT   *forward, /* forward solve */
    PPFLOAT *changeRHS, /* change in right hand side */
    PPINT           nf  /* number of columns to add */
) ;

void pproj_lsol_partial
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPINT      jstart,
    PPINT      botrow,
    PPINT     *RLinkUp
) ;

void pproj_lsol
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPINT      jstart,
    PPINT      botrow,
    PPINT     *RLinkUp
) ;

void pproj_lsolve
(
    PPwork      *W,
    PPFLOAT     *X, /* X [0 .. (L->ncol)-1], right hand side, on input.
                           solution to Lx=b in locations jstart to botrow
                           on output */
    PPINT *RLinkUp,
    PPINT   jstart, /* either toprow or seprow */
    PPINT   botrow,
    int     update
) ;

void pproj_dltsol
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPFLOAT *Xforward,
    PPINT        iend,
    PPINT      toprow,
    PPINT    *RLinkDn
) ;

void pproj_dltsol_partial
(
    cholmod_factor *L,
    PPFLOAT        *X,
    PPFLOAT *Xforward,
    PPINT        iend,
    PPINT      toprow,
    PPINT    *RLinkDn,
    PPINT      botrow
) ;

void pproj_dltsolve
(
    PPwork        *W,
    PPFLOAT       *X, /* X [0 .. (L->ncol)-1], right hand side, on input. */
    PPFLOAT *forward, /* solution to DL'x=b, on output */
    PPINT   *RLinkDn,
    PPINT     toprow,
    PPINT       iend,
    PPINT     update,
    PPINT     botrow
) ;

void pproj_lsolve0
(
    PPwork      *W,
    PPFLOAT     *X, /* X [0 .. (L->ncol)-1], right hand side, on input.
                       solution to Lx=b in locations jstart to botrow
                       on output */
    PPINT *RLinkUp,
    PPINT *RLinkDn,
    PPINT  *Rstart, /* return the new Rstart for botblk */
    PPINT   jstart, /* first row in seperator block */
    PPINT   toprow,
    PPINT   seprow,
    PPINT   botrow,
    int     update
) ;

PPFLOAT pproj_upspeed
(
    PPFLOAT  fl, /* flops to perform a chol (excludes AF*AF') */
    PPFLOAT lnz /* nonzeros in cholesky factor */
) ;

int pproj_cholquery
(
    PPcom *I
) ;

void pproj_iterquery
(
    PPcom *I
) ;

void pproj_updateAnz
(
    PPcom     *I,
    int location    /* = 0 means code called at the top of ascent
                           before adding the new rows to L
                        = 1 means at the factorization at the 
                            top of ascent
                        = 2 means inside the ascent iteration, it
                            was cheaper to refactor than update */
) ;

void pproj_rowadd_prep
(
    PPINT             k, /* number of the row to add */
    PPcom            *I,
    cholmod_sparse   *A, /* the matrix */
    PPINT          *ati, /* column numbers in row */
    PPFLOAT        *atx, /* nonzeros in row */
    PPINT            nz, /* number of nonzeros */
    cholmod_sparse   *R, /* new row of AF*AF' */
    PPINT         ndead, /* number of currently dead rows still to be added */
    PPINT    *dead_rows, /* row numbers of currently dead rows */
    cholmod_common *cmm
) ;
/* prototypes for print routines */
#include "pproj_print.h"

/* prototypes for check routines */
#include "pproj_check.h"

#endif
