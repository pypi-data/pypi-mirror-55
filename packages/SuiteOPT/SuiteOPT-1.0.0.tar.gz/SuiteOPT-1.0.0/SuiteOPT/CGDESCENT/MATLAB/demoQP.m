function demoQP 
%% -------------------------- Problem Details -------------------------- %%
%   This is a demo for solving the problem
%   
%                min     0.5 sum_{i=1}^n  i*x_i^2 + x_i
%   
%   with the purpose of illustrating how to set up and solve a problem
%   using the quadratic mode of cg_descent. 

%% ------------------ Initialize inputs for cg_descent ----------------- %%
    n = 10;          % dimension of primal variable
    x = ones(1, n) ; % initial guess
    c = ones(1, n) ; % linear term in objective function
    H = [1:n] ;
    
%% ------------- User defined parameter values for cg_descent ---------- %%
%   See cg_default inside CGDESCENT/Source/cg_default.c for a 
%   description of the parameters.
    cgdata.PrintStat = 1 ;   % print CGDESCENT statistics

%% ---------------- Calling cg_descent (Quadratic Cost) ---------------- %%
    % ----------------- Set options for cg_descent ------------------ %
    cgdata.x = x ; % Initial guess for solution
    cgdata.c = c ; % Linear term in cost function 
    cgdata.hprod = @myhprod ; % Function handle for hessian times vector 

    % ----------------------- Call cg_descent ----------------------- %
    x = cg_descent (cgdata) ;
    
%% --------------------- Print cg_descent outputs ---------------------- %%
    % Since cgdata.PrintStat = 1, the cg_descent statistics are printed
    % at the conclusion of the run. The numerical values for the statistics
    % are stored in the stats structure.

    % print solution x
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')

    fprintf('x (1:4) =') 
    for i = 1:4
        fprintf ('    %10.7f\n', x (i)) ;
    end

%% -------- User defined functions for cg_descent (Quadratic Cost) ----- %%
    % ---- Product of Hessian Times vector ---- %
    function p = myhprod (x)
        p = H'.*x ; % just multiply by diagonal elements
    end
end
