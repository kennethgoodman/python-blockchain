import numpy as np

def power_of_n(num, n):
    if int(n) == 2:
        return num != 0 and ((num & (num - 1)) == 0)
    else:
        raise NotImplementedError("Have not implemented n != 2, you put: n = {}".format(n))

def next_power_of_n(number, n):
    # Returns next power of two following 'number'
    log_c_x = np.log2(number)
    log_c_b = np.log2(n)
    log_b_x = log_c_x / log_c_b
    return np.ceil(log_b_x)
