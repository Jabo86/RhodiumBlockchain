#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain

def simulate_halvings():
    print("🎯 SIMULATORE HALVING RHODIUM")
    print("=" * 50)
    print("Parametri esatti Bitcoin:")
    print(f" - Blocchi per halving: 210,000")
    print(f" - Reward iniziale: 50 RHO")
    print(f" - Supply massima: 21,000,000 RHO")
    print()
    
    blockchain = RhodiumBlockchain()
    current_height = len(blockchain.chain)
    
    print("📈 TABELLA HALVING:")
    print("-" * 80)
    print(f"{'Epoca':<6} {'Blocco':<12} {'Reward':<12} {'RHO Totali':<15} {'Anno*':<10}")
    print("-" * 80)
    
    total_mined = 0
    block_reward = 50.0
    block_height = 0
    
    for epoch in range(0, 10):  # Primi 10 halving
        blocks_in_epoch = 210000 if epoch > 0 else 210000  # Genesis incluso
        epoch_mined = blocks_in_epoch * block_reward
        total_mined += epoch_mined
        
        # Stima anno (basato su 10 minuti per blocco)
        years = (block_height * 10) / (60 * 24 * 365)  # 10 minuti per blocco
        
        print(f"{epoch:<6} {block_height:<12,} {block_reward:<12} {total_mined:<15,.0f} ~{years:.1f}")
        
        block_height += blocks_in_epoch
        block_reward /= 2
        
        if block_reward < 0.00000001:  # Meno di 1 satoshi
            break
    
    print("-" * 80)
    print(f"Supply finale: {total_mined:,.0f} RHO")
    print()
    
    # Info attuali
    current_info = blockchain.get_next_halving_info()
    print("💎 STATO ATTUALE:")
    print(f" - Altezza blockchain: {current_height}")
    print(f" - Reward attuale: {current_info['current_reward']} RHO")
    print(f" - Prossimo halving: blocco {current_info['halving_at_block']}")
    print(f" - Blocchi rimanenti: {current_info['blocks_remaining']}")

if __name__ == "__main__":
    simulate_halvings()
