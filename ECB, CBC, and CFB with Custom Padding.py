from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

BLOCK_SIZE = 8  # 3DES block size = 8 bytes

# Custom padding: 0x80 followed by 0x00
def custom_pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    padding = b'\x80' + b'\x00' * (pad_len - 1)
    return data + padding

def custom_unpad(data: bytes) -> bytes:
    # Remove trailing zeros, then the final 0x80
    data = data.rstrip(b'\x00')
    if data[-1:] == b'\x80':
        return data[:-1]
    raise ValueError("Invalid padding")

# Encrypt with ECB mode
def encrypt_ecb(key: bytes, plaintext: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded = custom_pad(plaintext)
    return cipher.encrypt(padded)

# Encrypt with CBC mode
def encrypt_cbc(key: bytes, plaintext: bytes, iv: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded = custom_pad(plaintext)
    return cipher.encrypt(padded)

# Encrypt with CFB mode (segment size = block size)
def encrypt_cfb(key: bytes, plaintext: bytes, iv: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_CFB, iv, segment_size=64)
    return cipher.encrypt(plaintext)

# Decryption functions (using custom unpadding)
def decrypt_ecb(key: bytes, ciphertext: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_ECB)
    return custom_unpad(cipher.decrypt(ciphertext))

def decrypt_cbc(key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    return custom_unpad(cipher.decrypt(ciphertext))

def decrypt_cfb(key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
    cipher = DES3.new(key, DES3.MODE_CFB, iv, segment_size=64)
    return cipher.decrypt(ciphertext)

# Demo
if __name__ == "__main__":
    key = DES3.adjust_key_parity(get_random_bytes(24))  # 24-byte key
    iv = get_random_bytes(8)
    plaintext = b"HelloWorld123456"  # 16 bytes = 2 blocks, but we'll still pad it!

    print("Original plaintext:", plaintext)

    # ECB
    ciphertext_ecb = encrypt_ecb(key, plaintext)
    decrypted_ecb = decrypt_ecb(key, ciphertext_ecb)
    print("\n[ECB] Encrypted (Base64):", base64.b64encode(ciphertext_ecb).decode())
    print("[ECB] Decrypted:", decrypted_ecb)

    # CBC
    ciphertext_cbc = encrypt_cbc(key, plaintext, iv)
    decrypted_cbc = decrypt_cbc(key, ciphertext_cbc, iv)
    print("\n[CBC] Encrypted (Base64):", base64.b64encode(ciphertext_cbc).decode())
    print("[CBC] Decrypted:", decrypted_cbc)

    # CFB
    ciphertext_cfb = encrypt_cfb(key, plaintext, iv)
    decrypted_cfb = decrypt_cfb(key, ciphertext_cfb, iv)
    print("\n[CFB] Encrypted (Base64):", base64.b64encode(ciphertext_cfb).decode())
    print("[CFB] Decrypted:", decrypted_cfb)
