with open('rhodium_gui_fixed.py', 'r') as f:
    content = f.read()

# Sostituisci la funzione update_balance per sincronizzare
new_update_balance = '''
    def update_balance(self):
        """Aggiorna il saldo sincronizzando con la blockchain"""
        try:
            # Sincronizza wallet con blockchain
            self.wallet.sync_with_blockchain(self.blockchain)
            balance = self.wallet.get_balance()
            self.balance_label.config(text=f"💰 Saldo: {balance:.6f} RHO")
            
            # Aggiorna anche l'indirizzo se non è visibile
            if hasattr(self, 'address_label'):
                self.address_label.config(text=f"👛 Indirizzo: {self.wallet.get_address()}")
            else:
                # Crea label indirizzo se non esiste
                self.address_label = ttk.Label(self.root, text=f"👛 Indirizzo: {self.wallet.get_address()}", 
                                              font=("Arial", 10), background='#1a1a1a', foreground='white')
                self.address_label.pack(pady=5)
                
        except Exception as e:
            print(f"❌ Errore aggiornamento saldo: {e}")
            self.balance_label.config(text="💰 Saldo: Errore")
'''

# Sostituisci la funzione
import re
pattern = r'def update_balance\(self\):.*?def'
content = re.sub(pattern, new_update_balance + '\\n\\n    def', content, flags=re.DOTALL)

# Sostituisci la funzione send_transaction per usare il wallet
new_send_transaction = '''
    def send_transaction(self):
        """Invia RHO usando il wallet"""
        recipient = self.recipient_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not recipient or not amount_str:
            messagebox.showerror("Errore", "Inserisci indirizzo e importo")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Errore", "L\\'importo deve essere positivo")
                return
        except:
            messagebox.showerror("Errore", "Importo non valido")
            return
        
        # Usa la nuova funzione del wallet
        success, message = self.wallet.send_transaction(recipient, amount, self.blockchain)
        
        if success:
            messagebox.showinfo("Successo", message)
            self.recipient_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.update_balance()
            self.load_transaction_history()
            self.mining_log.insert(tk.END, f"💸 {message}\\\\n")
            self.mining_log.see(tk.END)
        else:
            messagebox.showerror("Errore", message)
'''

# Sostituisci la funzione
pattern = r'def send_transaction\(self\):.*?def start_mining'
content = re.sub(pattern, new_send_transaction + '\\n\\n    def start_mining', content, flags=re.DOTALL)

# Sostituisci load_transaction_history per usare il wallet
new_load_history = '''
    def load_transaction_history(self):
        """Carica la cronologia dal wallet"""
        try:
            # Pulisci la treeview
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Carica transazioni dal wallet
            transactions = self.wallet.get_complete_history(self.blockchain)
            
            # Mostra le transazioni (ultime 10, più recenti prima)
            for tx in reversed(transactions[-10:]):
                self.transaction_tree.insert('', tk.END, values=(
                    tx.get('type', 'N/A'),
                    f"{tx.get('amount', 0):.6f} RHO",
                    tx.get('address', 'N/A'),
                    tx.get('date', 'N/A')
                ))
                
            # Se vuoto, mostra messaggio
            if not transactions:
                self.transaction_tree.insert('', tk.END, values=(
                    'INFO', 'Nessuna transazione', 'Fai mining o invia RHO!', ''
                ))
                
        except Exception as e:
            print(f"⚠️ Errore caricamento transazioni: {e}")
'''

pattern = r'def load_transaction_history\(self\):.*?def update_balance'
content = re.sub(pattern, new_load_history + '\\n\\n    def update_balance', content, flags=re.DOTALL)

with open('rhodium_gui_fixed.py', 'w') as f:
    f.write(content)

print("✅ GUI completamente aggiornata!")
