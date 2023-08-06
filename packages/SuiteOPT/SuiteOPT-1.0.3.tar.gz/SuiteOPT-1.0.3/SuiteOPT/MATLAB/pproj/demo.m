function demo
%% -------------------------- Problem Details -------------------------- %%
%   This is a demo for solving the problem
%
%              min     0.5(x1 - 1)^2 + 0.5(x2 + 1)^2
%              s.t     -1 <= x <= 1, -1 <= x1 - x2 <= 1
%
%   The solution of this problem with all of the given constraints is
%   x = [0.5 -0.5]. This demo file serves as an example of how to set
%   up and solve a problem using the MATLAB interface for PPROJ.

%% -------------------- Initialize inputs for pproj -------------------- %%
    y  = [ 1 -1] ;    % point to project onto polyhedron
    lo = [-1 -1] ;    % lower bound for x
    hi = [ 1  1] ;    % upper bound for x
    A  = [ 1 -1] ;    % constraint matrix
    A  = sparse (A) ; % convert matrix to sparse format
    bl = [-1] ;       % lower bound for A*x
    bu = [ 1] ;       % upper bound for A*x

%% -------------- User defined parameter values for pproj -------------- %%
    % See pproj_default inside Source/pproj.c for a description of the
    % parameters.
    pprojdata.PrintStat = 1 ;   % print PPROJ statistics

    % The following command would set a custom stopping tolerance
%    pprojdata.grad_tol = 1.e-8 ;  % default tolerance is 1.e-10

%% ---------------------- Sample calls for pproj ----------------------- %%
%   If the problem does not have the constraint bl <= A*x <= bu, then
%   pprojdata->A, pprojdata->bl, pprojdata->bu are omitted. If pasadata->bl
%   is omitted, then it is assumed to be -infinity. Similarly, if pasadata->bu
%   is omitted, then it is assumed to be +infinity. pasadata->lo and
%   pasadata->hi are treated in a similar way. Since pprojdata->lambda is
%   not given, the initial guess for the multipliers associated with the
%   constraints bl <= A*x <= bu is zero

%    % -------------------- Set options for pproj -------------------- %
    pprojdata.y  = y ;          % point to project onto polyhedron
    pprojdata.lo = lo ;         % lower bound for x
    pprojdata.hi = hi ;         % upper bound for x
    pprojdata.A  = A ;          % sparse matrix A
    pprojdata.bl = bl ;         % lower bound for Ax
    pprojdata.bu = bu ;         % upper bound for Ax

    % -------------------------- Call pproj ------------------------- %
    % The only required output is x, both the statistics structure and
    % the multipliers lambda associated with the constraints bl <= A*x <= bu
    % are optional. To obtain lamda, stats must also be included.
    [x, stats, lambda] = pproj (pprojdata) ;

%% ------------------------ Print pproj outputs ------------------------ %%
    % Since pprojdata.PrintStat = 1, the statistics were printed at the
    % completion of the run. The numerical values for the statistics are
    % stored in the stats structure.
    
    % print solution for x
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')
    fprintf('    x = ')
    disp(x')

    % print lambda
    fprintf('\n  ------------------------- Multiplier ')
    fprintf('------------------------\n')
    fprintf('    lambda = ')
    disp(lambda)
