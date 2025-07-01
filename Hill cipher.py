# Helper functions
def char_to_num(c):
    return ord(c) - ord('a')

def num_to_char(n):
    return chr((n % 26) + ord('a'))

def preprocess(text):
    text = text.lower().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'x'
    return text

def modinv(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_mod_inv_2x2(m):
    a, b = m[0]
    c, d = m[1]
    det = (a * d - b * c) % 26
    inv_det = modinv(det)
    if inv_det is None:
        raise ValueError("Key matrix is not invertible.")
    return [
        [( d * inv_det) % 26, (-b * inv_det) % 26],
        [(-c * inv_det) % 26, ( a * inv_det) % 26]
    ]

def encrypt_pair(pair, key):
    x = (key[0][0] * pair[0] + key[0][1] * pair[1]) % 26
    y = (key[1][0] * pair[0] + key[1][1] * pair[1]) % 26
    return [x, y]

def encrypt(text, key):
    text = preprocess(text)
    ciphertext = ""
    print("\nEncryption Steps:")
    for i in range(0, len(text), 2):
        p1 = char_to_num(text[i])
        p2 = char_to_num(text[i+1])
        res = encrypt_pair([p1, p2], key)
        print(f"{text[i]}{text[i+1]} -> [{p1}, {p2}] -> {res} -> {num_to_char(res[0])}{num_to_char(res[1])}")
        ciphertext += num_to_char(res[0]) + num_to_char(res[1])
    return ciphertext

def decrypt(text, key):
    key_inv = matrix_mod_inv_2x2(key)
    plaintext = ""
    print("\nDecryption Steps:")
    for i in range(0, len(text), 2):
        c1 = char_to_num(text[i])
        c2 = char_to_num(text[i+1])
        p = encrypt_pair([c1, c2], key_inv)
        print(f"{text[i]}{text[i+1]} -> [{c1}, {c2}] -> {p} -> {num_to_char(p[0])}{num_to_char(p[1])}")
        plaintext += num_to_char(p[0]) + num_to_char(p[1])
    return plaintext

# --- Main Code ---
key_matrix = [[9, 4], [5, 7]]
message = "meet me at the usual place at ten rather than eight oclock"

cipher = encrypt(message, key_matrix)
print("\nCiphertext:", cipher)

plain = decrypt(cipher, key_matrix)
print("\nDecrypted Plaintext:", plain)
