#!/usr/bin/env python3
import hashlib
import time
import json
import os
from Crypto.PublicKey import ECC
import base58

class Transaction:
    def __init__(self, sender, recipient, amount, fee=0.001, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = float(amount)
        self.fee = float(fee)
        self.timestamp = time.time()
        self.signature = signature
        self.txid = self.calculate_hash()
    
    def calculate_hash(self):
        tx_data = f"{self.sender}{self.recipient}{self.amount}{self.fee}{self.timestamp}"
        return hashlib.sha256(tx_data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'txid': self.txid,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'fee': self.fee,
            'timestamp': self.timestamp,
            'signature': self.signature
        }

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, miner="system", difficulty=6):  # DIFFICULTY AUMENTATA
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.difficulty = difficulty
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        transactions_str = ''.join([tx.txid for tx in self.transactions])
        block_data = f"{self.index}{transactions_str}{self.timestamp}{self.previous_hash}{self.nonce}{self.difficulty}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'nonce': self.nonce,
            'miner': self.miner,
            'difficulty': self.difficulty
        }

class RhodiumBlockchain:
    def __init__(self, data_dir="blockchain_data"):
        self.data_dir = data_dir
        self.chain_file = os.path.join(data_dir, "chain.json")
        self.pending_file = os.path.join(data_dir, "pending.json")
        self.chain = []
        self.pending_transactions = []
        
        # DIFFICULTY MOLTO PIÙ ALTA - REALISTICA
        self.initial_difficulty = 6  # AUMENTATO DA 4 A 6 (256x più difficile!)
        self.target_block_time = 120  # 2 minuti per testing (più realistico)
        self.blocks_per_difficulty_adjustment = 10
        self.blocks_per_halving = 210000
        self.initial_reward = 50.0
        self.max_supply = 21000000
        
        self.total_mined = 0
        self.current_difficulty = self.initial_difficulty
        
        os.makedirs(data_dir, exist_ok=True)
        self.load_chain()
        self.load_pending()
        
        if not self.chain:
            self.create_genesis_block()
        else:
            self.current_difficulty = self.calculate_difficulty()
    
    def create_genesis_block(self):
        try:
            with open("wallet.dat", "r") as f:
                wallet_data = json.load(f)
            genesis_address = wallet_data["address"]
        except:
            genesis_address = "jabo867WwmfUePRCzYDNn6iqbAw"
        
        genesis_tx = Transaction("0", genesis_address, 1000000.0, 0.0)
        genesis_block = Block(0, [genesis_tx], time.time(), "0" * 64, 0, "genesis", self.initial_difficulty)
        
        self.chain.append(genesis_block)
        self.total_mined += 1000000.0
        self.save_chain()
        print("✅ Genesis Block creato!")
    
    def calculate_difficulty(self):
        """CALCOLO DIFFICULTY PIÙ AGGRESSIVO"""
        if len(self.chain) <= 1:
            return self.initial_difficulty
        
        recent_blocks = min(self.blocks_per_difficulty_adjustment, len(self.chain) - 1)
        total_time = 0
        
        for i in range(1, recent_blocks + 1):
            block_time = self.chain[-i].timestamp - self.chain[-(i+1)].timestamp
            total_time += max(0.1, block_time)  # Evita valori troppo bassi
        
        average_time = total_time / recent_blocks
        target_time = self.target_block_time
        
        print(f"📊 Difficulty adjustment:")
        print(f"   Tempo medio: {average_time:.1f}s (target: {target_time}s)")
        print(f"   Ratio: {average_time/target_time:.2f}")
        
        # AGGIUSTAMENTO PIÙ AGGRESSIVO
        if average_time < target_time * 0.3:  # Molto più veloce
            new_difficulty = self.current_difficulty + 2
            print(f"   📈📈 Aumento FORTE difficulty: {self.current_difficulty} → {new_difficulty}")
            return min(new_difficulty, 10)  # Massimo difficulty 10
        elif average_time < target_time * 0.7:  # Più veloce
            new_difficulty = self.current_difficulty + 1
            print(f"   📈 Aumento difficulty: {self.current_difficulty} → {new_difficulty}")
            return new_difficulty
        elif average_time > target_time * 3:  # Molto più lento
            new_difficulty = max(3, self.current_difficulty - 2)  # Minimo 3
            print(f"   📉📉 Diminuzione FORTE difficulty: {self.current_difficulty} → {new_difficulty}")
            return new_difficulty
        elif average_time > target_time * 1.5:  # Più lento
            new_difficulty = max(3, self.current_difficulty - 1)
            print(f"   📉 Diminuzione difficulty: {self.current_difficulty} → {new_difficulty}")
            return new_difficulty
        else:
            return self.current_difficulty
    
    def get_current_reward(self):
        halvings = len(self.chain) // self.blocks_per_halving
        reward = self.initial_reward / (2 ** halvings)
        return max(reward, 0)
    
    def get_next_halving_info(self):
        blocks_until_halving = self.blocks_per_halving - (len(self.chain) % self.blocks_per_halving)
        current_reward = self.get_current_reward()
        next_reward = current_reward / 2 if current_reward > 0 else 0
        
        return {
            'blocks_remaining': blocks_until_halving,
            'current_reward': current_reward,
            'next_reward': next_reward,
            'halving_at_block': (len(self.chain) // self.blocks_per_halving + 1) * self.blocks_per_halving
        }
    
    def save_chain(self):
        chain_data = [block.to_dict() for block in self.chain]
        with open(self.chain_file, 'w') as f:
            json.dump(chain_data, f, indent=4)
    
    def load_chain(self):
        if os.path.exists(self.chain_file):
            try:
                with open(self.chain_file, 'r') as f:
                    chain_data = json.load(f)
                
                self.chain = []
                for block_data in chain_data:
                    transactions = []
                    for tx_data in block_data['transactions']:
                        tx = Transaction(
                            tx_data['sender'],
                            tx_data['recipient'],
                            tx_data['amount'],
                            tx_data.get('fee', 0.001),
                            tx_data.get('signature')
                        )
                        tx.txid = tx_data['txid']
                        transactions.append(tx)
                    
                    block = Block(
                        block_data['index'],
                        transactions,
                        block_data['timestamp'],
                        block_data['previous_hash'],
                        block_data['nonce'],
                        block_data.get('miner', 'unknown'),
                        block_data.get('difficulty', self.initial_difficulty)
                    )
                    block.hash = block_data['hash']
                    self.chain.append(block)
                
                print(f"✅ Blockchain caricata: {len(self.chain)} blocchi")
                
                self.total_mined = 0
                for block in self.chain:
                    for tx in block.transactions:
                        if tx.sender == "0":
                            self.total_mined += tx.amount
                
                halving_info = self.get_next_halving_info()
                print(f"💰 Reward attuale: {halving_info['current_reward']} RHO")
                print(f"🎯 Difficulty: {self.current_difficulty}")
                print(f"⏳ Prossimo halving: {halving_info['blocks_remaining']:,} blocchi")
                
            except Exception as e:
                print(f"❌ Errore caricamento blockchain: {e}")
    
    def save_pending(self):
        pending_data = [tx.to_dict() for tx in self.pending_transactions]
        with open(self.pending_file, 'w') as f:
            json.dump(pending_data, f, indent=4)
    
    def load_pending(self):
        if os.path.exists(self.pending_file):
            try:
                with open(self.pending_file, 'r') as f:
                    pending_data = json.load(f)
                
                self.pending_transactions = []
                for tx_data in pending_data:
                    tx = Transaction(
                        tx_data['sender'],
                        tx_data['recipient'],
                        tx_data['amount'],
                        tx_data.get('fee', 0.001),
                        tx_data.get('signature')
                    )
                    tx.txid = tx_data['txid']
                    self.pending_transactions.append(tx)
                
                print(f"✅ Transazioni pendenti caricate: {len(self.pending_transactions)}")
            except Exception as e:
                print(f"❌ Errore caricamento transazioni pendenti: {e}")
    
    def get_latest_block(self):
        return self.chain[-1] if self.chain else None
    
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        self.save_pending()
        return True
    
    def get_balance(self, address):
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= (tx.amount + tx.fee)
        return balance
    
    def mine_block(self, miner_address):
        """MINING CON DIFFICULTY ALTA"""
        if len(self.chain) > 0 and len(self.chain) % self.blocks_per_difficulty_adjustment == 0:
            self.current_difficulty = self.calculate_difficulty()
        
        current_reward = self.get_current_reward()
        halving_info = self.get_next_halving_info()
        
        print(f"⛏️  Mining blocco {len(self.chain)}")
        print(f"   🎯 Difficulty: {self.current_difficulty}")
        print(f"   💰 Reward: {current_reward} RHO")
        print(f"   ⏳ Halving tra: {halving_info['blocks_remaining']:,} blocchi")
        
        reward_tx = Transaction("0", miner_address, current_reward, 0.0)
        
        if self.pending_transactions:
            block_transactions = [reward_tx] + self.pending_transactions
            print(f"   📦 Includendo {len(self.pending_transactions)} transazioni")
        else:
            block_transactions = [reward_tx]
            print(f"   💰 Mining blocco vuoto")
        
        previous_hash = self.get_latest_block().hash
        
        new_block = Block(len(self.chain), block_transactions, time.time(), previous_hash, 0, miner_address, self.current_difficulty)
        
        # PROOF OF WORK CON DIFFICULTY ALTA
        target = "0" * self.current_difficulty
        start_time = time.time()
        hashes_calculated = 0
        
        print(f"   🎯 Target: {target} ({self.current_difficulty} zeri)")
        print(f"   ⏳ Calcolando hash...", end='', flush=True)
        
        while new_block.hash[:self.current_difficulty] != target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            hashes_calculated += 1
            
            if hashes_calculated % 50000 == 0:  # Progresso più frequente
                print(".", end='', flush=True)
        
        mining_time = time.time() - start_time
        hash_rate = hashes_calculated / mining_time if mining_time > 0 else 0
        
        print()
        print(f"✅ Blocco {new_block.index} minato in {mining_time:.2f} secondi!")
        print(f"   📊 Hash calcolati: {hashes_calculated:,}")
        print(f"   ⚡ Hash rate: {hash_rate:,.0f} H/s")
        print(f"   🔨 Nonce: {new_block.nonce}")
        print(f"   💰 Ricompensa: {current_reward} RHO")
        print(f"   🔗 Hash: {new_block.hash[:32]}...")
        
        old_reward = current_reward
        self.chain.append(new_block)
        self.pending_transactions = []
        self.total_mined += current_reward
        self.save_chain()
        
        new_reward = self.get_current_reward()
        if new_reward < old_reward:
            print(f"🎉 HALVING AVVENUTO! Nuovo reward: {new_reward} RHO")
        
        if os.path.exists(self.pending_file):
            os.remove(self.pending_file)
        
        return new_block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            
            target = "0" * current_block.difficulty
            if current_block.hash[:current_block.difficulty] != target:
                return False
        
        return True

if __name__ == "__main__":
    blockchain = RhodiumBlockchain()
    print(f"📦 Blocchi: {len(blockchain.chain)}")
    
    halving_info = blockchain.get_next_halving_info()
    print(f"💰 Reward: {halving_info['current_reward']} RHO")
    print(f"🎯 Difficulty: {blockchain.current_difficulty}")
    print(f"⏳ Prossimo halving: {halving_info['blocks_remaining']:,} blocchi")
