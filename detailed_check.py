#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain

blockchain = RhodiumBlockchain()

print("🔍 ANALISI DETTAGLIATA BLOCKCHAIN")
print("=" * 50)

for i, block in enumerate(blockchain.chain):
    print(f"\n📦 BLOCCO #{i}:")
    print(f"   Miner: {block.miner}")
    print(f"   Hash: {block.hash}")
    
    total_sent = 0
    total_received = 0
    
    for tx in block.transactions:
        if tx.sender == 'jabo867WwmfUePRCzYDNn6iqbAw':
            total_sent += tx.amount + tx.fee
            print(f"   📤 INVIO: {tx.amount} RHO a {tx.recipient[:10]}... (fee: {tx.fee} RHO)")
        elif tx.recipient == 'jabo867WwmfUePRCzYDNn6iqbAw':
            total_received += tx.amount
            print(f"   📥 RICEVUTO: {tx.amount} RHO da {tx.sender}")
        elif tx.sender == '0':
            print(f"   ⛏️  REWARD: {tx.amount} RHO a {tx.recipient[:10]}...")
    
    if total_sent > 0:
        print(f"   💸 TOTALE INVIATO: {total_sent} RHO")
    if total_received > 0:
        print(f"   💰 TOTALE RICEVUTO: {total_received} RHO")

# Balance finale
balance = blockchain.get_balance('jabo867WwmfUePRCzYDNn6iqbAw')
print(f"\n🎯 BALANCE FINALE: {balance:,.6f} RHO")
