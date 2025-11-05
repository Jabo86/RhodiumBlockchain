#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from rhodium_wallet import RhodiumWallet
from rhodium_core import RhodiumBlockchain, Transaction
from rhodium_miner import main as miner_main

class RhodiumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🪙 Rhodium Wallet")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        self.wallet = RhodiumWallet()
        self.blockchain = RhodiumBlockchain()
        self.mining_thread = None
        self.mining_running = False
        
        self.setup_ui()
        self.update_balance()
        
    def setup_ui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Balance.TLabel', font=('Arial', 24, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(header_frame, text="🪙 Rhodium Wallet", style='Header.TLabel').grid(row=0, column=0)
        ttk.Label(header_frame, text=f"Indirizzo: {self.wallet.get_address()}").grid(row=1, column=0, pady=5)
        
        # Balance section
        balance_frame = ttk.LabelFrame(main_frame, text="Balance", padding="10")
        balance_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.balance_label = ttk.Label(balance_frame, text="Caricamento...", style='Balance.TLabel')
        self.balance_label.grid(row=0, column=0)
        
        ttk.Label(balance_frame, text="RHO").grid(row=0, column=1, padx=(10, 0))
        
        # Quick actions
        actions_frame = ttk.LabelFrame(main_frame, text="Azioni Rapide", padding="10")
        actions_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(actions_frame, text="🔄 Aggiorna Balance", 
                  command=self.update_balance).grid(row=0, column=0, padx=5)
        ttk.Button(actions_frame, text="📋 Copia Indirizzo", 
                  command=self.copy_address).grid(row=0, column=1, padx=5)
        ttk.Button(actions_frame, text="🌐 Explorer", 
                  command=self.open_explorer).grid(row=0, column=2, padx=5)
        
        # Send section
        send_frame = ttk.LabelFrame(main_frame, text="Invia RHO", padding="10")
        send_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(send_frame, text="A:").grid(row=0, column=0, sticky=tk.W)
        self.recipient_entry = ttk.Entry(send_frame, width=40)
        self.recipient_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        ttk.Label(send_frame, text="Importo:").grid(row=1, column=0, sticky=tk.W)
        self.amount_entry = ttk.Entry(send_frame, width=15)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        ttk.Label(send_frame, text="RHO").grid(row=1, column=2, sticky=tk.W)
        
        ttk.Button(send_frame, text="🚀 Invia", 
                  command=self.send_transaction).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Mining section
        mining_frame = ttk.LabelFrame(main_frame, text="Mining", padding="10")
        mining_frame.grid(row=1, column=1, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        self.mining_status = ttk.Label(mining_frame, text="⏸️ Mining Fermo")
        self.mining_status.grid(row=0, column=0, columnspan=2)
        
        self.mining_button = ttk.Button(mining_frame, text="⛏️ Avvia Mining", 
                                       command=self.toggle_mining)
        self.mining_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.mining_log = scrolledtext.ScrolledText(mining_frame, width=40, height=15, 
                                                   bg='#2d2d2d', fg='white', font=('Consolas', 8))
        self.mining_log.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Transaction history
        history_frame = ttk.LabelFrame(main_frame, text="Ultime Transazioni", padding="10")
        history_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.transaction_tree = ttk.Treeview(history_frame, columns=('Type', 'Amount', 'Address', 'Date'), 
                                           show='headings', height=6)
        self.transaction_tree.heading('Type', text='Tipo')
        self.transaction_tree.heading('Amount', text='Importo')
        self.transaction_tree.heading('Address', text='Indirizzo')
        self.transaction_tree.heading('Date', text='Data')
        
        self.transaction_tree.column('Type', width=80)
        self.transaction_tree.column('Amount', width=100)
        self.transaction_tree.column('Address', width=200)
        self.transaction_tree.column('Date', width=150)
        
        self.transaction_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Start balance update loop
        self.auto_update_balance()
        
    def update_balance(self):
        try:
            balance = self.blockchain.get_balance(self.wallet.get_address())
            self.balance_label.config(text=f"{balance:,.6f}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore aggiornamento balance: {e}")
    
    def auto_update_balance(self):
        self.update_balance()
        self.root.after(30000, self.auto_update_balance)  # Update every 30 seconds
    
    def copy_address(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.wallet.get_address())
        messagebox.showinfo("Successo", "Indirizzo copiato negli appunti!")
    
    def open_explorer(self):
        import webbrowser
        webbrowser.open("http://localhost:5000")
    
    def send_transaction(self):
        recipient = self.recipient_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not recipient:
            messagebox.showerror("Errore", "Inserisci l'indirizzo del destinatario")
            return
        
        if not recipient.startswith('jabo86'):
            messagebox.showerror("Errore", "Indirizzo non valido. Deve iniziare con 'jabo86'")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Errore", "L'importo deve essere positivo")
                return
        except ValueError:
            messagebox.showerror("Errore", "Importo non valido")
            return
        
        balance = self.blockchain.get_balance(self.wallet.get_address())
        if amount + 0.001 > balance:  # Include fee
            messagebox.showerror("Errore", f"Fondi insufficienti. Balance: {balance:.6f} RHO")
            return
        
        # Create transaction
        try:
            tx = Transaction(self.wallet.get_address(), recipient, amount, 0.001)
            if self.blockchain.add_transaction(tx):
                messagebox.showinfo("Successo", 
                                  f"Transazione creata!\n"
                                  f"A: {recipient}\n"
                                  f"Importo: {amount} RHO\n"
                                  f"Fee: 0.001 RHO\n\n"
                                  f"In attesa di essere minata...")
                self.recipient_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.update_balance()
            else:
                messagebox.showerror("Errore", "Errore creazione transazione")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore: {e}")
    
    def toggle_mining(self):
        if not self.mining_running:
            self.start_mining()
        else:
            self.stop_mining()
    
    def start_mining(self):
        self.mining_running = True
        self.mining_status.config(text="⛏️ Mining Attivo")
        self.mining_button.config(text="⏸️ Ferma Mining")
        self.mining_log.insert(tk.END, "🚀 Avvio mining...\n")
        self.mining_log.see(tk.END)
        
        self.mining_thread = threading.Thread(target=self.mining_worker, daemon=True)
        self.mining_thread.start()
    
    def stop_mining(self):
        self.mining_running = False
        self.mining_status.config(text="⏸️ Mining Fermo")
        self.mining_button.config(text="⛏️ Avvia Mining")
        self.mining_log.insert(tk.END, "🛑 Mining fermato\n")
        self.mining_log.see(tk.END)
    
    def mining_worker(self):
        while self.mining_running:
            try:
                # Mine one block
                block = self.blockchain.mine_block(self.wallet.get_address())
                if block:
                    self.root.after(0, self.on_block_mined, block)
                else:
                    self.root.after(0, self.mining_log.insert, tk.END, "❌ Nessuna transazione da minare\n")
                    self.root.after(0, self.mining_log.see, tk.END)
                
                time.sleep(2)  # Wait before next attempt
                
            except Exception as e:
                self.root.after(0, self.mining_log.insert, tk.END, f"❌ Errore mining: {e}\n")
                self.root.after(0, self.mining_log.see, tk.END)
                time.sleep(5)
    
    def on_block_mined(self, block):
        self.mining_log.insert(tk.END, f"✅ Blocco #{block.index} minato!\n")
        self.mining_log.insert(tk.END, f"   💰 Reward: {self.blockchain.get_current_reward()} RHO\n")
        self.mining_log.insert(tk.END, f"   🔗 Hash: {block.hash[:20]}...\n")
        self.mining_log.see(tk.END)
        self.update_balance()
        self.load_transaction_history()

    def load_transaction_history(self):
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        # Load transactions involving this wallet
        address = self.wallet.get_address()
        transactions = []
        
        for block in self.blockchain.chain:
            for tx in block.transactions:
                if tx.sender == address or tx.recipient == address:
                    tx_type = "Inviato" if tx.sender == address else "Ricevuto"
                    other_address = tx.recipient if tx.sender == address else tx.sender
                    if other_address == "0":
                        tx_type = "Mining Reward"
                        other_address = "Sistema"
                    
                    transactions.append({
                        'type': tx_type,
                        'amount': tx.amount,
                        'address': other_address,
                        'date': time.strftime('%Y-%m-%d %H:%M', time.localtime(tx.timestamp))
                    })
        
        # Add to treeview (most recent first)
        for tx in reversed(transactions[-10:]):  # Last 10 transactions
            self.transaction_tree.insert('', tk.END, values=(
                tx['type'], 
                f"{tx['amount']:.6f} RHO", 
                tx['address'], 
                tx['date']
            ))

def main():
    root = tk.Tk()
    app = RhodiumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("🖥️  Avvio Rhodium GUI Wallet...")
    main()
