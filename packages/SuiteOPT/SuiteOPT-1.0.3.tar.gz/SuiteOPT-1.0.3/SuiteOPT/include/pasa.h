#ifndef _PASA_H_
#define _PASA_H_

#include "pproj.h"
#include "napheap.h"
#include "cg_descent.h"

#define PASAFLOAT SuiteOPTfloat
#define PASAINT SuiteOPTint
#define PASAZERO ((PASAFLOAT) 0)
#define PASAONE  ((PASAFLOAT) 1)
#define PASATWO  ((PASAFLOAT) 2)

#define PASAMAX(a,b) ( ((a) > (b)) ? (a) : (b) )
#define PASAMIN(a,b) ( ((a) < (b)) ? (a) : (b) )

#define FALSE SuiteOPTfalse
#define TRUE SuiteOPTtrue

/* infinite integer */
#define PASAINFINT SuiteOPTinfint

/* infinite float */
#define PASAINF SuiteOPTinf

/* if the user only wants to solve bound constrained problems
   and pproj is not needed, then the following statement can
   be uncommented and the pproj library will not be formed */
/*
#define NOPPROJ
*/

/* ==========================================================================
   Status returned to the user by pasa if the run was successful or
   it terminates with an error inside pasa. Otherwise, the value of
   status corresponds to the routine where termination occurred.
   ========================================================================== */

#define PASA_ERROR_TOLERANCE_SATISFIED                            (0)
#define PASA_POLYHEDRON_INFEASIBLE                                (1)
#define PASA_INVALID_VARIABLE_BOUNDS                              (2)
#define PASA_INVALID_LINEAR_CONSTRAINT_BOUNDS                     (3)
#define PASA_INVALID_MATRIX_ELEMENT                               (4)
#define PASA_ITERATIONS_EXCEED_MAXITS_IN_GRAD_PROJ                (5)
#define PASA_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS_IN_GRAD_PROJ       (6)
#define PASA_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS_IN_ACTIVEGP        (7)
#define PASA_OUT_OF_MEMORY                                        (8)
#define PASA_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION_IN_GRAD_PROJ  (9)
#define PASA_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION_IN_ACTIVEGP  (10)
#define PASA_MUST_USE_CHOLMOD                                    (11)
#define PASA_STARTING_FUNCTION_VALUE_INFINITE_OR_NAN             (12)
#define PASA_FUNCTION_NAN_OR_INF                                 (13)
#define PASA_LAMBDA_IS_NULL_BUT_USE_LAMBDA_IS_TRUE               (14)
#define PASA_MATRIX_INCOMPLETE                                   (15)
#define PASA_FUNCTION_VALUE_OR_GRADIENT_MISSING                  (16)
#define PASA_MATRIX_GIVEN_BUT_RHS_MISSING                        (17)
#define PASA_RHS_GIVEN_BUT_MATRIX_MISSING                        (18)
#define PASA_MISSING_OBJECTIVE                                   (19)
#define PASA_PROBLEM_OVERSPECIFIED                               (20)
#define PASA_BOTH_A_AND_A_EXIST                                  (21)
#define PASA_WRONG_HPROD_GIVEN                                   (22)
#define PASA_PROBLEM_DIMENSION_NOT_GIVEN                         (23)
#define PASA_QUADRATIC_OBJECTIVE_NO_LINEAR_TERM                  (24)
#define PASA_START_MESSAGES                                       (0)
#define PASA_END_MESSAGES                                        (99)

/* not seen by user, used for flow control in pasa */
#define PASA_OK                                                  (-1)
#define PASA_SWITCH_ALGORITHM                                    (-2)
#define PASA_NEW_ACTIVE                                          (-3)
#define PASA_NO_CHANGE_IN_ACTIVE                                 (-4)
#define PASA_GRAD_PROJ                                           (-5)
#define PASA_ACTIVE_GP                                           (-6)
#define PASA_GRADPROJ_LP                                         (-7)
#define PASA_CG_DESCENT                                          (-8)
#define PASA_BASE_CODE                                           (-9)
#define PASA_ERROR_TOLERANCE_HOLDS_IN_CG                        (-10)
#define PASA_HITS_BOUNDARY_IN_CG                                (-11)
#define PASA_TRY_PROJECT2                                       (-12)
#define PASA_UNC                                                (-13)
#define PASA_BNC                                                (-14)
#define PASA_LP                                                 (-15)
#define PASA_QP                                                 (-16)
#define PASA_NL                                                 (-17)
#define PASA_NAPSACK                                            (-18)
#define PASA_PROJ                                               (-19)

/* -------------------------------------------------------------------------- */
/* pasa version information */
/* -------------------------------------------------------------------------- */
#define PASA_DATE "October 21, 2019"
#define PASA_MAIN_VERSION 1
#define PASA_SUB_VERSION 0
#define PASA_SUBSUB_VERSION 0

#define SET_USERX1 \
col = Com->sj [l] ; \
if ( col >= 0 ) \
{ \
    if ( Com->sx [l] > PASAZERO ) \
    { \
        userx [col] = Com->shi[l] ; \
    } \
    else \
    { \
        userx [col] = Com->slo[l] ; \
    } \
}

#define SET_USERX2 \
col = Com->sj [l] ; \
if ( col >= 0 ) \
{ \
    if ( Com->sx [l] > PASAZERO ) \
    { \
        userx [col] = Com->slo[l] ; \
    } \
    else \
    { \
        userx [col] = Com->shi[l] ; \
    } \
}

/* ==========================================================================
   =============== structures ===============================================
   ========================================================================== */

/* ==========================================================================
    PASAparm is a structure containing user controlled parameters related
    to PASA.  PASAdefault assigns default parameters values.
   ========================================================================== */
typedef struct PASAparm_struct
{
    /* Problem classifications, use EMPTY (-1) if not specified in any case).
       At most one true. If all are EMPTY (default), then the autodetect routine
       will determine the classification based on the input data in pasadata. */
    int UNC ;     /* T => unconstrained optimization */
    int BNC ;     /* T => bound constrained optimization */
    int LP  ;     /* T => linear program */
    int QP  ;     /* T => quadratic program */
    int NL  ;     /* T => nonlinear objective, polyhedral constraints */
    int NAPSACK ; /* T => separable convex quadratic obj., napsack constraint */
    int PROJ ;    /* T => projection on polyhedran */

    /* KKT error tolerance */
    PASAFLOAT grad_tol ;

    /* T => print status of run
       F => do not print status of run */
    int PrintStatus ;

    /* T => print statistics for pasa, pproj, and napheap if used
       F => do not print statistics */
    int PrintStat ;

    /* T => print all parameters values
       F => do not display parmeter values */
    int PrintParm ;

    /* Level 0  = no printing, ..., Level 3 = maximum printing */
    int PrintLevel ;

    /* T => only use gradient projection algorithm
       F => let algorithm decide between grad_proj and cg */
    int GradProjOnly ;

    /* T => when CG hits boundary of feasible region, branch to active set
            grad_proj
       F => when CG hits boundary, restart CG */
    int use_activeGP ;

    /* T => use NAPHEAP algorithm for the projection when there is one row in A
       F => always use PPROJ for the projection */
    int use_napheap ;

    /* T => use a provided routine to evaluate the Hessian at a given iterate
       F => Hessian is not provided
       CURRENTLY, THIS MUST BE FALSE SINCE PASA DOES NOT UTILIZE HESSIANS */
    int use_hessian ;

    /* T => lower bounds for x are present
       F => ignore lo, treat lo as -infinity */
    int loExists ;

    /* T => upper bounds for x are present
       F => ignore hi, treat hi as +infinity */
    int hiExists ;
    /* by default, loExists and hiExists are TRUE, an easy way to remove either
       lo or hi from the problem is to set the pasadata input lo or hi to NULL.
       Then they are removed from the problem regardless of the values of
       loExists or hiExists. */

    /* ..... Start of LP parameters ..... */
    int updateorder ; /* 1 or 2 (currently 2 not implement) */

    /* epsilon is multiplied by EpsilonDecay when b_err * b_factor <= c_err */
    PASAFLOAT epsilon ; /* proximal parameter */

    /* factor used to decide when to let the proximal parameter epsilon grow */
    PASAFLOAT cerr_decay ;

    /* epsilon is multiplied by EpsilonGrow when c_err <= cerr_decay*grad_tol */
    PASAFLOAT EpsilonGrow ;

    /* epsilon is multiplied by EpsilonDecay when b_err * b_factor <= c_err */
    PASAFLOAT EpsilonDecay ;
    /* ..... End of LP parameters ..... */

    /* an adjustment added to a linear or quadratic cost objective when it is
       evaluated */
    PASAFLOAT fadjust ;

    /* T => use the input starting guess for the dual multiplier lambda
            associated with the constraints for the first projection
       F => starting guess in the first projection is lambda = 0
       For the subsequent projections, the starting guess is determined by
       the parameter pproj_start_guess. */
    int use_lambda ;

    /* pproj_start_guess is based on the bound structure associated with the
       prior projection */
    int pproj_start_guess ;

    /* T => include multiplier term lambda'(Ax - b) + 0.5p||Ax-b||^2
            in objective when using CG
       F => unmodified objective */
    int use_penalty ;

    /* penalty when use_penalty = T */
    PASAFLOAT penalty ;

    /* debug = T => check that f_k+1 - f_k <= debugtol*fR.
       debug = F => no checking of function values */
    int          debug ;
    PASAFLOAT debugtol ;

    PASAFLOAT switchfactor; /* switch to grad_proj when local error
                               < switchfactor*global error */
    PASAFLOAT switchdecay ; /* switchfactor multiplied by switch decay when
                               undecided index set becomes empty */

    /* if terminate_agp iterations are performed in the active set gradient
       projection algorithm with no new active constraints, then branch to cg */
    int terminate_agp ;

    PASAINT testit ; /* number of iterations before testing error */

    PASAFLOAT GPtol ; /* Solution tolerance for the projected gradient */

    PASAINT gpmaxit ; /* max iteration in gradient projection algorithm */

    /* conjugate gradient method restarts after (n*restart_fac) iterations */
    PASAFLOAT restart_fac ;

/* ================ PARAMETERS USED TO COMPUTE REFERENCE VALUE ============== */
    /* The reference function value, updated using the procedure given in
       the function pasa_update_reference, employs the following parameters. */
    int            L ;
    int            M ; /* store maximum of M most recent function values */
    int            P ;
    PASAFLOAT gamma1 ;
    PASAFLOAT gamma2 ;
    PASAFLOAT gamma3 ;

/* ==== PARAMETERS USED TO COMPUTE BB APPROXIMATION bbk*I TO HESSIAN ==== */
    /* The in each iteration of the gradient projection algorithm,
       xk - bbk*gk is projected onto the polyhedron, where bbk
       is computed by a cyclic implementation of the BB formula.
       The BB scheme approximates the inverse Hessian by bbk*I. The nominal
       choice is bbk = ||x_k - x_k-1||^2 / (g_k - g_k-1)'(x_k - x_k-1).
       However, it is required that bbk is bounded away from 0.
       Hence, we impose a fixed lower bound denoted lambda0.  In the first
       iteration, x_k-1 is does not exist. In this case, the user can
       specify the starting bbk in the parameter bbk. If bbk <= 0,
       the starting choice for bbk is max(lambda0,lambda0Factor*||x||/||g||)
       when x != 0, and max (lambda0, normg) when x = 0. When the
       function is not locally convex, bbk grows by at least the factor
       bbexpand. */
    PASAFLOAT        lambda0 ;
    PASAFLOAT  lambda0Factor ;
    PASAFLOAT            bbk ;
    PASAFLOAT       bbexpand ;

    /* In certain cases we do not use the the BB formula to compute bbk.
       These cases mostly correspond to situations where the function
       is not locally convex. However, when the relative change in the
       function value is small enough, it becomes difficult to detect
       a loss of convexity, and in this case we use the BB formula.
       If |fnew - f| <= bbSwitchFactor*|f|, then we use the BB formula. */
    PASAFLOAT bbSwitchFactor ;

    /* In the cyclic implementation of the BB formula, we reuse the BB
       approximation bbk*I to the Hessian for one or more iterations
       before updating its value. The cycle length is the number of times
       that the BB parameter is reused. We try to recompute the BB parameter
       when the cycle length reaches NominalCycle. But if
       sy < 0, we prolong the cycle, but never past MaximumCycle. */
    int MaximumCycle ;
    int NominalCycle ;

/* =================== LINE SEARCH ========================================== */
    /* If approxstep is TRUE, use approximate Armijo or approximate Wolfe
       line search.  If approxstep is FALSE, then use ordinary line search and
       switch to the approximate step when |f - fnew| < ArmijoSwitchFactor*|fR|,
       where fR is an estimate of the function size. In the gradient projection
       algorithm, the function size is estimated by the reference function
       value, while in the conjugate gradient code, an averaging technique
       is employed. */
    int approxstep ;
    PASAFLOAT ArmijoSwitchFactor ;

    /* When performing an approximate Wolfe or an approximate Armijo line
       search, we always require that the new function value <= a perturbation
       of the prior function value. There are two different perturbations.
       If PertRule = 1, then the perturbation is Parm->pert_eps*|f|, while
       if PertRule = 0, then the perturbation is Parm->pert_eps */
    int  PertRule ;
    PASAFLOAT pert_eps ;

    /* maximum number of times that eps is updated */
    int neps ;

    /*  When a nonmonotone Armijo line search is performed, an acceptable
        stepsize alpha satisfies the condition

                fnew <= fR + alpha*deltaf,  deltaf = delta*gk'*dk

        In an approximate Armijo line search, the acceptance criterion is

                gnew'*dk <= 2(fR-f)/alpha + deltag,

        where deltag = (2*delta - 1)*gk'*dk. In an approximate Wolfe line
        search, fR = f and the acceptance criterion is gnew'*dk <= deltag.
        Different delta used in the Armijo line search of grad_proj and the
        Wolfe line search of cg. */
    PASAFLOAT Armijo_delta ;
    PASAFLOAT Wolfe_delta ;

    /* In a Wolfe line search, it is also required that gnew'*dk >=
       Wolfe_sigma*gk'*dk where Wolfe_sigma is between Wolfe_delta and 1. */
    PASAFLOAT Wolfe_sigma ;

    /* maximum number of attempts to find an acceptable step */
    int maxsteps ;

    /* The adjustment in the step alpha is done by different methods in
       different situations. One method is to multiply alpha by the factor
       stepdecay. Another method is to approximate a local minimum of
       the function in the search direction using either a quadratic
       interpolation step or a secant step, with safe guards to ensure
       that the new alpha lies in the interval [safe0, safe1]*alpha */
    PASAFLOAT stepdecay ;
    PASAFLOAT safe0 ;
    PASAFLOAT safe1 ;

    /* When an infinite or nan objective value is encountered, the
       stepsize is reduced in an effort to find a finite objective
       value. infdecay is the initial decay factor that is used when an
       infinite or nan objective value is encountered, ninf_tries is
       the number of attempts we make to find a finite objective value,
       and infdecay_rate is a factor by which infdecay is multiplied
       after each attampt to find a finite objective value. */
    PASAFLOAT infdecay ;
    PASAFLOAT infdecay_rate ;
    int     ninf_tries ;
} PASAparm ;

typedef struct PASAparms_struct
{
    PASAparm   *pasa ; /* parameters for PASA, NULL => use default */
    CGparm       *cg ; /* parameters for CG_DESCENT, NULL => use default */
    PPparm    *pproj ; /* parameters for PPROJ, NULL => use default */
    NAPparm *napheap ; /* parameters for NAPHEAP, NULL => use default */
} PASAparms ;

/* --------------------------------------------------------------------------
    PASAstat is a structure containing statistics which are returned to the
    user when PASA terminates. These are output if PrintLevel >= 1 or
    PrintFinal = TRUE. They can be print by user using pasa_print_stat.
   -------------------------------------------------------------------------- */
typedef struct PASAstat_struct
{
    int         status ; /* status at termination */
    int       maxsteps ; /* max number of attempts to satisfy the grad proj
                            line search condition */
    PASAFLOAT    lobad ; /* invalid lower bound for a variable */
    PASAFLOAT    hibad ; /* invalid upper bound for a variable */
    PASAINT       ibad ; /* index of the bad bound */
    PASAFLOAT grad_tol ; /* KKT error tolerance */
    int     ninf_tries ; /* number of tries to find finite objective value */
    PASAINT    gpmaxit ; /* max iteration in gradient projection algorithm */
    PASAFLOAT        f ; /* function value */
    PASAFLOAT      err ; /* || P (x - g) - x || */
    PASAINT       mcnf ; /* function evaluations in main code */
    PASAINT       mcng ; /* gradient evaluations in main code */
    PASAINT       gpit ; /* number of iterations in grad_proj */
    PASAINT       gpnf ; /* function evaluations in grad_proj */
    PASAINT       gpng ; /* gradient evaluations in grad_proj */
    PASAINT      agpit ; /* number of iterations in active set grad_proj */
    PASAINT      agpnf ; /* function evaluations in active set grad_proj */
    PASAINT      agpng ; /* gradient evaluations in active set grad_proj */
    PASAINT   nproject ; /* number of projections performed */
} PASAstat ;

typedef struct PASAstats_struct
{
    PASAstat   *pasa ; /* statistics for PASA */
    CGstat       *cg ; /* statistics for CG_DESCENT */
    PPstat    *pproj ; /* statistics for PPROJ */
    NAPstat *napheap ; /* statistics for NAPHEAP */

    /* used internally to record the routines used */
    int     use_pasa ; /* T => problem not solved purely by cg/pproj/napheap */
    int       use_cg ; /* T => cg was used */
    int    use_pproj ; /* T => pproj was used */
    int  use_napheap ; /* T => napheap was used */
} PASAstats ;

/* --------------------------------------------------------------------------
    PASAcopy is a structure containing copies of the problem data used in pproj.
    In the active set algorithm, we constantly compress the data as variables
    and constraints reach their bounds. When we free all the variables and
    constraints, we need to restore the original problem data. Note that the
    copies of lo, hi, bl, and bu are stored in the com structure since these
    copies are also relevant to napheap.
   -------------------------------------------------------------------------- */
typedef struct PASAcopy_struct
{
    PPINT         ncol ; /* number of cols in A */
    PPINT          *Ap ; /* size ncol+1, the column pointers */
    PPINT          *Ai ; /* size Ap [ncol], the row indices */
    PPFLOAT        *Ax ; /* size Ap [ncol], the numerical values in A */
    PPFLOAT         *b ; /* size nrow, right-hand-side */
    PPFLOAT        *bl ; /* size ni+1, bl_i with bl_i < bu_i */
    PPFLOAT        *bu ; /* size ni+1, bu_i with bl_i < bu_i */
    PPINT    *ineq_row ; /* size ni+2 (ineq_row [1], ... ineq_row [ni] are
                            the row numbers where bl_i < bu_i, while
                            ineq_row [ni+1] = nrow (a stopper) */
    PPINT   *col_start ; /* starting column in each block */
    int    *sol_to_blk ; /* size ni+2, for each singleton, 1st block in matrix*/

    /* AT is the transpose of the A matrix, compact format */
    PPINT         *ATp ; /* size nrow + 1, the column pointers */
    PPINT         *ATi ; /* size Ap [ncol], the column indices */
    PPFLOAT       *ATx ; /* size Ap [ncol], the numerical values in A */
} PASAcopy ;

/* --------------------------------------------------------------------------
    PASAhess is a structure that is passed to the user when pasa wishes
    to evaluate the Hessian of the objective.
   -------------------------------------------------------------------------- */
typedef struct PASAhess_struct
{
    PPINT         ncol ; /* number of cols in the Hessian */
    PPFLOAT         *x ; /* the point where the Hessian is evaluated */
    PPINT          *Hp ; /* size ncol+1, the column pointers */
    PPINT          *Hi ; /* size Hp [ncol], the row indices */
    PPFLOAT        *Hx ; /* size Hp [ncol], numerical values in the Hessian */
} PASAhess ;

/* --------------------------------------------------------------------------
    PASAdata is a structure containing all input data provided to for pasa.
    It is meant to be used in conjunction with the function pasa_setup
    which initializes the inputs to default values before calling pasa.
    A NULL value for the input argument means that it does not exist.
    pasa is designed to handle 7 problem classes.

        UNC     - unconstrained optimization:
                      min f(x) s.t. x in R^n
        BNC     - purely bound constrained optimization:
                      min f(x) s.t. lo <= x <= hi
        LP      - linear program:
                      min c'*x s.t. lo <= x <= hi, bl <= A*x <= bu
        QP      - quadratic program:
                      min 0.5*x'*Q*x + c'*x s.t. lo <= x <= hi, bl <= A*x <= bu
        NL      - nonlinear program:
                      min f(x) s.t. lo <= x <= hi, bl <= A*x <= bu
        NAPSACK - separable quadratic with napsack constraints:
                      min 0.5*x*'D*x + c'*x s.t. lo <= x <= hi, bl <= a'*x <= bu
        PROJ    - polyhedral constrained projection:
                      min 0.5*||x - y||^2 s.t. lo <= x <= hi, bl <= A*x <= bu
   -------------------------------------------------------------------------- */
typedef struct PASAdata_struct
{
    /* -------- pasa input data -------- */
    PASAFLOAT    *lambda ; /* If not NULL and pasaparm->use_lambda = T,
                              then lambda points to an array of size nrow
                              that contains a guess for the multiplier.
                              If lambda is NULL, then PASA allocates memory
                              for lambda and returns the multiplier in lambda.
                              Any allocated memory is freed by pasa_terminate.*/
    PASAFLOAT         *x ; /* size ncol, points to a starting guess for
                              routines that require one. Currently NAPHEAP,
                              PPROJ, and the LP solver do not require a
                              starting guess.  If not required and NULL,
                              then PASA allocates memory for x. The problem
                              solution is returned in x.  Any allocated memory
                              is freed by pasa_terminate. */
    PASAparms     *Parms ; /* 4 structures pasa, cg, pproj, and
                              napheap with parameters */
    PASAstats     *Stats ; /* 4 structures are returned with statistics
                              for each of the codes used. */
    PASAINT         nrow ; /* number of rows in A */
    PASAINT         ncol ; /* number of components in x and number of cols in
                              A if it exists */
    /* If A exists, then its nonzero elements are stored in sparse matrix
       format corresponding to two integer arrays and one real array. When
       A does not exist, these arrays should be NULL */
    PASAINT          *Ap ; /* size ncol+1, column pointers */
    PASAINT          *Ai ; /* size Ap [ncol], row indices for A, increasing
                             order in each column */
    PASAFLOAT        *Ax ; /* size Ap [ncol], numerical entries of A */
    PASAFLOAT        *bl ; /* size nrow, lower bounds for inequalities
                              NULL => use -infinity */
    PASAFLOAT        *bu ; /* size nrow, upper bounds for inequalities
                              NULL => use +infinity */
    PASAFLOAT        *lo ; /* size ncol, lower bounds for x
                              NULL => use -infinity */
    PASAFLOAT        *hi ; /* size ncol, upper bounds for x
                              NULL => use +infinity */
    PASAFLOAT         *y ; /* size ncol, project y onto polyhedron in PPROJ */

    PASAFLOAT         *c ; /* size ncol, linear term if objective is quadratic
                              or linear */

    PASAFLOAT         *a ; /* size ncol, the constraint is *Bl <= a'x <= *Bu */

    PASAFLOAT         *d ; /* size ncol, diagonal in NAPHEAP */

    PASAFLOAT     *xWork ; /* NULL => pasa should allocate real work space.
                              Otherwise, see allocation section of pasa to
                              determine memory requirements. */

    PASAINT       *iWork ; /* NULL  => pasa should allocate integer work space.
                              Otherwise, see allocation section of pasa to
                              determine memory requirements. */

    CGdata       *cgdata ; /* input data for CG_DESCENT */

    PPdata       *ppdata ; /* input data structure for PPROJ */

    NAPdata     *napdata ; /* input data for NAPHEAP */

    /* For a quadratic objective, hprod evaluates Hessian times vector,
       NULL if objective not quadratic. When solving a constrained problem,
       or when solving an unconstrained problem, there are a different number
       of arguments since some components of the vector in the product
       are 0 when bounds are active. The unconstrained version is denoted
       cg_hprod. */
    void   (*hprod) (PASAFLOAT *, PASAFLOAT *, PASAINT *, PASAINT, PASAINT) ;
    /* for a quadratic objective, hprod evaluates Hessian times vector,
       NULL if objective not quadratic */
    void   (*cg_hprod) (PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* for a general nonlinear function, value (f, x, n) is function value,
       NULL if objective is quadratic */
    void   (*value) (PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* for a general nonlinear function, grad (g, x, n) is function gradient,
       NULL if objective is quadratic */
    void    (*grad) (PASAFLOAT *, PASAFLOAT *, PASAINT) ; /* grad  (g, x, n) */
    /* for a general nonlinear function, valgrad (f, g, x, n) gives both
       function value f and gradient g at x (size n), argument can be NULL  */
    void (*valgrad) (PASAFLOAT *, PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* Hessian evaluation routine for pasa, can be NULL, not currently used */
    void    (*hess) (PASAhess *) ;
    /* Hessian evaluation routine for cg, can be NULL, not currently used */
    void    (*cghess) (CGhess *) ;

    /* the following are used internally when the code allocates memory */
    PASAFLOAT *x_created ; /* pointer to memory created for x */
    PASAFLOAT *lambda_created ;/* pointer to memory created for lambda */
} PASAdata ;
/* --------------------------------------------------------------------------
    During the operation of PASA, parameter values are changed.
    The preserve structure stores a copy of the user's original parameter
    values before changes where made by PASA.
   -------------------------------------------------------------------------- */
typedef struct PASApreserve_struct
{
    /* napheap parameters */
    int n_PrintStatus ;
    int n_return_data ;
    int n_use_prior_data ;
    int n_loExists ;
    int n_hiExists ;
    int n_d_is_one ;

    /* pproj parameters */
    PASAFLOAT p_grad_tol ;
    int p_PrintStatus ;
    int p_return_data ;
    int p_use_prior_data ;
    int p_loExists ;
    int p_hiExists ;
    int p_getfactor ;
    int p_permute ;
    int p_start_guess ;
    int p_use_startup ;
    int p_LP ;

    /* cg parameters */
    int c_PrintStatus ;
    int c_PrintStat ;
    int c_PrintParm ;
    PASAFLOAT c_fadjust ;

} PASApreserve ;

/* --------------------------------------------------------------------------
    PASAcom is a structure containing the working data used throughout the code
   -------------------------------------------------------------------------- */
typedef struct PASAcom_struct /* common variables */
{
    int                  LP ; /* T => linear program */
    int                  QP ; /* T => quadratic program */
    PASAdata      *pasadata ; /* pasa's input data structure */
    PPdata     *ppdataDEBUG ; /* a PPdata structure for debugging pproj */
    PPcom            *ppcom ; /* PPcom structure of solution computed by pproj*/
    PASApreserve  userparms ; /* user parameters before changes made by pasa */
    int      save_use_ppcom ; /* initial value of pprojparm's use_ppcom */
    int      save_getfactor ; /* initial value of pprojparm's getfactor */
    int        save_permute ; /* initial value of pprojparm's permute */
    PASAcopy          *Copy ; /* copy of problem data in pproj format */
    int             Aexists ; /* T => constraints bl <= Ax <= bu are present */
    int            loExists ; /* T => for some j, lo [j] >-infinity */
    int            hiExists ; /* T => for some j, hi [j]  < infinity */
    int              Bounds ; /* T => lo or hi exists */
    int               fixed ; /* T => there are fixed variables */
    int         use_penalty ; /* T => include penalty term in CG */
    PASAFLOAT       penalty ; /* penalty parameter when use_penalty = TRUE */
    int           use_pproj ; /* pproj is used */
    int         use_napheap ; /* napheap is used */
    int              use_cg ; /* cg is used */
    int  initial_projection ; /* T => pproj has not yet been called */
    int  order_with_colperm ; /* T => convert to user ordering with colperm */
    int    order_with_ifree ; /* T => convert to user ordering with ifree */
    PASAINT          *ifree ; /* free columns in current x relative to user
                                 ordering of variables */
    PASAINT        *colperm ; /* colperm [j] = user index of internal index j
                                 this is the ordering generated by pproj, if
                                 there are fixed variables, colperm also takes
                                 into account the removed fixed variables. */
    PASAINT          *order ; /* this is the ordering in the active set methods
                                 when bound constraints present, order = ifree,
                                 when no bound constraints but linear
                                 constraints or fixed variables, order =
                                 colperm */
    PASAparm      *pasaparm ; /* parameters for pasa */
    PPparm       *pprojparm ; /* parameters for pproj */
    CGparm          *cgparm ; /* parameters for cg_descent */
    NAPparm        *napparm ; /* parameters for napheap */
    PASAstat      *pasastat ; /* statistics for pasa */
    PPstat       *pprojstat ; /* statistics for pproj */
    CGstat          *cgstat ; /* statistics for cg_descent */
    NAPstat        *napstat ; /* statistics for napheap */
    PASAstats        *Stats ; /* structure of all statistics used by pasa */
    PASAhess          *Hess ; /* Hessian structure */
    /* evaluate Hessian times vector for a quadratic objective */
    void   (*hprod) (PASAFLOAT *, PASAFLOAT *, PASAINT *, PASAINT, PASAINT) ;
    /* evaluate objective function */
    void   (*value) (PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* evaluate gradient */
    void    (*grad) (PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* evaluate function and gradient, NULL => use value & grad routines */
    void (*valgrad) (PASAFLOAT *, PASAFLOAT *, PASAFLOAT *, PASAINT) ;
    /* evalute the Hessian */
    void    (*hess) (PASAhess *) ;
    PASAFLOAT         *work ; /* not NULL => start of allocated work array */
    PASAINT          *iwork ; /* not NULL => start of allocated iwork array */
    PASAINT        *invperm ; /* inverse of pproj's colperm */
    PASAFLOAT        *userx ; /* ncol space used to store x with user's order */
    PASAFLOAT        *userg ; /* ncol space used to store user's gradient */
    PASAFLOAT         alpha ; /* stepsize */
    PASAFLOAT       maxstep ; /* max feasible stepsize in CG */
    int           boundtype ; /* +1 = bounds on x, -1 = linear constraints */
    PASAINT      boundindex ; /* indicates index of bound that became active */
    PASAFLOAT            df ; /* g'd in CG */
    PASAFLOAT            dp ; /* penalty term gradient * d in CG */
    PASAFLOAT           Ad2 ; /* p||Ad||^2 in CG, pd+alpha*Ad2 = deriv @ alpha*/
    PASAFLOAT            fp ; /* value of CG penalty term */
    PASAFLOAT        f_orig ; /* original function value in CG before penalty */
    PASAFLOAT          *Axk ; /* used in CG to store A*xk for inequalities */
    PASAFLOAT          *Adk ; /* used in CG to store A*dk for inequalities */
    PASAFLOAT       *cgwork ; /* start of work array for CG */
    PASAFLOAT           gtd ; /* d'g for current iterate in pasa */
    PASAFLOAT             e ; /* local error estimate in face of polyhedron */
    PASAFLOAT             E ; /* global error estimate ||proj(x-g) - x|| */
    PASAFLOAT          estE ; /* estimate of global error from gradproj_step */
    int            location ; /* 0 = grad_proj, 1 = activeGP, 2 = cg */
    PASAINT              nr ; /* no. of bound inequalities (rows)
                                 --see bound_rows */
    PASAINT              nc ; /* no. of bound variables (columns)
                                 --see bound_cols */
    PASAINT         nc_temp ; /* nc after doing gradproj_step, before compress*/
    PASAINT     *bound_rows ; /* row numbers of bound inequalities */
    PASAINT     *bound_cols ; /* col numbers of bound variables */
    PASAINT    *row_to_ineq ; /* maps row indices to inequality number */
    PASAFLOAT       fmaxmin ; /* fmaxmin(k) = max { fi : j <= i <= k, 
                                        fj = f_min(k), j  small as possible} */
    PASAFLOAT         f_max ; /* f_max(k) = max{ fj : max(k-M, 0) < j <= k } */
    PASAFLOAT         f_min ; /* f_min(k) = min { fj : j <= k} */
    PASAFLOAT         *fmem ; /* array with previous Parm->M function vals */
    PASAFLOAT            fr ; /* reference function value */
    int                memp ; /* index of value to be deleted in fmem */
    PASAFLOAT       *lambda ; /* current KKT multipliers (size nrow) */
    PASAFLOAT   *lambda_pen ; /* lambda used in CG penalty function */
    PASAFLOAT           bbk ; /* current value of the BB parameter */
    PASAFLOAT     cg_bb_est ; /* an estimate of the BB parameter from cg code */
    int            unitstep ; /* T => unit step taken in grad_proj */
    int           factor_ok ; /* T => current factor matches current iterate */
    PASAFLOAT            *x ; /* current iterate relative to pproj's perm */
    PASAFLOAT            *g ; /* gradient relative to pproj's perm */
    PASAFLOAT         *gpen ; /* gradient of penalty term in cg */
    PASAFLOAT            *d ; /* search direction relative to pproj's perm */
    PASAFLOAT         *xnew ; /* new current iterate in pproj's colperm */
    PASAFLOAT         *gnew ; /* new gradient in pproj's colperm */
    PASAFLOAT          fnew ; /* new function value */
    PASAFLOAT             f ; /* current function value */
    PASAFLOAT           *Qd ; /* Hessian times d for a quadratic program */
    PASAFLOAT         *gtot ; /* total gradient for a quadratic program in
                                 user ordering of variables, fixed variables
                                 removed */
    PASAFLOAT            *b ; /* b of pproj adjusted for active inequalities */
    PASAFLOAT           *bl ; /* bl of pproj compressed */
    PASAFLOAT           *bu ; /* bu of pproj compressed */
    PASAFLOAT           *lo ; /* lower bounds: x >= lo, compressed */
    PASAFLOAT           *hi ; /* upper bounds: x <= hi, compressed */
    PASAFLOAT       *copylo ; /* size ncol, copy of lo, lower bounds for x */
    PASAFLOAT       *copyhi ; /* size ncol, copy of hi, upper bounds for x */
    PASAFLOAT            *c ; /* linear term c after removing bound variables */
    PASAFLOAT        *userc ; /* userc before removing bound variables */

    /* variables associated with an LP */
    PASAINT           nsing ; /* total # of column singletons including ni */
    PASAFLOAT     *ColScale ; /* scaling applied to a columns of an LP */
    PASAFLOAT     *RowScale ; /* scaling applied to a rows of an LP */
    PASAFLOAT       *offset ; /* offset: x_j -> x_j - t in LP to shift bounds */
    PASAFLOAT       scale_x ; /* solution of LP b is scaled by scale_x */
    PASAFLOAT       scale_l ; /* solution of LP c is scaled by scale_l */
    PASAINT             *si ; /* row number in A for singleton */
    PASAINT             *sj ; /* col number in A for singleton */
    PASAINT       *row_sing ; /* start of singc indices for row */
    PASAINT       *singperm ; /* permutation from singc to sc */
    PASAFLOAT        *singc ; /* sorted sc */
    PASAFLOAT       *singlo ; /* sorted lower bounds */
    PASAFLOAT       *singhi ; /* sorted upper bounds */
    PASAFLOAT           *sx ; /* numerical entry in A for singleton */
    PASAFLOAT           *sc ; /* numerical entry in cost vector for singleton */
    PASAFLOAT          *slo ; /* lower bounds */
    PASAFLOAT          *shi ; /* upper bounds */

#ifndef NDEBUG
    PASAFLOAT           *BL ;
    PASAFLOAT           *BU ;
    PASAFLOAT           *AX ;
    PASAFLOAT           *LO ;
    PASAFLOAT           *HI ;
    PASAINT             *AI ;
    PASAINT             *AP ;
#endif
    PASAINT              nf ; /* number of free variables */
    PASAINT            ucol ; /* number of columns in A before compression */
    PASAINT            ncol ; /* number of columns in A after compression */
    PASAINT            nrow ; /* number of rows in A */
    PASAINT              ni ; /* number of i such that bl_i < bu_i */
    PASAINT             *Ap ; /* compressed column pointers for A */
    PASAINT             *Ai ; /* compressed row indices for A */
    PASAFLOAT           *Ax ; /* compressed nonzero numerical entries in A */
    int               first ; /* TRUE => first gradient projection iteration */
    int         nunit_steps ; /* number of consecutive unit steps */
    int        its_in_cycle ; /* num iters current bb step has been reused */
    int its_since_f_min_update ; /* iters since f_min updated */
    PASAFLOAT      grad_tol ; /* convergence tolerance */    
    PASAFLOAT         GPtol ; /* error tolerance for projected gradient */
    PASAFLOAT   switchfactor; /* switch to grad_proj when local error
                                 < switchfactor*global error */
    int          approxstep ; /* T => use approximate Armijo or Wolfe search */
    PASAFLOAT       testtol ; /* tolerance for testing local error */

    PASAFLOAT     *napxwork ; /* not NULL => start of napheap xwork array */
    PASAINT       *napiwork ; /* not NULL => start of napheap iwork array */
                              /* napheap linear constraint: bl <= a'x <= bu */
    PASAFLOAT        *nap_a ; /* dense linear constraint vector in napheap */
    PASAFLOAT    *nap_acopy ; /* copy of a after removing fixed variables */
    PASAFLOAT    *nap_auser ; /* user's a before removing fixed variables */
    PASAFLOAT        nap_a2 ; /* ||a||^2 (updated from prior a2save value) */
    PASAFLOAT    nap_a2save ; /* save ||a||^2 whenever it is recomputed */
    PASAFLOAT    nap_a2full ; /* ||a||^2 for the full (uncompressed) a */
    PASAFLOAT        nap_bl ; /* lower bound for linear constraint */
    PASAFLOAT        nap_bu ; /* upper bound for linear constraint */
    PASAFLOAT    nap_blcopy ; /* copy of bl */
    PASAFLOAT    nap_bucopy ; /* copy of bu */
    PASAFLOAT    nap_lambda ; /* the multiplier returned by napheap, we only
                                 store it in com->lambda when the line search
                                 moves to the projection returned by napheap */
    int      nap_constraint ; /* -1 = active inequality at lower bound,
                                  0 = inactive inequality,
                                  1 = active inequality at upper bound,
                                  2 = equality constraint */
    int   pproj_start_guess ; /* initial value of start_guess parm in pproj */
                              /* if LP is true, start_guess changed to 3 */
                              /* initial value restored after solving LP */
    /* if these temporary variables have to be created, then they will
       be freed in pasa_wrapup */
    PASAFLOAT  *temp_userBl ; /* NULL unless it has to be created */
    PASAFLOAT  *temp_userBu ; /* NULL unless it has to be created */
    PASAINT     *temp_ifree ; /* NULL unless it has to be created */
} PASAcom ;


/* ==========================================================================
   ================ pasa prototypes =========================================
   ========================================================================== */

int pasa
(
    PASAdata    *pasadata /* Struct containing pasa input data */
) ;

PASAdata *pasa_setup (void) ;

void pasa_terminate
(
    PASAdata **Data
) ;

int pasa_autodetect
(
    PASAdata *pasadata
) ;

void * pasa_malloc
(
    int *status,
    PASAINT   n,
    int    size
) ;

void pasa_free
(
    void * p
) ;

void pasa_error
(
    int status,
    const char *file,
    int line,
    const char *message
) ;

void pasa_default
(
    PASAparm    *Parm   /* pointer to parameter structure */
) ;

void pasa_print_parm
(
    PASAdata    *Data   /* PASAparm structure to be printed */
) ;

void pasa_print_TF
(
    int TF /* TRUE or FALSE */
) ;


void pasa_print_status
(
    PASAdata *Data  /* pasa data structure */
) ;

void pasa_print_stat
(
    PASAdata *Data  /* pasa data structure */
) ;

void pasa_print_stats
(
    PASAdata *Data  /* pasa data structure */
) ;

void pasa_print_parms
(
    PASAdata *Data  /* pasa data structure */
) ;

void pasa_wrapup
(
    int     status, /* termination status */
    int fastreturn, /* T => return after printing status and freeing temp mem */
    PASAcom   *Com  /* common data for PASA */
) ;

int pasa_gradproj_step
(
    PASAFLOAT stepsize,
    PASAcom       *Com  /* common data for PASA */
) ;

void pasa_null_project
(
    PASAFLOAT   *gproj, /* the projected gradient */
    PASAFLOAT       *g, /* the gradient to be projected */
    PASAFLOAT    *gpen, /* gradient of penalty term if it exists */
    int     LocalError, /* T => compute local error */
    PASAcom       *Com  /* common data for PASA */
) ;

int pasa_project
(
    PASAFLOAT         *x, /* projection of y onto the polyhedron */
    PASAFLOAT         *y, /* point to project onto the polyhedron */
    PASAcom         *Com  /* common data for PASA */
) ;

int pasa_project2
(
    PASAFLOAT       *x, /* projection of y onto the polyhedron */
    PASAFLOAT       *y, /* point to project onto the polyhedron */
    PASAcom       *Com  /* common data for PASA */
) ;

int pasa_grad_proj
(
    PASAcom  *Com  /* common data for PASA */
) ;

int pasa_activeGP
(
    PASAcom *Com  /* common data for PASA */
) ;

int pasa_gradprojLP
(
    PASAcom *Com  /* common data for PASA */
) ;

void pasa_errLP
(
    PASAFLOAT epsilon, /* some data is scaled by epsilon in gradprojLP */
    PASAcom      *Com  /* common data for PASA */
) ;

int pasa_bound_compress
(
    PASAcom    *Com  /* common variables */
) ;

int pasa_compress_prob
(
    int local_error, /* TRUE => compute local error */
    PASAcom    *Com  /* common variables */
) ;

int pasaAG_checktol
(
    PASAcom    *Com  /* pasa com structure */
) ;

PASAINT pasa_update_bb /* return lambda_k */
(
    PASAcom    *Com  /* common data for PASA */
) ;

PASAFLOAT pasa_update_reference
(
    PASAcom   *C  /* common data for PASA */
) ;

PASAINT pasa_compress_matrix
(
    PASAINT    *Ap, /* matrix column pointers */
    PASAINT    *Ai, /* matrix row indices */
    PASAFLOAT  *Ax, /* matrix numerical values */
    PASAINT   ncol, /* number of cols in A */
    PASAINT  *drop  /* drop columns for which drop [j] != 0 */
) ;

void pasa_step
(
    PASAFLOAT       *xnew, /* updated x vector */
    PASAFLOAT const    *x, /* current x */
    PASAFLOAT const    *d, /* search direction */
    PASAFLOAT const alpha, /* stepsize */
    PASAINT   const     n  /* dimension */
) ;

void pasa_hadamard
(
    PASAFLOAT       *x, /* x = y.*z */
    PASAFLOAT const *y,
    PASAFLOAT const *z,
    PASAINT   const  n  /* length of vectors */
) ;

void pasa_scale
(
    PASAFLOAT      *x,  /* array to be scaled */
    PASAFLOAT      *y,  /* array used for the scaling */
    PASAFLOAT const s,  /* scale */
    PASAINT   const n   /* length of x */
) ;

PASAFLOAT pasa_dot
(
    PASAFLOAT const *x, /* first vector */
    PASAFLOAT const *y, /* second vector */
    PASAINT   const  n  /* length of vectors */
) ;

void pasa_copyx
(
    PASAFLOAT    *x, /* copy of y */
    PASAFLOAT    *y, /* given vector */
    PASAINT const n  /* length of vectors */
) ;

void pasa_copyi
(
    PASAINT      *x, /* copy of y */
    PASAINT      *y, /* given vector */
    PASAINT const n  /* length of vectors */
) ;

void pasa_copyi_int
(
    int          *x, /* copy of y */
    int          *y, /* given vector */
    PASAINT const n  /* length of vectors */
) ;

void pasa_initi
(
    PASAINT      *x,  /* array to be initialized */
    PASAINT const s,  /* scalar */
    PASAINT const n   /* length of x */
) ;

void pasa_initx
(
    PASAFLOAT      *x,  /* array to be initialized */
    PASAFLOAT const s,  /* scalar */
    PASAINT   const n   /* length of x */
) ;

PASAFLOAT pasa_sup_norm
(
    PASAFLOAT const *x, /* vector */
    PASAINT   const  n  /* length of vector */
) ;

PASAINT pasa_isup
(
    PASAINT const *x, /* vector */
    PASAINT const  n  /* length of vector */
) ;

void pasa_transpose
(
    PASAINT   *Bp,   /* size nrow+1, column pointers (output) */
    PASAINT   *Bi,   /* size Ap [ncol], row indices of B (output) */
    PASAFLOAT *Bx,   /* size Ap [ncol], numerical entries of B (output) */
    PASAINT   *Ap,   /* size ncol+1, column pointers */
    PASAINT   *Ai,   /* size Ap [ncol], row indices for A */
    PASAFLOAT *Ax,   /* size Ap [ncol], numerical entries of A */
    PASAINT  nrow,   /* number of rows in A */
    PASAINT  ncol,   /* number of cols in A */
    PASAINT    *W    /* work array of size nrow */
) ;

void pasa_convert_to_user
(
    PASAFLOAT       *x, /* x in user order */
    PASAFLOAT const *y, /* y in pproj order */
    PASAINT     *ifree, /* ifree [j] = element of x associated with y [j] */
    PASAINT   const  n  /* dimension */
) ;

void pasa_convert_to_pproj
(
    PASAFLOAT   *x, /* x in pproj order */
    PASAFLOAT   *y, /* y in user order */
    PASAINT *ifree, /* ifree [j] = element of y associated with x [j] */
    PASAINT      n  /* dimension */
) ;

int pasa_evaluate
(
    PASAFLOAT alpha_good, /* a value of alpha for which function is finite */
    PASAFLOAT     *Alpha, /* stepsize along the search direction */
    PASAcom         *Com, /* PASAcom structure */
    char           *what  /* f = function, g = gradient, fg = function + gradient */
) ;

void pasa_check_feas
(   
    PASAcom    *Com /* PASAcom structure */
) ;

double pasa_time (void) ;

void check_zero
(
    PASAFLOAT *x,
    PASAINT    n,
    int        l
) ;

int pasa_cg_descent
(
    CGdata    *cgdata, /* CG data structure */
    PASAcom  *pasacom  /* common variables from pasa */
) ;

CGdata * pasa_cg_setup (void) ;

void pasa_cg_terminate
(
    CGdata **DataHandle
) ;

int pasa_cg_wrapup
(
    int       status,
    PASAcom *pasacom,
    CGcom     *cgcom
) ;

int pasa_cg_evaluate
(
    CGFLOAT alpha_good, /* a value of alpha for which function is finite */
    CGFLOAT     *Alpha, /* stepsize along the search direction */
    char         *what, /* fg = eval func & grad, g = grad only,f = func only */
    PASAcom   *pasacom,
    CGcom         *Com
) ;

int pasa_cg_Wolfe
(
    CGFLOAT  alpha, /* stepsize */
    CGFLOAT      f, /* function value associated with stepsize alpha */
    CGFLOAT   dphi, /* derivative value associated with stepsize alpha */
    CGcom   *cgcom
) ;

int pasa_cg_line
(
    int       repeat, /* TRUE => Wolfe search failed, retry using approxstep */
    PASAcom *pasacom,
    CGcom     *cgcom
) ;

int pasa_cg_contract
(
    CGFLOAT       *A, /* left side of bracketing interval */
    CGFLOAT      *fA, /* function value at a */
    CGFLOAT      *dA, /* derivative at a */
    CGFLOAT       *B, /* right side of bracketing interval */
    CGFLOAT      *fB, /* function value at b */
    CGFLOAT      *dB, /* derivative at b */
    PASAcom *pasacom,
    CGcom     *cgcom
) ;

CGFLOAT pasa_cg_cubic
(
    CGFLOAT  a,
    CGFLOAT fa, /* function value at a */
    CGFLOAT da, /* derivative at a */
    CGFLOAT  b,
    CGFLOAT fb, /* function value at b */
    CGFLOAT db  /* derivative at b */
) ;

CGFLOAT pasa_cg_maxstep
(
    PASAcom *pasacom,
    CGcom     *cgcom
) ;

int pasa_cg_checktol /* return:
                               PASA_ERROR_TOLERANCE_SATISFIED
                               PASA_GRAD_PROJ
                               CG_RESTART
                               CG_CONTINUE */
(
    CGFLOAT       *x, /* current iterate */
    PASAcom *pasacom,
    CGcom     *cgcom
) ;

#endif
