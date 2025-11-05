#!/usr/bin/env python3
from rhodium_core_fixed import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

print("⛏️  TEST DIFFICULTY CORRETTA")
print("=" * 50)

blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"Altezza iniziale: {len(blockchain.chain)} blocchi")
print(f"Difficulty iniziale: {blockchain.current_difficulty}")

# Mina 5 blocchi per vedere l'adjustment
for i in range(5):
    print(f"\n--- Mining blocco {len(blockchain.chain)} ---")
    start_time = time.time()
    
    block = blockchain.mine_block(wallet.get_address())
    
    if block:
        mining_time = time.time() - start_time
        print(f"✅ Tempo mining: {mining_time:.2f} secondi")
        print(f"🎯 Difficulty successiva: {blockchain.current_difficulty}")
    
    time.sleep(1)

print(f"\n🎉 TEST COMPLETATO!")
print(f"Altezza finale: {len(blockchain.chain)} blocchi")
print(f"Difficulty finale: {blockchain.current_difficulty}")
