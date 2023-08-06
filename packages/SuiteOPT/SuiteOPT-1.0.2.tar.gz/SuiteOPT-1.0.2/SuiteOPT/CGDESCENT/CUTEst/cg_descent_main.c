/* ====================================================
 * CUTEst interface for cg_descent       May 1, 2018
 *
 * W. Hager
 *
 * (Based on CUTEr gencma.c of D. Orban, Feb 3, 2003)
 * (CUTEst evolution, Nick Gould, Apr 2, 2014)
 * ====================================================
 */

/* macros */
#define CG_DESCENTMA

#define MAXLINE 256

#ifdef __cplusplus
extern "C" {   /* To prevent C++ compilers from mangling symbols */
#endif

#include "cutest.h"
#include "cg_descent.h"

#ifdef Isg95
#define MAINENTRY MAIN_
#else
#define MAINENTRY main
#endif

/* prototypes */
void cg_hess
(
    CGhess *Hess
) ;

void cg_value
(
    CGFLOAT *f,
    CGFLOAT *x,
    CGINT    n
) ;

void cg_grad
(
    CGFLOAT  *g,
    CGFLOAT  *x,
    CGINT     n
) ;

void cg_valgrad
(
    CGFLOAT  *f,
    CGFLOAT  *g,
    CGFLOAT  *x,
    CGINT     n
) ;

void cg_Hprod
(
    CGFLOAT  *Hd, /* Hd = H*d */
    CGFLOAT   *d,
    CGINT      n  /* number of nonzero entries in d */
) ;

void cg_sort_cols
(
    CGINT    *Ap, /* column pointers */
    CGINT    *Ai, /* row indices */
    CGFLOAT  *Ax, /* numerical values */
    CGINT   *atp, /* row pointers for transpose */
    CGINT   *ati, /* column indices for transpose */
    CGFLOAT *atx, /* numerical values for transpose */
    CGINT   nrow, /* number of rows */
    CGINT   ncol  /* number of cols */
) ;

void cg_transpose
(
    CGINT   *Bp,   /* size nrow+1, column pointers (output) */
    CGINT   *Bi,   /* size Ap [ncol], row indices of B (output) */
    CGFLOAT *Bx,   /* size Ap [ncol], numerical entries of B (output) */
    CGINT   *Ap,   /* size ncol+1, column pointers */
    CGINT   *Ai,   /* size Ap [ncol], row indices for A */
    CGFLOAT *Ax,   /* size Ap [ncol], numerical entries of A */
    CGINT  nrow,   /* number of rows in A */
    CGINT  ncol,   /* number of cols in A */
    CGINT    *W    /* work array of size nrow */
) ;

/* global variables */
    integer CUTEst_nvar;        /* number of variables */
    integer CUTEst_ncon;        /* number of constraints */
    integer *h_row, *h_col ;
    integer CUTEst_nnzh ;
    logical cute_true = TRUE_ ;
    logical cute_false = FALSE_ ;
    CGINT *Hi, *Hp ;
    CGFLOAT *Hx, *Qc ;
    CGINT *CGhmap, *HessHi, *HessHp ;
    CGFLOAT *H_val, *HessHx ;

/* main program */
int MAINENTRY( void )
{

    /* wall clock: */
    struct timeval tv ;
    int sec, usec ;
    double walltime ;
    char *fname = "OUTSDIF.d"; /* CUTEst data file */
    integer funit = 42;        /* FORTRAN unit number for OUTSDIF.d */
    integer io_buffer = 11;    /* FORTRAN unit for internal i/o */
    integer iout = 6;          /* FORTRAN unit number for error output */
    integer ierr;              /* Exit flag from OPEN and CLOSE */
    integer status;            /* Exit flag from CUTEst tools */
    char fullpathname [1024] ;
    char *cutest_dir ;

    integer     v_order, nnzh, H_anz,
                ncol ;
    CGFLOAT     *x, *lo, *hi, *zeros ;
    char        qpprob [MAXLINE+1], uprob [MAXLINE+1], *uname, *qpname, *pname ;

    doublereal  calls[7], cpu[2] ;
    integer     ExitCode;
    int         QP, status_cg, U ;
    CGFLOAT     fadjust, s, t ;
    CGINT       Ncol, row, col, i, j, k,
                *H_row, *H_col, *Hpp ;
#ifndef NDEBUG
    CGFLOAT     *g, *prod, *tempx ;
#endif

    FILE *QPfile, *Ufile ;

    Qc = NULL ;

    /* Open problem description file OUTSDIF.d */
    ierr = 0;
    FORTRAN_open( &funit, fname, &ierr ) ;
    if( ierr )
    {
        printf("Error opening file OUTSDIF.d.\nAborting.\n") ;
        exit(1) ;
    }

    /* --- Setup for unconstrained problem ---------- */
    printf ("Initializing CGdata structure.\n") ;
    CGdata *cgdata = cg_setup () ;
    if ( cgdata == NULL )
    {
            cg_error (-1, __FILE__, __LINE__, "cg_setup failed") ;
    }
    else
    {
        printf ("Successfully initialized CGdata structure.\n") ;
    }
    CGparm *cgparm = cgdata->Parm ;
    CGstat *Stat = cgdata->Stat ;

    /* Determine problem size */
    CUTEST_udimen( &status, &funit, &CUTEst_nvar) ;
    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
    ncol = CUTEst_nvar ; /* integer */
    Ncol = ncol ;        /* CGINT */

    /* v_order determines order of lin and nonlin variables */
    /* if v_order  = 1 then lin come before nonlin */
    /* if v_order  = 2 then nonlin come before lin */
    /* if v_order != 1 or 2 then order does not matter */
    v_order = 2 ;

    /* Reserve memory for variables, bounds, and multipliers */
    /* and call appropriate initialization routine for CUTEst */
    x =      (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
    lo =     (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
    hi =     (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
    CUTEST_usetup ( &status, &funit, &iout, &io_buffer, &ncol, x, lo, hi ) ;

    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }

    /* Store zero in an array named zeros, it is used below. */
    zeros = (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
    cg_initx (zeros, CGZERO, Ncol) ;

    /* Get problem name */
    pname = (char *) malloc ((FSTRING_LEN+1)*sizeof (char)) ;
    CUTEST_probname( &status, pname ) ;
    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
        exit(status) ;
    }

    /* Make sure to null-terminate problem name */
    pname[FSTRING_LEN] = '\0';
    i = FSTRING_LEN - 1;
    while(i-- > 0 && pname[i] == ' ')
    {
        pname[i] = '\0';
    }

    /* Print problem name */
    printf ("\n Problem: %s (n = %ld)\n", pname, (LONG) Ncol ) ;

    /* read the full path to the pasa/CUTEst directory and store it in the
       variable cutest_dir */
#include ".cutest_location"

    /* See if the problem is in the list of unconstrained problem.
       If not, then terminate with an error message. */
    strcpy (fullpathname, cutest_dir) ;
    Ufile = fopen (strcat (fullpathname, "/classU"), "r") ;
    U = FALSE ;
    while (fgets (uprob, MAXLINE, Ufile) != (char *) NULL)
    {
        for (uname = uprob; *uname; uname++)
        {
            if (isspace (*uname)) *uname = '\0' ;
        }
        uname = uprob ;
        if ( strcmp (uname, pname) == 0 )
        {
            U = TRUE ;
            break ;
        }
    }

    if ( U == FALSE )
    {
        printf ("Problem %s was not found in the list of "
                "unconstrained problems in the file %s\n",
                pname, strcat (fullpathname, "/classU")) ;
        printf ("Either the problem is constrained, or the file should be "
                "updated to include this new unconstrained problem.\n") ;
        cg_error (-1, __FILE__, __LINE__, "STOP") ;
    }

    /* see if the problem has a quadratic objective by comparing the name
       pname of the test problem to the names qpprob of the unconstrained
       QPs contained in the file classQPU */
    strcpy (fullpathname, cutest_dir) ;
    QPfile = fopen (strcat (fullpathname, "/classUQP"), "r") ;
    QP = FALSE ;
    while (fgets (qpprob, MAXLINE, QPfile) != (char *) NULL)
    {
        for (qpname = qpprob; *qpname; qpname++)
        {
            if (isspace (*qpname)) *qpname = '\0' ;
        }
        qpname = qpprob ;
        if ( strcmp (qpname, pname) == 0 )
        {
            QP = TRUE ;
            break ;
        }
    }


    /* If the problem has a quadratic objective, then extract the
       Hessian matrix and the linear term in the objective. */
    if ( QP == TRUE )
    {
        printf ("the problem has a quadratic objective\n") ;
        /* nnzh = the number of nonzeros required to store the sparse Hessian 
           matrix in coordinate format */
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status);
        }

        /* Reserve memory for H_val, H_row, H_col */
        CUTEST_udimsh ( &status, &nnzh );
        H_val = (CGFLOAT *) malloc (nnzh*sizeof (CGFLOAT)) ;
        H_row = (CGINT *)   malloc (nnzh*sizeof (CGINT)) ;
        H_col = (CGINT *)   malloc (nnzh*sizeof (CGINT)) ;
        h_row = (integer *) malloc (nnzh*sizeof (integer)) ;
        h_col = (integer *) malloc (nnzh*sizeof (integer)) ;

        /* Determine the nonzero values in the Hessian */
        CUTEST_ush ( &status, &ncol, zeros, &H_anz, &nnzh, H_val, h_row, h_col);

        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }
        if ( nnzh != H_anz )
        {
            printf ("nnzh (%ld) != H_anz (%ld)\n", (LONG) nnzh, (LONG) H_anz) ;
            cg_error (-1, __FILE__, __LINE__, "STOP") ;
        }

        for (i = 0; i < H_anz; i++)
        {
            H_row [i] = h_row [i] ;
            H_col [i] = h_col [i] ;
        }

        /* Determine number of nonzero values in the Hessian and the
           column counts. */
        Hp = (CGINT *) malloc ((Ncol+1)*sizeof (CGINT)) ;
        cg_initi (Hp, 0, Ncol+1) ;
        Hpp = Hp+1 ;
        k = 0 ;
        for (i = 0 ; i < nnzh; i++)
        {
            if ( H_val [i] != CGZERO )
            {
                k++ ;
                H_row [i]-- ;
                row = H_row [i] ;
                H_col [i]-- ;
                col = H_col [i] ;
                Hpp [col]++ ;
                if ( row != col )
                {
                    k++ ;
                    Hpp [row]++ ;
                    if ( row > col )
                    {
                        cg_error (-1, __FILE__, __LINE__,
                                      "problem has unsymmetric Hessian") ;
                    }
                }
            }
        }
        for (j = 1; j <= ncol; j++)
        {
            Hp [j] += Hp [j-1] ;
        }

        Hi = (CGINT *)   malloc (k*sizeof (CGINT)) ;
        Hx = (CGFLOAT *) malloc (k*sizeof (CGFLOAT)) ;

        for (i = 0 ; i < nnzh; i++)
        {
            if ( H_val [i] != CGZERO )
            {
                row = H_row [i] ;
                col = H_col [i] ;
                k = Hp [col] ;
                Hi [k] = row ;
                t = H_val [i] ;
                Hx [k] = t ;
                Hp [col]++ ;
                if ( row != col )
                {
                    k = Hp [row] ;
                    Hi [k] = col ;
                    Hx [k] = t ;
                    Hp [row]++ ;
                }
            }
        }
        for (i = ncol; i > 0; i--)
        {
            Hp [i] = Hp [i-1] ;
        }
        Hp [0] = 0 ;

        /* perform double transpose to ensure that the row indices of H
           are sorted in each column */
        cg_sort_cols (Hp, Hi, Hx, NULL, NULL, NULL, Ncol, Ncol) ;

        /* Determine c in objective function */
        Qc = (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
        CUTEST_uofg (&status, &ncol, zeros, &fadjust, Qc, &cute_true);

#ifndef NDEBUG
        tempx = (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
        for (j = 0; j < ncol; j++)
        {
                tempx [j] = 1 + (j % 10) ;
        }
        cg_value (&s, tempx, Ncol) ;
        prod = (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
        cg_Hprod (prod, tempx, Ncol) ;
        t = cg_dot (prod, tempx, Ncol) ;
        t = 0.5*t + cg_dot (tempx, Qc, Ncol) ;
        t += fadjust ;
        if ( s != 0 )
        {
            printf ("cost: %e cost error: %e relative error: %e\n",
                     s, fabs(s-t), fabs((s-t)/s)) ;
            if ( fabs((s-t)/s) > 1.e-8 )
            {
                cg_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else
        {
            printf ("cost: %e cost error: %e\n", s, fabs(s-t)) ;
        }

        g = (CGFLOAT *) malloc (Ncol*sizeof (CGFLOAT)) ;
        cg_grad (g, tempx, Ncol) ;
        cg_step (prod, prod, Qc, CGONE, Ncol) ;
        t = CGZERO ;
        s = CGZERO ;
        for (j = 0; j < Ncol; j++)
        {
            t += fabs (g [j] - prod [j]) ;
            s += fabs (g [j]) ;
        }
        if ( s != 0 )
        {
            printf ("grad: %e grad error: %e relative error: %e\n",
                     s, t, t/s) ;
            if ( t/s > 1.e-8 )
            {
                cg_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else
        {
            printf ("grad: %e grad error: %e\n", s, t) ;
        }

        free (prod) ;
        free (tempx) ;
        free (g) ;
#endif
    }
    else /* the matrix is not quadratic, prepare for evaluation of Hessian */
    {
        /* Reserve memory for H_val, H_row, H_col */
        CUTEST_udimsh ( &status, &CUTEst_nnzh ) ;
        H_val = (CGFLOAT *) malloc (CUTEst_nnzh*sizeof (CGFLOAT)) ;
        H_row = (CGINT *)   malloc (CUTEst_nnzh*sizeof (CGINT)) ;
        H_col = (CGINT *)   malloc (CUTEst_nnzh*sizeof (CGINT)) ;
        h_row = (integer *) malloc (CUTEst_nnzh*sizeof (integer)) ;
        h_col = (integer *) malloc (CUTEst_nnzh*sizeof (integer)) ;

       /* CUTEst_nnzh = the number of nonzeros required to store the
          sparse Hessian matrix in coordinate format */
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status);
        }

        /* Determine the nonzero values in the Hessian */
        CUTEST_ush ( &status, &ncol, zeros, &H_anz, &CUTEst_nnzh,
                      H_val, h_row, h_col ) ;
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }
        if ( CUTEst_nnzh != H_anz )
        {
            printf ("nnzh (%ld) != H_anz (%ld)\n",
                    (LONG) CUTEst_nnzh, (LONG) H_anz) ;
            cg_error (-1, __FILE__, __LINE__, "STOP") ;
        }
        for (i = 0; i < H_anz; i++)
        {
            H_row [i] = h_row [i] ;
            H_col [i] = h_col [i] ;
        }

        /* Determine the column counts */
        HessHp = (CGINT *) malloc ((Ncol+1)*sizeof (CGINT)) ;
        cg_initi (HessHp, 0, Ncol+1) ;
        Hpp = HessHp+1 ;
        nnzh = 0 ;
        for (i = 0; i < CUTEst_nnzh; i++)
        {
            nnzh++ ;
            H_row [i]-- ;
            row = H_row [i] ;
            H_col [i]-- ;
            col = H_col [i] ;
            Hpp [col]++ ;
            if ( row != col )
            {
                nnzh++ ;
                Hpp [row]++ ;
                if ( row > col )
                {
                    cg_error (-1, __FILE__, __LINE__,
                                  "problem has unsymmetric Hessian") ;
                }
            }
        }
        /* nnzh is the total number of nonzeros in the full matrix, not
           just the upper triangle, and HessHp gives column pointers for
           the full matrix */

        for (j = 1; j <= ncol; j++)
        {
            HessHp [j] += HessHp [j-1] ;
        }

        HessHi = (CGINT *) malloc (nnzh*sizeof (CGINT)) ;
        HessHx = (CGFLOAT *) malloc (nnzh*sizeof (CGFLOAT)) ;

        for (i = 0 ; i < CUTEst_nnzh; i++)
        {
            row = H_row [i] ;
            col = H_col [i] ;
            k = HessHp [col] ;
            HessHi [k] = row ;
            HessHx [k] = (CGFLOAT) i ;
            HessHp [col]++ ;
            if ( row != col )
            {
                k = HessHp [row] ;
                HessHi [k] = col ;
                HessHx [k] = (CGFLOAT) i ;
                HessHp [row]++ ;
            }
        }
        for (i = ncol; i > 0; i--)
        {
            HessHp [i] = HessHp [i-1] ;
        }
        HessHp [0] = 0 ;

        /* perform double transpose to ensure that the row indices of H
           are sorted in each column */
        cg_sort_cols (HessHp, HessHi, HessHx, NULL, NULL, NULL, Ncol, Ncol) ;
        CGhmap = malloc (nnzh*sizeof (CGINT)) ;
        for (i = 0; i < nnzh; i++)
        {
            /* store the location in H_val of Hx [i] */
            CGhmap [i] = (CGINT) HessHx [i] ;
        }
    }

    if ( QP == TRUE )
    {
        cgparm->fadjust  = fadjust ;
        cgdata->c = Qc ;
        cgdata->hprod = cg_Hprod ;
    }

    /* setup the cgdata structure */
    cgdata->x = x ;
    cgdata->n = Ncol ;
    cgdata->value = cg_value ;
    cgdata->grad = cg_grad ;
    cgdata->valgrad = cg_valgrad ;
    cgdata->hess= cg_hess ;

    /* set new parameter values for CG here, otherwise default values are used*/

    /* cgparm->grad_tol = 1.e-8 ; */ /* default is 1.e-6 */ ;

    /* Call the optimizer */

    /* time run using wall clock, call several times to exclude startup cost */
    gettimeofday (&tv, NULL) ;
    sec = tv.tv_sec ;
    usec = tv.tv_usec ;
    gettimeofday (&tv, NULL) ;
    walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;
    printf ("walltime start cost: %12.6f\n\n", walltime) ;

    gettimeofday (&tv, NULL) ;
    sec = tv.tv_sec ;
    usec = tv.tv_usec ;

    status_cg = cg_descent (cgdata) ;

    gettimeofday (&tv, NULL) ;
    walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;

    ExitCode = 0;

    /* Get CUTEst statistics */
    /* CUTEST_ureport( &status, calls, cpu) ;*/
    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
        exit(status) ;
    }

    /* print unformatted cg_descent statistics */
    printf ("!!%10s %6ld %7ld %7ld %7ld %5i %16.7e %16.7e %11.6f\n",
             pname, (LONG) Ncol, (LONG) Stat->iter, (LONG) Stat->nfunc,
            (LONG) Stat->ngrad, status_cg, Stat->err, Stat->f, walltime) ;

    /* print run status */
    cg_print_status (cgdata) ;

    printf("\n\n *********************** CG statistics **************"
           "**********\n\n") ;
    printf("Code used                 : cg_descent\n") ;
    printf("Problem                   : %-s\n", pname) ;
    printf("# variables               = %-10ld\n\n",
          (LONG) Ncol) ;
    printf("# cg iterations           = %-10ld\n\n",
          (LONG) Stat->iter) ;
    printf("# cg function evals       = %-10ld\n\n",
          (LONG) Stat->nfunc) ;
    printf("# cg gradient evals       = %-10ld\n\n",
          (LONG) Stat->ngrad) ;
    printf("|| g ||                   = %-16.7e\n", Stat->err) ;
    printf("Final f                   = %-16.7e\n", Stat->f) ;
    cg_value (&t, x, CUTEst_nvar) ;
    printf("Function value at final x = %-16.7e\n", t) ;
    printf("Solve time                = %-11.6f seconds\n", walltime) ;
    printf("\n ***********************************************************"
           "*******\n\n") ;

    /* Print lines to clearly separate problems */

    printf (" ====================================================\n\n" ) ;

    ierr = 0;
    FORTRAN_close( &funit, &ierr ) ;
    if ( ierr )
    {
        printf( "Error closing %s on unit %ld.\n", fname, (LONG) funit ) ;
        printf( "Trying not to abort.\n" ) ;
    }

    /* Free workspace */
    free (zeros) ;
    free (pname) ;
    free (x) ;
    free (lo) ;
    free (hi) ;
    free (H_val) ;
    free (H_row) ;
    free (H_col) ;
    free (h_row) ;
    free (h_col) ;
    if ( QP == TRUE )
    {
        free (Hx) ;
        free (Hi) ;
        free (Hp) ;
        free (Qc) ;
    }
    else /* not a quadratic, free Hessian workspace */
    {
        free (HessHp) ;
        free (HessHi) ;
        free (HessHx) ;
        free (CGhmap) ;
    }

    cg_terminate (&cgdata) ;

    /* end cutest */
    CUTEST_uterminate( &status ) ;

    /* close files */
    fclose(QPfile) ;
    fclose(Ufile) ;

    return 0;
}

#ifdef __cplusplus
}    /* Closing brace for  extern "C"  block */
#endif
void cg_hess
(
    CGhess *Hess
)
{
    CGINT i, N ;
    CGFLOAT *x ;
    integer n, H_anz, iprob, nnzh, status ;

    N = Hess->ncol ;
    n = N ;
    x = Hess->x ;
    Hess->Hp = HessHp ;
    Hess->Hi = HessHi ;
    Hess->Hx = HessHx ;
    nnzh = HessHp [N] ;
    iprob = 0 ;
    CUTEST_ush ( &status, &n, x, &H_anz, &CUTEst_nnzh, H_val, h_row, h_col) ;

    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }

    for (i = 0; i < nnzh; i++)
    {
        Hess->Hx [i] = H_val [CGhmap [i]] ;
    }
    return ;
}
void cg_value
(
    CGFLOAT *f,
    CGFLOAT *x,
    CGINT N
)
{
    integer status, n ;

    n = N ;
    CUTEST_ufn( &status, &n, x, f) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
        exit(status) ;
    }
/*printf ("function value: %e\n", *f) ;*/
    return ;
}

void cg_grad
(
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT N
)
{
    integer n, status;
    n = N ;
    CUTEST_ugr ( &status, &n, x, g) ;
/*printx (g, n, "user gradient") ;*/
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
}

void cg_valgrad
(
    CGFLOAT *f,
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT N
)
{
    integer n, status;
    n = N ;
    CUTEST_uofg( &status, &n, x, f, g, &cute_true) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
/*printf ("function value in valgrad: %e\n", *f) ;*/
    return ;
}

void cg_Hprod
(
    CGFLOAT     *Hd, /* Hd = H*d */
    CGFLOAT      *d,
    CGINT         n  /* number of nonzero entries in d */
)
{
    CGINT j, p, q ;
    CGFLOAT t ;
    cg_initx (Hd, CGZERO, n) ;
    for (j = 0; j < n; j++)
    {
        t = d [j] ;
        if ( t ) /* if t != 0 */
        {
            q = Hp [j+1] ;
            for (p = Hp [j]; p < q; p++)
            {
                Hd [Hi [p]] += t*Hx [p] ;
            }
        }
    }
}

/* perform double transpose to sort row indices in each column of matrix */
void cg_sort_cols
(
    CGINT    *Ap, /* column pointers */
    CGINT    *Ai, /* row indices */
    CGFLOAT  *Ax, /* numerical values */
    CGINT   *atp, /* row pointers for transpose */
    CGINT   *ati, /* column indices for transpose */
    CGFLOAT *atx, /* numerical values for transpose */
    CGINT   nrow, /* number of rows */
    CGINT   ncol  /* number of cols */
)
{
    CGINT *ATp, *ATi, *temp ;
    CGFLOAT *ATx ;
    ATp = atp ;
    ATi = ati ;
    ATx = atx ;
    if ( atp == NULL )
    {
        ATp = (CGINT *) malloc ((nrow+1)*sizeof (CGINT)) ;
        ATi = (CGINT *) malloc (Ap [ncol]*sizeof (CGINT)) ;
        ATx = (CGFLOAT *) malloc (Ap [ncol]*sizeof (CGFLOAT)) ;
    }
    temp = (CGINT *) malloc (CGMAX (nrow, ncol)*sizeof (CGINT)) ;
    cg_transpose (ATp, ATi, ATx, Ap, Ai, Ax, nrow, ncol, temp) ;
    cg_transpose (Ap, Ai, Ax, ATp, ATi, ATx, ncol, nrow, temp) ;
    if ( atp == NULL )
    {
        free (ATp) ;
        free (ATi) ;
        free (ATx) ;
    }
    free (temp) ;
}

/* ========================================================================== */
/* === cg_transpose ========================================================= */
/* ========================================================================== */
/*    Transpose a sparse matrix: B = A' */
/* ========================================================================== */

void cg_transpose
(
    CGINT   *Bp,   /* size nrow+1, column pointers (output) */
    CGINT   *Bi,   /* size Ap [ncol], row indices of B (output) */
    CGFLOAT *Bx,   /* size Ap [ncol], numerical entries of B (output) */
    CGINT   *Ap,   /* size ncol+1, column pointers */
    CGINT   *Ai,   /* size Ap [ncol], row indices for A */
    CGFLOAT *Ax,   /* size Ap [ncol], numerical entries of A */
    CGINT  nrow,   /* number of rows in A */
    CGINT  ncol,   /* number of cols in A */
    CGINT    *W    /* work array of size nrow */
)
{
    CGINT i, j, p, q, pp ;

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
