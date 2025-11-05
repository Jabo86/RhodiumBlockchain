from rhodium_core_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet

print("🎯 TEST SISTEMA SEMPLICE")
print("=" * 40)

# Inizializza
blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"👛 IL TUO INDIRIZZO: {wallet.get_address()}")
print(f"📦 Blockchain: {len(blockchain.chain)} blocchi")

# Sincronizza wallet
print("\n1. 🔄 Sincronizzazione wallet...")
wallet.sync_with_blockchain(blockchain)
print(f"   💰 Saldo: {wallet.get_balance()} RHO")

# Mostra cronologia
print("\n2. 📜 Cronologia transazioni...")
history = wallet.get_complete_history(blockchain)
print(f"   📋 Transazioni trovate: {len(history)}")
for tx in history[:3]:
    print(f"   - {tx['type']}: {tx['amount']} RHO")

print("\n🎉 SISTEMA PRONTO!")
print("\nAvvia la GUI: python3 rhodium_gui_fixed.py")
