#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from rhodium_wallet import RhodiumWallet
from rhodium_core_hard import RhodiumBlockchain, Transaction  # Usa la versione HARD

class RhodiumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rhodium Wallet")
        self.root.geometry("900x700")
        self.root.configure(bg='#0f0f0f')
        
        self.wallet = RhodiumWallet()
        self.blockchain = RhodiumBlockchain()
        self.mining_thread = None
        self.mining_running = False
        
        self.setup_ui()
        self.update_balance()
        # self.load_transaction_history()
        self.update_halving_info()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0f0f0f')
        style.configure('TLabel', background='#0f0f0f', foreground='#00ff00', font=('Courier', 10))
        style.configure('Treeview', background='#1a1a1a', fieldbackground='#1a1a1a', foreground='white')
        style.configure('Treeview.Heading', background='#333', foreground='#00ff00')

        # Header
        header = tk.Frame(self.root, bg='#0f0f0f')
        header.pack(pady=10)
        tk.Label(header, text="RHODIUM WALLET", font=('Arial', 16, 'bold'), fg='#00ff00', bg='#0f0f0f').pack()

        # Wallet Info
        info_frame = tk.Frame(self.root, bg='#0f0f0f')
        info_frame.pack(pady=10, fill='x', padx=20)
        self.addr_label = tk.Label(info_frame, text="", fg='#00ff88', bg='#0f0f0f', font=('Courier', 11), anchor='w')
        self.addr_label.pack(fill='x')
        self.balance_label = tk.Label(info_frame, text="Balance: 0.000000 RHO", fg='#00ff00', bg='#0f0f0f', font=('Courier', 14, 'bold'))
        self.balance_label.pack(pady=5)

        # Halving Info
        self.halving_label = tk.Label(info_frame, text="", fg='#ffaa00', bg='#0f0f0f', font=('Courier', 10))
        self.halving_label.pack(pady=2)

        # Buttons
        btn_frame = tk.Frame(self.root, bg='#0f0f0f')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Avvia Mining", command=self.start_mining, bg='#00aa00', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Ferma Mining", command=self.stop_mining, bg='#aa0000', fg='white', width=15).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Aggiorna", command=self.refresh_all, bg='#444', fg='white', width=15).pack(side='left', padx=5)

        # Mining Log
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10, fill='both', expand=True, padx=20)
        tk.Label(log_frame, text="Mining Log", fg='#00ff00', bg='#0f0f0f', font=('Arial', 12, 'bold')).pack(anchor='w')
        self.mining_log = scrolledtext.ScrolledText(log_frame, height=12, bg='#000', fg='#00ff00', font=('Courier', 9))
        self.mining_log.pack(fill='both', expand=True, pady=5)

        # Transactions
        tx_frame = tk.Frame(self.root)
        tx_frame.pack(pady=10, fill='both', expand=True, padx=20)
        tk.Label(tx_frame, text="Ultime Transazioni", fg='#00ff00', bg='#0f0f0f', font=('Arial', 12, 'bold')).pack(anchor='w')
        self.transaction_tree = ttk.Treeview(tx_frame, columns=('Type', 'Amount', 'To', 'Date'), show='headings', height=6)
        self.transaction_tree.heading('Type', text='Tipo')
        self.transaction_tree.heading('Amount', text='Importo')
        self.transaction_tree.heading('To', text='A')
        self.transaction_tree.heading('Date', text='Data')
        self.transaction_tree.column('Type', width=80)
        self.transaction_tree.column('Amount', width=120)
        self.transaction_tree.column('To', width=200)
        self.transaction_tree.column('Date', width=120)
        self.transaction_tree.pack(fill='both', expand=True)

    def log(self, text):
        self.root.after(0, lambda: self.mining_log.insert(tk.END, text + "\n"))
        self.root.after(0, lambda: self.mining_log.see(tk.END))

    
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


    def update_halving_info(self):
        info = self.blockchain.get_next_halving_info()
        diff = self.blockchain.current_difficulty
        text = f"Difficulty: {diff} | Reward: {info['current_reward']:.6f} RHO | Halving tra: {info['blocks_remaining']:,} blocchi"
        self.root.after(0, lambda: self.halving_label.config(text=text))

    def load_transaction_history(self):
        transactions = self.blockchain.get_all_transactions_for_address(self.wallet.get_address())
        for i in self.transaction_tree.get_children():
            self.transaction_tree.delete(i)
        for tx in reversed(transactions[-10:]):
            self.transaction_tree.insert('', 'end', values=(
                tx['type'],
                f"{tx['amount']:.6f}",
                tx['address'][:16] + "..." if len(tx['address']) > 16 else tx['address'],
                tx['date']
            ))

    def on_block_mined(self, block):
        self.log(f"BLOCCO MINATO #{block.index}")
        self.log(f"Hash: {block.hash[:20]}...")
        self.log(f"Nonce: {block.nonce:,}")
        self.update_balance()
        self.update_halving_info()
        # self.load_transaction_history()

    def mining_worker(self):
        self.log("Mining avviato...")
        halving_info = self.blockchain.get_next_halving_info()
        self.log(f"Difficulty: {self.blockchain.current_difficulty}")
        self.log(f"Target: {'0' * self.blockchain.current_difficulty}")
        self.log(f"Prossimo halving: {halving_info['blocks_remaining']:,} blocchi")

        while self.mining_running:
            try:
                start_time = time.time()
                self.log(f"\nMining blocco {len(self.blockchain.chain)}...")
                
                block = self.blockchain.mine_block(self.wallet.get_address())
                
                if block:
                    mining_time = time.time() - start_time
                    current_reward = self.blockchain.get_current_reward()
                    
                    self.log(f"Blocco {block.index} minato in {mining_time:.2f}s!")
                    self.log(f"Ricompensa: {current_reward:.6f} RHO")
                    self.log(f"Hash rate: {block.nonce / mining_time:,.0f} H/s")
                    
                    self.root.after(0, self.on_block_mined, block)
                else:
                    self.log("Nessuna transazione da minare")
                
                time.sleep(3)
                
            except Exception as e:
                self.log(f"Errore mining: {e}")
                time.sleep(5)

    def start_mining(self):
        if not self.mining_running:
            self.mining_running = True
            self.mining_thread = threading.Thread(target=self.mining_worker, daemon=True)
            self.mining_thread.start()
            self.log("THREAD MINING AVVIATO")

    def stop_mining(self):
        self.mining_running = False
        self.log("Mining fermato.")

    def refresh_all(self):
        self.update_balance()
        self.update_halving_info()
        # self.load_transaction_history()
        self.log("Dati aggiornati.")

def main():
    root = tk.Tk()
    app = RhodiumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("Avvio Rhodium GUI Wallet...")
    main()
