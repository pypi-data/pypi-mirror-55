/* ========================================================================= */
/* === check_link ========================================================== */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_link
(
    PPcom     *I,
    int *joblist,
    int       nj,
    char  *where
)
{
    PPINT ncol, nrow, nf, ni, ni1, ni2, ntot, i, i0, i1, j, j0, j1, k,
          botblk, botrow, botcol, topblk, toprow, topcol, row,
          *RLinkUp, *RLinkDn, *F, *ir, *lLinkUp, *lLinkDn, *uLinkUp, *uLinkDn,
          *lstart, *ustart, *ineq_row, *Rstart, *row_start, *sol_start ;
    int status, jobnum, *ib, *ib_old, *leftdesc, *temp ;
    PPprob *Prob ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check links %s\n", where) ;

    Prob = I->Prob ;
    ncol = Prob->ncol ;
    nrow = Prob->nrow ;
    ni = Prob->ni + Prob->nsing ;
    ni1= ni + 1 ;
    ni2= ni + 2 ;
    ntot = ni + ncol + 1 ;

    PPINT const nsing = Prob->nsing ;

    W = I->Work ;
    ib_old = W->ib ;
    ir = W->ir ;

    /* allocate workspace */
    F    = pproj_malloc (&status, ncol, sizeof (PPINT)) ;
    ib   = pproj_malloc (&status, ncol, sizeof (int)) ;
    temp = pproj_malloc (&status, PPMAX (ntot, nrow), sizeof (int)) ;

    nf = 0 ;
    for (j = 0; j < ncol; j++)
    {
        ib [j] = ib_old [j] ;
        if ( ib [j] == 0 ) F [nf++] = j ;
    }

    RLinkUp = W->RLinkUp ;
    RLinkDn = W->RLinkDn ;

    uLinkUp = W->SLinkUp ;
    uLinkDn = W->SLinkDn ;
    lLinkUp = W->SLinkUp ;
    lLinkDn = W->SLinkDn ;

    for (j = 0; j < ncol; j++) temp [j] = 0 ;

    for (k = 0; k < nf; k++)
    {
        j = F [k] ;
        if ( (j < 0) || (j >= ncol) )
        {
            printf ("F: %ld, out of range 0 to %ld, at k: %ld\n",
                   (LONG) j, (LONG) ncol, (LONG) k) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( temp [j] == 1 )
        {
            printf ("F: %ld, appears twice at k: %ld\n", (LONG) j, (LONG) k) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        temp [j] = 1 ;
    }

    for (i = 0; i < nrow; i++) temp [i] = 0 ;
    i0 = nrow ;

    while ( (i1 = RLinkUp [i0]) < nrow )
    {
        if ( i1 < 0 )
        {
            printf ("RLinkUp: %ld less than zero at %ld\n",
                   (LONG) i1, (LONG) i0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( ir [i1] > ni )
        {
            printf ("row: %ld in RLinks but ir = %ld > ni = %ld\n",
                   (LONG) i1, (LONG) ir[i1], (LONG) ni) ;
            pproj_error (-1, __FILE__, __LINE__, "stop") ;
        }
        if ( RLinkDn [i1] != i0 )
        {
            printf ("RLinkDn: %ld, at %ld does not match Up at %ld\n",
                   (LONG) RLinkDn [i1], (LONG) i1, (LONG) i0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( temp [i1] != 0 )
        {
            printf ("%ld in RLinkUp appears twice in link\n", (LONG) i1) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        temp [i1] = 1 ;
        i0 = i1 ;
    }
    for (i = 0; i < nrow; i++)
    {
        if ( ir [i] <= ni )
        {
           if ( !temp [i] )
           {
               printf ("ir: %ld <= ni = %ld but row: %ld not in RLinks\n",
                      (LONG) ir [i], (LONG) ni, (LONG) i) ;
               pproj_error (-1, __FILE__, __LINE__, "stop") ;
           }
        }
    }
    if ( nj == 0 )
    {
        pproj_free (temp) ;
        pproj_free (ib) ;
        pproj_free (F) ;
        return ;
    }

/* check block structure */

    leftdesc = W->leftdesc ;
    sol_start = W->sol_start ;
    lstart = W->lstart ;
    ustart = W->ustart ;
    Rstart = W->Rstart ;
    row_start = W->row_start ;
    ineq_row = Prob->ineq_row ;

    for (jobnum = 0; jobnum < nj; jobnum++)
    {
        botblk = joblist [jobnum] ;
        botrow = row_start [botblk+1] ;
        topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
        toprow = row_start [topblk] ;
        for (i = toprow; i < botrow; i++) temp [i] = 0 ;
        i = Rstart [botblk] ;

        while ( i < botrow )
        {
            if ( i < toprow )
            {
                printf ("job: %i botblk: %ld row: %ld < toprow: %ld\n",
                        jobnum, (LONG) botblk, (LONG) i, (LONG) toprow) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
            if ( temp [i] == 1 )
            {
                printf ("job: %i botblk: %ld row: %ld repeats\n",
                        jobnum, (LONG) botblk, (LONG) i) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
            temp [i] = 1 ;
            if ( ir [i] > ni ) /* row was dropped */
            {
                printf ("job: %i botblk: %ld row: %ld ir: %ld, row in links "
                        "but inactive\n",
                        jobnum, (LONG) botblk, (LONG) i, (LONG) ir [i]) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
            i = RLinkUp [i] ;
        }
        for (i = toprow; i < botrow; i++)
        {
            if ( ir [i] <= ni )
            {
                if ( !temp [i] ) /* active rows should be in linked list above*/
                {
                    printf ("job: %i botblk: %ld row: %ld ir: %ld, "
                            "missing from links\n",
                            jobnum, (LONG) botblk, (LONG) i, (LONG) ir [i]) ;
                    pproj_error (-1, __FILE__, __LINE__, "stop") ;
                }
            }
        }
    }

    for (jobnum = 0; jobnum < nj; jobnum++)
    {
        botblk = joblist [jobnum] ;
        botcol = sol_start [botblk+1] ; /* first inequality row of next block */
        botrow = row_start [botblk+1] ;
        topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
        topcol = sol_start [topblk] ; /* first inequality row */
        toprow = row_start [botblk] ;

        for (j = topcol; j < botcol; j++) temp [j] = 0 ;
        j = ustart [botblk] ;

        while ( j < botcol )
        {
            if ( j < topcol )
            {
                printf ("check ustart, sol\n") ;
                printf ("job: %i botblk: %ld col: %ld < topcol: %ld\n",
                        jobnum, (LONG) botblk, (LONG) j, (LONG) topcol) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            if ( temp [j] == 1 )
            {
                printf ("job: %i botblk: %ld col: %ld repeats\n",
                        jobnum, (LONG) botblk, (LONG) j) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            i = ineq_row [j] ;
            if ( nsing ) k = 1 ;
            else         k = j ;
            if ( ir [i] != k )
            {
                printf("job: %i botblk: %ld col: %ld i: %ld ir: %ld, col in "
                       "ulinks but ir not = %ld\n",
                        jobnum, (LONG) botblk, (LONG) j, (LONG) i,
                        (LONG) ir [i], (LONG) k) ;
                printf ("column in ulinks but not at upper bound check\n") ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            temp [j] = 1 ;
            j = uLinkUp [j] ;
        }
    }

    for (jobnum = 0; jobnum < nj; jobnum++)
    {
        botblk = joblist [jobnum] ;
        botcol = sol_start [botblk+1] ;
        botrow = row_start [botblk+1] ;
        topblk = leftdesc [botblk] ;  /* blks in range topblk:botblk */
        topcol = sol_start [topblk] ;
        toprow = row_start [botblk] ;
        for (j = topcol; j < botcol; j++) temp [j] = 0 ;
        j = lstart [botblk] ;

        while ( j < botcol )
        {
            if ( j < topcol )
            {
                printf ("check lstart, sol\n") ;
                printf ("job: %d botblk: %ld col: %ld < topcol: %ld\n",
                        jobnum, (LONG) botblk, (LONG) j, (LONG) topcol) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
            if ( temp [j] == 1 )
            {
                printf ("job: %i botblk: %ld col: %ld repeats\n",
                        jobnum, (LONG) botblk, (LONG) j) ;
                pproj_error (-1, __FILE__, __LINE__, "stop") ;
            }
            i = ineq_row [j] ;
            if ( nsing ) k = 1 ;
            else         k = -j ;
            if ( ir [i] != k )
            {
                printf ("job: %i botblk: %ld col: %ld i: %ld ir: %ld, col in "
                        "llinks but ir not = %ld\n",
                         jobnum, (LONG) botblk, (LONG) j, (LONG) i,
                         (LONG) ir [i], (LONG) k) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            temp [j] = 1 ;
            j = lLinkUp [j] ;
        }
    }

    for (j = lLinkUp [ni1]; j <= ni; j = lLinkUp [j])
    {
        row = ineq_row [j] ;
        if ( nsing ) k = 1 ;
        else         k = -j ;
        if ( ir [row] != k )
        {
            printf("row: %ld ir: %ld row in lLink (j = %ld) when dropped\n",
                  (LONG) row, (LONG) ir [row], (LONG) j) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    for (j = uLinkUp [ni2]; j <= ni; j = uLinkUp [j])
    {
        row = ineq_row [j] ;
        if ( nsing ) k = 1 ;
        else         k = j ;
        if ( ir [row] != k )
        {
            printf("row: %ld ir: %ld row in uLink (j = %ld) when dropped\n",
                  (LONG) row, (LONG) ir [row], (LONG) j) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    for (j = 0; j <= ni; j++) temp [j] = 0 ;
    j0 = ni1 ;
    while ( (j1 = lLinkUp [j0]) <= ni )
    {
        if ( (j1 < 1 ) || (j1 > ni) )
        {
            printf ("lLinkUp: %ld, out of range %d to %ld at %ld\n",
                   (LONG) j1, 1, (LONG) ni, (LONG) j0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( lLinkDn [j1] != j0 )
        {
            printf ("lLinkDn: %ld, at %ld does not match Up at %ld\n",
                   (LONG) lLinkDn [j1], (LONG) j1, (LONG) j0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( temp [j1] != 0 )
        {
            printf ("%ld in lLinkUp appears twice in link\n", (LONG) j1) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        temp [j1] = 1 ;
        j0 = j1 ;
    }

    for (j = 0; j <= ni; j++) temp [j] = 0 ;
    j0 = ni2 ;
    while ( (j1 = uLinkUp [j0]) <= ni )
    {
        if ( (j1 < 1 ) || (j1 > ni) )
        {
            printf ("uLinkUp: %ld, out of range %i to %ld at %ld\n",
                   (LONG) j1, 1, (LONG) ni, (LONG) j0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( uLinkDn [j1] != j0 )
        {
            printf ("uLinkDn: %ld, at %ld does not match Up at %ld\n",
                   (LONG) uLinkDn [j1], (LONG) j1, (LONG) j0) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( temp [j1] != 0 )
        {
            printf ("%ld in uLinkUp appears twice in link\n", (LONG) j1) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        temp [j1] = 1 ;
        j0 = j1 ;
    }

/*  printf ("Links OK at %s\n", where) ; */

    /* free workspace */
    pproj_free (F) ;
    pproj_free (ib) ;
    pproj_free (temp) ;
}
