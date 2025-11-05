#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import traceback

print("🔍 DEBUG MINING RHODIUM")
print("=" * 50)

# Carica blockchain e wallet
blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"📦 Blocchi attuali: {len(blockchain.chain)}")
print(f"📊 Transazioni pendenti: {len(blockchain.pending_transactions)}")
print(f"👛 Indirizzo miner: {wallet.get_address()}")

# Prova a minare un blocco
print("\n⛏️  Provando a minare blocco...")
try:
    block = blockchain.mine_block(wallet.get_address())
    if block:
        print(f"✅ SUCCESSO! Blocco #{block.index} minato!")
        print(f"   Hash: {block.hash}")
        print(f"   Transazioni: {len(block.transactions)}")
    else:
        print("❌ FALLITO: mine_block() ha restituito None")
        
except Exception as e:
    print(f"❌ ECCEZIONE durante mining:")
    print(f"   Errore: {e}")
    print("   Traceback:")
    traceback.print_exc()

# Verifica la blockchain dopo il tentativo
print(f"\n📦 Blocchi dopo tentativo: {len(blockchain.chain)}")
