import threading
import time
import hashlib
from typing import List, Dict
from rhodium_core_hard import RhodiumBlockchain, Block
from rhodium_wallet import RhodiumWallet

class MiningPool:
    def __init__(self):
        self.miners: List[Dict] = []
        self.blockchain = RhodiumBlockchain()
        self.current_block = None
        self.mining = False
        self.reward_distribution = {}
        
    def add_miner(self, miner_address: str, hashrate: int = 1000):
        """Aggiungi un minatore al pool"""
        miner = {
            'address': miner_address,
            'hashrate': hashrate,
            'shares': 0,
            'last_share': time.time()
        }
        self.miners.append(miner)
        print(f"👷 Minatore aggiunto: {miner_address} ({hashrate} H/s)")
        
    def start_mining_pool(self):
        """Avvia il pool di mining"""
        self.mining = True
        print("🏊 Pool di mining avviato")
        
        # Thread principale di mining
        mining_thread = threading.Thread(target=self.pool_mining_worker)
        mining_thread.daemon = True
        mining_thread.start()
        
    def pool_mining_worker(self):
        """Worker principale del pool"""
        while self.mining:
            if not self.current_block:
                self.prepare_new_block()
            
            # Simula mining condiviso
            if self.simulate_pool_mining():
                self.distribute_rewards()
                self.current_block = None
                
            time.sleep(5)
    
    def prepare_new_block(self):
        """Prepara un nuovo blocco per il mining"""
        miner_address = "pool_reward"  # Indirizzo del pool
        reward = self.blockchain.get_current_reward()
        
        # Crea transazione di reward per il pool
        from rhodium_core_hard import Transaction
        reward_tx = Transaction("0", miner_address, reward)
        
        # Prepara transazioni
        block_transactions = [reward_tx]
        if self.blockchain.pending_transactions:
            block_transactions.extend(self.blockchain.pending_transactions[:10])
        
        # Crea blocco
        previous_hash = self.blockchain.chain[-1].hash if self.blockchain.chain else "0"
        self.current_block = Block(
            index=len(self.blockchain.chain),
            transactions=block_transactions,
            timestamp=time.time(),
            previous_hash=previous_hash,
            difficulty=self.blockchain.difficulty
        )
        
        print(f"📦 Nuovo blocco preparato per il pool (Difficulty: {self.blockchain.difficulty})")
    
    def simulate_pool_mining(self):
        """Simula il mining condiviso del pool"""
        print(f"⛏️  Pool mining con {len(self.miners)} minatori...")
        
        # Simula shares dai minatori
        for miner in self.miners:
            shares = miner['hashrate'] // 100  # Shares basate sull'hashrate
            miner['shares'] += shares
            miner['last_share'] = time.time()
        
        # Simula finding del blocco (probabilità basata sulla difficoltà)
        total_hashrate = sum(miner['hashrate'] for miner in self.miners)
        probability = total_hashrate / (16 ** self.blockchain.difficulty)
        
        import random
        if random.random() < probability:
            print("🎉 Blocco minato dal pool!")
            return True
        
        return False
    
    def distribute_rewards(self):
        """Distribuisci le ricompense ai minatori"""
        if not self.miners:
            return
            
        total_shares = sum(miner['shares'] for miner in self.miners)
        block_reward = self.blockchain.get_current_reward()
        
        print(f"💰 Distribuzione ricompensa: {block_reward} RHO")
        
        for miner in self.miners:
            if miner['shares'] > 0:
                share_ratio = miner['shares'] / total_shares
                reward = block_reward * share_ratio
                
                print(f"   👷 {miner['address'][:12]}...: {reward:.6f} RHO ({miner['shares']} shares)")
                
                # Reset shares
                miner['shares'] = 0
    
    def get_pool_stats(self):
        """Restituisce statistiche del pool"""
        total_hashrate = sum(miner['hashrate'] for miner in self.miners)
        return {
            'miners_count': len(self.miners),
            'total_hashrate': total_hashrate,
            'current_difficulty': self.blockchain.difficulty,
            'block_reward': self.blockchain.get_current_reward()
        }

# Esempio di utilizzo
if __name__ == "__main__":
    pool = MiningPool()
    
    # Aggiungi alcuni minatori di test
    pool.add_miner("jabo861234567890", 50000)
    pool.add_miner("jabo869876543210", 75000)
    pool.add_miner("jabo864455667788", 30000)
    
    # Avvia il pool
    pool.start_mining_pool()
    
    # Mostra statistiche
    stats = pool.get_pool_stats()
    print(f"📊 Statistiche Pool:")
    print(f"   Minatori: {stats['miners_count']}")
    print(f"   Hashrate totale: {stats['total_hashrate']:,} H/s")
    print(f"   Difficulty: {stats['current_difficulty']}")
    print(f"   Reward per blocco: {stats['block_reward']} RHO")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        pool.mining = False
