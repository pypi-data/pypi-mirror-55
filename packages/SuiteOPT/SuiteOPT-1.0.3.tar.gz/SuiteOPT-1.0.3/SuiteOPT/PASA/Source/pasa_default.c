#include "pasa.h"

/* ==========================================================================
   === pasa_default =========================================================
   ==========================================================================
    Set PASA default parameter values
   ========================================================================== */
void pasa_default
(
    PASAparm *Parm /* pointer to a pasa parameter structure */
)
{
    /* The user can precisely specify the structure of the optimization
       problem by setting one of the parameters UNC, BNC, LP, QP, NL, PROJ,
       or NAPSACK to TRUE. Alternatively, if the problem structure is clear
       from the choice of the inputs in pasadata, then the parameters can
       be left EMPTY, and the pasa code will auto-detect the problem structure
       based on the input parameters. If the pasadata inputs do not
       uniquely define the problem structure, then the user needs to set
       exactly one of the parameters below to TRUE. */

    /* TRUE  => the problem has no constraints:
                    min f(x) s.t. x \in R^n.
       EMPTY => unspecified */
    Parm->UNC = EMPTY ;

    /* TRUE => the problem has only bound constraints:
                   min f(x) s.t. lo <= x <= hi.
       EMPTY => unspecified */
    Parm->BNC = EMPTY ;

    /* TRUE => the problem is a linear program:
                   min c'*x s.t. lo <= x <= hi, bl <= A*x <= bu.
       EMPTY => unspecified */
    Parm->LP = EMPTY ;

    /* TRUE => the problem is a quadratic program:
                   min 0.5*x'*Q*x + c'*x s.t. lo <= x <= hi, bl <= A*x <= bu.
       EMPTY => unspecified */
    Parm->QP = EMPTY ;

    /* TRUE => the objective is possibly nonlinear objective and
               the constraints are polyhedral:
                   min f(x) s.t. lo <= x <= hi, bl <= A*x <= bu.
       EMPTY => unspecified */
    Parm->NL = EMPTY ;

    /* TRUE => a separable convex quadratic napsack problem:
                   min 0.5*x*'D*x - c'*x s.t. lo <= x <= hi, bl <= a'*x <= bu,
             where D is a diagonal matrix and "a" is a vector. NOTE: the
             linear cost vector is "-c" in a napsack problem, but "+c"
             is a quadratic program.
       EMPTY => unspecified */
    Parm->NAPSACK = EMPTY ;

    /* TRUE => a polyhedral constrained projection:
             min 0.5*||x - y||^2 s.t. lo <= x <= hi, bl <= A*x <= bu.
       EMPTY => unspecified */
    Parm->PROJ = EMPTY ;

    /* KKT error tolerance */
    Parm->grad_tol = 1.e-6 ;

    /* T => print status of run
       F => do not print status of run */
    Parm->PrintStatus = TRUE ;

    /* T => print pasa statistics
       F => do not print statistics */
    Parm->PrintStat = FALSE ;

    /* T => print parameter values 
       F => do not print parameter values */
    Parm->PrintParm = FALSE ;

    /* Level 0 (no printing), 1 (key branching),
             2 (more printing outside loops), 3 (also print inside loops) */
    Parm->PrintLevel = 0 ;

    /* T => only use gradient projection algorithm
       F => let algorithm decide between grad_proj and cg */
    Parm->GradProjOnly = FALSE ;

    /* T => when CG hits boundary of feasible region, branch to active set
            grad_proj
       F => when CG hits boundary, restart CG */
    Parm->use_activeGP = TRUE ;

    /* T => use NAPHEAP algorithm for the projection when there is one row in A
       F => always use PPROJ for the projection */
    Parm->use_napheap = TRUE ;

    /* T => use a provided routine to evaluate the Hessian at a given iterate
       F => Hessian is not provided
       CURRENTLY, THIS MUST BE FALSE SINCE PASA DOES NOT UTILIZE HESSIANS */
    Parm->use_hessian = FALSE ;

    /* The parameters loExists/hiExists can be used to make the
       code ignore the corresponding input arguments in the pasadata structure.
       For example, setting Parm->loExists = FALSE is equivalent to setting
       pasadata->lo = NULL. */
    /* T => lower bounds for x are present
       F => lower bounds for x not present, ignore input argument userlo */
    Parm->loExists = TRUE ;

    /* T => upper bounds for x are present
       F => upper bounds for x not present, ignore input argument userhi */
    Parm->hiExists = TRUE ;

    /* For an LP, updateorder refers to the proximal update order.
       Currently, only a first-order update is implemented. Second-order
       will be later. */
    Parm->updateorder = 1 ;

    /* epsilon is the proximal regularization parameter for an LP.
       In a gradient projection step, 1/epsilon is the stepsize along
       the negative cost gradient. For an LP, this is just the negative
       of the linear cost vector.  If epsilon is 0, then the code uses
       the following formula for epsilon:

       if      ( nrow <  100 ) epsilon = 64
       else if ( nrow < 2500 ) epsilon = 8
       else                    epsilon = 1 */
    Parm->epsilon = PASAZERO ;

    /* In an LP, when c_err (the dual feasibility error) satisfies the
       relation c_err <= cerr_decay*grad_tol, then we let epsilon grow
       by the factor EpsilonGrow in an effort to make b_err (the primal
       infeasibility error) smaller in the next gradient projection step;
       this amounts to taking a smaller step along the negative gradient.
       Otherwise, epsilon decays by the factor EpsilonDecay, which amount
       to a larger step along the negative gradient in the gradient
       projection step, in an effort to make c_err smaller */
    Parm->cerr_decay = .1 ;
    Parm->EpsilonGrow = 32 ;
    Parm->EpsilonDecay = ldexp (1, -3) ; /* 1/8 by default */

    /* an adjustment added to a quadratic cost objective when it is evaluated */
    Parm->fadjust = PASAZERO ;

    /* T => use the input starting guess for the dual multiplier lambda
            associated with the constraints for the first projection
       F => starting guess in the first projection is lambda = 0
       For the subsequent projections, the starting guess is determined by
       the parameter start_guess of pproj. */
    Parm->use_lambda = FALSE ;

    /* pproj_start_guess is based on the bound structure associated with the
       prior projection */
    Parm->pproj_start_guess = 2 ;


    /* T => include multiplier term lambda'(Ax - b) + 0.5p||Ax-b||^2
            in objective when using CG
       F => unmodified objective */
    Parm->use_penalty = TRUE ;

    /* penalty when use_penalty = T */
    Parm->penalty = 1.e6 ;

    /* debug = T => check that f_k+1 - f_k <= debugtol*fR.
       debug = F => no checking of function values */
    Parm->debug = FALSE ;
    Parm->debugtol = 1.e-4 ;

/* =================== SWITCH BETWEEN GRAD_PROJ AND CG ====================== */
    /* The switch between grad_proj and cg is controlled by the parameter
       theta in the pasa paper, which is denoted switchfactor in the code.
       If the local error e >= switchfactor * global error E, then we
       branch from grad_proj to cg. When the undecided index set becomes
       empty, the switchfactor is multiplied by switchdecay. In the active
       set gradient projection algorithm, we switch to cg when terminate_agp
       iterations were performed without a change in the bounds on the
       variables or without a change in the active inequalities. */
    Parm->switchfactor = 0.10 ;
    Parm->switchdecay = 0.5 ;
    Parm->terminate_agp = 1 ;

/* =================== ERROR CHECKING ======================================= */
    /* If the active set algorithm is used, then we test the stopping
       condition in grad_proj at iterations 1, 2, 4, 7, 11, ...
       until the difference between tests reaches testit. Thereafter,
       we test for convergence every testit iterations. If the active set
       algorithm is not used, then we test for convergence every testit
       iteration.  In cg, we record the global error at the start, and
       then we continue cg iterations until the local error <=
       switchfactor*initial global error. */
    Parm->testit = 8 ;

    /* Solution tolerance for the projected gradient */
    Parm->GPtol = 1.e-12 ;

/* =================== LIMITS =============================================== */
    Parm->gpmaxit = PASAINFINT ; /* max # gradient projection iterations */

    /* conjugate gradient method restarts after (n*restart_fac) iterations */
    Parm->restart_fac = 6.0 ;

/* ================ PARAMETERS USED TO COMPUTE REFERENCE VALUE ============== */
    /* update fr if f_min was not improved after L iterations */
    Parm->L = 3 ;

    /* f_max = max (f_{k-i}, i = 0, 1, ..., min(k, M-1) */
    Parm->M = 8 ;

    /* update fr if initial stepsize was accepted in previous P iterations */
    Parm->P = 40 ;

    /* update reference value fr if (fr-f_min)/(fmaxmin-f_min) > gamma1 */
    Parm->gamma1 = (PASAFLOAT) Parm->M / (PASAFLOAT) Parm->L ;

    /* update fr if (fr-f)/(f_max-f) > gamma2, np > P, and f_max > f */
    Parm->gamma2 = (PASAFLOAT) Parm->P / (PASAFLOAT) Parm->M ;

    /* set fr = f_max if fr - f > gamma3|f| */
    Parm->gamma3 = 1000. ;

/* ==== PARAMETERS USED TO COMPUTE BB APPROXIMATION bbk*I TO HESSIAN ==== */
    Parm->lambda0 = 1.e-30 ; /* lower bound for bbk */

    /* initialize bbk as lambda0Factor*||x||/||g|| */
    Parm->lambda0Factor = 1. ;

    /* for the first iteration, a positive value for bbk can be given */
    Parm->bbk = PASAZERO ; /* 0 => use default startup procedure */

    /* if the function is not convex locally, then we bbk grows
       by at least the factor bbexpand */
    Parm->bbexpand = 2.0 ;

    /* In certain cases we do not use the the BB formula to compute bbk.
       These cases mostly correspond to situations where the function
       is not locally convex. However, when the relative change in the
       function value is small enough, it becomes difficult to detect
       a loss of convexity, and in this case we use the BB formula.
       If |fnew - f| <= bbSwitchFactor*|f|, then we use the BB formula. */
    Parm->bbSwitchFactor = 1.e-10 ;

    /* maximum cycle length in BB stepsize calculation */
    Parm->MaximumCycle = 6 ;

    /* nominal cycle length in BB stepsize calculation */
    Parm->NominalCycle = 4 ;

/* =================== LINE SEARCH ========================================== */
    /* T => use approximate Armijo step
       F => use ordinary Armijo,
            switch to approximate when |fR - f| < ArmijoSwitchFactor*|fR|
       ArmijoSwitchFactor = 0 => ordinary Armijo if approxstep = F */
    Parm->approxstep = FALSE ;
    Parm->ArmijoSwitchFactor = 1.e-6 ;

    /* When performing an approximate Wolfe or an approximate Armijo line
       search, we always require that the new function value <= a perturbation
       of the prior function value. There are two different perturbations.
       If PertRule = 1, then the perturbation is Parm->pert_eps*|f|, while
       if PertRule = 0, then the perturbation is Parm->pert_eps */
    Parm->PertRule = 1 ;
    Parm->pert_eps = 1.e-6 ;

    /* maximum number of times that eps is updated */
    Parm->neps = (int) 5 ;

    /* ordinary Armijo step accepted if phi(alpha) <= fR + alpha*delta*phi'(0)*/
    Parm->Armijo_delta = 1.0e-4 ;

    /* Wolfe line search parameter between 0 and 0.5
       phi (a) - phi (0) <= delta phi'(0) */
    Parm->Wolfe_delta = 0.1 ;

    /* In a Wolfe line search, it is also required that gnew'*dk >=
       Wolfe_sigma*gk'*dk where sigma is between Wolfe_delta and 1. */
    Parm->Wolfe_sigma = 0.9 ;

    /* maximum number of attempts to find an acceptable stepsize */
    Parm->maxsteps = (int) 99 ;

    /* backtracking decay factor for stepsize */
    Parm->stepdecay = 0.2 ;

    /* the quadratic interpolation and secant step is restricted to the
       safeguarded interval [safe0, safe1]*alpha */
    Parm->safe0 = 1.e-2 ;
    Parm->safe1 = 9.e-1 ;

    /* When an infinite or nan objective value is encountered, the
       stepsize is reduced in an effort to find a finite objective
       value. infdecay is the initial decay factor that is used when an
       infinite or nan objective value is encountered, ninf_tries is
       the number of attempts we make to find a finite objective value,
       and infdecay_rate is a factor by which infdecay is multiplied
       after each attempt to find a finite objective value. */

    Parm->infdecay = 0.5 ;
    Parm->infdecay_rate = 0.9 ;
    Parm->ninf_tries = 20 ;
}
