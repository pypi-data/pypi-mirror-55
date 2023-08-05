# auto-generated file
__all__ = ['lib', 'ffi']

import os
from omikuji_fast._libomikuji_fast__ffi import ffi

lib = ffi.dlopen(os.path.join(os.path.dirname(__file__), '_libomikuji_fast__lib.so'), 4098)
del os
