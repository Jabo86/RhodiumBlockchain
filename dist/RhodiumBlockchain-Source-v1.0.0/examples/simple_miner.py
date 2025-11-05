#!/usr/bin/env python3
"""
Esempio di miner semplice per Rhodium Blockchain
"""
from rhodium_core_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

def simple_miner():
    print("⛏️  Simple Miner Avviato")
    
    wallet = RhodiumWallet()
    blockchain = RhodiumBlockchain()
    
    print(f"👛 Indirizzo: {wallet.get_address()}")
    print(f"📦 Altezza blockchain: {len(blockchain.chain)}")
    
    while True:
        print(f"\n🎯 Minando blocco {len(blockchain.chain)}...")
        start_time = time.time()
        
        block = blockchain.mine_block(wallet.get_address())
        
        if block:
            mining_time = time.time() - start_time
            print(f"✅ Blocco minato in {mining_time:.2f}s")
            print(f"💰 Ricompensa: {blockchain.get_current_reward()} RHO")
        else:
            print("❌ Mining fallito")
        
        time.sleep(10)

if __name__ == "__main__":
    simple_miner()
