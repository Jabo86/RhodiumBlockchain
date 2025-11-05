with open('rhodium_gui_fixed.py', 'r') as f:
    content = f.read()

# Sostituisci la funzione load_transaction_history con una versione debug
new_function = '''
    def load_transaction_history(self):
        """Carica la cronologia transazioni - VERSIONE DEBUG"""
        try:
            # Pulisci la treeview
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            print("\\\\n🔍 [DEBUG] Caricamento transazioni in corso...")
            
            # TEST: prova a chiamare la funzione direttamente
            test_address = self.wallet.get_address()
            print(f"🔍 [DEBUG] Cerco transazioni per: {test_address}")
            
            transactions = []
            try:
                transactions = self.blockchain.get_all_transactions_for_address(test_address)
                print(f"✅ [DEBUG] Funzione chiamata, restituite {len(transactions)} transazioni")
            except Exception as e:
                print(f"❌ [DEBUG] Errore nella funzione: {e}")
                import traceback
                traceback.print_exc()
                transactions = []
            
            # DEBUG: mostra cosa abbiamo ottenuto
            print(f"🔍 [DEBUG] Transazioni ottenute: {len(transactions)}")
            for i, tx in enumerate(transactions[:3]):  # Prime 3
                print(f"   {i+1}. {tx}")
            
            # Se abbiamo transazioni, mostrale
            if transactions:
                print(f"✅ [DEBUG] Mostro {len(transactions)} transazioni nella GUI")
                for tx in transactions[-10:]:  # Ultime 10
                    self.transaction_tree.insert('', tk.END, values=(
                        tx.get('type', 'N/A'),
                        f"{tx.get('amount', 0):.6f} RHO",
                        tx.get('address', 'N/A'),
                        tx.get('date', 'N/A')
                    ))
            else:
                print("⚠️ [DEBUG] Nessuna transazione, mostro messaggio vuoto")
                self.transaction_tree.insert('', tk.END, values=(
                    'INFO', 'Nessuna transazione', 'Fai mining o invia RHO!', ''
                ))
                
            print("✅ [DEBUG] Caricamento transazioni completato\\\\n")
                
        except Exception as e:
            print(f"❌ [DEBUG] Errore generale: {e}")
            import traceback
            traceback.print_exc()
'''

import re
pattern = r'def load_transaction_history\(self\):.*?def update_balance'
content = re.sub(pattern, new_function + '\\n\\n    def update_balance', content, flags=re.DOTALL)

with open('rhodium_gui_fixed.py', 'w') as f:
    f.write(content)

print("✅ GUI aggiornata con debug!")
