from time import process_time

def run_and_time(f, *args, **kwargs):
    start_time = process_time()
    f(*args, **kwargs)
    return process_time() - start_time
