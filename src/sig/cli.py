# XXX:  In spite of Style Guide for Python Code (PEP 8), not all imports in
#   this file are necessarily at the beginning: there can be more somewhere
#   inside `main` function.
from argparse import ArgumentParser, ArgumentTypeError
# NOTE: `exit` already means something in Python
from sys import exit as sys_exit


def parse_sampling_number_arg(s):
    try:
        v = int(s)
    except ValueError:
        raise ArgumentTypeError("invalid int value '{}'".format(s))
    if not v >= 1:
        raise ArgumentTypeError('{} is less than 1'.format(v))
    return v


def parse_zero_threshold_arg(s):
    try:
        v = float(s)
    except ValueError:
        raise ArgumentTypeError("invalid float value '{}'".format(s))
    if not 0 <= v < 1:
        raise ArgumentTypeError(
          '{} is not in the interval [0, 1)'.format(v)
        )
    return v


def parse_args(args):
    arg_parser = ArgumentParser(
      description = 'Some algebraic numerical calculations.'
    )
    arg_parser.add_argument(
      'input_file_name',
      metavar = 'filename',
      help = 'JSON input file name'
    )
    arg_parser.add_argument(
      '-s', '-n', '--sampling-number',
      dest = 'sampling_number',
      metavar = 'int',
      type = parse_sampling_number_arg,
      required = True,
      help = 'number of sampling steps on a semicircle'
    )
    default_eigenvalue_zero_threshold = 1e-12
    arg_parser.add_argument(
      '-z', '--zero-threshold',
      dest = 'zero_threshold',
      metavar = 'delta',
      type = parse_zero_threshold_arg,
      default = default_eigenvalue_zero_threshold,
      help = (
        'the minimal positive value considered zero when '
        'computing the signature, must be in the interval '
        '[0, 1), the default value is {}'.format(
          default_eigenvalue_zero_threshold
        )
      )
    )
    arg_parser.add_argument(
      '-g', '--signature-parameter',
      dest = 'signature_parameter',
      metavar = 'int',
      type = int,
      help = ( 'the parameter used to detect interesting '
               'signatures' )
    )
    arg_parser.add_argument(
      '-r', '--periodicity-parameter',
      dest = 'periodicity_parameter',
      metavar = 'int',
      type = int,
      help = ( 'the parameter used to select only certain pairs of '
               'first two indices' )
    )
    arg_parser.add_argument(
      '-c', '--with-caution',
      dest = 'caution',
      action = 'store_true',
      help = ( 'test the computed matrices for being not too far '
               'from being Hermitian' )
    )
    return arg_parser.parse_args(args)


def main(argv):
    # NOTE:  If parsing arguments fails or if the program is run with `-h`
    #   switch to just get the help message, the rest of the function will
    #   not be executed.  Parsing arguments before importing and defining
    #   everything thus saves time if the user runs the program with `-h`
    #   flag or if the user makes a mistake in command line arguments.
    parsed_args = parse_args(argv[1:])

    # NOTE:  Putting imports here seems to be against Style Guide for
    #   Python Code (PEP 8).  However, having imports in the body of
    #   `main` function looks more justifiable than in the bodies of
    #   other functions.
    from .runner import go

    go( parsed_args.input_file_name,
        parsed_args.sampling_number,
        parsed_args.zero_threshold,
        parsed_args.signature_parameter,
        parsed_args.periodicity_parameter,
        parsed_args.caution )

    # NOTE:  Apparently according to current practices, `main` function
    #   is expected to return the exit status (with `return`, instead of
    #   calling `sys.exit` itself).  However, since `parse_args` is called
    #   inside this function, in some cases this function will be exiting
    #   through `sys.exit` anyway (for example, if the program is called
    #   with `-h` flag to get the help message).  Thus it seems unreasonable
    #   to try to return normally from this function in other situations.
    # TODO: make sure to return the correct exit status in all situations,
    #   based on the outcome of `go` execution
    sys_exit(0)


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
