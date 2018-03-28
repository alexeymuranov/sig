# XXX:  In spite of Style Guide for Python Code (PEP 8), not all imports in
#   this file are necessarily at the beginning.
import math
from scipy.linalg import eigvalsh
from sys import stderr, stdout
from time import process_time


def make_eigenvalues_analyser(eigenvalue_zero_threshold):

    eigenvalue_zero_suspicion_threshold = math.sqrt(
        eigenvalue_zero_threshold
    )

    def eigenvalues_analyser(eigenvalues):
        """
        Compute the signature and detect "suspicious" eigenvalues
        (eigenvalues that are treated as non-zero, but whose absolute values
        are suspiciously close to the "zero threshold").
        The eigenvalues must be given in the ascending order.
        """
        # Initialize the number of negative eigenvalues
        n = 0

        for v in eigenvalues:
            if v < -eigenvalue_zero_suspicion_threshold:
                n += 1
            else:
                break

        else:
            return ((0, n, 0), ([], []))

        neg_suspicious_vals = []

        for v in eigenvalues[n:]:
            if v < -eigenvalue_zero_threshold:
                neg_suspicious_vals.append(v)
                n += 1

            else:
                break

        else:
            return ((0, n, 0), (neg_suspicious_vals, []))

        # Initialize the number of zero eigenvalues
        z = 0

        for v in eigenvalues[n:]:
            if v <= eigenvalue_zero_threshold:
                z += 1
            else:
                break

        else:
            return ((0, n, z), (neg_suspicious_vals, []))

        # The number of positive eigenvalues
        p = eigenvalues.size - (n + z)
        pos_suspicious_vals = []

        for v in eigenvalues[(n + z):]:
            if v <= eigenvalue_zero_suspicion_threshold:
                pos_suspicious_vals.append(v)
            else:
                break

        return ((p, n, z), (neg_suspicious_vals, pos_suspicious_vals))

    return eigenvalues_analyser


def make_interesting_signature_detector(interesting_signature_parameter):

    if interesting_signature_parameter:
        def interesting_signature_detector(signature):
            p, n, z = signature
            return abs(p - n) >= z + interesting_signature_parameter

        return interesting_signature_detector

    else:
        return lambda _signature: True


# TODO: use `logging` module instead of printing to `stderr`
def process_data( matrix_sampler,
                  sample_index_iterator_maker,
                  eigenvalue_zero_threshold,
                  interesting_signature_parameter,
                  caution = False,
                  output_dest = stdout,
                  message_output_dest = stderr ):

    if caution:
        # NOTE: putting imports here seems to be against Style Guide for
        #   Python Code (PEP 8)
        from .checking_matrices import is_hermitian

    analyse_eigenvalues = make_eigenvalues_analyser(
        eigenvalue_zero_threshold
    )

    signature_is_interesting = make_interesting_signature_detector(
        interesting_signature_parameter
    )

    get_sample_matrix = matrix_sampler

    make_sample_index_iterator = sample_index_iterator_maker

    matrix_comput_time = 0
    eigval_comput_time = 0
    eigval_analys_time = 0

    main_loop_start_time = process_time()

    for inds in make_sample_index_iterator():
        time0 = process_time()
        mat = get_sample_matrix(inds)

        # If `caution` is true, check that the matrix is "almost"
        # Hermitian:
        if caution and not is_hermitian(mat):
            print( inds,
                   ": Attention!\n"
                   "  The computed matrix does not seem to be "
                   "sufficienly close to Hermitian:\n"
                   "{}".format(mat),
                   file = message_output_dest )

        # Transform the matrix to a truly Hermitian one:
        mat += mat.H
        time1 = process_time()
        eigenvalues = eigvalsh(mat, check_finite=False)
        time2 = process_time()
        (signature, (neg_suspicious_vals, pos_suspicious_vals)) = (
            analyse_eigenvalues(eigenvalues)
        )
        time3 = process_time()
        time3 -= time2
        time2 -= time1
        time1 -= time0
        matrix_comput_time += time1
        eigval_comput_time += time2
        eigval_analys_time += time3
        # print( "  Matrix computed in      {:.2e}s,\n"
        #        "  eigenvalues computed in {:.2e}s,\n"
        #        "  eigenvalues analysed in {:.2e}s."
        #        .format(time1, time2, time3),
        #        file = message_output_dest )

        if neg_suspicious_vals or pos_suspicious_vals:
            print( inds,
                   ": Attention!\n"
                   "  The following eigenvalues have been treated as "
                   "non-zero, but are\n"
                   "  suspiciously close to 0:\n"
                   "    {}"
                   .format((neg_suspicious_vals, pos_suspicious_vals)),
                   file = message_output_dest )

        if signature_is_interesting(signature):
            print(inds, ":", signature, file=output_dest)

    print( "Total time spent in the main loop: {:.3g}s.\n"
           "This includes the time spent\n"
           "  - computing matrices:    {:.3g}s,\n"
           "  - computing eigenvalues: {:.3g}s,\n"
           "  - analysing eigenvalues: {:.3g}s."
           .format( (process_time() - main_loop_start_time),
                    matrix_comput_time,
                    eigval_comput_time,
                    eigval_analys_time ),
           file = message_output_dest )


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
