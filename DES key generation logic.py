def permute(block, table):
    """Permute bits according to a given table."""
    return ''.join(block[i - 1] for i in table)

def left_shift(bits, n):
    """Perform left circular shift."""
    return bits[n:] + bits[:n]

# Initial 64-bit key permutation table (PC-1) to get 56-bit key (C and D)
PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Shift schedule for 16 rounds
SHIFT_SCHEDULE = [
    1, 1, 2, 2, 2, 2, 2, 2,
    1, 2, 2, 2, 2, 2, 2, 1
]

# Selection tables for first 24 bits and last 24 bits from C and D respectively
# These are like PC-2 but each picks 24 bits from respective 28-bit halves
# You can define any 24 unique indices in range(1, 29)
PC2_C = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 2, 18, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20]
PC2_D = [13, 2, 8, 18, 26, 1, 10, 9, 14, 17, 5, 6, 24, 15, 20, 22, 11, 3, 23, 21, 27, 12, 4, 19]

def generate_custom_keys(key_64bit):
    """Generate 16 subkeys where each is 48 bits:
       - First 24 from 28-bit C
       - Second 24 from disjoint 28-bit D
    """
    key_56bit = permute(key_64bit, PC1)
    C = key_56bit[:28]
    D = key_56bit[28:]
    subkeys = []

    for i in range(16):
        C = left_shift(C, SHIFT_SCHEDULE[i])
        D = left_shift(D, SHIFT_SCHEDULE[i])
        
        # Generate subkey: 24 bits from each half
        k1 = ''.join(C[j - 1] for j in PC2_C)
        k2 = ''.join(D[j - 1] for j in PC2_D)
        subkeys.append(k1 + k2)

    return subkeys

# Example usage
if __name__ == "__main__":
    key_64bit = '0001001100110100010101110111100110011011101111001101111111110001'  # Sample key
    subkeys = generate_custom_keys(key_64bit)

    print("Generated 16 Subkeys (48 bits each):\n")
    for i, k in enumerate(subkeys, 1):
        print(f"Round {i}: {k}")
