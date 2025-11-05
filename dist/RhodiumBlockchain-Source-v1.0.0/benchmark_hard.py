#!/usr/bin/env python3
from rhodium_core_hard import RhodiumBlockchain

print("📊 BENCHMARK DIFFICULTY ALTA")
print("=" * 50)

blockchain = RhodiumBlockchain()

print(f"🎯 Difficulty attuale: {blockchain.current_difficulty}")
print()

# Calcola tempi stimati - DIFFICULTY 6 è 256x più difficile di 4!
probability = 1 / (16 ** blockchain.current_difficulty)
hashes_needed = 1 / probability

print(f"🔢 Hash necessari: {hashes_needed:,.0f}")
print()

print("⏰ TEMPI STIMATI MINING (DIFFICULTY 6):")
print("-" * 50)

hash_rates = [
    ("CPU base", 1000),           # 1 kH/s
    ("CPU potente", 10000),       # 10 kH/s  
    ("GPU gaming", 10000000),     # 10 MH/s
    ("ASIC Bitcoin", 100000000000), # 100 TH/s
]

for device, hash_rate in hash_rates:
    time_seconds = hashes_needed / hash_rate
    
    if time_seconds < 60:
        time_str = f"{time_seconds:.1f}s"
    elif time_seconds < 3600:
        time_str = f"{time_seconds/60:.1f}m"
    elif time_seconds < 86400:
        time_str = f"{time_seconds/3600:.1f}h"
    else:
        time_str = f"{time_seconds/86400:.1f} giorni"
    
    print(f"   {device:<15} {hash_rate:>12,} H/s → {time_str}")

print(f"\n📈 CONFRONTO DIFFICULTY:")
difficulties = [4, 5, 6, 7, 8]
print("-" * 40)
for diff in difficulties:
    hashes_needed = 16 ** diff  # Hex: 16^difficulty
    time_cpu = hashes_needed / 10000  # CPU potente
    
    if time_cpu < 60:
        time_str = f"{time_cpu:.1f}s"
    elif time_cpu < 3600:
        time_str = f"{time_cpu/60:.1f}m"
    else:
        time_str = f"{time_cpu/3600:.1f}h"
    
    multiplier = 16 ** (diff - 4)  # Quanto più difficile di difficulty 4
    print(f"   Difficulty {diff}: {hashes_needed:>12,} hash → {time_str} ({multiplier:,.0f}x più difficile)")

print(f"\n💡 IMPATTO DELLA DIFFICULTY 6:")
print(f"   - CPU base: ~18 minuti per blocco")
print(f"   - CPU potente: ~1.8 minuti per blocco") 
print(f"   - GPU: ~1 secondo per blocco")
print(f"   - ASIC: ancora istantaneo, ma più realistico")
print(f"   - 256x più difficile della versione precedente!")
