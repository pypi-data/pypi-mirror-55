function napheap_make()
    % Used for printing details when compiling
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
             '../../MATLAB/Source/napheap_matlab'} ;

    % list of source files to include in mex compilation
    napheap_src = {'../Source/napheap_default', ...
                   '../Source/napheap_print', ...
                   '../Source/napheap', ...
                   '../Source/napheap_check'} ;
    
    %% ------------------- Required flags ------------------- %%
    % These flags are REQUIRED for the NAPHEAP mex function to compile
    % add '-DNAPHEAP_MATLAB' to indicate NAPHEAP
    flags = [flags ' -DNAPHEAP_MATLAB'] ;

    % add '-DSUITEOPT_MATLAB_BOUND_CONSTRAINTS' to indicate bound constraints
    flags = [flags ' -DSUITEOPT_MATLAB_BOUND_CONSTRAINTS'] ;

    %% ------------------- Debugging flags ------------------- %%
    % add '-g' flag for debugging           
    % flags = [flags ' -g'] ; 
    
    % add '-v' flag for verbose mode           
    %flags = [flags ' -v'] ; 
    
    % add '-DNDEBUG' to turn off debugging
    flags = [flags ' -DNDEBUG'] ;

    % add '-DDEBUG_SUITEOPT_MEX' to turn on debugging for SuiteOPT matlab funcs
    %flags = [flags ' -DDEBUG_SUITEOPT_MEX'] ;

    % add '-DDEBUG_NAPHEAP_MEX' to turn on debugging for NAPHEAP MEX funcs
    %flags = [flags ' -DDEBUG_NAPHEAP_MEX'] ;

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
        % logical class does not exist in MATLAB 6.1 or earlier
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
    source = [suiteopt_matlab_src napheap_src] ;
    
    % Keep track of all object files compiled for later cleanup of directory
    napheap_obj = '' ;
    
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
        napheap_obj = [napheap_obj ' ' o obj_extension] ;
        fprintf('\n\n  Making object file %s.o\n\n', o) ;
        s = sprintf('mex %s -DDLONG -O %s -c %s.c', flags, include, ff) ;
        kk = do_cmd (s, kk, details) ;
    end

    %% ---------------- Compile mex function(s) ---------------- %%
    % list of mex functions required in mex compilation of napheap
    napheap_mex_src = {'napheap_check', 'napheap'} ;
    
    % compile each mexFunction
    for f = napheap_mex_src
        fprintf('\n\n  Making mex function %s.mex\n\n', f{1}) ;
        s = sprintf('mex %s -DDLONG %s %s_mex.c %s -output %s', ...
                    flags, include, f{1}, napheap_obj, f{1}) ;
        kk = do_cmd (s, kk, details) ;
    end
    
    %% ---------------- Clean up and exit ---------------- %%
    s = ['delete ' napheap_obj] ;
    do_cmd (s, kk, details) ;
    fprintf ('\n  NAPHEAP successfully compiled\n') ;

    % Call napheap function to print information about napheap
    napheap ;
    
    %------------------------------------------------------------------------------
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
