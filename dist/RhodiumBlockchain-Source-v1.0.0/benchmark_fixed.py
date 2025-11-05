#!/usr/bin/env python3
from rhodium_core_fixed import RhodiumBlockchain

print("📊 BENCHMARK DIFFICULTY CORRETTA")
print("=" * 50)

blockchain = RhodiumBlockchain()

print(f"🎯 Difficulty attuale: {blockchain.current_difficulty}")
print()

# Calcola tempi stimati
print("⏰ TEMPI STIMATI MINING:")
print("-" * 40)

# Probabilità di trovare hash valido
probability = 1 / (16 ** blockchain.current_difficulty)  # Hex: 1/16^difficulty

hash_rates = [
    ("CPU base", 1000),           # 1 kH/s
    ("CPU potente", 10000),       # 10 kH/s  
    ("GPU gaming", 10000000),     # 10 MH/s
    ("ASIC Bitcoin", 100000000000), # 100 TH/s
]

for device, hash_rate in hash_rates:
    expected_hashes = 1 / probability
    time_seconds = expected_hashes / hash_rate
    
    if time_seconds < 60:
        time_str = f"{time_seconds:.1f}s"
    elif time_seconds < 3600:
        time_str = f"{time_seconds/60:.1f}m"
    elif time_seconds < 86400:
        time_str = f"{time_seconds/3600:.1f}h"
    else:
        time_str = f"{time_seconds/86400:.1f} giorni"
    
    print(f"   {device:<15} {hash_rate:>12,} H/s → {time_str}")

print(f"\n📈 DIFFICULTY PROGRESSIONE:")
for diff in range(1, 8):
    probability = 1 / (16 ** diff)
    hashes_needed = 1 / probability
    print(f"   Difficulty {diff}: {hashes_needed:,.0f} hash necessari")

print(f"\n💡 Bitcoin reale: Difficulty ~80 trilioni, ~10^22 hash per blocco")
