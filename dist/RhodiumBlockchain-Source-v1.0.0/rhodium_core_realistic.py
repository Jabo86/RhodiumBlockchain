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
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, miner="system", bits=None):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner = miner
        self.bits = bits  # Formato compact come Bitcoin
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        transactions_str = ''.join([tx.txid for tx in self.transactions])
        block_data = f"{self.index}{transactions_str}{self.timestamp}{self.previous_hash}{self.nonce}{self.bits}"
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
            'bits': self.bits
        }

class RhodiumBlockchain:
    def __init__(self, data_dir="blockchain_data"):
        self.data_dir = data_dir
        self.chain_file = os.path.join(data_dir, "chain.json")
        self.pending_file = os.path.join(data_dir, "pending.json")
        self.chain = []
        self.pending_transactions = []
        
        # PARAMETRI REALISTICI COME BITCOIN
        self.initial_bits = 0x1e0ffff0  # Difficulty iniziale (simile Bitcoin 2009)
        self.target_block_time = 600  # 10 minuti ESATTI
        self.blocks_per_difficulty_adjustment = 2016  # 2 settimane
        self.blocks_per_halving = 210000  # ~4 anni
        self.initial_reward = 50.0
        self.max_supply = 21000000
        
        self.total_mined = 0
        self.current_bits = self.initial_bits
        
        os.makedirs(data_dir, exist_ok=True)
        self.load_chain()
        self.load_pending()
        
        if not self.chain:
            self.create_genesis_block()
        else:
            self.current_bits = self.calculate_difficulty()
    
    def create_genesis_block(self):
        try:
            with open("wallet.dat", "r") as f:
                wallet_data = json.load(f)
            genesis_address = wallet_data["address"]
        except:
            genesis_address = "jabo867WwmfUePRCzYDNn6iqbAw"
        
        genesis_tx = Transaction("0", genesis_address, 1000000.0, 0.0)
        genesis_block = Block(0, [genesis_tx], time.time(), "0" * 64, 0, "genesis", self.initial_bits)
        
        self.chain.append(genesis_block)
        self.total_mined += 1000000.0
        self.save_chain()
        print("✅ Genesis Block creato!")
    
    def bits_to_target(self, bits):
        """Converti bits in target numerico"""
        exponent = bits >> 24
        coefficient = bits & 0xffffff
        return coefficient * (2 ** (8 * (exponent - 3)))
    
    def target_to_bits(self, target):
        """Converti target in formato compact"""
        if target <= 0:
            return self.initial_bits
        
        exponent = 0
        while target >= 0x800000:
            target >>= 8
            exponent += 1
        
        coefficient = target
        if coefficient > 0xffffff:
            coefficient >>= 8
            exponent += 1
        
        return (exponent << 24) | coefficient
    
    def calculate_difficulty(self):
        """DIFFICULTY ADJUSTMENT REALE COME BITCOIN"""
        if len(self.chain) <= self.blocks_per_difficulty_adjustment:
            return self.current_bits
        
        # Prendi il blocco prima del periodo di adjustment
        last_adjustment_block = self.chain[-self.blocks_per_difficulty_adjustment]
        time_span = self.chain[-1].timestamp - last_adjustment_block.timestamp
        
        # Tempo atteso per 2016 blocchi (2 settimane)
        expected_time = self.blocks_per_difficulty_adjustment * self.target_block_time
        
        print(f"📊 Adjusting difficulty:")
        print(f"   Periodo: {time_span/3600:.1f}h (atteso: {expected_time/3600:.1f}h)")
        print(f"   Ratio: {time_span/expected_time:.3f}")
        
        # Limita l'aggiustamento a 4x come Bitcoin
        if time_span < expected_time / 4:
            time_span = expected_time / 4
        elif time_span > expected_time * 4:
            time_span = expected_time * 4
        
        # Converti bits a target
        old_target = self.bits_to_target(last_adjustment_block.bits)
        
        # Calcola nuovo target
        new_target = old_target * time_span / expected_time
        
        # Converti a bits
        new_bits = self.target_to_bits(int(new_target))
        
        old_difficulty = self.get_difficulty_from_bits(self.current_bits)
        new_difficulty = self.get_difficulty_from_bits(new_bits)
        
        print(f"   Difficulty: {old_difficulty:,.0f} → {new_difficulty:,.0f}")
        
        return new_bits
    
    def get_difficulty_from_bits(self, bits):
        """Calcola difficulty number da bits"""
        target = self.bits_to_target(bits)
        max_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
        return max_target / target if target > 0 else float('inf')
    
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
                        block_data.get('bits', self.initial_bits)
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
                current_difficulty = self.get_difficulty_from_bits(self.current_bits)
                
                print(f"💰 Reward attuale: {halving_info['current_reward']} RHO")
                print(f"🎯 Difficulty: {current_difficulty:,.0f}")
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
        """MINING CON DIFFICULTY REALE"""
        # Aggiorna difficulty ogni 2016 blocchi
        if len(self.chain) > 0 and len(self.chain) % self.blocks_per_difficulty_adjustment == 0:
            self.current_bits = self.calculate_difficulty()
        
        current_reward = self.get_current_reward()
        current_difficulty = self.get_difficulty_from_bits(self.current_bits)
        halving_info = self.get_next_halving_info()
        
        print(f"⛏️  Mining blocco {len(self.chain)}")
        print(f"   🎯 Difficulty: {current_difficulty:,.0f}")
        print(f"   💰 Reward: {current_reward} RHO")
        print(f"   ⏳ Halving tra: {halving_info['blocks_remaining']:,} blocchi")
        
        # CREA TRANSAZIONE DI REWARD
        reward_tx = Transaction("0", miner_address, current_reward, 0.0)
        
        if self.pending_transactions:
            block_transactions = [reward_tx] + self.pending_transactions
            print(f"   📦 Includendo {len(self.pending_transactions)} transazioni")
        else:
            block_transactions = [reward_tx]
            print(f"   💰 Mining blocco vuoto")
        
        previous_hash = self.get_latest_block().hash
        
        new_block = Block(len(self.chain), block_transactions, time.time(), previous_hash, 0, miner_address, self.current_bits)
        
        # PROOF OF WORK REALE
        target = self.bits_to_target(self.current_bits)
        start_time = time.time()
        hashes_calculated = 0
        
        print(f"   🎯 Target: 0x{target:064x}")
        print(f"   ⏳ Calcolando hash...", end='', flush=True)
        
        while int(new_block.hash, 16) > target:
            new_block.nonce += 1
            new_block.hash = new_block.calculate_hash()
            hashes_calculated += 1
            
            if hashes_calculated % 100000 == 0:  # Mostra progresso ogni 100k hash
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
        
        # CONTROLLO HALVING
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
            
            # Verifica Proof of Work
            target = self.bits_to_target(current_block.bits)
            if int(current_block.hash, 16) > target:
                return False
        
        return True

if __name__ == "__main__":
    blockchain = RhodiumBlockchain()
    print(f"📦 Blocchi: {len(blockchain.chain)}")
    
    halving_info = blockchain.get_next_halving_info()
    current_difficulty = blockchain.get_difficulty_from_bits(blockchain.current_bits)
    
    print(f"💰 Reward: {halving_info['current_reward']} RHO")
    print(f"🎯 Difficulty: {current_difficulty:,.0f}")
    print(f"⏳ Prossimo halving: {halving_info['blocks_remaining']:,} blocchi")
