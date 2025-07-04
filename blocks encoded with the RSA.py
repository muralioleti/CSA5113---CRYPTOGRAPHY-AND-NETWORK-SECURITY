import math

# Given public key
e = 17
n = 667  # Suppose this is n = p * q, unknown to attacker

# Intercepted block known to be 59 (plaintext), and attacker knows it
m = 59

# Step 1: Compute GCD
g = math.gcd(m, n)
print(f"GCD({m}, {n}) = {g}")

if g != 1 and g != n:
    # Step 2: Break RSA
    p = g
    q = n // p
    phi = (p - 1) * (q - 1)

    # Step 3: Compute private key d
    def modinv(a, m):
        m0, x0, x1 = m, 0, 1
        while a > 1:
            q = a // m
            a, m = m, a % m
            x0, x1 = x1 - q * x0, x0
        return x1 % m0

    d = modinv(e, phi)
    print(f"RSA broken! p = {p}, q = {q}, φ(n) = {phi}, d = {d}")

    # Step 4: Decrypt intercepted ciphertext (demo)
    plaintext = pow(m, 1, n)
    print(f"Recovered plaintext block = {plaintext}")
else:
    print("No useful factor found. RSA remains secure.")
