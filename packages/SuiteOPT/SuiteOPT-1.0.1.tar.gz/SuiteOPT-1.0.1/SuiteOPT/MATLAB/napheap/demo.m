function demo
%% -------------------------- Problem Details -------------------------- %%
%   This is a demo for solving a problem of the form
%
%              min     0.5 * x'*D*x - y'*x
%              s.t     lo <= x <= hi, blo <= a'*x <= bhi
%
%   using the napheap mex function.

%% ------------------- Initialize inputs for napheap ------------------- %%
    rng('default') ;
    n = 20 ; % dimension of primal variable
    d = 5 + 5*rand (n, 1) ;   % diagonal hessian of cost function
    y = 20*rand (n, 1) - 10 ; % linear term in cost function
    a = 20*rand (n, 1) - 10 ; % linear constraint vector
    lo = -ones (n, 1) ;       % lower bound for x
    hi =  ones (n, 1) ;       % upper bound for x
    cumlo = 0 ;
    cumhi = 0 ;
    for j = 1:n
        t = a (j)*lo (j) ;
        s = a (j)*hi (j) ;
        cumlo = cumlo + min (t, s) ;
        cumhi = cumhi + max (t, s) ;
    end
    blo = cumlo + (cumhi-cumlo)*rand ; % lower bound for a'*x
    bhi = blo + 10 ;                   % upper bound for a'*x

%% ------------- User defined parameter values for napheap ------------- %%
    % See napheap_default inside Source/napheap.c for a description of
    % the parameters.
    napdata.PrintStat = 1 ;   % print NAPHEAP statistics

%% -------------------------- Calling napheap -------------------------- %%
    % ------------------- Set options for napheap ------------------- %
    napdata.d   = d ;   % diagonal hessian of cost function
    napdata.y   = y ;   % linear term in cost function
    napdata.a   = a ;   % linear constraint vector
    napdata.lo  = lo ;  % lower bound for x
    napdata.hi  = hi ;  % upper bound for x
    napdata.blo = blo ; % lower bound for a'*x
    napdata.bhi = bhi ; % upper bound for a'*x
    % If the problem dimension is smaller than the length of the data arrays,
    % then the problem dimension could be provided in napdata.n
    % A starting guess for the multiplier associated with the constraint
    % blo <= a'*x <= bhi could (optionally) be provided in napdata->lambda.
    % By default, napdata->blo = -infinity and napdata->bhi = +infinity.
    % The lower bound napdata->lo is assumed to be -infinity if not provided.
    % The upper bound napdata->hi is assumed to be +infinity if not provided.

    % ------------------------- Call napheap ------------------------ %
    % The only required output argument is x; the statistics structure stats
    % and the multiplier lambda are optional.  To obtain lambda, the stats
    % argument must be present.
    [x, stats, lambda] = napheap (napdata) ;

%% ----------------------- Print napheap outputs ----------------------- %%
    % Since napdata.PrintStat = 1, the napheap statistics were printed
    % at the end of the run. The numerical values for the statistics are
    % stored in the stats structure, which is a output argument in this
    % example.

    % print solution for x
    fprintf('\n  -------------------------- Solution ')
    fprintf('-------------------------\n')
    fprintf('x =\n')
    disp(x)

    % print newlambda
    fprintf('\n  ------------------------- Multiplier ')
    fprintf('------------------------\n')
    fprintf('    lambda = ')
    disp(lambda)

%% ----------------------- Calling napheap_check ----------------------- %%
    % ---------------- Set options for napheap_check ---------------- %
    napdata.x = x ; % store primal solution in napdata
    napdata.lambda = lambda ; % store dual solution in napdata

    % ---------------------- Call napheap_check --------------------- %
    [err, errb, errB, erry] = napheap_check (napdata) ;

%% -------------------- Print napheap_check outputs -------------------- %%
    % print napheap statistics
    fprintf('\n  ----------------- NAPHEAP check error values ')
    fprintf(     '----------------\n')
    fprintf('    errb = ')
    disp(errb)

    fprintf('    errB = ')
    disp(errB)

    fprintf('    erry = ')
    disp(erry)
