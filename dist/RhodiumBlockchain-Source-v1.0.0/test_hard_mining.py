#!/usr/bin/env python3
from rhodium_core_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

print("⛏️  TEST MINING CON DIFFICULTY ALTA")
print("=" * 50)
print("ATTENZIONE: Il mining sarà più lento e realistico!")
print("Difficulty 6 = 16.7 milioni di hash necessari in media")
print()

blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"Altezza iniziale: {len(blockchain.chain)} blocchi")
print(f"Difficulty iniziale: {blockchain.current_difficulty}")

# Mina solo 2-3 blocchi (sarà lento!)
target_blocks = min(3, 25 - len(blockchain.chain))  # Massimo 3 blocchi

for i in range(target_blocks):
    print(f"\n--- Mining blocco {len(blockchain.chain)} ---")
    start_time = time.time()
    
    block = blockchain.mine_block(wallet.get_address())
    
    if block:
        mining_time = time.time() - start_time
        print(f"✅ Tempo mining: {mining_time:.2f} secondi")
        print(f"🎯 Difficulty successiva: {blockchain.current_difficulty}")
        
        # Stima hash rate
        hashes_calculated = block.nonce
        hash_rate = hashes_calculated / mining_time if mining_time > 0 else 0
        print(f"⚡ Hash rate effettivo: {hash_rate:,.0f} H/s")
    
    time.sleep(1)

print(f"\n🎉 TEST COMPLETATO!")
print(f"Altezza finale: {len(blockchain.chain)} blocchi")
print(f"Difficulty finale: {blockchain.current_difficulty}")
