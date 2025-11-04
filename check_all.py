#!/usr/bin/env python3
from rhodium_core import RhodiumBlockchain

blockchain = RhodiumBlockchain()

print("💰 RHODIUM BALANCE CHECKER")
print("=" * 40)

# Wallet 1 (Tuo)
balance1 = blockchain.get_balance('jabo867WwmfUePRCzYDNn6iqbAw')
print(f"👤 TUO WALLET:")
print(f"   📬 jabo867WwmfUePRCzYDNn6iqbAw")
print(f"   💰 Balance: {balance1:,.6f} RHO")

print()

# Wallet 2 (Test)
balance2 = blockchain.get_balance('jabo864D9yQgEqzhdbViwohE4tP')
print(f"👤 WALLET TEST:")
print(f"   📬 jabo864D9yQgEqzhdbViwohE4tP")
print(f"   💰 Balance: {balance2:,.6f} RHO")

print()

# Calcoli
print("📊 ANALISI TRANSAZIONI:")
print(f"   📤 Tu hai inviato: 100 RHO")
print(f"   ⛽ Fee pagati: 0.001 RHO") 
print(f"   ⛏️  Reward mining: 50 RHO")
print(f"   📈 Saldo atteso: 1,000,000 - 100 - 0.001 + 50 = {1000000 - 100 - 0.001 + 50:,.3f} RHO")
print(f"   📉 Saldo effettivo: {balance1:,.3f} RHO")

print(f"\n✅ DIFFERENZA: {balance1 - (1000000 - 100 - 0.001 + 50):,.6f} RHO")
