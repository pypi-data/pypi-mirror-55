% =============================== NAPHEAP README ===============================
%  NAPHEAP is designed to solve a separable convex quadratic knapsack problem 
%  of the form:
%
%              min              .5 * x'*D*x - y'*x  
%          subject to    lo <= x <= hi, blo <= a'*x <= bhi
%
%  where y, a, lo, hi are vectors of length n, blo and bhi are scalars,
%  and D=diag(d) is a diagonal matrix with a nonnegative diagonal.  If any of
%  the problem data d, y, lo, hi, blo, or bhi are omitted from the user's
%  input data, then the associated term in the objective or the associated
%  inequality in the constraints is treated as nonexistent. If a is not
%  provided, then it defaults to ones (n, 1).
%
% =============================== NAPHEAP input data ==========================
%  NAPHEAP requires a single input, which is a structure containing the problem
%  data.  Here is a list of the potential structure elements:
%
%    - n      : problem dimension 
%    - d      : diagonal in hessian of cost function
%    - y      : linear term in cost function
%    - a      : linear constraint vector
%    - lo     : lower bounds for x
%    - hi     : upper bounds for x
%    - blo    : lower bound for a'*x
%    - bhi    : upper bound for a'*x
%
%  If the problem dimension n is not given, then it defaults to the minimum
%  length of d, y, a, lo, and hi. If y or d are not provided, then they
%  are treated as zero, while if lo or blo are missing, then they are treated
%  as -infinity. If hi or bhi are missing, then they are treated as +infinity.
%  When the relative error in the solution is checked using napheap_check,
%  the problem data structure should be augmented with two additional elements:
%
%    - x      : problem solution
%    - lambda : multiplier for a'*x
%
% Both the problem solution and the constraint multiplier are outputs of napheap
% and can be input to naheap_check to determine their accuracy.
%
% ============================== NAPHEAP outputs ===============================
%  There is one required output argument and two optional output arguments. 
%  The output arguments are provided in the following order:
%    1) x       : Solution computed by napheap                       (required)
%    2) lambda  : Multiplier computed by napheap                     (optional)
%    3) NAPstat : napheap statistics                                 (optional)
%
%  Note that the output NAPstat will be a struct containing the statistics
%  for the run of napheap on the user's problem. 
%
% ============================= NAPHEAP quick use ==============================
%  If napdata is a structure containing the user's problem data, then the
%  problem solution is obtained with a command of the form:
%
%       [x, lambda, NAPstat] = napheap (napdata) ;
%
%  As noted above, the only required output is x, the solution. If the
%  statistics structure is desired, then output lambda must be included.
%  See demo.m for an example.
%
% =============================== NAPHEAP check ================================
%  After solving a problem, the error of the solution can be computed by 
%  calling napheap_check. First store the computed solution for x and multiplier
%  lambda in the problem data structure:
%
%       napdata.x = x ;
%       napdata.lambda = lambda ;
%
%  Then the following call can be made to napheap_check:
%
%       [err, errb, errB, erry] = napheap_check (napdata);
%
%  The outputs errb, errB, and erry are outlined below:
%  
%   errb: (|pert b|+|pert lambda|) / (sum | a(j) * x(j) |)
%   errB: ||pert lo||_1 + ||pert hi||_1 over the 1-norm of the corresponding
%         original components
%   erry: ||pert y||_1 over the 1-norm of the corresponding original
%         components
%
%  The perturbed quantities estimate the smallest change that is needed to
%  satisfy the KKT conditions.  The output err is the maximum of errb,
%  errB, and erry. If napheap_check is used with one output, then it is err.
%
% ====================== Customize Parameters (optional) =======================
%  The default values of the parameters for the napheap algorithm can be seen
%  in the code Source/napheap_default.c.  If the user wishes to make custom
%  choices for any of the parameters, then the new parameter value can be
%  input using the napheap input data structure.  For example, the statement
%
%       napdata.PrintStat = 1 ;
%
%  will change the default value 0 = FALSE for the parameter PrintStat
%  to 1 = TRUE. This will cause napheap to print the run statistics at the
%  end of the run.  A list of all customizable parameters can be viewed
%  by typing 'napheap parm' in the command window.
%
% ======================== Compiling NAPHEAP for MATLAB ========================
%  To compile the mex function, startup MATLAB in this directory (or add the
%  SUITEOPT/NAPHEAP/MATLAB directory to your path) and then enter the following
%  command in MATLAB:
%
%       napheap_make
%
%  The remainder of this readme file describes the help commands available
%  after installing NAPHEAP for use with MATLAB. 
%
% ========================== NAPHEAP help within MATLAB ========================
%  For more information on napheap enter the following commands:
%      'napheap readme'  - For detailed information on napheap
%      'napheap parm'    - List of default napheap parameter values
%      'napheap demo'    - Detailed example showing how to set up and call 
%                          NAPHEAP demo
%      'napheap_check'   - General information about napheap and napheap_check
