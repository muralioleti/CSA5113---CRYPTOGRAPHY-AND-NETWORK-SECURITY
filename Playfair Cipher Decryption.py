def prepare_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")
    matrix = []
    used = set()

    for char in keyword:
        if char not in used and char.isalpha():
            matrix.append(char)
            used.add(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":  # 'J' is merged with 'I'
        if char not in used:
            matrix.append(char)

    key_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return key_matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None, None

def decrypt_pair(a, b, matrix):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:  # Same row
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:  # Same column
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:  # Rectangle rule
        return matrix[row1][col2] + matrix[row2][col1]

def decrypt_playfair(ciphertext, keyword):
    ciphertext = ciphertext.upper().replace("J", "I").replace(" ", "")
    matrix = prepare_key_matrix(keyword)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i+1]
        plaintext += decrypt_pair(a, b, matrix)

    return plaintext

# --- Example usage ---
cipher_text = """KXJEY UREBE ZWEHE WRYTU HEYFS 
KREHE GOYFI WTTTU OLKSY CAJPO 
BOTEI ZONTX BYBNT GONEY CUZWR 
GDSON SXBOU YWRHE BAAHY USEDQ"""

cipher_text = cipher_text.replace("\n", " ").replace(" ", "")
keyword = "MONARCHY"  # You can change the keyword if needed

decrypted = decrypt_playfair(cipher_text, keyword)
print("Decrypted Message:")
print(decrypted)
