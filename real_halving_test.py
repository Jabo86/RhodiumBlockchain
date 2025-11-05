#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain

print("🎯 HALVING REALE - PARAMETRI BITCOIN")
print("=" * 60)
print("Parametri:")
print(" - Halving ogni: 210,000 blocchi")
print(" - Reward iniziale: 50 RHO") 
print(" - Tempo blocco: 10 minuti")
print(" - Supply massima: 21,000,000 RHO")
print()

blockchain = RhodiumBlockchain()
current_height = len(blockchain.chain)

print("📈 TABELLA HALVING COMPLETA:")
print("-" * 70)
print(f"{'Epoca':<6} {'Blocco':<12} {'Reward':<12} {'RHO Totali':<15} {'Anno*':<10}")
print("-" * 70)

total_mined = 1000000  # Genesis block
block_reward = 50.0
block_height = 0

for epoch in range(0, 7):  # Primi 7 halving
    blocks_in_epoch = 210000
    epoch_mined = blocks_in_epoch * block_reward
    total_mined += epoch_mined
    
    # Stima anno (basato su 10 minuti per blocco)
    years = (block_height * 10) / (60 * 24 * 365)  # 10 minuti per blocco
    
    current_indicator = " ← CURRENT" if current_height >= block_height and current_height < block_height + blocks_in_epoch else ""
    
    print(f"{epoch:<6} {block_height:<12,} {block_reward:<12} {total_mined:<15,.0f} ~{years:.1f}{current_indicator}")
    
    block_height += blocks_in_epoch
    block_reward /= 2
    
    if block_reward < 0.00000001:  # Meno di 1 satoshi
        break

print("-" * 70)
print(f"Supply finale: {min(total_mined, 21000000):,.0f} RHO")
print("* Anni stimati basati su 10 minuti per blocco")

print(f"\n💎 STATO ATTUALE:")
halving_info = blockchain.get_next_halving_info()
print(f" - Altezza: {current_height:,} blocchi")
print(f" - Reward: {halving_info['current_reward']} RHO")
print(f" - Prossimo halving: {halving_info['halving_at_block']:,}")
print(f" - Blocchi rimanenti: {halving_info['blocks_remaining']:,}")

# Calcola quando sarà il prossimo halving
minutes_remaining = halving_info['blocks_remaining'] * 10
days_remaining = minutes_remaining / (60 * 24)
years_remaining = days_remaining / 365

print(f" - Tempo stimato: {days_remaining:,.0f} giorni (~{years_remaining:.1f} anni)")
