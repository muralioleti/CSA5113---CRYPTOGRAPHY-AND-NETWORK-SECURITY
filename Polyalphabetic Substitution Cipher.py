def generate_key(plaintext, keyword):
    keyword = keyword.lower()
    key = ''
    keyword_index = 0

    for char in plaintext:
        if char.isalpha():
            key += keyword[keyword_index % len(keyword)]
            keyword_index += 1
        else:
            key += char  # Preserve spaces/symbols
    return key

def encrypt_vigenere(plaintext, keyword):
    plaintext = plaintext.lower()
    key = generate_key(plaintext, keyword)
    ciphertext = ''

    for p_char, k_char in zip(plaintext, key):
        if p_char.isalpha():
            shift = ord(k_char) - ord('a')
            encrypted_char = chr((ord(p_char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext += encrypted_char
        else:
            ciphertext += p_char  # Keep non-alphabetic characters unchanged
    return ciphertext.upper()

# Input plaintext and keyword
plaintext = input("Enter the plaintext: ")
keyword = input("Enter the keyword: ")

ciphertext = encrypt_vigenere(plaintext, keyword)

print("\nEncrypted Ciphertext:")
print(ciphertext)
