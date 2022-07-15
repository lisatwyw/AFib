

# 1. Deep Survival Models
# 2. MLP-surv
# 3. DeepSurv

- Simplified from ```pysurvival```

0. Install Cython package
  ```pip install Cython --install-option="--no-cython-compile"```

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

### Round 1
- 70% training set
- 9105 hospitalized patients
- maximum time2event: 5.5 

| Algm | Brier Score | C-index |
|--|--|--|
| Nnet-survival | n/a | 72.8 | 
| DeepSurv-150 | n/a | 73.8 |
| DeepSurv-117-78 | n/a | 73.90 |
| DeepSurv-156-78-117 | n/a | 73.90 |


### Round 2
- 70% training + validation set

| Algm | Settings|Brier Score | C-index |
|--|--|--|--|
| Nnet-survival | Zeros | n/a | 72.7, 72.5 | 
| Nnet-survival | RandU | n/a | 72.8, 72.7 | 
| MLP-surv |BN-DO0-BS64 | n/a | 74.9, 71.6 | 
| MLP-surv |BN-DO0.3-BS64 | n/a | 73.5, 73.1 | 
| MLP-surv |BN-DO0.3-BS256 | n/a | 72.5, 72.3 | 

