import math

def factorial_log2(n):
    return math.log2(math.factorial(n))

def playfair_key_analysis():
    total_keys_log2 = factorial_log2(25)
    approx_total_keys = 2 ** total_keys_log2

    # Estimated effective keys after accounting for equivalences
    # Based on cryptographic studies and known reductions
    effective_keys_log2 = 61
    approx_effective_keys = 2 ** effective_keys_log2

    print(f"Total possible Playfair keys (25!): ≈ 2^{total_keys_log2:.1f}")
    print(f"Approx total keys (raw): {approx_total_keys:.2e}")
    print(f"Effectively unique Playfair keys: ≈ 2^{effective_keys_log2}")
    print(f"Approx effective keys: {approx_effective_keys:.2e}")

playfair_key_analysis()
