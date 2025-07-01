from math import gcd

# Extended Euclidean Algorithm for finding modular inverse
def modinv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def decrypt_affine(ciphertext, a, b):
    a_inv = modinv(a, 26)
    if a_inv is None:
        raise ValueError(f"No modular inverse for a = {a}")
    
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            C = ord(char.lower()) - ord('a')
            P = (a_inv * (C - b)) % 26
            decrypted_char = chr(P + ord('a'))
            plaintext += decrypted_char.upper() if char.isupper() else decrypted_char
        else:
            plaintext += char
    return plaintext

# Step 1: Solve 15a ≡ 19 mod 26
valid_a_values = [a for a in range(1, 26) if gcd(a, 26) == 1]
possible_keys = []

for a in valid_a_values:
    if (15 * a) % 26 == 19:
        b = (1 - a * 4) % 26  # From equation: (a*4 + b) % 26 = 1
        possible_keys.append((a, b))

# Step 2: Try each key and print possible plaintexts
ciphertext = input("Enter the Affine Ciphertext: ")

print("\nTrying all possible (a, b) pairs based on frequency analysis...")
for a, b in possible_keys:
    decrypted = decrypt_affine(ciphertext, a, b)
    print(f"\na = {a}, b = {b} --> Decrypted:")
    print(decrypted)
