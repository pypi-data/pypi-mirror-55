#include "pproj.h"

/* =========================================================================
   ============================== pproj_default ============================
   ========================================================================= */
void pproj_default
(
    PPparm *Parm /* Parameter structure */
)
{
    /* relative error tol for dual function gradient*/
    Parm->grad_tol = 1.e-10 ;

    /* T => print status of run
       F => do not print status of run */
    Parm->PrintStatus = TRUE ;

    /* T => print statistics
       F => do not print statistics */
    Parm->PrintStat = FALSE ;

    /* PrintLevel = 0 (noprint), 1 (final), 2 (outside of loops),
                    3 (inside loops) */
    Parm->PrintLevel = 0 ;

    /* PrintParm = TRUE => print the parameters */
    Parm->PrintParm = FALSE ;

    /* T => return the problem data in priordata argument of ppdata */
    Parm->return_data = FALSE ;

    /* T => use data in priordata argument of ppdata */
    Parm->use_prior_data = FALSE ;

    /* T     => lower bounds for x are present
       F     => lower bounds for x not present, treat lo as -infinity */
    Parm->loExists = TRUE ;

    /* T     => upper bounds for x are present
       F     => upper bounds for x not present, treat hi as +infinity */
    Parm->hiExists = TRUE ;

    /* T => do not terminate until the matrix has been factored
       F => terminate as soon as error tolerance condition is satisfied */
    Parm->getfactor = FALSE ;

    /* debug = 0 (no debugging)
       debug = 1 (debugging outside of main loops)
       debug = 2 (debugging inside of main loops) */
    Parm->debug = 0 ;

    /* relative tolerance for reporting an error in the debugging routines */
    Parm->checktol = 1.e-5 ;

    /* As explained in the comments at the start of this code, we solve
       the projection problem by optimizing a quadratic regularized version
       of the dual problem where the regularization parameters are a scalar
       sigma with a relatively small value (see below), and a vector
       shift_l. We are essentially computing the solution to the dual
       problem closest to shift_l. The integer assigned to start_guess has
       the following interpretation:

       start_guess = 0 => the initial guess for the solution of the dual
                          problem is lambda = 0 and shift_l = 0
                     1 => the user provided input argument lambda is put in
                          shift_l and the starting guess for the dual problem is
                          lambda = 0 (final dual solution is shift_l + lambda)
                          use this when the starting guess is very good
                     2 => shift_l = 0 and starting guess for the solution
                          to the dual problem is based on bound structure
                          associated with a prior run found in ppcom argument
                          of pproj
                     3 => shift_l = 0 and the starting guess for the solution
                          of the dual problem is the input argument lambda
                     4 => shift_l = 0 and the starting guess for the solution
                          of the dual problem is Work->lambda (from prior run)*/
    Parm->start_guess = 0 ;

    /* If user passes a prior PPcom structure, and permute = F,
       then it is assumed that the user is employing pproj's ordering. If
       permute = T, then the solution output is permuted to correspond to
       the user's ordering of variables. */
    Parm->permute = TRUE ;

    /* Phase1 controls the initial number of coordinate ascent iterations.
       The number of iterations is max {nrow^phase1, 5}. To skip phase1,
       set phase1 < 0 */
    Parm->phase1 = .333 ;

    /* T = use cholmod to update and downdate the linear equation
       F = solve linear equations by iterative method */
    Parm->cholmod = TRUE ;

    /* T = perform a multilevel partition of the problem (used if cholmod = T)
           and solve using the multilevel version of the algorithm
       F = use problem as given */
    Parm->multilevel = TRUE ;

    /* 0 = use relative criterion ||grad L (lambda)||_sup / absAx_sup <=
           grad_tol where absAx_sup = max_i sum_j |a_{ij}x_j| where x achieves
           min in dual function
       1 = use absolute stopping criterion ||grad L (lambda)||_sup <= grad_tol
       2 = use relative criterion ||grad L (lambda)||_sup / (absAx_sup + ymax)
           <= grad_tol where ymax is the sup-norm of the projection point y */
    Parm->stop_condition = 0 ;

    /* Upper bound on the maximum number of proximal updates. Assuming
       sigma is small, like 2^(-44), the number of proximal updates should
       be small. */
    Parm->nprox = 5 ;

    /* The dual function that is maximized includes a proximal term
       of the form 0.5*sigma*||lambda - mu||^2. We make sigma extremely
       small so that this term has very little effect. It ensures that
       the line search terminates. */
    Parm->sigma = ldexp (1, -90) ;

    /* To ensure that the factorization routine does not encounter a diagonal
       element <= 0, we add Asigma + sigma to the diagonal of A_F A_F' */
    Parm->Asigma = ldexp (1, -44) ;

    /* T => scale sigma and Asigma by max |a_{ij}| */
    Parm->ScaleSigma = TRUE ;

    /* In each proximal update, sigma decays by the factor sigma_decay */
    Parm->sigma_decay = PPONE ;

    /* Factor by which the stepsize parameter alpha grows when the Armijo
       condition in SpaRSA is not satisfied */
    Parm->armijo_grow = 4.0 ;

    /* Maximum number of times we try to satisfy the Armijo condition
       in SpaRSA */
    Parm->narmijo = 10 ;

    /* number of objective function values stored for the SpaRSA line search */
    Parm->mem = 8 ;

    /* Maximum number of SpaRSA iterations */
    Parm->nsparsa = 1000 ;

    /* The SpaRSA line search is nonmonotone. mem is the number of prior
       function values to store for computing the reference value in the
       line search */

    /* Stopping parameter for SpaRSA. Stop when there is a component of the
       gradient associated with equality constraints or bound inequality
       constraints for which |grad_i L_R| >= gamma * max_k |grad_k L_R| */
    Parm->gamma = 0.1 ;

    /* tau, beta, grad_decay, and gamma_decay are parameters that enter into
       the the definition of the undecided index set. An index j is undecided
       if sign (lambda_j) grad_j L_R <= -tau max_{k active} |grad_k L_R|^beta
       The active rows are the row in RLinkUp and RLinkDn. They correspond
       to equality constraints and active inequality constraints. Undecided
       indices are only monitored when ||current gradient|| <= grad_decay *
       ||initial gradient (after phase1)|| */
    Parm->tau = 0.1 ;
    Parm->beta = 0.5 ;
    Parm->grad_decay = 1.e-4 ;
    Parm->gamma_decay = 0.5 ;

    /* T = use CHOLMOD statistics to determine whether to perform a coordinate
           ascent iteration
       F = do not use coordinate ascent at the start of dasa */
    Parm->use_coor_ascent = TRUE ;

    /* The cost of a coordinate ascent iteration is proportional to Annz
       while the cost of an update/downdate iteration is proportional to Lnnz.
       We perform coordinate ascent iteration when Annz*coorcost <= estimate
       for the number of flops for an update */
    Parm->coorcost = 1. ;

    /* T = use ssor0 iteration
       F = do not use ssor0
       If T and CHOLMOD is used, then CHOLMOD statistics is used to decide
       whether the ssor0 iteration is worthwhile */
    Parm->use_ssor0 = TRUE ;

    /* T = use ssor1 iteration
       F = do not use ssor1
       If T and CHOLMOD is used, then CHOLMOD statistics is used to decide
       whether the ssor1 iteration is worthwhile */
    Parm->use_ssor1 = TRUE ;

    /* T = use SpaRSA iteration if appropriate
       F = do not use SpaRSA */
    Parm->use_sparsa = TRUE ;

    /* T means that the routines hotchol and phase1 are used when use_ppcom
       is T or F respectively. You must be an expert to set use_startup = F */
    Parm->use_startup = TRUE ;

    /* Stop ssor1 when current errls <= ssor_decay * errdual */
    Parm->ssordecay = 4.e-3 ;

    /* In the ssor1 iteration, we store ssormem prior search directions
       and optimize over the space spanned by these prior search directions
       when the active constraints change. */
    Parm->ssormem = 8 ; /* must be > 1 if ssor1 is used */

    /* The cost of an ssor iteration is proportional to Annz while the cost
       of an update/downdate iteration is proportional to Lnnz. We perform
       ssor iterations when Annz*ssorcost <= estimate for the number of
       flops for an update */
    Parm->ssorcost = 8. ;

    /* Upper bound on the number of ssor iterations */
    Parm->ssormaxits = PPINFINT ;

    /* If a row has been dropped, we do not immediately rebind it, but
       allow some slack before rebinding. If other optimality violations
       are large enough, we keep the row dropped or the column free
       until there is some benefit in the error from adding the row or
       binding the column */
    Parm->cutfactor = .0001 ;

    /* In the ssor iteration, we continue to ascend the dual function
       freeing variables until the residual error (err1) for the linear
       equation is small relative to the error (err) connected with free
       variables violating the bound constraints. Since the equation is
       positive definite, err1 tends to 0 as variables are freed and the
       dual function is ascended */
    Parm->tolssor = ldexp (1, -8) ; /* stop when err1 <= err*tolssor */

    /* To regularize the dual function, we add the proximal term
       sigma/2 ||lambda - shift_l|| to obtain the regularized dual function
       L_R (lambda) above. A proximal update is performed, replacing shift_l
       by the current lambda, when
       ||grad L_R (lambda)||_1 <= tolprox*||grad L (lambda)||_1 */
    Parm->tolprox = 0.01 ;

    /* Refactor A when
       ||b - Ax - sigma*(lamba-shift_l)||_1 >= tolrefactor*||b||_1
       The expression on the left is the norm of the residual of the
       linear system that is solved in dasa. */
    Parm->tolrefactor = .03125 ;

    /* Stop execution when the tolrefactor condition holds for
       badFactorCutoff consecutive iterations */
    Parm->badFactorCutoff = 3 ;

    /* LP = TRUE => PPROJ is being used to solve an LP */
    Parm->LP = FALSE ;

    /* There are special parameters when PPROJ is used to solve an LP.
       Terminate PPROJ when dual gradient <= grad_tol*LinGrad_tol*norm_lambda */
    Parm->LinGrad_tol = 1.e-2 ;

    /* Terminate PPROJ when normalized dual gradient (primal feasibility) <=
       LinFactor times normalized dual feasibility error */
    Parm->LinFactor = 1.e-4 ;
}
