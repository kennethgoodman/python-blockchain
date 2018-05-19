from mathlib import power_of_n, next_power_of_n
import numpy as np

def pad_to_power_of_n(arr, n):
    arr = np.array(arr)
    nextPower = next_power_of_n(len(arr), n=n)
    deficit = int(np.power(n, nextPower) - len(arr))
    return np.concatenate((arr, np.zeros(deficit,dtype=arr.dtype)))
