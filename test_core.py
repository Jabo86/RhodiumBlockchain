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

class TestBlockchain:
    def __init__(self, data_dir="test_blockchain"):
        self.data_dir = data_dir
        self.chain_file = os.path.join(data_dir, "chain.json")
        self.chain = []
        self.pending_transactions = []
        
        # PARAMETRI DI TEST - HALVING OGNI 5 BLOCCHI
        self.difficulty = 4
        self.blocks_per_halving = 5  # HALVING OGNI 5 BLOCCHI PER TEST
        self.initial_reward = 50.0
        self.max_supply = 21000000
        self.total_mined = 0
        
        os.makedirs(data_dir, exist_ok=True)
        self.load_chain()
        
        if not self.chain:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_tx = Transaction("0", "jabo867WwmfUePRCzYDNn6iqbAw", 1000000.0, 0.0)
        genesis_block = Block(0, [genesis_tx], time.time(), "0" * 64, 0, "genesis")
        self.chain.append(genesis_block)
        self.total_mined += 1000000.0
        self.save_chain()
        print("✅ Genesis Block creato!")
    
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
                        block_data.get('miner', 'unknown')
                    )
                    block.hash = block_data['hash']
                    self.chain.append(block)
                
                print(f"✅ Blockchain caricata: {len(self.chain)} blocchi")
                
                self.total_mined = 0
                for block in self.chain:
                    for tx in block.transactions:
                        if tx.sender == "0":
                            self.total_mined += tx.amount
                
            except Exception as e:
                print(f"❌ Errore caricamento: {e}")
    
    def mine_block(self, miner_address):
        current_reward = self.get_current_reward()
        halving_info = self.get_next_halving_info()
        
        print(f"⛏️  Mining blocco {len(self.chain)}")
        print(f"   💰 Reward: {current_reward} RHO")
        print(f"   ⏳ Halving tra: {halving_info['blocks_remaining']} blocchi")
        
        reward_tx = Transaction("0", miner_address, current_reward, 0.0)
        block_transactions = [reward_tx]
        
        previous_hash = self.chain[-1].hash if self.chain else "0" * 64
        
        new_block = Block(len(self.chain), block_transactions, time.time(), previous_hash)
        
        target = "0" * self.difficulty
        start_time = time.time()
        
        while new_block.hash[:self.difficulty] != target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        mining_time = time.time() - start_time
        
        old_reward = current_reward
        self.chain.append(new_block)
        self.total_mined += current_reward
        self.save_chain()
        
        new_reward = self.get_current_reward()
        
        print(f"✅ Blocco {new_block.index} minato in {mining_time:.2f}s")
        print(f"   🔗 Hash: {new_block.hash[:20]}...")
        
        if new_reward < old_reward:
            print(f"🎉 HALVING! Nuovo reward: {new_reward} RHO")
        
        return new_block

if __name__ == "__main__":
    blockchain = TestBlockchain()
    print(f"📦 Blocchi: {len(blockchain.chain)}")
    
    halving_info = blockchain.get_next_halving_info()
    print(f"💎 Reward: {halving_info['current_reward']} RHO")
    print(f"⏳ Prossimo halving: {halving_info['blocks_remaining']} blocchi")
