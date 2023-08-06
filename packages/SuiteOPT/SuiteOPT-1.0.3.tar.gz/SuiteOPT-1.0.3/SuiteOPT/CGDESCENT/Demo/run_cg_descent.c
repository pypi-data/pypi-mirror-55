/* -------------------------- Problem Details -------------------------- 
    This is a demo for solving the problem:
    
                min     0.5 sum_{i=1}^n exp (x_i) - sqrt(i)*x_i

    The routines for evaluating the objective and its gradient appear near
    the end of this file. */

#include "cg_descent.h"

/* prototypes */
void value
(
    CGFLOAT *f,
    CGFLOAT *x,
    CGINT    n
) ;

void grad
(
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT    n
) ;

void valgrad
(
    CGFLOAT *f,
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT    n
) ;

int main (void)
{
    CGINT i ;

    CGdata *cgdata = cg_setup () ; /* initialize a CGdata structure */

    cgdata->n = 1000 ; /* set problem dimension to 1000 */
    /* cgdata->x can be malloc'd and a starting guess provided.
       If there is no assignment to cgdata->x, then cg_descent will malloc
       cgdata->x and set the starting guess to x = zero. */

    /* the routines for evaluating the objective and its gradient appear at
       the end of this file */
    cgdata->value = value ;
    cgdata->grad  = grad ;

    /* run the code */
    cg_descent (cgdata) ;

    printf ("Run 1: no statistics, print first 4 components of x:\n") ;
    for (i = 0; i < 4; i++) printf ("  %10.7f\n", cgdata->x [i]) ;

    /* By default, cg_descent does not print statistics for the run.
       If you want the code to print the run statistics, then the
       parameter PrintStat, whose default value is FALSE, needs to be
       changed to TRUE. */
    cgdata->Parm->PrintStat = TRUE ;

    /* Note that cgdata->x now contains the solution, which becomes the
       starting guess for the next run of cg_descent. To make the statistics
       nontrivial, the first component of x is perturbed. */
    cgdata->x [0] = -1 ;

    printf ("\nRun 2: statistics are printed after the run is complete\n") ;

    cg_descent (cgdata) ;

    printf ("x [1:4] =\n") ;
    for (i = 0; i < 4; i++) printf ("  %10.7f\n", cgdata->x [i]) ;

    /* With a loss in speed, the valgrad argument of cg_descent has been
       omitted so far. Below, we also utilize the valgrad routine which
       evaluates the objective value and its gradient simultaneously.
       If the cg_descent has to evaluate both the objective and its gradient,
       it is usually faster to evaluate them simultaneously rather than
       evaluate first one and then the other. The running time comparison
       on a Dell T7610 was 0.00212 s for Run 2 versus 0.001476 s for Run 3.
       The number of iterations and function/gradient evaluations were
       identical. */
    cgdata->valgrad = valgrad ;

    printf ("\nRun 3: Repeat Run 2, but exploit valgrad\n") ;
    cgdata->x [0] = -1 ; /* perturb first component of x */

    cg_descent (cgdata) ;

    printf ("x [1:4] =\n") ;
    for (i = 0; i < 4; i++) printf ("  %10.7f\n", cgdata->x [i]) ;

    /* Note that the statistics are also returned in the structure
       cgdata->Stat. Below we print the number of gradient evaluations
       using the statistics structure. Note that cgdata->Stat contains
       the statistics structure even when cgdata->Parm->Stat = FALSE. */
    printf ("Number of Gradient Evaluations from the Stat structure: %i\n",
            cgdata->Stat->ngrad) ;

    /* Note that the run status message can be eliminated by
       setting cgdata->Parm->status = FALSE. Nonetheless the run status
       can be accessed in two different ways. First, it is returned by
       the cg_descent routine; that is, status = cg_descent (cgdata);
       second, it is contained in the Stat structure:
       status = cgdata->Stat->status.  If status = 0, then the error
       tolerance was satisfied. If the status is nonzero, then a text
       description of the error message is obtained by running
       "cg_print_status (cgdata)". */

    /* free the workspace created by cg_setup, including the memory
       allocated by cg_descent for cgdata->x */
    cg_terminate (&cgdata) ;
}

void value
(
    CGFLOAT *f,
    CGFLOAT *x,
    CGINT    n
)
{
    CGFLOAT t, s ;
    CGINT i ;
    s = 0. ;
    for (i = 0; i < n; i++)
    {
        t = i+1 ;
        t = sqrt (t) ;
        s += exp (x [i]) - t*x [i] ;
    }
    *f = s ;
}

void grad
(
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT    n
)
{
    CGFLOAT t ;
    CGINT i ;
    for (i = 0; i < n; i++)
    {
        t = i + 1 ;
        t = sqrt (t) ;
        g [i] = exp (x [i]) -  t ;
    }
}

void valgrad
(
    CGFLOAT *f,
    CGFLOAT *g,
    CGFLOAT *x,
    CGINT    n
)
{
    CGFLOAT ex, t, s ;
    CGINT i ;
    s = 0. ;
    for (i = 0; i < n; i++)
    {
        t = i + 1 ;
        t = sqrt (t) ;
        ex = exp (x [i]) ;
        s += ex - t*x [i] ;
        g [i] = ex -  t ;
    }
    *f = s ;
}
