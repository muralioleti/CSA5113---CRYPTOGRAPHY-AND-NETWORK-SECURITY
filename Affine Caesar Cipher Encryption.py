from math import gcd

# Convert character to index (a=0,...,z=25) and back
def char_to_index(c):
    return ord(c.lower()) - ord('a')

def index_to_char(i):
    return chr(i + ord('a'))

# Encryption function
def affine_encrypt(text, a, b):
    if gcd(a, 26) != 1:
        raise ValueError(f"Invalid 'a' value: {a} is not coprime with 26. Choose another.")

    ciphertext = ''
    for char in text:
        if char.isalpha():
            p = char_to_index(char)
            c = (a * p + b) % 26
            cipher_char = index_to_char(c)
            ciphertext += cipher_char.upper() if char.isupper() else cipher_char
        else:
            ciphertext += char  # Keep non-letter characters
    return ciphertext

# Sample usage
plaintext = input("Enter plaintext: ")
a = int(input("Enter key 'a' (must be coprime with 26): "))
b = int(input("Enter key 'b' (any integer between 0 and 25): "))

try:
    encrypted = affine_encrypt(plaintext, a, b)
    print("\nEncrypted Text:")
    print(encrypted)
except ValueError as e:
    print(f"Error: {e}")
