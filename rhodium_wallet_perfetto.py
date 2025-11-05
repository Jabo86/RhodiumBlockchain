import hashlib
import base58
import os
import json
import time
from rhodium_core_hard import Transaction

class RhodiumWallet:
    def __init__(self):
        # INDIRIZZO FISSO
        self.address = "jabo867WwmfUePRCzYDNn6iqbAw"
        self.balance = 0
        self.wallet_file = 'wallet_perfetto.json'
        
        print(f"👛 Wallet inizializzato: {self.address}")
        self.sync_completo()
        
    def get_address(self):
        return self.address
    
    def get_balance(self):
        return self.balance
    
    def create_transaction(self, recipient, amount):
        if amount <= 0:
            print("❌ Importo non valido")
            return None
            
        if amount > self.balance:
            print(f"❌ Saldo insufficiente: {self.balance} < {amount}")
            return None
            
        print(f"💸 Creando transazione: {self.address} -> {recipient}: {amount} RHO")
        
        transaction = Transaction(
            self.address,
            recipient,
            amount
        )
        
        transaction.signature = hashlib.sha256(
            f"{self.address}{recipient}{amount}{time.time()}".encode()
        ).hexdigest()
        
        transaction.timestamp = time.time()
        return transaction
    
    def sync_completo(self):
        """SINCRONIZZAZIONE COMPLETA E AFFIDABILE"""
        from rhodium_core_hard import RhodiumBlockchain
        
        print("🔄 Sincronizzazione COMPLETA in corso...")
        blockchain = RhodiumBlockchain()
        old_balance = self.balance
        self.balance = 0
        
        print(f"🔍 Analizzo {len(blockchain.chain)} blocchi...")
        
        for i, block in enumerate(blockchain.chain):
            for tx in block.transactions:
                # SE HO RICEVUTO SOLDI
                if tx.recipient == self.address:
                    self.balance += tx.amount
                    print(f"   ✅ Blocco {i}: +{tx.amount:>10.2f} RHO (da {tx.sender})")
                
                # SE HO INVIATO SOLDI (escludi mining)
                if tx.sender == self.address and tx.sender != "0":
                    self.balance -= tx.amount
                    print(f"   🔻 Blocco {i}: -{tx.amount:>10.2f} RHO (a {tx.recipient})")
        
        print(f"💰 Saldo aggiornato: {old_balance:,.2f} -> {self.balance:,.2f} RHO")
        
        # SALVA il wallet
        self.salva_wallet()
        
        return self.balance
    
    def salva_wallet(self):
        """Salva il wallet su file"""
        wallet_data = {
            'address': self.address,
            'balance': self.balance,
            'last_sync': time.time()
        }
        try:
            with open(self.wallet_file, 'w') as f:
                json.dump(wallet_data, f, indent=2)
            print(f"💾 Wallet salvato: {self.balance:,.2f} RHO")
        except Exception as e:
            print(f"❌ Errore salvataggio wallet: {e}")
    
    def carica_wallet(self):
        """Carica il wallet dal file"""
        try:
            with open(self.wallet_file, 'r') as f:
                wallet_data = json.load(f)
                self.balance = wallet_data.get('balance', 0)
                last_sync = wallet_data.get('last_sync', 0)
                print(f"📂 Wallet caricato: {self.balance:,.2f} RHO")
                print(f"⏰ Ultima sincronizzazione: {time.ctime(last_sync)}")
        except FileNotFoundError:
            print("📂 Nessun wallet trovato, sincronizzo con blockchain...")
            self.sync_completo()
        except Exception as e:
            print(f"❌ Errore caricamento wallet: {e}")
            self.sync_completo()
    
    def get_complete_history(self, blockchain):
        """Restituisce cronologia COMPLETA"""
        try:
            print("📜 Caricamento cronologia...")
            transactions = blockchain.get_all_transactions_for_address(self.address)
            print(f"📋 Trovate {len(transactions)} transazioni")
            return transactions
        except Exception as e:
            print(f"❌ Errore cronologia: {e}")
            return []
    
    def send_transaction(self, recipient, amount, blockchain):
        """Invia RHO - VERSIONE AFFIDABILE"""
        print(f"🚀 Tentativo invio: {amount} RHO a {recipient}")
        
        if amount <= 0:
            return False, "Importo non valido"
        
        # Sincronizza PRIMA di verificare il saldo
        self.sync_completo()
        
        if amount > self.balance:
            return False, f"Saldo insufficiente: {self.balance:.2f} RHO"
        
        # Crea transazione
        tx = self.create_transaction(recipient, amount)
        if not tx:
            return False, "Errore creazione transazione"
        
        # Aggiungi alla blockchain
        if blockchain.add_transaction(tx):
            print(f"✅ Transazione aggiunta alla blockchain")
            
            # Aggiorna saldo LOCALMENTE
            self.balance -= amount
            self.salva_wallet()
            
            return True, f"✅ Inviati {amount} RHO a {recipient[:12]}..."
        else:
            return False, "Errore aggiunta transazione alla blockchain"

# Sostituisci la funzione di sincronizzazione nell'inizializzazione
def _sync_on_init(self):
    self.carica_wallet()  # Prima carica dal file
    self.sync_completo()  # Poi sincronizza con blockchain

# Aggiungi questa funzione alla classe
RhodiumWallet.sync_on_init = _sync_on_init

if __name__ == "__main__":
    wallet = RhodiumWallet()
    print(f"👛 Indirizzo: {wallet.get_address()}")
    print(f"💰 Saldo FINALE: {wallet.get_balance():,.2f} RHO")
