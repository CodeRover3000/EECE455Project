from bitarray import bitarray

# takes a binary number or a hexadecimal number as inputs and converts them to a binary number string
def check_and_convert(input_str):
    if input_str.startswith("0x"):
        try:
            binary_value = bin(int(input_str, 16))[2:]
            return binary_value
        except ValueError:
            return "Invalid hexadecimal input"
    elif all(char in '01' for char in input_str):
        return input_str
    else:
        return "Invalid input, not binary or hexadecimal"
    
def binary_with_index(index):
    if index < 0:
        raise ValueError("Index should be a non-negative integer.")

    return '0' * index + '1' + '0' * (index - 1)
    
def indices_to_binary_string(indices):
    if not indices:
        return '0'

    max_index = max(indices)
    binary_string = ['0'] * (max_index + 1)

    for i in indices:
        binary_string[i] = '1'

    return ''.join(binary_string[::-1])

#used for division
def polynomial_subtraction2(poly_a, poly_b, shift=0):
    int_a = int(poly_a, 2)
    int_b = int(poly_b, 2)

    shifted_b = int_b << shift

    result = bin(int_a ^ shifted_b)[2:]

    return {'result': result, 'remainder': result.lstrip('0')}

def leading_term(poly):
    for i in range(len(poly)):
        if poly[i] == '1':
            return len(poly) - i - 1
    return -1

# converts binary to hex
def binary_to_hex(binary_str):
    try:
        hex_value = hex(int(binary_str, 2))
        return hex_value
    except ValueError:
        return "Invalid binary input"
    
# adjust length to fit a specific value
def adjust_binary_length(x, binary_string):
    if len(binary_string) > x-1:
        return binary_string[:x-1]
    elif len(binary_string) < x-1:
        return '0' * (x - len(binary_string)) + binary_string
    else:
        return binary_string
    
def remove_unnecessary_zeros(binary_string):
    return binary_string.lstrip('0') if binary_string != '0' else binary_string

def one_positions(binary_str):
    returnValue = []
    for i in range(len(binary_str)):
        if binary_str[i] == '1':
            returnValue.append(len(binary_str) - i - 1)
    return returnValue

def polynomial_addition(poly_a, poly_b):
    poly_a = adjust_binary_length(163, poly_a)
    poly_b = adjust_binary_length(163, poly_b)
    a = bitarray(poly_a)
    b = bitarray(poly_b)
    result = a ^ b
    return result.to01()

def polynomial_subtraction(poly_a, poly_b):
    poly_a = adjust_binary_length(163, poly_a)
    poly_b = adjust_binary_length(163, poly_b)
    a = bitarray(poly_a)
    b = bitarray(poly_b)
    result = a ^ b
    return remove_unnecessary_zeros(result.to01())

def polynomial_multiplication(poly_a, poly_b):
    poly_a = adjust_binary_length(163, poly_a)
    poly_b = adjust_binary_length(163, poly_b)
    positions = one_positions(poly_b)
    if (len(positions) == 0):
        return '0'
    a = bitarray(poly_a)
    shifted = []
    for x in positions:
        shifted.append(a << x)
    result = shifted[0]
    for index, x in enumerate(shifted):
        if index == 0:
            continue
        result = result ^ x
    return result.to01()

#takes two binary numbers as strings as inputs and returns the division result and remainder
def polynomial_division(poly_a, poly_b):
    poly_a = adjust_binary_length(163, poly_a)
    poly_b = adjust_binary_length(163, poly_b)
    leadA = leading_term(poly_a)
    leadB = leading_term(poly_b)

    if leadB > leadA:
        return {'result': '0', 'remainder': poly_a}

    result = []
    remainder = poly_a

    while leadA >= leadB:  
        mult = leadA - leadB

        subtracted = polynomial_subtraction2(remainder, poly_b, mult)
        remainder = subtracted['remainder']

        result.append(mult)
        leadA = leading_term(remainder)

    return {'result': indices_to_binary_string(result), 'remainder': remainder}


#Same as the division but returns remainder only
def polynomial_reduction(poly_a, poly_b):
    poly_a = adjust_binary_length(163, poly_a)
    poly_b = adjust_binary_length(163, poly_b)
    leadA = leading_term(poly_a)
    leadB = leading_term(poly_b)

    if leadB > leadA:
        return {'result': '0', 'remainder': poly_a}

    result = []
    remainder = poly_a

    while leadA >= leadB:  
        mult = leadA - leadB

        subtracted = polynomial_subtraction2(remainder, poly_b, mult)
        remainder = subtracted['remainder']

        result.append(mult)
        leadA = leading_term(remainder)

    return  remainder

"""
Correct Logic But requires modification due to error

def inverse_helper(A, B):
    if B[2] == '1':
        return B[1]
    if B[2] == '0':
        return '-1'
    Q = polynomial_division(A[2], B[2])['result']
    T = ['1', '1', '1']
    for i in range(3):
        T[i] = polynomial_subtraction(A[i], polynomial_multiplication(Q, B[i]))
    A[:] = B[:]
    B[:] = T[:]
    return inverse_helper(A, B)

def polynomial_inverse(poly):
    mod_poly = '100011011'  # binary_with_index(163)
    poly = adjust_binary_length(163, poly)
    mod_poly = adjust_binary_length(163, mod_poly)
    remove_unnecessary_zeros(poly)
    remove_unnecessary_zeros(mod_poly)

    A = ['1', '0', mod_poly]
    B = ['0', '1', poly]

    return inverse_helper(A, B)

def remove_unnecessary_zeros(poly):
    return poly.lstrip('0') or '0'
"""

print(binary_to_hex('1110'))
print(check_and_convert('0xFF'))
print(polynomial_division('1010110111101', '100011011'))
print(remove_unnecessary_zeros(polynomial_multiplication('1010110111101', '100011011')))
print(remove_unnecessary_zeros(polynomial_subtraction('1010110111101', '100011011')))
print(remove_unnecessary_zeros(polynomial_addition('1010110111101', '100011011')))
print(remove_unnecessary_zeros(polynomial_reduction('1010110111101', '100011011')))





