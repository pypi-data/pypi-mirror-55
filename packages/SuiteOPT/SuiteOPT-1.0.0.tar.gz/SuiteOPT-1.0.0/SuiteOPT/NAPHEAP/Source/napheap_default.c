/* ========================================================================== */
/* === napheap_default ====================================================== */
/* ========================================================================== */

/*  Set default parameter values for the napheap code. If the parameter
    argument of napheap is NULL, this routine is called automatically to
    set parameters to their default value.  If the user wishes to set
    parameter values, then the NAPparm structure should be declared
    in the main program. The user could call napheap_default to initialize
    the structure, and then individual elements in the structure
    could be changed, before passing the structure to napheap.
*/

#include "napheap.h"

void napheap_default
(
    NAPparm *Parm
)
{
    /* ---------------------------------------------------------------------- */
    /* Parm->PrintStatus */
    /* T => Print the status of the run */
    Parm->PrintStatus = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->PrintStat */
    /* T => Print the statistics for the run */
    Parm->PrintStat = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->PrintParm */
    /* T => Print the parameter values used for the run */
    Parm->PrintParm = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->use_prior_data */
    /* T => Use malloc'd arrays and data from a previous run.
            These arrays were saved during prior run by setting
            parameter return_data = TRUE */
    Parm->use_prior_data = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->return_data */
    /* T => Return malloc'd arrays for the current run in the
            input data structure napdata. This is useful when solving
            another problem where only the linear input data y changes. */
    Parm->return_data = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->loExists */
    /* T => the user provides lower bounds for the variables
       F => treat the lower bounds as -infinity
            Note: The lo argument of napheap is ignored, it could be NULL.
                  If the lo argument is NULL, then loExists is treated as F */
    Parm->loExists = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->hiExists */
    /* T => the user provides upper bounds for the variables
       F => treat the upper bounds as +infinity
            Note: The hi argument of napheap is ignored, it could be NULL.
                  If the hi argument is NULL, then hiExists is treated as F */
    Parm->hiExists = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->Aexists */
    /* T => there is a linear constraint bl <= a'x <= bu
       F => treat the upper bounds as +infinity */
    Parm->Aexists = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->d_is_pos: */
    /* T => all entries of diagonal of objective Hessian are > 0
       F => there could be zeros on the diagonal of the Hessian. */
    Parm->d_is_pos = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->d_is_zero: */
    /* T => all entries of diagonal of objective Hessian are zero
            Note: The d argument of napheap is ignored. It could be NULL
       F => there could be nonzeros on the diagonal of the Hessian. */
    Parm->d_is_zero = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->d_is_one: */
    /* T => diagonal of the objective Hessian is identically 1
            Note: The d argument of napheap is ignored. It could be NULL */
    Parm->d_is_one = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->K: */
    /* Upper bound on the number of Newton or variable fixing iterations.
       After performing these K iterations, the code switches to the break
       point search. The Newton algorithm also switches to the breakpoint
       search if two iterates are generated on opposite sides of the root. */
    Parm->K = 20 ;

    /* ---------------------------------------------------------------------- */
    /* Parm->newton: */
    /* T => use the Newton to update lambda, switch to the break point
            search either at iteration K or at the first time that two
            Newton iterates lie on opposite side of the root (whichever
            happens first)
       F => use K iterations of the variable fixing algorithm before
            switching to a breakpoint search */
    Parm->newton = TRUE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->newton_scale: */
    /* An ordinary Newton iteration often converges monotonically to the
       root. Hence, the Newton iterates are scaled by a factor greater than 1
       in an effort to produce an iterate on the opposite side of the root.
       When such an iterate is generated, the algorithm switches to a
       breakpoint search. The scaled iteration is given by

       lambda_new = lambda_old - newton_scale*L'(lambda_old)/L''(lambda_old) */

    Parm->newton_scale = 1.10 ;

    /* ---------------------------------------------------------------------- */
    /* Parm->decay: */
    /* To combat the effect of rounding errors, a2sum is recomputed whenever
       a2sum <= decay*a2max, the maximum a2sum encountered */
    Parm->decay = 0.01 ;

    /* ---------------------------------------------------------------------- */
    /* Parm->refine: */
    /* T => perform an iterative refinement step to improve solution accuracy
       F => no refinement
       Since the accuracy has been improved by monitoring the size of the
       a2sum variable, this parameter is ignored when d is positive.  In the
       next version of the code, this parameter will be removed. */
    Parm->refine = FALSE ;

    /* ---------------------------------------------------------------------- */
    /* Parm->err: */
    /* The solution is refined if |a'x - b| > err. This parameter will also
       be removed in the next version of the code. */
    Parm->err = NAPZERO ;

    /* ---------------------------------------------------------------------- */
    /* Parm->check: */
    /* Check the input parameters for dj < 0 or hij < loj or Bhi < Blo */
    Parm->check = FALSE ;
}
