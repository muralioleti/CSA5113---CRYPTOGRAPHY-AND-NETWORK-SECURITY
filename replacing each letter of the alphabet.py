def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Shift character and wrap around the alphabet using modulo
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
        else:
            result += char  # Non-alphabetic characters remain unchanged
    return result

# Input from the user
plain_text = input("Enter the text to encrypt: ")

print("\nCaesar Cipher Results (Shifts 1 to 25):")
for k in range(1, 26):
    encrypted = caesar_cipher(plain_text, k)
    print(f"Shift {k:2}: {encrypted}")
