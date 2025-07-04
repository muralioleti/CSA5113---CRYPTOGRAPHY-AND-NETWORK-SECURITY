# DES Decryption in Python

# Permutation and S-box tables (standard)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1]

SBOX =  [
    # S1 to S8 omitted for brevity
]

P = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2,
                  1, 2, 2, 2, 2, 2, 2, 1]

def permute(block, table):
    return ''.join([block[i - 1] for i in table])

def left_shift(bits, count):
    return bits[count:] + bits[:count]

def xor(bits1, bits2):
    return ''.join(['0' if b1 == b2 else '1' for b1, b2 in zip(bits1, bits2)])

# Key generation with shift schedule
def generate_keys(key_64bit):
    key = permute(key_64bit, PC1)
    C, D = key[:28], key[28:]
    keys = []
    for shift in SHIFT_SCHEDULE:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        keys.append(permute(C + D, PC2))
    return keys

# Simplified round function (without S-box logic here)
def feistel(right, subkey):
    expanded = permute(right, E)
    xored = xor(expanded, subkey)
    # Normally here, you'd apply the S-box substitution and P permutation
    return permute(xored[:32], P)

def des_decrypt(ciphertext_64bit, key_64bit):
    keys = generate_keys(key_64bit)
    keys.reverse()  # Reverse for decryption

    block = permute(ciphertext_64bit, IP)
    L, R = block[:32], block[32:]

    for k in keys:
        temp = R
        R = xor(L, feistel(R, k))
        L = temp

    decrypted = permute(R + L, FP)
    return decrypted

# Example usage
if __name__ == "__main__":
    # Example 64-bit inputs (binary strings)
    ciphertext = '1100101100000000110010101010101011001010101010110010101010101010'
    key = '0001001100110100010101110111100110011011101111001101111111110001'

    decrypted_binary = des_decrypt(ciphertext, key)
    print(f"Decrypted binary: {decrypted_binary}")
