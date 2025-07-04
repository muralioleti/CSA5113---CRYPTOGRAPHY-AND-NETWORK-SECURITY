def permute(bits, table):
    return ''.join([bits[i - 1] for i in table])

def left_shift(bits, n):
    return bits[n:] + bits[:n]

# Permutation tables for S-DES
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8  = [6, 3, 7, 4, 8, 5, 10, 9]
IP  = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP  = [4, 1, 2, 3, 2, 3, 4, 1]
P4  = [2, 4, 3, 1]

S0 = [[[1,0],[0,0],[3,0],[2,0]],
      [[3,0],[2,0],[1,0],[0,0]],
      [[0,0],[2,0],[1,0],[3,0]],
      [[3,0],[1,0],[3,0],[2,0]]]

S1 = [[[0,0],[1,0],[2,0],[3,0]],
      [[2,0],[0,0],[1,0],[3,0]],
      [[3,0],[0,0],[1,0],[0,0]],
      [[2,0],[1,0],[0,0],[3,0]]]

def xor(bits1, bits2):
    return ''.join(['0' if b1 == b2 else '1' for b1, b2 in zip(bits1, bits2)])

def sbox_lookup(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    val = sbox[row][col][0]
    return format(val, '02b')

def fk(bits, sk):
    L, R = bits[:4], bits[4:]
    temp = permute(R, EP)
    temp = xor(temp, sk)
    left, right = temp[:4], temp[4:]
    s0_out = sbox_lookup(left, S0)
    s1_out = sbox_lookup(right, S1)
    s_out = permute(s0_out + s1_out, P4)
    return xor(L, s_out) + R

def generate_keys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]
    left = left_shift(left, 1)
    right = left_shift(right, 1)
    k1 = permute(left + right, P8)

    left = left_shift(left, 2)
    right = left_shift(right, 2)
    k2 = permute(left + right, P8)
    return k1, k2

def sdes_encrypt_block(plaintext, key):
    k1, k2 = generate_keys(key)
    bits = permute(plaintext, IP)
    temp = fk(bits, k1)
    temp = temp[4:] + temp[:4]
    temp = fk(temp, k2)
    cipher = permute(temp, IP_INV)
    return cipher

def sdes_decrypt_block(ciphertext, key):
    k1, k2 = generate_keys(key)
    bits = permute(ciphertext, IP)
    temp = fk(bits, k2)
    temp = temp[4:] + temp[:4]
    temp = fk(temp, k1)
    plain = permute(temp, IP_INV)
    return plain

# CBC mode for S-DES
def cbc_encrypt(plaintext_blocks, key, iv):
    ciphertext_blocks = []
    prev = iv
    for block in plaintext_blocks:
        xor_in = xor(block, prev)
        enc = sdes_encrypt_block(xor_in, key)
        ciphertext_blocks.append(enc)
        prev = enc
    return ciphertext_blocks

def cbc_decrypt(ciphertext_blocks, key, iv):
    plaintext_blocks = []
    prev = iv
    for block in ciphertext_blocks:
        dec = sdes_decrypt_block(block, key)
        plain = xor(dec, prev)
        plaintext_blocks.append(plain)
        prev = block
    return plaintext_blocks

# Example test data
if __name__ == "__main__":
    # Inputs
    key = '0111111101'  # 10-bit key
    iv = '10101010'     # 8-bit IV
    plaintext_blocks = ['00000001', '00100011']  # Two blocks of 8 bits

    # Encrypt
    ciphertext_blocks = cbc_encrypt(plaintext_blocks, key, iv)
    print("Encrypted blocks:", ciphertext_blocks)

    # Decrypt
    decrypted_blocks = cbc_decrypt(ciphertext_blocks, key, iv)
    print("Decrypted blocks:", decrypted_blocks)

    # Expected Cipher: ['11110100', '00001011']
    expected = ['11110100', '00001011']
    print("\nExpected Encrypted:", expected)
    print("Match:", ciphertext_blocks == expected)
