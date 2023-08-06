function cg_descent_make()
    % Used for priniting details when compiling
    details = 0 ;
    % Used during compilation of objects
    kk = 0 ;
    % Initialize flags variable to null 
    flags = '' ;
    
    %% ---------- Indicate include directories and source code ---------- %%
    include = ['-I. -I../Include -I../../SuiteOPTconfig '] ;
    % Add directories containing prototypes for SUITEOPT matlab functions
    include = [include '-I../../MATLAB/Include '] ;
    
    % list of suiteopt source files to include in mex compilation
    suiteopt_matlab_src = {...
             '../../MATLAB/Source/suiteopt_matlab', ...
             '../../MATLAB/Source/cg_descent_matlab'} ;

    % list of source files to include in mex compilation
    cg_descent_src = {'../Source/cg_default', ...
                      '../Source/cg_descent', ...
                      '../Source/cg_print', ...
                      '../Source/cg_util'} ;

    %% ------------------- Required flags ------------------- %%
    % These flags are REQUIRED for the CGDESCENT mex function to compile
    % add '-DCGDESCENT_MATLAB' to indicate NAPHEAP
    flags = [flags ' -DCGDESCENT_MATLAB'] ;

    % add '-DSUITEOPT_MATLAB_OBJ' to indicate solver uses obj/grad/valgrad
    flags = [flags ' -DSUITEOPT_MATLAB_OBJ'] ;

    % add '-DSUITEOPT_MATLAB_CGHPROD' to indicate solver uses cghprod
    flags = [flags ' -DSUITEOPT_MATLAB_CGHPROD'] ;
    
    %% ------------------- Debugging flags ------------------- %%
    % add '-g' flag for debugging           
    % flags = [flags ' -g'] ; 
    
    % add '-v' flag for verbose mode           
    % flags = [flags ' -v'] ; 
    
    % add '-DNDEBUG' to turn off debugging for cg_descent source code
    flags = [flags ' -DNDEBUG'] ;

    % add '-DDEBUG_SUITEOPT_MEX' to turn on debugging for SuiteOPT mex funcs
    % flags = [flags ' -DDEBUG_SUITEOPT_MEX'] ;

    % add '-DDEBUG_CGDESCENT_MEX' to turn on debugging for cg_descent_mex func
    % flags = [flags ' -DDEBUG_CGDESCENT_MEX'] ;
    
    %% ---------------- Detect system running MATLAB ---------------- %%
    v = version ;
    try
        % ispc does not appear in MATLAB 5.3
        pc = ispc ;
        mac = ismac ;
    catch                                                                       %#ok
        % if ispc fails, assume we are on a Windows PC if it's not unix
        pc = ~isunix ;
        mac = 0 ;
    end
    
    is64 = ~isempty (strfind (computer, '64')) ;
    if (is64)
        % 64-bit MATLAB
        flags = [flags ' -largeArrayDims'] ;
    end

    % MATLAB 8.3.0 now has a -silent option to keep 'mex' from burbling too much
    if (~verLessThan ('matlab', '8.3.0'))
        flags = ['-silent ' flags] ;
    end
    
    if (verLessThan ('matlab', '7.0'))
        % do not attempt to compile CHOLMOD with large file support
        include = [include ' -DNLARGEFILE'] ;
    elseif (~pc)
        % Linux/Unix require these flags for large file support
        include = [include ' -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE'] ;
    end
    
    if (verLessThan ('matlab', '6.5'))
        % logical class does not exist in MATLAB 6.1 or earlie
        include = [include ' -DMATLAB6p1_OR_EARLIER'] ;
    end
    
    
    if (pc)
        % Also provide Windows with an empty <strings.h> include file.
        obj_extension = '.obj' ;
        Windows_path = '../../MATLAB/Windows/' ;
        include = [include ' -I' Windows_path] ;
    else
        obj_extension = '.o' ;
    end
    
    if (pc)
        if (verLessThan ('matlab', '7.5'))
            lapack = 'libmwlapack.lib' ;
        else
            lapack = 'libmwlapack.lib libmwblas.lib' ;
        end
    else
        if (verLessThan ('matlab', '7.5'))
            lapack = '-lmwlapack' ;
        else
            lapack = '-lmwlapack -lmwblas' ;
        end
    end
    
    if (is64 && ~verLessThan ('matlab', '7.8'))
        % versions 7.8 and later on 64-bit platforms use a 64-bit BLAS
        fprintf ('with 64-bit BLAS\n') ;
        flags = [flags ' -DBLAS64'] ;
    end
    
    if (~(pc || mac))
        % for POSIX timing routine
        lapack = [lapack ' -lrt'] ;
    end
    
    %% ---------------- Compile objects from source code ---------------- %%
    source = [suiteopt_matlab_src cg_descent_src] ;
    
    % Keep track of all object files compiled for later cleanup of directory
    cg_descent_obj = '' ;
    
    % compile object files 
    for f = source 
        ff = f {1} ;
        slash = strfind (ff, '/') ;
        if (isempty (slash))
            slash = 1 ;
        else
            slash = slash (end) + 1 ;
        end
        o = ff (slash:end) ;
        cg_descent_obj = [cg_descent_obj ' ' o obj_extension] ;
        fprintf('\n\n  Making object file %s.o\n\n', o) ;
        s = sprintf('mex %s -DDLONG -O %s -c %s.c', flags, include, ff) ;
        kk = do_cmd (s, kk, details) ;
    end
    
    %% ---------------- Compile mex function(s) ---------------- %%
    % list of mex functions required in mex compilation of cg_descent
    cg_descent_mex_src = {'cg_descent'} ;
    
    % compile each mexFunction
    for f = cg_descent_mex_src
        fprintf('\n\n  Making mex function %s.mex\n\n', f{1}) ;
        s = sprintf('mex %s -DDLONG %s %s_mex.c %s %s -output %s', ...
                    flags, include, f{1}, cg_descent_obj, lapack, f{1}) ;
        kk = do_cmd (s, kk, details) ;
    end
    
    %% ---------------- Clean up and exit ---------------- %%
    s = ['delete ' cg_descent_obj] ;
    do_cmd (s, kk, details) ;
    fprintf ('\n  CGDESCENT successfully compiled\n') ;

    % Call cg_descent function to print information about cg_descent
    cg_descent ;
    
    %---------------------------------------------------------------------------
    % Function used in installation routine
    function kk = do_cmd (s, kk, details)
         %DO_CMD: evaluate a command, and either print it or print a "."
        if (details)
            fprintf ('%s\n', s) ;
        else
            if (mod (kk, 60) == 0)
                fprintf ('\n') ;
            end
            kk = kk + 1 ;
            fprintf ('.') ;
        end
        eval (s) ; 
    end

end
