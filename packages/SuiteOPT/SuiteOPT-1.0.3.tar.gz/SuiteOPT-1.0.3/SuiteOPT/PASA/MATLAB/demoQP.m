function demoQP
%% -------------------------- Problem Details -------------------------- %%
%   This is a demo for showing how to set up and solve a QP using PASA. 
%   It is a simple problem of the form
%   
%              min             0.5 x'*x + c'*x
%              s.t      -1 <= x <= 1, -1 <= A*x <= 1 
%
%   where A = [1 0 -1] and c = [5 5 5].

%% --------------------- Initialize inputs for pasa -------------------- %%
    A  = [1 0 -1] ;        % initialize matrix A
    A  = sparse (A) ;      % convert to sparse matrix format
    bl = [-1] ;            % lower bound for Ax
    bu = [ 1] ;            % upper bound for Ax
    lo = [-1 -1 -1] ;      % lower bound for x
    hi = [ 1  1  1] ;      % upper bound for x
    c  = [5 5 5] ;         % linear term in the objective function 
    z  = zeros (3, 1) ;    % used in Hessian/vector product computation

%% ---------------- User defined parameter values for pasa ------------- %%
    % See pasa_default inside Source/pasa.c for a description of the
    % parameters. See pproj_default inside PPROJ/Source/pproj.c for 
    % a description of the parameters.
    pasadata.pasa.PrintParm = 1 ;   % print all parameter 0 = FALSE is default
    pasadata.pasa.PrintStat = 1 ;   % print statistics

    % --------------------- Set up the pasa structure -------------------- %
    % since an initial guess pasadata.x for the solution and pasadata.lamba
    % for the multiplier associated with the constraints bl <= A*x <= bu
    % are not given, they are assumed to be zero
    pasadata.lo = lo ;           % lower bounds for x
    pasadata.hi = hi ;           % upper bounds for x
    % if the constraints bl <= A*x <= bu did not exist, then the assignments
    % to pasadata.A, pasadata.bl, and pasadata.bu would be omitted. If
    % pasadata.lo is omitted, it is assumed to be -infinity. Similarly, if
    % pasadata.hi is omitted, it is assumed to be +infinity.
    % The bounds bl and bu are treated in a similar fashion.
    pasadata.A = A ;             % sparse matrix A
    pasadata.bl = bl ;           % lower bounds for Ax
    pasadata.bu = bu ;           % upper bounds for Ax
    pasadata.hprod = @myhprod ;  % evaluate hessian times vector
    pasadata.c = c ;             % linear term in objective 

    disp('This example requires no interations of napheap or cg') ;

    % -------------------------- Call pasa -------------------------- % 
    [x, stats, lambda] = pasa (pasadata) ;
%

%% ------------------------ Print pasa outputs ------------------------- %%
    % The numerical values for the statistics are stored in the structures
    % stats.pasa, stats.napheap, and stats.cg. Since A has a single row,
    % napheap is used instead of pproj.

    % print x 
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')
    fprintf('    x = ') 
    disp(x)

    % print lambda 
    fprintf('\n  ------------------------- Multiplier ')
    fprintf('------------------------\n')
    fprintf('    lambda = ') 
    disp(lambda)

%% ----------------- User defined functions for pasa ------------------- %%
%   If H is the Hessian of the quadratic, then the hprod routine should 
%   compute p = H (:, nzIndices)*x. In other words, the input x 
%   corresponds to the nonzero components of a vector and nzIndices are 
%   the associated columns of H. For this trivial example, the Hessian 
%   is the identity and the computation is obtained by setting 
%   p(nzIndices) = x.
 
    % -------- User hprod -------- %
    function p = myhprod (y, nzIndices)
        p = z ;             % initialize p to be zero vector
        p (nzIndices) = y ; % evaluate Hessian times vector.
                            % y(i) corresponds to x(nzIndices(i))
    end
end
