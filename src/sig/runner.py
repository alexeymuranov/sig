from json import load as load_json
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
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

    print(
      'Input parsing took {:.3g}s.'.format(
        process_time() - input_parsing_start_time
      ),
      file = stderr
    )

    initialization_start_time = process_time()

    matrix_sampler = make_matrix_sampler( e_mat,
                                          indeterminates,
                                          sampling_number )

    sample_index_iterator_maker = make_sample_index_iterator_maker(
      len(indeterminates),
      sampling_number,
      periodicity_selection_parameter
    )

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
# ## Smoke testing
# --------------------------------------------------------------------------

if __name__ == '__main__':

    def _smoke_test():
        # TODO: implement
        assert False

    def _run_and_time_smoke_test():
        from time import process_time
        smoke_test_start_time = process_time()
        _smoke_test()
        return process_time() - smoke_test_start_time

    t = _run_and_time_smoke_test()
    print('The module has passed a smoke test in {:.3g}s.'.format(t))
