properties = {
    'diameter': { 'max': 31 },
    'height': { 'max': 31}
}

properties_encoded = {
    'diameter': 5,
    'height': 5
}

def length_encoded_interval(max, min=0, step=1):
    return ceil(log((abs(max-min))/step, 2))

def bin_to_real(bin_string, min=0, step=1):
        base = 1
        num = 0
        for i in bin_string[::-1]:
            num += base*int(i)
            base *= 2
        return (num-min)*step
