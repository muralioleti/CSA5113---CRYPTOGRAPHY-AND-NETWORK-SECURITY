# Reuse functions from previous S-DES logic
def permute(bits, table):
    return ''.join([bits[i - 1] for i in table])

def left_shift(bits, n):
    return bits[n:] + bits[:n]

# S-DES Tables
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

# CTR Mode
def ctr_encrypt(plaintext_blocks, key, counter_start):
    ciphertext_blocks = []
    counter = counter_start
    for block in plaintext_blocks:
        counter_bin = format(counter % 256, '08b')
        keystream = sdes_encrypt_block(counter_bin, key)
        cipher_block = xor(block, keystream)
        ciphertext_blocks.append(cipher_block)
        counter += 1
    return ciphertext_blocks

def ctr_decrypt(ciphertext_blocks, key, counter_start):
    return ctr_encrypt(ciphertext_blocks, key, counter_start)  # Same as encryption in CTR

# Run Test Case
if __name__ == "__main__":
    key = '0111111101'  # 10-bit key
    counter_start = 0  # Initial counter
    plaintext_blocks = ['00000001', '00000010', '00000100']  # 3 blocks

    # Encrypt
    ciphertext_blocks = ctr_encrypt(plaintext_blocks, key, counter_start)
    print("Encrypted Blocks:", ciphertext_blocks)

    # Expected: ['00111000', '01001111', '00110010']
    expected = ['00111000', '01001111', '00110010']
    print("Expected Encrypted:", expected)
    print("Match:", ciphertext_blocks == expected)

    # Decrypt
    decrypted_blocks = ctr_decrypt(ciphertext_blocks, key, counter_start)
    print("Decrypted Blocks:", decrypted_blocks)
    print("Match with original:", decrypted_blocks == plaintext_blocks)
