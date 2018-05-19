def int_to_bin(num, num_digits=256):
    return format(num, '#0{}b'.format(num_digits+2))

