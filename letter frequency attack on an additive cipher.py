from collections import Counter
import string

# English letter frequency (rough %)
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

def decrypt_caesar(ciphertext, key):
    plaintext = ''
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p = (ord(char) - base - key) % 26
            plaintext += chr(p + base)
        else:
            plaintext += char
    return plaintext

def score_plaintext(text):
    text = text.upper()
    letter_counts = Counter(filter(str.isalpha, text))
    total = sum(letter_counts.values())
    if total == 0:
        return 0
    score = 0.0
    for letter in string.ascii_uppercase:
        observed = (letter_counts.get(letter, 0) / total) * 100
        expected = ENGLISH_FREQ.get(letter, 0)
        score += abs(observed - expected)
    return -score  # Lower difference = better match, so use negative

def frequency_attack(ciphertext, top_n=5):
    results = []
    for key in range(26):
        pt = decrypt_caesar(ciphertext, key)
        score = score_plaintext(pt)
        results.append((score, key, pt))
    results.sort(reverse=True)  # Highest score (least difference) first
    return results[:top_n]

# --- User Interface ---
if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")
    top_n = int(input("How many top plaintexts to show? "))

    top_guesses = frequency_attack(ciphertext, top_n)

    print("\nTop", top_n, "Possible Plaintexts (Ranked):\n")
    for rank, (score, key, pt) in enumerate(top_guesses, 1):
        print(f"{rank}. Key = {key:2d} | Score = {score:.2f}")
        print(f"   Plaintext: {pt}\n")
