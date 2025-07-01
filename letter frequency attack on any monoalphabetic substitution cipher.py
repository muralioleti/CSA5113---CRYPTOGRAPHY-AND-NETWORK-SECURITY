from collections import Counter
import string
import itertools

# Standard English letter frequency (ordered)
ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def preprocess(text):
    return ''.join(filter(str.isalpha, text.upper()))

def frequency_analysis(ciphertext):
    filtered = preprocess(ciphertext)
    freq = Counter(filtered)
    sorted_letters = [item[0] for item in freq.most_common()]
    return sorted_letters

def score_plaintext(plaintext):
    # Rough scoring: frequency closeness
    freqs = Counter(preprocess(plaintext))
    total = sum(freqs.values())
    if total == 0:
        return float('-inf')
    score = 0
    for letter, ideal in zip(ENGLISH_FREQ_ORDER, ENGLISH_FREQ_ORDER):
        observed = freqs.get(letter, 0) / total
        expected = ENGLISH_FREQ_ORDER.index(ideal) / 26
        score -= abs(observed - expected)
    return score

def substitute(ciphertext, mapping):
    table = str.maketrans(mapping)
    return ciphertext.translate(table)

def generate_candidate_mappings(cipher_freq_order, top_n=5):
    # Take the top `top_n` letters and permute their mappings to explore variations
    best_mappings = []
    for perm in itertools.permutations(ENGLISH_FREQ_ORDER[:top_n]):
        partial_map = dict(zip(cipher_freq_order[:top_n], perm))
        # Fill rest using 1-to-1 guessing
        unused = [ch for ch in ENGLISH_FREQ_ORDER if ch not in perm]
        remaining = [c for c in cipher_freq_order if c not in partial_map]
        full_map = partial_map.copy()
        for c, r in zip(remaining, unused):
            full_map[c] = r
        # Fill unmapped letters with themselves
        for c in string.ascii_uppercase:
            if c not in full_map:
                full_map[c] = c
        best_mappings.append(''.join([full_map.get(c, c) for c in string.ascii_uppercase]))
    return best_mappings

def frequency_attack(ciphertext, top_output=10):
    cipher_freq_order = frequency_analysis(ciphertext)
    mappings = generate_candidate_mappings(cipher_freq_order, top_n=5)

    results = []
    for keymap in mappings:
        # Build mapping dictionary
        mapping_dict = dict(zip(string.ascii_uppercase, keymap))
        decrypted = substitute(ciphertext.upper(), mapping_dict)
        score = score_plaintext(decrypted)
        results.append((score, keymap, decrypted))

    # Sort results by score descending
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:top_output]

# --- Main UI ---
if __name__ == "__main__":
    ciphertext = input("Enter the ciphertext: ")
    top_n = int(input("How many top plaintexts to show? "))

    candidates = frequency_attack(ciphertext, top_n)

    print(f"\nTop {top_n} Possible Plaintexts:\n")
    for rank, (score, keymap, plaintext) in enumerate(candidates, 1):
        print(f"{rank}. Score: {score:.4f}")
        print(f"   Mapping: {keymap}")
        print(f"   Plaintext: {plaintext}\n")
