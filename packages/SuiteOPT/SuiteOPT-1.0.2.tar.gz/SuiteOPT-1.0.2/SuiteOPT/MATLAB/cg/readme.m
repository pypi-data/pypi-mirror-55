% ============================== CG_DESCENT README =============================
% CG_DESCENT (Conjugate Gradient with guaranteed DESCENT) is designed to solve 
% unconstrained optimization problems. This file explains how to install and
% use cg_descent in MATLAB. The file is best viewed by starting MATLAB and
% typing the command
%
%    >> cg_descent readme
%
% ============================== CGDESCENT inputs ==============================
%  CGDESCENT requires a single input which is a structure containing all
%  problem data: 
%
%   1) cgdata : Struct containing problem data
%
% ============================= CGDESCENT outputs ==============================
%  List of all outputs for cg_descent in the expected ordering.
%    1) x        : Solution computed by cg_descent                  (required)
%    2) stats    : cg_descent statistics                            (optional)
%    3) status   : Status of run                                    (optional)
%
% =============================== CGDESCENT data ===============================
%  Here we list all of the elements that cg_descent checks for in the cgdata
%  structure.
%
%    cgdata.x           : Initial guess for solution
%    cgdata.objective   : Function handle for evaluating objective function
%    cgdata.gradient    : Function handle gradient of the objective function
%    cgdata.valgrad     : Function handle for objective and its gradient
%    cgdata.hprod       : Function handle for evaluating hessian times vector
%    cgdata.c           : Linear term in objective function
%
%  In addition, any of the parameters used by cg_descent can appear in the
%  pasadata structure. They are specified using a statement of the form
%
%  >> cgdata.PP = VV ;
%
%  where PP is the name of the parameter, and VV is the assigned value.
%  A list of the default parameter values is obtained with the command
%
%    >> cg_descent parm
%
%  The requirements for function evaluations using function handles and c are
%  outlined below (depending on if the user wishes to use quadratic or 
%  non-quadratic mode of cg_descent).
%
% ============================= Non-Quadratic Mode =============================
%  Here we outline which function handles are required and optional when
%  using the non-quadratic mode of cg_descent.
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
%  Note that hprod must be a function with one input and one output. An example
%  can be found in demoQP.m.
%
% ============================ CGDESCENT quick use =============================
%  Below is a sample call for using cg_descent that requires the minimal amount
%  of setup and customization. For examples illustrating how to initialize 
%  cgdata check the provided demo files (demo.m and demoQP.m). 
%
%   >> [x, stats, status] = cg_descent (cgdata);
%
% ==================== Compiling cg_descent for MATLAB ========================
%  To compile the mex function, startup MATLAB in this directory and then
%  enter the following command in MATLAB:
%
%    >> cg_descent_make
%
% ========================= Information within MATLAB ==========================
%  For more information on cg_descent enter the following commands:
%      'cg_descent readme'  - For detailed information on cg_descent 
%      'cg_descent parm'    - List of all default parameters values
%      'cg_descent demo'    - To view demo of non-quadratic mode
%      'cg_descent demoQP'  - To view demo of quadratic mode
%      'cg_descent'         - To view all available options
