/* ====================================================
 * CUTEst interface for pasa             August 1, 2016
 *
 * W. Hager
 *
 * (Based on CUTEr gencma.c of D. Orban, Feb 3, 2003)
 * (CUTEst evolution, Nick Gould, Apr 2, 2014)
 * ====================================================
 */

/* macros */
#define PASAMA

#define MAXLINE 256

#ifdef __cplusplus
extern "C" {   /* To prevent C++ compilers from mangling symbols */
#endif

#include "cutest.h"
#include "pasa.h"

#ifdef Isg95
#define MAINENTRY MAIN_
#else
#define MAINENTRY main
#endif

/* prototypes */
void pasa_errLP0
(
    PASAFLOAT *lambda,
    PASAINT      nrow,
    PASAINT      ncol,
    PASAFLOAT      *x,
    PASAFLOAT      *c,
    PASAFLOAT     *lo,
    PASAFLOAT     *hi,
    PASAFLOAT     *bl,
    PASAFLOAT     *bu,
    PASAINT       *Ap,
    PASAINT       *Ai,
    PASAFLOAT     *Ax,
    int    PrintLevel
) ;

void sort_cols
(
    PASAINT    *Ap, /* column pointers */
    PASAINT    *Ai, /* row indices */
    PASAFLOAT  *Ax, /* numerical values */
    PASAINT   *atp, /* row pointers for transpose */
    PASAINT   *ati, /* column indices for transpose */
    PASAFLOAT *atx, /* numerical values for transpose */
    PASAINT   nrow, /* number of rows */
    PASAINT   ncol  /* number of cols */
) ;

/* evaluation routine prototypes for unconstrained problems */
void cg_hess
(
    CGhess *Hess
) ;

void cg_value
(
    PASAFLOAT *f,
    PASAFLOAT *x,
    PASAINT    n
) ;

void cg_grad
(
    PASAFLOAT  *g,
    PASAFLOAT  *x,
    PASAINT     n
) ;

void cg_valgrad
(
    PASAFLOAT  *f,
    PASAFLOAT  *g,
    PASAFLOAT  *x,
    PASAINT     n
) ;

void cg_Hprod
(
    PASAFLOAT     *Hd, /* Hd = H*d */
    PASAFLOAT      *d,
    PASAINT         n  /* number of nonzero entries in d */
) ;

/* evaluation routine prototypes for constrained problems */
void pasa_hess
(
    PASAhess *Hess
) ;

void pasa_value
(
    PASAFLOAT *f,
    PASAFLOAT *x,
    PASAINT    n
) ;

void pasa_grad
(
    PASAFLOAT  *g,
    PASAFLOAT  *x,
    PASAINT     n
) ;

void pasa_valgrad
(
    PASAFLOAT  *f,
    PASAFLOAT  *g,
    PASAFLOAT  *x,
    PASAINT     n
) ;

void pasa_Hprod
(
    PASAFLOAT  *Hd, /* Hd = H*d */
    PASAFLOAT   *d,
    PASAINT *ifree,
    PASAINT      m, /* dimension of H */
    PASAINT      n  /* number of nonzero entries in d */
) ;


/* global variables */
    integer CUTEst_nvar;        /* number of variables */
    integer CUTEst_ncon;        /* number of constraints */
    integer *h_row, *h_col ;
    integer CUTEst_nnzh ;
    logical cute_true = TRUE_ ;
    logical cute_false = FALSE_ ;
    PASAINT *Hi, *Hp ;
    PASAFLOAT *Hx, *Qc ;
    PASAINT *PASAhmap, *HessHi, *HessHp ;
    PASAFLOAT *H_val, *HessHx ;

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

    VarTypes vtypes;

    integer     e_order, l_order, v_order, nnzj, nnzh, anz, lj1, lj2, H_anz,
                nrow, ncol, loExists, hiExists, *j_row, *j_col ;
    integer     iprob = 0 ;
    PASAFLOAT   *x, *xcopy, *lo, *hi, *lambda, *offset, *c, *bl, *bu, *Ax, *ATx,
                *J_val, *zeros ;
    char        qpprob [MAXLINE+1], *qpname, lpprob [MAXLINE+1], *lpname,
                uprob [MAXLINE+1], *uname, *pname ;
    logical     *equatn, *linear ;

    doublereal  calls[7], cpu[2] ;
    integer     ExitCode;
    int         LP, QP, UNC, status_pasa, status_cg ;
    PASAFLOAT   fadjust, s, t, *HTx ;
    PASAINT     Nrow, Ncol, row, col, free_cols, free_rows, i, j, k, l, p, q,
                *Ap, *Ai, *ATp, *ATi,
                *drop_col, *drop_row, *ifree, *J_col, *J_row,
                *H_row, *H_col, *HTi, *HTp, *Hpp, *temp ;
#ifndef NDEBUG
    PASAFLOAT   *g, *prod, *tempx ;
#endif

    FILE *spec, *LPfile, *QPfile, *Ufile ;
    PASAstat  *pasastat ;  /* statistics for PASA */
    CGstat      *cgstat ;  /* statistics for CG */
    PPstat   *pprojstat ;  /* statistics for PPROJ */
    NAPstat    *napstat ;  /* statistics for NAPHEAP */
    PASAparm  *pasaparm ;  /* parameters for PASA */
    CGparm      *cgparm ;  /* parameters for CG */
    NAPparm    *napparm ;  /* parameters for NAPHEAP */
    PPparm   *pprojparm ;  /* parameters for PPROJ */
    PASAdata  *pasadata ;  /* data structure for pasa input */

    /* --- Initialize indicators for problem types ------ */
    LP = FALSE ;
    QP = FALSE ;
    UNC = FALSE ;

    H_val = NULL ;
    H_row = NULL ;
    H_col = NULL ;
    h_row = NULL ;
    h_col = NULL ;
    c     = NULL ;
    Qc = NULL ;

    /* Open problem description file OUTSDIF.d */
    ierr = 0;
    FORTRAN_open( &funit, fname, &ierr ) ;
    if( ierr )
    {
        printf("Error opening file OUTSDIF.d.\nAborting.\n") ;
        exit(1) ;
    }

    /* Get problem name */
    pname = (char *) malloc ((FSTRING_LEN+1)*sizeof (char)) ;
    CUTEST_pname( &status, &funit, pname ) ;
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
    printf ("\n Problem: %s\n", pname) ;

    /* read the full path to the pasa/CUTEst directory and store it in the
       variable cutest_dir */
#include ".cutest_location"

    /* If the problem is unconstrained, use CUTEst unconstrained functions.
       CUTEst stores the unconstrained and constrained problems in different
       format and there are different tools for handling each format. */
    strcpy (fullpathname, cutest_dir) ;
    Ufile = fopen (strcat (fullpathname, "/classU"), "r") ;
    while (fgets (uprob, MAXLINE, Ufile) != (char *) NULL)
    {
        for (uname = uprob; *uname; uname++)
        {
            if (isspace (*uname)) *uname = '\0' ;
        }
        uname = uprob ;

        if ( strcmp (uname, pname) == 0 )
        {
            /* Indicate problem type */
            UNC = TRUE ;
            /* Exit while loop */
            break ;
        }
    }
    fclose(Ufile) ;

    /* --- Import problem data from CUTEst -------------- */
    if (UNC == TRUE)
    {
        CGdata *cgdata = cg_setup () ;
        CGstat *cgstat = cgdata->Stat ;
        cgparm = cgdata->Parm ;

        /* Setup for unconstrained problem
           see if the problem has a quadratic objective by comparing the name
           pname of the test problem to the names qpprob of the unconstrained
           QPs contained in the file classQPU */
        strcpy (fullpathname, cutest_dir) ;
        QPfile = fopen (strcat (fullpathname, "/classQP"), "r") ;
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
        fclose (QPfile) ;

        /* Determine problem size */
        CUTEST_udimen( &status, &funit, &CUTEst_nvar) ;
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
            exit(status);
        }
        ncol = CUTEst_nvar ; /* integer */
        Ncol = ncol ;        /* PASAINT */

        /* v_order determines order of lin and nonlin variables */
        /* if v_order  = 1 then lin come before nonlin */
        /* if v_order  = 2 then nonlin come before lin */
        /* if v_order != 1 or 2 then order does not matter */
        v_order = 2 ;

        /* Reserve memory for variables, bounds, and multipliers */
        /* and call appropriate initialization routine for CUTEst */
        x =      (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        lo =     (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        hi =     (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        CUTEST_usetup ( &status, &funit, &iout, &io_buffer, &ncol, x, lo, hi ) ;
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
            exit(status);
        }

        /* Store zero in an array named zeros, it is used below. */
        zeros = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        pasa_initx (zeros, PASAZERO, Ncol) ;

        /* If the problem has a quadratic objective, then extract the
           Hessian matrix and the linear term in the objective. */
        if ( QP == TRUE )
        {
            printf ("unconstrained problem has a quadratic objective\n") ;

            /* nnzh = the number of nonzeros required to store the sparse  
               Hessian matrix in coordinate format */
            CUTEST_udimsh ( &status, &nnzh );
            if (status)
            {
                printf("** CUTEst error, status = %ld, aborting\n", 
                       (LONG) status) ;
                exit(status);
            }
    
            /* Reserve memory for H_val, H_row, H_col */
            H_val = (PASAFLOAT *) malloc (nnzh*sizeof (PASAFLOAT)) ;
            H_row = (PASAINT *)   malloc (nnzh*sizeof (PASAINT)) ;
            H_col = (PASAINT *)   malloc (nnzh*sizeof (PASAINT)) ;
            h_row = (integer *) malloc (nnzh*sizeof (integer)) ;
            h_col = (integer *) malloc (nnzh*sizeof (integer)) ;
    
            /* Determine the nonzero values in the Hessian */
            CUTEST_ush ( &status, &ncol, zeros, &H_anz, &nnzh, 
                         H_val, h_row, h_col);
    
            if (status)
            {
                printf("** CUTEst error, status = %ld, aborting\n", 
                       (LONG) status) ;
                exit(status) ;
            }
            if ( nnzh != H_anz )
            {
                printf ("nnzh (%ld) != H_anz (%ld)\n", 
                        (LONG) nnzh, (LONG) H_anz) ;
                pasa_error (-1, __FILE__, __LINE__, "STOP") ;
            }
    
            for (i = 0; i < H_anz; i++)
            {
                H_row [i] = h_row [i] ;
                H_col [i] = h_col [i] ;
            }
    
            /* Determine number of nonzero values in the Hessian and the
               column counts. */
            Hp = (PASAINT *) malloc ((Ncol+1)*sizeof (PASAINT)) ;
            pasa_initi (Hp, 0, Ncol+1) ;
            Hpp = Hp+1 ;
            k = 0 ;
            for (i = 0 ; i < nnzh; i++)
            {
                if ( H_val [i] != PASAZERO )
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
                            pasa_error (-1, __FILE__, __LINE__,
                                          "problem has unsymmetric Hessian") ;
                        }
                    }
                }
            }
            for (j = 1; j <= ncol; j++)
            {
                Hp [j] += Hp [j-1] ;
            }
    
            Hi = (PASAINT *)   malloc (k*sizeof (PASAINT)) ;
            Hx = (PASAFLOAT *) malloc (k*sizeof (PASAFLOAT)) ;
    
            for (i = 0 ; i < nnzh; i++)
            {
                if ( H_val [i] != PASAZERO )
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
            sort_cols (Hp, Hi, Hx, NULL, NULL, NULL, Ncol, Ncol) ;
    
            /* Determine c in objective function */
            c = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
            CUTEST_uofg (&status, &ncol, zeros, &fadjust, c, &cute_true);
    
#ifndef NDEBUG
            tempx = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
            for (j = 0; j < ncol; j++)
            {
                    tempx [j] = 1 + (j % 10) ;
            }
            cg_value (&s, tempx, Ncol) ;
            prod = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
            /* p and i not taking on needed values; required to call function */
            cg_Hprod (prod, tempx, Ncol) ; 
            t = pasa_dot (prod, tempx, Ncol) ;
            t = 0.5*t + pasa_dot (tempx, c, Ncol) ;
            t += fadjust ;
            printf ("quad cost: %e\n", t) ;
            if ( s != 0 )
            {
                printf ("cost: %e cost error: %e relative error: %e\n",
                         s, fabs(s-t), fabs((s-t)/s)) ;
                if ( fabs((s-t)/s) > 1.e-8 )
                {
                    pasa_error (-1, __FILE__, __LINE__, "stop") ;
                }
            }
            else
            {
                printf ("cost: %e cost error: %e\n", s, fabs(s-t)) ;
            }
    
            g = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
            cg_grad (g, tempx, Ncol) ;
            pasa_step (prod, prod, c, PASAONE, Ncol) ;
            t = PASAZERO ;
            s = PASAZERO ;
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
                    pasa_error (-1, __FILE__, __LINE__, "stop") ;
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
        else /* the matrix is not quadratic, prepare for evaluation of Hessian*/
        {
            /* Reserve memory for H_val, H_row, H_col */
            CUTEST_udimsh ( &status, &CUTEst_nnzh ) ;
            if (status)
            {
                printf("** CUTEst error, status = %ld, aborting\n",
                       (LONG) status) ;
                exit(status);
            }

            /* CUTEst_nnzh = the number of nonzeros required to store the
               sparse Hessian matrix in coordinate format */
            H_val = (PASAFLOAT *) malloc (CUTEst_nnzh*sizeof (PASAFLOAT)) ;
            H_row = (PASAINT *)   malloc (CUTEst_nnzh*sizeof (PASAINT)) ;
            H_col = (PASAINT *)   malloc (CUTEst_nnzh*sizeof (PASAINT)) ;
            h_row = (integer *) malloc (CUTEst_nnzh*sizeof (integer)) ;
            h_col = (integer *) malloc (CUTEst_nnzh*sizeof (integer)) ;
    
            /* Determine the nonzero values in the Hessian */
            CUTEST_ush ( &status, &ncol, zeros, &H_anz, &CUTEst_nnzh,
                          H_val, h_row, h_col ) ;
            if (status)
            {
                printf("** CUTEst error, status = %ld, aborting\n",
                       (LONG) status) ;
                exit(status) ;
            }
            if ( CUTEst_nnzh != H_anz )
            {
                printf ("nnzh (%ld) != H_anz (%ld)\n",
                        (LONG) CUTEst_nnzh, (LONG) H_anz) ;
                pasa_error (-1, __FILE__, __LINE__, "STOP") ;
            }
            for (i = 0; i < H_anz; i++)
            {
                H_row [i] = h_row [i] ;
                H_col [i] = h_col [i] ;
            }
    
            /* Determine the column counts */
            HessHp = (PASAINT *) malloc ((Ncol+1)*sizeof (PASAINT)) ;
            pasa_initi (HessHp, 0, Ncol+1) ;
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
                        pasa_error (-1, __FILE__, __LINE__,
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
    
            HessHi = (PASAINT *) malloc (nnzh*sizeof (PASAINT)) ;
            HessHx = (PASAFLOAT *) malloc (nnzh*sizeof (PASAFLOAT)) ;
    
            for (i = 0 ; i < CUTEst_nnzh; i++)
            {
                row = H_row [i] ;
                col = H_col [i] ;
                k = HessHp [col] ;
                HessHi [k] = row ;
                HessHx [k] = (PASAFLOAT) i ;
                HessHp [col]++ ;
                if ( row != col )
                {
                    k = HessHp [row] ;
                    HessHi [k] = col ;
                    HessHx [k] = (PASAFLOAT) i ;
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
            sort_cols (HessHp, HessHi, HessHx, NULL, NULL, NULL, Ncol, Ncol) ;
            PASAhmap = malloc (nnzh*sizeof (PASAINT)) ;
            for (i = 0; i < nnzh; i++)
            {
                /* store the location in H_val of Hx [i] */
                PASAhmap [i] = (PASAINT) HessHx [i] ;
            }
        }

        if ( QP == TRUE )
        {
            cgparm->fadjust = fadjust ;
            cgdata->c = c ;
            cgdata->hprod = cg_Hprod ;
        }

        /* setup the cgdata structure */
        cgdata->x       = x ;
        cgdata->n       = Ncol ;
        cgdata->value   = cg_value ;
        cgdata->grad    = cg_grad ;
        cgdata->valgrad = cg_valgrad ;
        cgdata->hess    = cg_hess ;

        /* set new parameter values for cg here,
           otherwise default values are used */
    
        /* cgparm->grad_tol = 1.e-8 ; */ /* default is 1.e-6 */

        /* wall clock, call it several times to eliminate startup cost */
        gettimeofday (&tv, NULL) ;
        sec = tv.tv_sec ;
        usec = tv.tv_usec ;
        gettimeofday (&tv, NULL) ;
        walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;
        printf ("walltime start cost: %12.6f\n", walltime) ;

        gettimeofday (&tv, NULL) ;
        sec = tv.tv_sec ;
        usec = tv.tv_usec ;

        /* Call the optimizer */
        status_cg = cg_descent (cgdata) ;

        gettimeofday (&tv, NULL) ;
        walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;

        ExitCode = 0 ;

        /* Get CUTEst statistics */
        CUTEST_ureport(&status, calls, cpu) ;
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }

        /* print unformatted pasa statistics */
        printf ("!!%10s %6ld %7ld %7ld %7ld %5i %16.7e %16.7e %11.6f\n",
                 pname, (LONG) Ncol, (LONG) cgstat->iter,
                 (LONG) cgstat->nfunc, (LONG) cgstat->ngrad, status_cg,
                 cgstat->err, cgstat->f, walltime) ;
    
        /* print run status */
        cg_print_status (cgdata) ;

        printf("\n\n *********************** CG statistics **************"
               "**********\n\n") ;
        printf("Code used                 : cg_descent\n") ;
        printf("Problem                   : %-s\n", pname) ;
        printf("# variables               = %-10ld\n\n",
              (LONG) Ncol) ;
        printf("# cg iterations           = %-10ld\n\n",
              (LONG) cgstat->iter) ;
        printf("# cg function evals       = %-10ld\n\n",
              (LONG) cgstat->nfunc) ;
        printf("# cg gradient evals       = %-10ld\n\n",
              (LONG) cgstat->ngrad) ;
        printf("|| g ||                   = %-16.7e\n", cgstat->err) ;
        printf("Final f                   = %-16.7e\n", cgstat->f) ;
        cg_value (&t, x, CUTEst_nvar) ;
        printf("Function value at final x = %-16.7e\n", t) ;
        printf("Solve time                = %-11.6f seconds\n", walltime) ;
        printf("\n ***********************************************************"
               "*******\n\n") ;

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
            free (c) ;
        }
        else /* not a quadratic, free Hessian workspace */
        {
            free (HessHp) ;
            free (HessHi) ;
            free (HessHx) ;
            free (PASAhmap) ;
        }
    
        /* end cutest */
        CUTEST_uterminate (&status) ;

        return 0;
    }

    /* --- Setup for constrained problem ---------- */
    printf ("Initializing PASAdata structure.\n") ;
    pasadata = pasa_setup () ;
    if ( pasadata == NULL )
    {
            pasa_error (-1, __FILE__, __LINE__, "pasa_setup failed") ;
    }
    else
    {
        printf ("Successfully initialized PASAdata structure.\n") ;
    }
    pasaparm = pasadata->Parms->pasa ;

    /* Determine problem size */
    CUTEST_cdimen( &status, &funit, &CUTEst_nvar, &CUTEst_ncon) ;
    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
    ncol = CUTEst_nvar ; /* integer */
    Ncol = ncol ;        /* PASAINT */
    nrow = CUTEst_ncon ; /* integer */
    Nrow = nrow ;        /* PASAINT */

    /* e_order determines order of eqn and ineq in list of constraints */
    /* if e_order  = 1 then equations come before inequalities */
    /* if e_order  = 2 then inequalities come before equalities */
    /* if e_order != 1 or 2 then order does not matter */
    e_order = 1 ;

    /* l_order determines order of lin and nonlin constraints */
    /* if l_order  = 1 then lin come before nonlin */
    /* if l_order  = 2 then nonlin come before lin */
    /* if l_order != 1 or 2 then order does not matter */
    l_order = 1 ;

    /* v_order determines order of lin and nonlin variables */
    v_order = 2 ;

    /* Reserve memory for variables, bounds, and multipliers */
    /* and call appropriate initialization routine for CUTEst */
    x =      (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
    lo =     (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
    hi =     (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
    bl =     (PASAFLOAT *) malloc ((Nrow+1)*sizeof (PASAFLOAT)) ;
    bu =     (PASAFLOAT *) malloc ((Nrow+1)*sizeof (PASAFLOAT)) ;
    offset = (PASAFLOAT *) malloc ((Nrow+1)*sizeof (PASAFLOAT)) ;
    lambda = (PASAFLOAT *) malloc ((Nrow+1)*sizeof (PASAFLOAT)) ;
    MALLOC( equatn, nrow+1, logical ) ;
    MALLOC( linear, nrow+1, logical ) ;
    CUTEST_csetup ( &status, &funit, &iout, &io_buffer, &ncol,
                    &nrow, x, lo, hi, lambda, bl, bu, equatn, 
                    linear, &e_order, &l_order, &v_order ) ;

    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }

    /* Check if components of lo are equal to -1e+20 and, if so,
       update to -PASAINF */

    loExists = FALSE ;
    for (i = 0; i < ncol; i++)
    {
        if ( lo [i] == -1e+20 )
        {
            lo [i] = -PASAINF ;
        }
        else
        {
            loExists = TRUE ;
        }
    }

    /* Check if components of hi are equal to 1e+20 and, if so,
       update to PASAINF */

    hiExists = FALSE ;
    for (i = 0; i < ncol; i++)
    {
        if ( hi [i] == 1e+20 )
        {
            hi [i] = PASAINF ;
        }
        else
        {
            hiExists = TRUE ;
        }
    }

    /* if there are linear constraints, also check the bound for
       infinite values and setup the constraint Jacobian matrix */

    /* Store zero in an array named zeros, it is used below. */
    zeros = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
    pasa_initx (zeros, PASAZERO, Ncol) ;

    if ( nrow == 0 )
    {
        Ap = NULL ;
        ATp = NULL ;
        free (bl) ;
        free (bu) ;
        bl = NULL ;
        bu = NULL ;
    }
    else
    {
        /* Check if components of bl are equal to -1e+20 and, if so,
           update to -PASAINF */
    
        for (i = 0; i < nrow; i++)
        {
            if ( bl [i] == -1e+20 ) bl [i] = -PASAINF ;
        }

        /* Check if components of bu are equal to 1e+20 and, if so,
           update to PASAINF */

        for (i = 0; i < nrow; i++)
        {
            if ( bu [i] == 1e+20 ) bu [i] = PASAINF ;
        }

        /* Determine number of nonzeros required to store the constraint
           Jacobian in sparse format */

        CUTEST_cdimsj ( &status, &nnzj ) ;

        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }

        /* Reserve memory for a zero vector and for J_val, J_col,
           and J_val */
        J_val = (PASAFLOAT *) malloc (nnzj*sizeof (PASAFLOAT)) ;
        J_col = (PASAINT *)   malloc (nnzj*sizeof (PASAINT)) ;
        J_row = (PASAINT *)   malloc (nnzj*sizeof (PASAINT)) ;

        j_col = (integer *)   malloc (nnzj*sizeof (integer)) ;
        j_row = (integer *)   malloc (nnzj*sizeof (integer)) ;

        /* Evaluate constraint gradients at zero */
        CUTEST_csgr ( &status, &ncol, &nrow, zeros, lambda, 
                      &cute_false, &anz, &nnzj, J_val, j_col, j_row ) ;

        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }

        for (i = 0; i < nnzj; i++)
        {
            J_col [i] = j_col [i] ;
            J_row [i] = j_row [i] ;
        }

        /* Returned anz also includes nvar components of obj gradient */

        anz -= ncol ;

        /* Reserve memory for Ap, Ai, Ax */
        Ap = (PASAINT *) malloc ((Ncol+1)*sizeof (PASAINT)) ;
        Ai = (PASAINT *) malloc (anz*sizeof (PASAINT)) ;
        Ax = (PASAFLOAT *) malloc (anz*sizeof (PASAFLOAT)) ;

        /* Set Ap [i] = 0 for 0 <= i <= ncol */
        pasa_initi (Ap, 0, Ncol+1) ;

        /* Store column pointer values (Ap) */
        for (i = 0; i < nnzj; i++)
        {
            if ( J_row [i] != 0 ) 
            {
                j = J_col [i] ;
                Ap [j] += 1 ;
            }
        }

        for (j = 1; j <= ncol; j++)
        {
            Ap [j] += Ap [j-1] ;
        }

        /* Store row indices (Ai) and nonzero values of A (Ax) */

        for (k = 0; k < nnzj; k++)
        {
            if ( J_row [k] != 0 )
            {
                j = J_col [k] - 1 ;
                i = Ap [j] ;
                Ai [i] = J_row [k] - 1 ;
                Ax [i] = J_val [k] ;
                Ap [j]++ ;
            }
        }

        for (j = ncol; j > 0; j--)
        {
             Ap [j] = Ap [j-1] ;
        }
        Ap [0] = 0 ;

        /* perform double transpose to ensure that the rows indices of A
           are sorted in each column */
        ATp = (PASAINT *) malloc ((Nrow+1)*sizeof (PASAINT)) ;
        ATi = (PASAINT *) malloc (Ap [Ncol]*sizeof (PASAINT)) ;
        ATx = (PASAFLOAT *) malloc (Ap [Ncol]*sizeof (PASAFLOAT)) ;
        sort_cols (Ap, Ai, Ax, ATp, ATi, ATx, Nrow, Ncol) ;

        /* Adjust bl and bu for any constants in the constraints.
           We obtain the constants by evaluation at x = 0. */
        CUTEST_ccfg ( &status, &ncol, &nrow, zeros, offset, 
                      &cute_false, &lj1, &lj2, J_val, &cute_false ) ;

        for (i = 0; i < nrow; i++)
        {
            bl [i] -= offset [i] ;
            bu [i] -= offset [i] ;
        }
    }

    /* see if the problem has a linear objective by comparing the name
       pname of the test problem to the names lpprob of the LPs contained
       in the file classLP */
    strcpy (fullpathname, cutest_dir) ;
    LPfile = fopen (strcat (fullpathname, "/classLP"), "r") ;
    while (fgets (lpprob, MAXLINE, LPfile) != (char *) NULL)
    {
        for (lpname = lpprob; *lpname; lpname++)
        {
            if (isspace (*lpname)) *lpname = '\0' ;
        }
        lpname = lpprob ;
        if ( strcmp (lpname, pname) == 0 )
        {
            LP = TRUE ;
            break ;
        }
    }
    fclose(LPfile) ;

    /* see if the problem has a quadratic objective by comparing the name
       pname of the test problem to the names qpprob of the QPs contained
       in the file classQP */
    if ( LP == FALSE )
    {
        strcpy (fullpathname, cutest_dir) ;
        QPfile = fopen (strcat (fullpathname, "/classQP"), "r") ;
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
        fclose(QPfile) ;
    }

    if ( LP == TRUE )
    {
        /* If the problem has a linear objective, then extract the
           linear term in the objective. */

        c = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        CUTEST_cofg (&status, &ncol, zeros, &fadjust, c, &cute_true);
        Qc = c ;
    }
    else if ( QP == TRUE )
    {
        printf ("the problem has a quadratic objective\n") ;
        /* nnzh = the number of nonzeros required to store the sparse Hessian 
           matrix in coordinate format */

        /* If the problem has a quadratic objective, then extract the
           Hessian matrix and the linear term in the objective. */
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status);
        }

        /* Reserve memory for H_val, H_row, H_col */
        CUTEST_cdimsh ( &status, &nnzh );
        H_val = (PASAFLOAT *) malloc (nnzh*sizeof (PASAFLOAT)) ;
        H_row = (PASAINT *)   malloc (nnzh*sizeof (PASAINT)) ;
        H_col = (PASAINT *)   malloc (nnzh*sizeof (PASAINT)) ;
        h_row = (integer *)   malloc (nnzh*sizeof (integer)) ;
        h_col = (integer *)   malloc (nnzh*sizeof (integer)) ;

        /* Determine the nonzero values in the Hessian */
        CUTEST_cish ( &status, &ncol, zeros, &iprob, &H_anz, &nnzh,
                      H_val, h_row, h_col );

        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status) ;
        }

        if ( nnzh != H_anz )
        {
            printf ("nnzh (%ld) != H_anz (%ld)\n", (LONG) nnzh, (LONG) H_anz) ;
            pasa_error (-1, __FILE__, __LINE__, "STOP") ;
        }

        for (i = 0; i < H_anz; i++)
        {
            H_row [i] = h_row [i] ;
            H_col [i] = h_col [i] ;
        }

        /* Determine number of nonzero values in the Hessian and the
           column counts. */
        Hp = (PASAINT *) malloc ((Ncol+1)*sizeof (PASAINT)) ;
        pasa_initi (Hp, 0, Ncol+1) ;
        Hpp = Hp+1 ;
        k = 0 ;
        for (i = 0 ; i < nnzh; i++)
        {
            if ( H_val [i] != PASAZERO )
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
                        pasa_error (-1, __FILE__, __LINE__,
                                      "problem has unsymmetric Hessian") ;
                    }
                }
            }
        }
        for (j = 1; j <= ncol; j++)
        {
            Hp [j] += Hp [j-1] ;
        }

        Hi = (PASAINT *)   malloc (k*sizeof (PASAINT)) ;
        Hx = (PASAFLOAT *) malloc (k*sizeof (PASAFLOAT)) ;
        HTp= (PASAINT *)   malloc ((Ncol+1)*sizeof (PASAINT)) ;
        HTi= (PASAINT *)   malloc (k*sizeof (PASAINT)) ;
        HTx= (PASAFLOAT *) malloc (k*sizeof (PASAFLOAT)) ;

        for (i = 0 ; i < nnzh; i++)
        {
            if ( H_val [i] != PASAZERO )
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
        sort_cols (Hp, Hi, Hx, NULL, NULL, NULL, Ncol, Ncol) ;

        /* Determine c in objective function */
        c = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        CUTEST_cofg (&status, &ncol, zeros, &fadjust, c, &cute_true);

        /* find the fixed variables in the problem, they will be dropped */
        drop_col = (PASAINT *) malloc (Ncol*sizeof (PASAINT)) ;
        for (j = 0; j < ncol; j++)
        {
            if ( lo [j] == hi [j] )
            {
                drop_col [j] = 1 ;
                x [j] = lo [j] ;
            }
            else
            {
                drop_col [j] = 0 ;
            }
        }

        /* find any fixed variables connected with the linear constraints */
        if ( nrow > 0 )
        {
            drop_row = (PASAINT *) malloc (Nrow*sizeof (PASAINT)) ;
            l = 0 ;
            for (i = 0; i < nrow; i++)
            {
                drop_row [i] = 0 ;
                /* find equality constraints with one variable */
                if ( (ATp [i+1] - ATp [i] == 1) && (bl [i] == bu [i]) )
                {
                    k = ATp [i] ;
                    j = ATi [k] ;
                    x [j] = bl [i]/ATx [k] ; /* set x to bound */
                    drop_col [j] = 1 ; /* column   can be removed */
                    drop_row [i] = 1 ; /* equation can be removed */
                    l++ ;
                }
            }
        }
        xcopy = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        pasa_copyx (xcopy, x, Ncol) ;

        /* cost adjustment due to fixed variables is 0.5*xb'*H*xb + c'*xb
           c adjustment is xb'*H_{bf} */
        s = PASAZERO ;
        for (j = 0; j < ncol; j++)
        {
            q = Hp [j+1] ;
            if ( drop_col [j] == 1 )
            {
                t = x [j] ;
                fadjust += t*c [j] ;
                for (p = Hp [j]; p < q; p++)
                {
                    if ( drop_col [Hi [p]] == 1 )
                    {
                        s += t*Hx [p]*x [Hi [p]] ;
                    }
                }
                /* adjust bl and bu for the removed fixed variables */
                if ( nrow > 0 )
                {
                    q = Ap [j+1] ;
                    for (p = Ap [j]; p < q; p++)
                    {
                        i = Ai [p] ;
                        bl [i] -= t*Ax [p] ;
                        bu [i] -= t*Ax [p] ;
                    }
                }
            }
            else /* variable is free */
            {
                t = PASAZERO ;
                for (p = Hp [j]; p < q; p++)
                {
                    if ( drop_col [Hi [p]] == 1 )
                    {
                        t += Hx [p]*x [Hi [p]] ;
                    }
                }
                c [j] += t ;
            }
        }
        fadjust += 0.5*s ;

        /* compress c, lo, and hi */
        free_cols = 0 ;
        l = 0 ;
        ifree = (PASAINT *) malloc (Ncol*sizeof (PASAINT)) ;
        loExists = FALSE ;
        hiExists = FALSE ;
        for (j = 0; j < ncol; j++)
        {
            if ( drop_col [j] == 0 ) /* free variable */
            {
                c [free_cols] = c [j] ;   /* compress c */
                lo [free_cols] = lo [j] ; /* compress lo */
                if ( lo [j] > -PASAINF )
                {
                    loExists = TRUE ;
                }
                hi [free_cols] = hi [j] ; /* compress hi */
                if ( hi [j] < PASAINF )
                {
                    hiExists = TRUE ;
                }
                ifree [free_cols] = j ;   /* map to prior indices */
                free_cols++ ;
            }
        }
        Qc = c ;

        /* compress bl and bu */
        free_rows = 0 ;
        if ( nrow > 0 )
        {
            l = 0 ;
            for (i = 0; i < nrow; i++)
            {
                if ( drop_row [i] == 0 ) /* free variable */
                {
                    bl [free_rows] = bl [i] ; /* compress bl */
                    bu [free_rows] = bu [i] ; /* compress bu */
                    free_rows++ ;
                }
            }
        }

        /* remove columns from H corresponding to bound variables */
        free_cols = pasa_compress_matrix (Hp, Hi, Hx, Ncol, drop_col) ;

        /* transpose the matrix with the deleted columns */
        temp = (PASAINT *) malloc (PASAMAX(Nrow, Ncol)*sizeof (PASAINT)) ;
        pasa_transpose (HTp, HTi, HTx, Hp, Hi, Hx, Ncol, free_cols, temp) ;

        /* copy HT to H */
        pasa_copyx (Hx, HTx, HTp [Ncol]) ;
        pasa_copyi (Hi, HTi, HTp [Ncol]) ;
        pasa_copyi (Hp, HTp, Ncol+1) ;

        /* remove the deleted columns from the transpose matrix stored in H */
        free_cols = pasa_compress_matrix (Hp, Hi, Hx, Ncol, drop_col) ;

        /* check that the matrix is symmetric */
        pasa_transpose (HTp, HTi, HTx, Hp, Hi, Hx, free_cols, free_cols, temp);
        for (j = 0; j <= free_cols; j++)
        {
            if ( HTp [j] != Hp [j] )
            {
                pasa_error (-1, __FILE__, __LINE__, "error in H pointers") ;
            }
        }
        for (k = 0; k < Hp [free_cols]; k++)
        {
            if ( HTi [k] != Hi [k] )
            {
                pasa_error (-1, __FILE__, __LINE__, "error in H row indices") ;
            }
            if ( HTx [k] != Hx [k] )
            {
                printf ("HTx [%ld]: %e Hx [%ld]: %e\n",
                        (LONG) k, HTx [k], (LONG) k, Hx [k]) ;
                pasa_error (-1, __FILE__, __LINE__, "error in Hx values") ;
            }
        }

        if ( nrow > 0 )
        {
            /* compress A by removing deleted rows */
            free_rows = pasa_compress_matrix (ATp, ATi, ATx, Nrow, drop_row) ;

            /* transpose AT to get A with the deleted equations removed */
            pasa_transpose (Ap, Ai, Ax, ATp, ATi, ATx, Ncol, free_rows, temp) ;

            /* compress A be removing deleted columns */
            free_cols = pasa_compress_matrix (Ap, Ai, Ax, Ncol, drop_col);
        }

        /* free temp memory */
        free (temp) ;

        printf ("number of variables: %ld\n", (LONG) Ncol) ;
        printf ("number of free variables: %ld\n", (LONG) free_cols) ;
        printf ("number of equations: %ld\n", (LONG) Nrow) ;
        printf ("number of free equations: %ld\n", (LONG) free_rows) ;

#ifndef NDEBUG
        temp = (PASAINT *) malloc (PASAMAX(Nrow, Ncol)*sizeof (PASAINT)) ;
        tempx= (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        i = 0 ;
        for (j = 0; j < ncol; j++)
        {
            if ( drop_col [j] == 0 )
            {
                xcopy [j] = 1 + (j % 10) ;
                temp [i] = j ;
                tempx[i] = xcopy [j] ;
                i++ ;
            }
        }
        pasa_value (&s, xcopy, Ncol) ;
        prod = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        pasa_Hprod (prod, tempx, NULL, free_cols, free_cols) ;
        t = pasa_dot (prod, tempx, free_cols) ;
        t = 0.5*t + pasa_dot (tempx, Qc, free_cols) ;
        t += fadjust ;
        if ( s != 0 )
        {
            printf ("cost: %e cost error: %e relative error: %e\n",
                     s, fabs(s-t), fabs((s-t)/s)) ;
            if ( fabs((s-t)/s) > 1.e-8 )
            {
                pasa_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else
        {
            printf ("cost: %e cost error: %e\n", s, fabs(s-t)) ;
        }

        g = (PASAFLOAT *) malloc (Ncol*sizeof (PASAFLOAT)) ;
        pasa_grad (g, xcopy, Ncol) ;
        pasa_step (prod, prod, Qc, PASAONE, free_cols) ;
        t = PASAZERO ;
        s = PASAZERO ;
        for (i = 0; i < free_cols; i++)
        {
            j = temp [i] ;
            t += fabs (g [j] - prod [i]) ;
            s += fabs (g [j]) ;
        }
        if ( s != 0 )
        {
            printf ("grad: %e grad error: %e relative error: %e\n",
                     s, t, t/s) ;
            if ( t/s > 1.e-8 )
            {
                pasa_error (-1, __FILE__, __LINE__, "stop") ;
            }
        }
        else
        {
            printf ("grad: %e grad error: %e\n", s, t) ;
        }

        free (prod) ;
        free (temp) ;
        free (tempx) ;
        free (g) ;
#endif

        Ncol = free_cols ;
        Nrow = free_rows ;

        if ( nrow > 0 )
        {
            free (drop_row) ;
        }
        free (drop_col) ;
        free (HTp) ;
        free (HTi) ;
        free (HTx) ;
    }
    else /* the matrix is neither linear nor quadratic,
            prepare for evaluation of Hessian */
    {
        /* Reserve memory for H_val, H_row, H_col */
        CUTEST_cdimsh ( &status, &CUTEst_nnzh );
        H_val = (PASAFLOAT *) malloc (CUTEst_nnzh*sizeof (PASAFLOAT)) ;
        H_row = (PASAINT *)   malloc (CUTEst_nnzh*sizeof (PASAINT)) ;
        H_col = (PASAINT *)   malloc (CUTEst_nnzh*sizeof (PASAINT)) ;
        h_row = (integer *)   malloc (CUTEst_nnzh*sizeof (integer)) ;
        h_col = (integer *)   malloc (CUTEst_nnzh*sizeof (integer)) ;

       /* CUTEst_nnzh = the number of nonzeros required to store the sparse
          Hessian matrix in coordinate format */
        if (status)
        {
            printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
            exit(status);
        }

        /* Determine the nonzero values in the Hessian */
        CUTEST_cish ( &status, &ncol, zeros, &iprob, &H_anz, &CUTEst_nnzh,
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
            pasa_error (-1, __FILE__, __LINE__, "STOP") ;
        }
        for (i = 0; i < H_anz; i++)
        {
            H_row [i] = h_row [i] ;
            H_col [i] = h_col [i] ;
        }

        /* Determine the column counts: Note that CUTE only gives the
           nonzeros in the upper triangle */
        HessHp = (PASAINT *) malloc ((Ncol+1)*sizeof (PASAINT)) ;
        pasa_initi (HessHp, 0, Ncol+1) ;
        Hpp = HessHp+1 ;
        nnzh = 0 ;
        for (i = 0; i < CUTEst_nnzh; i++)
        {
            nnzh++ ;
            /* change from Fortran rows and cols to C rows and cols */
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
                    pasa_error (-1, __FILE__, __LINE__,
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

        HessHi = (PASAINT *) malloc (nnzh*sizeof (PASAINT)) ;
        HessHx = (PASAFLOAT *) malloc (nnzh*sizeof (PASAFLOAT)) ;

        for (i = 0 ; i < CUTEst_nnzh; i++)
        {
            row = H_row [i] ;
            col = H_col [i] ;
            k = HessHp [col] ;
            HessHi [k] = row ;
            HessHx [k] = (PASAFLOAT) i ;
            HessHp [col]++ ;
            if ( row != col )
            {
                k = HessHp [row] ;
                HessHi [k] = col ;
                HessHx [k] = (PASAFLOAT) i ;
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
        sort_cols (HessHp, HessHi, HessHx, NULL, NULL, NULL, Ncol, Ncol) ;
        PASAhmap = malloc (nnzh*sizeof (PASAINT)) ;
        for (i = 0; i < nnzh; i++)
        {
            /* store the location in H_val of Hx [i] */
            PASAhmap [i] = (PASAINT) HessHx [i] ;
        }
    }

    if ( ATp != NULL )
    {
        free (ATp) ;
        free (ATi) ;
        free (ATx) ;
    }

    pasaparm->loExists = TRUE ;
    if ( loExists == FALSE )
    {
        free (lo) ;
        lo = NULL ;
        pasaparm->loExists = FALSE ;
    }

    pasaparm->hiExists = TRUE ;
    if ( hiExists == FALSE )
    {
        free (hi) ;
        hi = NULL ;
        pasaparm->hiExists = FALSE ;
    }

    if ( QP == TRUE )
    {
        pasaparm->fadjust = fadjust ;
    }

    if ( LP == TRUE )
    {
        pasaparm->LP = TRUE ;
        pasaparm->fadjust = PASAZERO ;
    }

    /* set new parameter values for PASA/CG/PPROJ/NAPHEAP here,
       otherwise default values are used */
    cgparm    = pasadata->Parms->cg ;
    napparm   = pasadata->Parms->napheap ;
    pprojparm = pasadata->Parms->pproj ;
    pasaparm  = pasadata->Parms->pasa ;
    pprojparm->use_sparsa = FALSE ;
    pasaparm->PrintStat = TRUE ;       /* default PrintStat = FALSE */
    /* pasaparm->grad_tol = 1.e-8 ; */ /* default = 1.e-6 */

    /* Set up the pasadata structure.
       Here lambda is not used for start guess, only to make use of memory */ 
    pasadata->lambda = lambda ;
    pasadata->x = x ;
    pasadata->ncol = Ncol ;
    pasadata->nrow = Nrow ;
    pasadata->lo = lo ;
    pasadata->hi = hi ;
    pasadata->Ap = Ap ;
    pasadata->Ai = Ai ;
    pasadata->Ax = Ax ;
    pasadata->bl = bl ;
    pasadata->bu = bu ;
    pasadata->c = Qc ;
    if ( QP == TRUE ) pasadata->hprod = pasa_Hprod ;
    else              pasadata->hprod = NULL ;
    pasadata->value = pasa_value ;
    pasadata->grad = pasa_grad ;
    pasadata->valgrad = pasa_valgrad ;
    pasadata->hess = pasa_hess ;

    if ( Nrow > 0 )
    {
        printf ("sup norm of Ax: %e\n", pasa_sup_norm (Ax, Ap [Ncol])) ;
    }

    /* time run using wall clock, call several times to exclude startup cost */
    gettimeofday (&tv, NULL) ;
    sec = tv.tv_sec ;
    usec = tv.tv_usec ;
    gettimeofday (&tv, NULL) ;
    walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;
    printf ("walltime start cost: %12.6f\n", walltime) ;

    gettimeofday (&tv, NULL) ;
    sec = tv.tv_sec ;
    usec = tv.tv_usec ;

    /* Call the optimizer */
    pasa (pasadata) ;

    gettimeofday (&tv, NULL) ;
    walltime = tv.tv_sec - sec + (double) (tv.tv_usec - usec) /1.e6 ;

    status_pasa = pasadata->Stats->pasa->status ;
    if ( status_pasa != PASA_ERROR_TOLERANCE_SATISFIED )
    {
        pasa_print_status (pasadata) ;
        exit (status_pasa) ;
    }

    ExitCode = 0;

    /* Get CUTEst statistics */
    CUTEST_creport( &status, calls, cpu) ;
    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
        exit(status) ;
    }

#ifndef NDEBUG
    if ( LP == TRUE )
    {
        pasa_errLP0 (pasadata->lambda, Nrow, Ncol, x, Qc, lo, hi, bl, bu,
                     Ap, Ai, Ax, 3) ;
    }
#endif

    pasastat = pasadata->Stats->pasa ;
    cgstat = pasadata->Stats->cg ;
    pprojstat = pasadata->Stats->pproj ;
    napstat = pasadata->Stats->napheap ;
    long nchols ;
    if ( pasadata->Stats->use_pproj == TRUE )
    {
        nchols = pprojstat->nchols ;
    }
    else
    {
        nchols = 0 ;
    }
    /* print unformatted pasa statistics and nchols from pproj stats */
    if ( LP == TRUE )
    {
        printf ("!!%10s %6ld %4ld %4ld "
                "%5i %16.7e %25.16e %11.6f\n",
                 pname, (LONG) Ncol, (LONG) pasastat->nproject, nchols,
                 status_pasa, pasastat->err, pasastat->f, walltime) ;
    }
    else
    {
        printf ("!!%10s %6ld %4ld %4ld %4ld %4ld %4ld %4ld %6ld %6ld %6ld %7ld "
                "%7ld %5i %16.7e %16.7e %11.6f\n",
                 pname, (LONG) Ncol, (LONG) pasastat->gpit,
                 (LONG) pasastat->gpnf, (LONG) pasastat->gpng,
                 (LONG) pasastat->agpit, (LONG) pasastat->agpnf,
                 (LONG) pasastat->agpng, (LONG) cgstat->iter,
                 (LONG) cgstat->nfunc, (LONG) cgstat->ngrad,
                 (LONG) pasastat->nproject, nchols,
                 status_pasa, pasastat->err, pasastat->f, walltime) ;
    }

    printf(" Final f                         = %-16.7e\n", pasastat->f) ;
    pasa_value (&t, x, CUTEst_nvar) ;
    printf(" Function value at final x       = %-25.16e\n", t) ;

    /* map x back to original coordinates for QPs */
    if ( QP == TRUE )
    {
        for (j = 0; j < free_cols; j++)
        {
            xcopy [ifree [j]] = x [j] ;
        }
        pasa_copyx (x, xcopy, CUTEst_nvar) ;
    }

    /* Print lines to clearly separate problems */

    printf (" ====================================================\n\n" ) ;

    ierr = 0;
    FORTRAN_close( &funit, &ierr ) ;
    if ( ierr )
    {
        printf( "Error closing %s on unit %ld.\n", fname, (LONG) funit ) ;
        printf( "Trying not to abort.\n" ) ;
    }
    if ( nrow > 0 )
    {
        free (Ap) ;
        free (Ai) ;
        free (Ax) ;
        free (J_val) ;
        free (J_col) ;
        free (J_row) ;
        free (j_col) ;
        free (j_row) ;
    }

    /* Free workspace */
    free (zeros) ;
    free (offset) ;
    free (pname) ;
    free (x) ;
    if ( lo != NULL ) free (lo) ;
    if ( hi != NULL ) free (hi) ;
    if ( bl != NULL ) free (bl) ;
    if ( bu != NULL ) free (bu) ;
    free (lambda) ;
    if ( H_val != NULL )
    {
        free (H_val) ;
        free (H_row) ;
        free (H_col) ;
        free (h_row) ;
        free (h_col) ;
    }
    free (equatn) ; 
    free (linear) ;
    if ( LP == TRUE )
    {
        free (c) ;
    }
    else if ( QP == TRUE )
    {
        free (Hx) ;
        free (Hi) ;
        free (Hp) ;
        free (c) ;
        free (ifree) ;
        free (xcopy) ;
    }
    else /* not a quadratic, free Hessian workspace */
    {
        free (HessHp) ;
        free (HessHi) ;
        free (HessHx) ;
        free (PASAhmap) ;
    }

    /* free memory allocated for pasa data */
    pasa_terminate (&pasadata) ;

    /* end cutest */
    CUTEST_cterminate( &status ) ;
    fflush (stdout) ;

    return 0 ;
}

#ifdef __cplusplus
}    /* Closing brace for  extern "C"  block */
#endif
/* evaluation routines for unconstrained problems */
void cg_hess
(
    CGhess *Hess
)
{
    PASAINT i, N ;
    PASAFLOAT *x ;
    integer n, H_anz, nnzh, status ;

    N = Hess->ncol ;
    n = N ;
    x = Hess->x ;
    Hess->Hp = HessHp ;
    Hess->Hi = HessHi ;
    Hess->Hx = HessHx ;
    nnzh = HessHp [N] ;
    CUTEST_ush (&status, &n, x, &H_anz, &CUTEst_nnzh,
                  H_val, h_row, h_col) ;

    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }

    for (i = 0; i < nnzh; i++)
    {
        Hess->Hx [i] = H_val [PASAhmap [i]] ;
    }
    return ;
}
void cg_value
(
    PASAFLOAT *f,
    PASAFLOAT *x,
    PASAINT N
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
    return ;
}

void cg_grad
(
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT N
)
{
    integer n, status;
    n = N ;
    CUTEST_ugr( &status, &n, x, g) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
}

void cg_valgrad
(
    PASAFLOAT *f,
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT N
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
    return ;
}

void cg_Hprod
(
    PASAFLOAT     *Hd, /* Hd = H*d */
    PASAFLOAT      *d,
    PASAINT         n  /* number of nonzero entries in d */
)
{
    PASAINT j, p, q ;
    PASAFLOAT t ;
    pasa_initx (Hd, PASAZERO, n) ;
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


/* evaluation routines for constrained problems */
void pasa_hess
(
    PASAhess *Hess
)
{
    PASAINT i, N ;
    PASAFLOAT *x ;
    integer n, H_anz, iprob, nnzh, status ;

    N = Hess->ncol ;
    n = N ;
    x = Hess->x ;
    Hess->Hp = HessHp ;
    Hess->Hi = HessHi ;
    Hess->Hx = HessHx ;
    nnzh = HessHp [N] ;
    iprob = 0 ;
    CUTEST_cish (&status, &n, x, &iprob, &H_anz, &CUTEst_nnzh,
                  H_val, h_row, h_col) ;

    if (status)
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }

    for (i = 0; i < nnzh; i++)
    {
        Hess->Hx [i] = H_val [PASAhmap [i]] ;
    }
    return ;
}
void pasa_value
(
    PASAFLOAT *f,
    PASAFLOAT *x,
    PASAINT N
)
{
    PASAFLOAT *dummy ;
    integer status, n ;

    n = N ;
    CUTEST_cofg( &status, &n, x, f, dummy, &cute_false) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status) ;
        exit(status) ;
    }
    return ;
}

void pasa_grad
(
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT N
)
{
    PASAFLOAT F ;
    integer n, status;
    n = N ;
    CUTEST_cofg( &status, &n, x, &F, g, &cute_true) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
}

void pasa_valgrad
(
    PASAFLOAT *f,
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT N
)
{
    integer n, status;
    n = N ;
    CUTEST_cofg( &status, &n, x, f, g, &cute_true) ;
    if ((status == 1) || (status == 2))
    {
        printf("** CUTEst error, status = %ld, aborting\n", (LONG) status);
        exit(status);
    }
    return ;
}

void pasa_Hprod
(
    PASAFLOAT     *Hd, /* Hd = H*d */
    PASAFLOAT      *d,
    PASAINT    *ifree,
    PASAINT         m, /* dimension of H */
    PASAINT         n  /* number of nonzero entries in d */
)
{
    PASAINT j, k, p, q ;
    PASAFLOAT t ;
    pasa_initx (Hd, PASAZERO, m) ;
    if ( ifree != NULL )
    {
        for (j = 0; j < n; j++)
        {
            t = d [j] ;
            if ( t ) /* if t != 0 */
            {
                k = ifree [j] ;
                q = Hp [k+1] ;
                for (p = Hp [k]; p < q; p++)
                {
                    Hd [Hi [p]] += t*Hx [p] ;
                }
            }
        }
    }
    else
    {
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
}

/* perform double transpose to sort row indices in each column of matrix */
void sort_cols
(
    PASAINT    *Ap, /* column pointers */
    PASAINT    *Ai, /* row indices */
    PASAFLOAT  *Ax, /* numerical values */
    PASAINT   *atp, /* row pointers for transpose */
    PASAINT   *ati, /* column indices for transpose */
    PASAFLOAT *atx, /* numerical values for transpose */
    PASAINT   nrow, /* number of rows */
    PASAINT   ncol  /* number of cols */
)
{
    PASAINT *ATp, *ATi, *temp ;
    PASAFLOAT *ATx ;
    ATp = atp ;
    ATi = ati ;
    ATx = atx ;
    if ( atp == NULL )
    {
        ATp = (PASAINT *) malloc ((nrow+1)*sizeof (PASAINT)) ;
        ATi = (PASAINT *) malloc (Ap [ncol]*sizeof (PASAINT)) ;
        ATx = (PASAFLOAT *) malloc (Ap [ncol]*sizeof (PASAFLOAT)) ;
    }
    temp = (PASAINT *) malloc (PASAMAX (nrow, ncol)*sizeof (PASAINT)) ;
    pasa_transpose (ATp, ATi, ATx, Ap, Ai, Ax, nrow, ncol, temp) ;
    pasa_transpose (Ap, Ai, Ax, ATp, ATi, ATx, ncol, nrow, temp) ;
    if ( atp == NULL )
    {
        free (ATp) ;
        free (ATi) ;
        free (ATx) ;
    }
    free (temp) ;
}

/* ==========================================================================
   === pasa_errLP0 ==========================================================
   ==========================================================================
   Consider the following LP:

       min c'x subject to bl <= Ax <= bu, lo <= x <= hi

   At optimality, the constraints are satisfied and there exists lambda
   with the following properties:

       1. If A_j' lambda > c_j, then x_j = hi_j
       2. If A_j' lambda < c_j, then x_j = lo_j
       3. If lo_j < x_j < hi_j, then A_j'lambda = 0
       4. If bl_i < A_i'x < bu_i, then lambda_i = 0
       5. If A_i'x = bu_i, then lambda_i <= 0
       6. If A_i'x = bl_i, then lambda_i >= 0
   ========================================================================== */
void pasa_errLP0
(
    PASAFLOAT *lambda,
    PASAINT      nrow,
    PASAINT      ncol,
    PASAFLOAT      *x,
    PASAFLOAT      *c,
    PASAFLOAT     *lo,
    PASAFLOAT     *hi,
    PASAFLOAT     *bl,
    PASAFLOAT     *bu,
    PASAINT       *Ap,
    PASAINT       *Ai,
    PASAFLOAT     *Ax,
    int    PrintLevel
)
{
    int status ;
    PASAINT i, imaxprimal, imaxdual, j, jmax, k, p, q ;
    PASAFLOAT d, e, Eprimal, Elambda, Emax, loj, hij, Lmax, max_absAx, Xmax, t,
             *absAx, *y ;

    int const loExists = (lo != NULL) ? TRUE : FALSE ;
    int const hiExists = (hi != NULL) ? TRUE : FALSE ;
    y = pasa_malloc (&status, nrow, sizeof (PASAFLOAT)) ;
    pasa_initx (y, PASAZERO, nrow) ;
    absAx = pasa_malloc (&status, nrow, sizeof (PASAFLOAT)) ;
    pasa_initx (absAx, PASAZERO, nrow) ;
    Xmax = -PASAONE ;
    Emax = -PASAONE ;
    k = 0 ;
    if ( PrintLevel > 1 ) printf ("Primal Bound Errors:\n") ;
    for (j = 0; j < ncol; j++)
    {
        e = PASAZERO ;
        if ( loExists ) loj = lo [j] ;
        else            loj = -PASAINF ;
        if ( hiExists ) hij = hi [j] ;
        else            hij = PASAINF ;
        if ( x [j] < loj )
        {
            t = loj ;
            e = t - x [j] ;
        }
        else if ( x [j] > hij )
        {
            t = hij ;
            e = x [j] - t ;
        }
        else
        {
            t = x [j] ;
        }
        if ( PrintLevel > 2 )
        {
            printf ("%i %e %e %e %e\n", j, e, loj, x [j], hij) ;
        }
        if ( e > Emax )
        {
            Emax = e ;
            jmax = j ;
        }
        if ( fabs (t) > Xmax )
        {
            Xmax = fabs (t) ;
        }
        PASAINT const l = Ap [j+1] ;
        for (; k < l; k++)
        {
            y [Ai [k]] += t*Ax [k] ;
            absAx [Ai [k]] += fabs (t*Ax [k]) ;
        }
    }
    if ( PrintLevel > 1 )
    {
        printf ("Total: %e jmax: %i relative: %e Xmax: %e\n\n",
                 Emax, jmax, Emax/Xmax, Xmax) ;
        printf ("Primal Equation Errors:\n") ;
    }
    max_absAx = pasa_sup_norm (absAx, nrow) ;
    k = 0 ;
    Eprimal = -PASAONE ;
    Elambda = -PASAONE ;
    imaxprimal = -1 ;
    for (i = 0; i < nrow; i++)
    {
        e = PASAZERO ;
        if ( bl [i] >= y [i] )
        {
            e = bl [i] - y [i] ;
        }
        else if ( y [i] >= bu [i] )
        {
            e = y [i] - bu [i] ;
        }
        if ( PrintLevel > 2 )
        {
            printf ("p: %i %e %e %e %e\n", i, e, bl [i], y [i], bu [i]) ;
        }
        d = PASAZERO ;
        if ( lambda [i] > PASAZERO )
        {
            d = PASAMIN (lambda [i], fabs (bl [i] - y [i])) ;
        }
        else if ( lambda [i] < PASAZERO )
        {
            d = PASAMIN (-lambda [i], fabs (bu [i] - y [i])) ;
        }
        if ( PrintLevel > 2 )
        {
            printf ("d: %i %e %e %e %e\n", i, e, bl [i], lambda [i], bu [i]) ;
        }
        if ( d > Elambda )
        {
            Elambda = d ;
            imaxdual = i ;
        }
        if ( e > Eprimal )
        {
            Eprimal = e ;
            imaxprimal = i ;
        }
    }

    if ( PrintLevel > 1 )
    {
        printf ("Primal Total: %e imax: %i Relative: %e absAx: %e\n",
                        Eprimal, imaxprimal, Eprimal/max_absAx, max_absAx) ;
        printf ("Lambda Total: %e imax: %i Relative: %e\n\n",
                                   Elambda, imaxdual, Elambda/max_absAx) ;
        printf ("Dual Equation Errors:\n") ;
    }
    Emax = -PASAONE ;
    p = 0 ;
    for (j = 0; j < ncol; j++)
    {
        q = Ap [j+1] ;
        t = c [j] ;
        for (; p < q; p++)
        {
            t -= Ax [p]*lambda [Ai [p]] ;
        }
        e = PASAZERO ;
        if ( loExists ) loj = lo [j] ;
        else            loj = -PASAINF ;
        if ( hiExists ) hij = hi [j] ;
        else            hij = PASAINF ;
        if ( t > PASAZERO )
        {
            e = PASAMIN (t, fabs (loj - x [j])) ;
        }
        else if ( t < PASAZERO )
        {
            e = PASAMIN (-t, fabs (hij - x [j])) ;
        }
        if ( e > Emax )
        {
            Emax = e ;
            jmax = j ;
        }
        if ( PrintLevel > 2 )
        {
            printf ("%i %e %e %e %e\n", j, e, loj, x [j], hij) ;
        }
    }
    Lmax = pasa_sup_norm (lambda, nrow) ;
    if ( PrintLevel > 1 )
    {
        printf ("Total: %e jmax: %i Relative: %e lmax: %e\n\n",
                 Emax, jmax, Emax/Lmax, Lmax) ;
    }
}
