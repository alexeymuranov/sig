import numpy as nmp
from functools import reduce
from math import pi
from operator import mul
from sympy.utilities import lambdify


def make_matrix_sampler(e_mat, indeterminates, steps):

    # Build look-up tables t1, t2, t3
    t0 = nmp.exp(nmp.linspace(0, pi, steps + 1)[1:steps]*1j)
    t0 /= nmp.abs(t0)

    t1 = nmp.empty(2*steps, dtype=complex)
    t1[0] = 1
    t1[1:steps] = t0
    t1[steps] = -1
    t1[steps+1:] = nmp.conj(t1[steps-1:0:-1])

    t2 = -nmp.conj(t1)
    t3 = -t1 + 1

    def zero_func(*__): return 0

    # Using `zero_func` for zeros is faster
    def func_from_expr(e):
        if e == 0:
            return zero_func
        else:
            return lambdify(indeterminates, e)

    f_mat = [[func_from_expr(e) for e in row] for row in e_mat]

    def matrix_sampler(inds):
        vals = tuple(t2[i] for i in inds)
        mat = nmp.matrix( [[f(*vals) for f in row] for row in f_mat],
                          dtype = complex )
        mat *= reduce(mul, (t3[i] for i in inds))
        return mat

    return matrix_sampler


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# --------------------------------------------------------------------------
# ## Basic testing
# --------------------------------------------------------------------------

if __name__ == '__main__':

    from ._basic_testing_tools import run_and_time

    def _basic_tests():
        # TODO: implement
        assert False

    t = run_and_time(_basic_tests)
    print('The module passed basic tests in {:.3g}s.'.format(t))
