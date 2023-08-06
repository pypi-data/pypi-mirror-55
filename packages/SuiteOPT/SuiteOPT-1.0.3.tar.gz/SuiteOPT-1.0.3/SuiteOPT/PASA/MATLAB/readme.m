% ================================ PASA README =================================
% The PASA (Polyhedral Active Set Algorithm) is designed to solve problems of
% the form
%
%              min f(x)  subject to  bl <= A*x <= bu, lo <= x <= hi
%
% This file explains how to install and use pasa in MATLAB. The file is best
% viewed by starting MATLAB and typing the command
%
%    >> pasa readme
%
% ========================= Compiling PASA for MATLAB ==========================
%  To compile the mex function, startup MATLAB in this directory and then
%  enter the following command in MATLAB:
%
%    >> pasa_make
%
% ========================= Compiling PASA for MATLAB ==========================
%  To compile the mex function, startup MATLAB in this directory and then
%  enter the following command in MATLAB:
%
%    >> pasa_make
%
% ============================== PASA quick use ================================
%  The data describing the problem should be stored in a structure denoted
%  pasadata. The problem is solved using a statement of the form
%
%   >> [x, stats, lambda] = pasa (pasadata) ;
%
%  The only required output is x, the problem solution; both the statistics
%  structure (stats), and the multiplier (lambda) associated with the
%  constraints bl <= A*x <= bu are optional. If lambda is desired, then
%  stats must be included.
%
% ================================ PASA inputs =================================
%  The elements of the pasadata structure are the following:
%
%    pasadata.A         : constraint matrix (in sparse format)
%    pasadata.ncol      : number of cols in A
%    pasadata.bl        : lower bounds for A*x
%    pasadata.bu        : upper bounds for A*x
%    pasadata.lo        : lower bounds for x
%    pasadata.hi        : upper bounds for x
%    pasadata.x         : guess for the solution x
%    pasadata.lambda    : guess for multiplier of constraint bl <= A*x <= bu
%    pasadata.objective : Function handle for evaluating objective function
%    pasadata.gradient  : Function handle for gradient of the objective function
%    pasadata.valgrad   : Function handle for objective and its gradient
%    pasadata.hprod     : Function handle for evaluating hessian times vector
%    pasadata.c         : Linear term in objective function
%    pasadata.a         : The row vector A when nrow = 1
%    pasadata.d         : f(x) = .5x'*D*x + c'*x, D >= diagonal, d = diag(D)
%    pasadata.y         : f(x) = ||y-x||,
%    pasadata.cg_hprod  : Function handle for hessian times vector in
%                         unconstrained optimization
%
%  Finally, any of the parameters used by pasa, pproj, cg_descent, or napheap
%  can appear in the pasadata structure. They are specified using a statement
%  of the form
%
%  >> pasadata.SS.PP = VV ;
%
%  where SS is any of the solvers pasa, pproj, napheap, or cg, PP is the
%  name of the parameter, and VV is the value assigned to the parameter.
%  A list of the default parameter values is obtained by commands of the
%  following form:
%
%      'pasa all'     - List of all default parameters values
%      'pasa parm'    - List of default pasa parameter values
%      'pasa pproj'   - List of default pproj parameter values
%      'pasa cg'      - List of default cg_descent parameter values
%      'pasa napheap' - List of default napheap parameter values
%
%  For example, the stopping criterion in pasa to set to 1.e-8 by
%  >> pasadata.pasa.grad_tol = 1.e-8 ;
%
%  Nearly all the elements of the pasadata structure are optional; the code
%  will attempt to deduce the value of missing elements. If ncol is not given,
%  then the deduced value for ncol is the minimum of the column dimension of A
%  and the lengths of c, lo, hi, x, and y, if they exist. If the user wishes
%  to enforce the constraint bl <= A*x <= bu, then A and bl or bu are all
%  required, A must be provided in sparse format, and the lengths of bl and bu
%  must match the number of rows in A.  If pasadata.lo or pasadata.hi are
%  not given, then it is assumed that the respective constraints lo <= x
%  or x <= hi do not exist.  pasadata->bl and pasadata->bu are treated
%  similarly. If pasadata.x or pasadata.lambda are not given, then they
%  are taken to be zero.
%
% ============================= Non-Quadratic Mode =============================
%  Here we outline which function handles are required and optional when
%  using the non-quadratic mode of PASA.
%
%   ---------------------- Required Function Handles --------------------------
%    objective  : Function handle for evaluating objective function
%    gradient   : Function handle for gradient of the objective function
%   ---------------------- Optional Function Handle ---------------------------
%    valgrad    : Function handle for objective and gradient
%
%  Note that objective and gradient must be functions with one input and one 
%  output and valgrad must be a function with one input and two outputs. 
%
% =============================== Quadratic Mode ===============================
%  If the objective is quadratic, the user can provide a routine to evaluate 
%  the product between the objective Hessian and a vector. Additionally, the 
%  linear term in the objective must be provided. 
%   --------------------------- Required Inputs -------------------------------
%    hprod       : Function handle for evaluating hessian times vector
%    c           : Linear term in objective function
%
%  Note that hprod must be a function with two inputs and one output. An 
%  example can be found in demoQP.m.
%
% ================================ Linear Mode =================================
%  If the objective is linear, the user can provide just the linear term in the
%  objective.
%   --------------------------- Required Inputs -------------------------------
%    c           : Linear term in objective function
%
