#!/usr/bin/env python3
import json
import os
import hashlib
from Crypto.PublicKey import ECC
import base58

class RhodiumWallet:
    def __init__(self, wallet_file="wallet.dat"):
        self.wallet_file = wallet_file
        self.private_key = None
        self.public_key = None
        self.address = None
        self.load_wallet()
    
    def generate_keypair(self):
        """Genera una nuova coppia di chiavi ECC"""
        key = ECC.generate(curve='p256')
        self.private_key = key.export_key(format='DER')
        self.public_key = key.public_key().export_key(format='DER')
        self.address = self.generate_address()
        self.save_wallet()
        return self.address
    
    def generate_address(self):
        """Genera indirizzo che inizia con jabo86 - VERSIONE CORRETTA"""
        # Hash della public key (SHA256 + RIPEMD160)
        sha256_hash = hashlib.sha256(self.public_key).digest()
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(sha256_hash)
        hash_160 = ripemd160.digest()
        
        # Version byte per jabo86 (usiamo 0x58 come byte personalizzato)
        version_byte = b'\x58'
        payload = version_byte + hash_160
        
        # Checksum (doppio SHA256)
        checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        
        # Combina tutto e codifica in Base58
        address_bytes = payload + checksum
        address = base58.b58encode(address_bytes).decode('utf-8')
        
        # Forza l'indirizzo a iniziare con jabo86
        if not address.startswith('jabo86'):
            # Se non inizia con jabo86, usiamo un prefisso fisso + hash
            custom_prefix = "jabo86"
            address_hash = base58.b58encode(hash_160[:15]).decode('utf-8')
            address = custom_prefix + address_hash
        
        return address
    
    def save_wallet(self):
        """Salva wallet"""
        wallet_data = {
            'private_key': self.private_key.hex(),
            'public_key': self.public_key.hex(),
            'address': self.address
        }
        
        with open(self.wallet_file, 'w') as f:
            json.dump(wallet_data, f, indent=4)
        
        print(f"✅ Wallet salvato in {self.wallet_file}")
        print(f"🏠 Il tuo indirizzo Rhodium: {self.address}")
    
    def load_wallet(self):
        """Carica wallet esistente"""
        if os.path.exists(self.wallet_file):
            try:
                with open(self.wallet_file, 'r') as f:
                    wallet_data = json.load(f)
                self.private_key = bytes.fromhex(wallet_data['private_key'])
                self.public_key = bytes.fromhex(wallet_data['public_key'])
                self.address = wallet_data['address']
                print(f"✅ Wallet caricato: {self.address}")
            except Exception as e:
                print(f"❌ Errore: {e}")
    
    
    def sync_with_blockchain(self, blockchain):
        """Sincronizza il wallet con la blockchain - calcola saldo reale"""
        old_balance = self.balance
        self.balance = 0
        
        # Calcola il saldo dalle transazioni nella blockchain
        for block in blockchain.chain:
            for tx in block.transactions:
                # Se hai ricevuto fondi (mining o ricezione)
                if tx.recipient == self.get_address():
                    self.balance += tx.amount
                # Se hai inviato fondi (escluse ricompense mining)
                if tx.sender == self.get_address() and tx.sender != "0":
                    self.balance -= tx.amount
        
        print(f"💰 Wallet sincronizzato: {old_balance} -> {self.balance} RHO")
    
    def get_complete_history(self, blockchain):
        """Restituisce cronologia completa dalla blockchain"""
        transactions = []
        try:
            if hasattr(blockchain, 'get_all_transactions_for_address'):
                transactions = blockchain.get_all_transactions_for_address(self.get_address())
        except Exception as e:
            print(f"❌ Errore cronologia: {e}")
        return transactions
    
    def send_transaction(self, recipient, amount, blockchain):
        """Invia RHO e aggiunge alla blockchain"""
        if amount <= 0:
            return False, "Importo non valido"
        
        if amount > self.balance:
            return False, "Saldo insufficiente"
        
        # Crea transazione
        tx = self.create_transaction(recipient, amount)
        if not tx:
            return False, "Errore creazione transazione"
        
        # Aggiungi alla blockchain
        if blockchain.add_transaction(tx):
            # Aggiorna saldo immediatamente
            self.balance -= amount
            return True, f"✅ Inviati {amount} RHO a {recipient[:10]}..."
        else:
            return False, "Errore aggiunta transazione"
\n    def get_address(self):
        if not self.address:
            return self.generate_keypair()
        return self.address

def main():
    wallet = RhodiumWallet()
    if not wallet.address:
        print("🆕 Creazione nuovo wallet Rhodium...")
        address = wallet.generate_keypair()
        print(f"🎉 Nuovo wallet Rhodium creato!")
        print(f"📬 Il tuo indirizzo: {address}")
        print(f"💰 Riceverai 1,000,000 RHO nel Genesis Block!")
    else:
        print(f"📬 Wallet Rhodium esistente: {wallet.address}")

if __name__ == "__main__":
    main()

    def add_mining_reward(self, amount):
        """Aggiunge una ricompensa di mining al wallet"""
        self.balance += amount
        print(f"💰 Ricompensa mining: +{amount} RHO")
        
    def get_transaction_history(self, blockchain):
        """Restituisce la cronologia transazioni dal wallet"""
        transactions = []
        try:
            # Usa la funzione della blockchain se esiste
            if hasattr(blockchain, 'get_all_transactions_for_address'):
                transactions = blockchain.get_all_transactions_for_address(self.get_address())
        except:
            pass
        return transactions

    def add_mining_reward(self, amount):
        """Aggiunge una ricompensa di mining al wallet"""
        self.balance += amount
        print(f"💰 Ricompensa mining: +{amount} RHO")
        
    def get_transaction_history(self, blockchain):
        """Restituisce la cronologia transazioni dal wallet"""
        transactions = []
        try:
            # Usa la funzione della blockchain se esiste
            if hasattr(blockchain, 'get_all_transactions_for_address'):
                transactions = blockchain.get_all_transactions_for_address(self.get_address())
        except:
            pass
        return transactions
