

## DeepSurv


1. Create a script ```setup_functions.py``` with contents:
  ```
  import cython
  from Cython.Build import cythonize

  from distutils.core import setup, Extension



  # https://github.com/square/pysurvival/blob/841b9bc6ce700ba8898d2a1488aa9cd25ee7a8e6/setup.py | c++11

  setup(ext_modules = cythonize(Extension(
      "_functions",
      sources=["_functions.pyx" ],
      language="c++11",
      include_dirs=["../base"],
      extra_compile_args=["-DPLATFORM=linux -std=c++11"]
  )))
  ```
2. Execute:
  ```module load gcc/9.1.0```
3. Rum script
  ```python setup_functions.py build_ext --inplace```
  
