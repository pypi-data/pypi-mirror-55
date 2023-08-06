#ifndef _CG_DESCENT_H_
#define _CG_DESCENT_H_

#include "SuiteOPTconfig.h"

#define CGFLOAT SuiteOPTfloat
#define CGINT SuiteOPTint

#define FALSE SuiteOPTfalse
#define TRUE SuiteOPTtrue

#define CGINF SuiteOPTinf
#define CGINFINT SuiteOPTinfint

#define CGZERO ((CGFLOAT) 0)
#define CGONE  ((CGFLOAT) 1)

#define CGMAX(a,b) ( ((a) > (b)) ? (a) : (b) )
#define CGMIN(a,b) ( ((a) < (b)) ? (a) : (b) )

#ifdef PASA
#define PASA_CG_COM pasacom,cgcom
#define XXCG(name) pasa_cg_ ## name
#else
#define PASA_CG_COM cgcom
#define XXCG(name) cg_ ## name
#endif

#ifdef MATLAB_MEX_FILE
#define cg_malloc mxMalloc
#define cg_free mxFree
#else
#define cg_malloc malloc
#define cg_free free
#endif

/* ==========================================================================
 * =========== status returned by CG_DESCENT ================================
 * ========================================================================== */

#define CG_ERROR_TOLERANCE_SATISFIED                             (0)
#define CG_ITERATIONS_EXCEED_MAXITS                              (200)
#define CG_SLOPE_ALWAYS_NEGATIVE                                 (201)
#define CG_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS                     (202)
#define CG_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION                (203)
#define CG_WOLFE_CONDITIONS_NOT_SATISFIED                        (204)
#define CG_DEBUGGER_IS_ON_AND_FUNCTION_VALUE_INCREASES           (205)
#define CG_NO_COST_OR_GRADIENT_IMPROVEMENT                       (206)
#define CG_OUT_OF_MEMORY                                         (207)
#define CG_QUADRATIC_OBJECTIVE_NO_LOWER_BOUND                    (208)
#define CG_STARTING_FUNCTION_VALUE_INFINITE_OR_NAN               (209)
#define CG_EXCESSIVE_UPDATING_OF_PERT_EPS                        (210)
#define CG_FUNCTION_NAN_OR_INF                                   (211)
#define CG_QP_LINEAR_TERM_GIVEN_BUT_HPROD_MISSING                (212)
#define CG_HPROD_GIVEN_BUT_QP_LINEAR_TERM_MISSING                (213)
#define CG_N_IS_EMPTY                                            (214)

#define CG_START_MESSAGES                                        (200)
#define CG_END_MESSAGES                                          (299)

/* not seen by the caller, used for flow constrol */
#define CG_OK                                                    (-1)
#define CG_WOLFE_OK                                              (-2)
#define CG_WOLFE_NOT_OK                                          (-3)
#define CG_NEW_PERT                                              (-4)
#define CG_INTERVAL_OK                                           (-5)
#define CG_ERROR_TOLERANCE_DOES_NOT_HOLD                         (-6)
#define CG_RESTART                                               (-7)
#define CG_CONTINUE                                              (-8)
#define CG_HITS_BOUNDARY                                         (-9)

/* -------------------------------------------------------------------------- */
/* cg_descent version information */
/* -------------------------------------------------------------------------- */
#define CG_DATE "October 21, 2019"
#define CG_MAIN_VERSION 7
#define CG_SUB_VERSION 0
#define CG_SUBSUB_VERSION 0

/* If the BLAS are not installed, then the following definitions
   can be ignored. If the BLAS are available, then to use them,
   comment out the the next statement (#define NOBLAS) and make
   any needed adjustments to BLAS_UNDERSCORE and the START parameters.
   cg_descent already does loop unrolling, so there is likely no
   benefit from using unrolled BLAS. There could be a benefit from
   using threaded BLAS if the problems is really big. However,
   performing low dimensional operations with threaded BLAS can be
   less efficient than the cg_descent unrolled loops. Hence,
   START parameters should be specified to determine when to start
   using the BLAS. The floating point precision of the BLAS should
   coincide with CGFLOAT.  */


/*
#define NOBLAS
*/


#ifndef NOBLAS

/* if BLAS are used, comment out the next statement if no
      underscore in the subroutine names are needed */
#define BLAS_UNDERSCORE

/* only use ddot when the vector size >= DDOT_START */
#define DDOT_START 100

/* only use dcopy when the vector size >= DCOPY_START */
#define DCOPY_START 100

/* only use DAXPY when the vector size >= DAXPY_START */
#define DAXPY_START 100

/* only use dscal when the vector size >= DSCAL_START */
#define DSCAL_START 100

/* only use idamax when the vector size >= IDAMAX_START */
#define IDAMAX_START 100

/* only use matrix BLAS for transpose multiplication when number of
   elements in matrix >= MATVEC_START */
#define MATVEC_START 100

#ifdef BLAS_UNDERSCORE

#define CG_DGEMV dgemv_
#define CG_DTRSV dtrsv_
#define CG_DAXPY daxpy_
#define CG_DDOT ddot_
#define CG_DSCAL dscal_
#define CG_DCOPY dcopy_
#define CG_IDAMAX idamax_

#else

#define CG_DGEMV dgemv
#define CG_DTRSV dtrsv
#define CG_DAXPY daxpy
#define CG_DDOT ddot
#define CG_DSCAL dscal
#define CG_DCOPY dcopy
#define CG_IDAMAX idamax

#endif
#endif

/* ==========================================================================
 * =============== cg structures ============================================
 * ========================================================================== */

/* ============================================================================
   CGparm is a structure containing parameters used in cg_descent.
   CGdefault gives default values for these parameters.
============================================================================ */
typedef struct CGparm_struct
{
    /* T => print status of run
       F => do not print status of run */
    int PrintStatus ;

    /* T => print pasa statistics
       F => do not print statistics */
    int PrintStat ;

    /* T => print parameter values 
       F => do not print parameter values */
    int PrintParm ;

    /* Level 0  = no printing, ... , Level 2 = maximum printing */
    int PrintLevel ;

    /* an adjustment added to a quadratic cost objective when it is evaluated */
    CGFLOAT fadjust ;

    /* replace the Hessian Q of a quadratic by Q + QPshift */
    CGFLOAT QPshift ;

    /* nominal stopping criterion for cg_descent is ||grad||_infty <= grad_tol*/
    CGFLOAT grad_tol ;

    /* CG_DESCENT no longer includes the stopping criterion

         ||proj_grad||_infty <= grad_tol*(1 + |f_k|).

      If the optimization problem is unconstrained, then the stopping
      criterion is

         ||proj_grad||_infty <= testtol

      where testtol = max(grad_tol,initial ||grad||_infty*StopFact) and
      the default value of StopFact is zero. If the optimization problem
      contains constraints, testtol is the pasa stopping criterion
      switchfactor*global_error. This value for testtol is the PASA
      criterion to stop solving the unconstrained problem and return
      to the gradient project algorithm. */

    CGFLOAT StopFac ;

    /* T => check that f_k+1 - f_k <= debugtol*C_k
       F => no checking of function values */
    int debug ;
    CGFLOAT debugtol ;

    /* if step is nonzero, it is the initial step of the initial line search
       NOTE: if the user specifies the parameter bbk in PASA for the initial
             bb step, then bbk replaces the value of cgstep */
    CGFLOAT step ;

    /* 0 => use cg_descent
       1 => use L-BFGS
       2 => use L-BFGS when LBFGSmemory >= n, use cg_descent when memory < n
       3 => use L-BFGS when LBFGSmemory >= n, use limited memory CG otherwise */
    int LBFGS ;

    /* if LBFGS is used, then LBFGSmemory is the number of vectors in memory */
    int LBFGSmemory ;

    /* abort cg after maxit iterations */
    CGINT maxit ;

    /* conjugate gradient method restarts after (n*restart_fac) iterations */
    CGFLOAT restart_fac ;

    /* factor in [0, 1] used to compute average cost magnitude C_k as follows:
       Q_k = 1 + (Qdecay)Q_k-1, Q_0 = 0,  C_k = C_k-1 + (|f_k| - C_k-1)/Q_k */
    CGFLOAT Qdecay ;

    /* terminate after nslow iterations without strict improvement in
       either function value or gradient */
    int nslow ;

    /* factor by which eps grows when line search fails during contraction */
    CGFLOAT egrow ;

    /* T => attempt quadratic interpolation in line search when
                |f_k+1 - f_k|/f_k <= QuadCutoff
       F => no quadratic interpolation step */
    int    QuadStep ;
    CGFLOAT QuadCutOff ;

    /* maximum factor by which a quad step can reduce the step size */
    CGFLOAT QuadSafe ;

    CGFLOAT psi_lo ; /* in performing a QuadStep, we evaluate at point
                        betweeen [psi_lo, psi_hi]*psi2*previous step */
    CGFLOAT psi_hi ;
    CGFLOAT   psi1 ; /* for approximate quadratic, use gradient at
                        psi1*psi2*previous step for initial stepsize */

    CGFLOAT   qeps ; /* parameter in cost error for quadratic restart
                        criterion */
    CGFLOAT  qrule ; /* parameter used to decide if cost is quadratic */
    int   qrestart ; /* number of iterations the function should be
                        nearly quadratic before a restart */

    /* T => when possible, use a cubic step in the line search */
    int UseCubic ;

    /* use cubic step when |f_k+1 - f_k|/|f_k| > CubicCutOff */
    CGFLOAT CubicCutOff ;

    /* |f| < SmallCost*starting cost => skip QuadStep and set PertRule = FALSE*/
    CGFLOAT SmallCost ;

    /* maximum factor secant step increases stepsize in expansion phase */
    CGFLOAT ExpandSafe ;

    /* factor by which secant step is amplified during expansion phase
       where minimizer is bracketed */
    CGFLOAT SecantAmp ;

    /* factor by which rho grows during expansion phase where minimizer is
       bracketed */
    CGFLOAT RhoGrow ;

    /* If approxstep is TRUE, use approximate Wolfe line search.
       If approxstep is FALSE, then use ordinary line search and
       switch to the approximate step when |f - fnew| < ApproxSwitchFactor*|fR|,
       where fR is an estimate of the function size.  In the conjugate
       gradient code, an averaging technique is used to estimate function
       size. */
    int approxstep ;
    CGFLOAT ApproxSwitchFactor ;

    /* As the cg_descent converges, the function values typically
       approach a constant value. When this happens, the cubic interpolation
       step in the line search loses its accuracy and it is better to
       use a secant step based on the derivative of the objective function.
       The cost has converged when the relative change in the objective
       function <= CostConverge */
    CGFLOAT CostConverge ;

    CGFLOAT FuncGradSwitchFactor ;

    /* When performing an approximate Wolfe line search, we require
       that the new function value <= perturbation of the prior
       function value where the perturbation tries to take into
       rounding errors associated with the function value.
       There are two different perturbations:
       PertRule = 1 => fpert is f + Parm->pert_eps*|f| (relative change)
       PertRule = 0 => fpert is f + Parm->pert_eps     (absolute change) */
    int PertRule ;
    CGFLOAT pert_eps ;

    /* Maximum number of contractions in cg_contract. If it cannot find a
       step that either satisfies the Wolfe conditions or which has derivative
       >= 0 within ncontract attempts, then it is felt that fpert is too
       small and it will be increased so that the current function value
       is less than fpert. To increase fpert, we increase the value of
       pert_eps which is used to compute fpert. */
    int ncontract ;

    /* When pert_eps is increased, we multiply the new value by the growth
       factor eps_grow to ensure a healthy growth in pert_eps. */
    CGFLOAT eps_grow ;

    /* Maximum number of times that pert_eps is recomputed before a line
       search error is declared. */
    int neps ;

    CGFLOAT    cgdelta ; /* Wolfe line search parameter */
    CGFLOAT    cgsigma ; /* Wolfe line search parameter */
    int       maxsteps ; /* max number of tries to find acceptable step */
    CGFLOAT  stepdecay ; /* decay factor for bracket interval width */
    CGFLOAT        rho ; /* growth factor when searching for initial
                            bracketing interval */
    CGFLOAT       psi0 ; /* factor used in starting guess for iteration 1 */
    CGFLOAT       psi2 ; /* when starting a new cg iteration, our initial
                            guess for the line search stepsize is
                            psi2*previous step */
    CGFLOAT  BetaLower ; /* parameter connected with lower bound for beta */
    CGFLOAT      theta ; /* parameter describing the cg_descent family */
    int   AdaptiveTheta ; /* T => choose theta adaptively, F => use theta */

    /* When an infinite or nan objective value is encountered, the
       stepsize is reduced in an effort to find a finite objective
       value. infdecay is the initial decay factor that is used when an
       infinite or nan objective value is encountered, ninf_tries is
       the number of attempts we make to find a finite objective value,
       and infdecay_rate is a factor by which infdecay is multiplied
       after each attampt to find a finite objective value. */
    CGFLOAT cg_infdecay ;
    CGFLOAT cg_infdecay_rate ;
    int  cg_ninf_tries ;

/* ============ LIMITED MEMORY CG PARAMETERS ================================ */
    /* SubCheck and SubSkip control the frequency with which the subspace
       condition is checked. It it checked for SubCheck*mem iterations and
       if it is not activated, then it is skipped for Subskip*mem iterations
       and Subskip is doubled. Whenever the subspace condition is satisfied,
       SubSkip is returned to its original value. */
    int SubCheck ;
    int SubSkip ;

    /* when relative distance from current gradient to subspace <= eta0,
       enter subspace if subspace dimension = mem (eta0 = 0 means gradient
        inside subspace) */

    CGFLOAT   eta0 ; /* corresponds to eta0*eta0 in the paper */

    /* when relative distance from current gradient to subspace >= eta1,
       leave subspace (eta1 = 1 means gradient orthogonal to subspace) */
    CGFLOAT   eta1 ; /* corresponds to eta1*eta1 in the paper */

    /* when relative distance from current gradient to subspace <= eta2,
       always enter subspace (invariant space) */
    CGFLOAT   eta2 ;
} CGparm ;

/* --------------------------------------------------------------------------
    CGstat is a structure containing statistics which are returned to the
    user when cg_descent terminates.  They can be print by user
    using cg_print_stat or cg_print_status, or by setting the parameters
    PrintStat or PrintStatus to TRUE.
   -------------------------------------------------------------------------- */
typedef struct CGstat_struct
{
    int         status ; /* returned status from cg_descent */
    CGFLOAT          f ; /* function value at solution */
    CGFLOAT        err ; /* sup norm of the gradient */
    CGFLOAT   grad_tol ; /* error tolerance */
    CGFLOAT      gnorm ; /* max abs component of gradient */
    CGFLOAT        tol ; /* computing tolerance: gnorm <= tol */
    CGINT        maxit ; /* maximum number of iterations */
    int  cg_ninf_tries ; /* number of tries to find finite objective value */
    CGFLOAT       oldf ; /* old function value when debugger fails */
    CGFLOAT       newf ; /* new function value when debugger fails */
    int       maxsteps ; /* max number of attempts in the line search */
    int        NegDiag ; /* T => negative diagonal encountered in QP factor */
    CGINT         iter ; /* number of iterations in cg */
    CGINT        nfunc ; /* function evaluations in cg */
    CGINT        ngrad ; /* gradient evaluations in cg */
    int        IterSub ; /* number subspace iterations in limited memory cg */
    int         NumSub ; /* number of subspaces in limited memory cg */
} CGstat ;

/* --------------------------------------------------------------------------
    CGhess is a structure that is passed to the user when cg_descent wishes
    to evaluate the Hessian of the objective.
   -------------------------------------------------------------------------- */
typedef struct CGhess_struct
{
    CGINT     ncol ; /* number of cols in the Hessian */
    CGFLOAT     *x ; /* the point where the Hessian is evaluated */
    CGINT      *Hp ; /* size ncol+1, the column pointers */
    CGINT      *Hi ; /* size Hp [ncol], the row indices */
    CGFLOAT    *Hx ; /* size Hp [ncol], numerical values in the Hessian */
} CGhess ;

typedef struct CGdata_struct
{
    /* -------- cg input data -------- */
    CGFLOAT     *x ; /* size n, points to a starting guess
                        If NULL, then cg_descent allocates memory of size n
                        for x and sets the value of its entries to zero.
                        Any allocated memory is freed by cg_terminate. */
    CGINT        n ; /* dimension of x */
    CGparm   *Parm ; /* parameter structure */
    CGstat   *Stat ; /* statistics structure */

    CGFLOAT  *Work ; /* NULL => cg_descent should allocate real work
                          space. Otherwise, see allocation section of
                          cg_descent to determine memory requirements. */

    /* There are two structure elements tailored to a quadratic objective.
       These arguments should be NULL when the objective is not quadratic.
       If the objective is quadratic, then the element c can be used to store
       the linear term in the objective, while cg_hprod (p, x, n) is a
       routine to evaluate the product p between the Hessian and a vector x. */
    CGFLOAT *c ;
    void   (*hprod) (CGFLOAT *, CGFLOAT *, CGINT) ;

    /* for a general nonlinear function, value (f, x, n) is the function value*/
    void   (*value) (CGFLOAT *, CGFLOAT *, CGINT) ;
    /* for a general nonlinear function, grad (g, x, n) is the gradient */
    void    (*grad) (CGFLOAT *, CGFLOAT *, CGINT) ;
    /* for a general nonlinear function, valgrad (f, g, x, n) gives both
       function value f and gradient g at x (size n), the valgrad argument
       is optional. */
    void (*valgrad) (CGFLOAT *, CGFLOAT *, CGFLOAT *, CGINT) ;

    /* hess evaluates the Hessian at a given point, not currently used,
       optional argument */
    void    (*hess) (CGhess *) ;

    /* the following are used internally when the code allocates memory */
    CGFLOAT *x_created ; /* pointer to memory created for x */
} CGdata ;

typedef struct CGcom_struct /* common variables */
{
    CGdata        *cgdata ; /* pointer to cgdata structure */
    /* first two arguments below not used in unconstrained cg */
    CGFLOAT          *AAd ; /* (A'A)*d (Hessian of penalty) * d in CG */
    CGFLOAT         *gpen ; /* gradient of penalty term in CG */

    int          QuadCost ; /* TRUE is objective is quadratic */
    CGFLOAT            *c ; /* linear term when objective quadratic */
    /* Hessian times vector for a quadratic objective */
    void   (*hprod) (CGFLOAT *, CGFLOAT *, CGINT) ;
    /* cg_value (f, x, n) */
    void (*value) (CGFLOAT *, CGFLOAT *, CGINT) ;
    /* cg_grad (g, x, n) */
    void (*grad) (CGFLOAT *, CGFLOAT *, CGINT) ;
    /* cg_valgrad (f, g, x, n)*/
    void (*valgrad) (CGFLOAT *, CGFLOAT *, CGFLOAT *, CGINT) ;
    CGFLOAT *work_created ; /* work array created if none provided */
    CGFLOAT          f_at ; /* stepsize where function is evaluated */
    CGFLOAT         df_at ; /* stepsize where derivative is evaluated */
    CGFLOAT           *Qd ; /* Hessian * search direction d for quadratics */
    CGFLOAT       QPshift ; /* replace Hessian Q of quadratic by Q+QPshift*I */
    CGINT               n ; /* problem dimension, saved for reference */
    CGINT       FirstIter ; /* first iteration of pasa */
    int           NegDiag ; /* F => no negative diagonal element in QR factor */
    int            QuadOK ; /* T (quadratic step successful) */
    int          UseCubic ; /* T (use cubic step) F (use secant step) */
    int          PertRule ; /* 1 => estimated error in function value is eps*f,
                               0 => estimated error in function value is eps */
    int             QuadF ; /* T => function appears to be quadratic */
    int              neps ; /* number of time eps updated */
    CGFLOAT         fpert ; /* perturbation is pert_eps*|f| if PertRule = 1 */
    CGFLOAT      pert_eps ; /* current value of pert_eps */
    CGFLOAT       maxstep ; /* used in pasa for storing maximum allowed step */
    CGFLOAT     SmallCost ; /* |f| <= SmallCost => set PertRule = F */
    CGFLOAT         alpha ; /* stepsize along search direction */
    CGFLOAT             f ; /* function value for step alpha */
    CGFLOAT            df ; /* directional derivative for step alpha */
    CGFLOAT            f0 ; /* old function value */
    CGFLOAT           df0 ; /* old derivative */
    CGFLOAT            Ck ; /* average cost as given by the rule:
                               Qk = Qdecay*Qk + 1, Ck += (fabs (f) - Ck)/Qk */
    CGFLOAT      wolfe_hi ; /* upper bound for slope in Wolfe test */
    CGFLOAT      wolfe_lo ; /* lower bound for slope in Wolfe test */
    CGFLOAT     awolfe_hi ; /* upper bound for slope, approximate Wolfe test */
    int        approxstep ; /* T (use approximate Wolfe line search)
                               F (use             Wolfe line search) */
    int        AvoidFeval ; /* T when function values converges */
    int             Wolfe ; /* becomes T when Wolfe line search performed */
    CGFLOAT      alphaold ; /* previous value for stepsize alpha */
    CGFLOAT            *x ; /* current iterate */
    CGFLOAT            *d ; /* current search direction */
    CGFLOAT            *g ; /* gradient at x */
    CGFLOAT         *xnew ; /* x + alpha*d */
    CGFLOAT         *gnew ; /* gradient at x + alpha*d */
    /* if Wolfe line search fails and we try approxstep, need the following */
    CGFLOAT        savedf ;
    CGFLOAT     savealpha ;
    CGFLOAT        savefb ;
    int            saveqb ;
    CGFLOAT      maxeqerr ; /* ||Ax-b||_inf for active constraints */
    CGparm          *Parm ; /* user parameters */
    CGstat          *Stat ; /* CG statistics */
} CGcom ;

/* ==========================================================================
   ================ prototypes ==============================================
   ========================================================================== */
int cg_descent
(
    CGdata  *cgdata /* CG data structure */
) ;

CGdata * cg_setup (void) ;

void cg_terminate
(
    CGdata **DataHandle
) ;

int cg_wrapup
(
    int       status,
    CGcom     *cgcom
) ;

int cg_evaluate
(
    CGFLOAT alpha_good, /* a value of alpha for which function is finite */
    CGFLOAT     *Alpha, /* stepsize along the search direction */
    char         *what, /* fg = eval func & grad, g = grad only,f = func only */
    CGcom         *Com
) ;

int cg_line
(
    int       repeat, /* TRUE => Wolfe search failed, retry using approxstep */
    CGcom     *cgcom
) ;

int cg_contract
(
    CGFLOAT       *A, /* left side of bracketing interval */
    CGFLOAT      *fA, /* function value at a */
    CGFLOAT      *dA, /* derivative at a */
    CGFLOAT       *B, /* right side of bracketing interval */
    CGFLOAT      *fB, /* function value at b */
    CGFLOAT      *dB, /* derivative at b */
    CGcom     *cgcom
) ;

/* ==========================================================================
   ================ protypes for pure cg_descent routines ===================
   ========================================================================== */

void cg_default
(
    CGparm *Parm /* pointer to parameter structure */
) ;

void cg_print_status
(
    CGdata *Data /* pointer to cgdata structure */
) ;

void cg_print_stat
(
    CGdata *Data /* pointer to cgdata structure */
) ;

void cg_print_parm
(
    CGdata *Data /* pointer to cgdata structure */
) ;

void cg_print_TF
(
    int TF /* TRUE or FALSE */
) ;

int cg_Wolfe
(
    CGFLOAT  alpha, /* stepsize */
    CGFLOAT      f, /* function value associated with stepsize alpha */
    CGFLOAT   dphi, /* derivative value associated with stepsize alpha */
    CGcom   *cgcom
) ;

CGFLOAT cg_cubic
(
    CGFLOAT  a,
    CGFLOAT fa, /* function value at a */
    CGFLOAT da, /* derivative at a */
    CGFLOAT  b,
    CGFLOAT fb, /* function value at b */
    CGFLOAT db  /* derivative at b */
) ;

void cg_scale
(
    CGFLOAT *y, /* output vector */
    CGFLOAT *x, /* input vector */
    CGFLOAT  s, /* scalar */
    CGINT    n /* length of vector */
) ;

void cg_daxpy
(
    CGFLOAT     *x, /* input and output vector */
    CGFLOAT     *d, /* direction */
    CGFLOAT  alpha, /* stepsize */
    CGINT        n  /* length of the vectors */
) ;

CGFLOAT cg_dot
(
    CGFLOAT       *x, /* first vector */
    CGFLOAT       *y, /* second vector */
    CGINT   const  n /* length of vectors */
) ;

void cg_copy
(
    CGFLOAT       *y, /* output of copy */
    CGFLOAT       *x, /* input of copy */
    CGINT   const  n  /* length of vectors */
) ;

void cg_step
(
    CGFLOAT *xnew, /*output vector */
    CGFLOAT    *x, /* initial vector */
    CGFLOAT    *d, /* search direction */
    CGFLOAT alpha, /* stepsize */
    CGINT       n  /* length of the vectors */
) ;

void cg_initi
(
    CGINT *x,  /* array to be initialized */
    CGINT  s,  /* scalar */
    CGINT  n   /* length of x */
) ;

void cg_initx
(
    CGFLOAT *x, /* input and output vector */
    CGFLOAT  s, /* scalar */
    CGINT    n  /* length of vector */
) ;

CGFLOAT cg_update_2
(
    CGFLOAT *gold, /* old g */
    CGFLOAT *gnew, /* new g */
    CGFLOAT    *d, /* d */
    CGINT       n /* length of vectors */
) ;

void cg_update_beta
(
    CGFLOAT *oldproj,
    CGFLOAT *newproj,
    CGFLOAT   *GkPyk,
    CGFLOAT   *YkPyk,
    CGINT          n  /* length of vectors */
) ;

void cg_update_d
(
    CGFLOAT      *d,
    CGFLOAT  *gproj,
    CGFLOAT    beta,
    CGINT         n  /* length of vectors */
) ;

/* limited memory CG routines */

void cg_matvec
(
    CGFLOAT *y, /* product vector */
    CGFLOAT *A, /* dense matrix */
    CGFLOAT *x, /* input vector */
    CGINT    n, /* number of columns of A */
    CGINT    m, /* number of rows of A */
    int      w  /* T => y = A*x, F => y = A'*x */
) ;

void cg_trisolve
(
    CGFLOAT *x, /* right side on input, solution on output */
    CGFLOAT *R, /* dense matrix */
    int      m, /* leading dimension of R */
    int      n, /* dimension of triangular system */
    int      w  /* T => Rx = y, F => R'x = y */
) ;

void cg_scale0
(
    CGFLOAT *y, /* output vector */
    CGFLOAT *x, /* input vector */
    CGFLOAT  s, /* scalar */
    int      n /* length of vector */
) ;

void cg_daxpy0
(
    CGFLOAT    *x, /* input and output vector */
    CGFLOAT    *d, /* direction */
    CGFLOAT alpha, /* stepsize */
    int         n  /* length of the vectors */
) ;

CGFLOAT cg_dot0
(
    CGFLOAT *x, /* first vector */
    CGFLOAT *y, /* second vector */
    int      n /* length of vectors */
) ;

void cg_copy0
(
    CGFLOAT *y, /* output of copy */
    CGFLOAT *x, /* input of copy */
    int      n  /* length of vectors */
) ;

void cg_Yk
(
    CGFLOAT    *y, /*output vector */
    CGFLOAT *gold, /* initial vector */
    CGFLOAT *gnew, /* search direction */
    CGFLOAT  *yty, /* y'y */
    CGINT       n  /* length of the vectors */
) ;

CGFLOAT cg_update_inf2
(
    CGFLOAT   *gold, /* old g */
    CGFLOAT   *gnew, /* new g */
    CGFLOAT      *d, /* d */
    CGFLOAT *gnorm2, /* 2-norm of g */
    CGINT         n  /* length of vectors */
) ;

CGFLOAT cg_inf
(
    CGFLOAT *x, /* vector */
    CGINT    n /* length of vector */
) ;

/* ========================================================================== */
/* ====== cg_error ========================================================== */
/* ========================================================================== */
/* when -g compiler option is used, prints line number of error */
void cg_error
(
    int          status,
    const char    *file,
    int            line,
    const char *message
) ;

/* BLAS */
#ifndef NOBLAS
void CG_DGEMV (char *trans, BLAS_INT *m, BLAS_INT *n, CGFLOAT *alpha,
        CGFLOAT *A, BLAS_INT *lda, CGFLOAT *X, BLAS_INT *incx,
        CGFLOAT *beta, CGFLOAT *Y, BLAS_INT *incy) ;

void CG_DTRSV (char *uplo, char *trans, char *diag, BLAS_INT *n, CGFLOAT *A,
        BLAS_INT *lda, CGFLOAT *X, BLAS_INT *incx) ;

void CG_DAXPY (BLAS_INT *n, CGFLOAT *DA, CGFLOAT *DX, BLAS_INT *incx,
        CGFLOAT *DY, BLAS_INT *incy) ;

CGFLOAT CG_DDOT (BLAS_INT *n, CGFLOAT *DX, BLAS_INT *incx, CGFLOAT *DY,
        BLAS_INT *incy) ;

void CG_DSCAL (BLAS_INT *n, CGFLOAT *DA, CGFLOAT *DX, BLAS_INT *incx) ;

void CG_DCOPY (BLAS_INT *n, CGFLOAT *DX, BLAS_INT *incx, CGFLOAT *DY,
        BLAS_INT *incy) ;

BLAS_INT CG_IDAMAX (BLAS_INT *n, CGFLOAT *DX, BLAS_INT *incx) ;
#endif


#endif
