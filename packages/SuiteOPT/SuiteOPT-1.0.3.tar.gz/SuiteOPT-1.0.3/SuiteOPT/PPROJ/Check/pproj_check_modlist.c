/* ========================================================================= */
/* === check_modlist ======================================================= */
/* ========================================================================= */

#include "pproj.h"
void pproj_check_modlist
(
    PPcom    *I,
    char *where
)
{
    PPINT *RowmodList, *ColmodList, *RowmodFlag, *ColmodFlag,
          *ColFlag, *RowFlag, *ir, *ineq_row,
           nrow, ncol, nrowadd, nrowdel, ncoladd, ncoldel, i, j, k, ni ;
    int status, *ib ;
    PPprob *Prob ;
    PPwork    *W ;

#ifdef NDEBUG
    fprintf (stderr, "Debugging is on!\n") ; abort () ;
#endif
    printf ("check mod list %s\n", where) ;

    Prob = I->Prob ;
    nrow = Prob->nrow ;
    ncol = Prob->ncol ;
    ni = Prob->ni + Prob->nsing ;
    ineq_row = Prob->ineq_row ;
    W = I->Work ;
    nrowadd = W->nrowadd ;
    nrowdel = W->nrowdel ;
    ncoladd = W->ncoladd ;
    ncoldel = W->ncoldel ;
    ir = W->ir ;
    ib = W->ib ;

    if ( nrowadd < 0 )
    {
        PRINTF ("nrowadd (%ld) < 0 at %s\n", (LONG) nrowadd, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    if ( nrowdel < 0 )
    {
        PRINTF ("nrowdel (%ld) < 0 at %s\n", (LONG) nrowdel, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    if ( ncoladd < 0 )
    {
        PRINTF ("ncoladd (%ld) < 0 at %s\n", (LONG) ncoladd, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    if ( ncoldel < 0 )
    {
        PRINTF ("ncoldel (%ld) < 0 at %s\n", (LONG) ncoldel, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }

    /* if ( nrowadd >= nrow )
    {
        PRINTF ("nrowadd (%i) >= nrow (%i) at %s\n", nrowadd, nrow, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }*/
    if ( nrowdel > nrow )
    {
        PRINTF ("nrowdel (%ld) >= nrow (%ld) at %s\n",
               (LONG) nrowdel, (LONG) nrow, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    if ( ncoladd > ncol )
    {
        PRINTF ("ncoladd (%ld) > ncol (%ld) at %s\n",
               (LONG) ncoladd, (LONG) ncol, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }
    if ( ncoldel > ncol )
    {
        PRINTF ("ncoldel (%ld) >= ncol (%ld) at %s\n",
                (LONG) ncoldel, (LONG) ncol, where) ;
        pproj_error (-1, __FILE__, __LINE__, where) ;
    }

    RowmodList = W->RowmodList ;
    RowmodFlag = W->RowmodFlag ;
    ColmodList = W->ColmodList ;
    ColmodFlag = W->ColmodFlag ;

/* check range of list */

    for (i = 1; i <= nrowadd; i++)
    {
        if ( RowmodList [nrow-i] < 0 )
        {
            PRINTF ("%ld. Add RowmodList [%ld] = %ld < 0 at %s\n",
                   (LONG) i, (LONG) nrow-i, (LONG) RowmodList [nrow-i], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( RowmodList [nrow-i] >= nrow )
        {
            PRINTF ("%ld. Add RowmodList [%ld] = %ld >= nrow (%ld) at %s\n",
                   (LONG) i, (LONG) (nrow-i), (LONG) RowmodList [nrow-i],
                   (LONG) nrow, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    for (i = 0; i < nrowdel; i++)
    {
        if ( RowmodList [i] < 0 )
        {
            PRINTF ("Del RowmodList [%ld] = %ld < 0 at %s\n",
                   (LONG) i, (LONG) RowmodList [i], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( RowmodList [i] >= nrow )
        {
            PRINTF ("Del RowmodList [%ld] = %ld >= nrow (%ld) at %s\n",
                   (LONG) i, (LONG) RowmodList [i], (LONG) nrow, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    for (i = 1; i <= ncoldel; i++)
    {
        if ( ColmodList [ncol-i] < 0 )
        {
            PRINTF ("%ld. Del ColmodList [%ld] = %ld < 0 in %s\n",
                   (LONG) i, (LONG) ncol-i, (LONG) ColmodList [i], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( ColmodList [ncol-i] >= ncol )
        {
            PRINTF ("%ld. Del ColmodList [%ld] = %ld >= ncol (%ld) in %s\n",
                   (LONG) i, (LONG) (ncol-i), (LONG) ColmodList [i],
                   (LONG) ncol, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
    for (i = 0; i < ncoladd; i++)
    {
        if ( ColmodList [i] < 0 )
        {
            PRINTF ("Add ColmodList [%ld] = %ld < 0 at %s\n",
                   (LONG) i, (LONG) ColmodList [i], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        if ( ColmodList [i] >= ncol )
        {
            PRINTF ("Add ColmodList [%ld] = %ld >= ncol (%ld) at %s\n",
                   (LONG) i, (LONG) ColmodList [i], (LONG) ncol, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

/*  look for repetitions in list */
    ColFlag = (PPINT *) pproj_malloc (&status, ncol, sizeof (PPINT)) ;
    RowFlag = (PPINT *) pproj_malloc (&status, nrow, sizeof (PPINT)) ;

    for (i = 0; i < nrow; i++) RowFlag [i] = EMPTY ;
    for (j = 0; j < ncol; j++) ColFlag [j] = EMPTY ;

    for (i = 1; i <= nrowadd; i++)
    {
        k = RowmodList [nrow-i] ;
        if ( RowFlag [k] != EMPTY )
        {
            PRINTF ("Add RowmodList [%ld] = %ld repeats at %s\n",
                   (LONG) i, (LONG) k, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        RowFlag [k] = 1 ;
    }

    for (i = 0; i < nrowdel; i++)
    {
        k = RowmodList [i] ;
        if ( RowFlag [k] != EMPTY )
        {
            PRINTF ("Del RowmodList [%ld] = %ld repeats at %s\n",
                   (LONG) (nrow-i), (LONG) k, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        RowFlag [k] = 1 ;
    }

    for (i = 1; i <= ncoldel; i++)
    {
        k = ColmodList [ncol-i] ;
        if ( ColFlag [k] != EMPTY )
        {
            PRINTF ("Del ColmodList [%ld] = %ld repeats at %s\n",
                   (LONG) i, (LONG) k, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        ColFlag [k] = 1 ;
    }

    for (i = 0; i < ncoladd; i++)
    {
        k = ColmodList [i] ;
        if ( ColFlag [k] != EMPTY )
        {
            PRINTF ("Add ColmodList [%ld] = %ld repeats at %s\n",
                   (LONG) (ncol-i), (LONG) k, where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
        ColFlag [k] = 1 ;
    }

/* check that the modflags are only nonempty when there is a row or column
   in modlist */

    for (i = 0; i < nrow; i++) RowFlag [i] = EMPTY ;
    for (i = 0; i < nrowdel; i++) RowFlag [RowmodList [i]] = i ;
    for (i = 1; i <= nrowadd; i++) RowFlag [RowmodList [nrow-i]] = nrow - i ;

    for (i = 0; i < nrow; i++)
    {
        if ( RowmodFlag [i] != EMPTY )
        {
            /* is the row in RowmodList? */
            if ( RowFlag [i] == EMPTY )
            {
                printf ("RowmodFlag: %ld nrowadd: %ld nrowdel: %ld nrow: %ld\n",
                       (LONG) RowmodFlag [i], (LONG) nrowadd, (LONG) nrowdel,
                       (LONG) nrow) ;
                printf ("RowmodList: %ld\n",
                       (LONG) RowmodList [RowmodFlag [i]]) ;
                PRINTF ("row %ld has flag set, but not in modlist (%s)\n",
                       (LONG) i, where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            /* does the RowmodFlag point to the correct row? */
            if ( RowFlag [i] != RowmodFlag [i] )
            {
                PRINTF("row%ld, RowmodFlag points to row %ld (incorrect), "
                       "%s\n",
                       (LONG) i, (LONG) RowmodList [RowmodFlag [i]], where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        else
        {
            if ( RowFlag [i] != EMPTY )
            {
                PRINTF ("row %ld is in the modList, but flag not set, %s\n",
                       (LONG) i, where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }

    for (j = 0; j < ncol; j++) ColFlag [j] = EMPTY ;
    for (j = 0; j < ncoladd; j++) ColFlag [ColmodList [j]] = j ;
    for (j = 1; j <= ncoldel; j++) ColFlag [ColmodList [ncol-j]] = ncol - j ;

    for (j = 0; j < ncol; j++)
    {
        if ( ColmodFlag [j] != EMPTY )
        {
            /* is the col in ColmodList? */
            if ( ColFlag [j] == EMPTY )
            {
                PRINTF ("col %ld has flag set, but not in modlist, %s\n",
                       (LONG) j, where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
            /* does the ColmodFlag point to the correct col? */
            if ( ColFlag [j] != ColmodFlag [j] )
            {
                PRINTF ("col %ld, ColmodFlag points to col %ld "
                        "(incorrect), %s\n",
                        (LONG) j, (LONG) ColmodList [ColmodFlag [j]], where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
        else
        {
            if ( ColFlag [j] != EMPTY )
            {
                PRINTF ("col %ld is in the modList, but flag not set, %s\n",
                       (LONG) j, where) ;
                pproj_error (-1, __FILE__, __LINE__, where) ;
            }
        }
    }

    /* free workspace */
    pproj_free (ColFlag) ;
    pproj_free (RowFlag) ;

/* check sign of ir and ib for compatibility with deletions and additions */
    for (i = 1; i <= nrowadd; i++)
    {
        k = RowmodList [nrow-i] ;
        if ( ir [k] > ni )
        {
            PRINTF ("%ld. Add RowmodList [%ld] = %ld while "
                    "ir = %ld >= 0 in %s\n",
                   (LONG) i, (LONG) (nrow-i), (LONG) k, (LONG) ir [k], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    for (i = 0; i < nrowdel; i++)
    {
        k = RowmodList [i] ;
        if ( ir [k] <= ni )
        {
            PRINTF ("Del RowmodList [%ld] = %ld while ir = %ld < 0 at %s\n",
                   (LONG) i, (LONG) k, (LONG) ir [k], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    for (i = 1; i <= ncoldel; i++)
    {
        k = ColmodList [ncol-i] ;
        if ( ib [k] == 0 )
        {
            PRINTF ("%ld. Del ColmodList [%ld] = %ld while ib = %i at %s\n",
                   (LONG) i, (LONG) (ncol-i), (LONG) k, ib [k], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }

    for (i = 0; i < ncoladd; i++)
    {
        k = ColmodList [i] ;
        if ( ib [k] != 0 )
        {
            PRINTF ("Add ColmodList [%ld] = %ld while ib = %i != 0 at %s\n",
                   (LONG) (ncol-i), (LONG) k, ib [k], where) ;
            pproj_error (-1, __FILE__, __LINE__, where) ;
        }
    }
}
