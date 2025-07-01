from collections import Counter

ciphertext = """
53‡‡†305))6*;4826)4‡.)4‡);806*;48†8¶60))85;;]8*;:‡*8†83 (88)5*†;46(;88*96*?;8)*‡(;485);5*†2:*‡(;4956*2(5*—4)8¶8* 
;4069285);)6†8)4‡‡;1(‡9;48081;8:8‡1;48†85;4)485†528806*81 (‡9;48;(88;4(‡?34;48)4‡;161;:188;‡?; 
"""

# Remove spaces and newlines for analysis
filtered_text = ''.join(filter(lambda c: c not in [' ', '\n'], ciphertext))

# Step 1: Frequency Analysis
counter = Counter(filtered_text)

print("Character Frequencies (descending):")
for char, freq in counter.most_common():
    print(f"{repr(char)}: {freq}")
