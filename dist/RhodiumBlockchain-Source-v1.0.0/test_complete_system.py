from rhodium_core_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet

print("🎯 TEST SISTEMA COMPLETO")
print("=" * 50)

# Inizializza
blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"👛 IL TUO INDIRIZZO: {wallet.get_address()}")
print(f"📦 Blockchain: {len(blockchain.chain)} blocchi")

# 1. Sincronizza wallet
print("\\n1. 🔄 Sincronizzazione wallet...")
wallet.sync_with_blockchain(blockchain)
print(f"   💰 Saldo: {wallet.get_balance()} RHO")

# 2. Mostra cronologia
print("\\n2. 📜 Cronologia transazioni...")
history = wallet.get_complete_history(blockchain)
print(f"   📋 Transazioni trovate: {len(history)}")
for tx in history[:5]:  # Prime 5
    print(f"   - {tx['type']}: {tx['amount']} RHO -> {tx['address'][:15]}...")

# 3. Crea un altro wallet per test
print("\\n3. 👛 Creazione wallet di test...")
wallet2 = RhodiumWallet()
print(f"   Indirizzo wallet 2: {wallet2.get_address()}")

# 4. Prova invio transazione
print("\\n4. 💸 Test invio transazione...")
if wallet.get_balance() >= 5:
    success, message = wallet.send_transaction(wallet2.get_address(), 5.0, blockchain)
    print(f"   {message}")
    
    # Mining per confermare
    print("   ⛏️  Mining per confermare transazione...")
    block = blockchain.mine_block(wallet.get_address())
    if block:
        print(f"   ✅ Blocco {block.index} minato!")
    
    # Risincronizza
    wallet.sync_with_blockchain(blockchain)
    wallet2.sync_with_blockchain(blockchain)
    print(f"   💰 Tuo saldo: {wallet.get_balance()} RHO")
    print(f"   💰 Wallet2 saldo: {wallet2.get_balance()} RHO")
else:
    print("   ❌ Saldo insufficiente per test")

print("\\n🎉 TEST COMPLETATO!")
print("\\nOra avvia la GUI: python3 rhodium_gui_fixed.py")
