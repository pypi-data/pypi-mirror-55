/* =========================================================================
   ======================== CG_DESCENT =====================================
   =========================================================================
       ________________________________________________________________
      |      A conjugate gradient method with guaranteed descent       |
      |                Based on cg_descent version 6.8                 |
      |                                                                |
      |           William W. Hager    and   Hongchao Zhang             |
      |          hager@math.ufl.edu       hozhang@math.lsu.edu         |
      |                   Department of Mathematics                    |
      |                     University of Florida                      |
      |                 Gainesville, Florida 32611 USA                 |
      |                      352-392-0281 x 244                        |
      |                                                                |
      |                 Copyright by William W. Hager                  |
      |                                                                |
      |          http://www.math.ufl.edu/~hager/papers/CG              |
      |                                                                |
      |  Disclaimer: The views expressed are those of the authors and  |
      |              do not reflect the official policy or position of |
      |              the Department of Defense or the U.S. Government. |
      |                                                                |
      |      Approved for Public Release, Distribution Unlimited       |
      |________________________________________________________________|
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

      References:
      1. W. W. Hager and H. Zhang, A new conjugate gradient method
         with guaranteed descent and an efficient line search,
         SIAM Journal on Optimization, 16 (2005), 170-192.
      2. W. W. Hager and H. Zhang, Algorithm 851: CG_DESCENT,
         A conjugate gradient method with guaranteed descent,
         ACM Transactions on Mathematical Software, 32 (2006), 113-137.
      3. W. W. Hager and H. Zhang, A survey of nonlinear conjugate gradient
         methods, Pacific Journal of Optimization, 2 (2006), pp. 35-58.
      4. W. W. Hager and H. Zhang, Limited memory conjugate gradients,
         SIAM Journal on Optimization, 23 (2013), 2150-2168. */

#ifdef PASA
#include "pasa.h"
#else
#include "cg_descent.h"
#endif

int XXCG(descent)
(
    CGdata    *cgdata /* CG data structure */
#ifdef PASA
   ,PASAcom  *pasacom  /* common variables from pasa */
#endif
)
{
    int     IterQuad, QuadF, status,
            mem, memk, mlast, mp, mpp, spp, LBFGS, qrestart ;
    CGINT   i, j, k, IterRestart, maxit, nrestart, nslow, slowlimit ;
    CGFLOAT alpha, alphaold, alphabound, ApproxSwitchFactor, beta, Ck, Qk,
            delta2, denom, dnorm2, dphi, dphi0, dQd, err, f, fbest, fnew,
            gbest, maxstep, scale, ykyk, ykPyk, gkPyk, dkyk ,
            QuadTrust, t, trial, *d, *g,
           *gnew, *gproj, *gnewproj, *Sk, *SkYk, *tau, *work, *Yk, *xnew ;
    CGcom   *cgcom, cgcom_struc ;

    /* limited memory variables */
    int     l1, l2,  memsq, memk_begin, mlast_sub,
            mp_begin, nsub, spp1, SkFstart, SkFlast, Subspace, UseMemory,
            Restart, InvariantSpace,
            IterSubRestart, FirstFull, SubSkip, SubCheck,
            StartSkip, StartCheck, DenseCol1, memk_is_mem, d0isg ;
    CGINT   nrestartsub ;
    CGFLOAT gnorm2, gsubnorm2,  ratio, stgkeep,
            zeta, yty, ytg, t1, t2, t3, t4,
           *D, *Rk, *Re, *SkF, *stemp,
           *dsub, *gsub, *gsubtemp, *gkeep, *vsub, *wsub ;

#ifdef PASA
    int use_penalty ;
    CGINT ni, nrow, p, q, *order ;
    CGFLOAT fp, maxeqerr, penalty, s, *AAd, *gpen, *lambda ;
    const int use_napheap = pasacom->use_napheap ;
    const int use_pproj = pasacom->use_pproj ;
    const int Aexists = pasacom->Aexists ;
#else
    CGFLOAT cgtol, gnorm ;
    const int Aexists = FALSE ;
#endif
    cgcom = &cgcom_struc ;
    cgcom->cgdata = cgdata ;

    /* extract variables from cgdata structure */
    CGFLOAT    *x = cgdata->x ;
    CGINT       n = cgdata->n ;
    CGparm  *Parm = cgdata->Parm ;
    CGstat  *Stat = cgdata->Stat ;
    CGFLOAT *Work = cgdata->Work ;

    /* if n is unassigned, then terminate with error */
    if ( n == EMPTY )
    {
        status = XXCG(wrapup) (CG_N_IS_EMPTY, PASA_CG_COM) ;
        return (status) ;
    }

    /* if x is NULL, then allocate memory and initialize x to zero */
    if ( x == NULL )
    {
        x = (CGFLOAT *) cg_malloc (n*sizeof (CGFLOAT)) ;
        if ( x == NULL )
        {
            status = XXCG(wrapup) (CG_OUT_OF_MEMORY, PASA_CG_COM) ;
            return (status) ;
        }
        cg_initx (x, CGZERO, n) ;
        cgdata->x = cgdata->x_created = x ;
    }

    int const PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 1 )
    {
        printf ("\nSTART CG\n") ;
    }
    CGFLOAT const grad_tol = Parm->grad_tol ;

    /* initialize statistics structure */
    cgcom->Stat = Stat ;
    cgcom->Parm = Parm ;
    cgcom->work_created = NULL ;

    /* determine if the objective is quadratic */
#ifdef PASA
    /* pasa determined this already */
    int const QuadCost = pasacom->QP ;
    cgcom->QuadCost = QuadCost ;
#else
    if ( Parm->PrintParm )
    {
        cg_print_parm (cgdata) ;
    }
    /* cg needs to inspect the input arguments */
    int const QuadCost = ((cgdata->c == NULL) && (cgdata->hprod == NULL)) ?
                                                                  FALSE : TRUE ;
    cgcom->QuadCost = QuadCost ;

    /* in case there is an error, initialize the statistics */
    cgcom->FirstIter = Stat->iter  = 0 ;/* total number of iterations */
    Stat->nfunc = 0 ;   /* number of function evaluations */
    Stat->ngrad = 0 ;   /* number of gradient evaluations */
    Stat->IterSub = 0 ; /* number of iterations in subspace */
    Stat->NumSub =  0 ; /* total number of subspaces */
    cgcom->f = CGINF ;
    Stat->err = CGINF ;

    /* check to see if there is an error in the input arguments */
    if ( QuadCost && cgdata->hprod == NULL )
    {
        status = XXCG(wrapup) (CG_QP_LINEAR_TERM_GIVEN_BUT_HPROD_MISSING,
                                PASA_CG_COM) ;
        return (status) ;
    }
    if ( QuadCost && cgdata->c == NULL )
    {
        status = XXCG(wrapup) (CG_HPROD_GIVEN_BUT_QP_LINEAR_TERM_MISSING,
                                PASA_CG_COM) ;
        return (status) ;
    }
    
#endif

    cgcom->neps = 0 ;
    maxit = Parm->maxit ; /* abort when # iterations reaches maxit */

    /* QuadCost = T => objective is quadratic */
    if ( QuadCost )
    {
        cgcom->QPshift = Parm->QPshift ;
    }
    Stat->maxit = maxit ;
    Stat->NegDiag = FALSE ; /* no negative diagonal element in QR factor */
    Stat->maxsteps = Parm->maxsteps ;
    Stat->cg_ninf_tries = Parm->cg_ninf_tries ;

    /* cgcom structure initialization */
    cgcom->x = x ;
    cgcom->n = n ; /* problem dimension */
    cgcom->approxstep = Parm->approxstep ;
    ApproxSwitchFactor = Parm->ApproxSwitchFactor ;

    fbest = CGINF ; /* stores best function value */
    gbest = CGINF ; /* stores best norm of gradient */
    nslow = 0 ;     /* number of slow iterations */
    slowlimit = 2*n + Parm->nslow ;
    memk = 0 ;      /* number of vectors in subspace current memory */
    cgcom->AvoidFeval = FALSE ;

    Ck = CGZERO ; /* average cost magnitude */
    Qk = CGZERO ; /* used in estimate of average cost magnitude */

    /* limited memory initializations */
    UseMemory = FALSE ;/* => ignore CG memory */
    Subspace = FALSE ; /* => work in full space */
    FirstFull = FALSE ;/* => not first full iteration after leaving subspace */
    Restart = FALSE ;  /* => no restart in limited memory algorithm */
    IterRestart = 0 ; /* counts number of iterations since last restart */
    IterQuad = 0 ;    /* counts number of iterations that function change
                         is close to that of a quadratic */

    /* copy more values from Parm */
    cgcom->pert_eps = Parm->pert_eps ;
    cgcom->PertRule = Parm->PertRule ;
    cgcom->Wolfe    = FALSE ; /* initially a Wolfe line search not performed */
    delta2          = 2*Parm->cgdelta - CGONE ;

    /*  LBFGS = 0 => use cg_descent
                1 => use L-BFGS
                2 => use L-BFGS when LBFGSmemory >= n,
                     use cg_descent when LBFGSmemory < n
                3 => use L-BFGS when LBFGSmemory >= n, use limited
                     memory cg_descent when LBFGSmemory < n */
    LBFGS        = Parm->LBFGS ;


    qrestart     = CGMIN (n, Parm->qrestart) ;
    /* Initially the function is assumed to be not approximately quadratic.
       However, if QuadCost is TRUE, then the value of QuadF is ignored. */
    QuadF = FALSE ;

    /* the conjugate gradient algorithm is restarted every nrestart iteration */
    nrestart = (CGINT) (((CGFLOAT) n)*Parm->restart_fac) ;

    /* adjust LBFGS depending on value of mem */
    mem = Parm->LBFGSmemory ;
    mem = CGMIN (mem, n) ;
    if ( (mem == n) && (LBFGS >= 2) )
    {
        LBFGS = 1 ; /* use LBFGS */
    }
    /* if mem <= 2 and limited memory CG is requested, then switch to
       ordinary CG since the code breaks in Yk update. Note that
       L-BFGS still works with memory = 2, so LBFGS = 1 could be specified. */
    if ( (mem <= 2) && (LBFGS >= 2) )
    {
        mem = 0 ;
        LBFGS = 0 ; /* use cg_descent */
    }
    
    /* memory allocation */
    if ( Work == NULL )
    {
        /* memory for g, d, xnew, gnew */
        i = 4*n ;
        if ( QuadCost == TRUE )
        {
            i += n ;
        }
        if ( LBFGS == 1 ) /* use L-BFGS */
        {
            /* Sk (mem*n), Yk (mem*n), SkYk (mem), tau (mem) */
            i += 2*mem*(n+1) ;
        }
        else if ( LBFGS == 3 )
        {
            /* SkF (mem*n), stemp (n), gkeep (n), Sk (mem*mem), Rk (mem*mem),
               Re (mem+1) Yk (mem*(mem+1) +2), SkYk (mem), tau (mem),
               dsub (mem), gsub (mem+1), wsub (mem+1), vsub (mem),
               gsubtemp (mem) */
            i += (mem+2)*n + (3*mem+9)*mem + 5 ;
        }
        work = (CGFLOAT *) cg_malloc (i*sizeof (CGFLOAT)) ;
        if ( work == NULL )
        {
            status = XXCG(wrapup) (CG_OUT_OF_MEMORY, PASA_CG_COM) ;
            return (status) ;
        }
        cgcom->work_created = work ;
    }
    else
    {
        work = Work ;
    }

#ifndef PASA
    /* running CG by itself, not through PASA */
    cgcom->g    = g    = work ; work += n ;
    cgcom->d    = d    = work ; work += n ;
    cgcom->xnew = xnew = work ; work += n ;
    cgcom->gnew = gnew = work ; work += n ;

    /* with the follows definitions, some formulas work with either
       cg_descent or pasa */
    gproj = g ;
    gnewproj = gnew ;
    D = d ;
    if ( QuadCost == TRUE )
    {
        cgcom->Qd = work ; work += n ;
        cgcom->hprod = cgdata->hprod ;
        cgcom->c = cgdata->c ;
    }
    cgcom->value   = cgdata->value ;
    cgcom->grad    = cgdata->grad ;
    cgcom->valgrad = cgdata->valgrad ;
    t = CGZERO ;
    XXCG(evaluate) (t, &t, "fg", PASA_CG_COM) ;
    f = cgcom->f ;
    if ( (f != f) || (f >= CGINF) || (f <= -CGINF) )
    {
        status = XXCG(wrapup) (CG_STARTING_FUNCTION_VALUE_INFINITE_OR_NAN,
                                PASA_CG_COM) ;
        return (status) ;
    }

    /* set d = -g, compute gnorm  = infinity norm of g and
                           gnorm2 = square of 2-norm of g */
    gnorm = cg_update_inf2 (g, g, d, &gnorm2, n) ;
    Stat->tol = cgtol = CGMAX (gnorm*Parm->StopFac, grad_tol) ;
    Stat->err = gnorm ;
    if ( gnorm <= cgtol )
    {
        status = XXCG(wrapup) (CG_ERROR_TOLERANCE_SATISFIED, PASA_CG_COM) ;
        return (status) ;
    }
    dnorm2 = gnorm2 ;
    dphi0 = -gnorm2 ;

    /* determine starting stepsize */
    alpha = Parm->step ;
    if ( alpha == CGZERO )
    {
        CGFLOAT xnorm ;
        xnorm = cg_inf (x, n) ;
        if ( xnorm == CGZERO )
        {
            if ( f != CGZERO ) alpha = 2.*fabs (f)/gnorm2 ;
            else               alpha = CGONE ;
        }
        else alpha = Parm->psi0*xnorm/gnorm ;
    }
    cgcom->maxstep = maxstep = CGINF ; /* there are no bounds or constraints */

#else
    /* CG is run from PASA */
    Stat->tol = grad_tol ;
    cgcom->FirstIter = Stat->iter ; /* store first iteration */
    pasacom->location = PASA_CG_DESCENT ;
    use_penalty = pasacom->use_penalty ;
    nrow = pasacom->nrow ;
    order = pasacom->order ;
    /* cg_bb_est is initialized to be -1. Its value is reset to an estimate
       for the BB parameter at various places in the code where it is
       easy to generate an estimate */
    pasacom->cg_bb_est = -1.0 ;

    /* If use_penalty is TRUE, then A must exist.
       Check to see if there are active constraints */
    if ( use_penalty == TRUE )
    {
        /* check for an active equality */
        if ( use_pproj == TRUE )
        {
            PPINT *RLinkUp ;
            PPwork *W ;
            W = pasacom->ppcom->Work ;
            RLinkUp = W->RLinkUp ;
            status = ( nrow == RLinkUp [nrow] ) ; /* T => no active equality */
        }
        else /* use_napheap = TRUE */
        {
            status = (pasacom->nap_constraint == 0) ||
                     (pasacom->nap_a2 == CGZERO) ; /* T => no active equality */
        }

        if ( status == TRUE )
        {
            use_penalty = FALSE ;
            pasacom->use_penalty = FALSE ;
        }
        else
        {
            penalty = pasacom->pasaparm->penalty ;
            pasacom->penalty = penalty ;
        }
    }

    /* array allocation */
    g    = cgcom->g    = pasacom->g ;    /* gradient at x */
    d    = cgcom->d    = pasacom->d ;    /* search direction */
    xnew = cgcom->xnew = pasacom->xnew ; /* new x at x + alpha*d */
    gnew = cgcom->gnew = pasacom->gnew ; /* new g at x + alpha*d */
    AAd = NULL ;
    gpen = NULL ;
    if ( Aexists == TRUE )
    {
        if ( use_penalty == TRUE )
        {
             if ( PrintLevel >= 1 )
             {
                 printf ("include penalty term in objective\n") ;
             }
            lambda = pasacom->lambda_pen ;
            gpen = pasacom->gpen ;
            AAd  = work ;  work += n ;
        }
        gproj    = work ;  work += n ;
        gnewproj = work ;  work += n ;
        D        = work ;  work += n ;

        /* print bound rows */
        if ( PrintLevel >= 2 )
        {
            printf ("bound rows:\n") ;
            for (i = 0; i < pasacom->nr; i++)
            {
                j = pasacom->bound_rows [i] ;
                if ( j < 0 )
                {
                    printf ("%ld lower bound\n", (LONG) -(j+1)) ;
                }
                else
                {
                    printf ("%ld upper bound\n", (LONG) (j-1)) ;
                }
            }
        }
    }
    else /* only bound constraints are present */
    {
        gproj = g ;
        gnewproj = gnew ;
        D = d ;
    }

    cgcom->gpen = gpen ;
    cgcom->AAd = AAd ;
    cgcom->approxstep = pasacom->approxstep ;/* PASA overwrites CG start value*/

    /* penalty cost and derivative terms initialized to zero */
    pasacom->fp = CGZERO ; /* value of the penalty function at current iterate*/
    pasacom->dp = CGZERO ; /* derivative of penalty in search direction */
    pasacom->Ad2 = CGZERO ;/* penalty*||Ad||^2 */
    ni = 0 ;               /* no inequality constraints by default */

    /* If use_penalty = TRUE, then compute:
       (1) multiplier estimate lambda = (BB')^{-1}Bg, B = active rows and cols,
       (2) the gradient gpen of the penalty term lambda'(b-Bx) + 0.5p||b-Bx||^2
           gpen = B'(p(Bx-b) - lambda)
       (3) the value of the penalty term fp = lambda'(b-Bx) + 0.5p||b-Bx||^2 */
    fp = CGZERO ;
    maxeqerr = CGZERO ;
#ifndef NOPPROJ
    if ( (use_penalty == TRUE) && (use_pproj == TRUE) )
    {
        PPINT l, *Ap, *Ai, *Anz, *ATp, *ATi, *ir, *RLinkDn, *RLinkUp ;
        PPFLOAT c, *Ax, *ATx, *Axk, *b ;
        PPprob *Prob ;
        PPwork *W ;
        W = pasacom->ppcom->Work ;
        RLinkDn = W->RLinkDn ;
        RLinkUp = W->RLinkUp ;
        Prob = pasacom->ppcom->Prob ;
        b = pasacom->b ;
        Ap = Prob->Ap ;
        Anz = Prob->Anz ;
        Ai = Prob->Ai ;
        Ax = Prob->Ax ;
        pasa_initx (lambda, PASAZERO, nrow) ;
        /* this initx could be replaced by the following more precise
           code, however, valgrind errors could be generated in the back solve
           below since the factorization could have zeros that were not
           squeezed out
        k = nrow ;
        while ( (k = RLinkUp [k]) < nrow )
        {
            lambda [k] = PASAZERO ;
        } */
        for (j = 0; j < n; j++)
        {
            t = g [j] ;
            if ( t != PASAZERO )
            {
                k = Ap [j] ;
                l = k + Anz [j] ;
                for (; k < l; k++)
                {
                    lambda [Ai [k]] += t*Ax [k] ;
                }
            }
        }
        pproj_lsol (W->L, lambda, RLinkUp [nrow], nrow, RLinkUp) ;
        k = RLinkUp [nrow] ;
        /* momentarily set the initial RLinkDn to -1, this simplifies
           indexing in dltsolve */
        RLinkDn [k] = -1 ;
        l = RLinkDn [nrow] ;
        pproj_dltsol (W->L, lambda, lambda, l, k, RLinkDn) ;

        RLinkDn [k] = nrow ; /* restore RLinkDn */

        pasa_initx (gpen, PASAZERO, n) ;
        ATp = W->ATp ;
        ATi = W->ATi ;
        ATx = W->ATx ;
        Axk = pasacom->Axk ;
        ir = W->ir ;
        c = 0.5*penalty ;
        p = 0 ;
        l = 0 ;
        ni = Prob->ni ;
        for (i = 0; i < nrow; i++)
        {
            s = CGZERO ;
            q = ATp [i+1] ;
            for (; p < q; p++)
            {
/*printf ("i: %i j: %i Ax: %e x: %e\n", i, ATi [p], ATx [p], x [ATi [p]]) ;*/
                s += ATx [p]*x [ATi [p]] ;
            }
            if ( ir [i] == 0 )
            {
                t = b [i] - s ;
/*printf ("i: %i lambda: %e Ax-b: %e b: %e\n", i, lambda [i], t, b [i]) ;*/
/*printf ("i: %i t: %25.15e lambda: %25.15e\n", i, t, lambda [i]) ;*/

                fp += t*(c*t + lambda [i]) ;
                s = -(penalty*t + lambda [i]) ;
                t = fabs (t) ;
                maxeqerr = CGMAX (t, maxeqerr) ;
                p = ATp [i] ;
                for (; p < q; p++)
                {
                    gpen [ATi [p]] += ATx [p]*s ;
                }
            }
            else
            {
                ASSERT (ir [i] > ni) ;
                l++ ;
                Axk [l] = s ;
            }
        }
        ASSERT (l == ni) ;
        cgcom->maxeqerr = maxeqerr ;
        if ( QuadCost == FALSE )
        {
            /* Save function value before adding the penalty term to it.  */
            pasacom->f_orig = pasacom->f ;
            pasacom->f += fp ;
        }
        /* else if QuadCost = TRUE, then pasacom->f is unchanged */
    }
    else if ( (use_penalty == TRUE) && (use_napheap == TRUE) )
    {
        PASAFLOAT c, *a ;

        a = pasacom->nap_a ;
        /* multiplier estimate = a'g/a'a */
        const CGFLOAT Lambda = pasa_dot (a, g, n)/pasacom->nap_a2 ;
        *lambda = Lambda ;
        c = 0.5*penalty ;
        s = pasa_dot (a, x, n) ;
        t = pasacom->nap_bl - s ;
        cgcom->maxeqerr = fabs (t) ;
/*printf ("i: %i lambda: %e Ax-b: %e b: %e\n", i, lambda [i], t, b [i]) ;*/
/*printf ("i: %i t: %25.15e lambda: %25.15e\n", i, t, lambda [i]) ;*/

        fp = t*(c*t + Lambda) ;
        s = -(penalty*t + Lambda) ;
        pasa_scale (gpen, a, s, n) ;
        if ( QuadCost == FALSE )
        {
            /* Save function value before adding the penalty term to it.  */
            pasacom->f_orig = pasacom->f ;
            pasacom->f += fp ;
        }
        /* else if QuadCost = TRUE, then pasacom->f is unchanged */
    }
    else if ( (Aexists == TRUE) && (use_pproj == TRUE) )
    {
        PPprob *Prob ;
        PPwork *W ;
        PPINT row, *ineq_row, *ATp, *ATi ;
        PPFLOAT *ATx, *Axk ;
        /* Compute A*x for the inactive inequalities */
        Prob = pasacom->ppcom->Prob ;
        ni = Prob->ni ;
        if ( ni > 0 )
        {
            ineq_row = Prob->ineq_row ;
            W = pasacom->ppcom->Work ;
            ATp = W->ATp ;
            ATi = W->ATi ;
            ATx = W->ATx ;
            Axk = pasacom->Axk ;
            for (i = 1; i <= ni; i++)
            {
                row = ineq_row [i] ;
                s = CGZERO ;
                q = ATp [row+1] ;
                for (p = ATp [row]; p < q; p++)
                {
                    s += ATx [p]*x [ATi [p]] ;
                }
                Axk [i] = s ;
            }
        }
    }
    else if ( (Aexists == TRUE) && (use_napheap == TRUE) )
    {
        if ( pasacom->nap_constraint == 0 )
        {
            pasacom->Axk [1] = pasa_dot (pasacom->nap_a, x, n) ;
        }
    }
#endif

    pasacom->fp = fp ;
    cgcom->f = f = pasacom->f ;

    /* Compute projected gradient and store in gproj.
       gproj is the projection of the total gradient g + gpen */
    pasa_null_project (gproj, g, gpen, TRUE, pasacom) ;

    /* see if the convergence tolerance is satisfied */
    if ( pasacom->e <= pasacom->testtol )
    {
        status = XXCG(checktol) (x, PASA_CG_COM) ;
        if ( (status == PASA_ERROR_TOLERANCE_SATISFIED) ||
             (status == PASA_GRAD_PROJ) )
        {
            status = XXCG(wrapup) (status, PASA_CG_COM) ;
            return (status) ;
        }
        Stat->tol = pasacom->testtol ;
    }

    /* D is the search direction before the final projection */
    cg_scale (D, gproj, -CGONE, n) ;

    /* d is the final search direction */
    pasa_null_project (d, D, NULL, FALSE, pasacom) ;

    /* derivative in search direction without penalty term */
    dphi0 = cg_dot (g, d, n) ;
    if ( use_penalty == TRUE )
    {
        pasacom->dp = cg_dot (gpen, d, n) ;
    }
    dnorm2 = cg_dot (d, d, n) ;         /* square of 2-norm of d */

    alpha = pasacom->bbk ; /* starting step in cg is previous bb step */
    scale = pasacom->bbk ; /* scale is the approximation to inverse
                              Hessian in LBFGS */
/* end of pasa initialization */
#endif

    if ( LBFGS == 1 ) /* allocate storage connected with LBFGS */
    {
        if ( PrintLevel >= 1 )
        {
            printf ("use LBFGS, dimension %ld\n", (LONG) n) ;
        }
        LBFGS = TRUE ;      /* use L-BFGS */
        mlast = -1 ;
        Sk = work ;    work += mem*n ;
        Yk = work ;    work += mem*n ;
        SkYk = work ;  work += mem ;
        tau = work ;   work += mem ;
    }

    else if ( LBFGS == 3) /* allocate storage connected with limited memory CG*/
    {
        if ( PrintLevel >= 1 )
        {
            printf ("use Limited Memory CG, dimension %ld\n", (LONG) n) ;
        }
        UseMemory = TRUE ;            /* previous search direction is saved */
        SubSkip = 0 ;                 /* # iterations to skip checking memory*/
        SubCheck = mem*Parm->SubCheck;/* number of iterations to check */
        StartCheck = Stat->iter ;     /* start checking memory at initial iter*/
        InvariantSpace = FALSE ;      /* iterations not in invariant space */
        FirstFull = TRUE ;            /* first iteration in full space */
        nsub = 0 ;                    /* initial subspace dimension */
        memsq = mem*mem ;
        SkF = work ;   work += mem*n ;/* directions in memory (x_k+1 - x_k) */
        stemp = work ; work += n ;    /* stores x_k+1 - x_k */
        gkeep = work ; work += n ;    /* store grad when 1st direction != -g */
        Sk = work ;    work += memsq ;/* Sk = Rk at start LBFGS in subspace */
        Rk = work ;    work += memsq ;/* upper triangular factor in SkF=Zk*Rk*/
        Re = work ;    work += mem+1 ;/* end column of Rk, for new direction*/
        Yk = work ;    work += memsq+mem+2 ;
        SkYk = work ;  work += mem ;  /* dot products sk'yk in the subspace */
        tau = work ;   work += mem ;  /* stores alpha in Nocedal and Wright */
        dsub = work ;  work += mem ;  /* direction projection in subspace */
        gsub = work ;  work += mem+1 ;/* gradient projection in subspace */
        wsub = work ;  work += mem+1 ;/* work array for triangular solve */
        vsub = work ;  work += mem ;  /* work array for triangular solve */
        gsubtemp = work ; work += mem;/* new gsub before update */

        cg_initx (Rk, CGZERO, memsq) ; /* initialize Rk to 0 */
    }

    cgcom->f0 = f + f ;
    cgcom->SmallCost = fabs (f)*Parm->SmallCost ;
    cgcom->df0 = -2.0*fabs(f)/alpha ;


    /* Start the conjugate gradient iteration.
       alpha starts as old step, ends as final step for current iteration
       f is function value for alpha = 0
       QuadOK = TRUE means that a quadratic step was taken */

    while ( Stat->iter < maxit )
    {
#ifdef PASA
#ifndef NDEBUG
        pasa_check_feas (pasacom) ;
#endif
        maxstep = XXCG(maxstep) (pasacom, cgcom) ;
        /* iterate hits boundary immediately if maxstep = 0 */
        if ( maxstep == CGZERO )
        {
            /* cg hits boundary of the feasible region, restart cg_descent*/
            status = XXCG(wrapup) (CG_HITS_BOUNDARY, PASA_CG_COM) ;
            return (status) ; /* restart cg_descent */
        }
        err = pasacom->e ;
#else
        err = gnorm ;
#endif

        Stat->iter++ ;
        /* save old alpha to simplify formula computing subspace direction */
        alphaold = alpha ;
        if ( PrintLevel >= 2 )
        {
            printf ("CG iter: %ld f: %25.15e err: %e memk: %i\n",
                   (LONG) Stat->iter, f, err, memk) ;
        }
        if ( QuadCost == TRUE )
        {
            cgcom->f0 = f ; /* save prior function value */
#ifdef PASA
            t = -CGONE ;
            status = pasa_evaluate (CGZERO, &t, pasacom, "fg") ;
            if ( status == PASA_FUNCTION_NAN_OR_INF )
            {
                XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }
            if ( order != NULL )
            {
                dQd = PASAZERO ;
                /* dQd = pasa_dot (d, cgcom->>Qd, n) but Qd is in user's coor */
                for (j = 0; j < n; j++)
                {
                    dQd += d [j]*pasacom->Qd [order [j]] ;
                }
            }
            else /* no bounds, no linear constraints, no fixed variables */
            {
                dQd = pasa_dot (d, pasacom->Qd, n) ;
            }
            /* when dQd = 0, we take the max step along the search direction */
            if ( dQd + pasacom->Ad2 <= CGZERO )
            {
                if ( PrintLevel >= 2 )
                {
                    printf ("dQd = %e <= 0, take maxstep\n", dQd) ;
                }
                if ( maxstep >= CGINF ) /* unbounded objective */
                {
                    status = CG_QUADRATIC_OBJECTIVE_NO_LOWER_BOUND ;
                    XXCG(wrapup) (status, PASA_CG_COM) ;
                    return (status) ;
                }
                alpha = maxstep ;
            }
            else /* compute the exact minimizer in search direction */
            {
                alpha = -(dphi0+pasacom->dp)/(dQd + pasacom->Ad2) ;
            }
/*printf ("maxstep: %25.15e alpha: %25.15e\n", maxstep, alpha) ;*/
            if ( alpha >= maxstep ) /* hits boundary */
            {
                if ( PrintLevel >= 1 )
                {
                    printf ("cg hits boundary in QuadCost\n") ;
                }
                /* take maxstep and return */
                cg_step (x, x, d, maxstep, n) ;

                pasacom->f += maxstep*(0.5*dQd*maxstep + dphi0) ;

                /* update gradient */
                pasa_step (pasacom->gtot, pasacom->gtot, pasacom->Qd,
                           maxstep, pasacom->ncol);

                /* copy relevant part of gtot into g */
                if ( order != NULL )
                {
                    pasa_convert_to_pproj (g, pasacom->gtot, order, n) ;
                }
                else /* TODO: gtot can be eliminated when no constraints */
                {
                    pasa_copyx (g, pasacom->gtot, n) ;
                }
#ifndef NDEBUG
        pasa_check_feas (pasacom) ;
#endif
                /* cg hits boundary of the feasible region, restart cg_descent*/
                status = XXCG(wrapup) (CG_HITS_BOUNDARY, PASA_CG_COM) ;
                return (status) ; /* restart cg_descent */
            }
            /* take the step alpha */

            cg_step (xnew, x, d, alpha, n) ;

            /* update cost */
            pasacom->f -= 0.5*dphi0*dphi0/dQd ;
            cgcom->f = pasacom->f ;

            /* update gradient */
            pasa_step (pasacom->gtot, pasacom->gtot, pasacom->Qd,
                       alpha, pasacom->ncol) ;

            /* copy relevant part of gtot into gnew */
            if ( order != NULL )
            {
                pasa_convert_to_pproj (gnew, pasacom->gtot, order, n) ;
            }
            else
            {
                pasa_copyx (gnew, pasacom->gtot, n) ;
            }

            /* compute the derivative in the search direction */
            cgcom->df = pasa_dot (gnew, d, n) ;

            cgcom->QuadOK = TRUE ;
            cgcom->alpha = alpha ;
            status = CG_WOLFE_OK ;
#else
            /* CG is not being used with pasa */
            t = -CGONE ;
            XXCG(evaluate) (t, &t, "fg", PASA_CG_COM) ;
            dQd = cg_dot (d, cgcom->Qd, n) ;
            if ( dQd <= CGZERO )
            {
                status = CG_QUADRATIC_OBJECTIVE_NO_LOWER_BOUND ;
                XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }

            /* compute the exact minimizer in search direction */
            alpha = -dphi0/dQd ;

            /* take the step alpha */
            cg_step (xnew, x, d, alpha, n) ;

            /* update cost */
            cgcom->f -= 0.5*dphi0*dphi0/dQd ;

            /* update gradient */
            cg_step (gnew, g, cgcom->Qd, alpha, n) ;

            /* compute the derivative in the search direction */
            cgcom->df = cg_dot (gnew, d, n) ;
            cgcom->QuadOK = TRUE ;
            cgcom->alpha = alpha ;
            status = CG_WOLFE_OK ;
#endif
        }
        else /* general nonlinear objective */
        {
#ifdef PASA
            dphi0 += pasacom->dp ;
#endif
            /* will store that point where f or df is evaluated */
            cgcom->f_at = -CGONE ;
            cgcom->df_at = -CGONE ;
            cgcom->QuadOK = FALSE ;

            alpha *= Parm->psi2 ;
            if ( f != CGZERO )
            {
                t = fabs ((f-cgcom->f0)/f) ;
            }
            else
            {
                t = CGONE ;
            }
            cgcom->UseCubic = TRUE ;
            if ( (t < Parm->CubicCutOff) || !Parm->UseCubic )
            {
                cgcom->UseCubic = FALSE ;
            }
            if ( Parm->QuadStep )
            {
                /* test if quadratic interpolation step should be tried */
                if ( ((t > Parm->QuadCutOff)&&(fabs(f) >= cgcom->SmallCost))
                      || QuadF )
                {
                    if ( QuadF ) /* the function is approximately quadratic */
                    {
                        alpha *= Parm->psi1 ;
#ifdef PASA
                        /* truncate the nominal step if it exceeds maxstep */
                        if ( alpha >= maxstep )
                        {
                            alpha = maxstep ;
                        }
#endif
                        t = alpha ;
                        status = XXCG(evaluate) (CGZERO,&alpha,"g",PASA_CG_COM);
                        /* alpha may decrease if df is infinite or nan */
                        if ( status == CG_FUNCTION_NAN_OR_INF )
                        {
                            XXCG(wrapup) (status, PASA_CG_COM) ;
                            return (status) ;
                        }
                        cgcom->df_at = alpha ;

                        /* if stepsize reduced due to infinite function values
                           store the valid stepsize */
                        if ( alpha < t )
                        {
                            alphabound = alpha ;
                        }
                        else
                        {
                            alphabound = CGINF ;
                        }

                        /* secant approximation to step */
                        if ( cgcom->df > dphi0 )
                        {
                            alpha = -dphi0/((cgcom->df-dphi0)/alpha) ;
                            cgcom->QuadOK = TRUE ;
                        }
                        else if ( LBFGS == 1 )
                        {
                            if ( memk >= n )
                            {
                                alpha = CGONE ;
                                cgcom->QuadOK = TRUE ;
                            }
                            else
                            {
                                alpha = 2. ;
                            }
                        }
                        else if ( Subspace )
                        {
                            if ( memk >= nsub )
                            {
                                alpha = CGONE ;
                                cgcom->QuadOK = TRUE ;
                            }
                            else  alpha = 2. ;
                        }
                    }
                    else /* not approximately quadratic */
                    {
                        /* Attempt a quadratic quadratic interpolation step
                           based on the starting function value and derivative,
                           and the function value at the point "trial" below.
                           If the step is successful in the sense that the
                           quadratic is convex, then keep a safeguarded
                           version of the step. Otherwise, retain the
                           original alpha. */
                        t = CGMAX (Parm->psi_lo, cgcom->df0/(dphi0*Parm->psi2));
                        trial = alpha*CGMIN (t, Parm->psi_hi) ;
#ifdef PASA
                        /* truncate the nominal step if it exceeds maxstep */
                        if ( trial >= maxstep )
                        {
                            trial = maxstep ;
                        }
#endif
                        t = trial ;
                        status = XXCG(evaluate) (CGZERO,&trial,"f",PASA_CG_COM);
                        /* trial may decrease if f is infinite or nan */
                        if ( status == CG_FUNCTION_NAN_OR_INF )
                        {
                            XXCG(wrapup) (status, PASA_CG_COM) ;
                            return (status) ;
                        }
                        cgcom->f_at = trial ;

                        /* if stepsize reduced due to infinite function values
                           store the valid stepsize */
                        if ( trial < t )
                        {
                            alphabound = trial ;
                        }
                        else
                        {
                            alphabound = CGINF ;
                        }
                        fnew = cgcom->f ;
                        denom = 2.*(((fnew-f)/trial)-dphi0) ;
                        if ( denom > CGZERO ) /* convex quadratic */
                        {
                            /* t = quadratic interpolation iterate */
                            t = -dphi0*trial/denom ;
                            /* safeguard */
                            if ( fnew >= f )
                            {
                                alpha = CGMAX (t, trial*Parm->QuadSafe) ;
                            }
                            else
                            {
                                alpha = t ;
                            }
                            cgcom->QuadOK = TRUE ;
                        }
                        else /* quadratic is concave */
                        {
                            if ( (trial > alpha) &&
                               (fabs(fnew-f) > ApproxSwitchFactor*Ck) )
                            {
                                alpha = trial ;
                            }
                        }
                    }
                    if ( PrintLevel >= 2 )
                    {
                        if ( denom <= CGZERO )
                        {
                            printf("Quad step fails (denom = %14.6e)\n", denom);
                        }
                        else if ( cgcom->QuadOK )
                        {
                            printf ("Quad step %14.6e OK\n",
                                     CGMIN (alpha, maxstep));
                        }
                        else
                        {
                            printf ("Quad step %14.6e done, but not OK\n",
                                     CGMIN (alpha, maxstep)) ;
                        }
                    }
                }
                else if ( PrintLevel >= 2 )
                {
                    printf ("No quad step (chg: %14.6e, cut: %10.2e)\n",
                             t, Parm->QuadCutOff) ;
                }
            }
            if ( alpha > maxstep )
            {
                alpha = maxstep ;
                cgcom->QuadOK = FALSE ;
            }
            if ( alpha > alphabound )
            {
                alpha = alphabound ;
                cgcom->QuadOK = FALSE ;
            }

            cgcom->f0 = f ;                        /* f0 saved as prior value */
            cgcom->df0 = dphi0 ;
 
            if ( cgcom->PertRule == TRUE )
            {
                cgcom->fpert = f + cgcom->pert_eps*fabs (f) ;
            }
            else 
            {
                cgcom->fpert = f + cgcom->pert_eps ;
            }

            cgcom->wolfe_hi = Parm->cgdelta*dphi0 ;
            cgcom->wolfe_lo = Parm->cgsigma*dphi0 ;
            cgcom->awolfe_hi = delta2*dphi0 ;
            cgcom->alpha = alpha ;

            /* perform line search */
            status = XXCG(line) (FALSE, PASA_CG_COM) ;
            if ( status == CG_FUNCTION_NAN_OR_INF )
            {
                XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }

#ifdef PASA
            /* cg hits boundary of the feasible region, restart cg_descent*/
            if ( status == CG_HITS_BOUNDARY )
            {
                if ( PrintLevel >= 1 )
                {
                     printf ("cg hits boundary in line search\n") ;
                }
                cg_copy (x, xnew, n) ;
                cg_copy (g, gnew, n) ;
                status = XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ; /* restart cg_descent */
            }
#endif
    
            /*try approximate Wolfe line search if ordinary Wolfe fails */
            if ( (status != CG_WOLFE_OK) && !cgcom->approxstep )
            {
                if ( PrintLevel >= 1 )
                {
                     printf ("\nWOLFE LINE SEARCH FAILS\n") ;
                }
                if ( status != CG_SLOPE_ALWAYS_NEGATIVE )
                {
                    cgcom->approxstep = TRUE ;
                    cgcom->alpha = alpha ;
                    status = XXCG(line) (TRUE, PASA_CG_COM) ;
                    if ( status == CG_FUNCTION_NAN_OR_INF )
                    {
                        XXCG(wrapup) (status, PASA_CG_COM) ;
                        return (status) ;
                    }
                }
            }
        }

        /* parameters in Wolfe, approximate Wolfe conditions, and update */
        Qk = Parm->Qdecay*Qk + CGONE ;
        cgcom->Ck = Ck = Ck + (fabs (f) - Ck)/Qk ; /* average cost magnitude */

        alpha = cgcom->alpha ;
        f = cgcom->f ;
        dphi = cgcom->df ;

        if ( status != CG_WOLFE_OK ) /* line search fails */
        {
            XXCG(wrapup) (status, PASA_CG_COM) ;
            return (status) ;
        }

#ifdef PASA
        /* update the penalty gradient if penalty term present */
#ifndef NOPPROJ
        if ( use_penalty == TRUE )
        {
            pproj_saxpy (gpen, AAd, alpha*penalty, n) ;
            pasacom->fp += alpha*(pasacom->dp + 0.5*alpha*pasacom->Ad2);
        }

        /* update A*xk based on the current stepsize:
           new Axk = old Axk + alpha * Adk */
        if ( ni > 0 )
        {
            cg_daxpy (pasacom->Axk+1, pasacom->Adk+1, alpha, ni) ;
        }
#endif
#endif

        if ( QuadCost == FALSE )
        {
            /* test how close the cost function changes are to that of a
               quadratic QuadTrust = 0 means the function change matches
               that of a quadratic*/
            t = alpha*(dphi+dphi0) ;
            if ( fabs (t) <= Parm->qeps*CGMIN (Ck, CGONE) )
            {
                QuadTrust = CGZERO ;
            }
            else
            {
                QuadTrust = fabs((2.0*(f-cgcom->f0)/t)-CGONE) ;
            }
            if ( QuadTrust <= Parm->qrule)
            {
                IterQuad++ ;
            }
            else 
            {
                IterQuad = 0 ;
            }

            if ( IterQuad == qrestart )
            {
                QuadF = TRUE ;
            }

            /* as function values converge, they contain less information
               and are avoided when possible in the line search */
            cgcom->AvoidFeval = FALSE ;
            if ( fabs (f-cgcom->f0) <= Parm->CostConverge*fabs (f) )
            {
                cgcom->AvoidFeval = TRUE ;
            }

            /* check whether to change to approximate Wolfe line search */
            if ( !cgcom->approxstep )
            {
                if ( fabs (f-cgcom->f0) < ApproxSwitchFactor*Ck )
                {
                    if ( PrintLevel >= 1 )
                    {
                         printf ("change to approximate Wolfe line search\n") ;
                    }
                    cgcom->approxstep = TRUE ;
                    if ( cgcom->Wolfe == TRUE )
                    {
                        Restart = TRUE ;
                    }
                }
            }
        }

        IterRestart++ ;

        /* some bookkeeping for limited memory CG */
        if ( LBFGS == 3 )
        {
            if ( UseMemory == TRUE )
            {
                if ( (Stat->iter - StartCheck > SubCheck) && !Subspace )
                {
                    StartSkip = Stat->iter ;
                    UseMemory = FALSE ;
                    if ( SubSkip == 0 ) SubSkip = mem*Parm->SubSkip ;
                    else                SubSkip *= 2 ;
                    if ( PrintLevel >= 1 )
                    {
                        printf ("skip subspace %i iterations\n", SubSkip) ;
                    }
                }
            }
            else
            {
                if ( Stat->iter - StartSkip > SubSkip )
                {
                    StartCheck = Stat->iter ;
                    UseMemory = TRUE ;
                    memk = 0 ;
                }
            }
        }

        /* if we do not plan to do a restart, put the projection of gnew
           into gnewgproj, otherwise put it into gproj */
        if ( ((LBFGS == 1) && (IterRestart == nrestart)) ||
             (((LBFGS == 0) || (LBFGS == 2) ||
               ((LBFGS == 3) && (UseMemory == FALSE)))
                           && ((IterRestart >= nrestart) ||
                     ((IterQuad == qrestart) && (IterQuad != IterRestart)))) )
        {
            /* project gnew into the null space of the active
               constraint gradients and store projection in gproj */
#ifdef PASA
            pasa_null_project (gproj, gnew, gpen, TRUE, pasacom) ;
#endif
            if ( LBFGS == 3 )
            {
                Restart = TRUE ;
            }
        }
#ifdef PASA
        else /* no restart */
        {
            /* project gnew into the null space of the active
               constraint gradients and store projection in gnewproj */
            pasa_null_project (gnewproj, gnew, gpen, TRUE, pasacom) ;
        }

        if ( PrintLevel >= 2 )
        {
            printf ("Local error: %e testtol: %e Global error: %e\n",
                    pasacom->e, pasacom->testtol, pasacom->E) ;
        }
        /* test nominal stopping condition */
        if ( pasacom->e <= pasacom->testtol )
        {
            status = XXCG(checktol) (xnew, pasacom, cgcom) ;
            if ( (status == PASA_ERROR_TOLERANCE_SATISFIED) ||
                 (status == PASA_GRAD_PROJ) )
            {
                /* set x = xnew, g = gnew */
                cg_copy (x, xnew, n) ;
                cg_copy (g, gnew, n) ;
                status = XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }
            Stat->tol = pasacom->testtol ;
            if ( status == CG_RESTART )
            {
                /* since the penalty term was updated, resave cost and gproj */
                f = pasacom->f ;
                IterRestart = nrestart ;
                if ( (Aexists == TRUE) && (use_penalty == TRUE) )
                {
                     pasa_null_project (gproj, gnew, gpen, TRUE, pasacom) ;
                }
            }
        }
#else
        /* stand alone cg, no pasa */
        t = gnorm ;
        Stat->err = gnorm = cg_inf (gnew, n) ;
        if ( gnorm <= cgtol )
        {
            cg_copy (x, xnew, n) ;
            status = XXCG(wrapup) (CG_ERROR_TOLERANCE_SATISFIED, PASA_CG_COM) ;
            return (status) ;
        }
        /* for a quadratic objective, both the function value and gradient
           are evaluated by an update process. If the gradient shows a big
           drop, then re-evaluate objective value and gradient to
           maintain accuracy */
        if ( (gnorm <= 1.e-3*t) && (QuadCost == TRUE) )
        {
            if ( PrintLevel >= 1 )
            {
                printf ("re-evaluate quadratic objective and gradient\n") ;
            }
            cgcom->x = xnew ;
            cgcom->g = gnew ;
            t = CGZERO ;
            XXCG(evaluate) (t, &t, "fg", PASA_CG_COM) ;
            f = cgcom->f ;
            cgcom->x = x ;
            cgcom->g = g ;
        }
#endif

        /* compute search direction */
        if ( LBFGS == 1 )
        {
            if ( IterRestart >= nrestart ) /* restart the l-bfgs method */
            {
                if ( PrintLevel >= 1 )
                {
                    printf ("REstart LBFGS\n") ;
                }
                IterRestart = 0 ;
                IterQuad = 0 ;
                mlast = -1 ;
                memk = 0 ;
                scale = (CGFLOAT) 1 ;

                /* copy xnew to x */
                cg_copy (x, xnew, n) ;

                /* for a quadratic objective, evaluate objective
                   and its gradient from scratch */
                if ( QuadCost == TRUE )
                {
                    t = CGZERO ;
                    XXCG(evaluate) (t, &t, "fg", PASA_CG_COM) ;
                }
                else
                {
                    /* copy gnew to g */
                    cg_copy (g, gnew, n) ;
                }

                /* D = -g or -gproj, search direction before final projection */
                cg_scale (D, gproj, -CGONE, n) ;

#ifdef PASA
                /* d is the final search direction */
                pasa_null_project (d, D, NULL, FALSE, pasacom) ;
                pasacom->cg_bb_est = scale ;
#endif

                /* derivative in search direction without penalty term */
                dphi0  = cg_dot (g, d, n) ;
/*printf ("dphi0: %e\n", dphi0 + pasacom->dp) ;*/
            }
            else
            {
                if ( PrintLevel >= 2 )
                {
                    printf ("ordinary LBFGS update\n") ;
                }
                mlast = (mlast+1) % mem ;
                spp = mlast*n ;
                cg_scale (Sk+spp, D, alpha, n) ;

                /* copy xnew to x */
                cg_copy (x, xnew, n) ;

                cg_step (Yk+spp, gnewproj, gproj, -CGONE, n) ;

                /* copy gnew to g */
                cg_copy (g, gnew, n) ;

                if ( Aexists == TRUE )
                {
                    cg_copy (gproj, gnewproj, n) ;
                    cg_copy (gnew, gnewproj, n) ;
                }

                SkYk [mlast] = alpha*(dphi-dphi0) ;
                if (memk < mem)
                {
                    memk++ ;
                }

                /* calculate Hg = H g, saved in gnew */
                mp = mlast ;  /* memk is the number of vectors in the memory */
                for (j = 0; j < memk; j++)
                {
                    mpp = mp*n ;
                    t = cg_dot (Sk+mpp, gnew, n)/SkYk[mp] ;
                    tau [mp] = t ;
                    cg_daxpy (gnew, Yk+mpp, -t, n) ;
                    mp -=  1;
                    if ( mp < 0 )
                    {
                        mp = mem-1 ;
                    }
                }
                ykyk = cg_dot (Yk+spp, Yk+spp, n) ;
                if ( ykyk > CGZERO ) /* compute new approx to inverse Hessian */
                {
                    scale = SkYk[mlast]/ykyk ;/* approximates inverse Hessian */
#ifdef PASA
                    pasacom->cg_bb_est = scale ;
#endif
                }

                cg_scale (gnew, gnew, scale, n) ;

                for (j = 0; j < memk; j++)
                {
                    mp +=  1 ;
                    if ( mp == mem )
                    {
                        mp = 0 ;
                    }
                    mpp = mp*n ;
                    t = cg_dot (Yk+mpp, gnew, n)/SkYk[mp] ;
                    cg_daxpy (gnew, Sk+mpp, tau [mp]-t, n) ;
                }
                cg_scale (D, gnew, -CGONE, n) ;
#ifdef PASA
                /* transform back to x-space */
                pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

                dphi0 = cg_dot (g, d, n) ;
            }
        } /* end of LBFGS */
        else if ( LBFGS == 0 || LBFGS == 2 ) /* search direction by cg formula*/
        {

            /* check to see whether cg should be restated */
            if ( (IterRestart >= nrestart) || ((IterQuad == qrestart)
                                           && (IterQuad != IterRestart)) )
            {
                if ( PrintLevel >= 1 )
                {
                    printf ("Restart CG\n") ;
                }

                IterRestart = 0 ;
                IterQuad = 0 ;
                beta = CGZERO ;
                scale = (CGFLOAT) 1 ;

                /* set x = xnew, g = gnew */
                cg_copy (x, xnew, n) ;

                /* for a quadratic objective, evaluate objective
                   and its gradient from scratch when restart is performed */
                if ( QuadCost == TRUE )
                {
                    t = CGZERO ;
                    XXCG(evaluate) (t, &t, "fg", PASA_CG_COM) ;
                }
                else
                {
                    /* copy gnew to g */
                    cg_copy (g, gnew, n) ;
                }

                /* D is the search direction before the final projection */
                cg_scale (D, gproj, -CGONE, n) ;

#ifdef PASA
                pasacom->cg_bb_est = scale ;
                /* d is the final search direction */
                pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

                /* compute square of 2-norm of d (used in bb formula) */
                dnorm2 = cg_dot (d, d, n) ;

                /* derivative in search direction without penalty term */
                dphi0  = cg_dot (g, d, n) ;
            }
            else /* ordinary cg update without restart */
            {
                if ( PrintLevel >= 2 )
                {
                    printf ("ordinary cg update\n") ;
                }
                /* set x = xnew */
                cg_copy (x, xnew, n) ;

                /* compute: ykPyk  = (newproj - oldproj)*(newproj - oldproj),
                            gkPyk  =  newproj           *(newproj - oldproj)
                   update: oldproj = newproj */
                cg_update_beta (gproj, gnewproj, &gkPyk, &ykPyk, n) ;
                dkyk = dphi - dphi0 ;

#ifdef PASA
                /* For bound constrained problems, we set g = gnew in
                   update_beta since g = gproj and gnew = gnewproj.
                   When linear constraints present, we need to set g = gnew. */
                if ( Aexists == TRUE )
                {
                    cg_copy (g, gnew, n) ;
                }
                pasacom->cg_bb_est = alpha*dnorm2/dkyk ;
#endif


                if ( Parm->AdaptiveTheta )
                {
                    t = 2. - CGONE/(0.1*QuadTrust + CGONE) ;
                }
                else
                {
                    t = Parm->theta ;
                }
                beta = (gkPyk - t*dphi*ykPyk/dkyk)/dkyk ;

                /* faster: initialize dnorm2 = gnorm2 at start, then
                           dnorm2 = gnorm2 + beta**2*dnorm2 - 2.*beta*dphi
                           gnorm2 = ||g_{k+1}||^2
                           dnorm2 = ||d_{k+1}||^2
                           dpi = g_{k+1}' d_k */

                /* lower bound for beta is BetaLower*d_k'g_k/ ||d_k||^2 */
                beta = CGMAX (beta, Parm->BetaLower*dphi0/dnorm2) ;

                /* update search direction D = -gproj + beta*Dold */
                cg_update_d (D, gproj, beta, n) ;

#ifdef PASA
                /* project D into null space to obtain search direction */
                pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

                /* derivative in the new search direction */
                dphi0 = cg_dot (d, g, n) ;

                dnorm2 = cg_dot (d, d, n) ;
            }
        }   /* search direction by cg formula has been computed */
        else /* LBFGS = 3, limited memory CG formula */
        {
            if ( UseMemory == FALSE )
            {
                if ( (IterRestart >= nrestart) || ((IterQuad == qrestart)
                     && (IterQuad != IterRestart)) )
                {
                    Restart = TRUE ;
                }
            }
            else
            {
                if ( Subspace ) /* the iteration is in the subspace */
                {
                    IterSubRestart++ ;
                    if ( PrintLevel >= 2 )
                    {
                        printf ("iteration in subspace, IterSubRestart: %i\n",
                                 IterSubRestart) ;
                    }

                    /* compute projection of g into subspace */
                    gsubnorm2 = CGZERO ;
                    mp = SkFstart ;
                    j = nsub - mp ;

                    /* multiply basis vectors by new gradient */
                    cg_matvec (wsub, SkF, gnewproj, nsub, n, 0) ;

                    /* rearrange wsub and store in gsubtemp
                       (elements associated with old vectors should
                        precede elements associated with newer vectors */
                    cg_copy0 (gsubtemp, wsub+mp, j) ;
                    cg_copy0 (gsubtemp+j, wsub, mp) ;

                    /* solve Rk'y = gsubtemp */
                    cg_trisolve (gsubtemp, Rk, mem, nsub, 0) ;
                    gsubnorm2 = cg_dot0 (gsubtemp, gsubtemp, nsub) ;
                    /*  gnorm2 = cg_dot (gtemp, gtemp, n) ; */

                    gnorm2 = cg_dot (gnewproj, gnewproj, n) ;
                    ratio = sqrt(gsubnorm2/gnorm2) ;
                    if ( ratio < CGONE - Parm->eta1  )  /* Exit Subspace */
                    {
                       if ( PrintLevel >= 1 )
                       {
                           printf ("CG iter: %li exit subspace ratio: %e "
                                   "eta1: %e\n",
                                   (LONG) Stat->iter, ratio, Parm->eta1) ;
                       }
                       FirstFull = TRUE ; /* first iteration in full space */
                       Subspace = FALSE ; /* leave the subspace */
                       InvariantSpace = FALSE ;
                       /* check the subspace condition for SubCheck iterations
                          starting from the current iteration (StartCheck) */
                       StartCheck = Stat->iter ;
                    }
                    else
                    {
                       /* Check if a restart should be done in subspace */
                       if ( IterSubRestart == nrestartsub )
                       {
                           Restart = TRUE ;
                       }
                    }
                }
                else  /* in full space */
                {
                    if ( (IterRestart == 1) || FirstFull )
                    {
                        memk = 0 ;
                    }
                    if ( (memk == 1) && InvariantSpace )
                    {
                         memk = 0 ;
                         InvariantSpace = FALSE ;
                    }
                    if ( PrintLevel >= 2 )
                    {
                        printf ("iteration in full space, memk: %i\n", memk) ;
                    }
                    if (memk < mem )
                    {
                        memk_is_mem = FALSE ;
                        SkFstart = 0 ;
                        /* SkF stores basis vector of the form alpha*d. We
                           factor SkF = Zk*Rk where Zk has orthonormal columns
                           and Rk is upper triangular. Zk is not stored;
                           wherever it is needed, we use SkF * inv (Rk) */
                        if (memk == 0)
                        {
                            mlast = 0 ;  /* starting pointer in the memory */
                            memk = 1 ;   /* dimension of current subspace */

                            t = sqrt(dnorm2) ;
                            zeta = alpha*t ;
                            Rk [0] = zeta ;
                            cg_scale (SkF, D, alpha, n) ;

                            Yk [0] = (dphi - dphi0)/t ;
                            gsub [0] = dphi/t ;
                            SkYk [0] = alpha*(dphi-dphi0) ;
                            FirstFull = FALSE ;
                            if ( IterRestart > 1 )
                            {
                               /* Need to save g for later correction of first
                                  column of Yk. Since g does not lie in the
                                  subspace and the first column is dense
                               cg_copy (gkeep, g, n) ; */
                               cg_copy (gkeep, gproj, n);
                               /* Also store dot product of g with the first
                                 direction vector -- this saves a later dot
                                 product when we fix the first column of Yk */
                               stgkeep = dphi0*alpha ;
                               d0isg = FALSE ;
                            }
                            else d0isg = TRUE ;
                        }
                        else
                        {
                            mlast = memk ; /* starting pointer in the memory */
                            memk++ ;       /* total number of Rk in the memory*/
                            mpp = mlast*n ;
                            spp = mlast*mem ;
                            cg_scale (SkF+mpp, D, alpha, n) ;
                            
                            /* check if the alphas are far from 1 */
                            if ( (fabs(alpha-5.05)>4.95) ||
                                 (fabs(alphaold-5.05)>4.95) )
                            {
                                /* multiply basis vectors by new direction */
                                cg_matvec (Rk+spp, SkF, SkF+mpp, mlast,n,0);

                                /* solve Rk'y = wsub to obtain the components of
                                   the new direction vector relative to the
                                   orthonormal basis Z in S = ZR, store in
                                   next column of Rk */
                                cg_trisolve (Rk+spp, Rk, mem, mlast, 0) ;
                            }
                            else /* alphas are close to 1 */
                            {
                                t1 = -alpha ;
                                t2 = beta*alpha/alphaold ;
                                for (j = 0; j < mlast; j++)
                                {
                                    Rk [spp+j] = t1*gsub [j] +t2*Rk [spp-mem+j];
                                }
                            }

                            t = alpha*alpha*dnorm2 ;
                            t1 = cg_dot0 (Rk+spp, Rk+spp, mlast) ;
                            if (t <= t1)
                            {
                                zeta = t*1.e-10 ;
                                Stat->NegDiag = TRUE ;
                            }
                            else zeta = sqrt(t-t1);

                            Rk [spp+mlast] = zeta ;
                            /* t = cg_dot0 (Zk+mlast*n, g, n)*/
                            t = - zeta/alpha ;
                            Yk [spp-mem+mlast] = t ;
                            gsub [mlast] = t ;

                            /* multiply basis vectors by new gradient */
                            cg_matvec (wsub, SkF, gnewproj, mlast, n, 0) ;

                            /* exploit dphi for last multiply */
                            wsub [mlast] = alpha*dphi ;
                            /* solve for new gsub */
                            cg_trisolve (wsub, Rk, mem, memk, 0) ;

                            /* subtract old gsub from new gsub = column of Yk */
                            cg_Yk (Yk+spp, gsub, wsub, NULL, memk) ;

                            SkYk [mlast] = alpha*(dphi-dphi0) ;
                        }
                    }
                    else  /* memk = mem */
                    {
                        memk_is_mem = TRUE ;
                        mlast = mem-1 ;
                        cg_scale (stemp, D, alpha, n) ;
                        
                        /* compute projection of s_k = alpha_k d_k into subspace
                           check if the alphas are far from 1 */
                        if ((fabs(alpha-5.05)>4.95)||(fabs(alphaold-5.05)>4.95))
                        {
                            mp = SkFstart ;
                            j = mem - mp ;

                            /* multiply basis vectors by sk */
                            cg_matvec (wsub, SkF, stemp, mem, n, 0) ;
                            /* rearrange wsub and store in Re = end col Rk */
                            cg_copy0 (Re, wsub+mp, j) ;
                            cg_copy0 (Re+j, wsub, mp) ;

                            /* solve Rk'y = Re */
                            cg_trisolve (Re, Rk, mem, mem, 0) ;
                        }
                        else /* alphas close to 1 */
                        {
                            t1 = -alpha ;
                            t2 = beta*alpha/alphaold ;
                            for (j = 0; j < mem; j++)
                            {
                                Re [j] = t1*gsub [j] + t2*Re [j-mem] ;
                            }
                        }

                        /* t = 2-norm squared of s_k */
                        t = alpha*alpha*dnorm2 ;
                        /* t1 = 2-norm squared of projection */
                        t1 = cg_dot0 (Re, Re, mem) ;
                        if (t <= t1)
                        {
                            zeta = t*1.e-10 ;
                            Stat->NegDiag = TRUE ;
                        }
                        else zeta = sqrt(t-t1);

                        /* dist from new search direction to prior subspace*/
                        Re [mem] = zeta ;

                        /* projection of prior g on new orthogonal
                           subspace vector */
                        t = -zeta/alpha ; /* t = cg_dot(Zk+mpp, g, n)*/
                        gsub [mem] = t ;
                        Yk [memsq] = t ;  /* also store it in Yk */

                        spp = memsq + 1 ;
                        mp = SkFstart ;
                        j = mem - mp ;

                        /* multiply basis vectors by gnew */
                        cg_matvec (vsub, SkF, gnewproj, mem, n, 0) ;

                        /* rearrange and store in wsub */
                        cg_copy0 (wsub, vsub+mp, j) ;
                        cg_copy0 (wsub+j, vsub, mp) ;

                        /* solve Rk'y = wsub */
                        cg_trisolve (wsub, Rk, mem, mem, 0) ;
                        wsub [mem] = (alpha*dphi
                                     - cg_dot0 (wsub, Re, mem))/zeta;

                        /* add new column to Yk, store new gsub */
                        cg_Yk (Yk+spp, gsub, wsub, NULL, mem+1) ;

                        /* store sk (stemp) at SkF+SkFstart */
                        cg_copy (SkF+SkFstart*n, stemp, n) ;
                        SkFstart++ ;
                        if ( SkFstart == mem ) SkFstart = 0 ;

                        mp = SkFstart ;
                        for (k = 0; k < mem; k++)
                        {
                            spp = (k+1)*mem + k ;
                            t1 = Rk [spp] ;
                            t2 = Rk [spp+1] ;
                            t = sqrt(t1*t1 + t2*t2) ;
                            t1 = t1/t ;
                            t2 = t2/t ;

                            /* update Rk */
                            Rk [k*mem+k] = t ;
                            for (j = (k+2); j <= mem; j++)
                            {
                                spp1 = spp ;
                                spp = j*mem + k ;
                                t3 = Rk [spp] ;
                                t4 = Rk [spp+1] ;
                                Rk [spp1] = t1*t3 + t2*t4 ;
                                Rk [spp+1] = t1*t4 - t2*t3 ;
                            }
                            /* update Yk */
                            if ( k < 2 ) /* mem should be greater than 2 */
                            {
                                /* first 2 rows are dense */
                                spp = k ;
                                for (j = 1; j < mem; j++)
                                {
                                    spp1 = spp ;
                                    spp = j*mem + k ;
                                    t3 = Yk [spp] ;
                                    t4 = Yk [spp+1] ;
                                    Yk [spp1] = t1*t3 + t2*t4 ;
                                    Yk [spp+1] = t1*t4 -t2*t3 ;
                                }
                                spp1 = spp ;
                                spp = mem*mem + 1 + k ;
                                t3 = Yk [spp] ;
                                t4 = Yk [spp+1] ;
                                Yk [spp1] = t1*t3 + t2*t4 ;
                                Yk [spp+1] = t1*t4 -t2*t3 ;
                            }
                            else if ( (k == 2) && (2 < mem-1))
                            {
                                spp = k ;

                                /* col 1 dense since the oldest direction
                                    vector has been dropped */
                                j = 1 ;
                                spp1 = spp ;
                                spp = j*mem + k ;
                                /* single nonzero percolates down the column */
                                t3 = Yk [spp] ;  /* t4 = 0. */
                                Yk [spp1] = t1*t3 ;
                                Yk [spp+1] = -t2*t3 ;
                                /* process rows in Hessenberg part of matrix */
                                for (j = 2; j < mem; j++)
                                {
                                    spp1 = spp ;
                                    spp = j*mem + k ;
                                    t3 = Yk [spp] ;
                                    t4 = Yk [spp+1] ;
                                    Yk [spp1] = t1*t3 + t2*t4 ;
                                    Yk [spp+1] = t1*t4 -t2*t3 ;
                                }
                                spp1 = spp ;
                                spp = mem*mem + 1 + k ;
                                t3 = Yk [spp] ;
                                t4 = Yk [spp+1] ;
                                Yk [spp1] = t1*t3 + t2*t4 ;
                                Yk [spp+1] = t1*t4 -t2*t3 ;
                            }
                            else if ( k < (mem-1) )
                            {
                                spp = k ;

                                /* process first column */
                                j = 1 ;
                                spp1 = spp ;
                                spp = j*mem + k ;
                                t3 = Yk [spp] ;  /* t4 = 0. */
                                Yk [spp1] = t1*t3 ;
                                Yk [spp+1] = -t2*t3 ;

                                /* process rows in Hessenberg part of matrix */
                                j = k-1 ;
                                spp = (j-1)*mem+k ;
                                spp1 = spp ;
                                spp = j*mem + k ;
                                t3 = Yk [spp] ;
                                Yk [spp1] = t1*t3 ; /* t4 = 0. */
                                /* Yk [spp+1] = -t2*t3 ;*/
                                /* Theoretically this element is zero */
                                for (j = k; j < mem; j++)
                                {
                                    spp1 = spp ;
                                    spp = j*mem + k ;
                                    t3 = Yk [spp] ;
                                    t4 = Yk [spp+1] ;
                                    Yk [spp1] = t1*t3 + t2*t4 ;
                                    Yk [spp+1] = t1*t4 -t2*t3 ;
                                }
                                spp1 = spp ;
                                spp = mem*mem + 1 + k ;
                                t3 = Yk [spp] ;
                                t4 = Yk [spp+1] ;
                                Yk [spp1] = t1*t3 + t2*t4 ;
                                Yk [spp+1] = t1*t4 -t2*t3 ;
                            }
                            else /* k = mem-1 */
                            {
                                spp = k ;

                                /* process first column */
                                j = 1 ;
                                spp1 = spp ;
                                spp = j*mem + k ;
                                t3 = Yk [spp] ; /* t4 = 0. */
                                Yk [spp1] = t1*t3 ;

                                /* process rows in Hessenberg part of matrix */
                                j = k-1 ;
                                spp = (j-1)*mem+k ;
                                spp1 = spp ;
                                spp = j*mem + k ;
                                t3 = Yk [spp] ; /* t4 = 0. */
                                Yk [spp1] = t1*t3 ;

                                j = k ;
                                spp1 = spp ;
                                spp = j*mem + k ; /* j=mem-1 */
                                t3 = Yk [spp] ;
                                t4 = Yk [spp+1] ;
                                Yk [spp1] = t1*t3 + t2*t4 ;

                                spp1 = spp ;
                                spp = mem*mem + 1 + k ; /* j=mem */
                                t3 = Yk [spp] ;
                                t4 = Yk [spp+1] ;
                                Yk [spp1] = t1*t3 + t2*t4 ;
                            }
                            /* update g in subspace */
                            if ( k < (mem-1) )
                            {
                                t3 = gsub [k] ;
                                t4 = gsub [k+1] ;
                                gsub [k] = t1*t3 + t2*t4 ;
                                gsub [k+1] = t1*t4 -t2*t3 ;
                            }
                            else /* k = mem-1 */
                            {
                                t3 = gsub [k] ;
                                t4 = gsub [k+1] ;
                                gsub [k] = t1*t3 + t2*t4 ;
                            }
                        }

                        /* update SkYk */
                        for (k = 0; k < mlast; k++) SkYk [k] = SkYk [k+1] ;
                        SkYk [mlast] = alpha*(dphi-dphi0) ;
                    }

                    /* calculate t = ||gsub||/||gtemp||  */
                    gsubnorm2 = cg_dot0 (gsub, gsub, memk) ;

                    gnorm2 = cg_dot (gnewproj, gnewproj, n) ;
                    ratio = sqrt (gsubnorm2/gnorm2) ;
                    if ( ratio > CGONE-Parm->eta2) InvariantSpace = TRUE ;

                    /* check to see whether to enter subspace */
                    if ( ((memk > 1) && InvariantSpace) ||
                         ((memk == mem) && (ratio > CGONE-Parm->eta0)) )
                    {
                        Stat->NumSub++ ;
                        if ( PrintLevel >= 1 )
                        {
                            if ( InvariantSpace )
                            {
                                printf ("CG iter: %li invariant space, "
                                        "enter subspace\n", (LONG) Stat->iter) ;
                            }
                            else
                            {
                                printf ("CG iter: %li enter subspace\n",
                                         (LONG) Stat->iter) ;
                            }
                        }
                        /* if the first column is dense, we need to correct it
                           now since we do not know the entries until the basis
                           is determined */
                        if ( !d0isg && !memk_is_mem )
                        {
                            wsub [0] = stgkeep ;
                            /* mlast = memk -1 */
                            cg_matvec (wsub+1, SkF+n, gkeep, mlast, n, 0) ;
                            /* solve Rk'y = wsub */
                            cg_trisolve (wsub, Rk, mem, memk, 0) ;
                            /* corrected first column of Yk */
                            Yk [1] -= wsub [1] ;
                            cg_scale0 (Yk+2, wsub+2, -CGONE, memk-2) ;
                        }
                        if ( d0isg && !memk_is_mem ) DenseCol1 = FALSE ;
                        else                         DenseCol1 = TRUE ;

                        Subspace = TRUE ;
                        /* reset subspace skipping to 0, test invariance */
                        SubSkip = 0 ;
                        IterSubRestart = 0 ;
                        nsub = memk ; /* dimension of subspace */
                        nrestartsub = (int) (((CGFLOAT) nsub)*
                                                            Parm->restart_fac) ;
                        mp_begin = mlast ;
                        memk_begin = nsub ;
                        SkFlast = (SkFstart+nsub-1) % mem ;
                        cg_copy0 (gsubtemp, gsub, nsub) ;
                        /* Rk contains the sk for subspace, initialize Sk = Rk*/
                        cg_copy (Sk, Rk, (int) mem*nsub) ;
                    }
                    else
                    {
                       if ( (IterRestart == nrestart) ||
                          ((IterQuad == qrestart) && (IterQuad != IterRestart)))
                       {
                           Restart = TRUE ;
                       }
                    }
                } /* done checking the full space */
            } /* done using the memory */

            if ( Subspace ) /* compute search direction in subspace */
            {
                Stat->IterSub++ ;
                if ( PrintLevel >= 2 )
                {
                    printf(" Subspace Iteration, IterSub: %ld\n",
                          (LONG) Stat->IterSub);
                }
                
                /* set x = xnew and g = gnew */
                cg_copy (x, xnew, n) ;
                cg_copy (g, gnew, n) ;
                if ( Aexists )
                {
                    cg_copy(gproj, gnewproj,n) ;
                }

                if ( Restart ) /*restart in subspace*/
                {
                    Restart = FALSE ;
                    IterRestart = 0 ;
                    IterSubRestart = 0 ;
                    IterQuad = 0 ;
                    mp_begin = -1 ;
                    memk_begin = 0 ;
                    memk = 0 ;
                    scale = (CGFLOAT) 1 ;

                    if ( PrintLevel >= 1 )
                    {
                        printf ("REstart subspace in cg\n") ;
                    }

                    /* search direction d = -Zk gsub, gsub = Zk' g, dsub = -gsub
                       => d =  Zk dsub = SkF (Rk)^{-1} dsub */
                    cg_scale0 (dsub, gsubtemp, -CGONE, nsub) ;
                    cg_copy0 (gsub, gsubtemp, nsub) ;
                    cg_copy0 (vsub, dsub, nsub) ;
                    cg_trisolve (vsub, Rk, mem, nsub, 1) ;
                    /* rearrange and store in wsub */
                    mp = SkFlast ;
                    j = nsub - (mp+1) ;
                    cg_copy0 (wsub, vsub+j, mp+1) ;
                    cg_copy0 (wsub+(mp+1), vsub, j) ;
                    cg_matvec (D, SkF, wsub, nsub, n, 1) ;

                   /* dnorm2 = pasa_dot(D, D, n) ; */
                    dnorm2 = gsubnorm2 ;

#ifdef PASA
                    /* transform direction back to x-space */
                    pasa_null_project (d, D, NULL, FALSE, pasacom) ;
                    pasacom->cg_bb_est = scale ;
#endif

                    /* derivative in new search direction without penalty term*/
                    dphi0 = cg_dot (d, g, n) ;
                }
                else  /* continue in subspace without restart */
                {
                    mlast_sub = (mp_begin + IterSubRestart) % mem ;

                    if (IterSubRestart > 0 ) /* not 1st iteration in subspace */
                    {
                        /* add new column to Yk memory,
                           calculate yty, Sk, Yk and SkYk */
                        spp = mlast_sub*mem ;
                        cg_scale0 (Sk+spp, dsub, alpha, nsub) ;
                        /* yty = (gsubtemp-gsub)'(gsubtemp-gsub),
                           set gsub = gsubtemp */
                        cg_Yk (Yk+spp, gsub, gsubtemp, &yty, nsub) ;
                        SkYk [mlast_sub] = alpha*(dphi - dphi0) ;
                    }
                    else
                    {
                        yty = cg_dot0 (Yk+mlast_sub*mem,
                                           Yk+mlast_sub*mem, nsub) ;
                    }
                    if ( yty > CGZERO )
                    {
                        scale = SkYk [mlast_sub]/yty ;
#ifdef PASA
                        pasacom->cg_bb_est = scale ;
#endif
                    }

                    /* calculate gsubtemp = H gsub */
                    mp = mlast_sub ;
                    /* memk = size of the L-BFGS memory in subspace */
                    memk = CGMIN (memk_begin + IterSubRestart, mem) ;
                    l1 = CGMIN (IterSubRestart, memk) ;
                    /* l2 = number of triangular columns in Yk with a zero */
                    l2 = memk - l1 ;
                    /* l1 = number of dense column in Yk (excluding first) */
                    l1++ ;
                    l1 = CGMIN (l1, memk) ;

                    /* process dense columns */
                    for (j = 0; j < l1; j++)
                    {
                        mpp = mp*mem ;
                        t = cg_dot0 (Sk+mpp, gsubtemp, nsub)/SkYk[mp] ;
                        tau [mp] = t ;
                        /* update gsubtemp -= t*Yk+mpp */
                        cg_daxpy0 (gsubtemp, Yk+mpp, -t, nsub) ;
                        mp-- ;
                        if ( mp < 0 ) mp = mem-1 ;
                    }

                    /* process columns from triangular (Hessenberg) matrix */
                    for (j = 1; j < l2; j++)
                    {
                        mpp = mp*mem ;
                        t = cg_dot0 (Sk+mpp, gsubtemp, mp+1)/SkYk[mp] ;
                        tau [mp] = t ;
                        /* update gsubtemp -= t*Yk+mpp */
                        if ( mp == 0 && DenseCol1 )
                        {
                            cg_daxpy0 (gsubtemp, Yk+mpp, -t, nsub) ;
                        }
                        else
                        {
                            cg_daxpy0(gsubtemp, Yk+mpp, -t, CGMIN(mp+2,nsub));
                        }
                        mp-- ;
                        if ( mp < 0 ) mp = mem-1 ;
                    }
                    cg_scale0 (gsubtemp, gsubtemp, scale, nsub) ;

                    /* process columns from triangular (Hessenberg) matrix */
                    for (j = 1; j < l2; j++)
                    {
                        mp++ ;
                        if ( mp == mem ) mp = 0 ;
                        mpp = mp*mem ;
                        if ( mp == 0 && DenseCol1 )
                        {
                            t = cg_dot0 (Yk+mpp, gsubtemp, nsub)/SkYk[mp] ;
                        }
                        else
                        {
                            t = cg_dot0 (Yk+mpp, gsubtemp,
                                                   CGMIN(mp+2,nsub))/SkYk[mp] ;
                        }
                        /* update gsubtemp += (tau[mp]-t)*Sk+mpp */
                        cg_daxpy0 (gsubtemp, Sk+mpp, tau [mp] - t, mp+1) ;
                    }

                    /* process dense columns */
                    for (j = 0; j < l1; j++)
                    {
                        mp++ ;
                        if ( mp == mem ) mp = 0 ;
                        mpp = mp*mem ;
                        t = cg_dot0 (Yk+mpp, gsubtemp, nsub)/SkYk [mp] ;
                        /* update gsubtemp += (tau[mp]-t)*Sk+mpp */
                        cg_daxpy0 (gsubtemp, Sk+mpp, tau [mp] - t, nsub) ;
                    } /* done computing H gsubtemp */

                    /* compute d = Zk dsub = SkF (Rk)^{-1} dsub */
                    cg_scale0 (dsub, gsubtemp, -CGONE, nsub) ;
                    cg_copy0 (vsub, dsub, nsub) ;

                    cg_trisolve (vsub, Rk, mem, nsub, 1) ;

                    /* rearrange and store in wsub */
                    mp = SkFlast ;
                    j = nsub - (mp+1) ;
                    cg_copy0 (wsub, vsub+j, mp+1) ;
                    cg_copy0 (wsub+(mp+1), vsub, j) ;
                    cg_matvec (D, SkF, wsub, nsub, n, 1) ;

                    /*  dnorm2 = pasa_dot(D, D, n) ; */
                    dnorm2 = cg_dot0 (dsub, dsub, nsub);

#ifdef PASA
                    /* transform direction back to x-space */
                    pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

                    /* derivative in new search direction without penalty term*/
                    dphi0 = cg_dot (d, g, n) ;
                }
            } /* end of subspace search direction */
            else  /* compute the search direction in the full space */
            {
                if ( PrintLevel >= 1 )
                {
                    printf ("compute search direction in full space\n") ;
                }
                /* check to see whether cg should be restated */
                if ( Restart )
                {
                    if ( PrintLevel >= 1 )
                    {
                        printf ("REstart CG in limited memory\n") ;
                    }

                    Restart = FALSE ;
                    IterRestart = 0 ;
                    IterQuad = 0 ;
                    scale = (CGFLOAT) 1 ;
                    /* pasacom->cg_bb_est = scale ;*/

                    /* set x = xnew, g = gnew */
                    cg_copy (x, xnew, n) ;
                    cg_copy (g, gnew, n) ;

                    /*gnewproj and gnorm2 were already computed */
                    if ( UseMemory == TRUE )
                    {
                        if ( Aexists == TRUE )
                        {
                            cg_copy (gproj, gnewproj, n) ;
                        }
                    }
                    else
                    {
                        gnorm2 = cg_dot (gproj, gproj, n) ;
                    }

                    /* D is the search direction before the final projection */
                    cg_scale (D, gproj, -CGONE, n) ;
                    dnorm2 = gnorm2 ; 

#ifdef PASA
                    /* transform direction back to x-space */
                    pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

                    /* derivative in search direction without penalty term */
                    dphi0  = cg_dot (g, d, n) ;
                    beta = CGZERO ;
                }
                else if ( !FirstFull ) /* ordinary cg update without restart */
                {
                    if ( PrintLevel >= 2 )
                    {
                        printf ("ordinary cg update in limited memory\n") ;
                    }
                    /* set x = xnew */
                    cg_copy (x, xnew, n) ;

                    if ( UseMemory == FALSE )
                    {
                        gnorm2 = cg_dot(gnewproj, gnewproj, n);
                    }

                    /* compute: ykPyk  = (newproj - oldproj)*(newproj - oldproj)
                                gkPyk  =  newproj           *(newproj - oldproj)
                       update: oldproj = newproj */
                    cg_update_beta (gproj, gnewproj, &gkPyk, &ykPyk, n) ;

                    /* For bound constrained problems, we set g = gnew in
                       update_beta since g = gproj and gnew = gnewproj. When
                       linear constraints present, we need to set g = gnew. */
                    if ( Aexists == TRUE )
                    {
                        cg_copy (g, gnew, n) ;
                    }

                    dkyk = dphi - dphi0 ;
                    scale = alpha*dnorm2/dkyk ;

                    if ( Parm->AdaptiveTheta )
                    {
                        t = 2. - CGONE/(0.1*QuadTrust + CGONE) ;
                    }
                    else
                    {
                        t = Parm->theta ;
                    }
                    beta = (gkPyk - t*dphi*ykPyk/dkyk)/dkyk ;

                    /* faster: initialize dnorm2 = gnorm2 at start, then
                       dnorm2 = gnorm2 + beta**2*dnorm2 - 2.*beta*dphi
                       gnorm2 = ||g_{k+1}||^2
                       dpi = g_{k+1}' d_k */
 
                    /* lower bound for beta is BetaLower*d_k'g_k/ ||d_k||^2 */
                    beta = CGMAX (beta, Parm->BetaLower*dphi0/dnorm2) ;

                    /* update search direction D = -gproj + beta*Dold */
                    cg_update_d (D, gproj, beta, n) ;
                    dnorm2 = cg_dot(D, D, n) ;

#ifdef PASA
                    /* transform direction back to x-space */
                    pasa_null_project (d, D, NULL, FALSE, pasacom) ;
                    pasacom->cg_bb_est = scale ;
#endif

                    /* derivative in new search direction without penalty term*/
                    dphi0 = cg_dot (d, g, n) ;
                }
                else /* FirstFull = TRUE, precondition after leaving subspace*/
                {
                    if ( PrintLevel >= 1 )
                    {
                        printf ("first full iteration after subspace exit\n") ;
                    }
                    /* set x = xtemp */
                    cg_copy (x, xnew, n) ;

                    /* compute: ykPyk  = (newproj - oldproj)*(newproj - oldproj)
                                gkPyk  =  newproj           *(newproj - oldproj)
                       update: oldproj = newproj */
                    cg_update_beta (gproj, gnewproj, &gkPyk, &ykPyk, n) ;

                    /* For bound constrained problems, we set g = gnew in
                       update_beta since g = gproj and gnew = gnewproj. When
                       linear constraints present, we need to set g = gnew. */
                    if ( Aexists == TRUE )
                    {
                        cg_copy (g, gnew, n) ;
                    }

                    mlast_sub = (mp_begin + IterSubRestart) % mem ;
                    /* save Sk */
                    spp = mlast_sub*mem ;
                    cg_scale0 (Sk+spp, dsub, alpha, nsub) ;
                    /* calculate yty, save Yk, set gsub = gsubtemp */

                    cg_Yk (Yk+spp, gsub, gsubtemp, &yty, nsub) ;
                    ytg = cg_dot0  (Yk+spp, gsub, nsub) ;
                    t = alpha*(dphi - dphi0) ;
                    SkYk [mlast_sub] = t ;

                    /* scale = t/ykyk ; */
                    if ( yty > CGZERO )
                    {
                        scale = t/yty ;
                    }

                    /* calculate gsubtemp = H gsub */
                    mp = mlast_sub ;
                    /* memk = size of the L-BFGS memory in subspace */
                    memk = CGMIN (memk_begin + IterSubRestart, mem) ;
                    l1 = CGMIN (IterSubRestart, memk) ;
                    /* l2 = number of triangular columns in Yk with a zero */
                    l2 = memk - l1 ;
                    /* l1 = number of dense column in Yk (excluding first) */
                    l1++ ;
                    l1 = CGMIN (l1, memk) ;

                    /* process dense columns */
                    for (j = 0; j < l1; j++)
                    {
                        mpp = mp*mem ;
                        t = cg_dot0 (Sk+mpp, gsubtemp, nsub)/SkYk[mp] ;
                        tau [mp] = t ;
                        /* update gsubtemp -= t*Yk+mpp */
                        cg_daxpy0 (gsubtemp, Yk+mpp, -t, nsub) ;
                        mp-- ;
                        if ( mp < 0 ) mp = mem-1 ;
                    }

                    /* process columns from triangular (Hessenberg) matrix */
                    for (j = 1; j < l2; j++)
                    {
                        mpp = mp*mem ;
                        t = cg_dot0 (Sk+mpp, gsubtemp, mp+1)/SkYk[mp] ;
                        tau [mp] = t ;
                        /* update gsubtemp -= t*Yk+mpp */
                        if ( mp == 0 && DenseCol1 )
                        {
                            cg_daxpy0 (gsubtemp, Yk+mpp, -t, nsub) ;
                        }
                        else
                        {
                            cg_daxpy0 (gsubtemp, Yk+mpp,-t, CGMIN(mp+2,nsub));
                        }
                        mp-- ;
                        if ( mp < 0 ) mp = mem-1 ;
                    }
                    cg_scale0 (gsubtemp, gsubtemp, scale, nsub) ;

                    /* process columns from triangular (Hessenberg) matrix */
                    for (j = 1; j < l2; j++)
                    {
                        mp++ ;
                        if ( mp == mem ) mp = 0 ;
                        mpp = mp*mem ;
                        if ( mp == 0 && DenseCol1 )
                        {
                            t = cg_dot0 (Yk+mpp, gsubtemp, nsub)/SkYk[mp] ;
                        }
                        else
                        {
                            t = cg_dot0 (Yk+mpp, gsubtemp,
                                                    CGMIN(mp+2,nsub))/SkYk[mp] ;
                        }
                        /* update gsubtemp += (tau[mp]-t)*Sk+mpp */
                        cg_daxpy0 (gsubtemp, Sk+mpp, tau [mp] - t, mp+1) ;
                    }

                    /* process dense columns */
                    for (j = 0; j < l1; j++)
                    {
                        mp++ ;
                        if ( mp == mem ) mp = 0 ;
                        mpp = mp*mem ;
                        t = cg_dot0 (Yk+mpp, gsubtemp, nsub)/SkYk [mp] ;
                        /* update gsubtemp += (tau[mp]-t)*Sk+mpp */
                        cg_daxpy0 (gsubtemp, Sk+mpp, tau [mp] - t, nsub) ;
                    } /* done computing H gsubtemp */

                    /* compute beta */
                    dkyk = dphi - dphi0 ;
#ifdef PASA
                    pasacom->cg_bb_est = alpha*dnorm2/dkyk ;
#endif

                    if ( Parm->AdaptiveTheta )
                    {
                        t = 2. - CGONE/(0.1*QuadTrust + CGONE) ;
                    }
                    else
                    {
                        t = Parm->theta ;
                    }
                    /* Theoretically t1 = ykPyk - yty */
                    t1 = CGMAX(ykPyk-yty, CGZERO) ;
                    if ( ykPyk > CGZERO )
                    {
                        scale = (alpha*dkyk)/ykPyk ; /* = sigma */
                    }
                    beta = scale*((gkPyk - ytg) - t*dphi*t1/dkyk)/dkyk ;
                    /* beta = MAX (beta, Parm->BetaLower*dphi0/dnorm2) ; */
                    beta = CGMAX (beta, Parm->BetaLower*(dphi0*alpha)/dkyk) ;

                    /* compute search direction
                       d = -Zk (H - sigma)ghat - sigma g + beta d
                       Note: d currently contains last 2 terms so only need
                       to add the Zk term. Above gsubtemp = H ghat */

                    /* form vsub = sigma ghat - H ghat = sigma ghat - gsubtemp*/
                    cg_scale0 (vsub, gsubtemp, -CGONE, nsub) ;
                    cg_daxpy0 (vsub, gsub, scale, nsub) ;
                    cg_trisolve (vsub, Rk, mem, nsub, 1) ;

                    /* rearrange vsub and store in wsub */
                    mp = SkFlast ;
                    j = nsub - (mp+1) ;
                    cg_copy0 (wsub, vsub+j, mp+1) ;
                    cg_copy0 (wsub+(mp+1), vsub, j) ;


                    /* save old direction d in gnew */
                    cg_copy (gnew, D, n) ; 

                    /* D = Zk (sigma - H)ghat */
                    cg_matvec (D, SkF, wsub, nsub, n, 1) ;

                    /* incorporate the new g and old d terms in new d */
                    cg_daxpy (D, gproj, -scale, n) ;
                    cg_daxpy (D, gnew, beta, n) ;
                    dnorm2 = cg_dot(D, D, n) ;

#ifdef PASA
                    /* transform direction back to x-space */
                    pasa_null_project (d, D, NULL, FALSE, pasacom) ;                    
#endif
                    /* derivative in new search direction without penalty term*/
                    dphi0 = cg_dot (d, g, n) ; 

                }   /* end of preconditioned step */
            }
        }   /* search direction has been computed */

        t = CGZERO ;
#ifdef PASA
        if ( use_penalty == TRUE )
        {
            t = pasacom->dp = cg_dot (d, gpen, n) ;
        }
        err = pasacom->e ;
#else
        err = gnorm ;
#endif

        /* restart when search direction not a descent direction */
        if ( dphi0 + t  >= CGZERO )
        {
            if ( PrintLevel >= 1 )
            {
                printf ("REstart CG due to bad search direction\n") ;
            }

            IterRestart = 0 ;
            IterQuad = 0 ;
            mlast = -1 ;
            memk = 0 ;
            beta = CGZERO ;
            Restart = FALSE ;

            /* D is the search direction before the final projection */
            cg_scale (D, gproj, -CGONE, n) ;

#ifdef PASA
            /* d is the final search direction */
            pasa_null_project (d, D, NULL, FALSE, pasacom) ;
#endif

            /* compute square of 2-norm of d (used in bb formula) */
            dnorm2 = cg_dot (D, D, n) ;

            /* derivative in search direction without penalty term */
            dphi0  = cg_dot (g, d, n) ;

            t = CGZERO ;
#ifdef PASA
            if ( use_penalty == TRUE )
            {
                t = pasacom->dp = cg_dot (gpen, d, n) ;
            }
#endif

            if ( dphi0 + t > CGZERO )
            {
                status = CG_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION ;
                XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }
        }

        /* test for slow convergence */
        if ( (f < fbest) || (err < gbest) )
        {
            nslow = 0 ;
            if ( f < fbest )
            {
                fbest = f ;
            }
            if (err < gbest )
            {
                gbest = err ;
            }
        }
        else
        {
            nslow++ ;
        }
        if ( nslow > slowlimit )
        {
            status=XXCG(wrapup)(CG_NO_COST_OR_GRADIENT_IMPROVEMENT,PASA_CG_COM);
            return (status) ;
        }

#ifndef NDEBUG
        if ( Parm->debug )
        {
            if ( f > cgcom->f0 + Parm->debugtol*Ck )
            {
                Stat->newf = f ;
                Stat->oldf = cgcom->f0 ;
                status = CG_DEBUGGER_IS_ON_AND_FUNCTION_VALUE_INCREASES ;
                XXCG(wrapup) (status, PASA_CG_COM) ;
                return (status) ;
            }
        }
#endif

    }
    status = XXCG(wrapup) (CG_ITERATIONS_EXCEED_MAXITS, PASA_CG_COM) ;
    return (status) ;
}

/* ==========================================================================
   === cg_setup =============================================================
   ==========================================================================
    Generate a pointer to a CGdata structure with default values for all
    parameters, and NULL or EMPTY values for all inputs. Return NULL pointer if
    there is not enough memory.
   ========================================================================== */
CGdata * XXCG(setup) (void)
{
    /* Initialize PASAdata structure */
    CGdata *Data ;

    /* Allocate memory for parameters and statistics, initialize parameters */
    Data = (CGdata  *) cg_malloc (sizeof (CGdata)) ;
    if ( Data == NULL ) return (Data) ;
    Data->Parm = (CGparm *) cg_malloc (sizeof(CGparm)) ;
    Data->Stat = (CGstat *) cg_malloc (sizeof(CGstat)) ;
    if ( (Data->Parm == NULL) || (Data->Stat == NULL) )
    {
        Data = NULL ;
        return (Data) ;
    }

    cg_default (Data->Parm) ;

    /* set remaining values in the CGdata structure to EMPTY (= -1) or NULL */
    Data->x = NULL ;
    Data->n = EMPTY ;

    /* size n, the linear term for a quadratic or linear objective is c'*x */
    Data->c = NULL ;

    /* For a quadratic objective, hprod (p, x, n) evaluates the Hessian
       times a vector. Here the problem dimension n and x are given, while
       the routine should generate p = H*x where H is the Hessian of the
       objective. */
    Data->hprod = NULL ;

    /* evaluate the function f at x, value (f, x, n) */
    Data->value = NULL ;

    /* evaluate the gradient at x, grad  (g, x, n) */
    Data->grad = NULL ;

    /* evaluate the function f and gradient g at x, valgrad (f, g, x, n) */
    /* NULL => use value & grad */
    Data->valgrad = NULL ;

    /* evaluate Hessian */
    Data->hess = NULL ;

    /* NULL => allocate real work space. */
    Data->Work = NULL ;

    /* If the user does not provide a pointer to x, then an array of size
       n is malloc'd and set to zero.  pasa_terminate will free any allocated
       memory. The x_created pointer is only used internally by CG_DESCENT
       when it creates or frees  memory for x */
    Data->x_created = NULL ;

    /* Return pointer to CGdata structure */
    return (Data) ;
}

/* ==========================================================================
   === cg_terminate =========================================================
   ==========================================================================
    Free allocated memory associated with CGdata structure
   ========================================================================== */
void XXCG(terminate)
(
    CGdata **DataHandle
)
{
    CGdata *Data ;
    Data = *DataHandle ;
    /* Free memory allocated in pasa_setup */
    cg_free (Data->Parm) ;
    cg_free (Data->Stat) ;
    if ( Data->x_created != NULL )
    {
        if ( Data->x_created == Data->x )
        {
            cg_free (Data->x) ;
            Data->x = Data->x_created = NULL ;
        }
        else /* user created x */
        {
            cg_free (Data->x_created) ;
            Data->x_created = NULL ;
        }
    }
    cg_free (Data) ;
}

int XXCG(wrapup)
(
    int       status,
#ifdef PASA
    PASAcom *pasacom,
#endif
    CGcom     *cgcom
)
{
    CGparm *Parm ;
    CGstat *Stat ;

    Stat = cgcom->Stat ;
    Parm = cgcom->Parm ;

    Stat->status = status ;
    Stat->f = cgcom->f ;
    if ( Parm->PrintStatus == TRUE )
    {
        cg_print_status (cgcom->cgdata) ;
        printf ("\n") ;
    }

    if ( Parm->PrintStat == TRUE )
    {
        cg_print_stat (cgcom->cgdata) ;
    }
#ifdef PASA
    /* return to pasa */
    const int use_napheap = pasacom->use_napheap ;
    const int use_pproj = pasacom->use_pproj ;
    const int PrintLevel = Parm->PrintLevel ;
    const int loExists = pasacom->loExists ;
    const int hiExists = pasacom->hiExists ;
    /* the cg error is the local error */
    Stat->err = pasacom->e ;

    /* if the penalty term is used and the objective is nonquadratic,
       then the unpenalized objective is stored in f_orig */
    if ( (cgcom->QuadCost == FALSE) && (pasacom->use_penalty == TRUE) )
    {
        pasacom->f = pasacom->f_orig ;
    }

    /* If status is CG_HITS_BOUNDARY, then the iterate hit the boundary
       of the feasible region.  In this case, we compress the problem,
       update the factorization, and restart either CG or active grad_proj */
    if ( status == CG_HITS_BOUNDARY )
    {
        CGINT boundindex, j, k, km, ni, *Ap, *Anz, *Ai, *ATp, *ATi, *ir ;
        CGFLOAT *a, *Ax, *ATx, *b, *bl, *bu ;
        PPprob *Prob ;
        PPwork *Work ;

        if ( use_pproj == TRUE )
        {
            Prob = pasacom->ppcom->Prob ;
            Work = pasacom->ppcom->Work ;
            ATp = Work->ATp ;
            ATi = Work->ATi ;
            ATx = Work->ATx ;
            Ap = Prob->Ap ;
            Anz = Prob->Anz ;
            Ai = Prob->Ai ;
            Ax = Prob->Ax ;
            ni = Prob->ni ;
            ir = Work->ir ;
            b  = pasacom->b ;
            bl = pasacom->bl ;
            bu = pasacom->bu ;
        }
        else if ( use_napheap == TRUE )
        {
            a = pasacom->nap_a ;
        }
        boundindex = pasacom->boundindex ;

        if ( PrintLevel >= 1 )
        {
            if ( pasacom->boundtype == 1 )
            {
                printf ("Component of x hits bound in cg_descent, "
                        "index = %ld", (LONG) boundindex) ;
                j = boundindex ;
                if ( j < 0 )
                {
                    printf (" (user: %ld lower)\n\n",
                           (LONG) pasacom->ifree [-(j+1)]) ;
                }
                else
                {
                    printf (" (user: %ld upper)\n\n",
                           (LONG) pasacom->ifree [j-1]) ;
                }
            }
            else
            {
                printf ("New active linear inequality in cg_descent, "
                         "index = %ld", (LONG) boundindex) ;
                if ( boundindex < 0 )
                {
                    if ( use_pproj == TRUE )
                    {
                        printf (" (row: %ld lower)\n\n",
                               (LONG) Prob->ineq_row [-boundindex]) ;
                    }
                    {
                        printf (" (row: %i lower)\n\n", 0) ;
                    }
                }
                else
                {
                    if ( use_pproj == TRUE )
                    {
                        printf (" (row: %ld upper)\n\n",
                               (LONG) Prob->ineq_row [boundindex]) ;
                    }
                    else /* use_napheap == TRUE */
                    {
                        printf (" (row: %i upper)\n\n", 0) ;
                    }
                }
            }
        }

        if ( pasacom->boundtype == 1 )
        {
            CGINT nf, nc, *bound_cols, *ifree ;
            CGFLOAT xj, *g, *lo, *hi, *x ;
            /* find the active bound */
            ifree = pasacom->ifree ;
            nc = pasacom->nc ;
            bound_cols = pasacom->bound_cols ;
            lo = pasacom->lo ;
            hi = pasacom->hi ;
            if ( boundindex < 0 )
            {
                j = -(boundindex+1) ;
                /* set x [j] = lo [j] to account for rounding errors in x */
                k = ifree [j] ;
                xj = pasacom->userx [k] = lo [j] ;
                bound_cols [nc] = -(k + 1) ;
                if ( use_napheap == TRUE )
                {
                    pasacom->nap_bl -= a [j]* lo [j] ;
                }
            }
            else
            {
                j = boundindex - 1 ;
                /* set x [j] = hi [j] to account for rounding errors in x */
                k = ifree [j] ;
                xj = pasacom->userx [k] = hi [j] ;
                bound_cols [nc] = k ;
                if ( use_napheap == TRUE )
                {
                    pasacom->nap_bu -= a [j]*hi [j] ;
                }
            }
            pasacom->nc++ ;
    
            /* delete the jth element of x, g, lo, hi, and ifree
               if napheap is used, then delete the jth element of a */
            x = pasacom->x ;
            g = pasacom->g ;
            km = j ;
            nf = pasacom->nf ;
            for (k = j+1; k < nf; k++)
            {
                ifree [km] = ifree [k] ;
                x [km] = x [k] ;
                g [km] = g [k] ;
                if ( use_napheap )   a [km] =  a [k] ;
                if ( loExists )     lo [km] = lo [k] ;
                if ( hiExists )     hi [km] = hi [k] ;
                km = k ;
            }
            pasacom->nf = km ;
            if ( use_napheap == TRUE )
            {
                pasacom->nap_a2 -= a [j]*a [j] ;
                if ( pasacom->nap_a2 <= .01*pasacom->nap_a2save )
                {
                    pasacom->nap_a2save = pasacom->nap_a2 = pasa_dot (a, a, km);
                }
            }
            if ( PrintLevel >= 1 )
            {
                printf ("cg wrapup nc: %ld nf: %ld\n",
                         (LONG) pasacom->nc, (LONG) pasacom->nf) ;
            }

#ifndef NOPPROJ
            /* if A exists, compress the matrix and update the factorization*/
            if ( use_pproj == TRUE )
            {
                int blk, blks ;
                CGINT i, iri, l, m, ncol, ncoldel, nrow, p, pp, q, *col_start ;
                CGFLOAT t ;
 
                ASSERT (Work->ncoladd == 0) ;
                ASSERT (Work->ncoldel == 0) ;
                ASSERT (Work->nrowadd == 0) ;
                ASSERT (Work->nrowdel == 0) ;

#ifndef NDEBUG
                Work->ib [j] = 1 ; /* need for check routines in pproj */
#endif
                nrow = pasacom->nrow ;

                /* boundtype = 1 corresponds to a component of x hitting
                   either an upper or lower bound, while boundtype = -1
                   corresponds to a linear inequality becoming active. */
                ncol = Prob->ncol ;
                /* update the factorization if the column has active rows */
                if ( Anz [j] > 0 )
                {
                    ncoldel = 1 ;
                    Work->ColmodList [ncol-ncoldel] = j ;
                    Work->ColmodFlag [j] = ncol-ncoldel ;
                    Work->ncoldel = ncoldel ;
                    Work->Annz -= Anz [j] ;
                    pasacom->ppcom->Parm = pasacom->pprojparm ;
                    pproj_modcol (pasacom->ppcom, 0, 0, -1, NULL, Ap+j,
                                  Anz+j, NULL, NULL, 1) ;
                }
#ifndef NDEBUG
                Work->ib [j] = 0 ;
#endif
    
                /* adjust the right side of the inequalities to account
                   for the bound variable */
                if ( xj != CGZERO )
                {
                    q = Ap [j+1] ;
                    for (p = Ap [j]; p < q; p++)
                    {
                        i = Ai [p] ;
                        iri = ir [i] ;
                        t = Ax [p]*xj ;
                        if ( iri == 0 ) /* equality constraint */
                        {
                            b [i] -= t ;
                        }
                        else /* inequality constraint */
                        {
                            if ( iri < 0 )
                            {
                                iri = -iri ;
                            }
                            else if ( iri > ni )
                            {
                                iri -= ni ;
                            }
                            bl [iri] -= t ;
                            bu [iri] -= t ;
                        }
                    }
                }
    
                /* When columns are deleted, the column start of each block is
                   reduced by the number of proceeding columns that were
                   deleted.  Find the first block with column start > j.
                   The following code terminates since col_start [blks] =
                   number of columns in matrix. */
                col_start = Work->col_start ;
                blks = Work->blks ;
                for (blk = 1; blk <= blks; blk++)
                {
                    if ( col_start [blk] > j )
                    {
                        break ;
                    }
                }
                l = col_start [blk] ;
                m = Ap [j] ;
                p = Ap [j+1] ;
                km = j ;
                for (k = j+1; k < ncol; k++)
                {
                    if ( k == l )
                    {
                        col_start [blk] = km ;
                        blk++ ; 
                        while ( col_start [blk] == l )
                        {
                            col_start [blk] = km ;
                            blk++ ;
                        } 
                        l = col_start [blk] ;
                    }
                    q = Ap [k+1] ;
                    Anz [km] = Anz [k] ;
       
                    /* save column k in matrix */ 
                    Ap [k] = Ap [km] + q - p ;
                    for (; p < q; p++)
                    {
                        Ai [m] = Ai [p] ;
                        Ax [m] = Ax [p] ;
                        m++ ;
                    }
                    km = k ;
                }
                Prob->ncol = km ;
                Work->A->ncol = km ;
                Work->A->nzmax = Ap [km] ;
                col_start [blk] = km ;
                while ( blk < blks )
                {
                    blk++ ;
                    col_start [blk] = km ;
                }

                /* Update AT matrix. This can be done much more
                   efficiently if AT uses ATnz */
                pp = 0 ;
                p = 0 ;
                for (i = 0; i < nrow; i++)
                {
                    q = ATp [i+1] ;
                    for (; p < q; p++)
                    {
                        k = ATi [p] ;
                        if ( k < j ) /* keep the element unchanged */
                        {
                            ATi [pp] = k ;
                            ATx [pp] = ATx [p] ;
                            pp++ ;
                        }
                        else if ( k > j )  /* decrease element by 1 */
                        {
                            ATi [pp] = k - 1 ;
                            ATx [pp] = ATx [p] ;
                            pp++ ;
                        }
                        /* if k = j, then omit the element */
                    }
                    ATp [i+1] = pp ;
                }
                pasa_copyi (Work->AFTp, ATp, nrow+1) ;
            }
#endif
        }
        else /* boundtype = -1 (row becomes active) */
        {
#ifndef NOPPROJ
            int  *sol_to_blk ;
            CGINT i, nr, nrowadd, p, p1, p2, p2m1, q, q1, q2, row,
                 *bound_rows, *ineq_row, *RLinkDn, *RLinkUp ;
            CGFLOAT t ;

            CGINT const nrow = pasacom->nrow ;
            bound_rows = pasacom->bound_rows ;

            if ( use_napheap == TRUE )
            {
                /* boundindex = -1 if at lower bound, +1 if at upper bound */
                bound_rows [0] = pasacom->nap_constraint = boundindex ;
                if ( boundindex < 0 ) /* lower bound active */
                {
                    pasacom->nap_bu = pasacom->nap_bl ;
                }
                else                  /* upper bound active */
                {
                    pasacom->nap_bl = pasacom->nap_bu ;
                }
                pasacom->nr = 1 ;
            }
            else /* use_pproj == TRUE */
            {
                nr = pasacom->nr ;
                ineq_row = Prob->ineq_row ;
                sol_to_blk = Work->sol_to_blk ;
                if ( boundindex < 0 ) /* lower bound active */
                {
                    k = -boundindex ;
                    row = ineq_row [k] ;
                    b [row] = bl [k] ;
                    bound_rows [nr] = -(row+1) ;
                }
                else                  /* upper bound active */
                {
                    k = boundindex ;
                    row = ineq_row [k] ;
                    b [row] = bu [k] ;
                    bound_rows [nr] = row + 1 ;
                }

                Work->nactive++ ;
                Work->ATnz += ATp [row+1] - ATp [row] ;
                ir [row] = 0 ;
                nrowadd = 1 ;
                i = nrow - nrowadd ;
                Work->RowmodList [i]   = row ;
                Work->RowmodFlag [row] = i ;
                Work->nrowadd = nrowadd ;
    
                /* add row to linked lists */
                RLinkDn = Work->RLinkDn ;
                RLinkUp = Work->RLinkUp ;
    
                i = nrow ;
                while ( (i = RLinkUp [i]) < row )
    
                ASSERT (i != row) ;
                j = RLinkDn [i] ;
                RLinkDn [i] = row ;
                RLinkDn [row] = j ;
                RLinkUp [j] = row ;
                RLinkUp [row] = i ;
    
                /* Update A to put the new active row in the active part of A.
                   Recall that the active rows in column must be in increasing
                   order. */
                q = ATp [row+1] ;
                for (p = ATp [row]; p < q; p++)
                {
                    j = ATi [p] ;
                    p1 = Ap [j] ;
                    p2 = q1 = p1 + Anz [j] ;
                    q2 = Ap [j+1] ;
                    /* find row in the inactive part of matrix */
                    for (; p2 < q2; p2++)
                    {
                        if ( Ai [p2] == row )
                        {
                            /* move 1st inactive row to location of
                               row in column */
                            Ai [p2] = Ai [q1] ;
                            t = Ax [p2] ;
                            Ax [p2] = Ax [q1] ;
                            break ;
                        }
                    }
                    ASSERT (p2 < q2) ;
                    /* find where to insert row in the active part of column */
                    p2 = q1 ;
                    for (; p2 > p1; )
                    {
                        p2m1 = p2 - 1 ;
                        if ( Ai [p2m1] < row ) /* row goes at location p2 */
                        {
                            break ;
                        }
                        Ai [p2] = Ai [p2m1] ;
                        Ax [p2] = Ax [p2m1] ;
                        p2 = p2m1 ;
                    }
                    Ai [p2] = row ;
                    Ax [p2] = t ;
                    Anz [j]++ ;
                }
                pasacom->ppcom->Parm = pasacom->pprojparm ;
                pproj_modrow (pasacom->ppcom, 0, TRUE, FALSE, +1,
                              NULL, NULL, NULL, NULL) ;
     
                for (i = 1; i < k; i++)
                {
                    row = ineq_row [i] ;
                    ASSERT (ir [row] == i + ni) ;
                    ir [row]-- ; /* ni has decreased by 1 */
                }
                /* The bounds as well as the block numbers associated with each
                   inequality need to be shifted down. */
                km = k ;
                for (k = k+1; k <= ni; k++)
                {
                    bl [km] = bl [k] ;
                    bu [km] = bu [k] ;
                    sol_to_blk [km] = sol_to_blk [k] ;
                    row = ineq_row [k] ;
                    ASSERT (ir [row] == k + ni) ;
                    ir [row] -= 2 ; /* subtract 2 since ni and row decreased */
                    ineq_row [km] = row ;
                    km = k ;
                }
                sol_to_blk [km] = Work->blks ;
                Prob->ni-- ;    /* one fewer inequality to check */
                pasacom->nr++ ; /* one more bound inequality */
            }
#endif
        }
        pasa_null_project (NULL, pasacom->g, NULL, TRUE, pasacom) ;
        /* it might save some time to only perform this call to
           checktol when pasacom->e <= pasacom->testtol (similar to
           what is done in the main program). */
        if ( PrintLevel >= 1 )
        {
            printf ("Local error: %e testtol: %e Global error: %e\n",
                    pasacom->e, pasacom->testtol, pasacom->E) ;
        }

        status = XXCG(checktol) (pasacom->x, pasacom, cgcom) ;
        if ( (status == PASA_ERROR_TOLERANCE_SATISFIED) ||
             (status == PASA_GRAD_PROJ) )
        {
            return (status) ;
        }
        if ( pasacom->pasaparm->use_activeGP == TRUE )
        {
            return (PASA_ACTIVE_GP) ;
        }
        return (PASA_CG_DESCENT) ;
    }
#else
    CGFLOAT t ;
    if ( (cgcom->QuadCost == TRUE) && (Parm->QPshift > CGZERO) )
    {
        t = cg_dot (cgcom->x, cgcom->x, cgcom->n) ;
        Stat->f -= 0.5*t*t*Parm->QPshift ;
    }
    if ( cgcom->work_created != NULL )
    {
        cg_free (cgcom->work_created) ;
    }
#endif
    return (status) ;
}

int XXCG(evaluate)
(
    CGFLOAT alpha_good, /* a value of alpha for which function is finite */
    CGFLOAT     *Alpha, /* stepsize along the search direction */
    char         *what, /* fg = eval func & grad, g = grad only,f = func only */
#ifdef PASA
    PASAcom *pasacom,
#endif
    CGcom       *Com
)
{
    int const QuadCost = Com->QuadCost ;
#ifdef PASA
    int status ;
    /* pasa is used */
    status = pasa_evaluate (alpha_good, Alpha, pasacom, what) ;
    if ( !QuadCost )
    {
        if ( !strcmp (what, "fg") || !strcmp (what, "f") )
        {
            Com->f = pasacom->f ;
        }

        if ( !strcmp (what, "fg") || !strcmp (what, "g") )
        {
            Com->df = pasacom->df ;
        }
    }
    if ( status == PASA_OK )
    {
        return (CG_CONTINUE) ;
    }
    else
    {
        return (CG_FUNCTION_NAN_OR_INF) ;
    }
#else
    /* pasa is NOT being used */
    int i ;
    CGINT n ;
    CGFLOAT alpha, df, t, *d, *f, *g, *x, *gnew, *xnew ;
    CGparm *Parm ;
    CGstat *Stat ;

    Parm = Com->Parm ;
    alpha = *Alpha ;
    n = Com->n ;
    x = Com->x ;
    g = Com->g ;
    f = &(Com->f) ;
    Stat = Com->Stat ;

    /* initial evaluation of objective and gradient */
    if ( alpha == CGZERO )
    {
        Stat->ngrad++ ;
        if ( QuadCost ) /* quadratic objective */
        {
            Com->hprod (g, x, n) ;         /* g = Q*x */

            /* regularize the Hessian if QPshift > 0 */
            if ( Com->QPshift > CGZERO )   /* g = g + QPshift*x */
            {
                cg_step (g, g, x, Com->QPshift, n) ;
            }

            *f = 0.5*cg_dot (g, x, n) ;      /* f = .5*x'Qx */
            if ( Com->c != NULL )
            {
                *f += cg_dot(x, Com->c, n) ; /* f = .5*x'*Qx + c'*x */
                /* store gradient in userg */
                cg_step (g, g, Com->c, CGONE, n) ; /* g = Qx+c */
            }
            *f += Parm->fadjust ;     /* user adjustment */
        }
        else
        {
            Stat->nfunc++ ;
            if ( Com->valgrad != NULL )
            {
                Com->valgrad (f, g, x, n) ;
            }
            else
            {
                Com->grad  (g, x, n) ;
                Com->value (f, x, n) ;
            }
        }
        return (CG_CONTINUE) ;
    }

    d = Com->d ;
    /* evaluate Hessian times direction for a quadratic */
    if ( alpha == -CGONE )
    {
        Stat->ngrad++ ;
        Com->hprod (Com->Qd, d, n) ;
        /* add the regularization term if QPshift > 0 */
        if ( Com->QPshift > CGZERO )
        {
            cg_step (Com->Qd, Com->Qd, d, Com->QPshift, n) ;
        }
        return (CG_CONTINUE) ;
    }

    /* take a step along the search direction */
    gnew = Com->gnew ;
    xnew = Com->xnew ;
    cg_step (xnew, x, d, alpha, n) ;
    if ( !strcmp (what, "fg") )     /* compute function and gradient */
    {
        Stat->nfunc++ ;
        Stat->ngrad++ ;
        if ( Com->valgrad != NULL )
        {
            Com->valgrad (f, gnew, xnew, n) ;
        }
        else
        {
            Com->grad  (gnew, xnew, n) ;
            Com->value (f, xnew, n) ;
        }
        df = Com->df = cg_dot (gnew, d, n) ;
        if ( (*f == *f) && (*f < CGINF) && (*f > -CGINF) &&
             (df == df) && (df < CGINF) && (df > -CGINF) )
        {
            return (CG_CONTINUE) ;
        }
        t = Parm->cg_infdecay ;
        for (i = 0; i < Parm->cg_ninf_tries; i++)
        {
            Stat->nfunc++ ;
            Stat->ngrad++ ;
            alpha = alpha_good + t*(alpha - alpha_good) ;
            t *= Parm->cg_infdecay_rate ;
            cg_step (xnew, x, d, alpha, n) ;
            if ( Com->valgrad != NULL )
            {
                Com->valgrad (f, gnew, xnew, n) ;
            }
            else
            {
                Com->grad  (gnew, xnew, n) ;
                Com->value (f, xnew, n) ;
            }
            df = Com->df = cg_dot (gnew, d, n) ;
            if ( (*f == *f) && (*f < CGINF) && (*f > -CGINF) &&
                 (df == df) && (df < CGINF) && (df > -CGINF) )
            {
                break ;
            }
        }
    }
    else if ( !strcmp (what, "f") ) /* compute function value */
    {
        Stat->nfunc++ ;
        Com->value (f, xnew, n) ;
        if ( (*f == *f) && (*f < CGINF) && (*f > -CGINF) )
        {
            return (CG_CONTINUE) ;
        }
        t = Parm->cg_infdecay ;
        for (i = 0; i < Parm->cg_ninf_tries; i++)
        {
            Stat->nfunc++ ;
            alpha = alpha_good + t*(alpha - alpha_good) ;
            t *= Parm->cg_infdecay_rate ;
            cg_step (xnew, x, d, alpha, n) ;
            Com->value (f, xnew, n) ;
            if ( (*f == *f) && (*f < CGINF) && (*f > -CGINF) )
            {
                break ;
            }
        }
    }
    else
    {
        Stat->ngrad++ ;
        Com->grad (gnew, xnew, n) ;
        df = Com->df = cg_dot (gnew, d, n) ;
        if ( (df == df) && (df < CGINF) && (df > -CGINF) )
        {
            return (CG_CONTINUE) ;
        }
        t = Parm->cg_infdecay ;
        for (i = 0; i < Parm->cg_ninf_tries; i++)
        {
            Stat->ngrad++ ;
            alpha = alpha_good + t*(alpha - alpha_good) ;
            t *= Parm->cg_infdecay_rate ;
            cg_step (xnew, x, d, alpha, n) ;
            Com->grad (gnew, xnew, n) ;
            df = Com->df = cg_dot (gnew, d, n) ;
            if ( (df == df) && (df < CGINF) && (df > -CGINF) )
            {
                break ;
            }
        }
    }
    if ( i == Parm->cg_ninf_tries )
    {
        return (CG_FUNCTION_NAN_OR_INF) ;
    }
    else
    {
        *Alpha = alpha ;
        return (CG_CONTINUE) ;
    }
#endif
}

/* =========================================================================
   ==== cg_Wolfe ===========================================================
   =========================================================================
   Check whether the Wolfe or the approximate Wolfe conditions are satisfied
   Return:
       CG_WOLFE_OK     (Wolfe or approximate Wolfe conditions satisfied)
       CG_WOLFE_NOT_OK (Wolfe condition does not hold)
   ========================================================================= */
int XXCG(Wolfe)
(
    CGFLOAT  alpha, /* stepsize */
    CGFLOAT      f, /* function value associated with stepsize alpha */
    CGFLOAT   dphi, /* derivative value associated with stepsize alpha */
    CGcom   *cgcom 
)
{
    if ( dphi >= cgcom->wolfe_lo )
    {
        /* test original Wolfe conditions */
        if ( f - cgcom->f0 <= alpha*cgcom->wolfe_hi )
        {
            if ( cgcom->Parm->PrintLevel >= 2 )
            {
                printf ("Wolfe conditions hold\n") ;
/*              printf ("wolfe f: %25.15e f0: %25.15e df: %25.15e\n",
                         f, cgcom->f0, dphi) ;*/
            }
            return (CG_WOLFE_OK) ;
        }
        /* test approximate Wolfe conditions */
        else if ( cgcom->approxstep )
        {
/*          if ( cgcom->Parm->PrintLevel >= 2 )
            {
                printf ("f:    %e fpert:    %e ", f, cgcom->fpert) ;
                if ( f > cgcom->fpert ) printf ("(fail)\n") ;
                else                  printf ("(OK)\n") ;
                printf ("dphi: %e hi bound: %e ", dphi, cgcom->awolfe_hi) ;
                if ( dphi > cgcom->awolfe_hi ) printf ("(fail)\n") ;
                else                         printf ("(OK)\n") ;
            }*/
            if ( (f <= cgcom->fpert) && (dphi <= cgcom->awolfe_hi) )
            {
                if ( cgcom->Parm->PrintLevel >= 2 )
                {
                    printf ("Approximate Wolfe conditions hold\n") ;
/*                  printf ("f: %25.15e fpert: %25.15e dphi: %25.15e awolf_hi: "
                       "%25.15e\n", f, cgcom->fpert, dphi, cgcom->awolfe_hi) ;*/
                }
                return (CG_WOLFE_OK) ;
            }
        }
    }
    return (CG_WOLFE_NOT_OK) ;
}

/* =========================================================================
   ==== cg_line ============================================================
   =========================================================================
   Approximate Wolfe line search routine
   Return:
       CG_WOLFE_OK
       CG_WOLFE_CONDITIONS_NOT_SATISFIED
       CG_SLOPE_ALWAYS_NEGATIVE
       CG_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS
   ========================================================================= */
int XXCG(line)
(
    int       repeat, /* TRUE => Wolfe search failed, retry using approxstep */
#ifdef PASA
    PASAcom *pasacom,
#endif
    CGcom     *cgcom
)
{
    int approxstep, AvoidFeval, iter, ngrow, PrintLevel, qa, qa0, qb, qb0,
        status, toggle ;
    CGFLOAT alpha, a, a1, a2, b, bmin, da, db, d0, d1, d2, df, f, fa, fb,
           a0, b0, da0, db0, fa0, ExpandSafe, fb0, maxstep, rho, t, width ;
    char *s1, *s2, *fmt1, *fmt2, *fmt3 ;
    CGparm *Parm ;

    approxstep = cgcom->approxstep ;
    Parm = cgcom->Parm ;
    PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 2 )
    {
        if ( approxstep )
        {
            printf ("Approximate Wolfe line search\n") ;
            printf ("=============================\n") ;
        }
        else
        {
            printf ("Wolfe line search\n") ;
            printf ("=================\n") ;
        }
    }
    maxstep = cgcom->maxstep ;
    status = CG_CONTINUE ;

    /* We check the Wolfe conditions at alpha if it was computed
       by a quadratically accurate formula. However, below we can change
       this decision if the value of the derivative implies that the
       Wolfe conditions cannot be satisfied.

       As the cg_descent converges, the function values typically
       approach a constant value. When this happens, the cubic interpolation
       step in the line search loses its accuracy and it is better to
       use a secant step based on the derivative of the objective function.
       AvoidFeval is TRUE when the function values are close together.  */

    AvoidFeval = cgcom->AvoidFeval ;

    /* repeat = FALSE => implies that this is the initial attempt to
       satisfy the Wolfe conditions */
    if ( repeat == FALSE )
    {
        alpha = cgcom->alpha ;
        /* It is advantageous to have both the function value and
           derivative except when QuadOK = F and AvoidFeval = T.
           In this case, we will not check the Wolfe conditions, and
           since the function values have converged, the line search
           is based on the derivative. */
        if ( (cgcom->QuadOK == FALSE) && (AvoidFeval == TRUE) )
        {
            /* if the value of the objective at alpha exists, we
               nonetheless make note of it */
            if ( (cgcom->f_at >= CGZERO) && (alpha == cgcom->f_at) )
            {
                qb = TRUE ;
            }
            else
            {
                qb = FALSE ;
            }
            /* evaluate derivative if not present */
            if ( (cgcom->df_at < CGZERO) || (alpha != cgcom->df_at) )
            {
                status = XXCG(evaluate) (CGZERO, &alpha, "g", PASA_CG_COM) ;
                if ( status == CG_FUNCTION_NAN_OR_INF )
                {
                    return (status) ;
                }
            }
        }
        else /* we want to have both the objective value and derivative */
        {
            qb = TRUE ;
            a0 = alpha ;
            /* if function has already been computed, only need derivative */
            if ( (cgcom->f_at >= CGZERO) && (alpha == cgcom->f_at) )
            {
                status = XXCG(evaluate) (CGZERO, &alpha, "g", PASA_CG_COM) ;
            }
            /* if derivative has already been computed, only need value */
            else if ( (cgcom->df_at >= CGZERO) && (alpha == cgcom->df_at) )
            {
                status = XXCG(evaluate) (CGZERO, &alpha, "f", PASA_CG_COM) ;
            }
            /* otherwise both value and derivative are needed */
            else
            {
                a0 = -CGONE ;
                status = XXCG(evaluate) (CGZERO, &alpha, "fg", PASA_CG_COM) ;
            }
            /* since the evaluation routine decreases alpha when an nan
               or inf is encountered, it is possible in the first 2 cases
               above that the function and derivative were computed at
               different points */
            if ( (a0 >= CGZERO) && (a0 != alpha) )
            {
                status = XXCG(evaluate) (CGZERO, &alpha, "fg", PASA_CG_COM) ;
            }
            /* if the function was nan or inf everywhere it was evaluated,
               then return with error */
            if ( status == CG_FUNCTION_NAN_OR_INF )
            {
                return (status) ;
            }
        }

        /* if objective has been evaluated, then again check its reliability,
           and make any necessary adjustments for a Wolfe line search */
        if ( qb == TRUE )
        {
            fb = cgcom->f ;
            if ( !approxstep )
            {
                fb -= alpha*cgcom->wolfe_hi ;
            }

            if (fabs (cgcom->f-cgcom->f0) <= Parm->CostConverge*fabs (cgcom->f))
            {
                AvoidFeval = TRUE ;
            }
            else
            {
                AvoidFeval = FALSE ;
            }
        }
    }
    else /* this is second attempt to satisfy Wolfe conditions */
    {
        cgcom->df = cgcom->savedf ;
        qb = cgcom->saveqb ;
        alpha = cgcom->savealpha ;
        if ( qb == TRUE )
        {
            fb = cgcom->f = cgcom->savefb ;
        }
    }
    b = alpha ;

    if ( approxstep )
    {
        db = cgcom->df ;
        d0 = da = cgcom->df0 ;
    }
    else
    {

/*printf ("df: %e\n", cgcom->df) ;*/
/*printf ("wolfe_hi: %e\n", cgcom->wolfe_hi) ;*/
        db = cgcom->df - cgcom->wolfe_hi ;
        d0 = da = cgcom->df0 - cgcom->wolfe_hi ;

        /* save data in case we repeat the line search using approxstep */
        cgcom->savedf = cgcom->df ;
        cgcom->savealpha = alpha ;
        cgcom->saveqb = qb ;
        if ( qb == TRUE )
        {
            cgcom->savefb = cgcom->f ;
        }
    }

    a = CGZERO ;
    a1 = CGZERO ;
    d1 = d0 ;
    fa = cgcom->f0 ; /* alpha = 0 so no adjustment for Wolfe step */
    if ( PrintLevel >= 1 )
    {
        fmt1 = "%9s %2s a: %13.6e b: %13.6e fa: %13.6e fb: %13.6e "
               "da: %13.6e db: %13.6e\n" ;
        fmt2 = "%9s %2s a: %13.6e b: %13.6e fa: %13.6e fb:  x.xxxxxxxxxx "
               "da: %13.6e db: %13.6e\n" ;
        fmt3 = "%9s %2s a: %13.6e b: %13.6e fa:  x.xxxxxxxxxx "
               "fb: %13.6e da: %13.6e db: %13.6e\n" ;
        if ( cgcom->QuadOK ) s2 = "OK" ;
        else               s2 = "" ;
        if ( qb ) printf (fmt1, "start    ", s2, a, b, fa, fb, da, db);
        else      printf (fmt2, "start    ", s2, a, b, fa, da, db) ;
    }

    /* if a quadratic interpolation step performed, then f was evaluated at b,
       check Wolfe conditions */
    if ( (cgcom->QuadOK == TRUE) && (cgcom->f <= cgcom->f0) )
    {
        status = XXCG(Wolfe) (b, cgcom->f, cgcom->df, cgcom) ;
        if ( status == CG_WOLFE_OK )
        {
#ifdef PASA
            if ( alpha == maxstep )
            {
                return (CG_HITS_BOUNDARY) ;
            }
#endif
            return (status) ; /* Wolfe conditions hold */
        }
    }

    /* For a nice function, the Wolfe line search might terminate above
       in the quadratic interpolation step.  If it does not terminate there
       and a full Wolfe line search is performed, then set cg->Wolfe to TRUE */
    if ( !approxstep )
    {
        cgcom->Wolfe = TRUE ;
    }

    /*Find initial interval [a,b] such that
      da <= 0, db >= 0, fa <= fpert = [(f0 + eps*fabs (f0)) or (f0 + eps)] */
    rho = Parm->rho ;
    ExpandSafe = Parm->ExpandSafe ;
    ngrow = 1 ;
    qa = TRUE ;
    while ( db < CGZERO ) /* need db >= 0 */
    {
        /* evaluate function at b if not yet evaluated there */
        if ( AvoidFeval == FALSE )
        {
            if ( !qb )
            {
                b0 = b ;
                status = XXCG(evaluate) (a, &b, "f", PASA_CG_COM) ;
                /* Note that the initial value of is reduced in the evaluation
                   routine if nan or infinite function value encountered. */
                if ( status == CG_FUNCTION_NAN_OR_INF )
                {
                    return (status) ;
                }
                if ( b0 != b )
                {
                    status = XXCG(evaluate) (a, &b, "fg", PASA_CG_COM) ;
                    if ( status == CG_FUNCTION_NAN_OR_INF )
                    {
                        return (status) ;
                    }
                    db = cgcom->df ;
                }

                /* since the function was evaluated, we again check
                   on its reliability */
                if ( fabs (cgcom->f-cgcom->f0) <=
                                            Parm->CostConverge*fabs (cgcom->f) )
                {
                    AvoidFeval = TRUE ;
                }
                else
                {
                    AvoidFeval = FALSE ;
                }
 
                if ( approxstep )
                {
                    fb = cgcom->f ;
                    db = cgcom->df ;
                }
                else
                {
                    fb = cgcom->f - b*cgcom->wolfe_hi ;
                    db = cgcom->df - cgcom->wolfe_hi ;
                }
                qb = TRUE ;
            }
            if ( fb > cgcom->fpert ) /* contract interval [a, b] */
            {
                status = XXCG(contract) (&a, &fa, &da, &b, &fb,&db,PASA_CG_COM);
                if ( status == CG_WOLFE_OK )
                {
#ifdef PASA
                    if ( cgcom->alpha == maxstep )
                    {
                        /* cg hits boundary, restart cg_descent*/
                        return (CG_HITS_BOUNDARY) ;
                    }
#endif
                    return (status) ; /* Wolfe conditions hold */
                }
                else if ( status == CG_INTERVAL_OK ) /* db >= 0 */
                {
                    /* we now have fa <= fpert, da <= 0, and db >= 0,
                       go to the line search below */
                    break ;
                }
                else if ( (status == CG_EXCESSIVE_UPDATING_OF_PERT_EPS) ||
                          (status == CG_FUNCTION_NAN_OR_INF) )
                {
                    return (status) ;
                }
                /* else new fpert generated so that fb <= fpert */
            }
        }

        /* fb <= fpert and db < 0 */
#ifdef PASA
        if ( b == maxstep ) /* b cannot grow further in pasa */
        {
            /* cg hits boundary, restart cg_descent*/
            cgcom->alpha = b ;
            return (CG_HITS_BOUNDARY) ; /* restart cg_descent */
        }
#endif

        /* expansion phase */
        ngrow++ ;
        if ( ngrow > Parm->maxsteps )
        {
            return (CG_SLOPE_ALWAYS_NEGATIVE) ;
        }
        /* update interval (a replaced by b) */
        a = b ;
        if ( qb == TRUE )
        {
            fa = fb ;
            qa = TRUE ;
        }
        else
        {
            qa = FALSE ;
        }
        da = db ;
        /* store old values of a and corresponding derivative */
        d2 = d1 ;
        d1 = da ;
        a2 = a1 ;
        a1 = a ;

        bmin = rho*b ;
        if ( (ngrow == 2) || (ngrow == 3) || (ngrow == 6) )
        {
            if ( d1 > d2 )
            {
                /* Use secant to estimate the spot where derivative vanishes
                   since secant moves us to the right. Based on the
                   value of the derivative at a0 = 0, a1 and a2, we can
                   obtain an estimate for the third derivative. If the
                   estimate is positive, then the second derivative of the
                   first derivative is positive, and the secant method takes
                   us past the root of the first derivative. Note that when
                   ngrow = 2, a0 = a1 = 0, so we cannot estimate the second
                   derivative. */
                if ( (ngrow == 2) || ((d1-d2)/(a1-a2) >= (d2-d0)/a2) )
                {
                    b = a1 - (a1-a2)*(d1/(d1-d2)) ;
                }
                else
                {
                    /* The estimate of the second derivative is negative,
                       so the secant method is short of the the true root.
                       SecantAmp is a parameter that increases the step. */
                    {
                        b = a1 - Parm->SecantAmp*(a1-a2)*(d1/(d1-d2)) ;
                    }
                }
                /* safeguard growth */
                t = ExpandSafe*a1 ;
                if ( b > t )
                {
                    b = t ;
#if 0
                    /* rho smaller than ExpandSafe, set rho = ExpandSafe */
                    if ( rho < ExpandSafe )
                    {
                        rho = ExpandSafe ;
                    }
                    ExpandSafe *= Parm->RhoGrow ;
#endif
                }
            }
            else /* secant method makes no sense, must be far from the root,
                    increase rho and hence bmin above */
            {
                rho *= Parm->RhoGrow ;
            }
        }
        else
        {
            rho *= Parm->RhoGrow ;
        }
        b = CGMAX (bmin, b) ;
        if ( b > maxstep )
        {
            b = maxstep ;
        }
        status = XXCG(evaluate) (a, &b, "fg", PASA_CG_COM) ;
        if ( status == CG_FUNCTION_NAN_OR_INF )
        {
            return (status) ;
        }
        cgcom->alpha = b ;
        qb = TRUE ;
        /* since the function was evaluated, we again check on its reliability*/
        if ( fabs (cgcom->f-cgcom->f0) <= Parm->CostConverge*fabs (cgcom->f) )
        {
            AvoidFeval = TRUE ;
        }
        else
        {
            AvoidFeval = FALSE ;
        }
        if ( approxstep )
        {
            fb = cgcom->f ;
            db = cgcom->df ;
        }
        else
        {
            db = cgcom->df - cgcom->wolfe_hi ;
            fb = cgcom->f - b*cgcom->wolfe_hi ;
        }
        if ( PrintLevel >= 2 )
        {
            if ( cgcom->QuadOK ) s2 = "OK" ;
            else                 s2 = "" ;
            if ( qa == TRUE )
            {
                printf (fmt1, "expand   ", s2, a, b, fa, fb, da, db) ;
            }
            else
            {
                printf (fmt3, "expand   ", s2, a, b, fb, da, db) ;
            }
        }
    }

    /* We now have fa <= fpert, da <= 0, db >= 0; hence, the iteration is
       trapped in [a, b] and will not hit the boundary where a new
       constraint becomes active */
    toggle = 0 ;
    width = b - a ;
    for (iter = 0; iter < Parm->maxsteps; iter++)
    {
        /* determine the next iterate */
        if ( (toggle == 0) || ((toggle == 2) && ((b-a) <= width)) )
        {
            cgcom->QuadOK = TRUE ;
            if ( cgcom->UseCubic && qa && qb && (AvoidFeval == FALSE) )
            {
                s1 = "cubic 0  " ;
                alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
                if ( (alpha <= a) || (alpha >= b) ) /* use secant method */
                {
                    s1 = "secant 0 " ;
                    if      ( -da  < db ) alpha = a - (a-b)*(da/(da-db)) ;
                    else if (  da != db ) alpha = b - (a-b)*(db/(da-db)) ;
                    else                  alpha = -1. ;
                }
            }
            else
            {
                s1 = "secant 0 " ;
                if      ( -da  < db ) alpha = a - (a-b)*(da/(da-db)) ;
                else if (  da != db ) alpha = b - (a-b)*(db/(da-db)) ;
                else                  alpha = -1. ;
            }
            width = Parm->stepdecay*(b - a) ;
        }
        else if ( toggle == 1 ) /* another variation of cubic interpolation */
        {
            cgcom->QuadOK = TRUE ;
            if ( cgcom->UseCubic && (AvoidFeval == FALSE) )
            {
                s1 = "cubic 1  " ;
                if ( (alpha == a) && (a-a0 < b-a) && qa0 )
                {
                    /* a is most recent iterate and is closer to a0 than to b */
                    alpha = XXCG(cubic) (a0, fa0, da0, a, fa, da) ;
                }
                else if ( alpha == a && qb )
                {
                    /* a is most recent iterate and is closer to b than to a0 */
                    alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
                }
                else if ( alpha == b ) /* b is most recent iterate */
                {
                    /* check if b is closer to b0 than to a */
                    if ( (b0 - b < b - a) && qb0 )
                    {
                        alpha = XXCG(cubic) (b, fb, db, b0, fb0, db0) ;
                    }
                    else if ( qb && qa )      /* b is closer to a than to b0 */
                    {
                        alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
                    }
                    else
                    {
                        alpha = -1. ;
                    }
                }
                else
                {
                    alpha = -1. ;
                }

                /* if alpha no good, use cubic between a and b */
                if ( (alpha <= a) || (alpha >= b) )
                {
                    if ( qa && qb  )
                    {
                        alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
                    }
                    else
                    {
                        alpha = -1. ;
                    }
                }

                /* if alpha still no good, use secant method between a and b */
                if ( alpha < CGZERO )
                {
                    s1 = "secant 1 " ;
                    if      ( -da  < db ) alpha = a - (a-b)*(da/(da-db)) ;
                    else if (  da != db ) alpha = b - (a-b)*(db/(da-db)) ;
                    else                  alpha = -1. ;
                }
            }
            else /* ( use secant ) */
            {
                s1 = "secant 1b" ;
                if ( (alpha == a) && (da > da0) )/* use a0 if possible*/
                {
                    alpha = a - (a-a0)*(da/(da-da0)) ;
                }
                else if ( db < db0 )/* try b0 */
                {
                    alpha = b - (b-b0)*(db/(db-db0)) ;
                }
                else /* secant based on a and b */
                {
                    if      ( -da  < db ) alpha = a - (a-b)*(da/(da-db)) ;
                    else if (  da != db ) alpha = b - (a-b)*(db/(da-db)) ;
                    else                  alpha = -1. ;
                }

                if ( (alpha <= a) || (alpha >= b) )
                {
                    if      ( -da  < db ) alpha = a - (a-b)*(da/(da-db)) ;
                    else if (  da != db ) alpha = b - (a-b)*(db/(da-db)) ;
                    else                  alpha = -1. ;
                }
            }
        }
        else
        {
            alpha = .5*(a+b) ; /* use bisection if b-a decays slowly */
            s1 = "bisection" ;
            cgcom->QuadOK = FALSE ;
        }

        if ( (alpha <= a) || (alpha >= b) )
        {
            alpha = .5*(a+b) ;
            s1 = "bisection" ;
            if ( (alpha == a) || (alpha == b) )
            {
                return (CG_WOLFE_CONDITIONS_NOT_SATISFIED) ;
            }
            cgcom->QuadOK = FALSE ; /* bisection was used */
        }

        if ( toggle == 0 ) /* save values for next iteration */
        {
            a0 = a ;
            b0 = b ;
            da0 = da ;
            db0 = db ;
            if ( qa )
            {
                fa0 = fa ;
                qa0 = TRUE ;
            }
            else
            {
                qa0 = FALSE ;
            }
            if ( qb )
            {
                fb0 = fb ;
                qb0 = TRUE ;
            }
            else
            {
                qb0 = FALSE ;
            }
        }

        toggle++ ;
        if ( toggle > 2 ) toggle = 0 ;

        status = XXCG(evaluate) (a, &alpha, "fg", PASA_CG_COM) ;
        if ( status == CG_FUNCTION_NAN_OR_INF )
        {
            return (status) ;
        }

        /* since the function was evaluated, we again check
           on its reliability */
        if ( fabs (cgcom->f-cgcom->f0) <= Parm->CostConverge*fabs (cgcom->f) )
        {
            AvoidFeval = TRUE ;
        }
        else
        {
            AvoidFeval = FALSE ;
        }
        f = cgcom->f ;
        df = cgcom->df ;
        if ( cgcom->QuadOK )
        {
            status = XXCG(Wolfe) (alpha, f, df, cgcom) ;
            if ( status == CG_WOLFE_OK )
            {
                cgcom->alpha = alpha ;
                if ( PrintLevel >= 2 )
                {
                    printf ("             a: %13.6e f: %13.6e df: %13.6e %1s\n",
                             alpha, f, df, s1) ;
                }
                return (status) ;
            }
        }
        if ( !approxstep )
        {
            f -= alpha*cgcom->wolfe_hi ;
            df -= cgcom->wolfe_hi ;
        }
        if ( df >= CGZERO )
        {
            b = alpha ;
            fb = f ;
            db = df ;
            qb = TRUE ;
        }
        else if ( f <= cgcom->fpert )
        {
            a = alpha ;
            fa = f ;
            da = df ;
        }
        else /* df < 0 and f > fpert try to contract interval [a, alpha] */
        {
            CGFLOAT B, fB, dB ;
            B = alpha ;
            fB = f ;
            dB = df ;
            qb = TRUE ;
            /* contract interval [a, alpha] */
            status = XXCG(contract) (&a, &fa, &da, &B, &fB, &dB, PASA_CG_COM) ;
            if ( (status == CG_WOLFE_OK) ||
                 (status == CG_EXCESSIVE_UPDATING_OF_PERT_EPS) ||
                 (status == CG_FUNCTION_NAN_OR_INF) )
            {
                return (status) ;
            }
            if ( status == CG_NEW_PERT )
            {
                a = alpha ;
                fa = f ;
                da = df ;
            }
            else /* interval OK, returned B has positive derivative */
            {
                toggle = 0 ;
                b = B ;
                fb = fB ;
                db = dB ;
            }
        }
        if ( PrintLevel >= 2 )
        {
            if ( cgcom->QuadOK ) s2 = "OK" ;
            else                 s2 = "" ;
            if ( qa && !qb )     printf (fmt2, s1, s2, a, b, fa, da, db) ;
            else if ( qa && qb ) printf (fmt1, s1, s2, a, b, fa, fb, da, db) ;
            else /* !qa && qb */ printf (fmt3, s1, s2, a, b, fb, da, db) ;
        }
    }
    return (CG_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS) ;
}

/* =========================================================================
   ==== cg_contract ========================================================
   =========================================================================
   The input for this routine is an interval [a, b] with the property that
   fa <= fpert, da <= 0, db <= 0, and fb >= fpert. The returned status is
   Return:
       CG_WOLFE_OK            (Wolfe conditions are satisfied)
       CG_INTERVAL_OK         (a subinterval [a, b] is generated with the
                               property that fa <= fpert, da <= 0 and db >= 0)
       CG_NEW_PERT            (db < 0 and a new fpert is generated so that
                               fb < fpert -- hence, b can grow in the line
                               search)
       CG_EXCESSIVE_UPDATING_OF_PERT_EPS
       CG_FUNCTION_NAN_OR_INF

   NOTE: The input arguments are unchanged when status = CG_NEW_PERT since
         we need to move the original b to the right
   ========================================================================= */
int XXCG(contract)
(
    CGFLOAT       *A, /* left side of bracketing interval */
    CGFLOAT      *fA, /* function value at a */
    CGFLOAT      *dA, /* derivative at a */
    CGFLOAT       *B, /* right side of bracketing interval */
    CGFLOAT      *fB, /* function value at b */
    CGFLOAT      *dB, /* derivative at b */
#ifdef PASA
    PASAcom *pasacom,
#endif
    CGcom     *cgcom
)
{
    int approxstep, iter, PrintLevel, toggle, status ;
    CGFLOAT a, alpha, b, old, da, db, df, dold, f0, f, fa, fb, fold, t, width ;
    char *s ;
    CGparm *Parm ;

    approxstep = cgcom->approxstep ;
    Parm = cgcom->Parm ;
    PrintLevel = Parm->PrintLevel ;
    a = *A ;
    fa = *fA ;
    da = *dA ;
    b = *B ;
    fb = *fB ;
    db = *dB ;
    f0 = cgcom->f0 ;
    t = Parm->eps_grow*(fb-f0) ;
    toggle = 0 ;
    width = CGZERO ;
    for (iter = 0; iter < Parm->ncontract; iter++)
    {
        if ( (toggle == 0) || ((toggle == 2) && ((b-a) <= width)) )
        {
            /* cubic based on bracketing interval */
            alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
            toggle = 0 ;
            width = Parm->stepdecay*(b-a) ;
            cgcom->QuadOK = TRUE ;
        }
        else if ( toggle == 1 )
        {
            cgcom->QuadOK = TRUE ;
            /* cubic based on most recent iterate and smallest value */
            if ( (old < a) && (a - old < b - a) )
            {
                /* a is most recent iterate and a is closer to old than to b */
                alpha = XXCG(cubic) (a, fa, da, old, fold, dold) ;
            }
            else if ( (b < old) && (old - b < b - a) )
            {
                /* b is most recent iterate and b is closer to old than to a */
                alpha = XXCG(cubic) (b, fb, db, old, fold, dold) ;
            }
            else
            {
                alpha = XXCG(cubic) (a, fa, da, b, fb, db) ;
            }
        }
        else
        {
            alpha = .5*(a+b) ; /* use bisection if b-a decays slowly */
            cgcom->QuadOK = FALSE ;
        }

        if ( (alpha <= a) || (alpha >= b) )
        {
            alpha = .5*(a+b) ;
            cgcom->QuadOK = FALSE ; /* bisection was used */
        }

        toggle++ ;
        if ( toggle > 2 ) toggle = 0 ;

        status = XXCG(evaluate) (a, &alpha, "fg", PASA_CG_COM) ;
        if ( status == CG_FUNCTION_NAN_OR_INF )
        {
            return (status) ;
        }

        f = cgcom->f ;
        df = cgcom->df ;

        if ( cgcom->QuadOK )
        {
            status = XXCG(Wolfe) (alpha, f, df, cgcom) ;
            if ( status == CG_WOLFE_OK )
            {
                cgcom->alpha = alpha ;
                return (status) ;
            }
        }
        if ( !approxstep )
        {
            f -= alpha*cgcom->wolfe_hi ;
            df -= cgcom->wolfe_hi ;
        }
        if ( df >= CGZERO ) /* done */
        {
            *B = alpha ;
            *fB = f ;
            *dB = df ;
            *A = a ;
            *fA = fa ;
            *dA = da ;
            return (CG_INTERVAL_OK) ;
        }
        if ( f <= cgcom->fpert ) /* update a using alpha */
        {
            old = a ;
            a = alpha ;
            fold = fa ;
            fa = f ;
            dold = da ;
            da = df ;
        }
        else                     /* update b using alpha */
        {
            old = b ;
            b = alpha ;
            fold = fb ;
            fb = f ;
            dold = db ;
            db = df ;
        }
        if ( PrintLevel >= 2 )
        {
            if ( cgcom->QuadOK ) s = "OK" ;
            else                 s = "" ;
            printf ("contract  %2s a: %13.6e b: %13.6e fa: %13.6e fb: "
                    "%13.6e da: %13.6e db: %13.6e\n", s, a, b, fa, fb, da, db) ;
        }
    }

    /* cg_contract was unable to either satisfy the Wolfe conditions or
       obtain db >= 0. Return to the line search with a larger value for
       fpert. Check to see if the Wolfe conditions are satisfied. */
    f0 = cgcom->f0 ;
    if ( cgcom->PertRule == 1 )
    {
        if ( f0 != CGZERO )
        {
            cgcom->pert_eps = t/fabs (f0) ;
            cgcom->fpert = f0 + t ;
        }
        else
        {
            cgcom->fpert = 2.*fabs (*fB) ;
        }
    }
    else /* PertRule = 0 */
    {
        cgcom->pert_eps = t ;
        cgcom->fpert = f0 + t ;
    }
    /* count the number of times that pert_eps was modified */
    cgcom->neps++ ;

    /* check to see if the Wolfe line search conditions are now satisfied at
       the last iterate alpha */
    status = XXCG(Wolfe) (alpha, f, df, cgcom) ;
    if ( status == CG_WOLFE_OK )
    {
        cgcom->alpha = alpha ;
        return (status) ;
    }

    /* check to see if the Wolfe line search conditions are now satisfied at
       the right side of the original interval */
    status = XXCG(Wolfe) (*B, *fB, *dB, cgcom) ;
    if ( status == CG_WOLFE_OK )
    {
        cgcom->alpha = *B ;
        cgcom->f = *fB ;
        cgcom->df = *dB ;
        return (status) ;
    }

    /* If Wolfe conditions do not hold, then we have *fB > fpert, do not
       modify the returned arguments of cg_contract. */
    if ( cgcom->neps >= Parm->neps )
    {
        return (CG_EXCESSIVE_UPDATING_OF_PERT_EPS) ;
    }
    else
    {
        return (CG_NEW_PERT) ;
    }
}

/* =========================================================================
   ==== cg_cubic ===========================================================
   =========================================================================
   Compute the minimizer of a Hermite cubic. If the computed minimizer
   outside [a, b], return -1 (it is assumed that a >= 0).
   ========================================================================= */
CGFLOAT XXCG(cubic)
(
    CGFLOAT  a,
    CGFLOAT fa, /* function value at a */
    CGFLOAT da, /* derivative at a */
    CGFLOAT  b,
    CGFLOAT fb, /* function value at b */
    CGFLOAT db  /* derivative at b */
)
{
    CGFLOAT c, d1, d2, delta, t, v, w ;
    delta = b - a ;
    if ( delta == CGZERO ) return (a) ;
    v = da + db - 3.*(fb-fa)/delta ;
    t = v*v - da*db ;
    if ( t < CGZERO ) /* complex roots, use secant method */
    {
         if ( fabs (da) < fabs (db) ) c = a - (a-b)*(da/(da-db)) ;
         else if ( da != db )         c = b - (a-b)*(db/(da-db)) ;
         else                         c = -1 ;
         return (c) ;
    }

    if ( delta > CGZERO ) w = sqrt(t) ;
    else                  w =-sqrt(t) ;
    d1 = da + v - w ;
    d2 = db + v + w ;
    if ( (d1 == CGZERO) && (d2 == CGZERO) ) return (-1.) ;
    if ( fabs (d1) >= fabs (d2) ) c = a + delta*da/d1 ;
    else                          c = b - delta*db/d2 ;
    return (c) ;
}

#ifdef PASA
/* =========================================================================
   ==== cg_maxstep =========================================================
   =========================================================================
   Determine the maximum feasible step in the search direction.
   ========================================================================= */
CGFLOAT XXCG(maxstep)
(
    PASAcom *pasacom,
    CGcom     *cgcom
)
{
    CGINT boundindex, constraintindex, i, j, n, ni, p, q, row,
         *ineq_row, *ATp, *ATi ;
    CGFLOAT maxstep, s, t, *Adk, *Axk, *ATx, *bl, *bu, *d, *lo, *hi, *x ;
    PPprob *Prob ;
    PPwork *Work ;

/*printf ("check maxstep\n") ;*/
    const int loExists = pasacom->loExists ;
    const int hiExists = pasacom->hiExists ;
    const int use_napheap = pasacom->use_napheap ;
    const int use_pproj = pasacom->use_pproj ;
    const int use_penalty = pasacom->use_penalty ;
    const int Aexists = pasacom->Aexists ;
    n = pasacom->nf ;
/*printf ("nf in maxstep: %i\n", n) ;*/
    lo = pasacom->lo ;
    hi = pasacom->hi ;
    d = cgcom->d ;
    x = cgcom->x ;
    maxstep = CGINF ;
    boundindex = 0 ;
    pasacom->boundtype = 0 ;
    /* first find the maxstep based on the bounds */
    for (j = 0; j < n; j++)
    {
        if ( hiExists && (d [j] > CGZERO) )
        {
/*printf ("j: %i hi: %e x: %e d: %e\n", j, hi [j], x [j], d [j]) ;*/
            t = (hi [j]-x [j])/d [j] ;
            if ( t < maxstep )
            {
                maxstep = t ;
                boundindex = j + 1 ;
/*printf ("j: %i hi: %e x: %e d: %e maxstep: %e\n",
         j, hi [j], x [j], d [j], maxstep) ;*/
            }
        }
        else if ( loExists && (d [j]  < CGZERO) )
        {
/* printf ("j: %i lo: %e x: %e d: %e\n", j, lo [j], x [j], d [j]) ;*/
            t = (lo [j]-x [j])/d [j] ;
            if ( t < maxstep )
            {
                maxstep = t ;
                boundindex = -(j + 1) ;
/* printf ("j: %i lo: %e x: %e d: %e maxstep: %e\n",
         j, lo [j], x [j], d [j], maxstep) ; */
            }
        }
/*printf ("maxstep: %e\n", maxstep) ;*/
    }
    /* if a bound becomes active, then save it, and the boundtype is +1 */
    if ( boundindex != 0 )
    {
        pasacom->boundtype = 1 ;
    }
    pasacom->boundindex = boundindex ;

    /* Next, find the maxstep based on the inequality constraints.
       If the penalty technique is employed, we also need to compute
       the products Ad and A'Ad. If we are not using the penalty
       technique, then we only need the product between the inactive
       rows of A and d. */
    if ( use_pproj == TRUE )
    {
        bl = pasacom->bl ;
        bu = pasacom->bu ;
        Work = pasacom->ppcom->Work ;
        ATp = Work->ATp ;
        ATi = Work->ATi ;
        ATx = Work->ATx ;
        Axk = pasacom->Axk ;
        Adk = pasacom->Adk ;

        if ( use_penalty == TRUE )
        {
            PPINT l, nrow, *ir ;
            PPFLOAT *AAd ;
            AAd = cgcom->AAd ;
            pasa_initx (AAd, PASAZERO, n) ;
            ir = Work->ir ;
            pasacom->Ad2 = CGZERO ;
            nrow = pasacom->nrow ;
            constraintindex = 0 ;
            p = 0 ;
            l = 0 ;
            for (i = 0; i < nrow; i++)
            {
                s = CGZERO ;
                q = ATp [i+1] ;
                for (; p < q; p++)
                {
                    s += ATx [p]*d [ATi [p]] ;
                }
                if ( ir [i] == 0 )
                {
                    pasacom->Ad2 += s*s ;
                    p = ATp [i] ;
                    for (; p < q; p++)
                    {
                        AAd [ATi [p]] += ATx [p]*s ;
                    }
                }
                else
                {
                    l++ ;
                    Adk [l] = s ;
                    if ( s > CGZERO )
                    {
                        t = (bu [l] - Axk [l])/s ;
                        if ( t < maxstep )
                        {
                            maxstep = t ;
                            constraintindex = l ;
                        }
                    }
                    else if ( s < CGZERO )
                    {
                        t = (bl [l] - Axk [l])/s ;
                        if ( t < maxstep )
                        {
                            maxstep = t ;
                            constraintindex = -l ;
                        }
                    }
                    else
                    {
                        continue ;
                    }
                }
            }
            pasacom->Ad2 *= pasacom->penalty ;
        }
        else /* focus on the inactive inequalities */
        {
            constraintindex = 0 ;
            Prob = pasacom->ppcom->Prob ;
            ni = Prob->ni ;
            if ( ni > 0 )
            {
                ineq_row = Prob->ineq_row ;
                for (i = 1; i <= ni; i++)
                {
                    row = ineq_row [i] ;
                    s = CGZERO ;
                    q = ATp [row+1] ;
                    for (p = ATp [row]; p < q; p++)
                    {
                        s += ATx [p]*d [ATi [p]] ;
                    }
                    Adk [i] = s ;
                    if ( s > CGZERO )
                    {
                        t = (bu [i] - Axk [i])/s ;
                        if ( t < maxstep )
                        {
                            maxstep = t ;
                            constraintindex = i ;
                        }
                    }
                    else if ( s < CGZERO )
                    {
                        t = (bl [i] - Axk [i])/s ;
                        if ( t < maxstep )
                        {
                            maxstep = t ;
                            constraintindex = -i ;
                        }
                    }
                    else
                    {
                        continue ;
                    }
                }
            }
        }
    }
    else if ( use_napheap == TRUE )
    {
        CGFLOAT *a ;
        a = pasacom->nap_a ;
        s = cg_dot (a, d, n) ;
        constraintindex = 0 ;
        if ( use_penalty == TRUE ) /* => linear constraint is active */
        {
            pasacom->Ad2 = s*s*pasacom->penalty ;
            cg_scale (cgcom->AAd, a, s, n) ;
        }
        else if ( pasacom->nap_constraint == 0 ) /* => inactive linear const. */
        {
            pasacom->Adk [1] = s ;
            /* determine the maxstep */
            if ( s > CGZERO )
            {
                t = (pasacom->nap_bu - pasacom->Axk [1])/s ;
                if ( t < maxstep )
                {
                    maxstep = t ;
                    constraintindex = 1 ;
                }
            }
            else if ( s < CGZERO )
            {
                t = (pasacom->nap_bl - pasacom->Axk [1])/s ;
                if ( t < maxstep )
                {
                    maxstep = t ;
                    constraintindex = -1 ;
                }
            }
        }
    }
    if ( Aexists == TRUE )
    {
        /* if an inequality constraint becomes active before a bound index,
           then save it, and the boundtype is -1  */
        if ( constraintindex != 0 )
        {
            pasacom->boundtype = -1 ;
            pasacom->boundindex = constraintindex ;
        }
    }
    maxstep = CGMAX (CGZERO, maxstep) ;
    if ( cgcom->Parm->PrintLevel >= 1 )
    {
        printf ("boundtype: %i index: %ld maxstep: %e\n",
                 pasacom->boundtype, (LONG) pasacom->boundindex, maxstep) ;
    }
    cgcom->maxstep = pasacom->maxstep = maxstep ;
    return (maxstep) ;
}

/* =========================================================================
   ==== cg_checktol ========================================================
   =========================================================================
   This routine is entered when the nominal stopping criterion
   pasacom->e <= switchfactor*pasacom->E is satisfied where pasacom->E is the
   global error bound before entering CG. The goal is to decide what
   is done next. There are four possibilities:

   1. Terminate with status = PASA_ERROR_TOLERANCE_SATISFIED if the global
      error is sufficiently small.
   2. Terminate CG and return to grad_proj where bound variables are
      freed.
   3. If use_penalty is TRUE, then we could update the multiplier and
      penalty term and continue CG but with a restart.
   4. Continue the current iteration but with an updated (smaller)
      pasacom->E value.

   Recall that the optimization problem is

   min f(x) subject to lo <= x <= hi, bl <= Ax <= bu

   Let L(x, y) = f(x) + y'(Ax - b) be the Lagrangian where b_i = 0 if
   bl_i < (Ax)_i < bu_i, b_i = bu_i if (Ax)_i = bu_i, and b_i = bl_i otherwise.
   The first-order optimality conditions are that

       L'_j (x, y)  = 0 if lo_j < x_j < hi_j,
       L'_j (x, y) <= 0 if        x_j = hi_j,
       L'_j (x, y) >= 0 if lo_j = x_j,
           y_i      = 0 if bl_i < (Ax)_i < bu_i,
           y_i     <= 0 if bl_i = (Ax)_i
           y_i     >= 0 if        (Ax)_i = bu_i

   max {|L'_j(x, y)| : lo_j < x_j < hi_j} is stored in Com->e (computed
   previously in null_project).  The multiplier is chosen so that y_i = 0
   when bl_i < (Ax)_i < bu_i.  We let maxsignerr denote the maximum
   violation of the sign constraints on L'_j (x, y) and on the multiplier y.
   The estimate for the Lagrange multiplier was computed previously in
   null_project.  Also, we determine the maximum amount, denoted maxeqerr,
   that the current iterate violates the polyhedral constraint.
   Our decision about what to do next is based on the following rules:

   A. If MAX (pasacom->e, maxsignerr, maxeqerr) <= pasacom->grad_tol,
      then we terminate with status = PASA_ERROR_TOLERANCE_SATISFIED.
   B. If pasacom->e <= switchfactor*maxsignerr, then we branch to grad_proj.
      The rationale is that we wish to determine the active constraints
      at the solution and reduce maxsignerr.
   C. If pasacom->e < switchfactor*maxeqerr and use_penalty is FALSE,
      then we branch to grad_proj.  The rationale is that there is no
      mechanism in CG for reducing the equation error when use_penalty
      is FALSE. On the other hand, grad_proj will project onto the
      feasible set and remove the error associated with constraint violation.
   D. If pasacom->e < switchfactor*maxeqerr and use_penalty is TRUE,
      then we update the multiplier and penalty term, and restart CG.
      The rationale is that we wish to reduce the violation in the
      constraint by utilizing the multiplier structure of the objective.
      The stopping condition is pasacom->e <=
      switchfactor*MAX (maxsignerr, maxeqerr, old pasacom->e).
   E. If pasacom->e >= switchfactor*maxeqerr, then continue
      CG with the new stopping condition pasacom->e <=
      switchfactor*MAX (maxsignerr, maxeqerr, old pasacom->e).

   When Aexists = FALSE and there are only bound constraints, maxeqerr = 0.
   ========================================================================= */
int XXCG(checktol) /* return:
                               PASA_ERROR_TOLERANCE_SATISFIED
                               PASA_GRAD_PROJ
                               CG_RESTART
                               CG_CONTINUE */
(
    CGFLOAT       *x, /* current iterate */
    PASAcom *pasacom,
    CGcom     *cgcom
)
{
    int Aexists, PrintLevel, relerr ;
    CGINT j, k, nc, nrow, *ATi, *ATp, *bound_cols, *RLinkUp ;
    CGFLOAT E, Lambda, maxeqerr, maxsignerr, penalty, residual, switchfactor,
            testtol_old, *ATx, *userg, *lambda, *temp ;
    PASAparm *Parm ;      /* parameters for PASA */
    PPwork *Work ;
    CGstat *Stat ;

    Parm = pasacom->pasaparm ; /* parameters */
    const int use_penalty = pasacom->use_penalty ;
    const int use_pproj = pasacom->use_pproj ;
    const int use_napheap = pasacom->use_napheap ;
    penalty = Parm->penalty ;
    switchfactor = Parm->switchfactor ;
    PrintLevel = Parm->PrintLevel ;
    Aexists = pasacom->Aexists ;
    Stat = cgcom->Stat ;

    if ( pasacom->QP )
    {
        userg = pasacom->gtot ;
    }
    else
    {
        userg = pasacom->userg ;
    }

    /* we use the max violation of the first order optimality conditions
       relative to multiplier signs to determine whether to decrease testtol */
    maxsignerr = CGZERO ;
    maxeqerr = CGZERO ;
    nc = pasacom->nc ;
    bound_cols = pasacom->bound_cols ;
    nrow = pasacom->nrow ;
    if ( use_pproj == TRUE )
    {
        Work = pasacom->ppcom->Work ;
        RLinkUp = Work->RLinkUp ;
        /* the problem is effectively bound constrained if there are no
           active equations */
        if ( RLinkUp [nrow] == nrow )
        {
            Aexists = FALSE ;
        }
    }
    else if ( use_napheap == TRUE )
    {
        if ( (pasacom->nap_constraint == 0) || (pasacom->nap_a2 == PASAZERO) )
        {
            Aexists = FALSE ;
        }
    }
    if ( Aexists == FALSE ) /* only bound constraints present */
    {
        for (k = 0; k < nc; k++)
        {
            j = bound_cols [k] ;
            if ( j < 0 ) /* at lower bound */
            {
                j = -(j+1) ;
                maxsignerr = CGMAX (maxsignerr, -userg [j]) ;
            }
            else
            {
                maxsignerr = CGMAX (maxsignerr, userg [j]) ;
            }
        }
    }
#ifndef NOPPROJ
    else if ( use_pproj == TRUE ) /* linear equations/inequalities present*/
    {
        CGINT i, l, m, n, nr, p, q,
             *Ap, *Anz, *Ai, *bound_rows, *invperm, *ir, *RLinkDn ;
        CGFLOAT r, s, t, absAx, *Ax, *Axk, *b ;
        PPprob *Prob ;

        Prob = pasacom->ppcom->Prob ;

        /* If use_penalty is FALSE, then we can use lambda stored in
           pasacom->lambda for the multiplier. This lambda was computed
           during the last call to pasa_null_project.  If use_penalty is TRUE
           and we have not started the first iteration, then we can use
           the lambda computed at the top of CG (lambda_pen). Otherwise,
           we must update the lambda computed in null_project to take into
           account the fact that the complete multiplier is the sum
           of the multiplier computed in null_project, the multiplier
           lambda_pen obtained at the start of CG, and the penalty term
           p*(b-Bx). Instead of making these adjustments, we compute
           the multiplier from scatch here. Note though that time would
           be saved if the multiplier estimate was obtained by the update
           process. */
        lambda = pasacom->lambda ;
        if ( use_penalty == TRUE )
        {
            if ( Stat->iter == cgcom->FirstIter )
            {
                lambda = pasacom->lambda_pen ;
            }
            else /* compute lambda from scratch */
            {
                Ap = Prob->Ap ;
                Anz = Prob->Anz ;
                Ai = Prob->Ai ;
                Ax = Prob->Ax ;
                pasa_initx (lambda, CGZERO, nrow) ;
    
                /* use code from start of CG to estimate multiplier
                   NOTE: we could estimate the multiplier using the first-order
                         multiplier method update */
                n = pasacom->nf ;
                for (j = 0; j < n; j++)
                {
                    t = pasacom->g [j] ;
                    if ( t != PASAZERO )
                    {
                        k = Ap [j] ;
                        l = k + Anz [j] ;
                        for (; k < l; k++)
                        {
                            lambda [Ai [k]] += t*Ax [k] ;
                        }
                    }
                }
                RLinkDn = Work->RLinkDn ;
                pproj_lsol (Work->L, lambda, RLinkUp [nrow], nrow, RLinkUp) ;
                k = RLinkUp [nrow] ;
                /* momentarily set the initial RLinkDn to -1, this simplifies
                   indexing in dltsolve */
                RLinkDn [k] = -1 ;
                l = RLinkDn [nrow] ;
                pproj_dltsol (Work->L, lambda, lambda, l, k, RLinkDn) ;
                RLinkDn [k] = nrow ; /* restore RLinkDn */
            }
        }

        Ap = pasacom->Copy->Ap ;
        Ax = pasacom->Copy->Ax ;
        Ai = pasacom->Copy->Ai ;
        invperm = pasacom->invperm ;
        ir  = Work->ir ;
        for (k = 0; k < nc; k++)
        {
            j = bound_cols [k] ;
            if ( j < 0 ) /* at lower bound */
            {
                m = -(j+1) ;      /* user indexing */
                l = invperm [m] ; /* convert from user index to pproj index */
            }
            else
            {
                m = j ;
                l = invperm [j] ;
            }
            t = CGZERO ;
            q = Ap [l+1] ;
            for (p = Ap [l]; p < q; p++)
            {
                t -= lambda [Ai [p]]*Ax [p] ;
            }
            t += userg [m] ;
            if ( j < 0 ) /* variable at lower bound */
            {
                maxsignerr = CGMAX (maxsignerr, -t) ;
                if ( (PrintLevel >= 2) && (t < CGZERO) )
                {
                    printf ("lower bound %ld wrong sign: %e\n", (LONG) m, -t) ;
                }
            }
            else
            {
                maxsignerr = CGMAX (maxsignerr, t) ;
                if ( (PrintLevel >= 2) && (t > CGZERO) )
                {
                    printf ("upper bound %ld wrong sign: %e\n", (LONG) m, t) ;
                }
            }
        }
        nr = pasacom->nr ;
        bound_rows = pasacom->bound_rows ;
        for (k = 0; k < nr; k++)
        {
            j = bound_rows [k] ;
            if ( j < 0 ) /* at lower bound */
            {
                m = -(j+1) ;      /* row index */
                maxsignerr = CGMAX (maxsignerr, -lambda [m]) ;
                if ( (PrintLevel >= 2) && (lambda [m] < CGZERO) )
                {
                    printf ("lower ineqn %ld wrong sign: %e\n",
                           (LONG) m, -lambda [m]) ;
                }
            }
            else
            {
                m = j - 1 ;
                maxsignerr = CGMAX (maxsignerr, lambda [m]) ;
                if ( (PrintLevel >= 2) && (lambda [m] > CGZERO) )
                {
                    printf ("upper ineqn %ld wrong sign: %e\n",
                           (LONG) m, lambda [m]) ;
                }
            }
        }
/*pproj_error (-1, __FILE__, __LINE__, "stop") ;*/


        relerr = TRUE ;
        if ( pasacom->pprojparm->stop_condition == 1 ) /* use absolute error */
        {
            relerr = FALSE ;
        }

        /* maxeqerr is computed at top CG, otherwise compute it here */
        if ( Stat->iter > cgcom->FirstIter )
        {
            absAx = CGZERO ;   /* stores max_i sum_j |A_{ij}x_j| */
            ATp = Work->ATp ;
            ATi = Work->ATi ;
            ATx = Work->ATx ;
            temp = Work->arrayd ;
            pasa_initx (temp, PASAZERO, nrow) ;
            Axk = pasacom->Axk ;
            b = pasacom->b ;
            p = 0 ;
            l = 0 ;
            for (i = 0; i < nrow; i++)
            {
                r = s = CGZERO ;
                q = ATp [i+1] ;
                for (; p < q; p++)
                {
                    t = ATx [p]*x [ATi [p]] ;
                    s += t ;
                    r += fabs (t) ;
                }
                if ( r > absAx )
                {
                    absAx = r ;
                }
                if ( ir [i] == 0 )
                {
                    temp [i] = t = b [i] - s ;
                    if ( fabs (t) > maxeqerr )
                    {
                        maxeqerr = fabs (t) ;
                    }
                }
                else
                {
                    l++ ;
                    Axk [l] = s ;
                }
            }
            ASSERT (l == pasacom->ppcom->Prob->ni) ;
        }
        else /* extract absAx from pproj */
        {
            absAx = Work->absAx ;
        }
        if ( relerr == TRUE )
        {
            if ( absAx > CGZERO )
            {
                maxeqerr /= absAx ;
            }
        }
    }
#endif
    else if ( use_napheap == TRUE )
    {
        /* If use_penalty is FALSE, then we can use lambda stored in
           pasacom->lambda for the multiplier. This lambda was computed
           during the last call to pasa_null_project.  If use_penalty is TRUE
           and we have not started the first iteration, then we can use
           the lambda computed at the top of CG (lambda_pen). Otherwise,
           we must update the lambda computed in null_project to take into
           account the fact that the complete multiplier is the sum
           of the multiplier computed in null_project, the multiplier
           lambda_pen obtained at the start of CG, and the penalty term
           p*(b-Bx). Instead of making these adjustments, we compute
           the multiplier from scatch here. Note though that time would
           be saved if the multiplier estimate was obtained by the update
           process. */
        PASAINT m ;
        PASAFLOAT absAx, s, t, *a ;
        a = pasacom->nap_a ;
        Lambda = *(pasacom->lambda) ;
        if ( use_penalty == TRUE )
        {
            if ( Stat->iter == cgcom->FirstIter )
            {
                Lambda = *(pasacom->lambda_pen) ;
            }
            else /* compute lambda from scratch */
            {
                /* multiplier estimate = a'g/a'a */
                Lambda = pasa_dot (a, pasacom->g, pasacom->nf)/pasacom->nap_a2 ;
            }
        }
        for (k = 0; k < nc; k++)
        {
            j = bound_cols [k] ;
            if ( j < 0 ) /* at lower bound */
            {
                m = -(j+1) ;      /* user indexing */
            }
            else
            {
                m = j ;
            }
            t = userg [m] - Lambda*pasacom->nap_auser [m] ;
            if ( j < 0 ) /* variable at lower bound */
            {
                maxsignerr = CGMAX (maxsignerr, -t) ;
                if ( (PrintLevel >= 2) && (t < CGZERO) )
                {   
                    printf("lower bound %ld (user index) wrong sign: %e\n",
                          (LONG) m, -t) ;
                }

            }
            else
            {
                maxsignerr = CGMAX (maxsignerr, t) ;
                if ( (PrintLevel >= 2) && (t > PASAZERO) )
                {
                    printf("upper bound %ld (user index) wrong sign: %e\n",
                          (LONG) m, t) ;
                }

            }
        }
        if ( pasacom->nr > 0 )
        {
            if ( pasacom->bound_rows [0] < 0 ) /* at lower bound */
            {
                maxsignerr = PASAMAX (maxsignerr, -Lambda) ;
                if ( (PrintLevel >= 2) && (Lambda < PASAZERO) )
                {   
                    printf ("lower ineqn %i wrong sign: %e\n", 0, -Lambda) ;
                }
            }
            else                           /* at upper bound */
            {
                maxsignerr = PASAMAX (maxsignerr, Lambda) ;
                if ( (PrintLevel >= 2) && (Lambda > PASAZERO) )
                {   
                    printf ("upper ineqn %i wrong sign: %e\n", 0, Lambda) ;
                }
            }
        }
 
        relerr = TRUE ;
        absAx = CGZERO ;
        s = CGZERO ;
        for (j = 0; j < pasacom->nf; j++)
        {
            t = a [j]*x [j] ;
            s += t ;
            absAx += fabs (t) ;
        }
        residual = pasacom->nap_bl - s ;
        maxeqerr = fabs (residual) ;
        if ( relerr == TRUE )
        {
            if ( absAx > CGZERO )
            {
                maxeqerr /= absAx ;
            }
        }
    }

    /* TEST A: If MAX (pasacom->e, maxsignerr, maxeqerr) <= pasacom->grad_tol,
       then we terminate with status = PASA_ERROR_TOLERANCE_SATISFIED. */
    if ( PrintLevel >= 1 )
    {
        printf ("maxsignerr: %e maxeqerr: %e\n", maxsignerr, maxeqerr) ;
    }
    E = CGMAX (maxeqerr, maxsignerr) ;
    E = CGMAX (E, pasacom->e) ;
    testtol_old = pasacom->testtol ;
    if ( E < pasacom->E )
    {
        pasacom->E = E ;
        pasacom->testtol = E*Parm->switchfactor ;
        pasacom->testtol = CGMAX (pasacom->testtol, pasacom->grad_tol) ;
    }
    if ( PrintLevel >= 1 )
    {
        printf ("cg error bound E: %e Global error: %e testtol: %e\n",
                 E, pasacom->E, pasacom->testtol) ;
    }
    if ( pasacom->E <= pasacom->grad_tol )
    {
        if ( PrintLevel >= 1 )
        {
            printf ("checktol: A. Error tolerance satisfied\n") ;
        }
        return (PASA_ERROR_TOLERANCE_SATISFIED) ;
    }

    /* TEST B: If pasacom->e <= switchfactor*maxsignerr, then we branch
       to grad_proj.  The rationale is that we wish to determine the active
       constraints at the solution and reduce maxsignerr. */
    if ( pasacom->e <= pasacom->testtol )
    {
        if ( PrintLevel >= 1 )
        {
            printf ("B. Branch to grad_proj\n") ;
        }
        return (PASA_GRAD_PROJ) ;
    }

    /* TEST C: If pasacom->e < switchfactor*maxeqerr and use_penalty is FALSE,
       then we branch to grad_proj.  The rationale is that there is no
       mechanism in CG for reducing the equation error when use_penalty
       is FALSE. On the other hand, grad_proj will project onto the
       feasible set and remove the error associated with constraint violation.*/
    if ( (pasacom->e < switchfactor*maxeqerr) && (use_penalty == FALSE) )
    {
        if ( PrintLevel >= 1 )
        {
            printf ("checktol: C. Branch to grad_proj\n") ;
        }
        return (PASA_GRAD_PROJ) ;
    }

    /* TEST D: If pasacom->e <= switchfactor*maxeqerr and use_penalty is TRUE,
       then we update the multiplier and penalty term, and restart CG.
       The rationale is that we wish to reduce the violation in the
       constraint by utilizing the multiplier structure of the objective.
       The stopping condition is pasacom->e <=
       switchfactor*MAX (maxsignerr, maxeqerr, pasacom->e). */

    /* only perform test D in the middle of CG, not at the start */
    if ( Stat->iter > cgcom->FirstIter )
    {
        if ( (pasacom->e < switchfactor*maxeqerr) && (use_penalty == TRUE) )
        {
            CGINT i, p, q ;
            CGFLOAT c, fp, s, t, *gpen ;
            gpen = cgcom->gpen ;
            c = 0.5*penalty ;
            if ( use_pproj == TRUE )
            {
                fp = CGZERO ;
                pasa_initx (gpen, PASAZERO, pasacom->nf) ;
                i = nrow ;
                while ( (i = RLinkUp [i]) < nrow )
                {
                    t = temp [i] ;
                    /* fp = penalty term in the objective */
                    fp += t*(c*t + lambda [i]) ;
                    s = -(penalty*t + lambda [i]) ;
                    q = ATp [i+1] ;
                    for (p = ATp [i]; p < q; p++)
                    {
                        gpen [ATi [p]] += ATx [p]*s ;/* gradient of penalty */
                    }
                }
            }
            else if ( use_napheap == TRUE )
            {
                fp = residual*(c*residual + Lambda) ;
                s = -(penalty*residual + Lambda) ;
                pasa_scale (gpen, pasacom->nap_a, s, pasacom->nf) ;
            }
            pasacom->fp = fp ;
    
            /* since the penalty term has changed, recompute objective value */
            pasacom->f = pasacom->f_orig + fp ;

            /* if the testtol did not change, then make it smaller */
            if ( testtol_old == pasacom->testtol )
            {
                pasacom->testtol *= Parm->switchfactor ;
            }
    
            if ( PrintLevel >= 1 )
            {
                printf ("checktol: D. Restart CG with tolerance %e\n",
                         pasacom->testtol) ;
            }
            return (CG_RESTART) ;
        }
    }

    /* TEST E: If pasacom->e > switchfactor*maxeqerr, then continue CG.
       The stopping condition is pasacom->e <=
       switchfactor*MAX (maxsignerr, maxeqerr, pasacom->e). */
    if ( PrintLevel >= 1 )
    {
        printf ("checktol: E. Continue CG with new tolerance %e "
                "(old tolerance: %e\n", pasacom->testtol, testtol_old) ;
    }
    return (CG_CONTINUE) ;
}
#endif
