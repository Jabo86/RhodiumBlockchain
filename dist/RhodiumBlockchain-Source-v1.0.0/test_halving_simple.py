#!/usr/bin/env python3
from test_core import TestBlockchain
import time

print("🎯 TEST HALVING (ogni 5 blocchi)")
print("=" * 50)

blockchain = TestBlockchain()
miner_address = "jabo867WwmfUePRCzYDNn6iqbAw"

print(f"Altezza iniziale: {len(blockchain.chain)} blocchi")

# Mina 15 blocchi per vedere multiple halving
for i in range(15):
    print(f"\n--- Blocco {len(blockchain.chain)} ---")
    block = blockchain.mine_block(miner_address)
    
    halving_info = blockchain.get_next_halving_info()
    print(f"Prossimo halving tra: {halving_info['blocks_remaining']} blocchi")
    
    time.sleep(0.5)  # Piccola pausa

print(f"\n🎉 TEST COMPLETATO!")
print(f"Altezza finale: {len(blockchain.chain)} blocchi")
print(f"RHO totali minati: {blockchain.total_mined:,.2f}")

# Mostra storia reward
print(f"\n📈 STORIA HALVING:")
for i, block in enumerate(blockchain.chain):
    if i % blockchain.blocks_per_halving == 0:
        reward = blockchain.initial_reward / (2 ** (i // blockchain.blocks_per_halving))
        print(f"Blocco {i}: Reward = {reward} RHO")
