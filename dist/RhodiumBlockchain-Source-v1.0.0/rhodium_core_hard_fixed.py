import hashlib
import time
import json
import os
from datetime import datetime

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, difficulty=10):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        transactions_str = "".join([f"{tx.sender}{tx.recipient}{tx.amount}" for tx in self.transactions])
        block_data = f"{self.index}{transactions_str}{self.timestamp}{self.previous_hash}{self.nonce}{self.difficulty}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        print(f"   🎯 Target: {'0' * difficulty} ({difficulty} zeri)")
        print("   ⏳ Calcolando hash", end="")
        
        start_time = time.time()
        hash_calculated = 0
        
        while True:
            self.hash = self.calculate_hash()
            hash_calculated += 1
            
            if hash_calculated % 10000 == 0:
                print(".", end="", flush=True)
            
            if self.hash[:difficulty] == "0" * difficulty:
                mining_time = time.time() - start_time
                hash_rate = hash_calculated / mining_time if mining_time > 0 else 0
                
                print(f"\\n✅ Blocco {self.index} minato in {mining_time:.2f} secondi!")
                print(f"   📊 Hash calcolati: {hash_calculated:,}")
                print(f"   ⚡ Hash rate: {hash_rate:,.0f} H/s")
                print(f"   🔨 Nonce: {self.nonce}")
                print(f"   💰 Ricompensa: {self.get_block_reward()} RHO")
                print(f"   📦 Transazioni: {len(self.transactions)}")
                print(f"   🔗 Hash: {self.hash}")
                return True
            
            self.nonce += 1
            
            # Timeout di sicurezza (10 minuti)
            if time.time() - start_time > 600:
                print("\\n❌ Timeout mining")
                return False

    def get_block_reward(self):
        for tx in self.transactions:
            if tx.sender == "0":
                return tx.amount
        return 0

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None

class RhodiumBlockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 10  # DIFFICOLTÀ 10 FISSA
        self.blocks_per_halving = 210000
        self.initial_reward = 50.0
        self.total_mined = 0
        self.chain_file = 'blockchain_hard.json'
        self.pending_file = 'pending_hard.json'
        self.load_chain()

    def create_genesis_block(self):
        genesis_transaction = Transaction("0", "jabo867WwmfUePRCzYDNn6iqbAw", 1000000.0)
        return Block(0, [genesis_transaction], time.time(), "0", self.difficulty)

    def load_chain(self):
        try:
            if os.path.exists(self.chain_file):
                with open(self.chain_file, 'r') as f:
                    data = json.load(f)
                    self.chain = []
                    for block_data in data['chain']:
                        transactions = [
                            Transaction(tx['sender'], tx['recipient'], tx['amount'])
                            for tx in block_data['transactions']
                        ]
                        block = Block(
                            block_data['index'],
                            transactions,
                            block_data['timestamp'],
                            block_data['previous_hash'],
                            self.difficulty
                        )
                        block.nonce = block_data['nonce']
                        block.hash = block_data['hash']
                        self.chain.append(block)
                
                self.total_mined = data.get('total_mined', 0)
                print(f"✅ Blockchain caricata: {len(self.chain)} blocchi")
            else:
                self.chain = [self.create_genesis_block()]
                self.save_chain()
                print("✅ Genesis Block creato!")
        except Exception as e:
            print(f"❌ Errore caricamento blockchain: {e}")
            self.chain = [self.create_genesis_block()]

    def save_chain(self):
        data = {
            'chain': [
                {
                    'index': block.index,
                    'transactions': [
                        {
                            'sender': tx.sender,
                            'recipient': tx.recipient,
                            'amount': tx.amount,
                            'timestamp': tx.timestamp
                        }
                        for tx in block.transactions
                    ],
                    'timestamp': block.timestamp,
                    'previous_hash': block.previous_hash,
                    'nonce': block.nonce,
                    'hash': block.hash
                }
                for block in self.chain
            ],
            'total_mined': self.total_mined
        }
        
        with open(self.chain_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_current_reward(self):
        current_height = len(self.chain)
        halvings = current_height // self.blocks_per_halving
        reward = self.initial_reward / (2 ** halvings)
        return max(0.00000001, reward)

    def get_next_halving_info(self):
        current_height = len(self.chain)
        halving_at_block = ((current_height // self.blocks_per_halving) + 1) * self.blocks_per_halving
        blocks_remaining = halving_at_block - current_height
        
        return {
            'current_reward': self.get_current_reward(),
            'halving_at_block': halving_at_block,
            'blocks_remaining': blocks_remaining
        }

    def add_transaction(self, transaction):
        if transaction.amount <= 0:
            return False
        
        # Verifica saldo per transazioni normali (non mining)
        if transaction.sender != "0":
            sender_balance = self.get_balance(transaction.sender)
            if sender_balance < transaction.amount:
                print(f"❌ Saldo insufficiente: {sender_balance} < {transaction.amount}")
                return False
        
        self.pending_transactions.append(transaction)
        print(f"✅ Transazione aggiunta: {transaction.sender[:8]}... -> {transaction.recipient[:8]}...: {transaction.amount} RHO")
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address and tx.sender != "0":
                    balance -= tx.amount
        return balance

    def mine_block(self, miner_address):
        if not miner_address:
            print("❌ Indirizzo miner non valido")
            return None

        # Crea transazione di reward
        reward = self.get_current_reward()
        reward_tx = Transaction("0", miner_address, reward)
        reward_tx.timestamp = time.time()

        # Prepara transazioni per il blocco
        block_transactions = [reward_tx]
        
        # Aggiungi transazioni pendenti
        if self.pending_transactions:
            block_transactions.extend(self.pending_transactions[:10])
            print(f"   📦 Incluse {len(self.pending_transactions[:10])} transazioni pendenti")

        # Crea nuovo blocco
        previous_hash = self.chain[-1].hash if self.chain else "0"
        new_block = Block(
            index=len(self.chain),
            transactions=block_transactions,
            timestamp=time.time(),
            previous_hash=previous_hash,
            difficulty=self.difficulty
        )

        # Mining
        print(f"\\n⛏️  Mining blocco {new_block.index}")
        print(f"   🎯 Difficulty: {self.difficulty}")
        print(f"   💰 Reward: {reward} RHO")
        
        success = new_block.mine_block(self.difficulty)

        if success and new_block.hash:
            # Rimuovi transazioni confermate
            pending_to_remove = [tx for tx in self.pending_transactions if tx in block_transactions]
            for tx in pending_to_remove:
                if tx in self.pending_transactions:
                    self.pending_transactions.remove(tx)

            # Aggiungi blocco alla blockchain
            self.chain.append(new_block)
            self.total_mined += reward
            self.save_chain()
            
            return new_block
        else:
            print("❌ Mining fallito")
            return None

    def get_all_transactions_for_address(self, address):
        """Restituisce TUTTE le transazioni per un indirizzo"""
        transactions = []
        try:
            for block in self.chain:
                for tx in block.transactions:
                    # Transazione di MINING
                    if tx.sender == "0" and tx.recipient == address:
                        date_str = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M')
                        transactions.append({
                            'type': 'MINING',
                            'amount': float(tx.amount),
                            'address': 'RICHIESTA MINING',
                            'date': date_str
                        })
                    
                    # Transazione NORMALE (inviata)
                    elif tx.sender == address:
                        date_str = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M')
                        transactions.append({
                            'type': 'INVIO',
                            'amount': float(tx.amount),
                            'address': tx.recipient,
                            'date': date_str
                        })
                    
                    # Transazione NORMALE (ricevuta)
                    elif tx.recipient == address and tx.sender != "0":
                        date_str = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M')
                        transactions.append({
                            'type': 'RICEZIONE', 
                            'amount': float(tx.amount),
                            'address': tx.sender,
                            'date': date_str
                        })
        except Exception as e:
            print(f"❌ Errore transazioni: {e}")
            
        return transactions

if __name__ == "__main__":
    blockchain = RhodiumBlockchain()
    print(f"📦 Blocchi: {len(blockchain.chain)}")
    print(f"🎯 Difficulty: {blockchain.difficulty}")
    print(f"💰 Reward attuale: {blockchain.get_current_reward()} RHO")
