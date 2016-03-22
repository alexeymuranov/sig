import scipy.linalg as la

_inf = float('inf')

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
    dmat_scale = la.norm(dmat_real, ord=1) + la.norm(dmat_real, ord=_inf) +\
                 la.norm(dmat_imag, ord=1) + la.norm(dmat_imag, ord=_inf)
    mat_scale = la.norm(mat_real, ord=1) + la.norm(mat_real, ord=_inf) +\
                la.norm(mat_imag, ord=1) + la.norm(mat_imag, ord=_inf)
    return dmat_scale <= relative_discrepancy_limit*mat_scale
