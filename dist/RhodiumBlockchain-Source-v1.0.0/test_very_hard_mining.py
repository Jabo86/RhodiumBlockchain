#!/usr/bin/env python3
from rhodium_core_very_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

print("⛏️  TEST MINING MOLTO DIFFICILE")
print("=" * 50)
print("ATTENZIONE: Il mining sarà ESTREMAMENTE difficile!")
print("Difficulty 7 = 268 milioni di hash necessari")
print("REWARD NON GARANTITO - Potrebbe fallire!")
print()

blockchain = RhodiumBlockchain()
wallet = RhodiumWallet()

print(f"Altezza iniziale: {len(blockchain.chain)} blocchi")
print(f"Difficulty iniziale: {blockchain.current_difficulty}")

successful_blocks = 0
failed_attempts = 0
max_attempts = 3

for attempt in range(max_attempts):
    print(f"\n--- Tentativo {attempt + 1}/{max_attempts} ---")
    print("⏳ Avvio mining... (potrebbe richiedere tempo)")
    start_time = time.time()
    
    block = blockchain.mine_block(wallet.get_address())
    
    mining_time = time.time() - start_time
    
    if block:
        successful_blocks += 1
        print(f"✅✅ SUCCESSO! Blocco #{block.index} minato!")
        print(f"💰 Reward ricevuto: {blockchain.get_current_reward()} RHO")
        break  # Esci dopo il primo successo
    else:
        failed_attempts += 1
        print(f"❌ Tentativo {attempt + 1} fallito dopo {mining_time:.1f}s")
        
        if attempt < max_attempts - 1:
            print("🔄 Ritento tra 3 secondi...")
            time.sleep(3)

print(f"\n🎯 RISULTATO FINALE:")
print(f"   Tentativi: {max_attempts}")
print(f"   Successi: {successful_blocks}")
print(f"   Fallimenti: {failed_attempts}")
print(f"   Difficulty finale: {blockchain.current_difficulty}")

if successful_blocks > 0:
    print("🎉 Complimenti! Hai minato un blocco nonostante la difficoltà!")
else:
    print("💡 Prova con più potenza computazionale o diminuisci la difficulty")
