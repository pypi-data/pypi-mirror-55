#include "pproj.h"

/* =========================================================================
 * ================================= PPROJ =================================
 * =========================================================================
       ________________________________________________________________
      |                                                                |
      |   min 0.5||x0 - y0||^2 - y1'x1                                 |
      |                                                                |
      |      subject to  lo <= x <= hi,  bl <= Ax <= bu                |
      |                                                                |
      |   where A = [A0 -A1], x' = [x0' x1'], ||.|| is the Euclidean   |
      |   norm and the A1 part of A is a matrix for which each column  |
      |   is zero except for a single 1. The y1 and A1 data could be   |
      |   vacuous.  When y1 and A1 exist, it is required that bl = bu, |
      |   and the elements of y1 corresponding to the nonzeros in any  |
      |   row of A1 are all distinct and in increasing order.          |
      |                                                                |
      |                  Version 1.0  (January 9, 2015)                |
      |                  Version 1.1  (February 26, 2015)              |
      |                  Version 1.2  (August 1, 2019)                 |
      |                                                                |
      |                 Copyright by William W. Hager                  |
      |________________________________________________________________|

    The constraints are rewritten as

              lo <= x <= hi,  bl <= b <= bu,  Ax = b.

    The algorithm is based on maximizing the regularized dual function

        L (lambda) = inf {.5||x0 - y0||^2 - y1'x1 + lambda'(b - Ax) 
                       -.5*sigma||lambda - shift_l||^2 :
                        lo <= x <= hi,  bl <= b <= bu}

    Since b and x1 appear linearly in the minimization, the dual function can
    have a discontinuous derivative. The stopping condition is based on
    either the absolute gradient (Parm->stop_condition = 1) or a relative
    gradient (Parm->stop_condition = 0). The absolute stopping criterion is

        ||grad L (lambda)||_sup <= grad_tol,

    where the norm is the sup norm (maximum absolute component), while
    the relative stopping criteria is

        ||grad L (lambda)||_sup / absAx_sup <= grad_tol,

    where absAx_sup = max_i sum_j |a_{ij} * x_j| and x achieves minimum in the
    dual function.  Any scaling of the constraints should be done in advance.
    In the case where L is nondifferentiable, the gradient is interpreted as
    the minimum norm subdifferential.

    NOTE: The code is designed to solve efficiently multiple problems where
          only the y vector changes in each problem. To implement this,
          the parameter return_data is set to TRUE when solving the first
          problem with pproj. Then in subsequent runs, the parameter
          use_prior_data is also set to TRUE. All the data is freed after
          the problem set is solved by running pproj_terminate.
       ________________________________________________________________
      |This program is free software; you can redistribute it and/or   |
      |modify it under the terms of the GNU General Public License as  |
      |published by the Free Software Foundation; either version 2 of  |
      |the License, or (at your option) any later version.             |
      |This program is distributed in the hope that it will be useful, |
      |but WITHOUT ANY WARRANTY; without even the implied warranty of  |
      |MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   |
      |GNU General Public License for more details.                    |
      |                                                                |
      |You should have received a copy of the GNU General Public       |
      |License along with this program; if not, write to the Free      |
      |Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, |
      |MA  02110-1301  USA                                             |
      |________________________________________________________________|

      Alternative licenses are also available.  Please contact William Hager
      for details.
   ========================================================================== */

int pproj  /* return status 0 if solution found, see pproj.h for nonzero ints */
(
    PPdata *ppdata /* Structure containing pasa input data. Initialize it
                       using pproj_setup and then modify entries to describe
                       the user's problem */
)
{
    int it, status ;
    PPINT i, j, k, l, one, *RLinkUp, *RLinkDn ;
    PPFLOAT t, tic ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork *W ;
    PPcom  *I ;

    tic = pproj_timer () ;

    /* some initializations */
    status = PPROJ_STATUS_OK ;
    one = (PPINT) 1 ;
    Parm = ppdata->Parm ;
    Stat = ppdata->Stat ;
    Stat->grad_tol = Parm->grad_tol ;

    /* if return_data is TRUE, then the ppcom structure for the problem
       will be returned in the priordata element of ppdata */
    int const return_data = Parm->return_data ;

    /* if use_prior_data is TRUE, then the initialization phase of
       pproj will be skipped and the solution process begins immediately
       using the priordata element of ppdata */
    int const use_prior_data = Parm->use_prior_data ;

    if ( use_prior_data )
    {
        if ( ppdata->priordata == NULL )
        {
            status = PPROJ_MISSING_PRIOR_DATA ;
            if ( Parm->PrintStatus )
            {
                Stat->status = status ;
                pproj_print_status (ppdata) ;
            }
            return (status) ;
        }
        I = ppdata->priordata ;
    }
    else /* user does not provide prior data structure so create one */
    {
        I = (PPcom *) pproj_malloc (&status, one, sizeof (PPcom)) ;
        if ( status == PPROJ_OUT_OF_MEMORY )
        {
            if ( Parm->PrintStatus )
            {
                Stat->status = status ;
                pproj_print_status (ppdata) ;
            }
            return (status) ;
        }
        /* if the user wants ppcom, then store I in the ppcom argument */
        if ( return_data )
        {
            ppdata->priordata = I ;
        }
    }

    /* I now exists, either it was created or the user provided it */
    I->Parm = Parm ;
    I->Stat = Stat ;

    if ( Parm->PrintParm )
    {
        pproj_print_parm (ppdata) ;
    }

    int const PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel )
    {
        printf ("START PPROJ\n") ;
    }

    /* grab the problem info */
    PPINT   const     nrow = ppdata->nrow ;
    PPINT   const     ncol = ppdata->ncol ;
    PPINT   const    nsing = ppdata->nsing ;
    PPINT   const      *Ap = ppdata->Ap ;
    PPINT   const      *Ai = ppdata->Ai ;
    PPFLOAT const      *Ax = ppdata->Ax ;
    int     const loExists = (ppdata->lo == NULL) ? FALSE : Parm->loExists ;
    int     const hiExists = (ppdata->hi == NULL) ? FALSE : Parm->hiExists ;

    /* if the linear constraint is vacuous, the projection is trivial */
    if ( ((nrow == 0) || (Ap == NULL) || (Ax == NULL) || (Ai == NULL))
                      || (Ap [ncol] == 0) )
    {
        /* If there are no linear inequalities, then the projection is simply
           truncation. */
        PPFLOAT            *x = ppdata->x ;
        PPFLOAT const      *y = ppdata->y ;
        PPFLOAT const     *lo = ppdata->lo ;
        PPFLOAT const     *hi = ppdata->hi ;
        PPFLOAT const *singlo = ppdata->singlo ;
        PPFLOAT const *singhi = ppdata->singhi ;
        PPFLOAT const  *singc = ppdata->singc ;
        for (j = 0; j < ncol; j++)
        {
            t = y [j] ;
            if      ( loExists && (t < lo [j]) ) t = lo [j] ;
            else if ( hiExists && (t > hi [j]) ) t = hi [j] ;
            x [j] = t ;
        }
        if ( nsing )
        {
            PPFLOAT *xncol = x+ncol ;
            for (j = 0; j < nsing; j++)
            {
                if      ( singc [j] > PPZERO )      xncol [j] = singlo [j] ;
                else if ( singc [j] < PPZERO )      xncol [j] = singhi [j] ;
                else
                {
                    if      ( singlo [j] > PPZERO ) xncol [j] = singlo [j] ;
                    else if ( singhi [j] < PPZERO ) xncol [j] = singhi [j] ;
                    else                            xncol [j] = PPZERO ;
                }
            }
        }
   
        status = PPROJ_SOLUTION_FOUND ;
        pproj_wrapup (status, TRUE, ppdata, &I) ;
        return (status) ;
    }

    int const start_guess = Parm->start_guess ;
    if ( ((start_guess == 4) || (start_guess == 2)) && (use_prior_data==FALSE) )
    {
        status = PPROJ_START_GUESS_NEEDS_PRIOR_DATA ;
        pproj_wrapup (status, TRUE, ppdata, &I) ;
        return (status) ;
    }

    /* if the user provides the prior data and use_prior_data = TRUE,
       then extract work and prob structures */
    if ( use_prior_data )
    {
        W = I->Work ;
        W->x = ppdata->x ;
        Prob = I->Prob ;
        Stat->nprox = 0 ;

        if ( !Parm->LP )
        {
            /* copy Prob->b, Prob->lo, and Prob->hi to work structure since
               these were constantly updated during the previous run */
            pproj_copyx (W->b, Prob->b, nrow) ; 
            if ( loExists == TRUE ) pproj_copyx (W->lo, Prob->lo, ncol) ;
            else                    W->lo = NULL ;
            if ( hiExists == TRUE ) pproj_copyx (W->hi, Prob->hi, ncol) ;
            else                    W->hi = NULL ;

            /* store y and permute if cholmod is used */
            PPFLOAT *y = ppdata->y ;
        
            if ( Parm->cholmod == TRUE )
            {
                /* note that singc = y1 is not permuted, only y0 */
                if ( Parm->permute == TRUE )
                {
                    /* y should be ordered according to the column permutation
                       found in initlevels */
                    for (j = 0; j < ncol; j++)
                    {
                        Prob->y [j] = y [Prob->colperm [j]] ;
                    }
                }
                else
                {
                    pproj_copyx (Prob->y, y, ncol) ;
                }
            }
            else
            {
                Prob->y = y ; /* for iterative methods, no permutation of cols*/
            }
        }
    }
    else /* user does not provide prior data */
    {
        /* create prob structure */
        Prob = (PPprob *) pproj_malloc (&status, one, sizeof (PPprob)) ;

        /* create work structure */
        W = (PPwork *) pproj_malloc (&status, one, sizeof (PPwork)) ;
        W->return_data = return_data ;

        /* save the user's row_sing (used in final inversion) */
        W->user_row_sing = ppdata->row_sing ;

        /* create check structure */
        I->Check = (PPcheck *) pproj_malloc (&status, one, sizeof (PPcheck)) ;

        if ( Parm->cholmod == TRUE )
        {
            /* cholmod common */
            W->cmm = (cholmod_common *) pproj_malloc (&status, one,
                                                   sizeof (cholmod_common)) ;
        }

        /* check if any of the malloc's failed */
        if ( status == PPROJ_OUT_OF_MEMORY )
        {
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }

        I->Prob = Prob ;
        I->Work = W ;
        Prob->nsing = nsing ;
        W->loExists = loExists ;
        W->hiExists = hiExists ;
        W->x        = ppdata->x ;
        W->lambda   = ppdata->lambda ;
        /* If the user does not provide lambda, then allocate it and return it
           to the user in ppdata. In ppdata, also store pointer to any
           allocated array in lambda_created. pproj_terminate will free an
           array allocated by pproj. */
        if ( W->lambda == NULL )
        {
            W->lambda = ppdata->lambda = ppdata->lambda_created =
                    (PPFLOAT *) pproj_malloc (&status, nrow, sizeof (PPFLOAT)) ;
        }
        else ppdata->lambda_created = NULL ;

        if ( W->x == NULL )
        {
            W->x = ppdata->x = ppdata->x_created =
                    (PPFLOAT *) pproj_malloc (&status, ncol, sizeof (PPFLOAT)) ;
        }
        else ppdata->x_created = NULL ;

        /* initialize work arrays and fill-reducing ordering for user's data*/
        status = pproj_init (I, ppdata) ;
        if ( status != PPROJ_STATUS_OK )
        {
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }
    }

    /* by default, we do not need to factor the matrix; we only need
       to factor it if Parm->getfactor = TRUE and the solution was found */
    W->getfactor = FALSE ;

    /* stop_in_hotchol becomes TRUE if the code terminates in hot_chol.
       Hence, there was no change made to any previously computed
       factorization. */
    W->stop_in_hotchol = FALSE ;

    /* initialize the count on the number of times there was a large
       relative error in the solution of the dasa linear system */
    W->factor_not_OK = 0 ;

    if ( Parm->stop_condition == 2 )
    {
        W->ymax = pproj_max (ppdata->y, ncol) ;
    }

    W->shiftl_is_zero = TRUE ; /* it switches to false after proximal update */

    /* if using prior data and either the start_guess is 0 or
       sigma changed during the prior run, then we discard prior factorization
       and start from scratch */
    if ( use_prior_data && ((start_guess == 0) || (W->sigma != W->start_sigma)))
    {
        /* Any previous factorization is ignored */
        W->fac = FALSE ;
        W->nrowdel = 0 ;
        W->nrowadd = 0 ;
        W->ncoldel = 0 ;
        W->ncoladd = 0 ;
        W->nd      = 0 ;
        pproj_initi (W->RowmodFlag, (PPINT) EMPTY, nrow) ;
        pproj_initi (W->ColmodFlag, (PPINT) EMPTY, ncol) ;
        k = ncol + Prob->ni + nsing + 1 ;
        k = PPMAX (k, nrow) ;
        pproj_initi (W->ns, (PPINT) EMPTY, k) ;
        if ( W->sigma != W->start_sigma )
        {
            W->sigma = W->start_sigma ;
            W->Totsigma = W->sigma + W->Asigma ;
        }
    }

    PPFLOAT *lambda = W->lambda ;
    /* set up the starting guess */
    if ( start_guess == 0 )
    {
        /* lambda = 0 and shift_l = 0 */
        pproj_initx (lambda, PPZERO, nrow) ;
        pproj_initx (W->shift_l, PPZERO, nrow) ;

    }

    else if ( start_guess == 1 )
    {
        /* user provided input argument lambda is shift_l and the starting
           guess for the dual problem is lambda = 0 */
        if ( ppdata->lambda == NULL )
        {
            status = PPROJ_START_GUESS_IS_1_BUT_LAMBDA_NULL ;
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }
        pproj_initx (lambda, PPZERO, nrow) ;
        if ( Parm->permute == TRUE )
        {
            for (i = 0; i < nrow; i++)
            {   
                /* apply row perm and store lambda in shift_l */
                W->shift_l [i] = ppdata->lambda [Prob->rowperm [i]] ;
            }
        }
        else /* no perm */
        {
            pproj_copyx (W->shift_l, ppdata->lambda, nrow) ;
        }
        W->shiftl_is_zero = FALSE ;
    }
    else if ( start_guess == 2 )
    {
        /* use the bound structure from a prior run to generate a
           starting guess by solving a linear system (assumes that
           cholmod is used) */
        if ( Parm->cholmod == FALSE )
        {
            status = PPROJ_START_GUESS_IS_2_BUT_CHOLMOD_FALSE ;
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }
        /* The matrix factorization must be up-to-date; otherwise, we
           use W->lambda for the starting guess. */
        RLinkUp = W->RLinkUp ;
        if ( (W->fac == TRUE) &&
             (W->nrowadd + W->nrowdel + W->ncoladd + W->ncoldel == 0) &&
             (RLinkUp [nrow] < nrow)) /* if all rows drop, no equation */
        {
            if ( PrintLevel > 0 )
            {
                printf ("pproj: do solve to obtain starting guess\n") ;
            }
            /* set up equation (7.1) of pproj paper: A*A'*lambda = b - A*y
               where A corresponds to free columns and active rows
               in the original matrix, b is bl or bu for active rows,
               and y corresponds to free columns */
            pproj_initx (lambda, PPZERO, nrow) ;
            /* lambda = right side initially,
                      = solution shift_l after the solve */
            PPFLOAT const *B = Prob->b ;
            /* build rhs in lambda */
            if ( nsing == 0 )
            {
                PPFLOAT const *bl = Prob->bl ;
                PPFLOAT const *bu = Prob->bu ;
                for (i = RLinkUp [nrow]; i < nrow; i = RLinkUp [i])
                {
                    j = W->ir [i] ;
                    if ( j == 0 )
                    {
                        lambda [i] = B [i] ;
                    }
                    else if ( j > 0 ) /* for active rows j <= nsingni */
                    {
                        lambda [i] = bu [j] ;
                    }
                    else /* j < 0 */
                    {
                        lambda [i] = bl [-j] ;
                    }
                }
            }
            else /* nsing > 0 */
            {
                PPFLOAT const    *Singhi = Prob->singhi ;
                PPFLOAT const    *Singlo = Prob->singlo ;
                PPINT   const  *row_sing = Prob->row_sing ;
                PPINT   const *row_sing1 = row_sing+1 ;
                for (i = RLinkUp [nrow]; i < nrow; i = RLinkUp [i])
                {
                    /* adjust b for singletons */
                    t = B [i] ;
                    if ( W->ir [i] <= nsing ) /* active, singletons at bounds*/
                    {
                        j = row_sing [i] ;
                        PPINT const q  = W->slo [i] ;
                        PPINT const q1 = row_sing1 [i] ;
                        if ( q ) /* singletons at lower bound exist */
                        {
                           for (; j <= q; j++) t += Singlo [j] ;
                        }
                           for (; j < q1; j++) t += Singhi [j] ;
                        lambda [i] = t ; /* stored right side in lambda */
                    }
                }
            }
            for (j = 0; j < ncol; j++)
            {
                if ( W->ib [j] == 0 )
                {
                    t = Prob->y [j] ;
                }
                else if ( W->ib [j] < 0 )
                {
                    t = Prob->lo [j] ;
                }
                else
                {
                    t = Prob->hi [j] ;
                }
                if ( t != PPZERO )
                {
                    k = Prob->Ap [j] ;
                    l = k + Prob->Anz [j] ;
                    for (; k < l; k++)
                    {
                        lambda [Prob->Ai [k]] -= t*Prob->Ax [k] ;
                    }
                }
            }
            RLinkDn = W->RLinkDn ;
            pproj_lsol (W->L, lambda, RLinkUp [nrow], nrow, RLinkUp) ;
            i = RLinkUp [nrow] ;
            /* momentarily set the initial RLinkDn to -1, this simplifies
               indexing in dltsolve */
            RLinkDn [i] = -1 ;
            j = RLinkDn [nrow] ;
            pproj_dltsol (W->L, lambda, lambda, j, i, RLinkDn) ;
            RLinkDn [i] = nrow ; /* restore RLinkDn */
            /* At this point, we have computed an approximation based on
               the bound structure of the prior solution and stored it in
               lambda = W->lambda. */
            pproj_initx (W->shift_l, PPZERO, nrow) ;
        }
        else /* the prior solution stored in W->lambda is start guess */
        {
            if ( PrintLevel > 0 )
            {
                printf ("pproj: use prior solution for starting guess\n") ;
            }
            /* Apply the row perm to the start guess */
            if ( Parm->permute == TRUE )
            {
                for (i = 0; i < nrow; i++)
                {   
                    W->shift_l [i] = lambda [Prob->rowperm [i]] ;
                }
                pproj_copyx (lambda, W->shift_l, nrow) ;
                pproj_initx (W->shift_l, PPZERO, nrow) ;
            }
            else /* no perm needed, use lambda in W->lambda and shift_l = 0 */
            {
                pproj_initx (W->shift_l, PPZERO, nrow) ;
            }
        }
    }
    else if ( start_guess == 3 )
    {
        /* The starting guess is the lambda input argument and shift_l = 0 */
        if ( ppdata->lambda == NULL )
        {
            status = PPROJ_START_GUESS_IS_3_BUT_LAMBDA_NULL ;
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }
        if ( Parm->permute == TRUE )
        {
            for (i = 0; i < nrow; i++)
            {   
                W->shift_l [i] = ppdata->lambda [Prob->rowperm [i]] ;
            }
            pproj_copyx (lambda, W->shift_l, nrow) ;
            pproj_initx (W->shift_l, PPZERO, nrow) ;
        }
        else /* no perm needed */
        {
            if ( (use_prior_data && !W->shiftl_is_zero) || !use_prior_data )
            {
                pproj_initx (W->shift_l, PPZERO, nrow) ;
            }
        }
    }
    else if ( start_guess == 4 )
    {
        /* The starting guess is W->lambda and shift_l = 0 */
        if ( (use_prior_data && !W->shiftl_is_zero) || !use_prior_data )
        {
            pproj_initx (W->shift_l, PPZERO, nrow) ;
        }
    }

    Stat->initialize += pproj_timer () - tic ;

#ifndef NDEBUG
    /* check that ineq_row corresponds to the strict inequalities in the
       original matrix */
    if ( (Parm->cholmod == TRUE) && (Parm->use_prior_data == FALSE) )
    {
        for (k = 1; k <= Prob->ni; k++)
        {
            i = Prob->rowperm [Prob->ineq_row [k]] ;
            if ( (ppdata->bl != NULL) && (ppdata->bl [i] != Prob->bl [k]) )
            {
                pproj_error (-1, __FILE__, __LINE__,
                "bl not permuted according to rowperm\n") ;
            }
            if ( (ppdata->bu != NULL) && (ppdata->bu [i] != Prob->bu [k]) )
            {
                pproj_error (-1, __FILE__, __LINE__,
                "bu not permuted according to rowperm\n") ;
            }
        }
    }
#endif

    tic = pproj_timer () ;
    if ( Parm->use_startup )
    {
        if ( use_prior_data && (start_guess != 0) )
        {
            status = pproj_hotchol (I) ;
        }
        else /* use phase1 to obtain a starting guess */
        {
            status = pproj_phase1 (I) ;
        }
        Stat->phase1 += pproj_timer () - tic ;
        if ( status == PPROJ_SOLUTION_FOUND )
        {
            if ( (Parm->getfactor == FALSE) || (W->fac == TRUE) ||
                 (nrow == W->RLinkUp [nrow]) )
            {
                /* if pproj is not being called from the LP solve,
                   then invert row and column permutations */
                if ( !Parm->LP ) pproj_invert (I) ;
                pproj_wrapup (status, FALSE, ppdata, &I) ;
                return (status) ;
            }
        }
        else if ( status == PPROJ_OPTIMAL_COST_IS_MINUS_INFINITY )
        {
            pproj_wrapup (status, TRUE, ppdata, &I) ;
            return (status) ;
        }
    }
    else
    {
        status = PPROJ_TOLERANCE_NOT_MET ;
#ifndef NDEBUG
        /* save dual objective but do not check for increase */
        pproj_check_dual (I, NULL, "at startup of pproj", TRUE, FALSE);
#endif
    }

    /* Using the starting guess obtained in phase1, we now compute
       the projection of y onto the polyhedron. To facilitate the
       evaluation of the dual function, we make a change of variables
       x = x0 + z where x0 is a fixed point chosen to simplify the
       evaluation of the dual function.  After this translation, the
       dual function becomes

       (T)     L_R(lambda) = inf {.5||z + x0 - y||^2 + lambda'(b0 - Az) :
                                lo0 <= z <= hi0,  bl <= b <= bu}
                               -.5*sigma||lambda - shift_l||^2

       where b0 = b - A*x0, lo0 = lo - x0, and hi0 = hi - x0.

       The unconstrained minimizer x of the original Lagrangian before the
       translation is x(lambda) = y + A'lambda. x0 is chosen as follows:

           if x(lambda)_j < lo_j, then x0_j = lo_j,
           if x(lambda)_j > hi_j, then x0_j = hi_j,
           otherwise                   x0_j = (y + A'lambda)_j (j in F)

       After making this translation, the constrained minimizer of the
       Lagrangian (T) is z(lambda) = 0. Throughout the rest of the code,
       the variable x is really x0. z does not appear explicitly since
       it is readily computed. It is given by

           z(lambda) = mid (lo0, x(lambda) - x0, hi0),

       where mid is the componentwise operator which is the median (or middle
       of the 3 components).

       We also perform a translation in lambda. We express lambda as the
       sum of three vectors dlambda + lambda + shift_l, where shift_l is
       the proximal shift variable.  Both shift_l and lambda are fixed
       during the iteration of dasa, while dlambda is the variable that
       is being optimized over. Initially, dlambda = 0.  b0 above corresponds
       to the b array of the code.  The array c in the code stores
       the expression (y + A'lambda) - x0 which is contained in z(lambda).
       Thus cF = 0 initially by its definition above. If x(lambda)_j < lo_j,
       then c_j < 0, and when c_j reaches 0, the j-th constraint
       z_j >= 0 changes to free. By defining b and c in this way,
       the implementation of the dual active set algorithm is simplified.
       In particular, when we minimize the dual function for a given
       choice of F and B, we need to solve the linear system

       (AF*AF'+ sigma I)dlambda = b - sigma lambda - AB*xB - AF*cF

       where c = y + A'*(lambda + shift_l). Note that lambda and shift_l
       are fixed and xB in the translated problem is 0. Thus as indices
       move from B to F, the only thing that changes on the right side
       is cF, which is often a sparse change to the right side. Also,
       the directional derivative of the dual function in the direction d is

       d'*[b - sigma*(lambda + dlambda) - AB*xB -AF*cF].

       Again, xB = 0 in the translated problem so we only need to
       evaluate the product AF*cF since everything else in [ ... ]
       is fixed.  */
    it = 0 ;
    while ( status == PPROJ_TOLERANCE_NOT_MET )
    {
        it++ ;
        /* apply iteration of DASA, only free variables and drop rows */
        tic = pproj_timer () ;
        status = pproj_dasa (I) ;
        Stat->dasa += pproj_timer () - tic ;

        if ( (status == PPROJ_SSOR_NONASCENT) ||
             (status == PPROJ_SSOR_MAX_ITS) )
        {
            break ;
        }

        /* check the error and either add rows or bind variables */
        tic = pproj_timer () ;
        status = pproj_check_error (I) ;
        Stat->checkerr += pproj_timer () - tic ;

        if ( PrintLevel > 0 )
        {
            printf ("dasa iteration %i status = %i\n", it, status) ;
        }
        if ( status == PPROJ_PROX_UPDATE )
        {
            if ( Stat->nprox == Parm->nprox )
            {
                status = PPROJ_ERROR_DECAY_STAGNATES ;
            }
            else
            {
                if ( PrintLevel > 0 )
                {
                    printf ("proximal update\n") ;
                }
                tic = pproj_timer () ;
                status = pproj_prox_update (I) ;
                Stat->prox_update += pproj_timer () - tic ;
            }
        }
    }
    if ( Parm->cholmod )
    {
        cholmod_factor *L ;
        PPINT lnnz ;
        L = W->L ;
        lnnz = 0 ;
        if ( L != NULL )
        {
            PPINT *ir, *Lnz ;
            PPINT const nsingni = nsing + ppdata->ni ;
            Lnz = L->nz ;
            ir = W->ir ;
            for (i = 0; i < nrow; i++)
            {
                if ( ir [i] <= nsingni ) /* row is active */
                {
                    lnnz += Lnz [i] ;
                }
            }
        }
        Stat->lnnz = lnnz ;
    }
    /* if pproj is not being called from the LP solve,
       then invert row and column permutations, set lambda += shift_l */
    if ( !Parm->LP ) pproj_invert (I) ;
    pproj_wrapup (status, FALSE, ppdata, &I) ;
    return (status) ;
}

/* =========================================================================
   ============================== pproj_malloc =============================
   ========================================================================= */
void * pproj_malloc
(
    int *status,
    PPINT     n,
    int    size
)
{
    void *p ;

    if ( n > 0 )
    {
#ifdef MATLAB_MEX_FILE
        p = mxMalloc (n*size) ;
#else
        p = malloc (n*size) ;
#endif
    }
    else
    {
        return (NULL) ;
    }

    if ( p == NULL )
    {
        *status = PPROJ_OUT_OF_MEMORY ;
    }
    return (p) ;
}

/* =========================================================================
   ============================== pproj_free ===============================
   ========================================================================= */
void pproj_free
(
    void *p
)
{

#ifdef MATLAB_MEX_FILE
    mxFree (p) ;
#else
    free (p) ;
#endif

}

/* =========================================================================
   ============================== pproj_setup ==============================
   ========================================================================= */
PPdata * pproj_setup (void)
{
    int status ;
    PPdata *Data ;
    status = PPROJ_STATUS_OK ;
    Data       = (PPdata *) pproj_malloc (&status, 1, sizeof (PPdata)) ;
    Data->Stat = (PPstat *) pproj_malloc (&status, 1, sizeof (PPstat)) ;
    Data->Parm = (PPparm *) pproj_malloc (&status, 1, sizeof (PPparm)) ;
    if ( status == PPROJ_OUT_OF_MEMORY )
    {
        Data = NULL ;
        return (Data) ;
    }
    pproj_default (Data->Parm) ;
    Data->priordata       = NULL ;
    Data->Stat->updowns   = NULL ;
    Data->Stat->solves    = NULL ;
    Data->lambda          = NULL ;
    Data->x               = NULL ;
    Data->nrow            = 0 ;
    Data->ncol            = 0 ;
    Data->nsing           = 0 ;
    Data->ni              = -1 ;  /* => pproj computes # strict inequalities */
    Data->y               = NULL ;
    Data->Ap              = NULL ;
    Data->Ai              = NULL ;
    Data->Ax              = NULL ;
    Data->lo              = NULL ;
    Data->hi              = NULL ;
    Data->bl              = NULL ;
    Data->bu              = NULL ;
    Data->row_sing        = NULL ;
    Data->singlo          = NULL ;
    Data->singhi          = NULL ;
    Data->singc           = NULL ;

    /* the following are used internally when the code allocates memory */
    Data->lambda_created  = NULL ;
    Data->x_created       = NULL ;

    return (Data) ;
}

/* =========================================================================
   ============================== pproj_terminate ==========================
   ========================================================================= */
void pproj_terminate
(
    PPdata **DataHandle
)
{
    PPdata *Data ;
    Data = *DataHandle ;
    if ( Data->Stat->updowns != NULL ) pproj_free (Data->Stat->updowns) ;
    if ( Data->Stat->solves  != NULL ) pproj_free (Data->Stat->solves) ;
    if ( Data->lambda_created != NULL )
    {
        if ( Data->lambda_created == Data->lambda )
        {
            pproj_free (Data->lambda) ;
            Data->lambda_created = Data->lambda = NULL ;
        }
        else /* lambda was created by user */
        {
            pproj_free (Data->lambda_created) ;
            Data->lambda_created = NULL ;
        }
    }
    if ( Data->x_created != NULL )
    {
        if ( Data->x_created == Data->x )
        {
            pproj_free (Data->x) ;
            Data->x_created = Data->x = NULL ;
        }
        else /* x was created by user */
        {
            pproj_free (Data->x_created) ;
            Data->x_created = NULL ;
        }
    }
    pproj_free (Data->Stat) ;
    pproj_free (Data->Parm) ;
    if ( Data->priordata != NULL )
    {
        pproj_freeAll (&(Data->priordata)) ;
    }
    pproj_free (Data) ;
}

/* ========================================================================== */
/* === pproj_KKTerror.c ===================================================== */
/* ========================================================================== */

/*  Determine KKT error in a solution to the polyhedral projection problem
          min 0.5||x0 - y0|| - y1'x1

             subject to  lo <= x <= hi,  bl <= Ax <= bu

          where A = [A0 -A1], x' = [x0' x1'], || . || is the Euclidean
          norm and the A1 part of A is a matrix for which each column
          is zero except for a single nonzero entry. The y1 and A1 data
          could be vacuous.  When y1 and A1 exist, it is required that
          bl = bu, the nonzero elements of A1 are all 1, and the
          elements of y1 corresponding to the nonzeros in any row of A1
          are all  distinct.

    Input to the routine is a ppdata structure containing the computed
    projection x and a Lagrange multiplier lambda associated with the
    constraint b - Ax = 0. The Lagrangian for the problem is

        L (lambda, x, b) = 0.5||x0-y0||^2 - y1'x1 + lambda'(b - Ax).

    The dual function is defined by

        L (lambda) = inf { L(lambda, x, b) : lo <= x <= hi, bl <= b <= bu }.

    To estimate the error in the KKT conditions, we compute two things:

    1. The 1-norm of the computed solution and the 1-norm difference
       between the computed x and the minimizers of the dual function
       for the given lambda.
    2. The sup-norm distance from 0 to the subdifferential of the dual
       function.

    lambda is optimal if #2 vanishes.
    x is optimal if both #1 and #2 vanish.

    For a given lambda, the minimizer over x0 is given by

        x0_j (lambda) = mid {lo_j, c_j, hi_j}, where c = y0 + A0'lambda.

    Here mid {u, v, w} is the median (or middle) of u, v, and w.
    If (A1){ij} = 1 and the other elements in column j are zero, then the
    the minimizer over x1 is given by
                         -
                        |     lo1_j      if lambda_i > y1_j
        x1_j (lambda) = |     hi1_j      if lambda_i < y1_j
                        | [lo1_j, hi1_j] if lambda_i = y1_j
                         -

    This formula also yields the minimizing b with the following adjustments:
    x1 -> b, hi1 -> bu, lo1 ->bl, and y1 -> 0. That is,
                        -
                       |    bl_i      if lambda_i > 0,
        b_i (lambda) = |    bu_i      if lambda_i < 0,
                       | [bl_i, bu_i] if lambda_i = 0.
                        -
    The i-th component of the subdifferential g_i is given by

        g_i = b_i (lambda) + x1_j (lambda) - (A0*x0 (lambda))_i
    
    The minimizing x0 and x1 are given by the formulas above.
    In order to assess the relative subdifferential error, we also
    evaluate the sup-norm of absAx where absAx_i = sum_j |a_{ij}*x_j|
    and x_j is the computed solution */

PPFLOAT pproj_KKTerror /* returns the largest of the primal and dual errors */
(
    PPFLOAT   *errg, /* sup norm dist of g to 0 relative to sup-norm of absAx
                        (only returned when not NULL) */
    PPFLOAT   *errx, /* 1 norm relative difference of x and x(lambda)
                        (only returned when not NULL) */
    PPFLOAT  *absAx, /* sup norm of absAx (only returned when not NULL) */
    PPdata  *ppdata  /* problem data and computed solution */
)
{
    int status ;
    PPINT dropped, i, j, p, p0, q ;
    PPFLOAT xj, t, err, gb, gl, gu, pertx, pertb, normx, absAxi, absAxSup,
           *AtimesX, *absAtimesX, *work ;

    /* grab the problem info */
    PPFLOAT const         *x = ppdata->x ;
    PPFLOAT const    *lambda = ppdata->lambda ;
    PPFLOAT const         *y = ppdata->y ;
    PPFLOAT const        *bl = ppdata->bl ;
    PPFLOAT const        *bu = ppdata->bu ;
    PPFLOAT const        *lo = ppdata->lo ;
    PPFLOAT const        *hi = ppdata->hi ;
    PPINT   const       nrow = ppdata->nrow ;
    PPINT   const       ncol = ppdata->ncol ;
    PPINT   const      nsing = ppdata->nsing ;
    PPINT   const  *row_sing = ppdata->row_sing ;
    PPINT   const        *Ap = ppdata->Ap ;
    PPINT   const        *Ai = ppdata->Ai ;
    PPFLOAT const        *Ax = ppdata->Ax ;
    PPFLOAT const    *singlo = ppdata->singlo ; /* lo for x1 */
    PPFLOAT const    *singhi = ppdata->singhi ; /* hi for x1 */
    PPFLOAT const     *singc = ppdata->singc ;  /* y1 */
    PPparm  const      *Parm = ppdata->Parm ;
    int     const   loExists = (lo == NULL) ? FALSE : Parm->loExists ;
    int     const   hiExists = (hi == NULL) ? FALSE : Parm->hiExists ;
    int     const   blExists = (bl == NULL) ? FALSE : TRUE ;
    int     const   buExists = (bu == NULL) ? FALSE : TRUE ;
    int     const PrintLevel = Parm->PrintLevel ;

    i = (Ap == NULL) || (Ai == NULL) || (Ax == NULL) || (nrow <= 0) ;
    int const Aexists = ( i ) ? FALSE : TRUE ;

    /* dualval = PPZERO ;*/
    pertx = PPZERO ;
    pertb = PPZERO ;
    normx = PPZERO ;
    absAxSup = PPZERO ;
    status = PPROJ_STATUS_OK ;
    work = pproj_malloc (&status, 2*nrow, sizeof (PPFLOAT)) ;
    if ( status == PPROJ_OUT_OF_MEMORY )
    {
        printf ("ppdata->nrow: %ld not enough memory in routine "
                "pproj_KKTerror\n", (LONG) nrow) ;
        return (PPZERO) ;
    }
    AtimesX    = work ; work += nrow ;
    absAtimesX = work ; work += nrow ;
    pproj_initx (AtimesX, PPZERO, nrow) ;
    pproj_initx (absAtimesX, PPZERO, nrow) ;
    p = 0 ;
    for (j = 0; j < ncol; j++)
    {
        /* form x0_j (denoted xj below) */
        xj = y [j] ;
        if ( Aexists )
        {
            p0 = p ;
            q = Ap [j+1] ;
            for (; p < q; p++)
            {
                xj += lambda [Ai [p]]*Ax [p] ;
            }
        }
        if ( loExists && (xj < lo [j]) )
        {
            xj = lo [j] ;
        }
        else if ( hiExists && (xj > hi [j]) )
        {
            xj = hi [j] ;
        }
        pertx += fabs (xj - x [j]) ; /* x [j] = computed solution */
        normx += fabs (x [j]) ;
        /* dualval += .5*(xj - y [j])*(xj - y [j]) ;*/
        if ( Aexists )
        {
            p = p0 ;
            for (; p < q; p++)
            {
                PPINT ai = Ai [p] ;
                AtimesX [ai] += xj*Ax [p] ;
                absAtimesX [ai] += fabs (x [j]*Ax [p]) ;
            }
        }
    }
    if ( Aexists )
    {
        if ( nsing > 0 )
        {
            PPFLOAT lambdai ;
            PPFLOAT const *singx = x+ncol ; /* = x1 */
            p = 0 ;
            for (i = 0; i < nrow; i++)
            {
                q = row_sing [i+1] ;
                if ( p < q ) /* the row has column singletons */
                {
                    dropped = FALSE ; /* the row is active */
                    absAxi = absAtimesX [i] ;
                    gl = PPZERO ;
                    gu = PPZERO ;
                    gb = bl [i] - AtimesX [i] ;
                    for (; p < q; p++)
                    {
                        PPFLOAT const xjcomputed = singx [p] ;/* computed x1 */
                        normx += fabs (xjcomputed) ;          /* update 1-norm*/
                        lambdai = lambda [i] ;
                        if ( lambdai > singc [p] )
                        {
                            xj = singlo [p] ;
                            gb += xj ;
                            absAxi += fabs (xj) ;
                            pertx += fabs (xj-xjcomputed) ; /* error in x1_j */
                        }
                        else if ( lambdai < singc [p] )
                        {
                            xj = singhi [p] ;
                            gb += xj ;
                            absAxi += fabs (xj) ;
                            pertx += fabs (xj-xjcomputed) ; /* error in x1_j */
                        }
                        else /* y1_j = lambda_i, equation dropped */
                        {
                            dropped = TRUE ;
                            /* checked if xjcomputed violated bounds */
                            if ( xjcomputed < singlo [p] )
                            {
                                pertx += fabs (xjcomputed -singlo[p]);
                            }
                            else if ( xjcomputed > singhi [p] )
                            {
                                pertx += fabs (xjcomputed -singhi[p]);
                            }
                            gu += singhi [p] ;
                            gl += singlo [p] ;
                        }
                    }
                    /* Determine distance from subdifferential to 0.
                       If the equation is strictly satisfied, then do not
                       include absAxi in absAxSup */
                    if ( dropped == FALSE ) /* row is active */
                    {
                        if ( pertb < fabs (gb) ) pertb = fabs (gb) ;
                        if ( absAxSup < absAxi ) absAxSup = absAxi ;
                    }
                    else                   /* row was dropped */
                    {
                        if ( (t = gb - gu) > PPZERO )
                        {
                            if ( pertb < t ) pertb = t ;
                            if ( absAxSup < absAxi ) absAxSup = absAxi ;
                        }
                        else if ( (t = gl - gb) > PPZERO )
                        {
                            if ( pertb < t ) pertb = t ;
                            if ( absAxSup < absAxi ) absAxSup = absAxi ;
                        }
                        /* If t <= 0, then the equation holds strictly and
                           absAxSup was not updated */
                    }
                    if ( PrintLevel > 1 )
                    {
                        if ( dropped == FALSE )
                        {
                            printf ("constraint row: %ld violation: %e\n",
                                    (LONG) i, fabs (gb)) ;
                        }
                        else
                        {
                            if ( t > PPZERO )
                            {
                                printf ("constraint row: %ld violation: %e\n",
                                        (LONG) i, t) ;
                            }
                        }
                    }
                }
                else /* no singletons in row */
                {
                    pertb += fabs (bl [i] - AtimesX [i]) ;
                    if ( absAtimesX [i] > absAxSup ) absAxSup = absAtimesX [i] ;
                    if ( PrintLevel > 1 )
                    {
                        printf ("constraint row: %ld violation: %e\n",
                                (LONG) i, fabs (bl [i] - AtimesX [i])) ;
                    }
                }
            }
        }
        else /* no column singletons in problem */
        {
            absAxSup = PPZERO ;
            pertb = PPZERO ;
            for (i = 0; i < nrow; i++)
            {
                if ( lambda [i] < PPZERO )
                {
                    if ( buExists && (pertb < fabs (bu [i] - AtimesX [i])) )
                    {
                        pertb = fabs (bu [i] - AtimesX [i]) ;
                    }
                    if ( absAxSup < absAtimesX [i] ) absAxSup = absAtimesX [i] ;
                }
                else if ( lambda [i] > PPZERO )
                {
                    if ( blExists && (pertb < fabs (bl [i] - AtimesX [i])) )
                    {
                        pertb = fabs (bl [i] - AtimesX [i]) ;
                    }
                    if ( absAxSup < absAtimesX [i] ) absAxSup = absAtimesX [i] ;
                }
                else /* dropped equation */
                {
                    /* only include in absAxSup if equation violated */
                    if ( blExists && ((t = bl [i] - AtimesX [i]) > PPZERO) )
                    {
                        if ( pertb < t )                 pertb = t ;
                        if ( absAxSup < absAtimesX [i] ) absAxSup=absAtimesX[i];
                    }
                    else if ( buExists && (t = bu [i] - AtimesX [i] < PPZERO) )
                    {
                        if ( pertb < -t )                pertb = -t ;
                        if ( absAxSup < absAtimesX [i] ) absAxSup=absAtimesX[i];
                    }
                }
                if ( PrintLevel > 1 )
                {
                    t = PPZERO ;
                    if ( blExists && (AtimesX [i] < bl [i]) )
                    {
                        t = bl [i] - AtimesX [i] ;
                    }
                    else if ( (bu != NULL) && (AtimesX [i] > bu [i]) )
                    {
                        t = AtimesX [i] - bu [i] ;
                    }
                    if ( t > PPZERO )
                    {
                        printf ("constraint row: %ld violation: %e\n",
                                                                  (LONG) i, t) ;
                    }
                }
            }
        }
    }
    else
    {
        pertb = PPZERO ;
    }

    if ( absAxSup ) /* if norm not zero, compute relative error */
    {
        pertb /= absAxSup ;
    }
    if ( errg != NULL ) *errg = pertb ;

    if ( absAx != NULL ) *absAx = absAxSup ;

    if ( normx != PPZERO ) pertx /= normx ;
    if ( errx != NULL ) *errx = pertx ;

    /* return the largest error */
    err = PPMAX (pertx, pertb) ;
    pproj_free (AtimesX) ; /* this also frees absAtimesX */
    return (err) ;
}

/* ========================================================================== */
/* ====== pproj_error ======================================================= */
/* ========================================================================== */
/* when -g compiler option is used, prints line number of error */
void pproj_error
(
    int status,
    const char *file,
    int line,
    const char *message
)
{
    if (status < 0)
    {
        PRINTF ("file: %s line: %d status: %d %s\n",
                 file, line, status, message) ;
#ifdef MATLAB_MEX_FILE
        mexErrMsgTxt (message) ;
#else
        ASSERT (0) ;
        abort ( ) ;
#endif
    }
}

/* ========================================================================= */
/* === pproj_wrapup ======================================================== */
/* ========================================================================= */
/* Free memory allocated for PPcom structure */
/* ========================================================================= */
void pproj_wrapup
(
    int      status, /* termination status */
    int  fastreturn, /* T => return after printing status */
    PPdata  *ppdata,
    PPcom **Ihandle
)
{
    PPparm *Parm ;
    PPstat *Stat ;
    PPcom *I ;
    
    I = *Ihandle ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    Stat->status = status ;
    /* print message explaining status if requested */
    if ( Parm->PrintStatus )
    {
        pproj_print_status (ppdata) ;
    }
    if ( fastreturn ) return ;

    if ( Parm->PrintStat == TRUE )
    {
        pproj_print_stat (ppdata) ;
    }

    /* if the user does not want the PPcom structure, then free everything */
    if ( I->Work->return_data == FALSE )
    {
        pproj_freeAll (&I) ;
        ppdata->priordata = NULL ;
    }
    else /* otherwise, user wants PPcom, prepare for new run */
    {
        I->Work->chg_coor = 1 ;
        I->Work->chg_ssor0 = 1 ;
        I->Work->chg_ssor1 = 1 ;
        I->Work->chg_sparsa = 1 ;
        I->Work->sparsaOK = TRUE ;
    }
}

/* ========================================================================= */
/* === pproj_freeAll ======================================================= */
/* ========================================================================= */
/* Free memory allocated for PPcom structure */
/* ========================================================================= */
void pproj_freeAll
(
    PPcom **Ihandle
)
{
    PPcom     *I ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

    I = *Ihandle ;
    Parm = I->Parm ;
    Prob = I->Prob ;
    W = I->Work ;
    PPINT const nsing = Prob->nsing ;
    pproj_free (I->Check) ; /* created in pproj */

    /* allocations specific to update/downdates */
    if ( Parm->cholmod )
    {
        /* pproj */
        CHOLMOD (free_factor) (&(W->L), W->cmm) ;
        CHOLMOD (free_work) (W->cmm) ;
        pproj_free (W->cmm) ;
        pproj_free (Prob->rowperm) ;
        pproj_free (Prob->colperm) ;
        pproj_free (Prob->Anz) ;
        pproj_free (Prob->Ap) ;
        pproj_free (Prob->Ai) ;
        pproj_free (Prob->Ax) ;
        pproj_free (Prob->y) ;
        if ( W->loExists == TRUE )
        {
            pproj_free (Prob->lo) ;
        }
        if ( W->hiExists == TRUE )
        {
            pproj_free (Prob->hi) ;
        }

        /* init */
        if ( nsing )
        {
            pproj_free (Prob->row_sing) ;
            pproj_free (Prob->singc) ;
            pproj_free (Prob->singlo) ;
            pproj_free (Prob->singhi) ;
        }
        pproj_free (Prob->bl) ;
        pproj_free (Prob->bu) ;
        pproj_free (W->changeRHS) ;
        pproj_free (W->newrow) ;
        pproj_free (W->Cp) ;
        pproj_free (W->Cnz) ;
        pproj_free (W->A) ;
        pproj_free (W->AFT) ;

        pproj_free (W->Kids) ;
        pproj_free (W->nkids) ;
        pproj_free (W->parent) ;
        pproj_free (W->Kp) ;
        pproj_free (W->depth) ;
        pproj_free (W->leftdesc) ;
        pproj_free (W->col_start) ;
        pproj_free (W->sol_start) ;
        pproj_free (W->row_start) ;
        pproj_free (W->sol_to_blk) ;
        pproj_free (W->joblist) ;
        pproj_free (W->kidsleft) ;
        pproj_free (W->jobcols) ;
        pproj_free (W->jobrows) ;
        pproj_free (W->Rstart) ;
        pproj_free (W->Rend) ;
    }
    else
    {
#ifndef NDEBUG
        pproj_free (W->leftdesc) ;
        pproj_free (W->col_start) ;
        pproj_free (W->row_start) ;
#endif
    }

    /* allocations applying to both iterative methods and update/downdates */

    if ( nsing )
    {
        pproj_free (W->slo) ;
        pproj_free (W->shi) ;
    }
    pproj_free (Prob->ineq_row) ;
    pproj_free (Prob->b) ;
    pproj_free (Prob) ;

    pproj_free (W->ATp) ;
    pproj_free (W->ATi) ;
    pproj_free (W->ATx) ;
    pproj_free (W->AFTp) ;
    pproj_free (W->AFTnz) ;
    pproj_free (W->AFTi) ;
    pproj_free (W->AFTx) ;
    pproj_free (W->dlambda) ;
    pproj_free (W->lambda_tot) ;
    pproj_free (W->ns) ;
    pproj_free (W->RowmodList) ;
    pproj_free (W->RowmodFlag) ;
    pproj_free (W->ColmodList) ;
    pproj_free (W->ColmodFlag) ;
    pproj_free (W->dropped) ;
    pproj_free (W->F) ;
    pproj_free (W->ib) ;
    pproj_free (W->shift_l) ;
    pproj_free (W->b) ;
    pproj_free (W->c) ;
    pproj_free (W->cold) ;
    if ( W->loExists == TRUE )
    {
        pproj_free (W->lo) ;
    }
    if ( W->hiExists == TRUE )
    {
        pproj_free (W->hi) ;
    }
    pproj_free (W->D) ;
    pproj_free (W->RLinkUp) ;
    pproj_free (W->RLinkDn) ;
    pproj_free (W->SLinkUp) ;
    pproj_free (W->SLinkDn) ;
    pproj_free (W->ir) ;

    pproj_free (W->lstart) ;
    pproj_free (W->ustart) ;
    pproj_free (W->arrayi) ;
    pproj_free (W->arrayd) ;

    pproj_free (W) ;
    pproj_free (I) ;
}

/* ========================================================================= */
/* === pproj_check_error =================================================== */
/* ========================================================================= */
/* Check the error at the current dual iterate:

       errdual = sup-norm of dual function gradient excluding the proximal
                 term.  If errdual is sufficiently small, then we are done.

       errls   = sup-norm of the residual of the linear system. With
                 exact arithmetic, this should be zero. That is, at the final
                 iteration, after free variables and dropping rows, we
                 solve a linear system.  errls is the sup-norm of
                 the residual for this linear system. This basically measures
                 the accumulated error in the update/downdate process.
                 If errls is too big, then the matrix will be refactored.
                 The variable lhs is used to accumulate the left side term
                 AF*AF'*dlambda, which works out to be AF*cF. Both lhs and
                 sigma*dlambda are subtracted from b to obtain the residual
                 vector. The error is relative to ||absAx||_sup.

       errprox = sup-norm of the dual function gradient including the proximal
                 term.  If errprox is sufficiently small, then we should
                 perform a proximal update. However, the proximal term
                 is chosen so small, that a proximal update is not performed.

       colerr  = Max violation of bounds (if a violation is small enough
                 relative to the max violation, we keep the variable free)

       rowerr  = Max violation of inequality constraints (if a violation
                 for a row is small enough relative to the max violation,
                 the row remains dropped) */
/* ========================================================================= */
int pproj_check_error /* return status:
                             PPROJ_SOLUTION_FOUND
                             PPROJ_PROX_UPDATE
                             PPROJ_TOLERANCE_NOT_MET */
(
    PPcom *I
)
{
    PPINT  i, j, k, l, m, p, p0, q, ibj,
           nrowindex, ncolindex, row, Ll, Ul, Rl,
           prevblkL, prevblkU, Annz, ATnz, Lnnz, nactive,
           ncoldel, nrowdel, ncoladd, nrowadd, nf,
           *AFTp, *AFTi, *AFTnz,
           *ir, *ColmodFlag, *ColmodList, *RowmodFlag, *RowmodList,
           *ColIndex, *RowIndex, *F, *Lnz, *ns, *RLinkUp, *RLinkDn,
           *lstart, *ustart, *lLinkUp, *lLinkDn, *uLinkUp, *uLinkDn,
           *worki ;
    int blk, blks, return_chol, status, *ib, *sol_to_blk ;
    int const loExists = I->Work->loExists ;
    int const hiExists = I->Work->hiExists ;
    PPFLOAT cerr, s, t, errdual, errls, errprox, colerr, rowerr, normb,
            normx, ax, bi, newbi, cj, rowcutoff, colcutoff,
            z, tic, bi_noprox, norm_l,
            *b, *c, *AFTx, *D, *lambda, *dlambda, *lhs,
            *lo, *hi, *RowErri, *x, *workd ;

    PPstat *Stat ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;
    Parm = I->Parm ;
    int const PrintLevel = Parm->PrintLevel ;
    PPINT const cholmod = Parm->cholmod ;

#ifndef NDEBUG
    char *where ;
    I->Check->location = 5 ;
    where = "at start of check_err" ;
    pproj_checkF (I, where) ;
    pproj_checkD (I, where) ;
    pproj_checkb (I, where) ;
    pproj_check_modlist (I, where) ;
#endif

    tic = pproj_timer () ;
    Stat = I->Stat ;
    Prob = I->Prob ;
    W = I->Work ;

    /* sigma does not change */
    PPFLOAT const Asigma = W->Asigma ;
    PPFLOAT const sigma = W->sigma ;

    /* return_chol = TRUE if code returns from pproj_dasa with the chol */
    return_chol = W->return_chol ;

    /* PPprob */
    PPINT   const        *Ap = Prob->Ap ;
    PPINT   const        *Ai = Prob->Ai ;
    PPINT   const       *Anz = Prob->Anz ;
    PPFLOAT const        *Ax = Prob->Ax ;
    PPINT   const       ncol = Prob->ncol ;
    PPINT   const       nrow = Prob->nrow ;
    PPINT   const      nsing = Prob->nsing ;
    PPINT   const         ni = Prob->ni ;
    PPINT   const    nsingni = nsing + ni ;
    PPINT   const   nsingni1 = nsingni + 1 ;
    PPINT   const   nsingni2 = nsingni + 2 ;
    PPINT   const  *ineq_row = Prob->ineq_row ;
    PPINT   const  *row_sing = Prob->row_sing ;
    PPINT   const *row_sing1 = row_sing+1 ;
    PPFLOAT const        *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const        *bu = (nsing) ? Prob->singhi : Prob->bu ;
    PPFLOAT const   grad_tol = Parm->grad_tol ;
    PPINT               *slo = W->slo ;
    PPINT               *shi = W->shi ;

    /* Transpose of A */
    PPINT   const *ATp = W->ATp ;
    PPINT   const *ATi = W->ATi ;
    PPFLOAT const *ATx = W->ATx ;

    /* Transpose of AF */
    AFTp = W->AFTp ;
    AFTx = W->AFTx ;
    AFTi = W->AFTi ;
    AFTnz = W->AFTnz ;

    lambda = W->lambda ;
    dlambda = W->dlambda ;
    x = W->x ;

    /* ib [col] = +1 if column at upper bound
                  -1 if column at lower bound
                   0 if column is free */
    ib = W->ib ;

    /* ir [row] = 0       for an equality constraint
                = 1       for an active singleton row
                =  ineq # for an active inequality at upper bound
                = -ineq # for an active inequality at lower bound
                =  ineq # or singleton # + nsingni for a dropped constraint */
    ir = W->ir ;
    b = W->b ; /* the part of grad L (lambda) associated with bound variables */
    c = W->c ; /* y + A'lambda */
    F = W->F ; /* free indices */
    D = W->D ; /* diag of AF*AF' */
    ns = W->ns ; /* used in line search, points from index to break point # */
    lo = W->lo ; /* lower bounds on x */
    hi = W->hi ; /* upper bounds on x */

    /* ColmodFlag is empty if row not modified, otherwise points into
       ColmodList showing columns to modify*/
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;
    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;

    /* Links for active inequalities. lLinkUp points to the strict
       inequalities with b_i = bl_i while uLinkUp points to the strict
       inequalities with b_i = bu_i. Since only one of these can hold for
       each i, lLinkUp and uLinkUp can be stored in the same array */
    lLinkUp = W->SLinkUp ;
    lLinkDn = W->SLinkDn ;
    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;
    sol_to_blk = W->sol_to_blk ;

    /* Links for the active rows */
    RLinkUp = W->RLinkUp ;
    RLinkDn = W->RLinkDn ;

    /* lstart and ustart are associated with the inequalities that are
       strict.  For each block in the multilevel decomposition,
       lstart points to the first singleton at its lower bound while ustart
       points to the first singleton at it upper bound */
    lstart = W->lstart ;
    ustart = W->ustart ;

    blks = W->blks ; /* number of nodes (blocks) in the multilevel tree */

    /* work arrays used in checking error:

       lhs        - double nrow, grad L (lambda) (same space as RowErri)
       RowErri    - double ni, amount that currently dropped inequalities
                    violate bounds
       ColIndex   - int ncol, column indices of column violators
       RowIndex   - int ni, inequality index of row violators */

    workd = W->arrayd ;
    lhs = workd ; workd += nrow ;
    RowErri = lhs ;

    worki = W->arrayi ;
    ColIndex = worki ; worki += ncol ;
    RowIndex = worki ; worki += nrow ;

    errdual = PPZERO ;
    errls   = PPZERO ;
    errprox = PPZERO ;
    colerr  = PPZERO ;
    rowerr  = PPZERO ;
    normb   = PPZERO ;/* sup norm of b */
    normx   = PPZERO ;/* L1 norm of x */
    nrowindex = 0 ; /* number of dropped rows to activate */
    ncolindex = 0 ; /* number of free columns to bind */

    /* If errls, the norm of the residual in the linear system is large
       enough relative to the norm of the right side, then we refactor
       the matrix. To estimate the norm of the right right, we evaluate
       the norm of b. This neglects the change that occurred to the
       right side due to bound variables becoming free. */
    for (row = RLinkUp [nrow]; row < nrow; row = RLinkUp [row])
    {
        if ( normb < fabs (b [row]) )
        {
            normb = fabs(b [row]) ;
        }
    }
    cerr = PPZERO ;
    pproj_initx (lhs, PPZERO, nrow) ; /* used to store AF*cF */
    nf = 0 ;
    p = 0 ;
    for (j = 0; j < ncol; j++)
    {
        ibj = ib [j] ;
        if ( ibj == 0 ) /* currently free variable */
        {
            p = Ap [j] ;
            q = Ap [j+1] ;
            cj = c [j] ;
            if ( (loExists == TRUE) && (cj < lo [j]) ) /* lower bind */
            {
                z = lo [j] ;
                lo [j] = PPZERO ;
                cj -= z ;
                c [j] = cj ;
                /* save cj in case we decide later the violation was too small
                   and it is better to keep the variable free */
                ColIndex [ncolindex] = j ;
                ncolindex++ ;
                if ( hiExists == TRUE )
                {
                    hi [j] -= z ;
                }
                x [j] += z ;
                colerr = PPMAX (colerr, -cj) ;   /* max constraint violation */
                if ( z == PPZERO )
                {
                    for (; p < q; p++)
                    {
                        lhs [Ai [p]] += Ax [p]*cj ; /* AF*cF */
                    }
                }
                else
                {
                    for (; p < q; p++)
                    {
                        i = Ai [p] ;
                        ax = Ax [p] ;
                        b [i] -= ax*z ;    /* new right side b */
                        lhs [i] += ax*cj ; /* AF*cF */
                    }
                }
            }
            else if ( (hiExists == TRUE) && (cj > hi [j]) ) /* upper bind */
            {
                z = hi [j] ;
                hi [j] = PPZERO ;
                cj -= z ;
                c [j] = cj ;
                /* save cj in case we decide later the violation was too small*/
                ColIndex [ncolindex] = j ;
                ncolindex++ ;
                if ( loExists == TRUE )
                {
                    lo [j] -= z ;
                }
                x [j] += z ;
                colerr = PPMAX (colerr, cj) ;   /* max constraint violation */
                if ( z == PPZERO )
                {
                    for (; p < q; p++)
                    {
                        lhs [Ai [p]] += Ax [p]*cj ; /* AF*cF */
                    }
                }
                else
                {
                    for (; p < q; p++)
                    {
                        i = Ai [p] ;
                        ax = Ax [p] ;
                        b [i] -= ax*z ;    /* new right side b */
                        lhs [i] += ax*cj ; /* AF*cF */
                    }
                }
            }
            else /* x [j] is free and remains free */
            {
                F [nf++] = j ;
                if ( loExists == TRUE )
                {
                    lo [j] -= cj ;
                }
                if ( hiExists == TRUE )
                {
                   hi [j] -= cj ;
                }
                t = x [j] = x [j] + cj ;
                if ( cerr < fabs (t) )
                {
                    cerr = fabs (t) ;
                }
                c [j] = PPZERO ;
                for (; p < q; p++)
                {
                    b [Ai [p]] -= Ax [p]*cj ;
                }
            }
        }
        normx += fabs (x [j]) ;
    }

    W->cerr = cerr ;
    ATnz = 0 ;
    Lnnz = 0 ;
    Annz = 0 ;
    W->cholflops = 0 ;
    nactive = 0 ;
    if ( Stat->nchols > 0 )
    {
        Lnz = W->L->nz ;
    }
    norm_l = PPZERO ; /* evaluate the norm of lambda */
    for (i = 0; i < nrow; i++)
    {
        bi = b [i] ; /* includes prox term -sigma*lambda [i] */
        bi_noprox = bi + sigma*lambda [i] ;
        /* b [i] includes the proximal term, newbi also needs dlambda part */
        newbi = bi - sigma*dlambda [i] ;
        b [i] = newbi ;
        k = ir [i] ;
        if ( k <= nsingni ) /* i is an active row */
        {
            nactive++ ;
            ATnz += ATp [i+1] - ATp [i] ;
            Annz += AFTnz [i] ;
            /* residual in equation is newbi minus lhs */
            PPFLOAT const terrls = fabs (newbi - lhs [i] - Asigma*dlambda [i]) ;
            if ( errls < terrls )
            {
                errls = terrls ;
            }

            /* gradient of dual function excluding proximal term. */
            if ( errdual < fabs (bi_noprox) )
            {
                errdual = fabs (bi_noprox) ;
            }

            /* gradient of dual function including proximal term */
            if ( errprox < fabs (newbi) )
            {
                errprox = fabs (newbi) ;
            }

            /* update lambda (lambda does not change for dropped equations) */
            lambda [i] += dlambda [i] ;
            if ( fabs (lambda [i]) > norm_l )
            {
                norm_l = fabs (lambda [i]) ;
            }
            dlambda [i] = PPZERO ;
            Rl = i ;
            if ( Stat->nchols > 0 )
            {
                Lnnz += Lnz [i] ;
                W->cholflops += ((PPFLOAT) Lnz [i]) * ((PPFLOAT) Lnz [i]) ;
            }
        }
        else   /* i is a dropped row */
        {
            if ( nsing )
            {
                if ( fabs (lambda [i]) > norm_l )
                {
                    norm_l = fabs (lambda [i]) ;
                }
            }
            k -= nsingni ; /* k = ineqindex */
            PPFLOAT const loj = bl [k] ;
            s = newbi + loj ;
            if ( s > PPZERO ) /* lambda_i > 0 increases L */
            {
                if ( rowerr < s )
                {
                    rowerr = s ; /* max violation in dropped rows */
                }
                if ( PrintLevel > 1 )
                {
                    printf ("activate lower bound in row: %ld grad: %e\n",
                            (LONG) i, s);
                }
                RowErri [nrowindex] = s ;
                ns [i] = 1 ;     /* activate row at lower bound */
                RowIndex [nrowindex] = k ;
                nrowindex++ ;
            }
            else
            {
                s = newbi + bu [k] ;
                if ( s < PPZERO )     /* lambda_i < 0 increases dual function */
                {
                    if ( rowerr < -s )
                    {
                        rowerr = -s ; /* max violation in dropped rows */
                    }
                    if ( PrintLevel > 1 )
                    {
                        printf ("activate upper bound in row: %ld grad: %e\n",
                                (LONG) i, s);
                    }
                    RowErri [nrowindex] = s ;
                    ns [i] = 2 ;      /* active row at upper bound */
                    RowIndex [nrowindex] = k ;
                    nrowindex++ ;
                }
            }
            /* for dualerr, do not include the proximal term */
            s = bi_noprox + loj ;
            if ( s > PPZERO ) /* lambda_i > 0 increases L */
            {
                if ( errdual < s )
                {
                    errdual = s ; /* max violation in dropped rows */
                }
            }
            else
            {
                s = bi_noprox + bu [k] ;
                if ( s < PPZERO )     /* lambda_i < 0 increases dual function */
                {
                    if ( errdual < -s )
                    {
                        errdual = -s ; /* max violation in dropped rows */
                    }
                }
            }
        }
    }
    W->norm_l = norm_l ;
    if ( PrintLevel > 2 )
    {
        printf ("max norm lambda: %e\n", norm_l) ;
    }
    if ( errprox >= W->gamma*rowerr ) /* sparsa condition does not hold */
    {
        W->sparsaOK = FALSE ;
    }
    else                              /* condition for using sparsa holds */
    {
        W->sparsaOK = TRUE ;
    }
    errprox = PPMAX (errprox, rowerr) ; /* update errprox to include rowerr */

    /* if the stopping criterion is relative, not absolute, divide by absAx */
    PPFLOAT errdual_nonorm = errdual ;
    W->berr = errdual ;
    if ( Parm->stop_condition == 0 )
    {
        errdual /= (W->absAx + W->absAxk) ;
        errprox /= (W->absAx + W->absAxk) ;
        errls   /= (W->absAx + W->absAxk) ;
        normb   /= (W->absAx + W->absAxk) ;
    }
    else if ( Parm->stop_condition == 2 )
    {
        errdual /= (W->absAx + W->ymax) ;
        errprox /= (W->absAx + W->ymax) ;
        errls   /= (W->absAx + W->ymax) ;
        normb   /= (W->absAx + W->ymax) ;
    }
    Stat->errdual = errdual ;
    W->errdual = errdual ;

    if ( PrintLevel > 1 )
    {
        printf ("\ndual error:            %e\n", errdual) ;
        printf ("linear system error:   %e\n", errls) ;
        printf ("proximal error:        %e\n", errprox) ;
        printf ("column error:          %e\n", colerr) ;
        printf ("row error:             %e\n", rowerr) ;
        printf ("1-norm of x:           %e\n", normx) ;
        printf ("absAx:                 %e\n", W->absAx) ;
        printf ("sup-norm of b:         %e\n", normb) ;
        printf ("# new bound columns:   %ld\n", (LONG) ncolindex) ;
        printf ("# new active rows:     %ld\n", (LONG) nrowindex) ;
        printf ("# current active rows: %ld\n\n", (LONG) nactive) ;
    }

    /* By default, convergence tolerance has not been met */
    status = PPROJ_TOLERANCE_NOT_MET ;

    /* If the error in the residual for the linear system is large,
       even though the factored matrix was used to solve the linear system,
       then flag the matrix for a fresh factorization. It is possible that
       due to updates and downdates, an inaccurate factorization was
       generated, so hopefully, by refactoring the matrix, the solution
       accuracy will improve. */
    if ( (errls > normb*Parm->tolrefactor) && (W->return_chol == TRUE) )
    {
        W->fac = FALSE ; /* refactor the matrix from scratch */
        if ( PrintLevel > 1 )
        {
            printf ("Refactor, large relative error in solution\n"
                    "    number of tries: %i\n", W->factor_not_OK) ;
        }
        W->factor_not_OK++ ;
        if ( W->factor_not_OK >= Parm->badFactorCutoff )
        {
            return (PPROJ_DUAL_SOLVE_ERROR) ;
        }
    }
    else
    {
        W->factor_not_OK = 0 ;
    }

    /* If proximal error is sufficiently small, perform a proximal update.
       Note that proximal updates currently can not be handled when the
       problem is an LP. */
    if ( (errprox <= Parm->tolprox*errdual) && !Parm->LP )
    {
        status = PPROJ_PROX_UPDATE ;
    }

    /* If the dual error is sufficiently small, the solution was found */
    if ( errdual <= grad_tol )
    {
        status = PPROJ_SOLUTION_FOUND ;
    }
    else if ( Parm->LP ) /* special stopping conditions for an LP */
    {
        if ( PrintLevel >= 2 )
        {
            printf ("errdual_nonorm: %e norm_l: %e LinGrad_tol: %e\n",
                     errdual_nonorm, norm_l, Parm->LinGrad_tol) ;
            printf ("errdual: %e cerr/norm_l: %e LinFactor: %e\n",
                     errdual, cerr/norm_l, Parm->LinFactor) ;
            printf ("absAx: %e absAxk: %e 1-norm x: %e\n",
                     W->absAx, W->absAxk, normx) ;
        }
        /* the first condition implies that the unnormalized dual gradient
           is small relative to lambda, while the second condition implies that
           the normalized dual gradient (primal feasibility) is small
           relative to the normalized dual feasibility error */
        /*if ( errdual_nonorm <= Parm->LinGrad_tol * norm_l ||*/
        if ( errdual_nonorm <= norm_l*grad_tol*Parm->LinGrad_tol ||
             errdual        <= Parm->LinFactor * cerr )
        {
            if ( PrintLevel >= 1 )
            {
                printf ("LP terminate\n") ;
                printf ("unnormalized dual error: %e norm_l: %e\n",
                         errdual_nonorm, norm_l) ;
                printf ("  normalized dual error: %e cerr: %e\n",
                         errdual, cerr) ;
            }
            status = PPROJ_SOLUTION_FOUND ;
        }
    }

    if ( Stat->nchols > 0 )
    {
        W->Lnnz = Lnnz ;            /* number of nonzero in L */
        W->npup_old = W->npup_cur ; /* number of partial updates */
    }

    if ( status == PPROJ_SOLUTION_FOUND )
    {
        /* check if the matrix factorization is needed (this is,
           Parm->getfactor = TRUE), but dasa was previously not required
           to factor the matrix (since W->getfactor = FALSE) */
        if ( (W->getfactor == FALSE) && (Parm->getfactor == TRUE) )
        {
            /* If all the rows have dropped, then no need to factor the
               matrix (it does not exist). Also, if the matrix is factored
               and the factorization is up-to-date, then no need to return
               to dasa and factor the matrix. */
            if ( (nrow != RLinkUp [row]) && (W->fac == FALSE) ||
                 (W->nrowadd + W->nrowdel + W->ncoladd + W->ncoldel > 0) )
            {
                W->getfactor = TRUE ;
                status = PPROJ_TOLERANCE_NOT_MET ;
            }
        }
    }

    /* If the solution was found, then we return to the main program. */
    if ( (status == PPROJ_SOLUTION_FOUND) || (status == PPROJ_PROX_UPDATE) )
    {
        /* restore ns to be all EMPTY */
        for (k = 0; k < nrowindex; k++)
        {
            i = ineq_row [RowIndex [k]] ;
            ns [i] = EMPTY ;
        }

        /* restore F since it was overwritten near the start of check_error */
        nf = 0 ;
        for (j = 0; j < ncol; j++)
        {
            if ( !ib [j] )
            {
                F [nf++] = j ;
            }
        }
        W->nf = nf ;

        /* Reset ustart and lstart (first inequality at upper or lower
           bound for each block). The update rules in pproj_dasa may have
           messed up their values.  For each block in the multilevel
           decomposition, lstart points to the first singleton at its
           lower bound while ustart points to the first singleton at it
           upper bound */
        if ( cholmod )
        {
            for (k = 0; k < blks; k++)
            {
                lstart [k] = nsingni1 ;
                ustart [k] = nsingni2 ;
            }

            prevblkL = EMPTY ;
            for (j = lLinkUp [nsingni1]; j <= nsingni; j = lLinkUp [j])
            {
                SET_LSTART0(j) ;
            }

            prevblkU = EMPTY ;
            for (j = uLinkUp [nsingni2]; j <= nsingni; j = uLinkUp [j])
            {
                SET_USTART0(j) ;
            }
        }
         
        Stat->checkerr += pproj_timer () - tic ;
        W->nactive = nactive ;
        W->ATnz = ATnz ;
        W->Annz = Annz ;
        return (status) ;
    }

    /* Otherwise, get set for another iteration. Add dropped rows and
       bind columns for which the row error or the column error are
       sufficiently large. */
    if ( Parm->use_sparsa )
    {
        rowcutoff = PPZERO ;
        colcutoff = PPZERO ;
    }
    else
    {
        rowcutoff = Parm->cutfactor*rowerr ;
        colcutoff = Parm->cutfactor*colerr ;
    }

    ncoldel = W->ncoldel ;
    ncoladd = W->ncoladd ;
    nrowdel = W->nrowdel ;
    nrowadd = W->nrowadd ;

    /* ------------------------------------------------------------------ */
    /* check whether to activate query columns */
    /* ------------------------------------------------------------------ */
    for (k = 0; k < ncolindex; k++)
    {
        j = ColIndex [k] ;
        cj = c [j] ;
        if ( cj < 0 ) /* check lower bound */
        {
            if ( -cj > colcutoff )  /* lower bind j */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("j: %ld free -> lower (%e)\n", (LONG) j, -cj) ;
                }
                ib [j] = -1 ;
                /* add column to the delete list if not in the add list */
                if ( ColmodFlag [j] == EMPTY )
                {
                    ncoldel++ ;
                    W->ColmodList [ncol-ncoldel] = j ;
                    ColmodFlag [j] = ncol-ncoldel ;
                }
                else /* column was in the add list, remove it */
                {
                    l = ColmodFlag [j] ;
                    ncoladd-- ;
                    m = ColmodList [ncoladd] ;
                    ColmodList [l] = m ;
                    ColmodFlag [m] = l ;
                    ColmodFlag [j] = EMPTY ;
                }
                if ( return_chol ) /* pproj_dasa chol'd the matrix */
                {
                    q = Ap [j] + Anz [j] ;
                }
                else
                {
                    q = Ap [j+1] ;
                }
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( ir [i] <= nsingni )
                    {
                        Annz-- ;
                        ax = Ax [p] ;
                        D [i] -= ax*ax ;
                        ns [i] = 0 ; /* row with new bound variables */
                    }
                }
            }
            else        /* although it is bound, keep it free */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("j: %ld keep free (%e)\n", (LONG) j, -cj) ;
                }
                F [nf++] = j ;
                if ( loExists == TRUE )
                {
                    lo [j] -= cj ;
                }
                if ( hiExists == TRUE )
                {
                    hi [j] -= cj ;
                }
                c [j] = PPZERO ;
                x [j] += cj ;
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    b [Ai [p]] -= Ax [p]*cj ; /* fix b */
                }
            }
        }
        else
        {
            if ( cj > colcutoff )   /* upper bind j */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("j: %ld free -> upper (%e)\n", (LONG) j, cj) ;
                }
                ib [j] = +1 ;
                /* add column to the delete list if not in the add list */
                if ( ColmodFlag [j] == EMPTY )
                {
                    ncoldel++ ;
                    W->ColmodList [ncol-ncoldel] = j ;
                    ColmodFlag [j] = ncol-ncoldel ;
                }
                else /* column was in the add list, remove it */
                {
                    l = ColmodFlag [j] ;
                    ncoladd-- ;
                    m = ColmodList [ncoladd] ;
                    ColmodList [l] = m ;
                    ColmodFlag [m] = l ;
                    ColmodFlag [j] = EMPTY ;
                }
                if ( return_chol ) /* pproj_dasa chol'd the matrix */
                {
                    q = Ap [j] + Anz [j] ;
                }
                else
                {
                    q = Ap [j+1] ;
                }
                for (p = Ap [j]; p < q; p++)
                {
                    i = Ai [p] ;
                    if ( ir [i] <= nsingni )
                    {
                        Annz-- ;
                        ax = Ax [p] ;
                        D [i] -= ax*ax ;
                        ns [i] = 0 ; /* row with new bound variables */
                    }
                }
            }
            else        /* although it is bound, keep it free */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("j: %ld keep free (%e)\n", (LONG) j, cj) ;
                }
                F [nf++] = j ;
                if ( loExists == TRUE )
                {
                    lo [j] -= cj ;
                }
                if ( hiExists == TRUE )
                {
                    hi [j] -= cj ;
                }
                c [j] = PPZERO ;
                x [j] += cj ;
                q = Ap [j+1] ;
                for (p = Ap [j]; p < q; p++)
                {
                    b [Ai [p]] -= Ax [p]*cj ; /* fix b */
                }
            }
        }
    }


    /* ------------------------------------------------------------------ */
    /* check whether to activate query rows */
    /* ------------------------------------------------------------------ */
    /* 1. remove bound indices from AFT
       2. check to see if inactive row can be activated
       3. if inactive row is activated, then build row of AFT
       4. if inactive row remains inactive, then remove from link */

    if ( cholmod )
    {
        for (k = 0; k < blks; k++)
        {
            lstart [k] = nsingni1 ;
            ustart [k] = nsingni2 ;
        }
    }
    nrowindex = 0 ;
    Ll = nsingni1 ;
    Ul = nsingni2 ;
    Rl = nrow ;
    prevblkL = prevblkU = EMPTY ;
    for (i = 0; i < nrow; i++)
    {
        j = ns [i] ;
        PPINT const iri = ir [i] ;
        if ( j <= 0 )
        {
            if ( iri <= nsingni ) /* currently active row */
            {
                Rl = i ;
                if ( iri ) /* strict inequality or singleton present */
                {
                    if ( ni ) /* strict inequality */
                    {
                        if ( iri < 0 ) /* the row is active and at lower bound*/
                        {
                            k = -iri ;
                            Ll = k ;
                            SET_LSTART(k) ;
                        }
                        else   /* the row is active and at upper bound*/
                        {
                            Ul = iri ;
                            SET_USTART(iri) ;
                        }
                    }
                    else /* singleton present */
                    {
                        if ( (k = slo [i]) ) /* lower bound exists */
                        {
                            Ll = k ;
                            SET_LSTART(k) ;
                            if ( (k = shi [i]) ) /* upper bound exists */
                            {
                                Ul = k ;
                                SET_USTART_SIMPLE(k) ;
                            }
                        }
                        else if ( (k = shi [i]) ) /* upper bound exists */
                        {
                            Ul = k ;
                            SET_USTART(k) ;
                        }
                    }
                }
            }
            if ( j == 0 ) /* this is an active row with new bound variables */
            {
                if ( D [i] < sigma )
                {
                    D [i] = sigma ;
                }
                p0 = l = p = AFTp [i] ;
                q = p + AFTnz [i] ;
                ASSERT (ir [i] <= nsingni) ;
                for (; p < q; p++)
                {
                    if ( ib [AFTi [p]] == 0 ) /* column is free */
                    {
                        AFTi [l] = AFTi [p] ;
                        AFTx [l] = AFTx [p] ;
                        l++ ;
                    }
                }
                AFTnz [i] = l - p0 ;
                ns [i] = EMPTY ;
            }
            continue ;
        }
        if ( j == 1 ) /* inactive row that may activate at lower bound */
        {
            PPINT const sing = iri - nsingni ;
            s = RowErri [nrowindex] ;
            if ( s > rowcutoff ) /* activate row, lambda increases */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("i: %ld inactive -> lo active (err: %e)\n",
                             (LONG) i, RowErri [nrowindex]) ;
                }
                nactive++ ;
                dlambda [i] = PPZERO ;
                b [i] += bl [sing] ;
                ATnz += ATp [i+1] - ATp [i] ;
                /* if the row not in the delete list, then put it in add list */
                if ( RowmodFlag [i] == EMPTY )
                {
                    nrowadd++ ;
                    RowmodList [nrow-nrowadd] = i ;
                    RowmodFlag [i] = nrow-nrowadd ;
                }
                else /* keep row, remove row from the delete list */
                {
                    l = RowmodFlag [i] ;
                    nrowdel-- ;
                    m = RowmodList [nrowdel] ;
                    RowmodList [l] = m ;
                    RowmodFlag [m] = l ;
                    RowmodFlag [i] = EMPTY ;
                }

                /* add inequality to active list at lower bound */
                ADD_SING_IN_LLINK(sing) ;
                SET_LSTART(sing) ;
                if ( ni ) ir [i] = -sing ;/* unDrop row */
                else                      /* nsing */
                {
                    ir [i] = 1 ;
                    slo [i] = sing ;
                    /* in the case of column singletons, there could be
                       more than one in this row */
                    k = sing + 1 ;
                    if ( k < row_sing1 [i] ) /* k before start of next row */
                    {
                        /* add inequality to active list at upper bound */
                        shi [i] = k ;
                        ADD_SING_IN_ULINK(k) ;
                        SET_USTART_SIMPLE(k) ;
                    }
                    else shi [i] = 0 ;
                }
            }
            nrowindex++ ;
        }
        else if ( j == 2 ) /* inactive row may activate at upper bound */
        {
            PPINT const sing = iri - nsingni ; /* singleton number */
            s = RowErri [nrowindex] ;
            if ( -s > rowcutoff ) /* activate row, lambda decrease */
            {
                if ( PrintLevel > 1 )
                {
                    printf ("i: %ld inactive -> hi active (err: %e)\n",
                    (LONG) i, RowErri [nrowindex]) ;
                }
                nactive++ ;
                dlambda [i] = PPZERO ;
                b [i] += bu [sing] ;
                ATnz += ATp [i+1] - ATp [i] ;
                /* if the row not in the delete list, then put in add list */
                if ( RowmodFlag [i] == EMPTY )
                {
                    nrowadd++ ;
                    RowmodList [nrow-nrowadd] = i ;
                    RowmodFlag [i] = nrow-nrowadd ;
                }
                else /* keep row, remove row from the delete list */
                {
                    l = RowmodFlag [i] ;
                    nrowdel-- ;
                    m = RowmodList [nrowdel] ;
                    RowmodList [l] = m ;
                    RowmodFlag [m] = l ;
                    RowmodFlag [i] = EMPTY ;
                }

                /* add inequality to active list */
                ADD_SING_IN_ULINK(sing) ;
                SET_USTART(sing) ;

                if ( ni ) ir [i] = sing ;   /* activate row */
                else                     /* nsing */
                {
                    ir [i] = 1 ;
                    shi [i] = sing ;
                    k = sing - 1 ;
                    /* in the case of column singletons, there could be
                       more than one in this row */
                    if ( k >= row_sing [i] ) /* k remains in row */
                    {
                        /* add inequality to active list at upper bound */
                        slo [i] = k ;
                        ADD_SING_IN_LLINK(k) ;
                        SET_LSTART_SIMPLE(k) ;
                    }
                    else slo [i] = 0 ;
                }
            }
            nrowindex++ ;
        }
        ns [i] = EMPTY ;
        /* if the row is newly added, update AFT and RLink */
        if ( ((j == 1)  || (j == 2)) && (ir [i] <= nsingni) )
        {
            /* add row to the list of active rows */
            ADD_ROW_IN_RLINK(i) ;

            /* insert row in AFT */
            t = sigma ;
            q = ATp [i+1] ;
            p = ATp [i] ;
            l = AFTp [i] ;
            for (; p < q; p++)
            {
                j = ATi [p] ;
                if ( !ib [j] ) /* the column is free */
                {
                    ax = ATx [p] ;
                    t += ax*ax ;
                    AFTx [l] = ax ;
                    AFTi [l] = j ;
                    l++ ;
                }
            }
            D [i] = t ;            /* new diagonal element for SSOR */
            m =  l - AFTp [i] ;
            AFTnz [i] = m ;
            Annz += m ;
            ASSERT (ir [i] <= nsingni) ;
        }
    }
    W->nrowadd = nrowadd ;
    W->ncoladd = ncoladd ;
    W->nrowdel = nrowdel ;
    W->ncoldel = ncoldel ;
    W->ATnz = ATnz ;
    W->Annz = Annz ;
    W->nactive = nactive ;
    W->nf = nf ;

    /* if relative change in 1-norm of x >= 1.5, recompute absAx */
    if ( normx != PPZERO )
    {
        t = W->normx/normx ;
        W->normx = normx ;
        if ( (t >= 1.5) || (t <= .667) ) /* compute new absAx */
        {
            s = PPZERO ;
            for (row = RLinkUp [nrow]; row < nrow; row = RLinkUp [row])
            {
                t = PPZERO ;
                q = ATp [row+1] ;
                for (p = ATp [row]; p < q; p++)
                {
                    t += fabs (ATx [p]*x [ATi [p]]) ;
                }
                s = PPMAX (s, t) ;
            }
            W->absAx = s ;
        }
    }

#ifndef NDEBUG
    where = "before exiting check_error" ;
    pproj_check_modlist (I, where) ;
    k = PPMAX (ncol+nsingni+1, nrow) ;
    pproj_check_const (NULL, 0, ns, EMPTY, k, where) ;
    pproj_checkF (I, where) ;
    if ( status == PPROJ_TOLERANCE_NOT_MET )
    {
        pproj_checkb (I, where) ;
        pproj_checkD (I, where) ;
    }
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    if ( PrintLevel > 1 )
    {
        printf ("final # active rows:   %ld\n", (LONG) nactive) ;
        printf ("final # free columns:  %ld\n", (LONG) nf) ;
        printf ("# added rows:          %ld\n", (LONG) nrowadd) ;
        printf ("# deleted columns:     %ld\n", (LONG) ncoldel) ;
        printf ("rowcutoff:             %e\n", rowcutoff) ;
        printf ("colcutoff:             %e\n", colcutoff) ;
        printf ("Lnnz:                  %ld\n", (LONG) Lnnz) ;
        printf ("Annz:                  %ld\n", (LONG) Annz) ;
        printf ("nchol:                 %i\n", W->nchols) ;
        printf ("cholflops:             %e\n", W->cholflops) ;
        printf ("partial updates:       %e\n", W->npup) ;
        printf ("average flops:         %e\n", W->pupflops/PPMAX (1, W->npup)) ;
        printf ("rooted  updates:       %e\n", W->nrup) ;
        printf ("average flops:         %e\n", W->rupflops/PPMAX (1, W->nrup)) ;
        fflush(stdout) ;
    }
    Stat->checkerr += pproj_timer () - tic ;
    return (status) ;
}

/* ========================================================================= */
/* === pproj_prox_update =================================================== */
/* ========================================================================= */
/* Perform a proximal update, recompute b and c, and compute grad L to
   determine whether the stopping criterion is satisfied. */
/* ========================================================================= */
int pproj_prox_update
(
    PPcom *I
)
{
    PPINT  i, j, k, l, p, q, ncoladd, ineqindex, nf, nxmod,
           *AFTp, *AFTi, *AFTnz, *xmod_index,
           *ir, *ColmodFlag, *ColmodList, *F, *worki ;
    int    compute_rhsmod, set_to_bound, status, *ib ;
    const int loExists = I->Work->loExists ;
    const int hiExists = I->Work->hiExists ;
    PPFLOAT s, t, errdual, gradi, cj, xj, yj, tic,
            *c, *AFTx, *D, *lambda, *shift_l,
            *x, *absAx, *rhsmod, *workb, *worklo, *workhi, *workd ;

    PPstat *Stat ;
    PPprob *Prob ;
    PPparm *Parm ;
    PPwork    *W ;

    tic = pproj_timer () ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    Prob = I->Prob ;
    W = I->Work ;

    /* NOTE: sigma is updated later if we are not going to terminate */

    /* PPprob */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPFLOAT const      *singc = Prob->singc ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const       nsing = Prob->nsing ;
    PPINT   const     nsingni = nsing + Prob->ni ;
    PPFLOAT const         *lo = Prob->lo ;
    PPFLOAT const         *hi = Prob->hi ;
    PPFLOAT const          *y = Prob->y ;
    PPFLOAT const         *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const         *bu = (nsing) ? Prob->singhi : Prob->bu ;
    PPFLOAT const          *b = Prob->b ;
    PPINT   const        *slo = W->slo ;
    PPINT   const   *row_sing = Prob->row_sing ;
    PPINT   const  *row_sing1 = row_sing+1 ;

    /* Transpose of A */
    PPINT   const *ATp = W->ATp ;
    PPINT   const *ATi = W->ATi ;
    PPFLOAT const *ATx = W->ATx ;

    c = W->c ;
    workb = W->b ;
    worklo = W->lo ;
    workhi = W->hi ;


    /* Transpose of A */
    ATp = W->ATp ;
    ATi = W->ATi ;
    ATx = W->ATx ;

    workd = W->arrayd ;
    rhsmod = workd ; workd += nrow ;
    absAx  = workd ; workd += nrow ;

    worki = W->arrayi ;
    xmod_index = worki ; worki += ncol ;

    lambda = W->lambda ;
    shift_l = W->shift_l ;
    x = W->x ;

    D = W->D ;

    /* ib [col] = +1 if column at upper bound
                  -1 if column at lower bound
                   0 if column is free */
    ib = W->ib ;

    /* ir gives status of row i:
       ir [i] =  0 for an equality constraint
              =  1 for an active singleton row
              =  ineq # for active inequality at upper bound
              = -ineq # for active inequality at lower bound
              =  ineq # or singleton # + nsingni for a dropped
                 constraint */
    ir = W->ir ;

    if ( W->shiftl_is_zero )
    {
        pproj_copyx (shift_l, lambda, nrow) ;
    }
    else
    {
        pproj_saxpy (shift_l, lambda, PPONE, nrow) ;
    }
    /* starting lambda = 0 */
    pproj_initx (lambda, PPZERO, nrow) ;
    pproj_initx (absAx, PPZERO, nrow) ;

    /* shift_l != 0 */
    W->shiftl_is_zero = FALSE ;
    /* recompute c */
    pproj_copyx (c, y, ncol) ;
    /* initialize diagonal of D to be zero, if we do not terminate,
       then the new sigma is later added to the diagonal */
    pproj_initx (D, PPZERO, nrow) ;
    /* compute c by rows of A, set shift_l to zero for dropped rows */
    /* set b_i to bl, bu, or 0 */
    for (i = 0; i < nrow; i++)
    {
        k = ir [i] ;
        if ( k <= nsingni ) /* row is active */
        {
            if ( nsing )
            {
                s = b [i] ; /* Prob->b */
                PPINT const q0 = slo [i] ;
                PPINT const q1 = row_sing1 [i] ;
                /* remember that user's singlo and singhi were replaced
                   by -singlo and -singhi respectively in pproj_init
                   also above we set bl = singlo and bu = singhi */
                j = row_sing [i] ;
                if ( q0 ) /* singletons at lower bound exist */
                {
                    for (; j <= q0; j++) s += bl [j] ;
                }
                    for (; j < q1; j++)  s += bu [j] ;
            }
            else
            {
                if      ( k == 0 ) s = b [i] ; /* Prob->b */
                else if ( k <  0 ) s = bl [-k] ;
                else               s = bu [k] ;
            }
            t = shift_l [i] ;
            if ( t != PPZERO )
            {
                q = ATp [i+1] ;
                for (p = ATp [i]; p < q; p++)
                {
                    c [ATi [p]] += t*ATx [p] ;
                }
            }
        }
        else /* row is inactive, either strict inequality or singleton */
        {
            
            if ( nsing ) shift_l [i] = singc [k-nsing] ;
            else         shift_l [i] = PPZERO ;
            s = PPZERO ;
        }
        workb [i] = s ;
    }

    /* Compute the gradient of the dual function, absAx_sup, and check to
       see if the convergence tolerance has been satisfied.  Due to
       rounding errors, the ib flag may indicate that a component
       of x is bound, while the value of c may imply that the minimizer
       of the dual function is free. In this case, we need to change
       the ib value to 0 to free the variable. We compute both b,
       which corresponds to b0 in the pproj code, and a correction
       rhsmod that is added to b to obtain the dual gradient. */
    nf = W->nf ;
    AFTp = W->AFTp ;
    AFTi = W->AFTi ;
    AFTnz = W->AFTnz ;
    AFTx = W->AFTx ;
    F = W->F ;
    pproj_initx (rhsmod, PPZERO, nrow) ;
    ncoladd = W->ncoladd ;
    /* ColmodFlag is empty if row not modified, otherwise points into
       ColmodList showing columns to modify*/
    ColmodList = W->ColmodList ;
    ColmodFlag = W->ColmodFlag ;
    /* At this point, we do not know if we will terminate. Save a copy
       in xmod_index of the indices of components of x that may need to
       be adjusted if we have reached the stopping criterion. */
    nxmod = 0 ;
    p = 0 ;
    for (j = 0; j < ncol; j++)
    {
        k = ib [j] ;
        cj = c [j] ;
        q = Ap [j+1] ;
        if ( k == 0 ) /* treat variable as free */
        {
            if ( (loExists == TRUE) && (cj < lo [j]) )
            {
                xmod_index [nxmod] = j ;
                nxmod++ ;
                xj = lo [j] ;
                compute_rhsmod = TRUE ;
            }
            else if ( (hiExists == TRUE) && (cj > hi [j]) )
            {
                xmod_index [nxmod] = j ;
                nxmod++ ;
                xj = hi [j] ;
                compute_rhsmod = TRUE ;
            }
            else
            {
                compute_rhsmod = FALSE ;
            }
            if ( loExists == TRUE )
            {
                worklo [j] = lo [j] - cj ;
            }
            if ( hiExists == TRUE )
            {
                workhi [j] = hi [j] - cj ;
            }
            x [j] = cj ;
            c [j] = PPZERO ;
            /* If ib [j] = 0, we treat the variable as free, but in
               grad L, the variable could be bound. Hence, we compute
               rhsmod, which is the correction that is added to b
               to obtain grad L */
            if ( compute_rhsmod )
            {
                t = cj - xj ;
                for (; p < q; p++)
                {
                    PPINT row = Ai [p] ;
                    PPFLOAT ax = Ax [p] ;
                    D [row] += ax*ax ;
                    absAx [row] += fabs (xj*ax) ;
                    workb [row] -= cj*ax ;
                    rhsmod [row] += t*ax ;
                }
            }
            else
            {
                yj = fabs (y [j]) + fabs (cj - y [j]) ;
                for (; p < q; p++)
                {
                    PPINT row = Ai [p] ;
                    PPFLOAT ax = Ax [p] ;
                    D [row] += ax*ax ;
                    absAx [row] += fabs (ax*yj) ;
                    workb [row] -= cj*ax ;
                }
            }
        }
        else /* currently bound variable */
        {
            if ( (hiExists == TRUE) && (cj >= hi [j]) ) /* at upper bound */
            {
                set_to_bound = TRUE ;
                ib [j] = +1 ;
                t = hi [j] ;
                workhi [j] = PPZERO ;
                if ( loExists == TRUE )
                {
                    worklo [j] = lo [j] - t ;
                }
            }
            else if ( (loExists == TRUE ) && (cj <= lo [j]) ) /*at lower bound*/
            {
                set_to_bound = TRUE ;
                ib [j] = -1 ;
                t = lo [j] ;
                worklo [j] = PPZERO ;
                if ( hiExists == TRUE )
                {
                    workhi [j] = hi [j] - t ;
                }
            }
            else /* this bound variable does not satisfy a bound, hence,
                    we must make it free */
            {
                set_to_bound = FALSE ;
            }
            if ( set_to_bound ) /* the variable remains bound*/
            {
                x [j] = t ;
                c [j] -= t ;
                for (; p < q; p++)
                {
                    PPINT row = Ai [p] ;
                    PPFLOAT ax = Ax [p] ;
                    absAx [row] += fabs (t*ax) ;
                    workb [row] -= t*ax ;
                }
            }
            else /* the variable is bound but set free */
            {
                if ( Parm->PrintLevel > 1 )
                {
                    PPFLOAT const loj = (loExists) ? lo [j] : -PPINF ;
                    PPFLOAT const hij = (hiExists) ? hi [j] : PPINF ;
                    printf ("col %ld is bound (%i) but set to free in "
                            "pproj based on lo: %e cj: %e hi: %e\n",
                             (LONG) j, ib [j], loj, cj, hij) ;
                }
                F [nf] = j ;
                nf++ ;
                ib [j] = 0 ;
                ColmodList [ncoladd] = j ; /* use 1st part for add */
                ASSERT (ColmodFlag [j] == EMPTY) ;
                ColmodFlag [j] = ncoladd ;
                ncoladd++ ;
                x [j] = cj ;
                if ( hiExists == TRUE )
                {
                    workhi [j] = hi [j] - cj ;
                }
                if ( loExists == TRUE )
                {
                    worklo [j] = lo [j] - cj ;
                }
                c [j] = PPZERO ;
                yj = fabs (y [j]) + fabs (cj - y [j]) ;
                for (; p < q; p++)
                {
                    PPINT row = Ai [p] ;
                    PPFLOAT ax = Ax [p] ;
                    absAx [row] += fabs (ax*yj) ;
                    workb [row] -= cj*ax ;
                    if ( ir [row] <= nsingni ) /* row is active */
                    {
                        D [row] += ax*ax ;
                        l = AFTp [row] + AFTnz [row]++ ;
                        AFTx [l] = ax ;
                        AFTi [l] = j ;
                    }
                }
            }
        }
    }
    W->ncoladd = ncoladd ;
    W->nf = nf ;
    errdual = PPZERO ;
    t = PPZERO ;
    for (i = 0; i < nrow; i++)
    {
        /* add rhsmod to b to obtain gradient of dual function */
        gradi = workb [i] + rhsmod [i] ;
        k = ir [i] ;
        if ( k <= nsingni ) /* i is an active row */
        {
            if ( t < absAx [i] )
            {
                t = absAx [i] ;
            }
            if ( errdual < fabs (gradi) )
            {
                errdual = fabs (gradi) ;
            }
        }
        else /* row is inactive, subgradient = [gradi+loj, gradi+hij] */
        {
            ineqindex = k - nsingni ;
            s = gradi + bl [ineqindex] ;
            if ( s > PPZERO ) /* lambda_i > 0 increases L */
            {
                if ( errdual < s )
                {
                    errdual = s ; /* max violation in dropped rows */
                }
            }
            else
            {
                s = gradi + bu [ineqindex] ;
                if ( s < PPZERO )   /* lambda_i < 0 increases dual function */
                {
                    if ( errdual < -s )
                    {
                        errdual = -s ; /* max violation in dropped rows */
                    }
                }
            }
        }
    }
    if ( t == PPZERO )
    {
        t = PPONE ;
    }
    W->absAx = t ;
    if ( Parm->stop_condition == 0 )
    {
        errdual /= (t + W->absAxk) ;
    }
    else if ( Parm->stop_condition == 2 )
    {
        errdual /= (t + W->ymax) ;
    }
    if ( (errdual <= Parm->grad_tol) )
    {
        Stat->errdual = errdual ;
        status = PPROJ_SOLUTION_FOUND ;
        /* Adjust the xmod components of x so that they satisfy the bound
           constraints. */
        for (k = 0; k < nxmod; k++)
        {
            j = xmod_index [k] ;
            if ( (loExists == TRUE) && (x [j] < lo [j]) )
            {
                x [j] = lo [j] ;
            }
            else
            {
                x [j] = hi [j] ;
            }
        }
    }
    else /* update sigma */
    {
        W->sigma *= Parm->sigma_decay ;
        W->Totsigma = W->sigma + W->Asigma ;

        if ( Parm->cholmod )
        {
            W->cmm->dbound = W->Totsigma ;
            W->fac = FALSE ;              /* need to refactor the matrix */
        }
        /* add sigma to the diagonal D */
        for (i = 0; i < nrow; i++)
        {
            D [i] += W->sigma ;
        }
        status = PPROJ_TOLERANCE_NOT_MET ;
        if ( Parm->PrintLevel > 1 )
        {
            printf ("\nprox update dual error %e\n", errdual) ;
        }
    }
#ifndef NDEBUG
    /* record new dual value but do not insist on objective increase */
    pproj_check_dual (I, NULL, "in pproj after proximal step", TRUE, FALSE) ;
#endif
    Stat->nprox++ ;
    Stat->prox_update += pproj_timer () - tic ;
    return (status) ;
}

/* ==========================================================================
   ====== pproj_invert ======================================================
   ==========================================================================
   Invert any row permutations applied to lambda and any column permutations
   applied to x to obtain the solution relative to the starting problem.
   ========================================================================== */

void pproj_invert
(
    PPcom *I
)
{
    PPFLOAT tic, *lambda, *newlambda, *singk, *singx, *x, *newx, *workd ;
    PPINT    i, j, p ;
    PPwork    *W ;
    PPprob *Prob ;
    PPparm *Parm ;

    tic = pproj_timer () ;
    Prob = I->Prob ;
    PPINT   const     nrow = Prob->nrow ;
    PPINT   const     ncol = Prob->ncol ;
    PPFLOAT const      *lo = Prob->lo ;
    PPFLOAT const      *hi = Prob->hi ;
    PPINT   const *rowperm = Prob->rowperm ;
    PPINT   const *colperm = Prob->colperm ;
    W      = I->Work ;
    lambda = W->lambda ;
    x      = W->x ;
    int const loExists = W->loExists ;
    int const hiExists = W->hiExists ;

    workd = W->arrayd ; /* grab some memory */
    Parm = I->Parm ;
    int const permute = Parm->permute ;


    if ( permute )
    {
        /* need an array to handle permutation in lambda */
        newlambda = workd ;  workd += nrow ;
        if ( !W->shiftl_is_zero )
        {
            /* if shift_l is nonzero, then add it to lambda */
            for (i = 0; i < nrow; i++)
            {
                /* rowperm [i] is the row number of the original matrix
                   corresponding to row i of the permuted matrix */
                newlambda [rowperm [i]] = lambda [i] + W->shift_l [i] ;
            }
        }
        else
        {
            for (i = 0; i < nrow; i++)
            {
                newlambda [rowperm [i]] = lambda [i] ;
            }
        }
        pproj_copyx (lambda, newlambda, nrow) ;
    }
    else /* no perm needed */
    {
        if ( !W->shiftl_is_zero )
        {
            /* if shift_l is nonzero, then add it to lambda
               NOTE: newlambda = userlambda if it exists */
            pproj_step (lambda, lambda, W->shift_l, PPONE, nrow) ;
        }
    }

    /* now generate x in user ordering */
    PPINT const nsing = Prob->nsing ;
    newx = workd ;  workd += ncol+nsing ;
    /* start by generating the part of the solution x1 associated with column
       singletons if this is requested. */
    if ( nsing )
    {
        PPINT   const  *ineq_row = Prob->ineq_row ;
        PPINT   const  *row_sing = Prob->row_sing ;
        PPINT   const *row_sing1 = row_sing+1 ;
        PPFLOAT const    *singlo = Prob->singlo ;
        PPFLOAT const    *singhi = Prob->singhi ;
        PPINT   const       *ATp = W->ATp ;
        PPINT   const       *ATi = W->ATi ;
        PPFLOAT const       *ATx = W->ATx ;
 
        /* Note that userRowSing starts at 0 while pproj row_sing starts at 1 */
        PPINT const *userRowSing = W->user_row_sing ;
        singk = singx = x+ncol-1 ; /* j = 1 in pproj <==> ncol in user's x */
        for (j = 1; j <= nsing; j++)
        {
            PPINT const row = ineq_row [j] ; /* row associated with j */
            if ( permute )
            {
                i = rowperm [row] ; /* i = row in original matrix */
                singk = singx+(userRowSing [i] - j) ;
            }
            PPINT ksing = W->ir [row] ;
            if ( ksing == 1 )                /* all singletons at bounds */
            {
                PPINT const q0 = W->slo [row] ;
                /* lower bounds */
                for (; j <= q0; j++)
                {
                    singk [j] = singlo [j] ;
                }
                PPINT const q1 = row_sing1 [row] ;
                /* upper bounds */
                for (; j < q1; j++)
                {
                    singk [j] = singhi [j] ;
                }
            }
            else /*everything before ksing at lower, after at upper bound */
            {
                ksing -= nsing ;
                PPFLOAT t = -Prob->b [row] ;
                PPINT const q0 = ATp [row+1] ;
                for (p = ATp [row]; p < q0; p++)
                {
                    t += ATx [p]*x [ATi [p]] ;
                }
                /* lower bounds */
                for (; j < ksing; j++)
                {
                    singk [j] = singlo [j] ;
                    t -= singlo [j] ;
                }
                PPINT const q1 = row_sing1 [row] ;
                /* upper bounds */
                for (j++; j < q1; j++)
                {
                    singk [j] = singhi [j] ;
                    t -= singhi [j] ;
                }
                singk [ksing] = t ;
            }
        }
    }

    /* colperm [j] = column of original matrix corresponding to column j in
                     permuted matrix */
    x = W->x ;
    if ( permute )
    {
        for (j = 0; j < ncol; j++)
        {
            PPFLOAT xj = x [j] ;
            if ( loExists && (xj < lo [j]) )
            {
                xj = lo [j] ;
            }
            else if ( hiExists && (xj > hi [j]) )
            {
                xj = hi [j] ;
            }
            newx [colperm [j]] = xj ;
        }
        pproj_copyx (x, newx, ncol) ; /* copy newx to x */
    }
    else /* trim x if it violates a bound */
    {
        for (j = 0; j < ncol; j++)
        {
            if ( loExists && (x [j] < lo [j]) )
            {
                x [j] = lo [j] ;
            }
            else if ( hiExists && (x [j] > hi [j]) )
            {
                x [j] = hi [j] ;
            }
        }
    }
    /* if we will return PPcom structure and cholmod is used, then updateAnz */
    if ( (W->return_data == TRUE) && (Parm->cholmod == TRUE) )
    {
        pproj_updateAnz (I, 2) ; /*also sets AFTnz = 0 for dead rows*/
    }
    I->Stat->invert += pproj_timer () - tic ;
}

/* =========================================================================
   =========================== pproj_cholmod_sparse ========================
   =========================================================================
    Create a cholmod sparse matrix.
   ========================================================================== */

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
)
{
    A->nrow = nrow ;
    A->ncol = ncol ;
    A->p = p ;
    A->nz = nz ;
    A->i = i ;
    A->x = x ;
    A->packed = packed ;
    A->sorted = sorted ;
    A->xtype = xtype ;
    A->nzmax = nzmax ;
    A->z = NULL ;
    A->stype = 0 ; /* unsymmetric */
    /* CAUTION: need to sink these with cholmod */
    A->itype = CHOLMOD_INT ;
    A->dtype = CHOLMOD_DOUBLE ;
}

/* =========================================================================
   =========================== pproj_cholmod_dense =========================
   =========================================================================
    Create a cholmod dense vector.
   ========================================================================== */

void pproj_cholmod_dense
(
    cholmod_dense *A, /* pointer to a cholmod dense matrix */
    PPINT       nrow, /* number of rows */
    PPFLOAT       *x  /* size nrow, the numerical values in A */
)
{
    A->nrow = nrow ;
    A->ncol = 1 ;
    A->x = x ;
    A->nzmax = nrow ;
    /* CAUTION: need to sink these with cholmod */
    A->xtype = CHOLMOD_REAL ;
    A->dtype = CHOLMOD_DOUBLE ;
    A->z = NULL ;
    A->d = nrow ;
}

/* ========================================================================== */
/* === pproj_transpose ====================================================== */
/* ========================================================================== */
/*    Transpose a sparse matrix: B = A' */
/* ========================================================================== */

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
)
{
    PPINT i, j, p, q, pp ;

    /* ====================================================================== */
    /* === compute row counts of A ========================================== */
    /* ====================================================================== */

    for (i = 0; i < nrow; i++)
    {
        W [i] = 0 ;
    }
    p = 0 ;
    for (j = 1; j <= ncol; j++)
    {
        q = Ap [j] ;
        for (; p < q; p++)
        {
            W [Ai [p]]++ ;
        }
    }

    /* ====================================================================== */
    /* === compute column pointers of B given the counts ==================== */
    /* ====================================================================== */

    Bp [0] = 0 ;
    for (i = 0; i < nrow; i++)
    {
        Bp [i+1] = Bp [i] + W [i] ;
        W [i] = Bp [i] ;
    }

    /* ====================================================================== */
    /* === B = A' =========================================================== */
    /* ====================================================================== */

    p = 0 ;
    for (j = 0 ; j < ncol ; j++)
    {
        q = Ap [j+1] ;
        for (; p < q; p++)
        {
            pp = W [Ai [p]]++ ;
            Bi [pp] = j ;
            Bx [pp] = Ax [p] ;
        }
    }
}

    /* ====================================================================== */
    /* === pproj_iminsort =================================================== */
    /* ======================================================================
       ________________________________________________________
      |                                                        |
      |       sort an int array in increasing order            |
      |                                                        |
      |    input:                                              |
      |                                                        |
      |         x  --array of numbers (int *) of length n      |
      |         w  --working array (int *) of length n         |
      |         n  --number of array elements to sort          |
      |                                                        |
      |    output:                                             |
      |                                                        |
      |         x  --original array (int *) of length n        |
      |         y  --indices of x giving increasing order      |
      |              (int *) of length n                       |
      |________________________________________________________| */

void pproj_iminsort
(
    PPINT  *y, /* n-by-1 (output) */
    PPINT  *x, /* n-by-1 (input not modified) */
    PPINT  *w, /* n-by-1, (input, working array) */
    PPINT   n  /* number of elements to sort */
)
{
    PPINT *yi, *wi, i, j, k, l, m, p, q ;
    PPINT s, t ;

    y [0] = 0 ;
    if ( n < 2 ) return ;

    j = k = 0 ;
    for (i = 1; i < n; i++)
    {
        if ( x [i] < x [j] )
        {
            w [k] = i ;
            k = i ;
        }
        y [i] = j = i ;
    }

    w [k] = n ;
    while ( k > 0 )
    {
        l = m = 0 ;
        while ( l < n )
        {
            i = l ;
            p = y [i] ;
            s = x [p] ;
            j = w [i] ;
            k = j ;
            if ( j == n )
            {
                y [i] = j ;
                l = j ;
                w [m] = p ;
                k += m - i ;
                yi = y+(i-m) ;
                for (m++; m < k; m++)
                {
                    w [m] = yi [m] ;
                }
            }
            else
            {
                q = y [j] ;
                t = x [q] ;
                l = w [j] ;
                y [i] = l ;
                while ( 1 )
                {
                    if ( s > t )
                    {
                        w [m] = q ;
                        m++ ;
                        j++ ;
                        if ( j == l )
                        {
                            w [m] = p ;
                            k += m - i ;
                            yi = y+(i-m) ;
                            for (m++; m < k; m++)
                            {
                                w [m] = yi [m] ;
                            }
                            break ;
                        }
                        q = y [j] ;
                        t = x [q] ;
                    }
                    else
                    {
                        w [m] = p ;
                        m++ ;
                        i++ ;
                        if ( i == k )
                        {
                            w [m] = q ;
                            k = m + l - j ;
                            yi = y+(j-m) ;
                            for (m++; m < k; m++)
                            {
                                w [m] = yi [m] ;
                            }
                            break ;
                        }
                        p = y [i] ;
                        s = x [p] ;
                    }
                }
            }
        }
        if ( y [0] == n )
        {
            for (i = 0; i < n; i++)
            {
                y [i] = w [i] ;
            }
            return ;
        }

        l = m = 0 ;
        while ( l < n )
        {
            i = l ;
            p = w [i] ;
            s = x [p] ;
            j = y [i] ;
            k = j ;
            if ( j == n )
            {
                w [i] = j ;
                l = j ;
                y [m] = p ;
                k += m - i ;
                wi = w+(i-m) ;
                for (m++; m < k; m++)
                {
                    y [m] = wi [m] ;
                }
            }
            else
            {
                q = w [j] ;
                t = x [q] ;
                l = y [j] ;
                w [i] = l ;
                while ( 1 )
                {
                    if ( s > t )
                    {
                        y [m] = q ;
                        m++ ;
                        j++ ;
                        if ( j == l )
                        {
                            y [m] = p ;
                            k += m - i ;
                            wi = w+(i-m) ;
                            for (m++; m < k; m++)
                            {
                                y [m] = wi [m] ;
                            }
                            break ;
                        }
                        q = w [j] ;
                        t = x [q] ;
                    }
                    else
                    {
                        y [m] = p ;
                        m++ ;
                        i++ ;
                        if ( i == k )
                        {
                            y [m] = q ;
                            k = m + l - j ;
                            wi = w+(j-m) ;
                            for (m++; m < k; m++)
                            {
                                y [m] = wi [m] ;
                            }
                            break ;
                        }
                        p = w [i] ;
                        s = x [p] ;
                    }
                }
            }
        }
        if ( y [0] == n ) return ;
    }
}

    /* ====================================================================== */
    /* === pproj_xminsort =================================================== */
    /* ======================================================================
       ________________________________________________________
      |                                                        |
      |       sort a double array in increasing order          |
      |                                                        |
      |    input:                                              |
      |                                                        |
      |         x     --array of numbers (double *) of length n|
      |         w     --working array (int *) of length n      |
      |         n     --number of array elements to sort       |
      |                                                        |
      |    output:                                             |
      |                                                        |
      |         x     --original array (double *) of length n  |
      |         y     --indices of x giving increasing order   |
      |                 (int *) of length n                    |
      |________________________________________________________| */

void pproj_xminsort
(
    PPINT   *y, /* n-by-1 (output) */
    PPFLOAT *x, /* n-by-1 (input not modified) */
    PPINT   *w, /* n-by-1, (input, working array) */
    PPINT    n  /* number of elements to sort */
)
{
    PPINT *yi, *wi, i, j, k, l, m, p, q ;
    PPFLOAT s, t ;

    y [0] = 0 ;
    if ( n < 2 ) return ;
    if ( n < 3 )
    {
        if ( x [0] > x [1] )
        {
            y [0] = 1 ;
            y [1] = 0 ;
        }
        else y [1] = 1 ;
        return ;
    }

    j = k = 0 ;
    for (i = 1; i < n; i++)
    {
        if ( x [i] < x [j] )
        {
            w [k] = i ;
            k = i ;
        }
        y [i] = j = i ;
    }

    w [k] = n ;
    while ( k > 0 )
    {
        l = m = 0 ;
        while ( l < n )
        {
            i = l ;
            p = y [i] ;
            s = x [p] ;
            j = w [i] ;
            k = j ;
            if ( j == n )
            {
                y [i] = j ;
                l = j ;
                w [m] = p ;
                k += m - i ;
                yi = y+(i-m) ;
                for (m++; m < k; m++) w [m] = yi [m] ;
            }
            else
            {
                q = y [j] ;
                t = x [q] ;
                l = w [j] ;
                y [i] = l ;
                while ( 1 )
                {
                    if ( s > t )
                    {
                        w [m] = q ;
                        m++ ;
                        j++ ;
                        if ( j == l )
                        {
                            w [m] = p ;
                            k += m - i ;
                            yi = y+(i-m) ;
                            for (m++; m < k; m++) w [m] = yi [m] ;
                            break ;
                        }
                        q = y [j] ;
                        t = x [q] ;
                    }
                    else
                    {
                        w [m] = p ;
                        m++ ;
                        i++ ;
                        if ( i == k )
                        {
                            w [m] = q ;
                            k = m + l - j ;
                            yi = y+(j-m) ;
                            for (m++; m < k; m++) w [m] = yi [m] ;
                            break ;
                        }
                        p = y [i] ;
                        s = x [p] ;
                    }
                }
            }
        }
        if ( y [0] == n )
        {
            for (i = 0; i < n; i++) y [i] = w [i] ;
            return ;
        }

        l = m = 0 ;
        while ( l < n )
        {
            i = l ;
            p = w [i] ;
            s = x [p] ;
            j = y [i] ;
            k = j ;
            if ( j == n )
            {
                w [i] = j ;
                l = j ;
                y [m] = p ;
                k += m - i ;
                wi = w+(i-m) ;
                for (m++; m < k; m++) y [m] = wi [m] ;
            }
            else
            {
                q = w [j] ;
                t = x [q] ;
                l = y [j] ;
                w [i] = l ;
                while ( 1 )
                {
                    if ( s > t )
                    {
                        y [m] = q ;
                        m++ ;
                        j++ ;
                        if ( j == l )
                        {
                            y [m] = p ;
                            k += m - i ;
                            wi = w+(i-m) ;
                            for (m++; m < k; m++) y [m] = wi [m] ;
                            break ;
                        }
                        q = w [j] ;
                        t = x [q] ;
                    }
                    else
                    {
                        y [m] = p ;
                        m++ ;
                        i++ ;
                        if ( i == k )
                        {
                            y [m] = q ;
                            k = m + l - j ;
                            wi = w+(j-m) ;
                            for (m++; m < k; m++) y [m] = wi [m] ;
                            break ;
                        }
                        p = w [i] ;
                        s = x [p] ;
                    }
                }
            }
        }
        if ( y [0] == n ) return ;
    }
}

/* =========================================================================
   ======================== pproj_copyi ====================================
   =========================================================================
   Copy int vector x into vector y
   ========================================================================= */
void pproj_copyi
(
    PPINT       *y, /* output of copy */
    PPINT const *x, /* input of copy */
    PPINT const  n  /* length of vectors */
)
{
    PPINT i, n5 ;
    if ( (y == x) || (y == NULL) )
    {
        return ;
    }
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; i += 5)
    {
        y [i]   = x [i] ;
        y [i+1] = x [i+1] ;
        y [i+2] = x [i+2] ;
        y [i+3] = x [i+3] ;
        y [i+4] = x [i+4] ;
    }
}

/* =========================================================================
   ======================== pproj_copyi_int ================================
   =========================================================================
   Copy int vector x into vector y
   ========================================================================= */
void pproj_copyi_int
(
    int  *y, /* output of copy */
    int  *x, /* input of copy */
    PPINT n  /* length of vectors */
)
{
    PPINT i, n5 ;
    int *X, *Y ;
    if ( y == x )
    {
        return ;
    }
    n5 = n % 5 ;
    X = x+n5 ;
    Y = y+n5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; i += 5)
    {
        *Y++ = *X++ ;
        *Y++ = *X++ ;
        *Y++ = *X++ ;
        *Y++ = *X++ ;
        *Y++ = *X++ ;
    }
}

/* =========================================================================
   ======================== pproj_copyx ====================================
   =========================================================================
   Copy PPFLOAT vector x into vector y
   ========================================================================= */
void pproj_copyx
(
    PPFLOAT       *y, /* output of copy */
    PPFLOAT const *x, /* input of copy */
    PPINT   const  n  /* length of vectors */
)
{
    PPINT i, n5 ;
    if ( (y == x) || (y == NULL) )
    {
        return ;
    }
    n5 = n % 5 ;
    for (i = 0; i < n5; i++) y [i] = x [i] ;
    for (; i < n; i += 5)
    {
        y [i]   = x [i] ;
        y [i+1] = x [i+1] ;
        y [i+2] = x [i+2] ;
        y [i+3] = x [i+3] ;
        y [i+4] = x [i+4] ;
    }
}

/* =========================================================================
   ===================== proj_initi ========================================
   =========================================================================
   Initialize a PPINT array
   ========================================================================= */
void pproj_initi
(
    PPINT *x,  /* array to be initialized */
    PPINT  s,  /* scalar */
    PPINT  n   /* length of x */
)
{
    PPINT j, n5 ;
    PPINT *xj ;
    n5 = n % 5 ;
    for (j = 0; j < n5; j++) x [j] = s ;
    xj = x+j ;
    for (; j < n; j += 5)
    {
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
    }
}

/* =========================================================================
   ===================== pproj_initx =======================================
   =========================================================================
   Initialize a double array
   ========================================================================= */
void pproj_initx
(
    PPFLOAT *x,  /* array to be initialized */
    PPFLOAT  s,  /* scalar */
    PPINT   n   /* length of x */
)
{
    PPINT j, n5 ;
    PPFLOAT *xj ;
    n5 = n % 5 ;
    for (j = 0; j < n5; j++) x [j] = s ;
    xj = x+j ;
    for (; j < n; j += 5)
    {
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
        *(xj++) = s ;
    }
}

/* =========================================================================
   ===================== proj_initFx =======================================
   =========================================================================
   Initialize a double array at indices in F
   ========================================================================= */
void pproj_initFx
(
    PPFLOAT *x,  /* array to be initialized */
    PPFLOAT  s,  /* scalar */
    PPINT   *F,  /* indices to be initialized */
    PPINT    n   /* length of F */
)
{
    PPINT j, n5, *fj ;
    fj = F ;
    n5 = n % 5 ;
    for (j = 0; j < n5; j++) x [F [j]] = s ;
    fj = F+j ;
    for (; j < n; j += 5)
    {
        *(x+(*fj++)) = s ;
        *(x+(*fj++)) = s ;
        *(x+(*fj++)) = s ;
        *(x+(*fj++)) = s ;
        *(x+(*fj++)) = s ;
    }
}

/* =========================================================================
   ===================== proj_initstat =====================================
   ========================================================================= */
void pproj_initstat
(
    PPstat *Stat
)
{
    Stat->blks          = EMPTY ;
    Stat->maxdepth      = EMPTY ;
    Stat->solves        = NULL ; /* Stat->solves  initialized in pproj_init */
    Stat->updowns       = NULL ; /* Stat->updowns initialized in pproj_init */
    Stat->size_updowns = 0 ;
    /* initialize counting variables in Stat structure */
    Stat->phase1_its       = 0 ; /* # phase1 iterations */
    Stat->coor_ascent_its  = 0 ; /* # coordinate ascent iterations */
    Stat->ssor0_its        = 0 ; /* # ssor0 iterations */
    Stat->ssor1_its        = 0 ; /* # ssor1 iterations */
    Stat->sparsa_its       = 0 ; /* # sparsa iterations */
    Stat->nprox            = 0 ; /* # proximal updates */
    Stat->coldn            = 0 ; /* # column downdates to L */
    Stat->colup            = 0 ; /* # column updates to L */
    Stat->rowdn            = 0 ; /* # rows dropped from L */
    Stat->rowup            = 0 ; /* # rows added to L */
    Stat->coor_ascent_free = 0 ; /* # of variables freed in coor ascent */
    Stat->coor_ascent_drop = 0 ; /* # of rows dropped in coordinate ascent*/
    Stat->ssor0_free       = 0 ; /* # of variables freed in ssor0 */
    Stat->ssor0_drop       = 0 ; /* # of rows dropped in ssor0 */
    Stat->ssor1_free       = 0 ; /* # of variables freed in ssor1 */
    Stat->ssor1_drop       = 0 ; /* # of rows dropped in ssor1 */
    Stat->sparsa_col       = 0 ; /* # changes bound constraints in sparsa */
    Stat->sparsa_row       = 0 ; /* # changes row constraints in sparsa */
    Stat->sparsa_step_fail = 0 ; /* # of failures of Armijo step in sparsa*/
    Stat->nchols           = 0 ; /* # of Cholesky factorizations */
    Stat->lnnz             = 0 ; /* # of nonzeros in Cholesky factor */
    Stat->maxdepth         = 0 ; /* depth of multilevel partition tree */

    /* initialize timers in Stat structure */
    Stat->partition   = PPZERO ; /* compute reordering of rows of A */
    Stat->initialize  = PPZERO ; /* initwork & initlevels, with partition */
    Stat->phase1      = PPZERO ; /* time in phase1 */
    Stat->sparsa      = PPZERO ; /* sparsa */
    Stat->coor_ascent = PPZERO ; /* coordinate ascent */
    Stat->ssor0       = PPZERO ; /* ssor0 */
    Stat->ssor1       = PPZERO ; /* ssor1 */
    Stat->dasa        = PPZERO ; /* dasa(+coor_ascent, ssor0, ssor1)*/
    Stat->dasa_line   = PPZERO ; /* dasa line search */
    Stat->checkerr    = PPZERO ; /* check_error */
    Stat->prox_update = PPZERO ; /* proximal update */
    Stat->invert      = PPZERO ; /* invert permutation of rows and columns*/
    Stat->modrow      = PPZERO ; /* modrow (update L by add/delete rows) */
    Stat->modcol      = PPZERO ; /* modcol (rank 1 column updates of L) */
    Stat->chol        = PPZERO ; /* cholmod_analyze, cholmod_factorize */
    Stat->cholinc     = PPZERO ; /* incremental cholmod_rowfac */
    Stat->dltsolve    = PPZERO ; /* dltsolve (back solve) */
    Stat->lsolve      = PPZERO ; /* lsolve (forward solve) */
}

/* =========================================================================
   ===================== pproj_scale =======================================
   =========================================================================
   Scale a PPFLOAT array
   ========================================================================= */
void pproj_scale
(
    PPFLOAT *x,  /* array to be scaled */
    PPFLOAT *y,  /* array used for the scaling */
    PPFLOAT  s,  /* scale */
    PPINT    n   /* length of x */
)
{
    PPINT j, n5 ;
    PPFLOAT *xj, *yj ;
    n5 = n % 5 ;
    if ( s != -PPONE )
    {
        for (j = 0; j < n5; j++) x [j] = s*y [j] ;
        xj = x+j ;
        yj = y+j ;
        for (; j < n; j += 5)
        {
            *(xj++) = s*(*yj++) ;
            *(xj++) = s*(*yj++) ;
            *(xj++) = s*(*yj++) ;
            *(xj++) = s*(*yj++) ;
            *(xj++) = s*(*yj++) ;
        }
    }
    else
    {
        for (j = 0; j < n5; j++) x [j] = -y [j] ;
        xj = x+j ;
        yj = y+j ;
        for (; j < n; j += 5)
        {
            *(xj++) = -(*yj++) ;
            *(xj++) = -(*yj++) ;
            *(xj++) = -(*yj++) ;
            *(xj++) = -(*yj++) ;
            *(xj++) = -(*yj++) ;
        }
    }
}

/* =========================================================================
   ===================== pproj_dot =========================================
   =========================================================================
   Dot product between PPFLOAT arrays
   ========================================================================= */
PPFLOAT pproj_dot
(
    PPFLOAT *x,
    PPFLOAT *y,
    PPINT    n  /* length of x */
)
{
    PPINT j, n5 ;
    PPFLOAT *xj, *yj, t ;
    n5 = n % 5 ;
    t = PPZERO ;
    for (j = 0; j < n5; j++) t += x [j]*y [j] ;
    xj = x+j ;
    yj = y+j ;
    for (; j < n; j += 5)
    {
        t += (*xj++)*(*yj++) ;
        t += (*xj++)*(*yj++) ;
        t += (*xj++)*(*yj++) ;
        t += (*xj++)*(*yj++) ;
        t += (*xj++)*(*yj++) ;
    }
    return (t) ;
}

/* =========================================================================
   === pproj_sup_norm ======================================================
   =========================================================================
   Return max {|x [j]| : 1 <= j <= n}
   ========================================================================= */
PPFLOAT pproj_sup_norm
(
    PPFLOAT const *x, /* vector */
    PPINT   const  n  /* length of vector */
)
{
    PPFLOAT xnorm ;
    PPINT j, n5 ;
    n5 = n % 5 ;          /* n5 = n mod 5 */
    xnorm = PPZERO ;      /* initializing xnorm */
    for (j = 0; j < n5; j++)
    {
        if ( xnorm < fabs (x [j]) ) xnorm = fabs (x [j]) ;
    }
    for (; j < n; j += 5)
    {
        if ( xnorm < fabs (x [j]  ) ) xnorm = fabs (x [j]) ;
        if ( xnorm < fabs (x [j+1]) ) xnorm = fabs (x [j+1]) ;
        if ( xnorm < fabs (x [j+2]) ) xnorm = fabs (x [j+2]) ;
        if ( xnorm < fabs (x [j+3]) ) xnorm = fabs (x [j+3]) ;
        if ( xnorm < fabs (x [j+4]) ) xnorm = fabs (x [j+4]) ;
    }
    return (xnorm) ;        /* return ||x||_inf */
}

/* ==========================================================================
   ======================== pproj_minheap_build =============================
   ==========================================================================
   build a max heap in heap [1..nheap]
   ========================================================================== */

void pproj_minheap_build
(
    PPINT *heap, /* on input, an unsorted set of element numbers */
    PPFLOAT  *x, /* the numerical values to be ordered */
    PPINT nheap  /* number of elements to build into the heap */
)
{
    PPINT p ;
    for (p = nheap/2; p >= 1; p--)
    {
        pproj_minheap_ify (p, heap, x, nheap) ;
    }
}

/* ========================================================================== */
/* ===================== pproj_minheapify =================================== */
/* ========================================================================== */
/* heapify starting at node p.  On input, the heap below node p satisfies the */
/* heap property, except for heap [p] itself.  On output, the whole heap */
/* from p and below satisfies the heap property. */
/* ========================================================================== */

void pproj_minheap_ify
(
    PPINT     p, /* start at node p in the heap */
    PPINT *heap, /* size n, containing indices into x */
    PPFLOAT  *x, /* not modified */
    PPINT nheap  /* heap [1 ... nheap] is in use */
)
{
    PPINT left, right, e, hleft, hright ;
    PPFLOAT xleft, xright, xe ;

    e = heap [p] ;
    xe = x [e] ;

    while ( 1 )
    {
        left = p * 2 ;
        right = left + 1 ;

        if (right <= nheap)
        {
            hleft  = heap [left] ;
            hright = heap [right] ;
            xleft  = x [hleft] ;
            xright = x [hright] ;
            if (xleft < xright)
            {
                if (xe > xleft)
                {
                    heap [p] = hleft ;
                    p = left ;
                }
                else
                {
                    heap [p] = e ;
                    return ;
                }
            }
            else
            {
                if (xe > xright)
                {
                    heap [p] = hright ;
                    p = right ;
                }
                else
                {
                    heap [p] = e ;
                    return ;
                }
            }
        }
        else
        {
            if (left <= nheap)
            {
                hleft = heap [left] ;
                xleft = x [hleft] ;
                if (xe > xleft)
                {
                    heap [p] = hleft ;
                    p = left ;
                }
            }
            heap [p] = e ;
            return ;
        }
    }
}

/* ========================================================================== */
/* ======================== pproj_minheap_add =============================== */
/* ========================================================================== */
/* add a new leaf to a min-heap */
/* ========================================================================== */

void pproj_minheap_add
(
    PPINT   leaf, /* the new leaf */
    PPINT  *heap, /* size n, containing indices into x */
    PPINT    *ns, /* pointer from node to store in heap */
    PPFLOAT   *x, /* not modified */
    PPINT *nheap   /* number of elements in heap including new one */
)
{
    PPINT l, new, old ;
    PPFLOAT xold, xnew ;

    (*nheap)++ ;
    old = *nheap ;
    heap [old] = leaf ;
    xold = x [leaf] ;
    ns [leaf] = old ;
    while ( old > 1 )
    {
        new = old / 2 ;
        l = heap [new] ;
        xnew = x [l] ;
        if ( xnew > xold )
        {

/* swap new and old */

            ns [l] = old ;
            ns [leaf] = new ;
            heap [new] = leaf ;
            heap [old] = l ;
        }
        else return ;
        old = new ;
    }
}

/* ========================================================================== */
/* ======================== pproj_minheap_delete ============================ */
/* ========================================================================== */
/* delete the first element from a min-heap */
/* ========================================================================== */

void pproj_minheap_delete
(
    PPINT  *heap, /* containing indices into x, 1..n on input */
    PPINT    *ns, /* pointer from node to store */
    PPFLOAT   *x, /* not modified */
    PPINT *nheap, /* number of items in heap */
    PPINT      p  /* element to delete from the heap */
)
{

    PPINT j ;

/* Move element from the end of the heap to position p */

    j = heap [p] ;
    if ( *nheap == p )
    {
        ns [j] = EMPTY ;
        (*nheap)-- ;
        return ;
    }
    heap [p] = heap [(*nheap)--] ;
    ns [heap [p]] = p ;
    ns [j] = EMPTY ;

/* Update the heap at position p */

    pproj_minheap_update (heap, ns, x, *nheap, p) ;
}

/* ========================================================================== */
/* ======================== pproj_minheap_update ============================ */
/* ========================================================================== */
/* update the location of an element in a min-heap */
/* ========================================================================== */

void pproj_minheap_update
(
    PPINT *heap, /* size n, containing indices into x */
    PPINT   *ns, /* pointer from node to store in heap */
    PPFLOAT  *x, /* not modified */
    PPINT nheap, /* number of elements in the heap */
    PPINT     p  /* location of element to update */
)
{
    PPINT l, leaf, new, old ;
    PPFLOAT xnew, xold ;

/* Bubble up the heap */

    old = p ;
    leaf = heap [old] ;
    xold = x [leaf] ;
    while ( old > 1 )
    {
        new = old / 2 ;
        l = heap [new] ;
        xnew = x [l] ;
        if ( xnew > xold )
        {

/* swap new and old */

            ns [l] = old ;
            ns [leaf] = new ;
            heap [new] = leaf ;
            heap [old] = l ;
        }
        else if ( old == p ) break ;
        else                 return ;
        old = new ;
    }

/* Fix the heap below position p */

    pproj_minheap_ns (p, heap, ns, x, nheap) ;
}

/* ========================================================================== */
/* ======================== pproj_minheap_ns ================================ */
/* ========================================================================== */
/* heapify starting at node p.  On input, the heap at node p satisfies the */
/* heap property, except for heap [p] itself.  On output, the whole heap */
/* satisfies the heap property. Also, record pointers from nodes to store */
/* ========================================================================== */

void pproj_minheap_ns
(
    PPINT     p, /* start at node p in the heap */
    PPINT *heap, /* size n, containing indices into x */
    PPINT   *ns, /* pointer from node to store */
    PPFLOAT  *x, /* not modified */
    PPINT nheap  /* heap [1 ... nheap] is in use */
)
{
    PPINT left, right, e, hleft, hright ;
    PPFLOAT xleft, xright, xe ;

    e = heap [p] ;
    ns [e] = p ;
    xe = x [e] ;

    while ( 1 )
    {
        left = p * 2 ;
        right = left + 1 ;

        if (right <= nheap)
        {
            hleft  = heap [left] ;
            hright = heap [right] ;
            xleft  = x [hleft] ;
            xright = x [hright] ;
            if (xleft < xright)
            {
                if (xe > xleft)
                {
                    heap [p] = hleft ;
                    ns [hleft] = p ;
                    p = left ;
                }
                else
                {
                    heap [p] = e ;
                    ns [e] = p ;
                    return ;
                }
            }
            else
            {
                if (xe > xright)
                {
                    heap [p] = hright ;
                    ns [hright] = p ;
                    p = right ;
                }
                else
                {
                    heap [p] = e ;
                    ns [e] = p ;
                    return ;
                }
            }
        }
        else
        {
            if (left <= nheap)
            {
                hleft = heap [left] ;
                xleft = x [hleft] ;
                if (xe > xleft)
                {
                    heap [p] = hleft ;
                    ns [hleft] = p ;
                    p = left ;
                }
            }
            heap [p] = e ;
            ns [e] = p ;
            return ;
        }
    }
}
/* =========================================================================
   === pproj_step ==========================================================
   =========================================================================
    Set xnew = x + alpha*d
   ========================================================================= */
void pproj_step
(
    PPFLOAT       *xnew, /* updated x vector */
    PPFLOAT const    *x, /* current x */
    PPFLOAT const    *d, /* search direction */
    PPFLOAT const alpha, /* stepsize */
    PPINT   const     n  /* dimension */
)
{
    PPINT j, n5 ;
    
    if ( x == NULL )
    {
        return ;
    }
    n5 = n % 5 ;     /* n5 = n mod 5 */
    /* check if step size equals 1 */
    if ( alpha == PPONE )
    {
        for (j = 0; j < n5; j++)
        {
            xnew [j] = x [j] + d [j] ;
        }
        if ( xnew == x )
        {
            for (; j < n; )
            {
                 xnew [j] += d [j] ; j++ ;
                 xnew [j] += d [j] ; j++ ;
                 xnew [j] += d [j] ; j++ ;
                 xnew [j] += d [j] ; j++ ;
                 xnew [j] += d [j] ; j++ ;
            }
        }
        else
        {
            for (; j < n; )
            {
                 xnew [j] = x [j] + d [j] ; j++ ;
                 xnew [j] = x [j] + d [j] ; j++ ;
                 xnew [j] = x [j] + d [j] ; j++ ;
                 xnew [j] = x [j] + d [j] ; j++ ;
                 xnew [j] = x [j] + d [j] ; j++ ;
            }
        }
    }
    else if ( alpha == -PPONE )
    {
        for (j = 0; j < n5; j++)
        {
            xnew [j] = x [j] - d [j] ;
        }
        for (; j < n; )
        {
            xnew [j] = x [j] - d [j] ; j++ ;
            xnew [j] = x [j] - d [j] ; j++ ;
            xnew [j] = x [j] - d [j] ; j++ ;
            xnew [j] = x [j] - d [j] ; j++ ;
            xnew [j] = x [j] - d [j] ; j++ ;
        }
    }
    /* else step size is not 1 */
    else
    {
        for (j = 0; j < n5; j++)
        {
            xnew [j] = x [j] + alpha*d [j] ;
        }
        for (; j < n; )
        {
            xnew [j] = x [j] + alpha*d [j] ; j++ ;
            xnew [j] = x [j] + alpha*d [j] ; j++ ;
            xnew [j] = x [j] + alpha*d [j] ; j++ ;
            xnew [j] = x [j] + alpha*d [j] ; j++ ;
            xnew [j] = x [j] + alpha*d [j] ; j++ ;
        }
    }
}

/* ========================================================================== */
/* ====== pproj_saxpy ======================================================= */
/* ========================================================================== */
/* Perform the operation x <- x + s*y */
/* ========================================================================== */

void pproj_saxpy
(
    PPFLOAT *x,
    PPFLOAT *y,
    PPFLOAT  s,
    PPINT    n  /* dimension of the vectors */
)
{
    PPINT n5, i ;
    PPFLOAT *X, *Y ;
    n5 = n % 5 ;
    X = x+n5 ;
    Y = y+n5 ;
    if ( s == PPONE )
    {
        for (i = 0; i < n5; i++) x [i] += y [i] ;
        for (; i < n; i += 5)
        {
            *X++ += *Y++ ;
            *X++ += *Y++ ;
            *X++ += *Y++ ;
            *X++ += *Y++ ;
            *X++ += *Y++ ;
        }
    }
    else
    {
        for (i = 0; i < n5; i++) x [i] += s*y [i] ;
        for (; i < n; i += 5)
        {
            *X++ += s*(*Y++) ;
            *X++ += s*(*Y++) ;
            *X++ += s*(*Y++) ;
            *X++ += s*(*Y++) ;
            *X++ += s*(*Y++) ;
        }
    }
}

/* ========================================================================== */
/* ====== pproj_max ========================================================= */
/* ========================================================================== */
/* Evaluate the absolute maximum element in an array */
/* ========================================================================== */

PPFLOAT pproj_max
(
    PPFLOAT *x,
    PPINT    n  /* dimension of x */
)
{
    PPINT n5, i ;
    PPFLOAT t ;
    n5 = n % 5 ;
    t = PPZERO ;
    for (i = 0; i < n5; i++)
    {
        if ( fabs (x [i]) > t ) t = fabs (x [i]) ;
    }
    for (; i < n; i += 5)
    {
        if ( fabs (x [i]) > t ) t = fabs (x [i]) ;
        if ( fabs (x [i+1]) > t ) t = fabs (x [i+1]) ;
        if ( fabs (x [i+2]) > t ) t = fabs (x [i+2]) ;
        if ( fabs (x [i+3]) > t ) t = fabs (x [i+3]) ;
        if ( fabs (x [i+4]) > t ) t = fabs (x [i+4]) ;
    }
    return (t) ;
}

/* ========================================================================== */
/* ====== pproj_timer ======================================================= */
/* ========================================================================== */
/* Returns the time in seconds used by the process.  */
/* Used in mexFunctions only (not a part of the C-callable UMFPACK) */
/* ========================================================================== */

double pproj_timer ( void )
{
#if 0
    struct rusage ru ;
    double user, tsys ;
    (void) getrusage (RUSAGE_SELF, &ru) ;
    user =
    ru.ru_utime.tv_sec                  /* user time (seconds) */
    + 1e-6 * ru.ru_utime.tv_usec ;      /* user time (microseconds) */

    tsys =
    ru.ru_stime.tv_sec                  /* tsys time (seconds) */
    + 1e-6 * ru.ru_stime.tv_usec ;      /* tsys time (microseconds) */

    return (user + tsys) ;
#endif

    struct timeval tv ;
    double walltime ;

    (void) gettimeofday (&tv, NULL) ;
    walltime = tv.tv_sec + (double) (tv.tv_usec)/1.e6 ;
    return (walltime) ;
}
