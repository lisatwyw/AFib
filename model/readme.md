

# 1. Deep Survival Models
# 2. MLP-surv
# 3. DeepSurv

- Simplified from ```pysurvival```

1. Cythonize: 
  ```cythonize -a -i _functions.pyx```
2. Create a script ```setup_functions.py``` with contents:
  ```
    from setuptools import setup, Extension
    from Cython.Build import cythonize
    
    setup(ext_modules = cythonize( Extension(      
        name="_functions",
        sources = ["cpp_extensions/_functions.cpp",
               "cpp_extensions/functions.cpp" ,
               ],        
        extra_compile_args = extra, 
        language="c++" 
      )))
    
    
  ```
3. Execute:
  ```module load gcc/9.1.0```
4. Run script:
  - ```python setup_functions.py build_ext --inplace```; or 
  - ```python setup_functions.py install --user  # <-- if you don't have admin rights ```
  
 

## Requirements

- torch
- copy
- progressbar



## Results on SUPPORT

| Algm | Brier Score | C-index |
|--|--|--|
| DeepSurv-150 | n/a | 73.8 |
| DeepSurv-117-78 | | 73.9 |
