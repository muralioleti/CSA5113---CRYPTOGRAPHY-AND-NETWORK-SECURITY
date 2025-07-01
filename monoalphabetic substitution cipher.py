import string
import random

def generate_cipher_alphabet():
    letters = list(string.ascii_lowercase)
    shuffled = letters[:]
    random.shuffle(shuffled)
    return dict(zip(letters, shuffled))

def encrypt(plaintext, cipher_map):
    result = ""
    for char in plaintext:
        if char.isalpha():
            is_upper = char.isupper()
            lower_char = char.lower()
            cipher_char = cipher_map[lower_char]
            result += cipher_char.upper() if is_upper else cipher_char
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result

# Generate cipher map
cipher_map = generate_cipher_alphabet()
print("Cipher Alphabet Mapping:")
for k, v in cipher_map.items():
    print(f"{k} -> {v}")

# Input plaintext
plaintext = input("\nEnter the plaintext to encrypt: ")
ciphertext = encrypt(plaintext, cipher_map)

print("\nEncrypted Ciphertext:")
print(ciphertext)
