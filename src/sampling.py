import itertools as itt
from functools import reduce
from operator import mul
from cmath import exp
import numpy as nmp
from numpy import pi

def _splice_first(t):
    x, *ys = t
    return x + tuple(ys)

def make_sample_params_iterator_maker(n, steps, r):
    """
    Make a generator of iterators that iterate over n-uples of complex
    numbers on the unit circle with a given number on steps on a half
    circle.
    """
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

    def vals_from_inds(inds):
        return (inds,
                tuple(t1[i] for i in inds),
                tuple(t2[i] for i in inds),
                reduce(mul, (t3[i] for i in inds)))

    indr1 = range(1, steps + 1)
    indr2 = range(-steps + 1, 0)

    if r is None:
        def make_ind_iterator():
            return\
                itt.product(
                        indr1,
                        *[itt.chain(indr1, indr2) for _ in range(1, n)])
    else:
        if n == 1:
            def make_ind_iterator(): return indr1
        else:
            if r % n == 0:
                rr = [r]
            else:
                rr = [r, -r]
            def make_2ind_iterator():
                for i1 in indr1:
                    for m in rr:
                        i2 = (m - i1 + n - 1) % (2*n) - n + 1
                        yield (i1, i2)
            if n == 2:
                make_ind_iterator = make_2ind_iterator
            elif n >= 3:
                def make_ind_iterator():
                    return map(_splice_first,
                            itt.product(
                                make_2ind_iterator(),
                                *[itt.chain(indr1, indr2) for
                                    _ in range(2, n)]))

    return lambda: map(vals_from_inds, make_ind_iterator())
