def modinv(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def matrix_inverse_2x2(mat):
    a, b = mat[0]
    c, d = mat[1]
    det = (a * d - b * c) % 26
    det_inv = modinv(det)
    if det_inv is None:
        raise ValueError("Matrix is not invertible.")
    return [
        [( d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, ( a * det_inv) % 26]
    ]

def matrix_mult_2x2(A, B):
    return [
        [(A[0][0]*B[0][0] + A[0][1]*B[1][0]) % 26,
         (A[0][0]*B[0][1] + A[0][1]*B[1][1]) % 26],
        [(A[1][0]*B[0][0] + A[1][1]*B[1][0]) % 26,
         (A[1][0]*B[0][1] + A[1][1]*B[1][1]) % 26]
    ]

def text_to_matrix(text):
    # Convert digraphs into numeric matrix (column-wise)
    return [[ord(text[0]) - ord('a'), ord(text[1]) - ord('a')],
            [ord(text[2]) - ord('a'), ord(text[3]) - ord('a')]]

def recover_key_matrix(plain_digraphs, cipher_digraphs):
    # Convert text digraphs to matrices
    P = [[ord(p[0]) - ord('a'), ord(p[1]) - ord('a')] for p in plain_digraphs]
    C = [[ord(c[0]) - ord('a'), ord(c[1]) - ord('a')] for c in cipher_digraphs]

    # Form plaintext matrix and invert
    P_matrix = [[P[0][0], P[1][0]], [P[0][1], P[1][1]]]
    C_matrix = [[C[0][0], C[1][0]], [C[0][1], C[1][1]]]

    P_inv = matrix_inverse_2x2(P_matrix)
    key_matrix = matrix_mult_2x2(C_matrix, P_inv)

    return key_matrix

# --- Example usage ---
# Known plaintext and ciphertext digraphs
plaintext_digraphs = ["he", "lp"]  # h=7, e=4, l=11, p=15
ciphertext_digraphs = ["ri", "jv"] # r=17, i=8, j=9, v=21

key = recover_key_matrix(plaintext_digraphs, ciphertext_digraphs)

print("Recovered Key Matrix:")
for row in key:
    print(row)
