from itertools import chain as iter_chain
from itertools import product as iter_product


def _splice_first(t):
    x, *ys = t
    return x + tuple(ys)


def make_sample_index_iterator_maker(n, steps, r):
    """
    Make a generator of iterators that iterate over n-uples of integers
    that parametrize certain complex numbers on the unit circle with a
    given number of steps on a semicircle.
    """

    indr1 = range(1, steps + 1)
    indr2 = range(-steps + 1, 0)

    if r is None:
        return lambda: iter_product(
            indr1,
            *[iter_chain(indr1, indr2) for __ in range(1, n)]
        )

    else:
        if n == 1:
            return lambda: iter(indr1)

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
                return make_2ind_iterator

            elif n >= 3:
                return lambda: map(
                    _splice_first,
                    iter_product( make_2ind_iterator(),
                                  *[ iter_chain(indr1, indr2)
                                     for __ in range(2, n) ] )
                )


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# --------------------------------------------------------------------------
# ## Basic testing
# --------------------------------------------------------------------------

if __name__ == "__main__":

    from ._basic_testing_tools import run_and_time

    def _basic_tests():
        # TODO: implement
        assert False

    t = run_and_time(_basic_tests)
    print("The module passed basic tests in {:.3g}s.".format(t))
