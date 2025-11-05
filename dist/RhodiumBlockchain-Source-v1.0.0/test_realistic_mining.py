#!/usr/bin/env python3
from rhodium_core_realistic import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

print("⛏️  TEST MINING REALISTICO")
print("=" * 50)
print("Parametri reali Bitcoin:")
print(" - Difficulty adjustment: ogni 2016 blocchi")
print(" - Tempo blocco: 10 minuti")
print(" - Halving: ogni 210,000 blocchi")
print()

blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"Altezza iniziale: {len(blockchain.chain)} blocchi")

# Mina solo 2 blocchi per test (sarà lento!)
for i in range(2):
    print(f"\n--- Mining blocco {len(blockchain.chain)} ---")
    start_time = time.time()
    
    block = blockchain.mine_block(wallet.get_address())
    
    if block:
        mining_time = time.time() - start_time
        print(f"✅ Tempo mining: {mining_time:.2f} secondi")
        
        halving_info = blockchain.get_next_halving_info()
        current_difficulty = blockchain.get_difficulty_from_bits(blockchain.current_bits)
        
        print(f"💰 Reward successivo: {halving_info['current_reward']} RHO")
        print(f"🎯 Difficulty: {current_difficulty:,.0f}")
    
    time.sleep(1)

print(f"\n🎉 TEST COMPLETATO!")
print(f"Altezza finale: {len(blockchain.chain)} blocchi")
