import numpy as nmp
from functools import reduce
from math import pi
from operator import mul
from sympy.utilities import lambdify


def _first_to_nmp_array(p):
    a, b = p
    return (nmp.array(a, dtype=int), b)

def make_matrix_sampler(p_mat, indeterminates, steps):
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

    def zero_func(__): return 0

    def t1_i(m, inds): return (steps*sum(m) - sum(inds*m)) % (2*steps)

    def make_polynomial_sampler(p):
        if p.is_zero:
            return zero_func
        else:
            l = list(map(_first_to_nmp_array, p.as_dict().items()))
            def get_sample(inds):
                inds = nmp.array(inds, dtype=int)
                return sum(c*t1[t1_i(m, inds)] for m, c in l)
            return get_sample

    sampling_mat = [ [make_polynomial_sampler(p) for p in row]
                     for row in p_mat ]

    def matrix_sampler(inds):
        mat = nmp.matrix( [[f(inds) for f in row] for row in sampling_mat],
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
