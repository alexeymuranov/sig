from scipy import inf
from scipy.linalg import norm


def is_hermitian(mat, relative_discrepancy_limit=1e-10):
    """
    Check that the square matrix is "relatively close" to being Hermitian.
    The matrix `mat` is expected to be a NumPy matrix.
    """
    dmat = mat - mat.H
    dmat_real = dmat.real
    dmat_imag = dmat.imag
    mat_real = mat.real
    mat_imag = mat.imag
    dmat_scale = ( norm(dmat_real, ord=1) + norm(dmat_real, ord=inf)
                 + norm(dmat_imag, ord=1) + norm(dmat_imag, ord=inf) )
    mat_scale = ( norm(mat_real, ord=1) + norm(mat_real, ord=inf)
                + norm(mat_imag, ord=1) + norm(mat_imag, ord=inf) )
    return dmat_scale <= relative_discrepancy_limit*mat_scale


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# --------------------------------------------------------------------------
# ## Smoke testing
# --------------------------------------------------------------------------

if __name__ == '__main__':

    def _smoke_test():
        import numpy as nmp
        hermitian_matrix = nmp.matrix(
          [[1, 1+2j], [1-2j, 3]],
          dtype = complex
        )
        almost_hermitian_matrix1 = nmp.matrix(
          [[1, 1+2j], [1-2.00000000001j, 3]],
          dtype = complex
        )
        almost_hermitian_matrix2 = nmp.matrix(
          [[1, 1+2j], [1-2j, 3+0.00000000001j]],
          dtype = complex
        )
        non_hermitian_matrix1 = nmp.matrix(
          [[1, 1+2j], [1-2.1j, 3]],
          dtype = complex
        )
        non_hermitian_matrix2 = nmp.matrix(
          [[1, 1+2j], [1-2j, 3+0.1j]],
          dtype = complex
        )
        non_hermitian_matrix3 = nmp.matrix(
          [[1j, 1], [1, -1j]],
          dtype = complex
        )
        assert is_hermitian( hermitian_matrix,
                             relative_discrepancy_limit = 1e-10)
        assert is_hermitian( almost_hermitian_matrix1,
                             relative_discrepancy_limit = 1e-10 )
        assert is_hermitian( almost_hermitian_matrix2,
                             relative_discrepancy_limit = 1e-10 )
        assert not is_hermitian( non_hermitian_matrix1,
                                 relative_discrepancy_limit = 1e-10 )
        assert not is_hermitian( non_hermitian_matrix2,
                                 relative_discrepancy_limit = 1e-10 )
        assert not is_hermitian( non_hermitian_matrix3,
                                 relative_discrepancy_limit = 1e-10 )
        assert not is_hermitian( almost_hermitian_matrix1,
                                 relative_discrepancy_limit = 1e-12 )
        assert not is_hermitian( almost_hermitian_matrix2,
                                 relative_discrepancy_limit = 1e-12 )

    def _run_and_time_smoke_test():
        from time import process_time
        smoke_test_start_time = process_time()
        _smoke_test()
        return process_time() - smoke_test_start_time

    t = _run_and_time_smoke_test()
    print('The module has passed a smoke test in {:.3g}s.'.format(t))
