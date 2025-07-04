def letter_to_int(ch):
    return ord(ch.upper()) - ord('A')

def int_to_letter(i):
    return chr(i + ord('A'))

def rsa_encrypt(m, e, n):
    return pow(m, e, n)

def rsa_decrypt(c, d, n):
    return pow(c, d, n)

# Public key
e = 17
n = 3233  # small for demo, typically large in real RSA

# Attacker precomputes encrypted values
lookup = {}
for m in range(26):
    c = rsa_encrypt(m, e, n)
    lookup[c] = m

print("Attacker's Lookup Table:")
for c, m in lookup.items():
    print(f"Cipher: {c} => Plaintext: {int_to_letter(m)}")

# Example: Encrypted message intercepted
ciphertext = [2187, 3000, 1647]  # represents some letters
print("\nIntercepted Ciphertext:", ciphertext)

# Attacker decrypts using lookup table
decrypted = [int_to_letter(lookup[c]) for c in ciphertext]
print("Decrypted Message:", ''.join(decrypted))
