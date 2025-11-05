import hashlib
import base58
import os
import json
import time
from rhodium_core_hard import Transaction

class RhodiumWallet:
    def __init__(self):
        self.private_key = os.urandom(32)
        self.balance = 0
        self.load_wallet()
        
    def get_address(self):
        sha256 = hashlib.sha256(self.private_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256)
        ripemd160_digest = ripemd160.digest()
        version_prefix = b'R'
        payload = version_prefix + ripemd160_digest
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        full_payload = payload + checksum
        address = base58.b58encode(full_payload).decode('ascii')
        return "jabo86" + address[6:12] + address[12:24]
    
    def get_balance(self):
        return self.balance
    
    def create_transaction(self, recipient, amount):
        if amount <= 0:
            return None
            
        transaction = Transaction(
            self.get_address(),
            recipient,
            amount
        )
        
        transaction.signature = hashlib.sha256(
            f"{self.get_address()}{recipient}{amount}{time.time()}".encode()
        ).hexdigest()
        
        transaction.timestamp = time.time()
        return transaction
    
    def save_wallet(self):
        wallet_data = {
            'private_key': self.private_key.hex(),
            'balance': self.balance
        }
        with open('wallet.json', 'w') as f:
            json.dump(wallet_data, f)
    
    def load_wallet(self):
        try:
            with open('wallet.json', 'r') as f:
                wallet_data = json.load(f)
                self.private_key = bytes.fromhex(wallet_data['private_key'])
                self.balance = wallet_data.get('balance', 0)
            print(f"✅ Wallet caricato: {self.get_address()}")
        except FileNotFoundError:
            print("✅ Nuovo wallet creato")
            self.save_wallet()

    def sync_with_blockchain(self, blockchain):
        """Sincronizza il wallet con la blockchain"""
        old_balance = self.balance
        self.balance = 0
        
        for block in blockchain.chain:
            for tx in block.transactions:
                if tx.recipient == self.get_address():
                    self.balance += tx.amount
                if tx.sender == self.get_address() and tx.sender != "0":
                    self.balance -= tx.amount
        
        print(f"💰 Wallet sincronizzato: {old_balance} -> {self.balance} RHO")
        self.save_wallet()
    
    def get_complete_history(self, blockchain):
        """Restituisce cronologia completa"""
        try:
            return blockchain.get_all_transactions_for_address(self.get_address())
        except:
            return []
    
    def send_transaction(self, recipient, amount, blockchain):
        """Invia RHO e aggiunge alla blockchain"""
        if amount <= 0:
            return False, "Importo non valido"
        
        # Verifica saldo sincronizzato
        self.sync_with_blockchain(blockchain)
        
        if amount > self.balance:
            return False, f"Saldo insufficiente: {self.balance} RHO"
        
        # Crea transazione
        tx = self.create_transaction(recipient, amount)
        if not tx:
            return False, "Errore creazione transazione"
        
        # Aggiungi alla blockchain
        if blockchain.add_transaction(tx):
            self.balance -= amount
            self.save_wallet()
            return True, f"✅ Inviati {amount} RHO a {recipient[:10]}..."
        else:
            return False, "Errore aggiunta transazione"

if __name__ == "__main__":
    wallet = RhodiumWallet()
    print(f"👛 Indirizzo: {wallet.get_address()}")
    print(f"💰 Saldo: {wallet.get_balance()} RHO")
