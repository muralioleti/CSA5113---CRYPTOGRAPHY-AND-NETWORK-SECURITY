def mod_exp(base, exp, mod):
    return pow(base, exp, mod)

# Publicly shared values
q = 23      # prime modulus
a = 5       # primitive root modulo q

# Private secrets
alice_secret = 6  # x
bob_secret = 15   # y

# Alice computes A = a^x mod q
alice_public = mod_exp(a, alice_secret, q)

# Bob computes B = a^y mod q
bob_public = mod_exp(a, bob_secret, q)

# Exchange public values
print("Alice sends:", alice_public)
print("Bob sends:", bob_public)

# Shared secret: s = B^x mod q = A^y mod q
alice_shared = mod_exp(bob_public, alice_secret, q)
bob_shared = mod_exp(alice_public, bob_secret, q)

print("\nShared key (Alice):", alice_shared)
print("Shared key (Bob):", bob_shared)
