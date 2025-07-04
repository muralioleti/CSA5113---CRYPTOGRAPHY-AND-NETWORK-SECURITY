import math

# Step 1: Factor n
def factor_n(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i, n // i
    return None, None

# Step 2: Compute Euler's totient function
def compute_phi(p, q):
    return (p - 1) * (q - 1)

# Step 3: Extended Euclidean Algorithm to find modular inverse
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    if math.gcd(a, m) != 1:
        return None  # No inverse
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0

# Step 4: RSA encryption and decryption
def encrypt(message, e, n):
    return pow(message, e, n)

def decrypt(cipher, d, n):
    return pow(cipher, d, n)

# Main execution
if __name__ == "__main__":
    e = 31
    n = 3599

    # 1. Factor n
    p, q = factor_n(n)
    print(f"p = {p}, q = {q}")

    # 2. Compute φ(n)
    phi = compute_phi(p, q)
    print(f"φ(n) = {phi}")

    # 3. Find d such that (d * e) % phi == 1
    d = modinv(e, phi)
    print(f"Private key d = {d}")

    print(f"\nPublic Key: (e={e}, n={n})")
    print(f"Private Key: (d={d}, n={n})")

    # Test RSA
    message = 1234
    cipher = encrypt(message, e, n)
    print(f"\nEncrypted message: {cipher}")

    decrypted = decrypt(cipher, d, n)
    print(f"Decrypted message: {decrypted}")
