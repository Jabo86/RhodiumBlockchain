#!/usr/bin/env python3
from rhodium_core_realistic import RhodiumBlockchain
import time

print("📊 BENCHMARK DIFFICULTY")
print("=" * 50)

blockchain = RhodiumBlockchain()
current_difficulty = blockchain.get_difficulty_from_bits(blockchain.current_bits)

print(f"🎯 Difficulty attuale: {current_difficulty:,.0f}")
print()

# Calcola tempi stimati
print("⏰ TEMPI STIMATI MINING:")
print("-" * 40)

hash_rates = [
    ("CPU base", 1000),           # 1 kH/s
    ("CPU potente", 10000),       # 10 kH/s  
    ("GPU gaming", 10000000),     # 10 MH/s
    ("ASIC Bitcoin", 100000000000), # 100 TH/s
]

for device, hash_rate in hash_rates:
    probability = 1 / current_difficulty
    expected_hashes = 1 / probability
    time_seconds = expected_hashes / hash_rate
    time_minutes = time_seconds / 60
    time_hours = time_minutes / 60
    time_days = time_hours / 24
    
    if time_seconds < 60:
        time_str = f"{time_seconds:.1f}s"
    elif time_minutes < 60:
        time_str = f"{time_minutes:.1f}m"
    elif time_hours < 24:
        time_str = f"{time_hours:.1f}h"
    else:
        time_str = f"{time_days:.1f} giorni"
    
    print(f"   {device:<15} {hash_rate:>12,} H/s → {time_str}")

print(f"\n💡 Nota: Difficulty reale Bitcoin: ~80,000,000,000,000")
print(f"   La nostra difficulty è {current_difficulty/80000000000000*100:.6f}% di Bitcoin")
