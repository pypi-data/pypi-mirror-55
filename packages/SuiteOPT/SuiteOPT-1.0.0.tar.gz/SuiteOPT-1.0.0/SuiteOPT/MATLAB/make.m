function make()
  %% ----------------------- Prompt user for input ------------------------ %%
  % Initialize array of solvers
  solvers = {'cg_descent', 'napheap', 'pproj', 'pasa'} ;
  % Initialize user prompt to select solver
  fprintf('  1 CGDESCENT: Unconstrained optimization\n') ;
  fprintf('  2 NAPHEAP..: Separable convex quadratic knapsack problem\n') ;
  fprintf('  3 PPROJ....: Projection onto polyhedron\n') ;
  fprintf('  4 PASA.....: Polyhedral constrained optimization\n') ;
  fprintf('  5 Install all solvers\n\n') ;
  fprintf('  0 Exit installation\n\n') ;
  fprintf('To indicate the solver to be installed in MATLAB, type an integer\n')
  fprintf('between 1 and 5, or type 0 to exit; then press enter:') ;
  i = input(' ') ;
  % Start outer while loop to stay in program until user is done
  while(1)
    % Check if i is 0
    if (i == 0)  
      break
    end
    
    %% --------------- Install user specified solver(s) ---------------- %%
    if(i < length(solvers)+1)
      % Install one solver 
      installed = install_solver( solvers{i} ) ;
      % Print out instructions to user
      wrapup_installation( installed, solvers{i} ) ;
      fprintf('But first, would you like to install another solver?\n') ;
      fprintf('If so, type an integer between 1 and 5, or type 0 to exit;\n') ;
      fprintf('then press return:') ;
      i = input(' ') ;
    else
      % Initialize installed array
      installed = zeros(length(solvers)) ;
      % Install all solvers 
      for i = 1:length(solvers)
        installed(i) = install_solver( solvers{i} ) ;
      end
      % Print out instructions to user
      wrapup_installation( installed, solvers ) ;
      break ;
    end
  end

  %---------------------------------------------------------------------------
  % Functions used in installation routine
  function [installed] = install_solver(solver)
    % Initialize installed to 1 
    installed = 1 ;
    % Navigate to solver MATLAB directory
    if ( strcmp(solver,'cg_descent') )
      % Set folder name to uppercase folder name
      folder = 'CGDESCENT' ;
    else
      % Set folder name to uppercase name of solver
      folder = upper(solver) ;
    end
    s = sprintf('cd ../%s/MATLAB', folder) ;
    eval(s) ;
    % Print message for installing solver
    fprintf('Installing %s for use with MATLAB...\n\n', solver) ;
    % Run solver_make to install solver
    s = sprintf('%s_make', solver) ;
    try
      eval(s) ;
    catch install_error
      % Error occured so set installed to 0 
      installed = 0 ;
      % Print error message
      fprintf('\nError installing %s...\n', solver) ;
      fprintf(1,'\nError identifier:\n%s\n', install_error.identifier) ;
      fprintf(1,'\nError message...:\n%s\n', install_error.message) ;
      % Check for certain type of error indicative of missing SuiteSparse
      if (strcmp(install_error.identifier, 'MATLAB:mex:SrcNotFound'))
        fprintf(['\nBased on this error, it is likely that the user has\n',...
                 'not provided a symbolic link to SuiteSparse in the\n',...
                 'SuiteOPT directory which is required for the\n',...
                 'installation of pproj and pasa.\n\n']) ;
      end
    end
    % Navigate back to main MATLAB directory
    eval('cd ../../MATLAB') ;
  end

  function wrapup_installation(installed, solver)
    % Check if installation was successful 
    if (length(installed) == 1)
      % User installed one solver
      if (installed)
        if ( strcmp(solver,'cg_descent') )
          folder = 'cg' ;
        else
          folder = solver ;
        end
        fprintf(['\nInstallation of %s for use with MATLAB complete!\n',...
               '\nTo use the SuiteOPT solver %s in MATLAB, navigate to\n',...
               'the directory containing %s.mex by typing "cd %s".\n\n',...
              'After navigating to the "%s" directory, information on how\n',...
               'to set up and solve a problem using %s can be viewed by\n',...
               'typing "%s". For a set up example, type "%s demo".\n\n'],...
               solver, solver, solver, folder, folder, solver, solver, solver) ;
      else % Installation failed
        fprintf(['\nFailed to install %s for use with MATLAB.\n',...
             '\nTo determine what caused the installation to fail\n',...
             'check the command window output during the installation\n',...
             'of the solver %s.\n\n'], solver, solver) ;
      end
    else % User installed all solvers
      % Initialize vell array to contain successful and failed solvers
      success = {} ;
      failed = {} ;
      % Determine successful and failed installations 
      for i = 1:length(installed) 
        % Check if solver installed
        if ( installed(i) )
          % Successfully installed solver i
          success{end+1} = solver{i} ; 
        else
          % Failed to install solver i
          failed{end+1} = solver{i} ; 
        end
      end
      % Print successful installations 
      if (~isempty(success))
        % Join strings in cell array
        success = strjoin(success,'/') ;
        % Print success message
        fprintf(['\nInstallation of %s for use with MATLAB complete!\n',...
             '\nTo use the SuiteOPT solver(s) %s in MATLAB,\n',...
             'navigate to the directory containing %s.mex\n',...
             'by typing "cd solver_name" where solver_name is the name of\n',...
             'the solver that will be used. After navigating to the\n',...
             'correct directory, information on how to set up and solve\n',...
             'a problem is obtained by typing "solver_name".\n',...
             'To see a set up problem, type "solver_name demo".\n\n'],...
             success, success, success) ;
      end

      % Print failed installations 
      if (~isempty(failed))
        % Join strings in cell array
        failed = strjoin(failed,'/') ;
        % Print failed message
        fprintf(['\nFailed to install %s for use with MATLAB.\n',...
             '\nTo determine what caused the installation to fail\n',...
             'check the command window output during the installation\n',...
             'of the solver(s) %s.\n\n'], failed, failed) ;
      end
    end
  end

end
