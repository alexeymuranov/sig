from json import load as load_json
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
from sympy.polys.polytools import poly
from sys import stderr
from time import process_time

from .analysing import process_data
from .sampling import make_matrix_sampler
from .sweeping import make_sample_index_iterator_maker


def go( input_file_name,
        sampling_number,
        eigenvalue_zero_threshold,
        interesting_signature_parameter,
        periodicity_selection_parameter,
        caution ):

    with open(input_file_name) as f:
        data = load_json(f)

    input_parsing_start_time = process_time()

    indeterminates = symbols(data['indeterminates'])

    e_mat = [[parse_expr(s) for s in row] for row in data['matrix']]
    p_mat = [[poly(e, *indeterminates) for e in row] for
                row in e_mat]

    # TODO: use `logging` module instead of printing to `stderr`:
    #
    #     https://docs.python.org/3/library/logging.html
    #
    print(
      'Input parsing took {:.3g}s.'.format(
        process_time() - input_parsing_start_time
      ),
      file = stderr
    )

    initialization_start_time = process_time()

    matrix_sampler = make_matrix_sampler( p_mat,
                                          indeterminates,
                                          sampling_number )

    sample_index_iterator_maker = make_sample_index_iterator_maker(
      len(indeterminates),
      sampling_number,
      periodicity_selection_parameter
    )

    # TODO: use `logging` module instead of printing to `stderr`
    print(
      'Initialization took {:.3g}s.'.format(
        process_time() - initialization_start_time
      ),
      file = stderr
    )

    process_data( matrix_sampler,
                  sample_index_iterator_maker,
                  eigenvalue_zero_threshold,
                  interesting_signature_parameter,
                  caution = caution )


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
