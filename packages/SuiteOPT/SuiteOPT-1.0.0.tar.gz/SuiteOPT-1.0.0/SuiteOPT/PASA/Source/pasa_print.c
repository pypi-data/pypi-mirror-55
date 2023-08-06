/* ==========================================================================
   === pasa_print_status ====================================================
   ==========================================================================
    Print the status at termination of the run
   ========================================================================== */
#include "pasa.h"
#ifdef MATLAB_MEX_FILE
#define LPAREN "("
#define RPAREN ")"
#define OFFSET 1
#else
#define LPAREN "["
#define RPAREN "]"
#define OFFSET 0
#endif

void pasa_print_status
(
    PASAdata *Data  /* pasa data structure */
)
{
    PASAstats *Stats = Data->Stats ;
    int status = Stats->pasa->status ;
    /* check to see if status arose in any of the routines called by pasa */
    if ( (status >= PPROJ_START_MESSAGES) && (status <= PPROJ_END_MESSAGES) )
    {
#ifndef NOPPROJ
        Stats->pproj->status = status ;
        pproj_print_status (Data->ppdata) ;
#endif
    }
    else if ( (status >= CG_START_MESSAGES) && (status <= CG_END_MESSAGES) )
    {
        cg_print_status (Data->cgdata) ;
    }
    else if ( (status >= NAPHEAP_START_MESSAGES) &&
              (status <= NAPHEAP_END_MESSAGES) )
    {
        Stats->napheap->status = status ;
        napheap_print_status (Data->napdata) ;
    }
    else /* status arose in pasa itself */
    {
        PASAstat *pasastat = Stats->pasa ;
        printf ("\nPASA run status (Version %d.%d, %s):\n\n",
                   PASA_MAIN_VERSION, PASA_SUB_VERSION, PASA_DATE) ;

        if ( status == PASA_ERROR_TOLERANCE_SATISFIED )
        {
            printf ("PASA success: Error %e satisfies error "
                    "tolerance %e.\n", pasastat->err, pasastat->grad_tol) ;
        }
        else if ( status == PASA_POLYHEDRON_INFEASIBLE )
        {
            printf ("Input polyhedron for PASA is infeasible\n") ;
        }
        else if ( status == PASA_INVALID_VARIABLE_BOUNDS )
        {
            printf ("In PASA, the variables bounds are invalid since\n"
                    "    lo %s%ld%s = %e > hi %s%ld%s = %e.\n",
            LPAREN, (LONG) pasastat->ibad+OFFSET, RPAREN, pasastat->lobad, 
            LPAREN, (LONG) pasastat->ibad+OFFSET, RPAREN, pasastat->hibad) ;
        }
        else if ( status == PASA_INVALID_LINEAR_CONSTRAINT_BOUNDS )
        {
            printf ("In PASA, the linear equation bounds are invalid since\n"
                    "    lo %s%ld%s = %e > hi %s%ld%s = %e.\n",
            LPAREN, (LONG) pasastat->ibad+OFFSET, RPAREN, pasastat->lobad, 
            LPAREN, (LONG) pasastat->ibad+OFFSET, RPAREN, pasastat->hibad) ;
        }
        else if ( status == PASA_INVALID_MATRIX_ELEMENT )
        {
            printf ("In PASA, a matrix element in row %ld or right "
                    "side was infinite\n", (LONG) pasastat->ibad) ;
        }
        else if ( status == PASA_ITERATIONS_EXCEED_MAXITS_IN_GRAD_PROJ )
        {
            printf ("Number of iterations in the PASA gradient projection "
                    "routine exceeds the parameter gpmaxit = %ld\n",
                    (LONG) pasastat->gpmaxit) ;
        }
        else if ( status == PASA_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS_IN_GRAD_PROJ)
        {
            printf ("After %i attempts (Parm.maxsteps), the PASA gradient\n"
                    "projection routine, was unable to find an acceptable\n"
                    "step in the line search\n", pasastat->maxsteps) ;
        }
        else if ( status == PASA_LINE_SEARCH_STEPS_EXCEED_MAXSTEPS_IN_ACTIVEGP)
        {
            printf ("After %i attempts (Parm.maxsteps), the PASA active\n"
                    "set gradient projection routine, was unable to find\n"
                    "an acceptable step in the line search.\n",
                     pasastat->maxsteps) ;
        }
        else if ( status == PASA_OUT_OF_MEMORY )
        {
            printf ("PASA ran out of memory.\n") ;
        }
        else if ( status ==
                      PASA_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION_IN_GRAD_PROJ )
        {
            printf ("In PASA, a search direction in the gradient projection "
                    "was not a descent direction\n") ;
        }
        else if ( status ==
                      PASA_SEARCH_DIRECTION_NOT_DESCENT_DIRECTION_IN_ACTIVEGP )
        {
            printf ("In PASA, a search direction in active set gradient "
                    "projection routine was not a descent direction\n") ;
        }
        else if ( status == PASA_MUST_USE_CHOLMOD )
        {
            printf ("User specifies no CHOLMOD in PASA, while the code "
                    "currently requires CHOLMOD\n") ;
        }
        else if ( status == PASA_STARTING_FUNCTION_VALUE_INFINITE_OR_NAN)
        {
            printf ("Objective value in PASA is infinite or nan at either the\n"
                    "starting point or its projection on the polyhedron.\n") ;
        }
        else if ( status == PASA_FUNCTION_NAN_OR_INF )
        {
            printf ("The line search in PASA could not locate a finite "
                    "objective value\nafter Parm->ninf_tries attempts.\n") ;
            printf ("-- currently Parm->ninf_tries = %i\n",
                    pasastat->ninf_tries) ;
        }
        else if ( status == PASA_LAMBDA_IS_NULL_BUT_USE_LAMBDA_IS_TRUE )
        {
            printf ("The parameter use_lambda was TRUE, however, the\n"
                    "lambda input argument of PASA is NULL.\n") ;
        }
        else if ( status == PASA_MATRIX_INCOMPLETE )
        {
            printf ("The sparse matrix input to PASA requires three arrays\n"
                    "Ap, Ai, and Ax. At least one of these is missing.\n") ;
        }
        else if ( status == PASA_FUNCTION_VALUE_OR_GRADIENT_MISSING )
        {
            printf ("PASA needs both a function value and its gradient,\n"
                    "but only one of these was provided.\n") ;
        }
        else if ( status == PASA_MATRIX_GIVEN_BUT_RHS_MISSING )
        {
            printf ("The polyhedral matrix in PASA was given, but the\n"
                    "right and left side vectors are both missing.\n") ;
        }
        else if ( status == PASA_RHS_GIVEN_BUT_MATRIX_MISSING )
        {
            printf ("The right or left side vectors describing the\n"
                    "polyhedral constraint in PASA were given, but the\n"
                    "matrix is missing.\n") ;
        }
        else if ( status == PASA_MISSING_OBJECTIVE )
        {
            printf ("The objective function in PASA is missing\n") ;
        }
        else if ( status == PASA_PROBLEM_OVERSPECIFIED )
        {
            printf ("The user chose more than one of the problem classes in\n"
                    "the pasaparm structure to be TRUE. If the user does not\n"
                    "employ the autodetect feature and chooses the problem\n"
                    "class, then only one of the problem classes can be set\n"
                    "to TRUE.\n") ;
        }
        else if ( status == PASA_BOTH_A_AND_A_EXIST )
        {
            printf ("In PASA, both the sparse matrix Ap, Ai, Ax, and the\n"
                     "dense vector pasadata->a exist. If the matrix has just\n"
                     "one row, it can be input using the dense vector\n"
                     "pasadata->a. Otherwise, it should be input using the\n"
                     "sparse matrix.\n") ;
        }
        else if ( status == PASA_WRONG_HPROD_GIVEN )
        {
            printf ("The problem provided to PASA seems to be a quadratic\n"
                    "program with constraints, however, the user provided the\n"
                    "routine pasadata->cg_hprod, which corresponds to an\n"
                    "unconstrained problem. When the problem has constraints,\n"
                    "provide the routine pasadata->hprod which has an\n"
                    "has an additional argument.\n") ;
        }
        else if ( status == PASA_PROBLEM_DIMENSION_NOT_GIVEN )
        {
            printf ("The input data structure provided to PASA does not\n"
                    "contain a value for pasadata->ncol (the problem\n"
                    "dimension). A value for pasadata->ncol must be given.\n") ;
        }
        else if ( status == PASA_QUADRATIC_OBJECTIVE_NO_LINEAR_TERM )
        {
            printf ("The problem input to PASA has a quadratic objective\n"
                    "but the linear term is not specified.\n") ;
        }
    }
    fflush (stdout) ;
}

void pasa_print_stat
(
    PASAdata *Data  /* pasa data structure */
)
{
    PASAstat *Stat = Data->Stats->pasa ;
    if ( Stat == NULL ) return ;

    printf ("\nPASA run statistics (Version %d.%d, %s):\n",
        PASA_MAIN_VERSION, PASA_SUB_VERSION, PASA_DATE) ;

    printf("|| P (x - g) - x ||                   : %-25.15e\n", Stat->err);
    printf("Final f                               : %-25.15e\n\n", Stat->f);

    printf("Iterations of gradient projection (GP): %-10ld\n",
          (LONG) Stat->gpit) ;
    printf("Iterations of active set GP           : %-10ld\n",
          (LONG) Stat->agpit) ;

    printf("Function evaluation in main code      : %-10ld\n",
          (LONG) Stat->mcnf) ;
    printf("Function evaluations in GP            : %-10ld\n",
          (LONG) Stat->gpnf) ;
    printf("Function evaluations in active set GP : %-10ld\n",
          (LONG) Stat->agpnf) ;

    printf("Gradient evaluations in main code     : %-10ld\n",
          (LONG) Stat->mcng) ;
    printf("Gradient evaluations in GP            : %-10ld\n",
          (LONG) Stat->gpng) ;
    printf("Gradient evaluations in active set GP : %-10ld\n",
          (LONG) Stat->agpng) ;
    printf ("\n") ;
}

/* ==========================================================================
   === pasa_print_stats =====================================================
   ==========================================================================
    Print the statistics for all routines called by pasa
   ========================================================================== */
void pasa_print_stats
(
    PASAdata *Data  /* pasa data structure */
)
{
    if ( Data == NULL ) return ;

    PASAstats *Stats = Data->Stats ;
    if ( Stats->use_pasa == TRUE )
    {
        pasa_print_stat (Data) ;
    }
#ifndef NOPPROJ
    if ( Stats->use_pproj == TRUE )
    {
        pproj_print_stat (Data->ppdata) ;
    }
#endif
    if ( Stats->use_napheap == TRUE )
    {
        napheap_print_stat (Data->napdata) ;
    }
    if ( Stats->use_cg == TRUE )
    {
        cg_print_stat (Data->cgdata) ;
    }
}

/* ==========================================================================
   === pasa_print_parms =====================================================
   ==========================================================================
    Print the parameters for all routines called by pasa
   ========================================================================== */
void pasa_print_parms
(
    PASAdata *Data  /* pasa data structure */
)
{
    if ( Data == NULL ) return ;

    pasa_print_parm (Data) ;
    cg_print_parm (Data->cgdata) ;
    napheap_print_parm (Data->napdata) ;
#ifndef NOPPROJ
        pproj_print_parm (Data->ppdata) ;
#endif
}

/* ==========================================================================
   === pasa_print_parm ======================================================
   ==========================================================================
    Print values in PASAparm structure
   ========================================================================== */
void pasa_print_parm
(
    PASAdata *Data
)
{
    PASAparm *Parm = Data->Parms->pasa ;
    printf ("\nPASA parameter settings (Version %d.%d, %s):\n",
        PASA_MAIN_VERSION, PASA_SUB_VERSION, PASA_DATE) ;

    printf ("(see pasa_default for definitions)\n\n") ;
    printf ("UNC ...................................: ") ;
    pasa_print_TF (Parm->UNC) ;
    printf ("BNC ...................................: ") ;
    pasa_print_TF (Parm->BNC) ;
    printf ("LP ....................................: ") ;
    pasa_print_TF (Parm->LP) ;
    printf ("QP ....................................: ") ;
    pasa_print_TF (Parm->QP) ;
    printf ("NL ....................................: ") ;
    pasa_print_TF (Parm->NL) ;
    printf ("NAPSACK ...............................: ") ;
    pasa_print_TF (Parm->NAPSACK) ;
    printf ("PROJ ..................................: ") ;
    pasa_print_TF (Parm->PROJ) ;
    printf ("grad_tol ..............................: %e\n",
             Parm->grad_tol) ;
    printf ("PrintStatus ...........................: ") ;
    pasa_print_TF (Parm->PrintStatus) ;
    printf ("PrintStat .............................: ") ;
    pasa_print_TF (Parm->PrintStat) ;
    printf ("PrintParm .............................: ") ;
    pasa_print_TF (Parm->PrintParm) ;
    printf ("Print level (0 = none, 3 = maximum) ...: %i\n",
             Parm->PrintLevel) ;
    printf ("GradProjOnly ..........................: ") ;
    pasa_print_TF (Parm->GradProjOnly) ;
    printf ("use_activeGP ..........................: ") ;
    pasa_print_TF (Parm->use_activeGP) ;
    printf ("use_napheap ...........................: ") ;
    pasa_print_TF (Parm->use_napheap) ;
    printf ("use_hessian ...........................: ") ;
    pasa_print_TF (Parm->use_hessian) ;
    printf ("loExists ..............................: ") ;
    pasa_print_TF (Parm->loExists) ;
    printf ("hiExists ..............................: ") ;
    pasa_print_TF (Parm->hiExists) ;
    printf ("epsilon ...............................: %e\n",
             Parm->epsilon) ;
    printf ("cerr_decay ............................: %e\n",
             Parm->cerr_decay) ;
    printf ("EpsilonGrow ...........................: %e\n",
             Parm->EpsilonGrow) ;
    printf ("EpsilonDecay ..........................: %e\n",
             Parm->EpsilonDecay) ;
    printf ("fadjust ...............................: %e\n",
             Parm->fadjust) ;
    printf ("use_lambda ............................: ") ;
    pasa_print_TF (Parm->use_lambda) ;
    printf ("pproj_start_guess .....................: %i\n",
             Parm->pproj_start_guess) ;
    printf ("use_penalty ...........................: ") ;
    pasa_print_TF (Parm->use_penalty) ;
    printf ("penalty ...............................: %e\n",
             Parm->penalty) ;
    printf ("debug .................................: ") ;
    pasa_print_TF (Parm->debug) ;
    printf ("debugtol ..............................: %e\n",
             Parm->debugtol) ;
    printf ("switchfactor ..........................: %e\n",
             Parm->switchfactor) ;
    printf ("switchdecay ...........................: %e\n",
             Parm->switchdecay) ;
    printf ("terminate_agp .........................: %i\n",
             Parm->terminate_agp) ;
    printf ("testit ................................: %ld\n",
             (LONG) Parm->testit) ;
    printf ("GPtol .................................: %e\n",
             Parm->GPtol) ;
    printf ("gpmaxit ...............................: %ld\n",
             (LONG) Parm->gpmaxit) ;
    printf ("restart_fac ...........................: %e\n",
             Parm->restart_fac) ;
    printf ("L .....................................: %i\n",
             Parm->L) ;
    printf ("M .....................................: %i\n",
             Parm->M) ;
    printf ("P .....................................: %i\n",
             Parm->P) ;
    printf ("gamma1 ................................: %e\n",
             Parm->gamma1) ;
    printf ("gamma2 ................................: %e\n",
             Parm->gamma2) ;
    printf ("gamma3 ................................: %e\n",
             Parm->gamma3) ;
    printf ("lambda0 ...............................: %e\n",
             Parm->lambda0) ;
    printf ("lambda0Factor .........................: %e\n",
             Parm->lambda0Factor) ;
    printf ("bbk ...................................: %e\n",
             Parm->bbk) ;
    printf ("bbexpand ..............................: %e\n",
             Parm->bbexpand) ;
    printf ("bbSwitchFactor ........................: %e\n",
             Parm->bbSwitchFactor) ;
    printf ("MaximumCycle ..........................: %i\n",
             Parm->MaximumCycle) ;
    printf ("NominalCycle ..........................: %i\n",
             Parm->NominalCycle) ;
    printf ("approxstep ............................: ") ;
    pasa_print_TF (Parm->approxstep) ;
    printf ("ArmijoSwitchFactor ....................: %e\n",
             Parm->ArmijoSwitchFactor) ;
    printf ("PertRule ..............................: ") ;
    pasa_print_TF (Parm->PertRule) ;
    printf ("pert_eps ..............................: %e\n",
             Parm->pert_eps) ;
    printf ("Armijo_delta ..........................: %e\n",
             Parm->Armijo_delta) ;
    printf ("maxsteps ..............................: %i\n",
             Parm->maxsteps) ;
    printf ("stepdecay .............................: %e\n",
             Parm->stepdecay) ;
    printf ("safe0 .................................: %e\n",
             Parm->safe0) ;
    printf ("safe1 .................................: %e\n",
             Parm->safe1) ;
    printf ("infdecay ..............................: %e\n",
             Parm->infdecay) ;
    printf ("infdecay_rate .........................: %e\n",
             Parm->infdecay_rate) ;
    printf ("ninf_tries ............................: %i\n",
             Parm->ninf_tries) ;
}

void pasa_print_TF
(
    int TF /* TRUE or FALSE */
)
{
    if ( TF == TRUE )
    {
        printf ("TRUE\n") ;
    }
    else if ( TF == FALSE )
    {
        printf ("FALSE\n") ;
    }
    else
    {
        printf ("EMPTY\n") ;
    }
}
