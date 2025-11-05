with open('rhodium_core_hard.py', 'r') as f:
    content = f.read()

# Aggiungi una versione semplificata ma funzionante della funzione
new_function = '''
    def get_transactions_for_address(self, address):
        """Restituisce tutte le transazioni per un indirizzo specifico - VERSIONE SICURA"""
        transactions = []
        try:
            for block in self.chain:
                for tx in block.transactions:
                    # Controlla che la transazione abbia gli attributi necessari
                    if hasattr(tx, 'sender') and hasattr(tx, 'recipient') and hasattr(tx, 'amount'):
                        if tx.sender == address or tx.recipient == address:
                            tx_type = 'INVIO' if tx.sender == address else 'RICEZIONE'
                            other_address = tx.recipient if tx.sender == address else tx.sender
                            
                            # Formatta la data
                            from datetime import datetime
                            date_str = datetime.fromtimestamp(getattr(tx, 'timestamp', 0)).strftime('%Y-%m-%d %H:%M')
                            
                            transactions.append({
                                'type': tx_type,
                                'amount': float(tx.amount),
                                'address': str(other_address),
                                'date': date_str
                            })
        except Exception as e:
            print(f"⚠️  Errore nel caricamento transazioni: {e}")
            
        return transactions
'''

# Cerca e sostituisci la funzione esistente
import re
pattern = r'def get_transactions_for_address\(self, address\):.*?return transactions'
content = re.sub(pattern, new_function, content, flags=re.DOTALL)

with open('rhodium_core_hard.py', 'w') as f:
    f.write(content)

print("✅ Funzione transazioni aggiornata con versione sicura!")
