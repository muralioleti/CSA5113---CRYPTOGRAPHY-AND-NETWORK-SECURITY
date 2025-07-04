from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64

def encrypt_cbc_3des(plaintext: str, key: bytes, iv: bytes) -> str:
    """
    Encrypts the given plaintext using 3DES in CBC mode.
    :param plaintext: The message to encrypt (string).
    :param key: 24-byte (192-bit) 3DES key.
    :param iv: 8-byte initialization vector.
    :return: Base64-encoded ciphertext.
    """
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), DES3.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(iv + ciphertext).decode('utf-8')  # prepend IV

# Example usage
if __name__ == "__main__":
    plaintext = "Encrypt this message securely using 3DES CBC mode"
    
    # Generate a secure 24-byte key and 8-byte IV
    key = DES3.adjust_key_parity(get_random_bytes(24))  # 3DES needs parity-adjusted key
    iv = get_random_bytes(8)  # Block size for DES is 8 bytes

    encrypted = encrypt_cbc_3des(plaintext, key, iv)
    
    print("Plaintext:", plaintext)
    print("3DES CBC Encrypted (Base64):", encrypted)
