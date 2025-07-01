def prepare_text(text):
    # Remove non-letter characters, convert to lowercase, and replace 'j' with 'i'
    text = ''.join(filter(str.isalpha, text)).lower().replace('j', 'i')
    
    # Form digraphs (two-letter pairs), inserting 'x' if letters repeat or length is odd
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = ''
        if i + 1 < len(text):
            b = text[i + 1]
            if a == b:
                b = 'x'
                i += 1
            else:
                i += 2
        else:
            b = 'x'
            i += 1
        pairs.append((a, b))
    return pairs

def create_matrix(keyword):
    matrix = []
    seen = set()
    keyword = keyword.lower().replace('j', 'i')
    
    # Add unique letters from keyword
    for char in keyword:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    # Add remaining letters of the alphabet
    for char in 'abcdefghijklmnopqrstuvwxyz':
        if char not in seen and char != 'j':
            seen.add(char)
            matrix.append(char)

    # Convert to 5x5 grid
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None

def encrypt_pair(matrix, a, b):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)
    
    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def playfair_encrypt(plaintext, keyword):
    matrix = create_matrix(keyword)
    pairs = prepare_text(plaintext)
    
    print("\n5x5 Playfair Matrix:")
    for row in matrix:
        print(' '.join(row))

    encrypted = ''
    for a, b in pairs:
        encrypted += encrypt_pair(matrix, a, b)
    return encrypted.upper()

# Input keyword and plaintext
keyword = input("Enter the keyword for Playfair Cipher: ")
plaintext = input("Enter the plaintext to encrypt: ")

ciphertext = playfair_encrypt(plaintext, keyword)

print("\nEncrypted Ciphertext:")
print(ciphertext)
