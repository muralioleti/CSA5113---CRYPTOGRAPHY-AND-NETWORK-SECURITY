def generate_cipher_alphabet(keyword):
    keyword = keyword.upper()
    seen = set()
    cipher_alphabet = []

    # Add letters from the keyword
    for char in keyword:
        if char not in seen and char.isalpha():
            cipher_alphabet.append(char)
            seen.add(char)

    # Add remaining letters of alphabet
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char not in seen:
            cipher_alphabet.append(char)
    
    return cipher_alphabet

def encrypt(plaintext, cipher_alphabet):
    plaintext = plaintext.upper()
    encrypted = []
    for char in plaintext:
        if char.isalpha():
            encrypted.append(cipher_alphabet[ord(char) - ord('A')])
        else:
            encrypted.append(char)  # Preserve spaces and punctuation
    return ''.join(encrypted)

def decrypt(ciphertext, cipher_alphabet):
    reverse_map = {char: chr(i + ord('A')) for i, char in enumerate(cipher_alphabet)}
    ciphertext = ciphertext.upper()
    decrypted = []
    for char in ciphertext:
        if char.isalpha():
            decrypted.append(reverse_map[char])
        else:
            decrypted.append(char)
    return ''.join(decrypted)

# --- Example Usage ---
keyword = "CIPHER"
cipher_alpha = generate_cipher_alphabet(keyword)

message = "HELLO WORLD"
encrypted_msg = encrypt(message, cipher_alpha)
decrypted_msg = decrypt(encrypted_msg, cipher_alpha)

print("Keyword        :", keyword)
print("Cipher Alphabet:", ''.join(cipher_alpha))
print("Plaintext      :", message)
print("Encrypted      :", encrypted_msg)
print("Decrypted      :", decrypted_msg)
