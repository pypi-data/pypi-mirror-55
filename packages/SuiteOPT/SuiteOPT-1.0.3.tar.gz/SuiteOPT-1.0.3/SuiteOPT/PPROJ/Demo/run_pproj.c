/* ========================================================================== */
/* Read in a polyhedron in the form:

                 bl <= Ax <= bu,  lo <= x <= hi

   and project an infeasible point onto the polyhedron */
/* ========================================================================== */

#include "pproj.h"

int main (void /*int argc, char **argv*/)
{
    char s [300], *testprobs, *probname, fullpathname [3000] ;
    PPINT i, j, p, nrow, ncol, anz, ni ;
    int probnum, status ;
    PPFLOAT t, errb, errx, absAx, err, normx,
          *bu, *bl, *Ax, *lo, *hi, *x, *y ;
    double tic, elapsed ;
    FILE *f, *namefile ;
    PPINT *Ap, *Ai ;
    PPdata *ppdata ;

    testprobs = "Probs/" ;
    namefile = fopen ("names", "r") ;
    /* ---------------------------------------------------------------------- */
    /* read problem names */
    /* ---------------------------------------------------------------------- */

    probnum = 0 ;
    while (fgets (s, 300, namefile) != (char *) NULL)
    {
        probnum++ ;
        for (probname = s; *probname; probname++)
        {
            if (isspace (*probname)) *probname = '\0' ;
        }
        probname = s ;
        strcpy (fullpathname, testprobs) ;
        strcat (fullpathname, probname) ;
        /* read in the problem and put pointers in ppdata structure */
        printf ("reading problem: %s\n", fullpathname) ;
        f = fopen (fullpathname, "r") ;
        if (f == (FILE *) NULL)
        {
            printf ("file %s not found\n", fullpathname) ;
            pproj_error (-1, __FILE__, __LINE__, "stop\n") ;
        }

        /* read the number of rows, columns, and nonzeros in matrix */
        long I, Nrow, Ncol, Anz ;
        fscanf (f, "%ld %ld %ld\n", &Nrow, &Ncol, &Anz) ;

        /* create the ppdata structure */
        ppdata = pproj_setup() ;
        if ( ppdata == NULL )
        {
            pproj_error (-1, __FILE__, __LINE__,
                         "Out of memory in pproj_setup\n") ;
        }

        /* fill in the data structure */
        anz = Anz ;
        ppdata->nrow = nrow = Nrow ;
        ppdata->ncol = ncol = Ncol ;
        ppdata->Ap = Ap = (PPINT *) malloc ((ncol+1)*sizeof (PPINT)) ;
        ppdata->Ai = Ai = (PPINT *) malloc (anz*sizeof (PPINT)) ;
        ppdata->Ax = Ax = (PPFLOAT *) malloc (anz*sizeof (PPFLOAT)) ;
        ppdata->lo = lo = (PPFLOAT *) malloc (ncol*sizeof (PPFLOAT)) ;
        ppdata->hi = hi = (PPFLOAT *) malloc (ncol*sizeof (PPFLOAT)) ;
        ppdata->bu = bu = (PPFLOAT *) malloc (nrow*sizeof (PPFLOAT)) ;
        ppdata->bl = bl = (PPFLOAT *) malloc (nrow*sizeof (PPFLOAT)) ;
        ppdata->y  =  y = (PPFLOAT *) malloc (ncol*sizeof (PPFLOAT)) ;

        /* read the matrix */
        for (j = 0; j <= ncol; j++)
        {
            fscanf (f, "%ld\n",  &I) ;
            Ap [j] = I ;
        }
        for (p = 0; p < anz ; p++)
        {
            fscanf (f, "%ld\n", &I) ;
            Ai [p] = I ;
        }
        for (p = 0; p < anz ; p++)
        {
            fscanf (f, "%lg\n", Ax+p) ;
            if ( Ax [p] == 0 )
            {
                printf ("error: Ax [%ld] == 0 on input", (LONG) p) ;
                printf ("(input matrix should be in sparse format)\n") ;
                pproj_error (-1, __FILE__, __LINE__, "stop\n") ;
            }
        }

        /* read the bounds on the variables */
        for (j = 0; j < ncol ; j++)
        {
            fscanf (f, "%lg %lg\n", lo+j, hi+j) ;
        }
        for (i = 0; i < nrow ; i++)
        {
            fscanf (f, "%lg %lg\n", bl+i, bu+i) ;
        }
        fclose (f) ;

        /* read the infeasible point */
        strcpy (fullpathname, testprobs) ;
        strcat (fullpathname, "InfeasiblePoints/");
        strcat (fullpathname, probname) ;
        /* printf ("reading point: %s\n", fullpathname) ;*/
        f = fopen (fullpathname, "r") ;
        if (f == (FILE *) NULL)
        {
            printf ("file %s not found\n", fullpathname) ;
            pproj_error (-1, __FILE__, __LINE__, "stop\n") ;
        }
        for (j = 0; j < ncol ; j++)
        {
            fscanf (f, "%lg\n", y+j) ;
        }
        fclose (f) ; 

        /* before calling pproj, set any nondefault parameter values
           in ppdata->Parm */
        tic = pproj_timer () ;
        status = pproj (ppdata) ; 
        elapsed = pproj_timer () - tic ;

        /* print the status of the run to check that it was successful */
        pproj_print_status (ppdata) ;

        /* evaluate relative error in computed solution by comparing with
           relatively high accuracy solution stored in the Solutions directory*/
        strcpy (fullpathname, testprobs);
        strcat (fullpathname, "Solutions/");
        strcat (fullpathname, probname) ;
        printf ("location of solution: %s\n", fullpathname) ;
        f = fopen (fullpathname, "r") ;
        if (f == (FILE *) NULL)
        {
            printf ("file %s not found\n", fullpathname) ;
            pproj_error (-1, __FILE__, __LINE__, "stop\n") ;
        }

        /* The problem solution is stored in ppdata->x. A high accuracy
           solution was put in the directory Probs/Solutions. Below we
           read in the high accuracy solution and compare it to the
           computed solution. The computing tolerance is stored in
           ppdata->grad_tol (default 1.e-10). */
        err = 0. ;
        normx = 0. ;
        x = ppdata->x ;
        for (j = 0; j < ncol; j++)
        {
            fscanf (f, "%lg\n", &t) ;
            if ( fabs (t) > normx )
            {
                normx = fabs (t) ;
            }
            if ( fabs (x [j] - t) > err )
            {
                err = fabs (x [j] - t) ;
            }
        }
        fclose (f) ;

        if ( normx > 0. )
        {
            err /= normx ;
        }

        ni = 0 ;
        for (i = 0; i < nrow; i++)
        {
            if ( bl [i] < bu [i] ) ni++ ;
        }

        printf ("\n======================================================\n") ;
        printf ("---------- Problem Description ----------\n") ;
        printf ("problem ................................. %s\n", probname) ;
        printf ("   location: %s\n", testprobs) ;
        printf ("relative error in solution .............. %e\n", err) ;
        printf ("solution status ......................... %i\n", status) ;
        printf ("number of rows .......................... %ld\n", (LONG) nrow);
        printf ("number of columns ....................... %ld\n", (LONG) ncol);
        printf ("number of strict inequalities ........... %ld\n", (LONG) ni) ;
        printf ("run time ................................ %e\n", elapsed) ;

        /* pproj_KKTerror estimates the KKT error */
        t = pproj_KKTerror (&errb, &errx, &absAx, ppdata) ;

        printf ("\n----------- Error Statistics ------------\n") ;
        printf ("specified tolerance ..................... %e\n",
                ppdata->Parm->grad_tol) ;
        printf ("rel. sup norm of dual function gradient . %e\n", errb) ;
        printf ("relative diff between x & dual minimizer  %e\n", errx) ;
        printf ("absAx ................................... %e\n", absAx) ;

        /* print the statistics for the run */
        pproj_print_stat (ppdata) ;

        printf ("======================================================\n") ;
#ifndef NDEBUG
        if ( (status != PPROJ_SOLUTION_FOUND) &&
             (status != PPROJ_ERROR_DECAY_STAGNATES) )
        {
            pproj_error (-1, __FILE__, __LINE__, "problem not solved\n") ;
        }
#endif

        /* free memory that I created */
        free (bu) ;
        free (bl) ;
        free (Ap) ;
        free (Ai) ;
        free (Ax) ;
        free  (y) ;
        if ( lo != NULL)
        {
            free (lo) ;
        }
        if ( hi != NULL )
        {
            free (hi) ;
        }
        /* Routine pproj_terminate frees the ppdata structure along with
           any arrays created by pproj, such as ppdata->x and ppdata->lambda.
           If the user creates ppdata->x or ppdata->lambda, then they are
           not touched by pproj_terminate. */
        pproj_terminate (&ppdata) ;

    } /* read the next problem */
    fclose (namefile) ;
    return (0) ;
}
