/* ========================================================================== */
/* ==== pproj_init ========================================================== */
/* ========================================================================== */
/*
    The program allocates memory for the work arrays and sets up the Prob
    structure. The equations are reordered so as to reduce fill-in
    during the factorization of A*A'. If a nested dissection ordering is
    performed, then we also generate a block partitioning of the rows of
    the matrix. This partitioning is employed in the dasa to improve
    performance.
*/

#include "pproj.h"

int pproj_init /* return status:
                             PPROJ_OUT_OF_MEMORY
                             PPROJ_STATUS_OK */
(
    PPcom       *I, /* pproj's common structure for all the routines */
    PPdata *ppdata  /* user problem description */
)
{
    PPINT      maxdepth, maxcol, maxrow, i, j, k, ki, kd, l, m,
               n, Ni, p, pp, q, row, iend, col,
              *rowperm, *colperm, *invperm, *rowcount, *ineq_row,
              *Ai, *Ap, *Anz, *ATp, *ATi, *AFTp, *col_start,
              *row_start, *blk_preperm, *ncols, *row_to_blk,
              *twork, *tworkstart, *Cmember, *Cparent ;

    int    root, blk, blk1, blks, status, *Kids, *nkids, *parent,
          *Kp, *Kp2, *leftdesc, *depth ;
    const int loExists = I->Work->loExists ;
    const int hiExists = I->Work->hiExists ;

    PPFLOAT    Amax, bli, bui, tic, t, *Ax, *ATx, *b, *bl, *bu, *lo, *hi ;

    PPprob   *Prob ;
    PPparm   *Parm ;
    PPstat   *Stat ;
    PPwork      *W ;
    cholmod_common *cmm ;
    W    = I->Work ;
    Prob = I->Prob ;    /* the problem structure */
    Stat = I->Stat ;
    Parm = I->Parm ;

    /* some initialization */
    status = PPROJ_STATUS_OK ;
    int   const PrintLevel = Parm->PrintLevel ;
    PPINT const         sF = sizeof (PPFLOAT) ;
    PPINT const         sI = sizeof (PPINT) ;
    PPINT const         si = sizeof (int) ;
#ifndef NDEBUG
    I->Check->b            = NULL ;
    I->Check->lo           = NULL ;
    I->Check->hi           = NULL ;
#endif

    PPINT   const    nrow = Prob->nrow  = ppdata->nrow ; /* # rows in A*/
    PPINT   const    ncol = Prob->ncol  = ppdata->ncol ; /* # cols in A*/
    PPINT   const   nsing = Prob->nsing = ppdata->nsing ;/* # singletons */
    PPINT   const *userAp = ppdata->Ap ;                 /* column pointers */
    PPINT   const *userAi = ppdata->Ai ;                 /* row indices */
    PPFLOAT const *userAx = ppdata->Ax ;                 /* numerical vals */
    PPINT   const    Annz = userAp [ncol] ;            /* # nonzeros in A */
    PPFLOAT const  *usery = ppdata->y ;                  /* projection point */
    PPFLOAT const *userlo = ppdata->lo ;                 /* lower bounds x0 */
    PPFLOAT const *userhi = ppdata->hi ;                 /* upper bounds x0 */
    PPFLOAT const *userbl = ppdata->bl ;                 /* lower bounds Ax */
    PPFLOAT const *userbu = ppdata->bu ;                 /* upper bounds Ax */
    PPINT   const *userRowsing = ppdata->row_sing ; /* point row->sing*/
    PPFLOAT const  *userSinglo = ppdata->singlo ;   /* lower bounds x1 */
    PPFLOAT const  *userSinghi = ppdata->singhi ;   /* upper bounds x1 */
    PPFLOAT const   *userSingc = ppdata->singc ;    /* cost vector */

    /* initialize the statistics to zero */
    pproj_initstat (Stat) ;
    Stat->ssormaxits = Parm->ssormaxits ;
    Stat->badFactorCutoff = Parm->badFactorCutoff ;
    Stat->nrow = nrow ;
    Stat->cholmod = Parm->cholmod ;

    /* store sigma values in work struc */
    W->sigma    = Parm->sigma ;
    W->Asigma   = Parm->Asigma ;
    W->Totsigma = Parm->sigma + Parm->Asigma ;
    W->absAxk   = PPZERO ;

    /* determine the number of strict inequalities and if the user has not
       provided them */
    if ( (Ni = ppdata->ni) < 0 )
    {
        if      (  userbl == userbu )                    Ni = 0 ;
        else if ( (userbl == NULL) || (userbu == NULL) ) Ni = nrow ;
        else
        {
            Ni = 0 ; /* counter for the number of strict inequalities */
            for (i = 0; i < nrow; i++)
            {
                if ( userbl [i] < userbu [i] )
                {
                    Ni++ ;
                }
                else if ( userbl [i] > userbu [i] )
                {
                    Stat->lobad = userbl [i] ;
                    Stat->hibad = userbu [i] ;
                    Stat->ibad = i ;
                    status = PPROJ_INVALID_LINEAR_CONSTRAINT_BOUNDS ;
                    return (status) ;
                }
            }
        }
        ppdata->ni = Ni ;
    }
    if ( (Ni > 0) && (nsing > 0) )
    {
        status = PPROJ_BOTH_NI_AND_NSING_POSITIVE ;
        return (status) ;
    }

    if ( (nsing > 0) && (Parm->start_guess != 0) )
    {
        status = PPROJ_NSING_START_GUESS_PROB ;
        return (status) ;
    }
    Prob->ni = Ni ;             /* number of inequalities that are strict */
    PPINT const       ni = Ni ;
    PPINT const  nsingni = nsing + ni ; /* nsing > 0 or ni > 0, not both */
    PPINT const nsingni1 = nsingni + 1 ;
    PPINT const     ntot = nsingni1 + ncol ;

    /* initially the matrix is not factored so L is null */
    W->fac = FALSE ;
    W->L = NULL ; 

    W->nrowadd = 0 ;
    W->nrowdel = 0 ;
    W->ncoladd = 0 ;
    W->ncoldel = 0 ;

    /* initial value for SpaRSA stopping parameter */
    W->gamma = Parm->gamma ;

    /* initialize the change variables to be 1 so that either
       coordinate ascent or ssor iterations are performed if possible */
    W->chg_coor = 1 ;
    W->chg_ssor0 = 1 ;
    W->chg_ssor1 = 1 ;
    W->chg_sparsa = 1 ;
    W->sparsaOK = TRUE ;
    W->Annz = 0 ;

    /* ns used in line search, points from index to break point number.
       Also, used for bookkeeping in check_error */
    PPINT const nssize = PPMAX (nrow, ncol + nsingni1) ;
    W->ns = (PPINT *) pproj_malloc (&status, nssize, sI) ;

    /* empty if row not modified, otherwise points into Rowmodlist
       which contains list of rows to modify*/
    W->RowmodFlag = (PPINT *) pproj_malloc (&status, nrow, sI);

    /* empty if column not modified, otherwise points into Colmodlist
       which contains list of columns to modify*/
    W->ColmodFlag = (PPINT *) pproj_malloc (&status, ncol, sI) ;

    /* first part of this list contains the rows to delete
       the tail contains the rows to add */
    W->RowmodList = (PPINT *) pproj_malloc (&status, nrow, sI) ;

    /* first part of this list contains the columns to add
       the tail contains the columns to delete */
    W->ColmodList = (PPINT *) pproj_malloc (&status, ncol, sI) ;

    /* space for AT (A transpose) */
    ATp = W->ATp = (PPINT *) pproj_malloc (&status, (nrow+1), sI) ;
    ATi = W->ATi = (PPINT *) pproj_malloc (&status, Annz, sI) ;
    ATx = W->ATx = (PPFLOAT *) pproj_malloc (&status, Annz, sF) ;

    /* space for AFT (free part of A transpose) */
    AFTp = W->AFTp = (PPINT *) pproj_malloc (&status, (nrow+1), sI) ;
    W->AFTnz = (PPINT *) pproj_malloc (&status, nrow, sI) ;
    W->AFTi = (PPINT *) pproj_malloc (&status, Annz, sI) ;
    W->AFTx = (PPFLOAT *) pproj_malloc (&status, Annz, sF) ;
    /* Create the cholmod sparse matrix structure for storing AFT.
       The columns (rows of the original matrix) are not sorted since
       we add indices as they are freed. Also, the matrix is not packed,
       it only contains indices for free variables. */
    W->AFT = (cholmod_sparse *) pproj_malloc
                                     (&status, 1, sizeof (cholmod_sparse)) ;
    pproj_cholmod_sparse (W->AFT, ncol, nrow, Annz, AFTp, W->AFTnz, W->AFTi,
                          W->AFTx, FALSE, FALSE, CHOLMOD_REAL) ;

    /* lambda_tot = lambda + shift_l */
    W->lambda_tot = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;

    /* the change in lambda */
    W->dlambda = (PPFLOAT *) pproj_malloc (&status, nrow, sF);

    /* list of rows that are dropped since last call to updateAnz */
    W->dropped = pproj_malloc (&status, nsingni, sI) ;

    /* list of free variables */
    W->F = (PPINT *) pproj_malloc (&status, ncol, sI) ;

    /* ib [col] = +1 if column at upper bound
                  -1 if column at lower bound
                   0 if column is free */
    W->ib = (int *) pproj_malloc (&status, ncol, si) ;

    /* proximal lambda */
    W->shift_l = (PPFLOAT *) pproj_malloc (&status, nrow, sF);
 
    W->b = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;
    W->c = (PPFLOAT *) pproj_malloc (&status, ncol, sF) ;
    W->cold = (PPFLOAT *) pproj_malloc (&status, ncol, sF) ;

    if ( loExists == TRUE )
    {
        W->lo = (PPFLOAT *) pproj_malloc (&status, ncol, sF) ;
    }
    if ( hiExists == TRUE )
    {
        W->hi = (PPFLOAT *) pproj_malloc (&status, ncol, sF) ;
    }
    W->D = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;

    /* links for active rows */
    W->RLinkUp = (PPINT *) pproj_malloc (&status, (nrow+1), sI);
    W->RLinkDn = (PPINT *) pproj_malloc (&status, (nrow+1), sI);

    /* Links for active singletons. Two links are stored in the same
       array. uLink points to the singletons with variables at upper bound and
       lLink points to the singletons with variables at lower bound.
       Note that the location of strict inequality rows starts at 1
       so the last element is ni+nsing. ni+nsing+1 marks the end of lLink
       and ni+nsing+2 marks the end of uLink.
       Note that in LPDASA, the column singletons start at 0 not 1. Also
       the singleton variables have the same sign as the other x variables.
       For consistency and to simplify coding, we start the column singleton
       array singlo, singhi, and singc at 1, not 0. Also, we flip the bounds
       so that in pproj, lo and hi in LPDASA become -singhi and -singlo in
       pproj. */
    W->SLinkUp = (PPINT *) pproj_malloc (&status, nsingni+3, sI) ;
    W->SLinkDn = (PPINT *) pproj_malloc (&status, nsingni+3, sI) ;

    /* ineq_row [j] is the row associated with the jth singleton, either in
       the bl/bu or singlo/singhi list */
    Prob->ineq_row = ineq_row = (PPINT *) pproj_malloc (&status, nsingni+2, sI);

    /* ir gives status of row i. If nsing = 0:
           ir [i] =  0 for an equality constraint
                  =  1 for an active singleton row
                  =  ineq # for an active inequality at upper bound
                  = -ineq # for an active inequality at lower bound
                  =  ineq # or singleton # + nsingni for a dropped constraint*/

    W->ir = (PPINT *) pproj_malloc (&status, nrow, sI) ;

    if ( nsing )
    {
        /* shi points from the row number to the singleton index j for which
           singc [j] is just above lambda [i] at the current row i
           slo ...      just below lambda [i] at the current row i */
        W->slo = (PPINT *) pproj_malloc (&status, nrow, sI) ;
        W->shi = (PPINT *) pproj_malloc (&status, nrow, sI) ;
    }
    else
    {
        W->slo = NULL ;
        W->shi = NULL ;
    }

    if ( Parm->cholmod == TRUE )
    {
        /* === initialize the parameter in the cholmod common structure === */
        cmm = W->cmm ;
        CHOLMOD (start) (cmm) ;
        cmm->error_handler = pproj_error ;
        cmm->final_asis = FALSE ;
        cmm->final_super = FALSE ;
        cmm->final_ll = FALSE ; 
        cmm->final_pack = FALSE ;
        cmm->final_resymbol = TRUE ; 
        cmm->final_monotonic = FALSE ;
        cmm->print = 0 ;
        /* previous 1.2, 1.2 10 */
        cmm->grow0 = 1.1 ; /* factor grows by this much (multiplicative) */
        cmm->grow1 = 1.2 ; /* column grows by this much (multiplicative) */
        cmm->grow2 = 5 ;   /* pad this much space in a col (additive, int)*/

        /* col grows to grow1*need + grow2, if reallocated */
        /* factor grows to grow0*need

           defaults:
               grow0: 1.2 (used 2 in LPDASA)
               grow1: 1.2 (used 2 in LPDASA)
               grow2: 5   (used 5 in LPDASA) */

        cmm->nrealloc_col = 0 ;
        cmm->nrealloc_factor = 0 ;

        /* the diagonal offset in cholmod is Asigma + sigma */
        cmm->dbound = W->Totsigma ;
        /* ========== end of CHOLMOD initialization ========== */

        /* changeRHS stores the right side change. It is initialized to be
           zero and then restored to 0 after being used to update the change
           in the forward solve due to the change in the right side */
        W->changeRHS = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;
        pproj_initx (W->changeRHS, PPZERO, nrow) ;

        /* newrow added in modrow. It is initialized to be zero and restored
           to zero after use in rowadd_prep */
        W->newrow = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;
        pproj_initx (W->newrow, PPZERO, nrow) ;

        W->nd = 0 ; /* number of dropped rows */

        /* The column in A that are updated are pointed to by Cp while Cnz
           gives the number of nonzeros in the column */
        W->Cp = (PPINT *) pproj_malloc (&status, ncol, sI) ;
        W->Cnz = (PPINT *) pproj_malloc (&status, ncol, sI) ;

        /* If cholmod is used, then permutations are performed.
           rowperm [i] is the row number of the original matrix corresponding
           to row i of the permuted matrix

           colperm [j] is the column number of the original matrix corresponding
           to column j in permuted matrix */

        Prob->rowperm = (PPINT *) pproj_malloc (&status, nrow, sI) ;
        Prob->colperm = (PPINT *) pproj_malloc (&status, ncol, sI) ;

        Prob->Ax  = (PPFLOAT *) pproj_malloc (&status, Annz, sF) ;
        Prob->Ai  = (PPINT *)   pproj_malloc (&status, Annz, sI) ;
        Prob->Ap  = (PPINT *)   pproj_malloc (&status, ncol+1, sI) ;
        Prob->Anz = (PPINT *)   pproj_malloc (&status, ncol, sI) ;

        Prob->y  = (PPFLOAT *) pproj_malloc (&status, ncol, sF) ;
        Prob->lo = (loExists) ? (PPFLOAT *) pproj_malloc (&status,ncol,sF):NULL;
        Prob->hi = (hiExists) ? (PPFLOAT *) pproj_malloc (&status,ncol,sF):NULL;
        Prob->b  = (PPFLOAT *) pproj_malloc (&status, nrow, sF) ;

        if ( nsing )
        {
            Prob->row_sing = (PPINT *)   pproj_malloc (&status, nrow+1,  sI) ;
            Prob->singc    = (PPFLOAT *) pproj_malloc (&status, nsing+1, sF) ;
            Prob->singlo   = (PPFLOAT *) pproj_malloc (&status, nsing+1, sF) ;
            Prob->singhi   = (PPFLOAT *) pproj_malloc (&status, nsing+1, sF) ;
            Prob->bl = Prob->bu = NULL ; /* use Prob->b since no strict ineq */
        }
        else
        {
            Prob->row_sing = NULL ;
            Prob->singc    = NULL ;
            Prob->singlo   = NULL ;
            Prob->singhi   = NULL ;
        }
        Prob->bl = (PPFLOAT *) pproj_malloc (&status, nsingni1, sF) ;
        Prob->bu = (PPFLOAT *) pproj_malloc (&status, nsingni1, sF) ;

        /* We keep track of the size of the updates and downdates */
        k = 3.*sqrt ((double) ncol) ;
        PPINT const size_updowns = PPMAX (k, 10) ;
        W->size_updowns = Stat->size_updowns = size_updowns ;
        Stat->updowns = (int *) pproj_malloc (&status, (size_updowns+1), si) ;

        /* initialize updowns array */
        for (i = 0; i <= Stat->size_updowns; i++)
        {
            Stat->updowns [i] = 0 ;
        }
    }
    else /* no cholmod, iterative method */
    {
        W->cmm = NULL ;
        Prob->rowperm = NULL ;
        Prob->colperm = NULL ;
        Prob->Anz     = NULL ;
        Prob->Ap      = (PPINT *)   userAp ;
        Prob->Ai      = (PPINT *)   userAi ;
        Prob->Ax      = (PPFLOAT *) userAx ;
        Prob->y       = (PPFLOAT *) usery ;
        Prob->lo = (loExists) ? (PPFLOAT *) userlo : NULL ;
        Prob->hi = (hiExists) ? (PPFLOAT *) userhi : NULL ;
        if ( nsing )
        {
            Prob->singlo   = (PPFLOAT *) userSinglo ;
            Prob->singhi   = (PPFLOAT *) userSinghi ;
            Prob->singc    = (PPFLOAT *) userSingc ;
            Prob->row_sing = (PPINT *  ) userRowsing ;
        }
        if ( ni )
        {
            Prob->bl = (PPFLOAT *) userbl ;
            Prob->bu = (PPFLOAT *) userbu ;
        }
    }

    /* if any of these malloc's failed, then terminate the run */
    if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

    /* now that the arrays are malloc'd, we can do some initialization */
    if ( nsing )
    {
        pproj_initi (W->slo, (PPINT) 0, nrow) ;
        pproj_initi (W->shi, (PPINT) 0, nrow) ;
    }
    ineq_row [nsingni1] = nrow ; /* stopper */
    pproj_initi (W->ir, (PPINT) 0, nrow) ;
    pproj_initi (W->ns, (PPINT) EMPTY, nssize) ;
    pproj_initi (W->RowmodFlag, (PPINT) EMPTY, nrow) ;
    pproj_initi (W->ColmodFlag, (PPINT) EMPTY, ncol) ;

#ifndef NDEBUG
    /* for checking that matrix is correctly permuted */
    PPFLOAT *CheckAx, *CheckATx ;
    PPINT *CheckAi, *CheckAp, *CheckATi, *CheckATp ;
    pproj_initx (W->dlambda, PPZERO, nrow) ;
    pproj_initx (W->x, PPZERO, ncol) ;
#endif

    Ax      = Prob->Ax ;   /* numerical entries in A */
    Ai      = Prob->Ai ;   /* row indices in A */
    Ap      = Prob->Ap ;   /* column pointers for A */
    Anz     = Prob->Anz ;  /* number of nonzeros in each column of A */
    rowperm = Prob->rowperm ;
    colperm = Prob->colperm ;
    lo      = Prob->lo ;
    hi      = Prob->hi ;
    bl      = Prob->bl ;
    bu      = Prob->bu ;
    b       = Prob->b ;

    /* ---------------------------------------------------------------------- */
    /* fill-reducing permutation */
    /* ---------------------------------------------------------------------- */

    /* The rows of the original matrix A will be permuted to reduce fill-in.
       rowperm [i] is the row number of the original matrix that
       is inserted in row i of the permuted matrix. In a multilevel
       partitioning, Cmember [i] is the block number associated with row i
       in the original matrix. Cparent is an array of size equal to the
       number of blocks, and Cparent [k] is the parent of node (block) k in
       the tree associated with the multilevel partition. Think of the
       permuted matrix having the rows associated with block 0 at the
       top of the matrix, followed by the rows associated with block 1,
       and so on. The trailing rows in the matrix correspond to the
       root of the tree. */
 
    if ( Parm->cholmod == TRUE )
    {
#ifndef NDEBUG
        /* check for sorted rows in each column */
        p = 0 ;
        for (j = 0; j < ncol; j++)
        {
            q = userAp [j+1] ;
            i = -1 ;
            for (; p < q; p++)
            {
                if ( userAi [p] <= i )
                {
                    printf ("row numbers in col %ld of input matrix "
                            "not sorted\n", (LONG) j) ;
                    printf ("    row index %ld follows row %ld in column %ld\n",
                            (LONG) userAi [p], (LONG) i, (LONG) j) ;
                    pproj_error (-1, __FILE__, __LINE__,
                    "input matrix has row indices out-of-order\n") ;
                }
                i = userAi [p] ;
            }
        }
#endif

        tic = pproj_timer ( ) ;
        /* both Cmember and Cparent are freed later */
        Cmember = (PPINT *) pproj_malloc (&status, nrow, sI) ;
        Cparent = (PPINT *) pproj_malloc (&status, nrow, sI) ;

        /* set up the matrix to reorder */
        W->A = (cholmod_sparse *) pproj_malloc
                                     (&status, 1, sizeof (cholmod_sparse)) ;

        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

        /* Store the user's packed matrix with sorted columns in W->A.
           The two TRUEs below correspond to sorted and packed column. */
        pproj_cholmod_sparse (W->A, nrow, ncol, Annz, (PPINT *) userAp, NULL,
              (PPINT *) userAi, (PPFLOAT *) userAx, TRUE, TRUE, CHOLMOD_REAL) ;

        if ( Parm->multilevel == TRUE ) /* perform a multilevel partition of A*/
        {
            double nd_oksep = 0.06 ; /* was 0.12 */
            int nd_small = 500 ;

            /* -------------------------------------------------------------- */
            /* multilevel case:  partition and order the matrix */
            /* -------------------------------------------------------------- */

            /* compute maximum number of nonzeros in a column */
            maxcol = 0 ;
            p = 0 ;
            for (j = 1; j <= ncol; j++)
            {
                q = userAp [j] ;
                if ( q - p > maxcol ) maxcol = q - p ;
                p = q ;
            }
            Prob->maxcol = maxcol ;

            if (Prob->maxcol > 0.5 * nrow)
            {
                if ( PrintLevel )
                {
                    printf ("-- ordering method: colamd (forcing one block)\n");
                }
                CHOLMOD (colamd) (W->A, NULL, 0, TRUE, rowperm, cmm) ;
                blks = 1 ;
            }
            else
            {
                cmm->current = 0 ;

                /* use old default method - order each connected component
                 * separately.  This can result in an unbalanced separator tree.
                 */
                cmm->method [0].nd_components = 1 ;

                /* use new default method
                cmm->method [0].nd_components = 0 ;
                */

                if ( PrintLevel )
                {
                    printf ("nd_components: %d\n",
                             cmm->method [0].nd_components) ;
                }

                blks = CHOLMOD (nested_dissection) (W->A, NULL, 0, rowperm,
                        Cparent, Cmember, cmm) ;

                if ( PrintLevel )
                {
                    printf ("orig blks %d\n", blks) ;
                }

#ifndef NDEBUG
                for (i = 0 ; i < nrow ; i++)
                {
                    blk = Cmember [i] ;
                    if (blk < 0 || blk > blks)
                    {
                        printf ("Hey orig! %ld %i\n", (LONG) i, blk) ;
                    }
                    ASSERT (blk >= 0 && blk < blks) ;
                }
#endif
                /* prune the separator tree */
                if ( PrintLevel )
                {
                    printf ("prune %g %d\n", nd_oksep, nd_small) ;
                }
                blks = CHOLMOD (collapse_septree) (nrow, blks, nd_oksep,
                       nd_small, Cparent, Cmember, cmm) ;
            }

            if ( PrintLevel )
            {
                printf ("blks: %d\n", blks) ;
            }

            /* Fix Cparent.  CHOLMOD can return a forest, but PPROJ expects a
             * tree.  Force all root nodes < blks-1 to have node blks-1 as their
             * parent. */

            for (blk = 0 ; blk < blks-1 ; blk++)
            {
                if (Cparent [blk] == EMPTY)
                {
                    Cparent [blk] = blks-1 ;
                }
            }

        }
        else /* not multilevel, reorder rows to reduce fill-in */
        {
            blks = 1 ; /* there is only one block */
            /* -------------------------------------------------------------- */
            /* CHOLMOD nested dissection, or COLAMD if dense cols exist: */
            /* -------------------------------------------------------------- */

            if ( PrintLevel )
            {
                printf ("--- ordering method: nd or colamd\n") ;
                printf ("maxcol %ld  nrow %ld   maxcol/nrow %8.5f  "
                        "maxcol/sqrt(nrow) %8.5f\n",
                (LONG) Prob->maxcol, (LONG) nrow, Prob->maxcol/((PPFLOAT) nrow),
                Prob->maxcol/sqrt((PPFLOAT) nrow)) ;
            }

            if (Prob->maxcol > 0.5 * nrow)
            {

                if ( PrintLevel )
                {
                    printf ("--- ordering method: colamd\n") ;
                }
                CHOLMOD (colamd) (W->A, NULL, 0, TRUE, rowperm, cmm) ;
            }
            else
            {
                /* use old default method - order each connected component
                 * separately.  This can result in an unbalanced separator
                 * tree. */
                cmm->current = 0 ;
                cmm->method [0].nd_components = 1 ;

                if ( PrintLevel )
                {
                    printf ("--- ordering method: nd\n") ;
                }
                CHOLMOD (nested_dissection) (W->A, NULL, 0, rowperm,
                    Cparent, Cmember, cmm) ;
            }
        }

        if ( PrintLevel )
        {
            printf ("\n--------------- pproj_initlevels has found rowperm\n") ;
        }

        /* the CHOLMOD sparse matrix W->A will be replaced by a new matrix
           generated below by performing row and column exchanges based
           on the ordering that was generated above. Throughout pproj_dasa,
           the matrix is not packed since the row indices for deleted
           rows are essentially removed (the elements of Anz are reduced
           when rows are deleted, and the deleted rows are moved to the
           tail end of the column). Note that the active elements in the
           column are always sorted. The TRUE and FALSE below correspond
           to sorted and unpacked columns. */
        pproj_cholmod_sparse (W->A, nrow, ncol, Annz, Prob->Ap,
                  Prob->Anz, Prob->Ai, Prob->Ax, TRUE, FALSE, CHOLMOD_REAL) ;

        Stat->partition = pproj_timer ( ) - tic ;

        /* ------------------------------------------------------------------ */
        /* allocate remainder of the multilevel part of W */
        /* ------------------------------------------------------------------ */
        /* the tree describing the multilevel decomposition is quite small,
           int or short is fine */
        W->Kids       = (int *) pproj_malloc (&status, blks, si) ;
        W->nkids      = (int *) pproj_malloc (&status, blks, si) ;
        W->parent     = (int *) pproj_malloc (&status, blks, si) ;
        W->Kp         = (int *) pproj_malloc (&status, blks, si) ;
        W->depth      = (int *) pproj_malloc (&status, blks, si) ;
        W->leftdesc   = (int *) pproj_malloc (&status, blks, si) ;

        /* The following relate to the matrix, first 3 could be long int */
        W->col_start  = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->sol_start  = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->row_start  = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->sol_to_blk = (int *)   pproj_malloc (&status, (nsingni+2), si) ;

        /* The following arrays change, and are stored in the work structure */
        W->joblist  = (int *) pproj_malloc (&status, blks, si) ;
        W->kidsleft = (int *) pproj_malloc (&status, blks, si) ;
        W->jobcols= (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->jobrows= (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->Rstart = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        W->Rend   = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

        row_start = W->row_start ;
        if ( blks > 1 )
        {
            /* compute row_start.  After permuting the matrix, block k starts at
             * row row_start [k] and ends at row row_start [k+1]-1. */
            for (blk = 0 ; blk < blks ; blk++)
            {
                row_start [blk] = 0 ;
            }
            for (i = 0 ; i < nrow ; i++)
            {
                blk = Cmember [i] ;
#ifndef NDEBUG
                if (blk < 0 || blk > blks)
                {
                    printf ("Hey! %ld %i\n", (LONG) i, blk) ;
                }
                ASSERT (blk >= 0 && blk < blks) ;
#endif
                row_start [blk]++ ;
            }
            q = 0 ;
            for (blk = 0 ; blk < blks ; blk++)
            {
                p = q ;
                q += row_start [blk] ;
                row_start [blk] = p ;
            }
            row_start [blks] = nrow ;
        }
        else /* single level, 1 block */
        {
            Cparent [0] = EMPTY ;
            row_start [0] = 0 ;
            row_start [1] = nrow ;
        }
        pproj_free (Cmember) ;

        nkids = W->nkids ;
        leftdesc = W->leftdesc ;
        col_start = W->col_start ;
        depth = W->depth ;

        /*
        Given:
            row_start [blk] = first row in blk
            parent    [blk] = parent of node blk

        Compute:
            leftdesc  [blk] = left descendant of blk
            nkid      [blk] = number of children of blk
            col_start [blk] = first column in blk
            sol_start [blk] = index of first singleton in blk
            sol_to_blk[j]   = k if jth strict inequality/singleton is in block k

        Work array:
            ncols      [blk] = number of columns in blk
            blk_preperm[j]   = blk associated with column j before the perm
            row_to_blk [i]   = k if row i after rowperm is in block k 

        */

        /* permute the entries of the b vector and setup bl and bu */
        if ( ni == 0 ) /* permute the entire vector, no strict inequalities */
        {
            for (i = 0; i < nrow; i++)
            {
                ASSERT (rowperm [i] >= 0 && rowperm [i] < nrow) ;
                b [i] = userbl [rowperm [i]] ;
            }
        }
        else /* ni > 0, no column singletons */
        {
            const int blExists = (userbl == NULL) ? FALSE : TRUE ;
            const int buExists = (userbu == NULL) ? FALSE : TRUE ;
            /* The components of b are defined as follows:
               b_i = Bl_i if Bl_i = Bu_i
               b_i = 0  otherwise (a place holder) */
            k = 0 ;
            for (row = 0; row < nrow; row++) /* row in the permuted matrix*/
            {
                i = rowperm [row] ;
                bli = (blExists) ? userbl [i] : -PPINF ;
                bui = (buExists) ? userbu [i] :  PPINF ;
                if ( bli < bui )
                {
                    b  [row] = PPZERO ;
                    k++ ;
                    bl [k] = bli ;
                    bu [k] = bui ;
                    ineq_row [k] = row ;
                }
                else
                {
                    b [row] = bli ;
                }
            }
        }

        /* if there are column singletons, then permute the data to
           correspond to the new row ordering */
        if ( nsing )
        {
            l = 1 ; /* store singletons starting at 1 not 0 */
            PPINT *row_sing = Prob->row_sing ;
            PPFLOAT *singlo = Prob->singlo ;
            PPFLOAT *singhi = Prob->singhi ;
            PPFLOAT  *singc = Prob->singc ;
            for (i = 0; i < nrow; i++) /* i = row in the permuted matrix */
            {
                row = rowperm [i] ;     /* original row in the user matrix */
                j = userRowsing [row] ;
                q = userRowsing [row+1] ;
                row_sing [i] = l ;
                if ( j == q ) continue ; /* no singletons in the row */
                k = l - j ;
                l += q - j ;             /* add the number of singletons to l */
                PPINT   *ineq_rowk = ineq_row+k ;
                PPFLOAT   *singlok = singlo+k ;
                PPFLOAT   *singhik = singhi+k ;
                PPFLOAT    *singck = singc+k ;
                for (; j < q; j++)
                {
                    ineq_rowk [j] = i ;
                    singlok   [j] = userSinglo [j] ;
                    singhik   [j] = userSinghi [j] ;
                    singck    [j] = userSingc [j] ;
                }
            }
            row_sing [nrow] = l ;
        }
        /* Temporary work space that will be freed below */
        twork = (PPINT *) pproj_malloc (&status, (ncol+3*nrow+blks+1), sI) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

        tworkstart  = twork ; /* save for future reference */
        invperm     = twork ; twork += nrow ;
        rowcount    = twork ; twork += nrow ;
        blk_preperm = twork ; twork += ncol ;
        ncols       = twork ; twork += blks ;
        row_to_blk  = twork ; twork += nrow+1 ;

        root = blks - 1 ;
        for (blk = 0; blk < blks; blk++)
        {
            ncols [blk] = nkids [blk] = 0 ;
            depth [blk] = leftdesc [blk] = EMPTY ;
        }
        depth [root] = 0 ;

        /* Evaluate number of children and left descendant */

        leftdesc [root] = 0 ;
        i = 0 ;
        maxdepth = 0 ;
        parent = W->parent ;
        for (blk = 0; blk < root; blk++)
        {
            iend = row_start [blk+1] ;
            for (; i < iend; i++)
            {
                row_to_blk [i] = blk ;
            }

            parent [blk] = Cparent [blk] ;
            nkids [Cparent [blk]]++ ;
            if ( nkids [blk] == 0 ) leftdesc [blk] = blk ;
            /* go up the tree and set the left descendants of the successive
               parents to be blk if they have not yet been set. This loop
               terminates since the left descendant of the root has been
               initialized to 0 */
            l = blk ;
            while ( leftdesc [(l = Cparent [l])] == EMPTY )
            {
                leftdesc [l] = blk ;
            }
            l = blk ;
            m = 0 ;
            while ( depth [l] == EMPTY )
            {
                l = Cparent [l] ;
                m++ ;
            }
            m += depth [l] ;
            maxdepth = PPMAX (maxdepth, m) ;
            l = blk ;
            while ( depth [l] == EMPTY )
            {
                depth [l] = m-- ;
                l = Cparent [l] ;
            }
        }
        for (; i < nrow; i++)
        {
            row_to_blk [i] = root ;
        }
        row_to_blk [nrow] = blks ; /* = root + 1 */
        W->maxdepth = Stat->maxdepth = maxdepth ;
        /* Stat->solves counts number of solves at each level in the tree. */
        Stat->solves = (int *) pproj_malloc (&status, (maxdepth+1), si);
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

        /* initialize the solve statistics */
        for (blk = 0; blk <= maxdepth; blk++)
        {
            Stat->solves [blk] = 0 ;
        }

        ASSERT (row_start [root+1] == nrow) ;

        /* Invert rowperm, initialize row counters */
        for (i = 0; i < nrow; i++)
        {
            /* invperm [i] = row in permuted matrix corresponding to row i
                             in original matrix */
            invperm [rowperm [i]] = i ;
        }
        pproj_initi (rowcount, (PPINT) 0, nrow) ;

        /* Evaluate number of columns in each block */
        p = 0 ;
        for (j = 0; j < ncol; j++)
        {
            /* locate the smallest row index, count number elements in row */
            q = userAp [j+1] ;
            k = nrow - 1 ;
            for ( ; p < q ; p++)
            {
                i = invperm [userAi [p]] ;
                k = PPMIN (k, i) ;    /* smallest row index in column */
                rowcount [i]++ ;    /* # elements in row of permuted matrix */
            }

            /* count number of columns in block */
            blk_preperm [j] = row_to_blk [k] ;
            ncols [blk_preperm [j]]++ ;
        }

        /* set up Kp (pointer to kids), col_start (first column singleton in
           block) */
        Kids = W->Kids ;
        Kp = W->Kp ;
        n = m = 0 ;
        Kp2 = (int *) pproj_malloc (&status, blks, si) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;
        for (blk = 0; blk < blks; blk++)
        {
            Kp [blk] = n ;
            Kp2[blk] = n ;
            n += nkids [blk] ;
            l = m + ncols [blk] ;
            /* ncols is temporary start of cols in block blk */
            ncols [blk] = col_start [blk] = m ;
            m = l ;
        }
        col_start [blks] = l ;

        /* Kids is the array of node children pointed into by Kp */
        for (blk = 0 ; blk < root ; blk++)
        {
            Kids [Kp2 [Cparent [blk]]++] = blk ;
        }

        /* done using Cparent and Kp2, free it */
        pproj_free (Cparent) ;
        pproj_free (Kp2) ;

        /* sol_to_blk [j] = block associated with jth column singleton
           sol_start gives the first singleton associated with
           each block. Unlike lstart and ustart, we do not care whether the
           inequality is currently at the lower or upper bound or inactive. */
        int   *sol_to_blk = W->sol_to_blk ;
        PPINT *sol_start  = W->sol_start ;
        j = 1 ;
        sol_to_blk [0] = 0 ;
        blk1 = sol_to_blk [j] = row_to_blk [ineq_row [j]] ;
        blk = 0 ;
        /* set sol_start to 1 for all blocks before first inequality */
        while ( blk < blk1 )
        {
            sol_start [blk] = j ;
            blk++ ;
        }

        while ( blk < blks )
        {
            /* blk1 = sol_to_blk [j] and
               j = first strict inequality in block blk1 */
            sol_start [blk1] = j ;
            j++ ;

            /* find the first row in the next block */
            while ( (sol_to_blk [j] = row_to_blk [ineq_row [j]]) <= blk1 )
            {
                j++ ;
            }
            /* store the block associated with the first row */
            blk1 = sol_to_blk [j] ;
            /* set the start of all blocks before this new block to j */
            while ( blk < blk1 )
            {
                blk++ ;
                sol_start [blk] = j ;
            }
        }
        sol_start [blk] = nsingni1 ;

        /* colperm [k] = column of original matrix corresponding to column k in
                         permuted matrix */
        for (j = 0; j < ncol; j++)
        {
            k = ncols [blk_preperm [j]]++ ;
            colperm [k] = j ;
            if ( loExists ) lo [k] = userlo [j] ;
            if ( hiExists ) hi [k] = userhi [j] ;
            Prob->y [k] = usery [j] ;
        }

       /* Apply colperm to columns of A and rowperm to rows of A to obtain AT.
          The goal of the row and column permutations is to obtain the structure
          shown in Figure 3 of the multilevel paper (Math. Program.,
          Ser. A (2008) 112:403–425 DOI 10.1007/s10107-006-0022-3)*/

        k = 0 ;
        for (i = 0; i < nrow; i++)
        {
            l = k + rowcount [i] ;
            rowcount [i] = k ;
            ATp  [i] = k ;
            AFTp [i] = k ;
            k = l ;
        }
        ATp  [nrow] = k ;
        AFTp [nrow] = k ;

        /* done using blk_preperm above, now use the space to store the
           number of nonzeros in each column of A */
        Anz = blk_preperm ;
        Amax = PPZERO ;
        for (col = 0; col < ncol; col++)
        {
            j = colperm [col] ;
            p = userAp [j] ;
            q = userAp [j+1] ;
            Anz [col] = q - p ;
            for (; p < q; p++)
            {
                i = invperm [userAi [p]] ;
                k = rowcount [i]++ ;
                ATi [k] = col ;
                t = userAx [p] ;
                ATx [k] = t ;
                if ( fabs (t) > Amax ) Amax = fabs (t) ;
            }
        }
        Prob->Amax = Amax ;
        if ( (Parm->ScaleSigma == TRUE) && (Amax != PPZERO) )
        {
            /* sigma may decay during a run due to proximal updates.
               If ppcom = TRUE, then in a subsequent run, we initialize
               sigma = start_sigma */
            W->sigma      *= Amax ;
            W->start_sigma = W->sigma ;
            W->Asigma     *= Amax ;
            W->Totsigma    = W->sigma + W->Asigma ;
            W->cmm->dbound = W->Totsigma ;
        }

        /* construct the final A matrix, A = AT' */
        Ap [0] = 0 ;
        for (j = 0; j < ncol; j++)
        {
            Ap [j+1] = Ap [j] + Anz [j] ;
            Anz [j] = Ap [j] ;
        }
        p = 0 ;
        for (i = 0; i < nrow; i++)
        {
            q = ATp [i+1] ;
            for (; p < q; p++)
            {
                pp = Anz [ATi [p]]++ ;
                Ai [pp] = i ;
                Ax [pp] = ATx [p] ;
            }
        }
        /* A and AT have now been formed */

#ifndef NDEBUG
        /* check that A and AT are correctly permuted */
        n = userAp [ncol] ;
        CheckAp = (PPINT *) pproj_malloc (&status, (ncol+1), sI) ;
        CheckAi = (PPINT *) pproj_malloc (&status, n, sI) ;
        CheckAx = (PPFLOAT *) pproj_malloc (&status, n, sF) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

        /* copy column pointers and the numerical values to the check matrix */
        pproj_copyi (CheckAp, Ap, ncol+1) ;
        pproj_copyx (CheckAx, Ax, n) ;

        /* map rows of the current permuted A to rows of the original matrix*/
        for (p = 0; p < n; p++)
        {
            CheckAi [p] = rowperm [Ai [p]] ;
        }

        /* now transpose CheckA */
        CheckATp = (PPINT *) pproj_malloc (&status, (nrow+1), sI) ;
        CheckATi = (PPINT *) pproj_malloc (&status, n, sI) ;
        CheckATx = (PPFLOAT *) pproj_malloc (&status, n, sF) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;
        pproj_transpose (CheckATp, CheckATi, CheckATx, CheckAp, CheckAi,
                         CheckAx, nrow, ncol, tworkstart) ;

        /* map the columns in checkA to those in the original matrix */
        for (p = 0; p < n; p++)
        {
            CheckATi [p] = colperm [CheckATi [p]] ;
        }
        pproj_transpose (CheckAp, CheckAi, CheckAx, CheckATp, CheckATi,
                         CheckATx, ncol, nrow, tworkstart) ;

        /* checkA  should now equal the original matrix */
        for (j = 0; j <= ncol; j++)
        {
            if ( userAp [j] != CheckAp [j] )
            {
                pproj_error (-1, __FILE__, __LINE__,
                "error in Ap in initlevels\n") ;
            }
        }
        /* check Ai and Ax */
        for (p = 0; p < n; p++)
        {
            if ( userAi [p] != CheckAi [p] )
            {
                printf ("p: %ld Ai: %ld check: %ld\n",
                        (LONG) p, (LONG) Ai [p], (LONG) CheckAi [p]) ;
                pproj_error (-1, __FILE__, __LINE__,
                "error in Ai in initlevels\n") ;
            }
            if ( userAx [p] != CheckAx [p] )
            {
                printf ("p: %ld Ax: %e check: %e\n",
                        (LONG) p, Ax [p], CheckAx [p]) ;
                pproj_error (-1, __FILE__, __LINE__,
                "error in Ax in initlevels\n") ;
            }
        }
        /* check transpose */
        pproj_transpose (CheckATp, CheckATi, CheckATx, Ap, Ai, Ax,
                         nrow, ncol, tworkstart) ;
        /* check ATp */
        for (i = 0; i <= nrow; i++)
        {
            if ( ATp [i] != CheckATp [i] )
            {
                pproj_error (-1, __FILE__, __LINE__,
                "error in ATp in initlevels\n") ;
            }
        }
        /* check ATi and ATx */
        for (p = 0; p < n; p++)
        {
            if ( ATi [p] != CheckATi [p] )
            {
                printf ("p: %ld ATi: %ld check: %ld\n",
                        (LONG) p, (LONG) ATi [p], (LONG) CheckATi [p]) ;
                pproj_error (-1, __FILE__, __LINE__,
                "error in ATi in initlevels\n") ;
            }
            if ( ATx [p] != CheckATx [p] )
            {
                printf ("p: %ld ATx: %e check: %e\n",
                        (LONG) p, ATx [p], CheckATx [p]) ;
                pproj_error (-1, __FILE__, __LINE__,
                "error in ATx in initlevels\n") ;
            }
        }
        pproj_free (CheckAp) ;
        pproj_free (CheckATp) ;
        pproj_free (CheckAi) ;
        pproj_free (CheckATi) ;
        pproj_free (CheckAx) ;
        pproj_free (CheckATx) ;
#endif
        pproj_free (tworkstart) ;
    }
    else /* for an iterative method, the row permutation is the identity; we
            just need to compute AT and the column pointers for AFT */
    {
        blks = 1 ;
        if ( Parm->ScaleSigma == TRUE )
        {
            Amax = pproj_max (Ax, Annz) ;
            Prob->Amax = Amax ;
            if ( Amax != PPZERO )
            {
                W->sigma *= Amax ;
            }
        }
        pproj_transpose (ATp, ATi, ATx, Ap, Ai, Ax, nrow, ncol,
                         W->AFTp /* work array */) ;
        /* store pointers in AFTp */
        pproj_copyi (AFTp, ATp, nrow+1) ;
        /* copy Prob->b, Prob->lo, and Prob->hi to work structure */
        pproj_copyx (W->b, Prob->b, nrow) ;
        if ( loExists == TRUE )
        {
            pproj_copyx (W->lo, Prob->lo, ncol) ;
        }
        if ( hiExists == TRUE )
        {
            pproj_copyx (W->hi, Prob->hi, ncol) ;
        }
        Stat->solves = (int *) pproj_malloc (&status, 1, si) ;
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;
        Stat->solves [0] = 0 ;
        W->sol_to_blk = NULL ;
        W->ustart = NULL ;
        W->lstart = NULL ;

#ifndef NDEBUG
        W->leftdesc  = (int *) pproj_malloc (&status, blks, si) ;
        W->col_start = (PPINT *) pproj_malloc (&status, (blks+1),sI);
        W->row_start = (PPINT *) pproj_malloc (&status, (blks+1),sI);
        if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;
        W->leftdesc [0] = 0 ;
        W->row_start [0] = 0 ;
        W->row_start [1] = nrow ;
        W->col_start [0] = 0 ;
        W->col_start [1] = ncol ;
#endif
    }
    W->blks = blks ;
    Stat->blks = blks ;
    /* Both AT and A are now permuted according to the rowperm and colperm */

    /* Complete the allocation of the workspace W by allocating the
       pointers to the starting column in each block of the multilevel
       decomposition. lstart is associated with the equations at lower
       bounds and ustart is associated with the equations at upper bound */
    W->lstart = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
    W->ustart = (PPINT *) pproj_malloc (&status, (blks+1), sI) ;
    if ( status == PPROJ_OUT_OF_MEMORY ) return (status) ;

    /* determine the length of the longest row in A */
    maxrow = 0 ;
    p = 0 ;
    for (i = 1; i <= nrow; i++) 
    {
        q = ATp [i] ;
        if ( q - p > maxrow ) maxrow = q - p ;
        p = q ;
    }
    Prob->maxrow = maxrow ;

    ki = 0 ; /* PPINT space */
    kd = 0 ; /* PPFLOAT space */
    /* ntot = nsingni + 1 + ncol */

    /* space for phase1 */
    if ( Parm->phase1 >= 0 )
    {
        j = 3*maxrow ;
        if ( j > ki ) ki = j ;

        j = ntot ;
        if ( j > ki ) ki = j ;

        j = nrow ;
        if ( j > ki ) ki = j ;

        j = 2*nrow + ncol + ntot ;
        if ( j > kd ) kd = j ;
    }

    /* space for SpaRSA */
    if ( Parm->use_sparsa == TRUE )
    {
        if ( sI >= si )
        {
            j = ntot + nrow + ncol ;
            if ( j > ki ) ki = j ;
        }
        else
        {
            i = ceil ((double) si / (double) sI) ;
            j = ntot + nrow + i*ncol ;
            if ( j > ki ) ki = j ;
        }

        j = ncol + ntot + nrow + Parm->mem ;
        if ( j > kd ) kd = j ;
    }

    /* space for coordinate ascent steps */
    if ( Parm->use_coor_ascent == TRUE )
    {
        j = 3*maxrow ;
        if ( j > ki ) ki = j ; /* int space */

        j = maxrow ;
        if ( j > kd ) kd = j ; /* double space */
    }

    /* Allocate space for ssor algorithms. These are either used in the
       iterative mode or in a presolve phase before starting the updates
       and downdates */

    if ( ((Parm->cholmod == TRUE) && (Parm->use_ssor0 == TRUE)) ||
          (Parm->cholmod == FALSE) )
    {
        if ( ntot + ncol > ki )
        {
            ki = ntot + ncol ; /* int space */
        }

        j = 2*nrow +ncol + ntot ;
        if ( j > kd ) kd = j ; /* double space */
    }

    if ( ((Parm->cholmod == TRUE) && (Parm->use_ssor1 == TRUE)) ||
         (Parm->cholmod == FALSE) )
    {
        if ( ntot + ncol + nrow > ki )
        {
            ki = ntot + ncol + nrow ; /* int space */
        }
        j = 5*nrow + ncol + ntot ;
        k = PPMIN (nrow, Parm->ssormem) ;
        k = PPMIN (k, ncol) ;
        k = PPMAX (k, 2) ;         /* ssormem must be at least 2 */
        W->ssormem = k ;
        j += (4+nrow)*k + (k*(k-1))/2 ;
        if ( j > kd ) kd = j ;   /* double space */
    }

    /* initialize some statistics */
    W->nrup = 0 ;            /* total number of rooted updates */
    W->npup = 0 ;            /* total number of partial updates */
    W->nchols = 0 ;          /* total number of chols */
    W->cholaatflops = PPZERO ; /* average flops in a chol (incl. AA') */
    W->rupflops = PPZERO ;     /* average flops in a rooted update */
    W->pupflops = PPZERO ;     /* average flops in a partial update */

    if ( Parm->cholmod == TRUE ) /* use update/downdate */
    {
        /* -> line search */
        j = (ntot + 1) ;
        if ( ki < j ) ki = j ;

        /* forward (nrow), dl (nrow), pA (ncol), Br_value (ntot) */
        /* NOTE: it seems that 3*nrow can be replaced by 2*nrow */
        j = (2*ncol + 3*nrow + nsingni + 1) ;
        if ( kd < j ) kd = j ;
        /* (2*ncol + 3*nrow + ni)*sizeof(double) + (ntot + 1)*sI) */

        /* -> update/downdate at top of ascent */
        j = (2*ncol + 4*nrow) ;
        if ( ki < j ) ki = j ;

        j = (PPMAX (nrow, ncol) + nrow) ;
        if ( kd < j) kd = j ;
        /* (MAX (nrow, ncol) + nrow)*sizeof(double)
                 + (2*ncol + 4*nrow)*sI) */

        /* -> update_Anz */
        j = (ncol+3*nrow) ;
        if ( ki < j ) ki = j ;

        j = nrow ;
        if ( kd < j ) kd = j ;
        /* 2*nrow*sizeof(double) + (ncol+3*nrow)*sI */

        /* -> modrow inside big iteration updates */
        j = nrow ;
        if ( ki < j ) ki = j ;

        j = 4*nrow ;
        if ( kd < j ) kd = j ;
        /* 4*nrow*sizeof(double) + nrow*sI */

        /* -> modrow at start of big iteration */
        j = (nrow+ncol) ;
        if ( ki < j ) ki = j ;

        j = (2*nrow+ncol) ;
        if ( kd < j ) kd = j ;
        /* (2*nrow+ncol)*sizeof(double) + (nrow+ncol)*sI */

        /* -> error check */
        j = ntot ;
        if ( ki < j ) ki = j ;

        j = (3*nrow+ntot) ;
        if ( kd < j ) kd = j ;
        /* (3*nrow+ntot)*sizeof(double) + ntot*sI */

        /* -> line search */
        j = (ntot+1) ;
        if ( ki < j ) ki = j ;

        /* added 1 to make sure that there is enough space for the line
           search in gradprojLP */
        j = (3*nrow+2*ncol+nsingni + 1) ;
        if ( kd < j ) kd = j ;
        /* (3*nrow+2*ncol+ni)*sizeof(double) + (ntot+1)*sI */

        /* -> multilevel implementation */
        if ( Parm->multilevel == TRUE )
        {
            j = (4*nrow+3*ncol) ;
            if ( ki < j ) ki = j ;
        }

        /* workspace needed by CHOLMOD */
        j = 5*nrow ;
        if ( ki < j ) ki = j ;
    }

    /* allocate int work space */
    W->arrayi = (PPINT *) pproj_malloc (&status, ki, sI) ;

    /* allocate double work space */
    W->arrayd = (PPFLOAT *) pproj_malloc (&status, kd, sF) ;

    return (status) ;
}
