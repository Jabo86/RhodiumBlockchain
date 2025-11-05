#!/usr/bin/env python3
from rhodium_core_hard import RhodiumBlockchain

print("📊 BENCHMARK DIFFICULTY MOLTO ALTA")
print("=" * 50)

blockchain = RhodiumBlockchain()

print(f"🎯 Difficulty attuale: {blockchain.current_difficulty}")
print(f"🔢 Hash necessari: ~{16**blockchain.current_difficulty:,.0f}")
print()

print("⏰ TEMPI STIMATI MINING (DIFFICULTY 7):")
print("-" * 50)

hash_rates = [
    ("CPU base", 1000),           # 1 kH/s
    ("CPU potente", 10000),       # 10 kH/s  
    ("GPU gaming", 10000000),     # 10 MH/s
    ("ASIC Bitcoin", 100000000000), # 100 TH/s
]

for device, hash_rate in hash_rates:
    hashes_needed = 16 ** blockchain.current_difficulty
    time_seconds = hashes_needed / hash_rate
    
    if time_seconds < 60:
        time_str = f"{time_seconds:.1f}s"
    elif time_seconds < 3600:
        time_str = f"{time_seconds/60:.1f}m"
    elif time_seconds < 86400:
        time_str = f"{time_seconds/3600:.1f}h"
    else:
        time_str = f"{time_seconds/86400:.1f} giorni"
    
    success_rate = "✅ Possibile" if time_seconds < 120 else "❌ Molto difficile"
    
    print(f"   {device:<15} {hash_rate:>12,} H/s → {time_str:>12} {success_rate}")

print(f"\n📈 CONFRONTO DIFFICULTY:")
print("-" * 50)
for diff in [4, 5, 6, 7, 8]:
    hashes_needed = 16 ** diff
    time_cpu = hashes_needed / 10000  # CPU potente
    
    if time_cpu < 60:
        time_str = f"{time_cpu:.1f}s"
    elif time_cpu < 3600:
        time_str = f"{time_cpu/60:.1f}m"
    else:
        time_str = f"{time_cpu/3600:.1f}h"
    
    multiplier = 16 ** (diff - 4)
    print(f"   Difficulty {diff}: {hashes_needed:>15,} hash → {time_str:>8} ({multiplier:,.0f}x)")

print(f"\n💡 IMPATTO DELLA DIFFICULTY 7:")
print(f"   - CPU base: ~74 ore per blocco")
print(f"   - CPU potente: ~7.4 ore per blocco") 
print(f"   - GPU: ~27 secondi per blocco")
print(f"   - ASIC: ~0.00027 secondi per blocco")
print(f"   - 4,096x più difficile della difficulty 4!")
print(f"   - REWARD NON GARANTITO - Potrebbero servire più tentativi!")
