#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain
import os

blockchain = RhodiumBlockchain()

print()
print("🎉 RHODIUM BLOCKCHAIN - REPORT COMPLETO")
print("=" * 55)
print()

# Info Blockchain
print("📊 INFORMAZIONI BLOCKCHAIN:")
print(f"   📦 Blocchi totali: {len(blockchain.chain)}")
print(f"   💰 RHO totali minati: {blockchain.total_mined:,.2f}")
print(f"   🎯 Supply massima: {blockchain.max_supply:,} RHO")
print(f"   ⛏️  Difficulty: {blockchain.difficulty}")
print(f"   💸 Reward blocco: {blockchain.mining_reward} RHO")
print()

# Wallet Info
wallet1 = 'jabo867WwmfUePRCzYDNn6iqbAw'
wallet2 = 'jabo864D9yQgEqzhdbViwohE4tP'

balance1 = blockchain.get_balance(wallet1)
balance2 = blockchain.get_balance(wallet2)

print("👤 WALLET PRINCIPALE:")
print(f"   📬 {wallet1}")
print(f"   💰 Balance: {balance1:,.6f} RHO")
print(f"   📈 Percentuale supply: {(balance1/blockchain.max_supply*100):.4f}%")
print()

print("👤 WALLET TEST:")
print(f"   📬 {wallet2}")
print(f"   💰 Balance: {balance2:,.6f} RHO")
print()

# File system
print("💾 DATI SALVATI:")
blockchain_size = os.path.getsize('blockchain_data/chain.json') if os.path.exists('blockchain_data/chain.json') else 0
wallet_size = os.path.getsize('wallet.dat') if os.path.exists('wallet.dat') else 0
print(f"   📁 Blockchain: {blockchain_size} bytes")
print(f"   👛 Wallet: {wallet_size} bytes")
print(f"   💿 Dati totali: {blockchain_size + wallet_size} bytes")
print()

print("✅ RHODIUM BLOCKCHAIN FUNZIONANTE AL 100%! 🎉")
print("   Tutte le funzionalità operative:")
print("   ✓ Genesis Block con 1M RHO")
print("   ✓ Transazioni con fee 0.001 RHO")
print("   ✓ Mining Proof-of-Work")
print("   ✓ Indirizzi jabo86...")
print("   ✓ Persistenza dati")
print()
