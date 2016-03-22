#!/usr/bin/env python3

import sys, time
import argparse, json, math
import numpy as nmp
import sympy as smp
from sympy.parsing.sympy_parser import parse_expr
import scipy.linalg as la

from sampling import make_matrix_sampler,\
                     make_sample_index_iterator_maker

arg_parser = argparse.ArgumentParser(
        description='Some algebraic numerical calculations.' )
arg_parser.add_argument( 'input_file_name',
                         metavar='filename',
                         help='JSON input file name' )
def parse_sampling_number_arg(s):
    try:
        v = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(
                "invalid int value '{}'".format(s) )
    if not v >= 1:
        raise argparse.ArgumentTypeError(
                '{} is less than 1'.format(v) )
    return v
arg_parser.add_argument( '-s', '-n', '--sampling-number',
                         dest='sampling_number',
                         metavar='int',
                         type=parse_sampling_number_arg,
                         required=True,
                         help='number of sampling steps on a semicircle' )
def parse_zero_threshold_arg(s):
    try:
        v = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(
                "invalid float value '{}'".format(s) )
    if not 0 <= v < 1:
        raise argparse.ArgumentTypeError(
                '{} is not in the interval [0, 1)'.format(v) )
    return v
default_eigenvalue_zero_threshold = 1e-12
arg_parser.add_argument(
        '-z', '--zero-threshold',
        dest='zero_threshold',
        metavar='delta',
        type=parse_zero_threshold_arg,
        default=default_eigenvalue_zero_threshold,
        help='the minimal positive value considered zero when '\
                'computing the signature, must be in the interval '\
                '[0, 1), the default value is {}'.format(
                        default_eigenvalue_zero_threshold ) )
arg_parser.add_argument(
        '-g', '--signature-parameter',
        dest='signature_parameter',
        metavar='int',
        type=int,
        help='the parameter used to detect interesting signatures' )
arg_parser.add_argument(
        '-r', '--periodicity-parameter',
        dest='periodicity_parameter',
        metavar='int',
        type=int,
        help='the parameter used to select only certain pairs of first '\
                'two indices' )
args = arg_parser.parse_args()

input_file_name                 = args.input_file_name
sampling_number                 = args.sampling_number
eigenvalue_zero_threshold       = args.zero_threshold
interesting_signature_parameter = args.signature_parameter
periodicity_selection_parameter = args.periodicity_parameter

eigenvalue_zero_suspicion_threshold = math.sqrt(eigenvalue_zero_threshold)

with open(input_file_name) as f:
    data = json.load(f)

input_processing_start_time = time.process_time()

indeterminates = smp.symbols(data['indeterminates'])

e_mat = [[parse_expr(s) for s in row] for row in data['matrix']]

def analyse_eigenvalues(eigenvalues):
    """
    Compute the signature and detect "suspicious" eigenvalues (eigenvalues
    that are treated as non-zero, but whose absolute values are suspiciously
    close to the "zero threshold").
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

if interesting_signature_parameter:
    def signature_is_interesting(p, n, z):
        return abs(p - n) >= z + interesting_signature_parameter
else:
    def signature_is_interesting(_p, _n, _z): return True

get_sample_matrix = make_matrix_sampler( e_mat,
                                         indeterminates,
                                         sampling_number )

make_sample_index_iterator = make_sample_index_iterator_maker(
        len(indeterminates),
        sampling_number,
        periodicity_selection_parameter )

print(  "Initialization took {:.3g}s.".format(
                time.process_time() - input_processing_start_time ),
        file=sys.stderr )

matrix_comput_time = 0
eigval_comput_time = 0
eigval_analys_time = 0

main_loop_start_time = time.process_time()

for inds in make_sample_index_iterator():
    time0 = time.process_time()
    mat = get_sample_matrix(inds)
    time1 = time.process_time()
    eigenvalues = la.eigvalsh(mat, check_finite=False)
    time2 = time.process_time()
    signature, ( neg_suspicious_vals,
                 pos_suspicious_vals ) = analyse_eigenvalues(eigenvalues)
    time3 = time.process_time()
    time3 -= time2
    time2 -= time1
    time1 -= time0
    matrix_comput_time += time1
    eigval_comput_time += time2
    eigval_analys_time += time3
    # print(  "  Matrix computed in      {:.2e}s,\n"
    #         "  eigenvalues computed in {:.2e}s,\n"\
    #         '  eigenvalues analysed in {:.2e}s.'.format(
    #                 time1, time2, time3 ),
    #         file=sys.stderr )
    if neg_suspicious_vals or pos_suspicious_vals:
        print(  inds,
                "Attention!\n"\
                '  The following eigenvalues have been treated as '\
                "non-zero, but are\n"\
                "  suspiciously close to 0:\n"\
                '    {}'.format(
                           (neg_suspicious_vals, pos_suspicious_vals) ),
               file=sys.stderr )
    if signature_is_interesting(*signature):
        print(inds, signature)

print(  "Total time spent computing matrices:    {:.3g}s,\n"\
        "total time spent computing eigenvalues: {:.3g}s,\n"\
        'total time spent analysing eigenvalues: {:.3g}s.'.format(
                matrix_comput_time,
                eigval_comput_time,
                eigval_analys_time ),
        file=sys.stderr )
print(  'Total time spent in the main loop: {:.3g}s.'.format(
                (time.process_time() - main_loop_start_time) ),
        file=sys.stderr )
