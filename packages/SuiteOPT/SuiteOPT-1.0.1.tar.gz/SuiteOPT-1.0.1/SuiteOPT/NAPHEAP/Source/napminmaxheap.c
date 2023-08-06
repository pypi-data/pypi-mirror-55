/* ========================================================================== */
/* === napminmaxheap.c ====================================================== */
/* ========================================================================== */

/* This module creates two kinds of heap: a min heap and a maxheap */

#ifdef CONSTRUCT_MINHEAP_FUNCTIONS
/* min heap functions */
#define NAPHEAP_BUILD  napminheap_build
#define NAPHEAP_DELETE napminheap_delete
#define NAPHEAP_ADD    napminheap_add
#define NAPHEAPIFY     napminheapify
#define IN_ORDER(a,b)     (a < b)
#define OUT_OF_ORDER(a,b) (a > b)
#endif

#ifdef CONSTRUCT_MAXHEAP_FUNCTIONS
/* max heap functions */
#define NAPHEAP_BUILD  napmaxheap_build
#define NAPHEAP_DELETE napmaxheap_delete
#define NAPHEAP_ADD    napmaxheap_add
#define NAPHEAPIFY     napmaxheapify
#define IN_ORDER(a,b)     (a > b)
#define OUT_OF_ORDER(a,b) (a < b)
#endif

/* For the macros above:
    in_order(a,b) is true if [a,b] is in the proper order in the heap.
    out_of_order(a,b) is true if [a,b] is not in proper order in the heap */

/* ==========================================================================
   === NAPHEAP_BUILD ========================================================
   ==========================================================================
   build a min/max heap in heap [1..nheap]
   heap [i] is an index of an element of array X
   ========================================================================== */

PRIVATE void NAPHEAP_BUILD
(
    NAPINT      *heap, /* on input, unsorted set of indices.  size nheap+1 */
    NAPFLOAT const *X, /* numbers to sort (not modified) */
    NAPINT      nheap  /* number of elements to build into the heap */
)
{
    NAPINT p ;

    for (p = nheap/2 ; p >= 1 ; p--)
    {
        NAPHEAPIFY (heap, X, p, nheap) ;
    }
}

/* ==========================================================================
   === NAPHEAP_DELETE =======================================================
   ==========================================================================
   delete the top element in a min/max heap
   ========================================================================== */

PRIVATE NAPINT NAPHEAP_DELETE  /* return new size of heap */
(
    NAPINT      *heap, /* indices into X, 1..n on input.  size nheap+1 */
    NAPFLOAT const *X, /* not modified */
    NAPINT      nheap  /* number of items in heap */
)
{
    if (nheap <= 1)
    {
        return (0) ;
    }

    /* move element from the end of the heap to the top */
    heap [1] = heap [nheap] ;
    nheap-- ;
    NAPHEAPIFY (heap, X, 1, nheap) ;
    return (nheap) ;
}

/* ========================================================================== */
/* === NAPHEAP_ADD ========================================================== */
/* ========================================================================== */

/* add a new leaf to a min/max heap */

PRIVATE NAPINT NAPHEAP_ADD      /* returns the new size of the heap */
(
    NAPINT      *heap, /* size n, containing indices into X.  size nheap+2 */
    NAPFLOAT const *X, /* not modified */
    NAPINT       leaf, /* the new leaf */
    NAPINT      nheap  /* number of elements in heap not counting new one */
)
{
    NAPFLOAT Xold, Xnew ;
    NAPINT i, newindex, old ;

    nheap++ ;
    old = nheap ;
    heap [old] = leaf ;
    Xold = X [leaf] ;
    while ( old > 1 )
    {
        newindex = old/2 ;
        i = heap [newindex] ;
        Xnew = X [i] ;
        if (OUT_OF_ORDER (Xnew, Xold)) /* for min heap: ( Xnew > Xold ) */
        {
            /* Xnew and Xold are out of order, so swap them */
            heap [newindex] = leaf ;
            heap [old] = i ;
        }
        else return (nheap) ;
        old = newindex ;
    }
    return (nheap) ;
}

/* ========================================================================== */
/* === napminheapify ======================================================== */
/* ========================================================================== */

/* heapify starting at node p.  On input, the heap at node p satisfies the */
/* heap property, except for heap [p] itself.  On output, the whole heap */
/* satisfies the heap property. */

PRIVATE void NAPHEAPIFY
(
    NAPINT      *heap, /* size nheap+1, containing indices into X */
    NAPFLOAT const *X, /* not modified */
    NAPINT          p, /* start at node p in the heap */
    NAPINT      nheap  /* heap [1 ... n] is in use */
)
{
    NAPFLOAT Xe, Xleft, Xright ;
    NAPINT left, right, e, hleft, hright ;

    e = heap [p] ;
    Xe = X [e] ;

    while ( TRUE )
    {
        left = p * 2 ;
        right = left + 1 ;

        if ( right <= nheap )
        {
            /* both left and right children of p are in the heap */
            hleft  = heap [left] ;
            hright = heap [right] ;
            Xleft  = X [hleft] ;
            Xright = X [hright] ;
            if (IN_ORDER (Xleft, Xright)) /* for min heap: (Xleft < Xright) */
            {
                /* traverse down the left heap */
                if (OUT_OF_ORDER (Xe, Xleft)) /* for min heap: (Xe > Xleft) */
                {
                    /* swap e with the left child */
                    heap [p] = hleft ;
                    p = left ;
                }
                else
                {
                    /* element e, with value Xe, has found its final home */
                    heap [p] = e ;
                    return ;
                }
            }
            else
            {
                /* traverse down the right heap */
                if (OUT_OF_ORDER (Xe, Xright)) /* for min heap: (Xe > Xright) */
                {
                    /* swap e with the right child */
                    heap [p] = hright ;
                    p = right ;
                }
                else
                {
                    /* element e, with value Xe, has found its final home */
                    heap [p] = e ;
                    return ;
                }
            }
        }
        else
        {
            /* only the left child of p is in the heap */
            if ( left <= nheap )
            {
                /* traverse down the left heap */
                hleft = heap [left] ;
                Xleft = X [hleft] ;
                if (OUT_OF_ORDER (Xe, Xleft)) /* for min heap: (Xe > Xleft) */
                {
                    /* swap e with the left child */
                    heap [p] = hleft ;
                    p = left ;
                }
            }
            /* element e, with value Xe, has found its final home */
            heap [p] = e ;
            return ;
        }
    }
}

#undef NAPHEAP_BUILD
#undef NAPHEAP_DELETE
#undef NAPHEAP_ADD
#undef NAPHEAPIFY
#undef IN_ORDER
#undef OUT_OF_ORDER
#undef CONSTRUCT_MINHEAP_FUNCTIONS
#undef CONSTRUCT_MAXHEAP_FUNCTIONS
