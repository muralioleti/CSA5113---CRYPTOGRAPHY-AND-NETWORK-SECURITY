import random

def random_nonzero_64bit():
    while True:
        val = random.getrandbits(64)
        if val != 0:
            return val

def simulate_diffusion_until_all_capacity_lanes_nonzero():
    # Initial 25 lanes (each 64 bits)
    lanes = [random_nonzero_64bit() for _ in range(16)] + [0] * 9  # 16 non-zero + 9 zero lanes
    round_count = 0
    capacity_indices = list(range(16, 25))  # Last 9 lanes
    
    while any(lanes[i] == 0 for i in capacity_indices):
        round_count += 1

        # For simulation: XOR each lane with two randomly selected others
        new_lanes = lanes.copy()
        for i in range(25):
            a, b = random.sample(range(25), 2)
            new_lanes[i] ^= (lanes[a] ^ lanes[b])
        
        lanes = new_lanes

    return round_count

# Run multiple trials for average
trials = 100
results = [simulate_diffusion_until_all_capacity_lanes_nonzero() for _ in range(trials)]
average_rounds = sum(results) / trials

print(f"Simulated {trials} trials.")
print(f"Average rounds to fully diffuse into all capacity lanes: {average_rounds:.2f}")
print(f"Min rounds: {min(results)}, Max rounds: {max(results)}")
