import ctypes
import numpy

from vitaoptimum.vo.constrained import VitaOptimumConstrained
from vitaoptimum.base import Strategy, Validation
from vitaoptimum.result import VitaOptimumIcsResult


class Ics(VitaOptimumConstrained):
    """Integer Constrained Global Optimization Method"""

    def __init__(self, fobj, dim, ng, nh, low, high,
                 nfe=10000, np=25, f=0.85, cr=0.4,
                 strategy=Strategy.rand3, tol=0.001):
        self._low = low
        self._high = high
        self._f = f
        self._cr = cr
        VitaOptimumConstrained.__init__(self, fobj, dim, nfe, np, strategy, ng, nh, tol)

    def run(self, restarts=1, verbose=False):
        """Runs the algorithm"""

        xopt = numpy.zeros(self._dim, dtype=ctypes.c_int)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)
        constr = numpy.zeros(self._ng + self._nh, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_int),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int)

        self._lib.vitaOptimum_Ics.restype = ctypes.c_double
        self._lib.vitaOptimum_Ics.argtypes = [ctypes.c_bool,
                                              callback_type,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              self._array_1d_int,
                                              self._array_1d_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_double,
                                              ctypes.c_double,
                                              ctypes.c_int,
                                              ctypes.c_double,
                                              self._array_1d_int,
                                              self._array_1d_double,
                                              self._array_1d_double
                                              ]
        best = self._lib.vitaOptimum_Ics(verbose,
                                         callback_type(self._fobj),
                                         self._dim,
                                         self._ng,
                                         self._nh,
                                         self._low,
                                         self._high,
                                         self._nfe,
                                         self._np,
                                         self._f,
                                         self._cr,
                                         self._strategy.value,
                                         self._tol,
                                         xopt,
                                         constr,
                                         conv)
        return VitaOptimumIcsResult(self._dim, self._low, self._high,
                                    self._fobj_orig, best, xopt, constr,
                                    self._ng, self._nh,
                                    conv[:int(self._nfe / self._np) * self._np])

    def info(self):
        self._lib.vitaOptimum_Ics_info()

    def _validate(self):
        Validation.lh(self._low, self._high, self._dim)
        Validation.f(self._f)
        Validation.cr(self._cr)

    def _fobj_wrapper(self, x, d, g, ng, h, nh):
        x = numpy.ctypeslib.as_array(x, shape=(d,))
        g = numpy.ctypeslib.as_array(g, shape=(ng,))
        h = numpy.ctypeslib.as_array(h, shape=(nh,))
        return self._fobj_orig(x, g, h)

    def _set_wrapper(self, fobj_orig):
        self._fobj = self._fobj_wrapper
