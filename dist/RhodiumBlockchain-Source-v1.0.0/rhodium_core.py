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
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, miner="system"):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        transactions_str = ''.join([tx.txid for tx in self.transactions])
        block_data = f"{self.index}{transactions_str}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'nonce': self.nonce,
            'miner': self.miner
        }

class RhodiumBlockchain:
    def __init__(self, data_dir="blockchain_data"):
        self.data_dir = data_dir
        self.chain_file = os.path.join(data_dir, "chain.json")
        self.pending_file = os.path.join(data_dir, "pending.json")
        self.chain = []
        self.pending_transactions = []
        
        # PARAMETRI ESATTI COME BITCOIN
        self.initial_difficulty = 4  # Difficulty iniziale
        self.target_block_time = 600  # 10 minuti ESATTI come Bitcoin
        self.blocks_per_difficulty_adjustment = 2016  # ESATTO come Bitcoin (2 settimane)
        self.blocks_per_halving = 210000  # ESATTO come Bitcoin (~4 anni)
        self.initial_reward = 50.0  # ESATTO come Bitcoin originale
        self.max_supply = 21000000  # ESATTO come Bitcoin
        
        self.total_mined = 0
        self.difficulty = self.initial_difficulty
        
        os.makedirs(data_dir, exist_ok=True)
        self.load_chain()
        self.load_pending()
        
        if not self.chain:
            self.create_genesis_block()
        else:
            # Aggiorna difficulty basata sulla blockchain caricata
            self.difficulty = self.calculate_difficulty()
    
    def create_genesis_block(self):
        try:
            with open("wallet.dat", "r") as f:
                wallet_data = json.load(f)
            genesis_address = wallet_data["address"]
        except:
            genesis_address = "jabo867WwmfUePRCzYDNn6iqbAw"
        
        genesis_tx = Transaction("0", genesis_address, 1000000.0, 0.0)
        genesis_block = Block(0, [genesis_tx], time.time(), "0" * 64, 0, "genesis")
        
        self.chain.append(genesis_block)
        self.total_mined += 1000000.0
        self.save_chain()
        print("✅ Genesis Block creato!")
    
    def calculate_difficulty(self):
        """CALCOLO DIFFICULTY ESATTO COME BITCOIN"""
        if len(self.chain) <= self.blocks_per_difficulty_adjustment:
            return self.initial_difficulty
        
        # Prendi l'ultimo blocco del periodo precedente
        last_adjustment_block = self.chain[-self.blocks_per_difficulty_adjustment]
        current_block = self.chain[-1]
        
        # Tempo reale impiegato per i 2016 blocchi
        actual_time = current_block.timestamp - last_adjustment_block.timestamp
        
        # Tempo atteso per 2016 blocchi (2 settimane)
        expected_time = self.blocks_per_difficulty_adjustment * self.target_block_time
        
        print(f"📊 Adjusting difficulty:")
        print(f"   Periodo: {actual_time:.0f}s (atteso: {expected_time:.0f}s)")
        print(f"   Ratio: {actual_time/expected_time:.2f}")
        
        # Limita l'aggiustamento a 4x come Bitcoin
        if actual_time < expected_time / 4:
            actual_time = expected_time / 4
        elif actual_time > expected_time * 4:
            actual_time = expected_time * 4
        
        # Calcola nuovo difficulty
        difficulty_ratio = actual_time / expected_time
        new_difficulty = self.difficulty * difficulty_ratio
        
        # Arrotonda e limita
        new_difficulty = max(1, min(20, int(new_difficulty + 0.5)))  # Max difficulty 20 per testing
        
        print(f"   Difficulty: {self.difficulty} → {new_difficulty}")
        return new_difficulty
    
    def get_current_reward(self):
        """CALCOLO REWARD CON HALVING ESATTO COME BITCOIN"""
        halvings = len(self.chain) // self.blocks_per_halving
        reward = self.initial_reward / (2 ** halvings)
        return max(reward, 0)  # Non scendere sotto zero
    
    def get_next_halving_info(self):
        """Informazioni sul prossimo halving"""
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
                        block_data.get('miner', 'unknown')
                    )
                    block.hash = block_data['hash']
                    self.chain.append(block)
                
                print(f"✅ Blockchain caricata: {len(self.chain)} blocchi")
                
                # Calcola total mined e halving info
                self.total_mined = 0
                for block in self.chain:
                    for tx in block.transactions:
                        if tx.sender == "0":
                            self.total_mined += tx.amount
                
                # Mostra info halving
                halving_info = self.get_next_halving_info()
                print(f"💰 Reward attuale: {halving_info['current_reward']} RHO")
                print(f"⏳ Prossimo halving: blocco {halving_info['halving_at_block']} ({halving_info['blocks_remaining']} blocchi rimanenti)")
                
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
        print(f"✅ Transazione aggiunta alla pool pendente")
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
        """MINING CON HALVING E DIFFICULTY COME BITCOIN"""
        # Aggiorna difficulty ogni 2016 blocchi
        if len(self.chain) % self.blocks_per_difficulty_adjustment == 0:
            self.difficulty = self.calculate_difficulty()
        
        current_reward = self.get_current_reward()
        halving_info = self.get_next_halving_info()
        
        print(f"⛏️  Mining blocco {len(self.chain)}")
        print(f"   🎯 Difficulty: {self.difficulty}")
        print(f"   💰 Reward: {current_reward} RHO")
        print(f"   ⏳ Halving: {halving_info['blocks_remaining']} blocchi rimanenti")
        
        # CREA TRANSAZIONE DI REWARD
        reward_tx = Transaction("0", miner_address, current_reward, 0.0)
        
        # Se ci sono transazioni pendenti, includile
        if self.pending_transactions:
            block_transactions = [reward_tx] + self.pending_transactions
            print(f"   📦 Includendo {len(self.pending_transactions)} transazioni pendenti")
        else:
            block_transactions = [reward_tx]
            print(f"   💰 Mining blocco vuoto (solo reward)")
        
        previous_hash = self.get_latest_block().hash
        
        new_block = Block(len(self.chain), block_transactions, time.time(), previous_hash)
        
        # PROOF OF WORK
        target = "0" * self.difficulty
        start_time = time.time()
        hashes_calculated = 0
        
        print(f"   🎯 Target: {target}")
        print(f"   ⏳ Calcolando hash...", end='', flush=True)
        
        while new_block.hash[:self.difficulty] != target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            hashes_calculated += 1
            
            if hashes_calculated % 10000 == 0:
                print(".", end='', flush=True)
        
        mining_time = time.time() - start_time
        hash_rate = hashes_calculated / mining_time if mining_time > 0 else 0
        
        print()
        print(f"✅ Blocco {new_block.index} minato in {mining_time:.2f} secondi!")
        print(f"   📊 Hash calcolati: {hashes_calculated:,}")
        print(f"   ⚡ Hash rate: {hash_rate:,.0f} H/s")
        print(f"   🔨 Nonce: {new_block.nonce}")
        print(f"   💰 Ricompensa: {current_reward} RHO")
        print(f"   📦 Transazioni: {len(block_transactions)}")
        
        # Controlla se è avvenuto un halving
        if (new_block.index + 1) % self.blocks_per_halving == 0:
            new_reward = self.get_current_reward()
            print(f"🎉 HALVING! Nuovo reward: {new_reward} RHO")
        
        self.chain.append(new_block)
        self.pending_transactions = []
        self.total_mined += current_reward
        self.save_chain()
        
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
        
        return True

if __name__ == "__main__":
    blockchain = RhodiumBlockchain()
    print(f"📦 Blocchi: {len(blockchain.chain)}")
    print(f"📊 Transazioni pendenti: {len(blockchain.pending_transactions)}")
    print(f"💰 RHO totali minati: {blockchain.total_mined:,.2f}")
    
    halving_info = blockchain.get_next_halving_info()
    print(f"🎯 Difficulty attuale: {blockchain.difficulty}")
    print(f"💎 Reward attuale: {halving_info['current_reward']} RHO")
    print(f"⏳ Prossimo halving: blocco {halving_info['halving_at_block']}")
    print(f"   ({halving_info['blocks_remaining']} blocchi rimanenti)")
