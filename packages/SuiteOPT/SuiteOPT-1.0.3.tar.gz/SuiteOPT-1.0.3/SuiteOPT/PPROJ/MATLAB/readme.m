% ================================ PPROJ README ================================
%  PPROJ is designed to solve problems of the form
%
%              min         0.5 || x0 - y0 || - x1'y1
%          subject to    bl <= Ax <= bu, lo <= x <= hi
%
%  where A = [A0 -A1], x' = [x0' x1'], ||.|| is the Euclidean norm and the A1 
%  part of A is a matrix for which each column is zero except for a single 1. 
%  The y1 and A1 data could be vacuous. When y1 and A1 exist, it is required 
%  that bl = bu, the nonzero elements of A1 are all 1, and the elements of y1 
%  corresponding to the nonzeros in any row of A1 are all distinct and in 
%  increasing order. (y1 and A1 are used by PASA when solving a linear program).
%
% ================================ PPROJ inputs ================================
%  PPROJ requires a single input, a structure containing all problem data: 
%
%   1) pprojdata : Structure containing problem data
%
% =============================== PPROJ outputs ================================
%  There is one required output argument and two optional output arguments. 
%  The output arguments should always be provided in the following order:
%   1) x      : Solution computed by pproj                   (required)
%   2) stats  : A structure containing the run statistics    (optional)
%   3) lambda : Multiplier for constraint bl <= A*x <= bu    (optional)
%
%  Note that the output PPROJstat will be a struct containing the statistics
%  for the run of pproj on the user's problem. 
%
% ============================= PPROJ input data ===============================
%  Here we list all of the elements that will be checked for in the pprojdata
%  structure. The elements of the user's options structure corresponding to
%  the following elements are expected to have the exact name as provided below.
%
%    - grad_tol  : stopping tolerance for PPROJ (default value of 1e-10)
%    - y         : point to project onto polyhedron
%    - A         : constraint matrix (in sparse format)
%    - bl        : lower bounds for Ax
%    - bu        : upper bounds for Ax
%    - ncol      : number of columns in matrix A (also length of y)
%    - lo        : lower bounds for x
%    - hi        : upper bounds for x
%    - lambda    : guess for multipliers of constraint bl<=Ax<=bu (length nrow)
%    - nsing     : number of column singletons in A1
%    - row_sing  : if not NULL, size nrow+1 where sing_row[row] = index of
%                  first element of y1 for each row of A1
%    - singlo    : if not NULL, size nsing, contains elements of lo1
%    - singhi    : if not NULL, size nsing, contains elements of hi1
%    - singc     : if not NULL, size nsing, contains elements of y1
%
%  Finally, any of pproj's parameters can appear in the pprojdata structure.
%  See pproj_default.c for a description of the parameters.  Except for y,
%  the point being projected onto the polyhedron, any of the pprojdata structure
%  elements are optional. The code attempts to deduce the missing elements from
%  the data that is provided. Thus if ncol is not given, the deduced value
%  of ncol is the minimum of the column dimension of A and the lengths of
%  lo, hi, and y.  If the user wishes to enforce the constraint bl <= Ax <= bu,
%  then A, bl, and bu are all required, A must be provided in sparse format,
%  and the lengths of bl and bu must match the number of rows in A.
%  If pprojdata.lo is not given, then it is assumed to be -infinity.
%  If pprojdata.hi is not given, then it is assumed to be +infinity.
%  pprojdata->bl and pprojdata->bu are treated similarly.
%
% ============================== PPROJ quick use ===============================
%  Below is a sample call for using pproj which requires the minimal amount of
%  setup and customization.  See the demo files (demo.m and demoAfiro.m) for
%  examples showing how to initialize pprojdata.
%
%   >> [x, stats, lambda] = pproj (pprojdata);
%
% ====================== Customize Parameters (optional) =======================
%  If the user wishes to provide custom parameter values for pproj, the user
%  should modify the values of each parameter by name as an element of the
%  pprojdata struct.  A list of all customizable parameters can be viewed
%  by typing 'pproj parm'.
%
%
% ========================= Compiling PPROJ for MATLAB =========================
%  To compile the mex function, startup MATLAB in this directory (or add the
%  SUITEOPT/PPROJ/MATLAB directory to your path) and then enter the following
%  command in MATLAB:
%
%    >> pproj_make
%
%  The remainder of this readme file describes the help commands available
%  after installing PPROJ for use with MATLAB. 
%
% ========================== PPROJ help within MATLAB ==========================
%  For more information on pproj enter the following commands:
%      'pproj readme'  - For detailed information on pproj
%      'pproj parm'    - List of default pproj parameter values
%      'pproj demo'    - Detailed example showing how to set up and call PPROJ
