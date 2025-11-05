from rhodium_core_hard import RhodiumBlockchain
import time

print("⛏️  TEST MINING HARD")
print("=" * 50)

blockchain = RhodiumBlockchain()
print(f"✅ Blockchain caricata: {len(blockchain.chain)} blocchi")
print(f"🎯 Difficulty: {blockchain.current_difficulty}")

# Prova a minare un blocco
print(f"\n--- Mining blocco {len(blockchain.chain)} ---")
start_time = time.time()

try:
    block = blockchain.mine_block("test_miner")
    
    if block:
        mining_time = time.time() - start_time
        print(f"✅ SUCCESSO! Blocco minato in {mining_time:.2f}s")
        print(f"   Hash: {block.hash[:20]}...")
        print(f"   Nonce: {block.nonce}")
    else:
        print("❌ Fallito: mine_block() ha restituito None")
        
except KeyboardInterrupt:
    print("\n⏹️  Mining interrotto dall'utente")
except Exception as e:
    print(f"❌ Errore: {e}")

print(f"\n📦 Altezza finale: {len(blockchain.chain)} blocchi")
