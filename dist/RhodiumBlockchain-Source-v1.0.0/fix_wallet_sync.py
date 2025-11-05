with open('rhodium_wallet.py', 'r') as f:
    content = f.read()

# Aggiungi funzioni per sincronizzare con la blockchain
new_wallet_functions = '''
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
'''

# Aggiungi le nuove funzioni alla classe
if 'def get_address(self):' in content:
    content = content.replace('def get_address(self):', new_wallet_functions + '\\n    def get_address(self):')

with open('rhodium_wallet.py', 'w') as f:
    f.write(content)

print("✅ Wallet aggiornato con sincronizzazione!")
