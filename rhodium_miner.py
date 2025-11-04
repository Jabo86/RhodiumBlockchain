#!/usr/bin/env python3
import time
import sys
from rhodium_core import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet

def main():
    print("🚀 RHODIUM MINER - Avvio mining...")
    
    blockchain = RhodiumBlockchain()
    wallet = RhodiumWallet()
    miner_address = wallet.get_address()
    
    print(f"⛏️  Miner: {miner_address}")
    print(f"💰 Balance attuale: {blockchain.get_balance(miner_address):,.6f} RHO")
    print(f"📦 Altezza blockchain: {len(blockchain.chain)}")
    print("---")
    
    try:
        block_count = 0
        while True:
            print(f"🔄 Tentativo mining blocco #{len(blockchain.chain)}...")
            
            block = blockchain.mine_block(miner_address)
            if block:
                block_count += 1
                current_balance = blockchain.get_balance(miner_address)
                print(f"✅ Blocco #{block.index} minato!")
                print(f"💰 Balance aggiornato: {current_balance:,.6f} RHO")
                print(f"🎯 Totale blocchi minati: {block_count}")
                print("---")
            
            # Aspetta prima del prossimo tentativo
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n⏹️  Mining fermato dall'utente")
        print(f"📊 Riepilogo:")
        print(f"   Blocchi minati: {block_count}")
        print(f"   Balance finale: {blockchain.get_balance(miner_address):,.6f} RHO")
        print("Grazie per aver minato Rhodium! 🎉")

if __name__ == "__main__":
    main()
