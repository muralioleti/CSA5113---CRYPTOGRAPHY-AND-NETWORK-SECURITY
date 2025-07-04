from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# AES CBC-MAC: No IV, final cipher block is the MAC
def cbc_mac(key, message):
    cipher = AES.new(key, AES.MODE_CBC, iv=bytes(16))
    padded = pad(message, 16)
    ciphertext = cipher.encrypt(padded)
    mac = ciphertext[-16:]
    return mac

def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# 1-block message X
X = b'This is 1 block!'  # 16 bytes

# Random AES key
key = os.urandom(16)

# Compute MAC of X
T = cbc_mac(key, X)
print(f"MAC of X: {T.hex()}")

# Construct forged message: X || (X ⊕ T)
X2 = xor_bytes(X, T)
forged_message = X + X2

# Compute MAC of forged message
T_forged = cbc_mac(key, forged_message)
print(f"MAC of forged message (X || X⊕T): {T_forged.hex()}")

# Validate forgery
print(f"Forgery successful? {T == T_forged}")
