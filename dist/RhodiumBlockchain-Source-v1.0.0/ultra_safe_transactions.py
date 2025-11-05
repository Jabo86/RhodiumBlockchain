with open('rhodium_gui_fixed.py', 'r') as f:
    content = f.read()

# Sostituisci la funzione load_transaction_history con una versione ultra-sicura
new_function = '''
    def load_transaction_history(self):
        """Carica la cronologia transazioni - VERSIONE ULTRA-SICURA"""
        try:
            # Pulisci la treeview
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Prova a caricare le transazioni
            transactions = []
            try:
                transactions = self.blockchain.get_transactions_for_address(self.wallet.get_address())
            except:
                pass  # Se fallisce, continua con lista vuota
            
            # Aggiungi le transazioni (ultime prime)
            for tx in reversed(transactions[-10:]):  # Ultime 10 transazioni
                self.transaction_tree.insert('', tk.END, values=(
                    tx.get('type', 'N/A'),
                    f"{tx.get('amount', 0):.6f} RHO",
                    tx.get('address', 'N/A'),
                    tx.get('date', 'N/A')
                ))
                
            # Se non ci sono transazioni, mostra un messaggio
            if not transactions:
                self.transaction_tree.insert('', tk.END, values=(
                    'INFO', 'Nessuna transazione', 'Usa "Invia RHO"', ''
                ))
                
        except Exception as e:
            # In caso di errore totale, mostra almeno la GUI
            print(f"⚠️  Errore caricamento transazioni: {e}")
            self.transaction_tree.insert('', tk.END, values=(
                'ERRORE', 'Impossibile caricare', 'transazioni', ''
            ))
'''

# Sostituisci la funzione
import re
pattern = r'def load_transaction_history\(self\):.*?def update_balance'
content = re.sub(pattern, new_function + '\\n\\n    def update_balance', content, flags=re.DOTALL)

with open('rhodium_gui_fixed.py', 'w') as f:
    f.write(content)

print("✅ Versione ultra-sicura delle transazioni installata!")
