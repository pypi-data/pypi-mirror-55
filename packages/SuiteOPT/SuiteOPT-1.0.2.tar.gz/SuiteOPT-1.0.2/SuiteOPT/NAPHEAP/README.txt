   =========================================================================
   ============================== NAPHEAP ==================================
   =========================================================================

       ________________________________________________________________
      |Solve a separable convex quadratic knapsack problem of the form:|
      |                                                                |
      | min .5x'Dx - y'x  subject to  lo <= x <= hi, blo <= a'x <= bhi |
      |                                                                |
      |where lo and hi are vectors, blo and bhi are scalars, and D is a|
      |           a diagonal matrix with nonnegative diagonal.         |
      |                                                                |
      |                 Copyright by Timothy A. Davis                  |
      |                              William W. Hager                  |
      |                              James T. Hungerford               |
      |                                                                |
      |          http://www.math.ufl.edu/~hager/papers/Software        |
      |                                                                |
      |  Disclaimer: The views expressed are those of the authors and  |
      |              do not reflect the official policy or position of |
      |              the Department of Defense or the U.S. Government. |
      |                                                                |
      |      Approved for Public Release, Distribution Unlimited       |
      |________________________________________________________________|

    The constraints are rewritten as

               lo <= x <= hi,    blo <= b <= bhi,    a'x = b

    The code solves the dual problem obtained by introducing
    a multiplier lambda for the constraint a'x = b.  The dual function is

    L(lambda) = inf {.5x'Dx - y'x + lambda (a'x - b):
                                 lo <= x <= hi, blo <= b <= bhi}

    The dual function is concave, and the solution to the original (primal)
    problem can be constructed from the maximizer of the dual function.
    If blo < bhi, then there is a discontinuity at lambda = 0.  D is a
    diagonal matrix, and if d = diag(D) contains zeros, there could be
    additional points of discontinuity.  The algorithm iterates on lambda
    until 0 lies in the subdifferential of L(lambda).  The optimal x is
    constructed from the minimizers of the dual function.  Three algorithms
    are implemented: a break point searching algorithm, a variable fixing
    algorithm, and a Newton/secant algorithm.  A starting guess for the
    optimal multiplier can be provided.  If the user does not have a good
    starting guess, at most Parm->K (default 20) iterations of a Newton-type
    algorithm are used to generate a starting guess. The Newton-type method
    terminates when the root is bracketted.

    By default, Newton's method is used for the startup (Parm->newton defaults
    is TRUE).  Set Parm->newton to FALSE to choose the variable fixing
    algorithm for startup. After the startup iterations, the breakpoint
    algorithm is used to compute the final solution. When Newton's method is
    used for the startup, all entries of d must be positive (otherwise an error
    is returned), so to solve problems with zeros in d, you must set
    Parm->newton to FALSE.  No value of d can be negative, for any method.

    The user can either provide work arrays or let the code malloc work arrays.
    The necessary size for the work arrays depends on the choice of the
    algorithm, as can be seen in the memory allocation routine.  The most
    memory that the code will require is an integer work array of size 4*n+2
    and a real work array of size 5*n where n is the problem dimension.

    The default parameter values used by the software are given in the
    napheap_defaults routine.  To alter the default parameter values, the
    user can first initialize the parameters to their default values using
    napheap_defaults, make any changes to the values in the parameter
    structure, and provide the updated parameter structure as an input to the
    napheap code. Note that TRUE = 1 and FALSE = 0.

    The code records the number of iterations for either the variable fixing or
    Newton method, and the number of break points that are passed through
    during the solution process.  These statistics are returned when the user
    provides a nonnull structure for the statistics argument of the code.  The
    statistics and parameters can be printed with napheap_print_stats and
    napheap_print_parms.

    If the user wishes to override the default definition of infinity
    given in Include/napheap.h, modify the OPTFLAGS as explained in
    Lib/napheap.mk.
       ________________________________________________________________
      |This program is free software; you can redistribute it and/or   |
      |modify it under the terms of the GNU General Public License as  |
      |published by the Free Software Foundation; either version 2 of  |
      |the License, or (at your option) any later version.             |
      |This program is distributed in the hope that it will be useful, |
      |but WITHOUT ANY WARRANTY; without even the implied warranty of  |
      |MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the   |
      |GNU General Public License for more details.                    |
      |                                                                |
      |You should have received a copy of the GNU General Public       |
      |License along with this program; if not, write to the Free      |
      |Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, |
      |MA  02110-1301  USA                                             |
      |________________________________________________________________|

      Alternative licenses are also available.  Please contact the authors
      for details.

      Reference:
         T. A. Davis, W. W. Hager, and J. T. Hungerford, An Efficient
         Hybrid Algorithm for the Separable Convex Quadratic Knapsack Problem,
         see Doc/napheap_paper.pdf

Files and directories in the napheap distribution:

./Makefile                  for compiling and testing napheap
./README.txt                this file

Demo:
    Demo/napheap_demo.c     simple demo of the C-callable napheap function
    Demo/Makefile           makefile to compile the demo
    Demo/napheap_demo.out   outout of demo

Doc:
    Doc/ChangeLog           changes since first-released version
    Doc/gpl.txt             license (contact authors for a commercially-suitable one)
    Doc/napheap_paper.pdf   paper describing the algorithm

Include:
    Include/napheap.h       include file for user-programs

Lib:
    Lib/Makefile            makefile to compile the C-callable napheap library
    Lib/napheap.mk          makefile configurations: edit this for your system

MATLAB:                     MATLAB interface
    MATLAB/Contents.m           list of MATLAB napheap functions
    MATLAB/napheap.m            for 'help napheap'
    MATLAB/napheap_check.m      for 'help napheap_check'
    MATLAB/napheap_check_mex.c  MATLAB mexFunction interface for napheap_check
    MATLAB/napheap_install.m    to install for use in MATLAB
    MATLAB/napheap_mex.c        MATLAB mexFunction interface for napheap
    MATLAB/napheap_mex.h        include file for MATLAB mexFunctions
    MATLAB/napheap_test.m       test for napheap mexFunctions
    MATLAB/napheap_util_mex.c   helper functions for mexFunctions

Source:                     C source code
    Source/napheap.c            the primary C napheap functions
    Source/napheap_check.c      for checking the solution from napheap
    Source/napheap_defaults.c   for setting default parameters
    Source/napheap_internal.h   internal include file, not for user programs
    Source/napheap_print.c      for printing parameters and statistics
    Source/napminmaxheap.c      min/max heaps for napheap

Test:                       exhaustive test suite for napheap
    Test/Makefile               makefile to compile and run the tests
    Test/naptest.c              the C test function


To compile and run the tests and demo, you can use 'make' in this directory:

    make                    compiles the library and runs a simple demo
    make library            just compiles the library
    make purge              remove all files not in the original distribution
    make distclean          same as 'make purge'
    make clean              remove all files not in the original distribution,
                            except keep the compiled programs and libraries
    make tests              run the exhaustive test
    make cov                run the exhaustive test with statement coverage
    make valgrind           run the exhaustive test with valgrind (requires Linux)
    make install            copy the compiled library to the install location
    make uninstall          remove the compiled library from install location
                            see Lib/napheap.mk for the default install location

