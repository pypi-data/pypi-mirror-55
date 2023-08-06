% Test problem contributed by Mahya Aghaee
function demoOC
%% --------------------- Initialize inputs for pasa -------------------- %%
    % ------ Initialize constant parameters ------ %
    global gama beta nu rho kappa mu alpha eta T n a b c p
    clf ;
    gama = 0.00683 ;   %birth rate of the population
    nu = 0.00188 ;     %natural death rate of the population
    beta = 0.2426 ;    %rate of infectiousness of the disease
    rho = 0.007 ;      %resensitization rate
    kappa = 0.3 ;      %effectiveness of vaccination
    mu = 0.005 ;       %disease induced death rate
    alpha = 0.00002 ;  %rate at which disease is overcome
    eta = 0.1 ;        %effectiveness of treatment
    T = 50 ;           %time horizon (weeks)
    n = 2000 ;         % Dimension of u and v
    a = 5 ;            % Constant in cost function
    b = 50 ;           % Constant in cost function
    c = 300 ;          % Constant in cost function
    p = 1e-1 ;         % penalty parameter in cost function
    h = T/n ;          % Step size
    S = zeros (n, 1) ;
    I = zeros (n, 1) ;
    R = zeros (n, 1) ;

    % ------------ Initialize matrix A ----------- %
    A1 = spdiags([ones(n-1,1) -ones(n-1,1)], [0,1], n-1, n) ;
    A2 = speye(n-1,n) ;
    A = sparse (n-1, 4*n-2) ;
    A(:, 1:6000) = [A1 -A2 A2] ;

    % ------- Initialize polyhedral bounds ------- %
    bl = zeros (n-1,1) ;
    bu = zeros (n-1,1) ;

    % -------- Initialize variable bounds -------- %
    lo = zeros(4*n-2,1) ;
    hi = [ones(n,1); inf*ones(n-1,1); inf*ones(n-1,1); ones(n,1)] ;

    % ------- Initialize pasadata for pasa ------- %

%% ---------------- User defined parameter values for pasa ------------- %%
    % See pasa_default inside Source/pasa.c for a description of the
    % parameters. See pproj_default inside PPROJ/Source/pproj.c for
    % a description of the parameters.
    pasadata.pasa.PrintStat = 1 ;       % print statistics for used routines
    pasadata.pasa.grad_tol = 1.e-8 ;    % stopping tolerance for PASA

    % -------------------- Setup pasadata -------------------- %
    % since pasadata.x and pasadata.lambda are not given, the initial values
    % for the solution and for the multipliers associated with the constraints
    % bl <= A*x <= bu are zero
    pasadata.lo = lo ;                  % lower bound for x
    pasadata.hi = hi ;                  % upper bound for x
    pasadata.A = A ;                    % sparse matrix A
    pasadata.bl = bl ;                  % lower bound for Ax
    pasadata.bu = bu ;                  % upper bound for Ax
    pasadata.gradient = @grad ;         % objective gradient
    pasadata.objective = @computeCost ; % objective value

    % --------------- Call pasa to determine optimal x -------------- %
    [x, stats] = pasa (pasadata) ;

    % Since pasadata.pasa.PrintStat = 1, the statistics are displayed at
    % the end of the run. Since the stats structure was included as an
    % output, the corresponding numerical entries cat be found in the
    % structures stats.pasa and stats.cg

    % ---------------------- Plot the states ---------------------- %
    [S, I, R] = state (x(1:n), x(3*n-1: 4*n-2));

    t = linspace (0, T, n) ;
    subplot(3,2,1)
    plot (t, S,'linewidth',2) ;
    xlabel('Time')
    ylabel('S')
    subplot(3,2,2)
    plot (t, I, 'linewidth',2) ;
    xlabel('Time')
    ylabel('I')
    subplot(3,2,3)
    plot (t, R, 'linewidth',2) ;
    xlabel('Time')
    ylabel('R')

    % ----------------- Plot the controls u and v ----------------- %
    u = x (1:n) ;
    v = x (3*n-1:4*n-2) ;
    t = linspace (0, T, n) ;
    subplot(3,2,5);
    plot (t, u,'linewidth',2) ;
    xlabel('Time')
    ylabel({'Control','(Vaccination)'})
    subplot(3,2,6);
    plot (t, v, 'linewidth',2) ;
    xlabel('Time')
    ylabel({'Control','(Treatment)'})


    % ----------- Determine switching time for control u ------------ %
    % Determine index of mesh where first switch occurs
    index = 1 ;
    while (u(index) == 1)
        index = index + 1 ;
        if (index > n)
           break ;
        end
    end
    % Set initial switching time for u
    u_t1 = T * (index - 1)/n ;

    % Determine index of mesh where final switch occurs
    index = n ;
    while (u(index) == 0)
        index = index - 1 ;
        if (index < 0)
           break ;
        end
    end
    % Set final switching time for u
    u_t2 = T * (index + 1)/n ;

    % ----------- Determine switching time for control v ------------ %
    % Determine index of mesh where first switch occurs
    index = 1 ;
    while (v(index) == 1)
        index = index + 1 ;
        if (index > n)
           break ;
        end
    end
    % Set initial switching time for v
    v_t1 = T * (index - 1)/n ;

    disp('Jump times for the control:') ;
    fprintf ('v: %e u1: %e u2: %e\n', v_t1, u_t1, u_t2) ;

%% ------------------ User defined functions for pasa ------------------ %%
    % ---- Objective function ---- %
    function J = computeCost(x)
        h = T/n ;
        u = x(1:n) ;
        zeta = x(n+1:2*n-1) ;
        iota = x(2*n:3*n-2) ;
        v = x(3*n-1: 4*n-2) ;
        [S, I, R] = state (u, v) ;
        J = h*(a*sum(I) + b*sum(u) + c*sum(v)) ;
        J = J + p*sum(zeta + iota) ;
    end

    % ---- Gradient of objective function ---- %
    function g = grad(x)
        h = T/n ;
        u = x(1:n) ;
        v = x(3*n-1: 4*n-2) ;

        % Compute state and costate
        [S, I, R] = state (u, v);
        [lS, lI, lR] = costate (S, I, R, u, v) ;

        % Update gradient values
        for i=1:n
            Fu(i) = h*(b - lS(i)*kappa*S(i) + lR(i)* kappa*S(i));
            Fv(i) = h*(c - lI(i)*eta*I(i) + lR(i)*eta*I(i));
        end

        % Store gradient values in array g to return
        g = [Fu, p*ones(1,n-1), p*ones(1,n-1), Fv] ;
    end

    % ---- State ---- %
    function [S, I, R] = state (u, v)
        h = T/n;
        S(1) = 1000 ;
        I(1) = 10 ;
        R(1) = 0 ;

        for i = 1:n-1
            N = S(i) + I(i) + R(i) ;
            S(i + 1) = S(i) + h*(gama*N - nu*S(i) - (beta*S(i)*I(i))/N ...
                +  rho*R(i) - kappa*S(i)*u(i));
            I(i + 1) = I(i) + h*(beta*S(i)*I(i)/N - (nu + mu + alpha)*I(i)...
                - eta*I(i)*v(i)) ;
            R(i + 1) = R(i) + h*( - nu*R(i) - rho*R(i) ...
                +  kappa*S(i)*u(i) + alpha*I(i) + eta*I(i)*v(i)) ;
        end
    end

    % ---- Costate ---- %
    function [lS, lI, lR] = costate (S, I, R, u, v)
        h = T/n ;
        lS(n) = 0 ;
        lI(n) = 0 ;
        lR(n) = 0 ;

        for i=n:-1:2
            N = S(i) + I(i) + R(i) ;
            lS(i-1) = lS(i)+ h*lS(i)*(gama - nu - beta*(I(i)/N) ...
                        + beta*(S(i)*I(i)/(N^2)) - kappa*u(i))...
                        + h*lI(i)*(beta*(I(i)/N) - beta*(S(i)*I(i)/(N^2)))...
                        + h*lR(i)*(kappa*u(i));
            lI(i-1) = lI(i)+ h*a +h*lS(i)*(gama - (beta*S(i))/N ...
                        + (beta*S(i)*I(i))/N^2)...
                        + h*lI(i)*(( beta*S(i))/N - (beta*S(i)*I(i))/(N^2) ...
                        - (nu + mu + alpha) - eta*v(i))...
                        + h*lR(i)*(alpha + eta*v(i));
            lR(i-1) = lR(i)+ h*lS(i)*(gama + (beta*S(i)*I(i))/(N^2) + rho)...
                        + h* lI(i)*(- (beta*S(i)*I(i))/(N^2) ) ...
                        + h* lR(i)*(- nu - rho);
        end
    end

end
