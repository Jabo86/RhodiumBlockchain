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
        self.difficulty = 2
        self.mining_reward = 50.0
        self.block_time = 150
        self.max_supply = 21000000
        self.total_mined = 0
        
        os.makedirs(data_dir, exist_ok=True)
        self.load_chain()
        self.load_pending()
        
        if not self.chain:
            self.create_genesis_block()
    
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
        """Aggiungi transazione alla pool e SALVALA"""
        self.pending_transactions.append(transaction)
        self.save_pending()  # SALVA SUBITO!
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
        if not self.pending_transactions:
            print("❌ Nessuna transazione da minare")
            return None
        
        print(f"⛏️  Mining blocco {len(self.chain)} con {len(self.pending_transactions)} transazioni...")
        
        # Aggiungi reward al miner
        reward_tx = Transaction("0", miner_address, self.mining_reward, 0.0)
        block_transactions = [reward_tx] + self.pending_transactions
        previous_hash = self.get_latest_block().hash
        
        new_block = Block(len(self.chain), block_transactions, time.time(), previous_hash)
        
        # PROOF OF WORK
        target = "0" * self.difficulty
        start_time = time.time()
        
        while new_block.hash[:self.difficulty] != target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
        
        mining_time = time.time() - start_time
        print(f"✅ Blocco {new_block.index} minato in {mining_time:.2f} secondi!")
        
        self.chain.append(new_block)
        self.pending_transactions = []  # Pulisci le transazioni processate
        self.save_chain()
        
        # Rimuovi il file delle transazioni pendenti
        if os.path.exists(self.pending_file):
            os.remove(self.pending_file)
        
        self.total_mined += self.mining_reward
        
        print(f"💰 Ricompensa: {self.mining_reward} RHO per {miner_address}")
        print(f"🔗 Hash blocco: {new_block.hash}")
        
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
