#ifndef _SuiteOPT_H_
#define _SuiteOPT_H_
#include <sys/resource.h>
#include <math.h>
#include <limits.h>
#include <float.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <sys/time.h>
#include <time.h>

#ifdef MATLAB_MEX_FILE
#include "matrix.h"
#include "mex.h"
#endif

/* debugging options */
#ifndef NDEBUG
#ifdef MATLAB_MEX_FILE
#define ASSERT(expression) (mxAssert ((expression), ""))
#else
#define ASSERT(expression) (assert (expression))
#endif
#else
#define ASSERT(expression)
#endif

#define SuiteOPTfalse 0
#define SuiteOPTtrue 1

/* define the long version of integers */
#define LONG long

/* define the integer precision for the BLAS */
#define BLAS_INT long

#ifndef NULL
#define NULL 0
#endif

/* SuiteOPTfloat is the default precision of floating point variables */
#define SuiteOPTfloat double

/* If compiling in MATLAB, then need to use doubles and long ints.
   DLONG is a compiler flags that is defined when compiling with MATLAB. */
#ifdef DLONG
#define SuiteOPTfloat double
#define SuiteOPTint long
#define SuiteOPTinfint LONG_MAX
#define CHOLMODlong SuiteOPTtrue

#else
/* Otherwise, select precision by commenting out one pair of definitions and
   keeping the other.  SuiteOPTint is default precision of integers; CHOLMODlong
   is true if using long integers in SuitOPT, otherwise it is false */

/* standard ints */

#define SuiteOPTint int
#define CHOLMODlong SuiteOPTfalse
#define SuiteOPTinfint INT_MAX

/* long ints */

/*
#define SuiteOPTint long
#define CHOLMODlong SuiteOPTtrue
#define SuiteOPTinfint LONG_MAX
*/

#endif

#define EMPTY (SuiteOPTint) -1

/* When using long its, need to include "_l" when calling CHOLMOD routines */
#if CHOLMODlong
#define CHOLMOD(name) cholmod_l_ ## name
#else
#define CHOLMOD(name) cholmod_ ## name
#endif


/* ANSI C99 has a clean definition of IEEE infinity, defined in <math.h>.
   MATLAB has this as well.  With the ANSI (C90) version of C, there is no
   well-defined infinity, so DBL_MAX is used instead.

   You can override these defaults and define your own version of infinity
   with (for example):

   cc -ansi -DSuiteOPTinf=1e200 pproj.c ...
*/

/* infinite float */
#ifdef INFINITY
/* ANSI C99 (gcc -std=c99) */
#define SuiteOPTinf INFINITY
#else
/* ANSI C90 (gcc -ansi) */
#define SuiteOPTinf DBL_MAX
#endif

#endif
