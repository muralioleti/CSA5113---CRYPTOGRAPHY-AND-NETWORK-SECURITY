from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import copy

def corrupt(ciphertext: bytes, block_index: int, byte_offset: int = 0, bit_mask: int = 0b00000001) -> bytes:
    """Introduce a bit error in a specified ciphertext block"""
    corrupted = bytearray(ciphertext)
    pos = block_index * 8 + byte_offset
    corrupted[pos] ^= bit_mask  # Flip a bit
    return bytes(corrupted)

def encrypt_ecb(plaintext: str, key: bytes):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded = pad(plaintext.encode(), DES3.block_size)
    ciphertext = cipher.encrypt(padded)
    return ciphertext

def decrypt_ecb(ciphertext: bytes, key: bytes):
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, DES3.block_size).decode(errors='replace')

def encrypt_cbc(plaintext: str, key: bytes, iv: bytes):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded = pad(plaintext.encode(), DES3.block_size)
    ciphertext = cipher.encrypt(padded)
    return ciphertext

def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, DES3.block_size).decode(errors='replace')

if __name__ == "__main__":
    # Example data
    plaintext = "BLOCK1-BLOCK2-BLOCK3-BLOCK4"
    key = DES3.adjust_key_parity(get_random_bytes(24))
    iv = get_random_bytes(8)

    print("\n--- ECB Mode ---")
    ciphertext_ecb = encrypt_ecb(plaintext, key)
    corrupted_ecb = corrupt(ciphertext_ecb, 1)  # Corrupt block 1
    print("Decrypted ECB (original):", decrypt_ecb(ciphertext_ecb, key))
    print("Decrypted ECB (with error in C1):", decrypt_ecb(corrupted_ecb, key))

    print("\n--- CBC Mode ---")
    ciphertext_cbc = encrypt_cbc(plaintext, key, iv)
    corrupted_cbc = corrupt(ciphertext_cbc, 1)  # Corrupt C1
    print("Decrypted CBC (original):", decrypt_cbc(ciphertext_cbc, key, iv))
    print("Decrypted CBC (with error in C1):", decrypt_cbc(corrupted_cbc, key, iv))
