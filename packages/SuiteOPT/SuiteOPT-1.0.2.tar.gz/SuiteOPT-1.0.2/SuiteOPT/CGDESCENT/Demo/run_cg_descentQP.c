/* -------------------------- Problem Details -------------------------- 
    This is a demo for solving the problem:
    
                min     0.5 sum_{i=1}^n  i*x_i^2 + x_i

    The primary purpose of this demo is to show the user how to utilize
    cg_descent's specialized routines for handling a quadratic objective. */

#include "cg_descent.h"

/* prototypes */
void hprod
(
    CGFLOAT   *val,
    CGFLOAT     *x,
    CGINT        n
) ;

int main (void)
{
    CGINT i, n ;

    CGdata *cgdata = cg_setup () ; /* initialize a CGdata structure */

    n = cgdata->n = 100 ; /* set problem dimension to 100 */
    /* since cgdata->x is not specified, the starting guess is x = 0 */

    /* Since the objective is a quadratic, we will provide the objective's
       linear cost vector and a routine hprod to evaluate the product
       between the objective Hessian and a vector. The routine hprod appears
       at the end of this code. */
    cgdata->hprod = hprod ;
    cgdata->c = cg_malloc (n*sizeof (CGFLOAT)) ; /* linear cost vector space */
    /* cg_descent has a special routine for setting all components of a real
       vector to the same value */
    cg_initx (cgdata->c, 1, n) ;

    /* by default, the run statistics are not printed. Set PrintStat to TRUE */
    cgdata->Parm->PrintStat = TRUE ;
    
    printf ("\nRun 1: print run statistics and first 4 components of x.\n") ;
    cg_descent (cgdata) ;

    printf ("x [1:4] =\n") ;
    for (i = 0; i < 4; i++) printf ("    %10.7f\n", cgdata->x [i]) ;

    /* to obtain the statistics structure, and not print the statistics,
       do the following */
    printf ("\nRun 2: use the Stat structure to print the number\n"
            "        of function and gradient evaluations. The problem is\n"
            "        solved quickly since the starting guess in cgdata->x\n"
            "        is the solution computed in Run 1.\n") ;
     
    /* Set PrintStat to FALSE */
    cgdata->Parm->PrintStat = FALSE ;

    cg_descent (cgdata) ;

    /* access the number of function and gradient evaluations from the
       Stat structure */
    printf ("Number of Function Evaluations: %i\n", cgdata->Stat->nfunc) ;
    printf ("Number of Gradient Evaluations: %i\n", cgdata->Stat->ngrad) ;

    /* free the memory allocated by the user for c */
    free (cgdata->c) ;

    /* free the workspace created by cg_setup, including the memory
       allocated by cg_descent for cgdata->x */
    cg_terminate (&cgdata) ;
}

/* hprod evaluates the product between the vector x and the Hessian matrix =
   diag (1, 2, ..., n) */
void hprod
(
    CGFLOAT *p,
    CGFLOAT *x,
    CGINT    n
)
{
    CGINT i ;
    for (i = 0; i < n; i++) p [i] = (i+1)*x [i] ;
}
