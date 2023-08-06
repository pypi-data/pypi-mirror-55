/* ========================================================================== */
/* === Source/napheap_print.c =============================================== */
/* ========================================================================== */

/* user-callable functions for printing napheap parameters and statistics. */

#include "napheap.h"
#include <stdio.h>

#ifdef MATLAB_MEX_FILE
#define LPAREN "("
#define RPAREN ")"
#define OFFSET 1
#else
#define LPAREN "["
#define RPAREN "]"
#define OFFSET 0
#endif

/* ========================================================================== */
/* === napheap_print_status ================================================= */
/* ========================================================================== */

/* print the status at termination of the napheap run */

void napheap_print_status
(
    NAPdata *Data
)
{
    NAPstat *Stat = Data->Stat ;
    int status = Stat->status ;
    printf ("\nNAPHEAP run status (Version %d.%d, %s):\n\n",
        NAPHEAP_MAIN_VERSION, NAPHEAP_SUB_VERSION, NAPHEAP_DATE) ;

    if ( status == NAPHEAP_STATUS_OK )
    {
        printf ("No errors detected by NAPHEAP when solving "
                "the knapsack problem.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_INFEASIBLE )
    {
        printf ("Knapsack problem in NAPHEAP is infeasible.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_UNBOUNDED )
    {
        printf ("Optimal value for the knapsack problem in NAPHEAP "
                "is -infinity.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_OUT_OF_MEMORY )
    {
        printf ("NAPHEAP ran out of memory.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_INVALID_N )
    {
        printf ("In NAPHEAP, the specified problem dimension "
                "is either missing or negative (%ld).\n", (LONG) Stat->kerror) ;
    }
    else if ( status == NAPHEAP_STATUS_INVALID_BOUNDS )
    {
        printf ("In NAPHEAP, the problem bounds are invalid since "
                "lo %s%ld%s = %e > hi %s%ld%s = %e.\n",
            LPAREN, (LONG) Stat->kerror + OFFSET, RPAREN, Stat->lobad,
            LPAREN, (LONG) Stat->kerror + OFFSET, RPAREN, Stat->hibad) ;
    }
    else if ( status == NAPHEAP_STATUS_INVALID_NEWTON )
    {
        printf ("In NAPHEAP, Newton's method can only be used when the "
                "Hessian diagonal is positive.\n") ;
        printf ("Check the values for parameters d_is_zero and d_is_pos.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_INVALID_D )
    {
        if ( Stat->dbad < 0 )
        {
            printf ("In NAPHEAP, the Hessian diagonal d is invalid "
                    "(d %s%ld%s = %e < 0).\n", LPAREN,
                     (LONG) Stat->kerror + OFFSET, RPAREN, Stat->dbad) ;
        }
        else
        {
            printf ("In NAPHEAP, the parameter Parm.d_is_pos is TRUE "
                    "but d %s%ld%s = 0\n", LPAREN,
                    (LONG) Stat->kerror + OFFSET, RPAREN) ;
        }
    }
    else if ( status ==  NAPHEAP_STATUS_CONFLICTING_PARM_D )
    {
        printf ("The parameters d_is_one, d_is_pos, and d_is_zero are "
                "assigned conflicting values.\n") ;
        printf ("For example, both d_is_zero and d_is_one are TRUE, which is "
                "impossible.\n") ;
        printf ("If d_is_one and d_is_zero are both FALSE, then the d argument "
                "of napheap cannot be NULL.\n") ;
    }
    else if ( status == NAPHEAP_STATUS_MISSING_PARM )
    {
        printf ("In NAPHEAP, the Parm structure of the input napdata\n"
                "is missing. This should be created by napheap_setup.") ;
    }
    else if ( status == NAPHEAP_STATUS_MISSING_STAT )
    {
        printf ("In NAPHEAP, the Stat structure of the input napdata\n"
                "is missing. This should be created by napheap_setup.") ;
    }
}

/* ========================================================================== */
/* === napheap_print_stat =================================================== */
/* ========================================================================== */

/* print the napheap statistics */
void napheap_print_stat
(
    NAPdata *Data
)
{
    NAPstat *Stat = Data->Stat ;
    if (Stat == NULL)
    {
        return ;
    }

    printf ("\nNAPHEAP statistics (Version %d.%d, %s):\n",
        NAPHEAP_MAIN_VERSION, NAPHEAP_SUB_VERSION, NAPHEAP_DATE) ;

    printf ("Stat.nkf (number of known free variables):           %ld\n",
        (LONG) Stat->nkf) ;
    printf ("Stat.nfree (free variables in initial heap):         %ld\n",
        (LONG) Stat->nfree) ;
    printf ("Stat.nbound (bound variables in initial heap):       %ld\n",
        (LONG) Stat->nbound) ;
    printf ("Stat.nbrks (break points to reach initial solution): %ld\n",
        (LONG) Stat->nbrks) ;
    printf ("Stat.nrefine (break points during refinement):       %ld\n",
        (LONG) Stat->nrefine) ;
    printf ("Stat.nvarfix (variable fixing iterations):           %ld\n",
        (LONG) Stat->nvarfix) ;
    printf ("Stat.nnewton (number of Newton iterations):          %ld\n",
        (LONG) Stat->nnewton) ;
    printf ("Stat.nsecant (number of secant iterations):          %ld\n",
        (LONG) Stat->nsecant) ;
    printf ("\n") ;
}

/* ========================================================================== */
/* === napheap_print_parm ================================================== */
/* ========================================================================== */

void napheap_print_parm
(
    NAPdata  *Data        /* parameter structure */
)
{
    NAPparm *Parm, Default_Parm ;

    if ( Data == NULL ) Parm = NULL ;
    else                Parm = Data->Parm ;
    printf ("\nNAPHEAP parameter settings (Version %d.%d, %s):\n",
        NAPHEAP_MAIN_VERSION, NAPHEAP_SUB_VERSION, NAPHEAP_DATE) ;

    if (Parm == NULL)
    {
        /* initialize the default parameters */
        Parm = &Default_Parm ;
        napheap_default (Parm) ;
    }

    printf ("Parm.PrintStatus    ") ;
    if ( Parm->PrintStatus == TRUE )
    {
        printf ("TRUE (print the status of the run)\n") ;
    }
    else
    {
        printf ("FALSE (do not print the status of the run)\n") ;
    }

    printf ("Parm.PrintStat      ") ;
    if ( Parm->PrintStat == TRUE )
    {
        printf ("TRUE (print the statistics for the run)\n") ;
    }
    else
    {
        printf ("FALSE (do not print the statistics for the run)\n") ;
    }

    printf ("Parm.PrintParm      ") ;
    if ( Parm->PrintParm == TRUE )
    {
        printf ("TRUE (print the parameters used for the run)\n") ;
    }
    else
    {
        printf ("FALSE (do not print the parameters used for the run)\n") ;
    }

    printf ("Parm.use_prior_data ") ;
    if ( Parm->use_prior_data == TRUE )
    {
        printf ("TRUE (use internal arrays from previous run)\n") ;
    }
    else
    {
        printf ("FALSE (do not use arrays from previous run)\n") ;
    }

    printf ("Parm.return_data    ") ;
    if ( Parm->return_data == TRUE )
    {
        printf ("TRUE (return arrays from current run in napdata input\n"
                "                           argument of napheap)\n") ;
    }
    else
    {
        printf ("FALSE (do not return data arrays from current run)\n") ;
    }

    printf ("Parm.loExists       ") ;
    if ( Parm->loExists == TRUE )
    {
        printf ("TRUE (lower bounds on the variables are present)\n") ;
    }
    else
    {
        printf ("FALSE (lower bounds on the variables are treated as "
                "-infinity)\n") ;
    }

    printf ("Parm.hiExists       ") ;
    if ( Parm->hiExists == TRUE )
    {
        printf ("TRUE (upper bounds on the variables are present)\n") ;
    }
    else
    {
        printf ("FALSE (upper bounds on the variables are treated as "
                "+infinity)\n") ;
    }

    printf ("Parm.Aexists        ") ;
    if ( Parm->Aexists == TRUE )
    {
        printf ("TRUE (the linear constraint bl <= a'x <= bu is present)\n") ;
    }
    else
    {
        printf ("FALSE (the only constraints are bound constraints "
                "lo <= x <= hi)\n") ;
    }

    printf ("Parm.d_is_zero:     ") ;
    if ( Parm->d_is_zero )
    {
        printf ("TRUE (diagonal of objective Hessian is zero)\n") ;
        printf ("                          d argument of napheap and "
                                    "Parm.d_is_pos are ignored\n") ;
    }
    else
    {
        printf ("FALSE (d, diagonal of objective Hessian is nonzero)\n");
    }

    printf ("Parm.d_is_one:      ") ;
    if ( Parm->d_is_one )
    {
        printf ("TRUE (diagonal of objective Hessian is identically one)\n") ;
        printf ("                           d argument of napheap and "
                                    "Parm.d_is_pos are ignored\n") ;
    }
    else
    {
        printf ("FALSE (d, diagonal of objective Hessian is not all one)\n") ;
    }

    printf ("Parm.d_is_pos:      ") ;
    if ( Parm->d_is_pos )
    {
        printf ("TRUE (diagonal of objective Hessian is strictly positive)\n") ;
        printf ("                          Parm.d_is_pos ignored if either "
                                    "Parm.d_is_zero or\n") ;
        printf ("                          Parm.d_is_one are TRUE\n") ;
    }
    else
    {
        printf ("FALSE (d, diagonal of objective Hessian can have either\n") ;
        printf ("                                   "
                "positive or zero entries)\n") ;
    }

    printf ("Parm.refine:        ") ;
    if ( Parm->refine )
    {
        printf ("TRUE (perform refinement step)\n") ;
        printf ("Parm.err:           %e (solution refined if constraint"
            " violation exceeds this value)\n", Parm->err) ;
    }
    else
    {
        printf ("FALSE (do not perform refinement step)\n") ;
        printf ("Parm.err:           ignored (only used for refinement)\n") ;
    }

    printf ("Parm.K:             ") ;
    if ( Parm->K <= 0 )
    {
        printf ("0 (only use break point searching algorithm)\n") ;
        printf ("Parm.newton:        ignored (only used if K > 1)\n") ;
    }
    else
    {
        printf ("%d (max number of Newton or variable fixing iterations)\n",
                Parm->K) ;
        printf ("Parm.newton:        ") ;
        if ( Parm->newton )
        {
            printf ("TRUE (use Newton's method)\n") ;
            printf ("Parm.newton_scale:  ") ;
            printf ("%6.4f (multiply Newton step by this factor)\n",
                    Parm->newton_scale) ;
        }
        else
        {
            printf ("FALSE (use variable fixing algorithm)\n") ;
        }
    }

    printf ("Parm.decay:         ") ;
    printf ("%6.4f (recompute L'' when it decreases by decay factor)\n",
             Parm->decay) ;

    printf ("Parm.check:         ") ;
    if ( Parm->check )
    {
        printf ("TRUE (check the problem data for consistency)\n") ;
    }
    else
    {
        printf ("FALSE (do not check the problem data)\n") ;
    }
}
