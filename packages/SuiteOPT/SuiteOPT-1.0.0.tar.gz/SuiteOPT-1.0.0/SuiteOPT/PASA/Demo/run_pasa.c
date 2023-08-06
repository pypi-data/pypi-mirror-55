    /* Test problem: Below are the details of the included test problem. 

       Dimension: n = 5

         min f(x)   s.t.   lo <= x <= hi, bl <= Ax <= bu

       where

         f(x) = Sum_{i = 1 to n-1} 100 (x [i+1] - x [i]^2)^2 + (1 - x [i])^2

         lo = [ -1; -1; -1; -1; -1 ]
         hi = [  2;  2;  2;  2;  2 ]
         bl = [  3; -1; -2; -1 ]
         bu = [  5;  3;  0;  1 ]

          A = |  1   1   1   1   1  |
              |  1   1   1   0  -1  |
              |  1   0  -1  -1   1  |
              |  1  -1   0   1   0  |

       The function f is the fifth degree generalization of the Rosenbrock
       function. For unconstrained optimization, the absolute minimum of f
       is obtained at x = [  1;  1;  1;  1;  1 ] and f attains a local min
       at x = [  -1;  1;  1;  1;  1 ]. The linear and bound constraints were
       chosen so that both of these vectors lie within the feasible region
       for the test problem described above.  */

#include "pasa.h"

/* prototypes */
void pasa_value
(
    PASAFLOAT *val,
    PASAFLOAT   *x,
    PASAINT      n
) ;

void pasa_grad
(
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT    n
) ;

void pasa_valgrad
(
    PASAFLOAT *val,
    PASAFLOAT   *g,
    PASAFLOAT   *x,
    PASAINT      n
) ;

/* main function */
int main (void /*int argc, char **argv*/)
{
    PASAdata *pasadata ; 
    /* upper and lower bounds on x are stored in the arrays lo and hi below */
    PASAFLOAT lo [] = {-1, -1, -1, -1, -1} ;
    PASAFLOAT hi [] = { 2,  2,  2,  2,  2} ;
    /* The nonzeros in the constraint matrix are stored in sparse matrix
       format by columns. Ap contains the column pointers, Ai contains
       the row indices for nonzeros in each column, and Ax gives the
       numerical values of the nonzeros. */
    PASAINT Ap []   = { 0,  4,  7, 10, 13, 16} ;
    PASAINT Ai []   = { 0,  1,  2,  3,  /* indices in column 1 of A */
                        0,  1,      3,  /* indices in column 2 of A */
                        0,  1,  2,      /* indices in column 3 of A */
                        0,      2,  3,  /* indices in column 4 of A */
                        0,  1,  2    } ;/* indices in column 5 of A */
    PASAFLOAT Ax [] = { 1,  1,  1,  1,  /* values  in column 1 of A */
                        1,  1,     -1,  /* values  in column 2 of A */
                        1,  1, -1,      /* values  in column 3 of A */
                        1,     -1,  1,  /* values  in column 4 of A */
                        1, -1,  1    } ;/* values  in column 5 of A */
    /* we put the upper and lower bounds for the linear equalities and
       inequalities in the arrays bl and bu */
    PASAFLOAT bl [] = { 3, -1, -2, -1} ;
    PASAFLOAT bu [] = { 5,  3,  0,  1} ;

    /* Initialize the structure containing input data using pasa_setup.
       This routine returns a pointer to the pasa input data structure
       where parameter values are set to their default values: all integer
       inputs are set to zero, and all pointers are set to NULL. */
    printf ("Initializing PASAdata structure.\n") ;
    pasadata = pasa_setup () ;
    if ( pasadata == NULL )
    {
        printf ("pasa_setup ran out of memory\n") ;
    }
    else
    {
        printf ("Successfully initialized PASAdata structure.\n") ;
    }

    /* Store the arrays defining the problem in the pasadata structure
       that was initialized by the setup program above. */

    pasadata->lo = lo ;
    pasadata->hi = hi ;
    pasadata->Ap = Ap ;
    pasadata->Ai = Ai ;
    pasadata->Ax = Ax ;
    pasadata->bl = bl ;
    pasadata->bu = bu ;

    /* Also need to specify the problem dimension */
    pasadata->ncol = 5 ;

    /* By default, the number of rows in A is the maximum element in Ai,
       if it exists. If A does not exist, or equivalently, pasadata->Ap,
       pasadata->Ai, and pasadata->Ax are not specified, then nrow is 0
       by default. */

    /* An initial guess for the solution can be provided in pasadata->x.
       This requires that the array pasadata->x be first malloc'd, and
       then the initial guess for the components of x can be assigned.
       If no starting guess is provided, that pasa uses the vector with
       all components zero for the starting guess. Let's not specify x,
       so the starting guess is x = 0. Note that the starting guess does
       not need to be feasible. */

    /* The routines to evaluate the function and the gradient appear below,
       while their prototypes are above.  Since it is often easy to
       evaluate the gradient at the same time as the function value,
       we also code a routine valgrad below that simultaneously evaluates
       the function and its gradient.  Both the value and gradient routines
       are currently required, while the valgrad routine is optional.
       By including valgrad, the solution time can be reduced for some
       problems. */
    pasadata->value = pasa_value ;
    pasadata->grad = pasa_grad ;
    pasadata->valgrad = pasa_valgrad ;

    /* ---------------------- Customizing parameters ------------------------ */
    /* When pasa_setup() is called, all pasa parameters are set to their
       default values, which means that there is no printing. */

    /* call pasa */
    pasa (pasadata) ; 

    /* By default, pasadata->Parm->print_status = TRUE, so the status of
       the run will be printed. If this parameter was FALSE, then the
       status is printed using pasa_print_status (pasadata) ; */

    /* If the run was successful, the the solution is stored in pasadata->x */
    pproj_printx (pasadata->x, pasadata->ncol, "solution =") ;

    /* The pasa_print_stats routine gives all the statistics for the run */
    pasa_print_stats (pasadata) ;

    /* The pasa_print_parms routine gives the parameter values of all the
       routines that were used during the solution process. */
    pasa_print_parms (pasadata) ;

    /* Specific statistics can be extracted from the pasadata structure
       as shown below. */

    printf("\n\n *********************** PASA statistics **************"
           "**********\n\n") ;
    printf(" Code used                   : pasa\n") ;
    printf(" Problem                     : %-s\n", "PASA Test Problem") ;
    printf(" # variables                 = %-10ld\n",
          (LONG) pasadata->ncol) ;

    printf(" # grad proj iterations      = %-10ld\n",
          (LONG) pasadata->Stats->pasa->gpit) ;
    printf(" # grad proj function evals  = %-10ld\n",
          (LONG) pasadata->Stats->pasa->gpnf) ;
    printf(" # grad proj gradient evals  = %-10ld\n",
          (LONG) pasadata->Stats->pasa->gpng) ;
    printf(" # cg iterations             = %-10ld\n",
          (LONG) pasadata->Stats->cg->iter) ;
    printf(" # cg function evals         = %-10ld\n",
          (LONG) pasadata->Stats->cg->nfunc) ;
    printf(" # cg gradient evals         = %-10ld\n",
          (LONG) pasadata->Stats->cg->ngrad) ;
    printf(" # projections               = %-10ld\n",
          (LONG) pasadata->Stats->pasa->nproject) ;
    printf(" # Cholesky factorizations   = %-10i\n",
           pasadata->Stats->pproj->nchols) ;
    printf(" || P (x - g) - x ||         = %-16.7e\n",
          pasadata->Stats->pasa->err) ;
    printf(" Final f                     = %-16.7e\n",
          pasadata->Stats->pasa->f) ;

    printf("\n ***********************************************************"
           "*******\n\n") ;
    /* Note that the error tolerance in pasa is specified by parameter
       grad_tol (default 1.e-6). */
 
    /* There is some checking of the input data. For example, if the
       bounds are invalid in the sense that lo [i] > hi [i] for some i,
       then an error is reported when the code is run. As an example,
       we use the following invalid bounds. */
    pasadata->lo [3] = 2 ;
    pasadata->hi [3] = -1 ;
    printf ("!! Output when invalid bounds intentionally given to pasa !! \n") ;

    /* call pasa */
    pasa (pasadata) ; 

    /* The statistics and parameter values can also be printed
       during the pasa run by setting parameter values. For example,
       to print the the statistics and parameter values,
       the parameter values are set as follows: */
    pasadata->Parms->pasa->PrintStat = TRUE ;
    pasadata->Parms->pasa->PrintParm = TRUE ;

    /* use pasa_terminate to free the pasadata structure and all the memory
       that was malloc'd for the pasadata structure. */
    pasa_terminate (&pasadata) ;

    /* Note that pasa_terminate does not free any memory malloc'd by the user.
       Thus if the user malloc's pasadata->x when specifying the
       starting guess, then the user needs to free it. */

    /* exit the program */
    return (0) ;
}

void pasa_value
(
    PASAFLOAT *val,
    PASAFLOAT   *x,
    PASAINT      n
)
{
    PASAFLOAT f, t1, t2, t3 ;
    PASAINT i ;

    f = 0 ; /* initialize function value f */

    for (i = 0; i < n - 1; i++)
    {
        t1 = x [i] ;
        t2 = x [i + 1] - t1 * t1 ;
        t3 = t1 - 1 ;
        f += 100 * t2 * t2 + t3 * t3 ;
    }

    *val = f;
}

void pasa_grad
(
    PASAFLOAT *g,
    PASAFLOAT *x,
    PASAINT    n
)
{
    PASAFLOAT t0, t1, t2, t3 ;
    PASAINT i ;

    t1 = x [0] ;
    t0 = 200*(x [1] - t1*t1) ;
    g [0] = 2*(t1 - 1 - t0*t1) ;
    for (i = 1; i < n - 1; i++)
    {
        t1 = x [i] ;
        t2 = 200*(x [i + 1] - t1 * t1) ;
        t3 = t1 - 1 ;
        g [i] = 2*(t3 - t2*t1)  + t0 ;
        t0 = t2 ;
    }
    g [i] = t2 ;                        /* last entry of gradient */
}

void pasa_valgrad
(
    PASAFLOAT *val,
    PASAFLOAT   *g,
    PASAFLOAT   *x,
    PASAINT      n
)
{
    PASAFLOAT f, t0, t1, t2, t3 ;
    PASAINT i ;

    t1 = x [0] ;
    t3 = t1 - 1 ;
    t0 = 200*(x [1] - t1*t1) ;
    g [0] = 2*(t3 - t0*t1) ;
    f = 0.0025*t0*t0 + t3*t3 ;

    for (i = 1; i < n - 1; i++)
    {
        t1 = x [i] ;
        t2 = 200*(x [i + 1] - t1 * t1) ;
        t3 = t1 - 1 ;
        g [i] = 2*(t3 - t2*t1)  + t0 ;
        f += 0.0025*t2*t2 + t3*t3 ;
        t0 = t2 ;
    }
    g [i] = t2 ;
    *val = f ;
}
