function demo 
%% ----------- User defined parameter values for cg_descent ------------ %%
%   See cg_default inside CGDESCENT/Source/cg_default.c for a 
%   description of the parameters.
    cgdata.PrintParm = 1 ;    % print the parameter value (0 = FALSE is default)
    cgdata.PrintStat = 1 ;    % print cg_descent statistics
    cgdata.grad_tol = 1.e-8 ; % Stopping tolerance for cg_descent (1e-6 default)

%% ------------- Calling cg_descent (Non-Quadratic Cost) --------------- %%
    % ----------------------- Required Inputs ------------------------ %
    cgdata.x = zeros(100, 1) ;    % Initial guess for solution
    cgdata.objective = @myvalue ; % Function handle for objective
    cgdata.gradient = @mygrad ;   % Function handle for gradient of obj

    % ----------------------- Optional Input ------------------------- %
       % Since it is often easy to evaluate the gradient at the same
       % time as the function value, we also code a routine valgrad below
       % that simultaneously evaluates the function and its gradient.
       %  Both the value and gradient routines are currently required,
       % while the valgrad routine is optional.  By including valgrad,
       % the solution time can be reduced for some problems.
    cgdata.valgrad = @myvalgrad ; % Function handle for objective & gradient

    % ----------------------- Call cg_descent ----------------------- %
       % The only required output is x, the solution. Optionally, the
       % run status and the cg_descent statistics are returned.
       % If status = 0, then the sup-norm of the gradient satisfied the
       % stopping condition, otherwise an error occurred. By default,
       % cgdata.PrintStatus = 1 and the status is printed at
       % the conclusion of the run. If the value of status is desired,
       % then the stats structure must be included as an output.
    [x, stats, status] = cg_descent (cgdata) ;

%% --------------------- Print cg_descent outputs ---------------------- %%
   
    % Since cgdata.PrintStat = 1, the statistics for cg_descent are
    % printed at the conclusion of the run. The numerical values for
    % the statistics can be extracted from the stats output argument.

    % print solution x
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')
    fprintf('x[1:4] =\n') 
    for i = 1:4
        fprintf ('%10.4f\n', x(i)) ;
    end

%% ----- User defined functions for cg_descent (Non-Quadratic Cost) ---- %%
    % ---- Objective function ---- %
    function f = myvalue(x)
       f = 0;
       n = length(x) ;
       for i=1:n
           t = i^0.5 ;
           f = f + exp(x(i)) - t*x(i) ;
       end
    end
    
    % ---- Gradient of objective function ---- %
    function g = mygrad(x)
        n = length(x) ;
        g = zeros (1,n) ;
        for i=1:n
           t = i^0.5 ;
           g(i) = exp(x(i))-t ;
        end
    end
    
    % ---- Objective function and gradient ---- %
    % first output is function value, second is the gradient vector
    function [f,g] = myvalgrad(x)
        n = length(x) ;
        f = 0 ;
        g = zeros (1,n) ;
        for i=1:n
           t = i^0.5 ;
           ex = exp(x(i)) ;
           f = f + ex - t*x(i) ;
           g(i) = ex - t ;
        end
    end
end
