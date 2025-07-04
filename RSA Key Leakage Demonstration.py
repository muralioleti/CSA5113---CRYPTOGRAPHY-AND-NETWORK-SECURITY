import math
import random

def gcd(a, b):
    while b: a, b = b, a % b
    return a

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    return x1 % m0

# Step 1: Generate RSA keys (for demo, small primes)
def generate_rsa_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1)*(q - 1)
    e = 17
    d = modinv(e, phi)
    return p, q, n, e, d

# Step 2: Attacker uses leaked d to recover phi and p, q
def recover_keys_from_leaked_d(e, d, n):
    # Try to find φ(n) from e*d ≡ 1 mod φ(n)
    k = 1
    while True:
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            for i in range(2, n):
                if n % i == 0:
                    p = i
                    q = n // i
                    if (p - 1)*(q - 1) == phi:
                        return p, q, phi
        k += 1
        if k > 1000: break
    return None, None, None

# Step 3: Generate new key pair using same n
def new_keys_from_phi(phi):
    e_new = 7
    while gcd(e_new, phi) != 1:
        e_new += 2
    d_new = modinv(e_new, phi)
    return e_new, d_new

# Simulation
p, q, n, e, d = generate_rsa_keys()
print(f"Original RSA Key:")
print(f"  p = {p}, q = {q}, n = {n}")
print(f"  e = {e}, d = {d}")

print("\nBob leaks private key d. Attacker uses (e, d, n) to factor n...")

p_leaked, q_leaked, phi_leaked = recover_keys_from_leaked_d(e, d, n)
print(f"Attacker found p = {p_leaked}, q = {q_leaked}, φ(n) = {phi_leaked}")

e_new, d_new = new_keys_from_phi(phi_leaked)
print(f"\nBob tries to use new key pair (e'={e_new}, d'={d_new}) with SAME n")

print("But attacker also knows φ(n), so they can generate the same keys!")
