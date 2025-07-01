def create_fixed_matrix():
    matrix = [
        ['M', 'F', 'H', 'I', 'K'],
        ['U', 'N', 'O', 'P', 'Q'],
        ['Z', 'V', 'W', 'X', 'Y'],
        ['E', 'L', 'A', 'R', 'G'],
        ['D', 'S', 'T', 'B', 'C']
    ]
    pos = {}
    for i in range(5):
        for j in range(5):
            letter = matrix[i][j]
            if letter == 'I':
                pos['I'] = pos['J'] = (i, j)
            else:
                pos[letter] = (i, j)
    return matrix, pos

def prepare_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join(filter(str.isalpha, text))  # remove spaces/punctuation
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    if len(pairs[-1]) == 1:
        pairs[-1] = (pairs[-1][0], 'X')
    return pairs

def encrypt_pair(a, b, matrix, pos):
    ra, ca = pos[a]
    rb, cb = pos[b]
    if ra == rb:
        return matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5]
    elif ca == cb:
        return matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb]
    else:
        return matrix[ra][cb] + matrix[rb][ca]

def playfair_encrypt(message):
    matrix, pos = create_fixed_matrix()
    pairs = prepare_text(message)
    encrypted = [encrypt_pair(a, b, matrix, pos) for a, b in pairs]
    return ' '.join(encrypted)

# --- Test the encryption ---
plaintext = "Must see you over Cadogan West. Coming at once."
ciphertext = playfair_encrypt(plaintext)

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext)
