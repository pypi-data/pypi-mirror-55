/* ========================================================================= */
/* === pproj_ssor1 ========================================================= */
/* ========================================================================= */

/*
    Apply SSOR Gauss-Seidel preconditioned conjugate gradients to
    the dual problem. Periodically, we check to see whether a variable
    should be freed or a row should be dropped at the current iterate.
    If the answer is no, then the CG iteration continues. If there is
    a change in the active set, then we perform a line search along the
    direction from the starting CG iterate to the current point.
    As the iterations proceed, we also save up to ssormem of the
    previous CG search directions. After the line search and before
    restarting the CG iteration, we minimize the objective corresponding
    to the new active set over the space spanned by the directions in memory.
    We can efficiently solve this subspace problem since the CG method
    is diagonalizing the Hessian relative to the search directions,
    and we only need to consider the effect of the rank-1 changes to
    the Hessian associated with the freeing of variables and the rank-2
    changes to the Hessian associated with the dropping of rows.

    The difference between ssor0 and ssor1 is that the goal in ssor0
    is to free as many variables and drop as many rows as possible by
    performing a gradient ascent iteration. In ssor1, we try to solve
    the dasa subproblems more accurately by performing an SSOR
    Gauss-Seidel preconditioned conjugate gradient iteration. A few
    iterations of the CG algorithm generates an approximation to the
    solution to the linear system solved in dasa using a Cholesky
    factorization.  The routine pproj_iterquery uses the number of nnz's in
    the Cholesky factor and the number of nnz's in the reduced A matrix
    to determine how many ssor iterations should be performed.
    The ssor and coordinate ascent routines can be turned on or off
    using the parameters Parm->coorquery, Parm->ssor0query, and
    Parm->ssor1query.

    Consider an optimization problem of the form
 
    max -.5x'Qx + b'x

    The SSOR Gauss-Seidel preconditioner P =  inv (S)' inv (S),
    where S = (D+L) inv (sqrt(D)) and L+D+L' = Q, was introduced
    in the preconditioned gradient ascent code ssor0. The corresponding
    SSOR preconditioned conjugate gradient iteration is the following:

    beta_0 = 0, alpha_0 = 0, g_0 = b - Qx_0, d_0 = Pg_0

    for k = 0, 1, 2, ...

        x_k+1 = x_k + alpha_k d_k,   alpha_k = g_k'd_k/(d_k'Qd_k)

        g_k+1 = g_k - alpha_k Qd_k,

        d_k+1 = Pg_k+1 + beta_k d_k, beta_k = gk+1' P gk+1 / (gk' P gk)

    end

    Here we are using the Fletcher-Reeves formula, and the gradients are
    updated in each iteration for stability, as explained in [1].
    Note that g_k'Pg_k and g_k'd_k are equal, so we only need to compute
    one of them.

    According to the theory for the conjugate gradient method, the
    directions d0, ... , dk are Q conjugate. Hence, we have

    [d0 | d1 | ... | dk]'Q[d0 | d1 | ... | dk] =

        diag([d0'Qd0, d1'Qd1, ... , dk'Qdk])

    As the CG iteration proceeds, we save the ssormem most recent d_k.
    When we reach an iterate where there is a change in the active set
    (either a variable frees or a row drops), we maximize the dual function
    along the line segment [lambda0, lambdak]. If lambda_bar is the optimum,
    then we maximize the dual function over lambda_bar plus the linear
    space spanned by [dj, ... dk], the directions stored in the limited
    memory. The effect to the new free variables and the new dropped rows
    is to add to the current Hessian Q the sum of say m rank-1 matrices
    r_i r_i', 1 <= i <= m. The quadratic for this limited memory
    optimization problem is

    [dj | ... | dk] (Q + sum_{i=1}^m r_i r_i') [dj | ... | dk] =

    diag([dj'Qdj, ... , dk'Qdk]) + sum_{i=1}^m v_i v_i' where

    v_i' =   r_i' [dj | ... | dk]. Hence, the effect of the change in
    the active set is to perturb the diagonal matrix by the sum of m
    rank-1 matrices. We can either form this "ssormem by ssormem" matrix
    and Cholesky factor it, or we can update its factorization, starting from
    the diagonal matrix.

    If we directly implemented the preconditioned CG algorithm as
    described above, each iteration requires 5 multiplications between
    A_F and a vector. By reorganizing the computations, this cost can
    be reduced to 4 multiplications. We introduce the following new
    variables:

    pk = inv (D+L) Q dk
    qk = inv (D+L) gk
    sk = (D+L)' dk

    Observe that

    pk = inv (D+L) (D + L + L') dk
       = inv (D+L) (D + L + L') inv (D+L)' sk
       = inv (D+L) (I + L inv (D+L)') sk
       = inv (D+L) (sk + L dk)

    Also note that the numerator of alpha_k satisfies the following relations:

    gk' dk = qk' sk = gk' P gk = qk' D qk

    In terms of the new variables, the preconditioned CG iteration
    can be expressed as follows:

    q_0 = inv (D+L) g0

    s0 = D q0

    d0 = inv (D+L)' s0

    x1 = x0 + alpha_0 d0,   alpha_0 = q0' D q0/(d0' Q d0)

    for k = 0, 1, 2, ...

        pk = inv (D+L) (sk + Ldk)

        qk+1 = qk - alpha_k pk,       alpha_k = (qk' D qk)/(dk' Q dk)

        sk+1 = D qk+1 + beta_k sk,    beta_k = (qk+1' D qk+1) / (qk' D qk)
 
        dk+1 = inv (D+L)' sk+1

        xk+2 = xk+1 + alpha_k+1 dk+1, alpha_k+1 = (qk+1' D qk+1) /(dk+1' Q dk+1)

    end

    Comparing the new structure to the old, note that computation of x1
    was moved to the initialization step, and then in the loop, the computation
    of x is moved to the end of the loop. With this organization, at the
    end of each iteration, we have both a new direction vector and the new x
    associated with the new direction.  If Q = A * A', then A'*dk can
    be computed at the same time that dk = inv (D+L)' sk is evaluated. There
    are two multiplies when dk+1 is evaluated and two when we solve for pk.

    In the first part of the code, we perform the ssor iterations and
    save up to ssormem of the search directions. In these iterations,
    we do not take into account any changes in the dual function associated
    with the freeing of variables or the dropping of row. These iterations
    generate a search direction, and we optimize along the search direction
    while taking into account the freeing of variables and dropping of rows,
    the same as in pproj_dasa and pproj_ssor0. If there is a change in
    constraint activity, then we reoptimize the dual function over the
    manifold associated with the ssormem search directions. Update and
    downdate techniques are used to take into account the change in the
    Hessian associated with the change in constraint activity. This
    leads to a new search direction and a new line search. This process
    continues until there is no change in constraint activity.

    [1] William W. Hager and Hongchao Zhang, The Limited Memory Conjugate
        Gradient Method, SIAM Journal on Optimization, 23 (2013), pp. 2150-2168. 
Flow structure:
break 0: all rows dropped, go to final exit
break 1: fd = 0 in CG startup, max achieved, go to final exit
break 2: dual maximized, go to final exit
break 3: fd <= 0 or sd = 0 in subit, go to line search
break 4: fd <  0 or sd = 0 in break point calc, will either exit with error 
         if nlinesearch = 1, return to dasa if nlinesearch = 1 and
         it - it0 >= ssor1_its, or restart CG without updating lambda, b, and c
break 5: no constraints in the search interval, take step st and update 
         lambda, b, and c, continue cg if error tolerance not satisfied
break 6: line search termination due to new break point > st0 update
         lambda, b, c with step st, reset ns, go to subspace minimization
break 7: line search terminated with zero slope, update lambda, b, c with 
         step st, reset ns, go to subspace minimization
break 8: sd <= 0 in line search, treat same as break 6
break 9:  fd <= 0 after row delete, set lineflag = 1, fd = 0, same as break 6
break 10: before subspace minimization, check if all rows have dropped,
          if so then go to final exit
break 11: all rows have dropped, go to final exit
break 12: to many iterations, go to final exit
break 14: the number of iteration since last restart of CG exceeds
          ssor1_its without change in constraint activity
break 15: solution found, final exit
break 16: relaxed dual maximized, final exit
*/

#include "pproj.h"

int pproj_ssor1 /* returned error status:
                       PPROJ_SOLUTION_FOUND
                       PPROJ_SSOR_NONASCENT
                       PPROJ_SSOR_MAX_ITS

                    flow control:
                       PPROJ_STATUS_OK (relaxed dual was maximized)
                       PPROJ_ALL_ROWS_DROPPED
                       PPROJ_SWITCH_TO_UPDOWN */
(
    PPcom *I
)
{
    int     blk, dstatus, flag, lineflag, ibj, ssormem,
            sub_it, sub_inc, status, memp, n, n1, n2, nlinesearch, *ib ;
    PPINT   active_rows, it, it0, i, j, k, first, last, nup, chg,
            l, m, p, p1, q, q1, col, row, nbrk, nb, nf, nf0,
            nrowdel, nrowadd, ncoladd, ncoldel, rowp, nr, sing,
           *AFTi, *AFTnz, *AFTp,
           *Heap, *F, *bound, *rowlist, *RLinkDn, *RLinkUp,
           *uLinkUp, *uLinkDn, *lLinkUp, *lLinkDn, *lstart, *ustart,
           *RowmodFlag, *RowmodList, *ColmodFlag, *ColmodList,
           *ir, *ns, *worki ;

    PPFLOAT Br, ax, cj, alpha, beta, beta_denom, errdual, errls,
            s, t, u, y, z, st, st0, fd, fn, sd, tic, dknew, snew,
           *AFTx, *b, *c, *lambda, *shift_l,
           *Br_value, *D, *L, *Lj, *Lk, *diag, *e, *v, *w,
           *dk, *dk_start, *dl, *pk, *qk, *sk, *pA, *gk, *workd ;

    PPprob *Prob ;
    PPparm *Parm ;
    PPstat *Stat ;
    PPwork    *W ;

    tic = pproj_timer () ;

#ifndef NDEBUG
    char   *where ;
    I->Check->location = 4 ; /* code operates in ssor1 */
#endif

    /* extract the problem, statistics, and work structures from I */
    Prob = I->Prob ;
    Parm = I->Parm ;
    Stat = I->Stat ;
    W = I->Work ;

    int const PrintLevel = Parm->PrintLevel ;
    if ( PrintLevel >= 2 )
    {
        printf ("start ssor1\n") ;
    }

    const int loExists = I->Work->loExists ;
    const int hiExists = I->Work->hiExists ;

    /* Problem data */
    PPINT   const         *Ap = Prob->Ap ;
    PPINT   const         *Ai = Prob->Ai ;
    PPFLOAT const         *Ax = Prob->Ax ;
    PPFLOAT const      *singc = Prob->singc ;
    PPINT   const        ncol = Prob->ncol ;
    PPINT   const        nrow = Prob->nrow ;
    PPINT   const          ni = Prob->ni ;
    PPINT   const       nsing = Prob->nsing ;
    PPINT   const    nsingni  = nsing + ni ;
    PPINT   const    nsingni1 = nsingni + 1 ;
    PPINT   const    nsingni2 = nsingni + 2 ;
    PPINT   const        ntot = nsingni1 + ncol ;
    PPINT                *slo = W->slo ;
    PPINT                *shi = W->shi ;
    PPINT   const   *ineq_row = Prob->ineq_row ;
    PPFLOAT const         *bl = (nsing) ? Prob->singlo : Prob->bl ;
    PPFLOAT const         *bu = (nsing) ? Prob->singhi : Prob->bu ;
    int     const *sol_to_blk = W->sol_to_blk ;
    PPFLOAT const       sigma = W->sigma ;
    PPFLOAT const    grad_tol = Parm->grad_tol ;

    /* Transpose of A */
    PPINT   const *ATp = W->ATp ;
    PPINT   const *ATi = W->ATi ;
    PPFLOAT const *ATx = W->ATx ;

    /* Transpose of AF */
    AFTp = W->AFTp ;
    AFTnz = W->AFTnz ;
    AFTi = W->AFTi ;
    AFTx = W->AFTx ;

    /* Links point to active rows */
    RLinkUp = W->RLinkUp ;
    RLinkDn = W->RLinkDn ;

    /* Links point to active singletons. lLinkUp points to the strict
       inequalities with b_i = bl_i while uLinkUp points to the strict
       inequalities with b_i = bu_i. Since only one of these can hold for
       each i, lLinkUp and uLinkUp can be stored in the same array */
    lLinkUp = W->SLinkUp ; 
    lLinkDn = W->SLinkDn ;
    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;

    /* working arrays */
    lambda  = W->lambda ;
    shift_l = W->shift_l ;
    ib      = W->ib ;
    ir      = W->ir ;
    b       = W->b ; /* the part of grad L associated with bound variables */
    c       = W->c ; /* y + A'lambda */
    F       = W->F ;
    D       = W->D ;
    ns      = W->ns ;

    ssormem = W->ssormem ;

    nf      = W->nf ;
    nrowdel = W->nrowdel ;
    nrowadd = W->nrowadd ;
    ncoladd = W->ncoladd ;
    ncoldel = W->ncoldel ;
    RowmodFlag = W->RowmodFlag ;
    RowmodList = W->RowmodList ;
    ColmodFlag = W->ColmodFlag ;
    ColmodList = W->ColmodList ;

    lstart = W->lstart ;
    ustart = W->ustart ;

    /* ======== start allocations ========
    -> work arrays in ssor step:

       Heap     - INT    ntot, line search
       bound    - INT    ncol, line search
       rowlist  - INT    nrow, active rows associated with update
       pA       - double ncol, A'lambda
       Br_value - double ntot, line search
       gk       - double nrow, starting gradient in CG iteration
       pk       - double nrow, used in CG iteration = inv (D+L) Q dk
       qk       - double nrow, used in CG iteration = inv (D+L) gk
       sk       - double nrow, used in CG iteration = (D+L)' dk
       dk       - double nrow, search direction in a CG iteration (ssor memory)
       dl       - double nrow, search direction from initial CG iterate
       L        - double ssormem*(ssormem-1)/2, Cholesky factor below diagonal
       diag     - double ssormem, diagonal of Cholesky factory
       e        - double ssormem, used in updates
       v        - double ssormem, used in updates
       w        - double ssormem, used in updates */

    worki = W->arrayi ;
    Heap    = worki ; worki += ntot ;
    bound   = worki ; worki += ncol ;
    rowlist = worki ; worki += nrow ;

    workd = W->arrayd ;
    pA       = workd ; workd += ncol ;
    Br_value = workd ; workd += ntot ;
    gk       = workd ; workd += nrow ;
    pk       = workd ; workd += nrow ;
    qk       = workd ; workd += nrow ;
    sk       = workd ; workd += nrow ;
    dk_start = workd ; workd += ssormem*nrow ;
    dl       = workd ; workd += nrow ;
    L        = workd ; workd += (ssormem*(ssormem-1))/2 ;
    diag     = workd ; workd += ssormem ;
    e        = workd ; workd += ssormem ;
    v        = workd ; workd += ssormem ;
    w        = workd ; workd += ssormem ;
    /* ======== end of allocations ======== */

    nb = 0 ;
    /* all bound indices are stored in bound array */
    for (j = 0; j < ncol; j++)
    {
        if ( ib [j] )
        {
            bound [nb] = j ;
            nb++ ;
        }
    }
    it = 0 ;
    chg = 0 ;  /* count the number of variables freed and rows dropped */
    flag = -1 ; /* restart CG iteration */

#ifndef NDEBUG
    where = "at very start of ssor1" ;
    pproj_checkF (I, where) ;
    pproj_checkc (I, where) ;
    Heap [ntot-1] = EMPTY ;
    pproj_checkb (I, where) ;
    pproj_check_const (NULL, 0, ns, EMPTY, ntot, where) ;
    pproj_checkD (I, where) ;
    pproj_check_AT (I, where) ;
    pproj_check_AFT (I, TRUE, where) ;
    pproj_check_link (I, (int *) NULL, 0, where) ;
    pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
#endif

    /* status will be reset during the iteration below */
    status =  PPROJ_TOLERANCE_NOT_MET ;
    while ( 1 )
    {
#ifndef NDEBUG
        if ( it > 0 )
        {
            if ( flag < 0 )
            {
                for (i = first; i < nrow; i = RLinkUp [i])
                {
                    dl [i] = PPZERO ;
                }
            }
            pproj_check_dual (I, dl, "start of CG iteration", TRUE, TRUE) ;
        }
        else
        {
            pproj_initx (dl, PPZERO, nrow) ;
        }
#endif
        if ( flag < 0 ) /* restart CG iteration */
        {
           if ( PrintLevel > 2 )
           {
               printf ("restart CG in ssor1\n") ;
           }
            /* record the starting iteration */
            it0 = it ;
            it++ ;
            /* number of CG iterations before checking for active constraints */
            sub_inc = 2 ;
            first = RLinkUp [nrow] ;
            if ( first == nrow ) /* all equations have dropped */
            {
                if ( PrintLevel > 2 ) printf ("break 0\n") ;
                status =  PPROJ_ALL_ROWS_DROPPED ;
                break ;
            }
            /* b = part of grad L (lambda) associated with bound variables
                   (includes proximal term -sigma*lambda)
               gk = grad L_R (lambda) for active rows */

            /* compute objective gradient at the current iterate */
            for (i = first; i < nrow; i = RLinkUp [i])
            {
                t = b [i] ; /* includes -sigma*lambda [i] */
                ASSERT (ir [i] <= nsingni) ;
                p = AFTp [i] ;
                q = p + AFTnz [i] ;
                for (; p < q; p++)
                {
                    t -= AFTx [p]*c [AFTi [p]] ;
                }
                gk [i] = t ;
            }

            /* compute q0 = inv (D+L) * g0,  s0 = D * q0, and
                       alpha_num = q0'Dq0.  (initializations above) */

            pproj_initFx (pA, PPZERO, F, nf) ; /* set pA [F [k]] = 0 */

            i = first ;
            s = gk [i] ;
            sk [i] = s ;
            t = s/D [i] ;
            fd = s*t ; /* = q0' * D * q0 = d0'g0 = s0*q0 */
            qk [i] = t ;

            /* compute s0, q0, and fd */
            last = RLinkDn [nrow] ;
            while (i < last)
            {

                ASSERT (ir [i] <= nsingni) ;

                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    pA [AFTi [p]] += AFTx [p]*t ;
                }

                i = RLinkUp [i] ;

                ASSERT (ir [i] <= nsingni) ;

                t = PPZERO ;

                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    t += AFTx [p]*pA [AFTi [p]] ;
                }
                s = gk [i] - t ;
                sk [i] = s ;
                t = s/D [i] ;
                fd += s*t ;
                qk [i] = t ;
            }

            if ( fd == PPZERO ) /* gradient vanishes at current iterate */
            {
                status = PPROJ_STATUS_OK ; /* relaxed dual maximized */
                if ( PrintLevel > 2 ) printf ("break 1\n") ;
                break ;
            }

            dk = dk_start ;
            memp = 0 ; /* pointer to current memory location */

            /* compute d0 = inv (D+L)' * s0, pA = A_F' * d0, and sd = q0 D q0 */
            pproj_initFx (pA, PPZERO, F, nf) ; /* set pA [F [k]] = 0 */
            sd = t*t ; /* sd initially stores d'd */
            dk [i] = t ;

            while ( i > first )
            {
                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1 ; p++)
                {
                    pA [AFTi [p]] += AFTx [p]*t ;
                }

                i = RLinkDn [i] ;

                ASSERT (ir [i] <= nsingni) ;

                t = PPZERO ;

                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    t += AFTx [p]*pA [AFTi [p]] ;
                }
                t = (sk [i] - t)/D [i] ;
                dk [i] = t ;
                sd += t*t ;
            }

            p = AFTp [i] ;
            p1 = p + AFTnz [i] ;
            for (; p < p1; p++)
            {
                pA [AFTi [p]] += AFTx [p]*t ;
            }
            /* end computation of dk and pA = A'*dk */

            sd *= sigma ; /* sd stored sigma * dk' * dk */
            for (k = 0; k < nf; k++)
            {
                j = F [k] ;
                sd += pA [j]*pA [j] ; /* sd stores  dk'(AF*AF' + sigma I)dk */
            }
            if ( sd == PPZERO ) /* gradient vanishes at current iterate */
            {
                status = PPROJ_STATUS_OK ; /* relaxed dual maximized */
                if ( PrintLevel > 2 ) printf ("break 2\n") ;
                break ;
            }

            /* numerator of alpha is denominator of beta */
            beta_denom = fd ;
            alpha = fd/sd ;
            diag [memp] = sd ;
            /* dl stores the total movement from the initial iterate */
            for (i = first; i < nrow; i = RLinkUp [i])
            {
                dl [i] = alpha*dk [i] ;
            }
        } /* CG startup complete */
        flag = 0 ;

        /* perform CG iterations */
        if ( PrintLevel > 2 )
        {
            printf ("perform %i cg iterations\n", sub_inc) ;
        }
        for (sub_it = 0; sub_it < sub_inc; sub_it++)
        {
            /* evaluate pk, qk, and fd = numerator of next beta
                                       = numerator of next alpha */
            pproj_initFx (pA, PPZERO, F, nf) ; /* set pA [F [k]] = 0 */
            i = first ;
            s = sk [i]/ D [i] ;
            pk [i] = s ;
            t = dk [i] - s ;
            s = qk [i] - alpha*s ;
            qk [i] = s ;
            fd = s*s*D [i] ;
            while (i < last)
            {
                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    pA [AFTi [p]] += AFTx [p]*t ;
                }

                i = RLinkUp [i] ;

                t = PPZERO ;
                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    t += AFTx [p]*pA [AFTi [p]] ;
                }
                t = (sk [i] + t)/D [i] ;
                pk [i] = t ;
                s = qk [i] - alpha*t ;
                qk [i] = s ;
                fd += s*s*D [i] ;
                t = dk [i] - t ;
            }
            if ( fd > PPZERO )
            {
                beta = fd/beta_denom ;
                beta_denom = fd ;        /* fd = denominator of next beta */

                memp++ ;
                if ( memp == ssormem )
                {
                    memp = 0 ;
                    dk = dk_start ;
                }
                else
                {
                    dk = dk_start+(memp*nrow) ;
                }

                /* evaluate sk, dk, and sd */
                pproj_initFx (pA, PPZERO, F, nf) ; /* set pA [F [k]] = 0 */
                t = D [i]*qk [i] + beta*sk [i] ; /* = new sk [i] */
                sk [i] = t ;
                t /= D [i] ;
                sd = t*t ;  /* sd stores dk' * dk */
                dk [i] = t ;
                while (i > first)
                {
                    p = AFTp [i] ;
                    p1 = p + AFTnz [i] ;
                    for (; p < p1; p++)
                    {
                        pA [AFTi [p]] += AFTx [p]*t ;
                    }
                    i = RLinkDn [i] ;

                    t = PPZERO ;
                    p = AFTp [i] ;
                    p1 = p + AFTnz [i] ;
                    for (; p < p1; p++)
                    {
                        t += AFTx [p]*pA [AFTi [p]] ;
                    }
                    s = D [i]*qk [i] + beta*sk [i] ;
                    sk [i] = s ;
                    t = (s - t)/D [i] ;
                    dk [i] = t ;
                    sd += t*t ;
                }

                p = AFTp [i] ;
                p1 = p + AFTnz [i] ;
                for (; p < p1; p++)
                {
                    pA [AFTi [p]] += AFTx [p]*t ;
                }

                sd *= sigma ; /* sd stored sigma * dk' * dk */
                for (k = 0; k < nf; k++)
                {
                    j = F [k] ;
                    sd += pA [j]*pA [j] ; /* sd = dk'(AF*AF' + sigma I)dk */
                }
            }
            /* If gradient vanishes at current iterate, then the relaxed
               dual has been maximized at the current iterate. Must do line
               search since rows could drop or columns could become free
               as we move along the search direction. */
            if ( (fd <= PPZERO) || (sd == PPZERO) )
            {
                memp-- ;
                if ( memp < 0 )
                {
                    memp = ssormem - 1 ;
                }
                status = PPROJ_DO_LINE_SEARCH ;
                if ( PrintLevel > 2 ) printf ("break 3\n") ;
                break ;
            }
            diag [memp] = sd ;
            alpha = fd/sd ;
            /* dl stores the total movement from the initial iterate */
            for (i = first; i < nrow; i = RLinkUp [i])
            {
                dl [i] += alpha*dk [i] ;
            }
        }
        it += sub_it ;

        nlinesearch = 0 ;
        /* Minimize over the directions in memory until no change in the
           active constraints. If in the first iteration there is no
           change in the active constraints, then continue the CG iteration.
           If there is a change in the active constraints, then we continue
           to minimize over the search directions in memory until there is
           no change in the active constraints. */
        while ( 1 )
        {
            nlinesearch++ ;
            if ( PrintLevel > 2 )
            {
                printf ("ssor1 line search %i\n", nlinesearch) ;
            }
            pproj_initx (pA, PPZERO, ncol) ;
            fd = PPZERO ;
            sd = PPZERO ;

            for (i = first; i < nrow; i = RLinkUp [i])
            {
                t = dl [i] ;
                q = ATp [i+1] ;
                for (p = ATp [i] ; p < q ; p++)
                {
                    pA [ATi [p]] += t*ATx [p] ;
                }
                fd += t*gk [i] ;
                sd += t*t ;
            }
            sd *= sigma ;
            for (k = 0; k < nf; k++)
            {
                sd += pA [F [k]]*pA [F [k]] ;
            }
            if ( PrintLevel > 2 )
            {
                printf ("fd: %e sd: %e\n", fd, sd) ;
            }
            /* If the derivative from the current point in the cg search
               direction is negative, then dual has been maximized at the
               current iterate. */
            if ( (sd == PPZERO) || (fd <= PPZERO) )
            {
                status = PPROJ_STATUS_OK ; /* relaxed dual maximized */
                if ( PrintLevel > 2 ) printf ("break 4\n") ;
                break ;
            }
            nbrk = 0 ;
            nup = 0 ; /* number of updates */
            st0 = st = fd/sd ;
            for (k = 0; k < nb; k++)
            {
                j = bound [k] ;
                if ( (ibj = ib [j]) < 0 )
                {
                    if ( pA [j] > PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < st )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;        /* add to heap  */
                        }
                    }
                }
                else if ( ibj > 0 )
                {
                    if ( pA [j] < PPZERO )
                    {
                        s = -c [j]/pA [j] ;
                        if ( s < st )
                        {
                            Br_value [j] = s ;
                            nbrk++ ;
                            Heap [nbrk] = j ;        /* add to heap */
                        }
                    }
                }
            }

            if ( W->shiftl_is_zero )
            {
                for (j = lLinkUp [nsingni1]; j <= nsingni; j = lLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) < PPZERO )
                    {
                        /* lambda > 0 for lLinkUp */
                        if ( ni ) s = -lambda [row]/t ;
                        else      s = (singc [j] - lambda [row])/t ;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
                for (j = uLinkUp [nsingni2]; j <= nsingni; j = uLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) > PPZERO )
                    {
                        /* lambda < 0 for uLinkUp */
                        if ( ni ) s = -lambda [row]/t ;
                        else      s = (singc [j] - lambda [row])/t ;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
            }
            else /* shift_l != 0 */
            {
                for (j = lLinkUp [nsingni1]; j <= nsingni; j = lLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) < PPZERO )
                    {
                        /* lambda > 0 for lLinkUp */
                        if ( ni ) s = -(lambda [row]+shift_l [row])/t ;
                        else      s = (singc[j]-(lambda [row]+shift_l [row]))/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
                for (j = uLinkUp [nsingni2]; j <= nsingni; j = uLinkUp [j])
                {
                    row = ineq_row [j] ;
                    if ( (t = dl [row]) > PPZERO )
                    {
                        /* lambda < 0 for uLinkUp */
                        if ( ni ) s = -(lambda [row]+shift_l [row])/t ;
                        else      s = (singc[j]-(lambda [row]+shift_l [row]))/t;
                        if ( s < st )
                        {
                            k = j + ncol ;
                            Br_value [k] = s ;
                            nbrk++ ;
                            Heap [nbrk] = k ; /* add to heap  */
                        }
                    }
                }
            }

            /* If no constraints activated, then return to the CG iteration
               after taking the step. */
            if ( nbrk == 0 )
            {
                if ( PrintLevel > 2 ) printf ("break 5\n") ;
                break ;
            }

            /* ============================================================== */
            /* sort break points, do a line search */
            /* ============================================================== */

            pproj_minheap_build (Heap, Br_value, nbrk) ;
            for (k = 1; k <= nbrk; k++)
            {
                ns [Heap [k]] = k ;
            }

#ifndef NDEBUG
            pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                "build Heap, ssor1") ;
#endif

            lineflag = 0 ;
            nf0 = nf ;
            rowp = ntot ;
            st = PPZERO ;
            while ( nbrk > 0 )
            {
                if ( sd > PPZERO )
                {
                    col = Heap [1] ;
                    Br = PPMAX (Br_value [col], PPZERO) ;
                    /* If current break point is beyond the stepsize st0
                       for which we extracted break points, then terminate,
                       either at the global minimum in the search direction,
                       or at st0. */
                    if ( Br >= st0 )
                    {
                        Br = st + fd/sd ;
                        if ( Br < st0 )
                        {
                            st = Br ; 
                        }
                        else
                        {
                            st = st0 ;
                            /* lineflag = -2 means that in the debugger,
                               we should only check that slope >= 0 */
                            lineflag = -2 ;
                        }
                        fd = PPZERO ;
                        if ( PrintLevel > 2 ) printf ("break 6\n") ;
                        break ;
                    }
                    pproj_minheap_delete (Heap, ns, Br_value, &nbrk, 1) ;
                    fn = fd - sd * (Br - st) ;

#ifndef NDEBUG
                    pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                            "Heap delete, ssor1") ;
                    if ( PrintLevel > 2 )
                    {
                        PRINTF("    brk: %ld col: %ld fn: %9.3e fd: %9.3e"
                               " sd: %9.3e st: %9.3e Br_value: %9.3e\n",
                               (LONG) nbrk, (LONG) col, fn, fd, sd, st, Br) ;
                    }
#endif

                    if ( fn <= PPZERO )
                    {
                        ASSERT (nup > 0) ;
                        if ( fd != fn )
                        {
                            st += (fd/(fd-fn))*(Br - st);
                        }
                        fd = PPZERO ;
                        if ( PrintLevel > 2 ) printf ("break 7\n") ;
                        break ; /* line search complete */
                    }
                    else
                    {
                        fd = fn ;
                    }
                    nup++ ;
                }
                else /* sd <= 0 */
                {
                    if ( PrintLevel > 2 ) printf ("break 8\n") ;
                    break ; /* do not try to make the step any bigger */
                }

                st = Br ;

                if ( col < ncol ) /* free column */
                {
                    F [nf++] = col ;
                    s = pA [col] ;
                    sd += s*s ;
                    ib [col] = 0 ;
                    k = ColmodFlag [col] ;
                    if ( k != EMPTY )
                    {
                        l = ColmodList [ncol-ncoldel] ;
                        ColmodList [k] = l ;
                        ColmodFlag [l] = k ;
                        ColmodFlag [col] = EMPTY ;
                        ncoldel-- ;
                    }
                    else
                    {
                        ColmodList [ncoladd] = col ;
                        ColmodFlag [col] = ncoladd ;
                        ncoladd++ ;
                    }
                    q = Ap [col+1] ;
                    for (p = Ap [col]; p < q; p++)
                    {
                        i = Ai [p] ;
                        if ( ir [i] <= nsingni )
                        {
                            ax = Ax [p] ;
                            D [i] += ax*ax ;
                            l = AFTp [i] + AFTnz [i]++ ;
                            AFTx [l] = ax ;
                            AFTi [l] = col ;
                        }
                    }
                }
                else              /* drop row */
                {
                    Stat->ssor1_drop++ ;
                    sing = col - ncol ;
                    /* save singleton in unused part of heap */
                    Heap [--rowp] = sing ;
                    row = ineq_row [sing] ;

#ifndef NDEBUG
                    if ( PrintLevel > 2 )
                    {
                        PRINTF("    jsing: %ld row: %ld ir: %ld\n",
                               (LONG) (col - ncol), (LONG) row,
                               (LONG) ir [row]) ;
                    }
                    if ( ir [row] > nsingni )
                    {
                        PRINTF ("row: %ld ir: %ld was already deleted "
                                "in ssor1\n", (LONG) row, (LONG) ir [row]) ;
                        pproj_error (-1, __FILE__, __LINE__, "stop") ;
                    }
#endif
                    ASSERT ((ir [row] != 0) && (ir [row] <= nsingni)) ;
                    /* set ir [row] = nsingni+sing after updates, keep
                       track of nonzeros in row until after the update
                       associated with rank 1 changes to the matrix */
                    i = RLinkDn [row] ;
                    k = RLinkUp [row] ;
                    RLinkUp [i] = k ;
                    RLinkDn [k] = i ;

                    k = RowmodFlag [row] ;
                    if ( k != EMPTY ) /* row set to be added, remove it */
                    {
                        AFTnz [row] = 0 ;
                        /* move last added row to replace new dropped row */
                        l = RowmodList [nrow-nrowadd] ;
                        RowmodList [k] = l ;
                        RowmodFlag [l] = k ;
                        RowmodFlag [row] = EMPTY ;
                        nrowadd-- ; /* one less row to add */
                    }
                    else /* add row to the delete list */
                    {
                        RowmodList [nrowdel] = row ;
                        RowmodFlag [row] = nrowdel ;
                        nrowdel++ ;
                    }

                    if ( W->shiftl_is_zero )
                    {
                        if ( ni )
                        {
                            dknew = -lambda [row] ;
                            lambda [row] = PPZERO ;
                        }
                        else /* nsing */
                        {
                            dknew = singc [sing] - lambda [row] ;
                            lambda [row] = singc [sing] ;
                        }
                    }
                    else
                    {
                        if ( ni )
                        {
                            dknew = -(lambda [row]+shift_l [row]) ;
                            lambda [row] = -shift_l [row] ;
                        }
                        else /* nsing */
                        {
                            t = singc [sing] - shift_l [row] ;
                            dknew = t - lambda [row] ;
                            lambda [row] = t ;
                        }
                    }

                    b [row] -= sigma*dknew ;
                    PPFLOAT const dk_row = dl [row] ;
                    /* fd += dk_row*(Dsigma*dknew-b [row]) ;*/
                    fd -= dk_row*b [row] ;
                    sd -= sigma*dk_row*dk_row ;
                    if ( dk_row > PPZERO ) /* drop upper bound bu */
                    {
                        b [row] -= bu [sing] ;
                        m = uLinkUp [sing] ;
                        l = uLinkDn [sing] ;
                        uLinkUp [l] = m ;
                        uLinkDn [m] = l ;
                        if ( Parm->cholmod == TRUE )
                        {
                            blk = sol_to_blk [sing] ;
                            if ( sing == ustart [blk] )
                            {
                                ustart [blk] = m ;
                            }
                        }
                        if ( nsing )
                        {
                            shi [row] = 0 ;
                            j = slo [row] ;
                            if ( j )
                            {
                                m = lLinkUp [j] ;
                                l = lLinkDn [j] ;
                                lLinkUp [l] = m ;
                                lLinkDn [m] = l ;
                                slo [row] = 0 ;
                                if ( j == lstart [blk] )
                                {   
                                    lstart [blk] = m ;
                                }
                            }
                        }
                    }
                    else /* drop lower bound bl */
                    {
                        b [row] -= bl [sing] ;
                        m = lLinkUp [sing] ;
                        l = lLinkDn [sing] ;
                        lLinkUp [l] = m ;
                        lLinkDn [m] = l ;
                        if ( Parm->cholmod == TRUE )
                        {
                            blk = sol_to_blk [sing] ;
                            if ( sing == lstart [blk] )
                            {
                                lstart [blk] = m ;
                            }
                        }
                        if ( nsing )
                        {
                            slo [row] = 0 ;
                            j = shi [row] ;
                            if ( j )
                            {
                                m = uLinkUp [j] ;
                                l = uLinkDn [j] ;
                                uLinkUp [l] = m ;
                                uLinkDn [m] = l ;
                                shi [row] = 0 ;
                                if ( Parm->cholmod == TRUE )
                                {
                                    if ( j == ustart [blk] )
                                    {
                                        ustart [blk] = m ;
                                    }
                                }
                            }
                        }
                    }

                    q = ATp [row+1] ;
                    for (p = ATp [row] ; p < q ; p++)
                    {
                        j = ATi [p] ;
                        ax = ATx [p] ;
                        s = pA [j] ;
                        /* cj = c after taking the step */
                        cj = c [j] + st*s ;
                        /* modify c to account for later update */
                        c [j] += dknew*ax ;

                        t = dk_row*ax ;
                        snew = pA [j] = s - t ;
                        /* update c, pA, sd, fd */
                        if ( !ib [j] )
                        {
                            fd += cj*t ;
                            sd -= t*(s + snew) ;
                        }
                        else
                        {
                            if ( ib [j] < 0 )
                            {
                                if ( snew > PPZERO )
                                {
                                    Br_value [j] = st - cj/snew ;
                                    if ( ns [j] != EMPTY )
                                    {
                                        pproj_minheap_update (Heap,
                                           ns, Br_value, nbrk, ns [j]) ;
                                    }
                                    else
                                    {
                                       pproj_minheap_add (j, Heap,
                                           ns, Br_value, &nbrk) ;
                                    }
                                }
                                else
                                {
                                    if ( ns [j] != EMPTY )
                                    {
                                        pproj_minheap_delete (Heap,
                                           ns, Br_value, &nbrk, ns [j]);
                                    }
                                }
                            }
                            else
                            {
                                if ( snew < PPZERO )
                                {
                                    Br_value [j] = st - cj/snew ;
                                    if ( ns [j] != EMPTY )
                                    {
                                        pproj_minheap_update (Heap,
                                           ns, Br_value, nbrk, ns [j]) ;
                                    }
                                    else
                                    {
                                        pproj_minheap_add (j, Heap,
                                            ns, Br_value, &nbrk) ;
                                    }
                                }
                                else
                                {
                                    if ( ns [j] != EMPTY )
                                    {
                                        pproj_minheap_delete (Heap,
                                           ns, Br_value, &nbrk, ns [j]);
                                    }
                                }
                            }
                        }
                    }
                }

#ifndef NDEBUG
                if ( PrintLevel > 2 )
                {
                    if ( col < ncol ) PRINTF ("    free: %ld\n", (LONG) col);
                    else
                    {
                        PRINTF ("    drop row: %ld\n", (LONG) row) ;
                    }
                }
                if ( col >= ncol )
                {
                    dl [row] = PPZERO ;
                }
                pproj_check_minheap (Heap, Br_value, ns, nbrk, ntot,
                                    "line search of ssor1") ;
#endif
                /* check if line search complete due to slope change at
                   a break point associated with a dropped row */
                if ( fd <= PPZERO )
                {

#ifndef NDEBUG
                    if ( PrintLevel > 2 )
                    {
                        PRINTF("    premature break from line search: %e\n",fd);
                    }
#endif

                    lineflag = 1 ;
                    fd = PPZERO ;
                    if ( PrintLevel > 2 ) printf ("break 9\n") ;
                    break ;
                }
            }
            if ( sd > PPZERO )
            {
                st += fd/sd ;
            }
            if ( st > st0 )
            {
                st = st0 ;
                lineflag = -1 ;
            }

            for (k = 1; k <= nbrk; k++)
            {
                ns [Heap [k]] = EMPTY ;
            }

            active_rows = 0 ;
            if ( st > PPZERO )
            {
                for (row = RLinkUp [nrow]; row < nrow; row = RLinkUp [row])
                {
                    t = st*dl [row] ;
                    lambda [row] += t ;
                    b [row] -= sigma*t ;
                    active_rows++ ;          /* count number of active rows */
                }
                pproj_saxpy (c, pA, st, ncol) ;
            }
            else                             /* count number of active rows */
            {
                for (row = RLinkUp [nrow]; row < nrow; row = RLinkUp [row])
                {
                    active_rows++ ;
                }
            }

            if ( active_rows == 0 ) /* all rows have dropped */
            {
                status = PPROJ_ALL_ROWS_DROPPED ;
                if ( PrintLevel > 2 ) printf ("break 10\n") ;
                break ; /* all rows became inactive */
            }
#ifndef NDEBUG
            where = "end of ssor1 line search" ;
            pproj_check_line (I, lineflag, W->blks - 1, nup, dl, st) ;
            Heap [rowp-1] = EMPTY ;
            pproj_check_dual (I, NULL, where, TRUE, TRUE) ;
            pproj_checkb (I, where) ;
            pproj_check_const (NULL, PPZERO, ns, EMPTY, ntot, where) ;
            pproj_checkD (I, where) ;
            pproj_checkc (I, where) ;
#endif
            /* subspace minimization only when after an update/downdate */
            if ( nup == 0 ) break ;
            chg += nup ;

            /* If there are lots of downdates (= ntot - rowp) relative
               to the size of the memory, then skip the subspace stuff
               and restart CG, likely little accuracy in the downdates */
            int subdim = PPMIN (ssormem, it - it0) ;
            if ( ntot - rowp >= subdim - 1 )
            {
                flag = 2 ;
                /* since ir was not updated above, we now need to set it to its
                   correct value */
                for (m = rowp; m < ntot; m++)
                {
                    sing = Heap [m] ;
                    row = ineq_row [sing] ;
                    AFTnz [row] = 0 ;
                    /* Heap [m] stores the singleton row */
                    ir [row] = nsingni + sing ;
                }
                break ;
            }
  
            /* START SUBSPACE MINIMIZATION */
            if ( it - it0 >= ssormem )
            {
                memp = ssormem - 1 ; /* we can use all the memory */
            }
#if 0
            /* reduce memp when > number of active rows in the matrix */
            if ( memp >= active_rows )
            {
printf ("reduce memp: %i\n", memp) ;
                dk = dk_start ;
                l = memp - active_rows + 1 ;
                dj = dk_start+(nrow*l) ;
                memp = active_rows - 1 ;
                for (i = 0; i < active_rows; i++)
                {
                    for (row = first; row < nrow; row = RLinkUp [row])
                    {
                        dk [row] = dj [row] ;
                    }
                    dj = dj+nrow ;
                    dk = dk+nrow ;
                }
            }
#endif
            if ( nlinesearch == 1 ) /*initialization for subspace minimization*/
            {
                n = memp + 1 ; /* diag [0, ... , memp] */
                n1 = n - 1 ;
                n2 = n - 2 ;
                pproj_initx (L, PPZERO, (n*(n-1))/2) ; /* initialize L = 0*/
                /* add a small multiple of identity to encourage the
                   matrix to be positive definite after removing rows */
                t = pproj_max (diag, n) ;
                t *= 1.e-8 ;
                for (i = 0; i < n; i++)
                {
                    diag [i] += t ;
                }
            }

            /* When nlinesearch > 1, we must do update/downdate, however,
               after the first line search, it may be more efficient to
               simply form the ssormem by ssormem matrix by scratch and
               LDL' factor it */
            if ( (nlinesearch > 1) ||
                 (nf-nf0 + 2*(ntot-rowp) < 0.16*n) ) /* update */
            {

#ifndef NDEBUG
                if ( PrintLevel > 2 )
                {
                    printf("update the matrix, nf0: %ld nf: %ld n: %i\n",
                           (LONG) nf0, (LONG) nf, n) ;
                }
#endif

                dstatus = PPROJ_SSOR1_DIAG_OK ;
                for (k = nf0; k < nf; k++)
                {
                    j = F [k] ;
                    dk = dk_start ;
                    q = Ap [j+1] ;
                    for (l = 0; l < n; l++)
                    {
                        s = PPZERO ;
                        for (p = Ap [j] ; p < q ; p++)
                        {
                            i = Ai [p] ;
                            if ( ir [i] <= nsingni )
                            {
                                s += dk [i]*Ax [p] ;
                            }
                        }
                        v [l] = s ;
                        dk = dk+nrow ;
                    }

                    /* update the factorization */

                    dstatus = pproj_updown_dense (/* I, */ L, diag, v, +1, n) ;
                    if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
                    {
                        break ;
                    }
                }
                if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
                {
                    flag = 1 ; /* restart cg */
                    st = PPZERO ;
                    if ( PrintLevel > 2 ) printf ("break 17\n") ;
                    break ;
                }

                for (m = rowp; m < ntot; m++)
                {
                    sing = Heap [m] ;
                    row = ineq_row [sing] ;
                    /* form AF times row of AF  */
                    p = AFTp [row] ;
                    q = p + AFTnz [row] ;
                    ASSERT (ir [row] <= nsingni) ;
                    nr = 0 ;
                    for ( ; p < q ; p++)
                    {
                        j = AFTi [p] ;
                        q1 = Ap [j+1] ;
                        t = AFTx [p] ;
                        for (l = Ap [j]; l < q1; l++)
                        {
                            i = Ai [l] ;
                            if ( ir [i] <= nsingni )
                            {
                                if ( ns [i] == EMPTY )
                                {
                                    ns [i] = 1 ;
                                    rowlist [nr++] = i ;
                                    pk [i] = PPZERO ;
                                }
                                pk [i] += Ax [l]*t ;
                            }
                        }
                    }

                    s = .5*(pk [row] - sigma) ;
                    pproj_initx (e, PPZERO, n) ;

                    for (l = 0; l < nr; l++)
                    {
                        i = rowlist [l] ;
                        ns [i] = EMPTY ;
                        t = pk [i] ;
                        dk = dk_start+i ;
                        if ( ir [i] <= nsingni )
                        {
                            for (k = 0; k < n; k++)
                            {
                                e [k] -= t*(*dk) ;
                                dk = dk+nrow ;
                            }
                        }
                    }

                    dk = dk_start+row ;
                    u = PPZERO ;
                    for (k = 0; k < n; k++)
                    {
                        t = v [k] = *dk ;
                        u += t*t ;
                        e [k] += s*t ;
                        dk = dk+nrow ;
                    }
                    ir [row] = nsingni + sing ; /* drop row */
                    AFTnz [row] = 0 ;

                    t = PPZERO ;
                    for (k = 0; k < n; k++)
                    {
                        t += e [k]*e [k] ;
                    }

                    dstatus = PPROJ_SSOR1_DIAG_OK ;
                    if ( (t > PPZERO) && (u > PPZERO) )
                    {
                        t = sqrt (t) ;
                        u = sqrt (u) ;
                        s = sqrt (.5*t*u) ;
                        t = s/t ;
                        u = s/u ;
                        for (k = 0; k < n; k++)
                        {
                            y = u*v [k] ;
                            z = t*e [k] ;
                            v [k] = y + z ;
                            e [k] = y - z ;
                        }

                        /* update the factorization */
                        dstatus = pproj_updown_dense (L, diag, v, +1, n) ;
                        if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
                        {
                            break ;
                        }

                        /* downdate the factorization */
                        dstatus = pproj_updown_dense (L, diag, e, -1, n) ;
                        if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
                        {
                            break ;
                        }
                    }
                }
                if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
                {
                    flag = 1 ; /* restart cg */
                    st = PPZERO ;
                    if ( PrintLevel > 2 ) printf ("break 18\n") ;
                    break ;
                }

            }
            else /* construct the matrix from scratch and factor it */
            {
#ifndef NDEBUG
                if ( PrintLevel > 2 )
                {
                    PRINTF("build and factor matrix, nf0: %ld nf: %ld n: %i\n",
                            (LONG) nf0, (LONG) nf, n) ;
                }
#endif
                /* ------------------------------------------------------ */
                /* add the columns */
                /* ------------------------------------------------------ */

                for (k = nf0; k < nf; k++)
                {
                    j = F [k] ;
                    dk = dk_start ;
                    q = Ap [j+1] ;
                    for (l = 0; l < n; l++)
                    {
                        s = 0. ;
                        for (p = Ap [j]; p < q; p++)
                        {
                            i = Ai [p] ;
                            if ( ir [i] <= nsingni )
                            {
                                s += dk [i]*Ax [p] ;
                            }
                        }
                        v [l] = s ;
                        dk = dk+nrow ;
                    }

                    Lj = L-1 ;
                    for (j = 0; j < n; j++)
                    {
                        t = v [j] ;
                        diag [j] += t*t ;
                        for (i = j+1; i < n; i++)
                        {
                            Lj [i] += t*v [i] ;
                        }
                        Lj = Lj+(n2-j) ;
                    }
                }

                /* ------------------------------------------------------ */
                /* remove the rows */
                /* ------------------------------------------------------ */

                for (m = rowp; m < ntot; m++)
                {
                    sing = Heap [m] ;
                    row = ineq_row [sing] ;
                    /* form AF times row of AF  */
                    p = AFTp [row] ;
                    q = p + AFTnz [row] ;
                    ASSERT (ir [row] <= nsingni) ;
                    nr = 0 ;
                    for (; p < q; p++)
                    {
                        j = AFTi [p] ;
                        q1 = Ap [j+1] ;
                        t = AFTx [p] ;
                        for (l = Ap [j]; l < q1; l++)
                        {
                            i = Ai [l] ;
                            if ( ir [i] <= nsingni )
                            {
                                if ( ns [i] == EMPTY )
                                {
                                    ns [i] = 1 ;
                                    rowlist [nr++] = i ;
                                    pk [i] = PPZERO ;
                                }
                                pk [i] += Ax [l]*t ;
                            }
                        }
                    }

                    s = .5*(pk [row] - sigma) ;
                    pproj_initx (e, PPZERO, n) ;

                    for (l = 0; l < nr; l++)
                    {
                        i = rowlist [l] ;
                        ns [i] = EMPTY ;
                        t = pk [i] ;
                        dk = dk_start+i ;
                        if ( ir [i] <= nsingni )
                        {
                            for (k = 0; k < n; k++)
                            {
                                e [k] -= t*(*dk) ;
                                dk = dk+nrow ;
                            }
                        }
                    }

                    dk = dk_start+row ;
                    for (k = 0; k < n; k++)
                    {
                        t = v [k] = *dk ;
                        e [k] += s*t ;
                        dk = dk+nrow ;
                    }
                    ir [row] = nsingni + sing ; /* drop the row */
                    AFTnz [row] = 0 ;
 
                    Lj = L-1 ;
                    for (j = 0; j < n; j++)
                    {
                        t = v [j] ;
                        s = e [j] ;
                        diag [j] += 2.*s*t ;
                        for (i = j+1; i < n; i++)
                        {
                            Lj [i] += t*e [i] + s*v [i] ;
                        }
                        Lj = Lj+(n2-j) ;
                    }
                }
 
                /* ------------------------------------------------------ */
                /* factor the matrix by columns */
                /* ------------------------------------------------------ */

                dstatus = PPROJ_SSOR1_DIAG_ZERO ;
                Lj = L-1 ;
                for (j = 0; j < n; j++)
                {
                    /* apply previous columns to column j */
                    Lk = L-1 ;
                    s = 0. ;
                    for (k = 0; k < j; k++)
                    {
                        t = Lk [j] ;
                        z = diag [k] * t ;
                        s += t*z ;
                        for (i = j+1; i < n; i++)
                        {
                            Lj [i] -= Lk [i]*z ;
                        }
                        Lk = Lk+(n2-k) ;
                    }
                    s = diag [j] - s ;
                    if ( s <= PPZERO )
                    {
                        dstatus = PPROJ_SSOR1_DIAG_ZERO ;
                        break ;
                    }
#if 0
                    if ( s <= PPZERO )
                    {
                        s = W->sigma ;
                    }
#endif
                    diag [j] = s ;
                    for (k = j+1; k < n; k++)
                    {
                        Lj [k] /= s ;
                    }
                    Lj = Lj+(n2-j) ;
                }
            }
            if ( dstatus == PPROJ_SSOR1_DIAG_ZERO )
            {
                flag = 1 ; /* restart cg */
                st = PPZERO ;
                if ( PrintLevel > 2 ) printf ("break 19\n") ;
                break ;
            }

#ifndef NDEBUG
            where = "ssor1 after update" ;
            W->nrowdel = nrowdel ;
            W->nrowadd = nrowadd ;
            W->ncoladd = ncoladd ;
            W->ncoldel = ncoldel ;
            pproj_check_link (I, (int *) NULL, 0, where) ;
            pproj_check_modlist (I, where) ;
#endif
            /* ---------------------------------------------------------- */
            /* compute residual at current point */
            /* ---------------------------------------------------------- */

            first = RLinkUp [nrow] ;
            for (i = first; i < nrow; i = RLinkUp [i])
            {
                t = b [i] ;
                p = AFTp [i] ;
                q = p + AFTnz [i] ;
                ASSERT (ir [i] <= nsingni) ;
                for (; p < q; p++)
                {
                    t -= AFTx [p]*c [AFTi [p]] ;
                }
                gk [i] = t ;
            }
            dk = dk_start ;
            for (l = 0; l < n; l++)
            {
                t = PPZERO ;
                for (i = first; i < nrow; i = RLinkUp [i])
                {
                    t += gk [i]*dk [i] ;
                }
                w [l] = t ;
                dk = dk+nrow ;
            }

            /* ---------------------------------------------------------- */
            /* forward solve the factored system */
            /* ---------------------------------------------------------- */

            Lj = L-1 ;
            for (j = 0; j < n1; j++)
            {
                t = w [j] ;
                for (i = j+1; i < n; i++)
                {
                    w [i] -= t * Lj [i] ;
                }
                Lj = Lj+(n2-j) ;
            }

            /* ---------------------------------------------------------- */
            /* back solve the factored system */
            /* ---------------------------------------------------------- */

            for (i = n1; i >= 0; i--)
            {
                t = w [i] / diag [i] ;
                for (j = i+1; j < n; j++)
                {
                    t -= w [j]*Lj [j] ;
                }
                w [i] = t ;
                Lj = Lj-(n1-i) ;
            }

            for (l = 0; l < n; l++)
            {
                t = w [l] ;
                if ( l > 0 )
                {
                    for (i = first; i < nrow; i = RLinkUp [i])
                    {
                        dl [i] += dk [i]*t ;
                    }
                    dk = dk+nrow ;
                }
                else
                {
                    dk = dk_start ;
                    for (i = first; i < nrow; i = RLinkUp [i])
                    {
                        dl [i] = dk [i]*t ;
                    }
                    dk = dk+nrow ;
                }
            }
        }   /* return to perform a new line search in the direction dl */

        if ( (status == PPROJ_ALL_ROWS_DROPPED) || (status == PPROJ_STATUS_OK) )
        {
            if ( PrintLevel > 2 ) printf ("break 11\n") ;
            break ;
        }

        /* check to see if the iteration limit was reached */
        if ( it >= Parm->ssormaxits )
        {
            status = PPROJ_SSOR_MAX_ITS ;
            if ( PrintLevel > 2 ) printf ("break 12\n") ;
            break ;
        }

        /* If no variables are freeing or rows are dropping, then switch
           to update/downdate. Note that ssor1_its = INT_MAX if
           cholmod not used. */
        if ( (nlinesearch == 1) && (it - it0 >= W->ssor1_its) && (flag != 1) &&
              (flag != 2) )
        {
            status = PPROJ_SWITCH_TO_UPDOWN ;
            if ( PrintLevel > 2 ) printf ("break 14\n") ;
            break ;
        }

        /* flag = 1 means zero on diagonal in subspace problem
           flag = 2 means the number of row downdates is more than the
                    dimension of the subspace (the factorization is likely
                    very inaccurate) */
        if ( (nlinesearch > 1) || (flag == 1) || (flag == 2) )
        {
            if ( PrintLevel > 2 )
            {
                printf ("restart CG, nlinesearch = %i flag = %i\n",
                         nlinesearch, flag) ;
            }
            flag = -1 ; /* restart CG */
            continue ;
        }

        /* check error and continue CG */
        flag = 0 ;
        sub_inc = PPMIN (sub_inc+2, 10) ;
        for (k = 0; k < nf; k++)
        {
            j = F [k] ;
            t = c [j] ;
            if      ( loExists && (t < W->lo [j]) ) t = W->lo [j] ;
            else if ( hiExists && (t > W->hi [j]) ) t = W->hi [j] ;
            pA [j] = t ; /* projection of c on the box */
        }
        errls = PPZERO ;
        errdual = PPZERO ;
        for (i = first; i < nrow; i = RLinkUp [i])
        {
            t = b [i] ;                /* includes -sigma*lambda [i] */
            s = t + sigma*lambda [i] ; /* remove -sigma*lambda [i] term */
            dl [i] = PPZERO ;
            ASSERT (ir [i] <= nsingni) ;
            p = AFTp [i] ;
            q = p + AFTnz [i] ;
            for (; p < q; p++)
            {
                j = AFTi [p] ;
                ax = AFTx [p] ;
                t -= ax*c [j] ;
                s -= ax*pA [j] ; /* pA stores projection of c on the box */
            }
            gk [i] = t ;
            if ( fabs (s) > errdual ) errdual = fabs (s) ;
            if ( fabs (t) > errls   ) errls   = fabs (t) ;
        }
        if ( Parm->stop_condition == 0 )
        {
            errdual /= W->absAx ;
            errls   /= W->absAx ;
        }
        else if ( Parm->stop_condition == 2 )
        {
            errdual /= (W->absAx + W->ymax) ;
            errls   /= (W->absAx + W->ymax) ;
        }
        if ( PrintLevel > 1 )
        {
            printf ("it: %ld errdual: %e errls: %e\n",
                    (LONG) it, errdual, errls) ;
        }

        if ( errdual <= 0.8*grad_tol )
        {
            status = PPROJ_SOLUTION_FOUND ;
            if ( PrintLevel > 2 ) printf ("break 15\n") ;
            break ;
        }
        if ( errls <= Parm->ssordecay*errdual )
        {
            if ( PrintLevel > 2 ) printf ("break 16\n") ;
            status = PPROJ_STATUS_OK ;
            break ;
        }
    }
    W->ncoladd = ncoladd ;
    W->ncoldel = ncoldel ;
    W->nrowdel = nrowdel ;
    W->nrowadd = nrowadd ;
    Stat->ssor1_free += nf - W->nf ;
    W->chg_ssor1 = chg ;
    W->nf = nf ;
    Stat->ssor1 += pproj_timer () - tic ;
    Stat->ssor1_its += it ;
    if ( PrintLevel > 1 )
    {
        PRINTF ("SSOR1 complete, it: %ld\n", (LONG) it) ;
    }
    return (status) ;
}

/* ========================================================================= */
/* === pproj_updown_dense ================================================== */
/* ========================================================================= */

int pproj_updown_dense
(
    PPFLOAT    *L, /* lower triangle of factorization (beneath diagonal) */
    PPFLOAT *diag, /* D in the LDL' factorization */
    PPFLOAT    *w, /* update/downdate matrix */
    int      info, /* +1 = update, -1 = downdate */
    PPINT       n  /* rank of the matrix */
)
{
    int j, n2, p ;
    double *Lj, a, abar, dj, gamma, t, wj ;

/* update the factorization stored in L */

    a = 1. ;
    n2 = n - 2 ;
    Lj = L - 1 ;
    if ( info > 0 ) /* update */
    {
        for (j = 0; j < n; j++)
        {
            dj = diag [j] ;
            wj = w [j] ;
            abar = a +  wj*wj / dj ;
            dj *= abar ;
            if ( dj == PPZERO )
            {
                return (PPROJ_SSOR1_DIAG_ZERO) ;
            }
            gamma = wj / dj ;
            dj /= a ;
            diag [j] = dj ;
            a = abar ;
            for (p = j+1; p < n; p++)
            {
                t = w [p] = w [p] - wj*Lj [p] ;
                Lj [p] += gamma * t ;
            }
            Lj = Lj+(n2-j) ;
        }
    }
    else            /* downdate */
    {
        for (j = 0; j < n; j++)
        {
            dj = diag [j] ;
            wj = w [j] ;
            abar = a -  wj*wj / dj ;
            dj *= abar ;
            if ( dj == PPZERO )
            {
                return (PPROJ_SSOR1_DIAG_ZERO) ;
            }
            gamma = wj / dj ;
            dj /= a ;
            diag [j] = dj ;
            a = abar ;
            for (p = j+1; p < n; p++)
            {
                t = w [p] = w [p] - wj*Lj [p] ;
                Lj [p] -= gamma * t ;
            }
            Lj = Lj+(n2-j) ;
        }
    }
    return (PPROJ_SSOR1_DIAG_OK) ;
}
