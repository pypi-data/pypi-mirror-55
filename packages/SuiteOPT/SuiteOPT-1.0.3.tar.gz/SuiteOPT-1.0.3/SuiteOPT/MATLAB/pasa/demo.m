function demo
%% -------------------------- Problem Details -------------------------- %%
%   This is a demo for solving the problem
%   
%              min                 f(x)  
%              s.t     -1 <= x <= 2, bl <= Ax <= bu
%
%   where
%
%    f(x) = Sum_{i = 1, n-1} 100 (x [i+1] - x [i]^2)^2 + (1 - x [i])^2,
%
%   bl = [  3; -1; -2; -1 ], bu = [  5;  3;  0;  1 ], and
%
%                       A = |  1   1   1   1   1  |
%                           |  1   1   1   0  -1  |
%                           |  1   0  -1  -1   1  |
%                           |  1  -1   0   1   0  |
%
%   The function f is a generalization of the Rosenbrock function.
%   For unconstrained optimization, the absolute minimum of f
%   is obtained at x = [  1;  1;  1;  1;  1 ] and f attains a local min
%   at x = [  -1;  1;  1;  1;  1 ]. The linear and bound constraints were
%   chosen so that both of these vectors lie within the feasible region
%   for the test problem described above (the constraints are inactive).

%% --------------------- Initialize inputs for pasa -------------------- %%
    ncol = 5 ;               % dimension of primal variable 
    lo(1:ncol) = -1 ;        % lower bound for x
    hi(1:ncol) =  2 ;        % upper bound for x
    A = [ 1   1   1   1   1
          1   1   1   0  -1
          1   0  -1  -1   1
          1  -1   0   1   0] ;
    A = sparse(A) ;          % create the sparse matrix A
%   see PPROJ/MATLAB/demoAfiro where A is generated using triples and
%   converted to a sparse matrix
    bl = [3,-1,-2,-1] ;      % lower bound for Ax
    bu = [5, 3, 0, 1] ;      % upper bound for Ax

%% ---------------- User defined parameter values for pasa ------------- %%
    % See pasa_default inside Source/pasa.c for a description of the
    % parameters. See pproj_default inside PPROJ/Source/pproj.c for 
    % a description of the parameters.
    pasadata.pasa.PrintParm = 1 ;   % print parameters for all routines used
    pasadata.pasa.PrintStat = 1 ;   % print statistics for all routines used

    % --------------------- Set data for problem -------------------- %
    % An initial guess for the problem solution would be stored in pasadata.x
    % If no initial guess is given, pasa uses x = 0.
    % An initial guess for the dual multiplier associated with the
    % constraint bl <= A*x <= bu could be stored in pasa.lambda
    % If the constraint bl <= A*x <= bu was not present, then the assignments
    % below to pasadata.A, pasadata.bl, and pasadata.bu are omitted.
    % If pasadata.bl is omitted, then it is assumed to be -infinity.
    % If pasadata.bu is omitted, then it is assumed to be +infinity.
    % The bounds lo and hi are treated in a similar fashion.
    % By default, pasa will attempt to deduce the problem dimensions from
    % the size of the provided matrices and vectors. If in this example,
    % the bounds had been stored in vectors of length 10, then pasa will not
    % be able to determine the problem dimension. In this case, it would
    % necessary to specify pasadata.ncol = 5 and pasadata.nrow = 4
    %
    pasadata.lo = lo ;              % lower bound for x
    pasadata.hi = hi ;              % upper bound for x
    pasadata.A  = A ;               % sparse matrix A
    pasadata.bl = bl ;              % lower bound for Ax
    pasadata.bu = bu ;              % upper bound for Ax
    pasadata.objective = @myvalue ; % objective function
    pasadata.gradient = @mygrad ;   % gradient function
    pasadata.valgrad = @myvalgrad ; % objective and gradient function (optional)

    % -------------------------- Call pasa -------------------------- %
    % The only required output argument is the solution argument x.
    % Optionally, pasa returns the statistics structure and the multiplier
    % associated with the constraints bl <= A*x <= bu
    [x, stats, lambda] = pasa (pasadata) ;

%% ------------------------ Print pasa outputs ------------------------- %%
    % In this example, we set pasadata.pasa.PrintStat = 1. This implies
    % that the statistics for all the routines that were used to solve
    % the problem will be printed. Since pasa, pproj, and cg_descent were
    % used, the statistics for all three routines are displayed. The second
    % returned argument return by pasa above, stats, contains the numerical
    % values of the statistics. Since pasa, pproj, and cg_descent were
    % used, the associated numerical values for the statistics are found
    % in stats.pasa, stats.pproj, and stats.cg. If napheap was used to
    % solve the problem, then its statistics would be in stats.napheap.

    % print solution
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')
    fprintf('x = ') 
    disp(x)

    % print multiplier (exact multiplier is 0)
    fprintf('\n  ------------------------- Multiplier ')
    fprintf('------------------------\n')
    fprintf('lambda = ') 
    disp(lambda)

    disp('pasa parameter values chosen by the user:') ;
    pasadata.pasa

%% ----------------- User defined functions for pasa ------------------- %%
    % ---- Objective function ---- %
    function f = myvalue(x)
        f = 0;
        n = length(x) ;
        for i=1:n-1
            t1 = x(i) ;
            t2 = x(i+1) - t1*t1 ;
            t3 = t1 - 1 ;
            f = f + (100*t2*t2 + t3*t3) ;
        end
    end
    
    % ---- Gradient of objective function ---- %
    function g = mygrad(x)
        n = length(x) ;
        g = zeros (1,n) ;
        t1 = x(1) ;
        t0 = 200*(x(2) - t1*t1) ;
        g(1) = 2*(t1 - 1 - t0*t1) ;
        for i=2:(n-1)
           t1 = x(i) ;
           t2 = 200*(x(i+1) - t1*t1) ;
           t3 = t1 - 1 ;
           g(i) = 2*(t3 - t2*t1) + t0 ;
           t0 = t2 ;
        end
        g(n) = 200*(x(n) - x(n-1)*x(n-1)) ;
    end
    
    % ---- Objective function and gradient ---- %
    function [f,g] = myvalgrad(x)
        n = length(x) ;
        f = 0 ;
        g = zeros (1,n) ;
        t1 = x (1) ;
        t3 = t1 - 1 ;
        t0 = 200*(x(2) - t1*t1) ;
        g(1) = 2*(t3 - t0*t1) ;
        f = 0.0025*t0*t0 + t3*t3 ;
        for i=2:(n-1)
           t1 = x(i) ;
           t2 = 200*(x(i+1) - t1*t1) ;
           t3 = t1 - 1 ;
           g(i) = 2*(t3 - t2*t1) + t0 ;
           f = f + 0.0025*t2*t2 + t3*t3 ;
           t0 = t2 ;
        end
        g(n) = 200*(x(n) - x(n-1)*x(n-1)) ;
    end

end
