#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain

blockchain = RhodiumBlockchain()
print("🔍 STATO BLOCKCHAIN RHODIUM")
print("=" * 50)
print(f"📦 Altezza blockchain: {len(blockchain.chain)} blocchi")
print(f"🎯 Difficulty: {blockchain.difficulty}")
print(f"💰 RHO totali minati: {blockchain.total_mined:,.2f}")

halving_info = blockchain.get_next_halving_info()
print(f"💎 Reward attuale: {halving_info['current_reward']} RHO")
print(f"⏳ Prossimo halving: blocco {halving_info['halving_at_block']:,}")
print(f"📅 Blocchi rimanenti: {halving_info['blocks_remaining']:,}")

# Calcola tempo stimato
blocks_remaining = halving_info['blocks_remaining']
days_remaining = (blocks_remaining * 10) / (60 * 24)  # 10 minuti per blocco
years_remaining = days_remaining / 365

print(f"⏰ Tempo stimato: {days_remaining:,.0f} giorni (~{years_remaining:.1f} anni)")

print(f"\n📊 Ultimi 5 blocchi:")
print("-" * 60)
for block in blockchain.chain[-5:]:
    reward_tx = None
    for tx in block.transactions:
        if tx.sender == "0":
            reward_tx = tx
            break
    
    print(f"Blocco #{block.index:4} | Hash: {block.hash[:16]}... | Reward: {reward_tx.amount if reward_tx else 'N/A'} RHO")
