def preprocess(text):
    return ''.join(filter(str.isalpha, text.lower()))

def encrypt(plaintext, keystream):
    plaintext = preprocess(plaintext)
    ciphertext = ""
    for i, char in enumerate(plaintext):
        p = ord(char) - ord('a')
        k = keystream[i]
        c = (p + k) % 26
        ciphertext += chr(c + ord('a'))
        print(f"{char.upper()}({p}) + {k} = {c} → {chr(c + ord('a')).upper()}")
    return ciphertext

def decrypt(ciphertext, keystream):
    ciphertext = preprocess(ciphertext)
    plaintext = ""
    for i, char in enumerate(ciphertext):
        c = ord(char) - ord('a')
        k = keystream[i]
        p = (c - k + 26) % 26
        plaintext += chr(p + ord('a'))
        print(f"{char.upper()}({c}) - {k} = {p} → {chr(p + ord('a')).upper()}")
    return plaintext

def find_keystream(plaintext, ciphertext):
    plaintext = preprocess(plaintext)
    ciphertext = preprocess(ciphertext)
    keystream = []
    for p_char, c_char in zip(plaintext, ciphertext):
        p = ord(p_char) - ord('a')
        c = ord(c_char) - ord('a')
        k = (c - p + 26) % 26
        keystream.append(k)
        print(f"{c_char.upper()}({c}) - {p_char.upper()}({p}) = {k}")
    return keystream

# Part (a) Encryption
plaintext1 = "send more money"
keystream1 = [9, 0, 1, 7, 23, 15, 21, 14, 11, 11, 2, 8, 9]
print("=== Encryption ===")
ciphertext1 = encrypt(plaintext1, keystream1)
print("\nCiphertext:", ciphertext1)

# Part (b) Key Recovery
new_plaintext = "cash not needed"
ciphertext2 = ciphertext1  # same ciphertext as from part (a)
print("\n=== Key Recovery for new plaintext ===")
recovered_keystream = find_keystream(new_plaintext, ciphertext2)
print("\nRecovered Keystream:", recovered_keystream)
