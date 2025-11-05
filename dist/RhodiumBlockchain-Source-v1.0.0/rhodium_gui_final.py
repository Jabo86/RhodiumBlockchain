#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from rhodium_wallet import RhodiumWallet
from rhodium_core_hard import RhodiumBlockchain

class RhodiumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🪙 Rhodium Wallet - DIFFICULTY 10")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        self.wallet = RhodiumWallet()
        self.blockchain = RhodiumBlockchain()
        self.mining_thread = None
        self.mining_active = False
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='white', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Treeview', background='#2a2a2a', foreground='white', fieldbackground='#2a2a2a')
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header con info
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=10)
        
        self.balance_label = ttk.Label(header_frame, text="💰 Saldo: 0.000000 RHO", 
                                      font=('Arial', 16, 'bold'), foreground='#00ff00')
        self.balance_label.pack(side=tk.LEFT)
        
        self.address_label = ttk.Label(header_frame, text="👛 Indirizzo: caricamento...", 
                                      font=('Arial', 10), foreground='#cccccc')
        self.address_label.pack(side=tk.RIGHT)
        
        # Info blockchain
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="🎯 Difficulty: 10 | 📦 Blocchi: 0", 
                                   font=('Arial', 10), foreground='#ffaa00')
        self.info_label.pack()
        
        # Mining section
        mining_frame = ttk.LabelFrame(main_frame, text="⛏️ Mining - DIFFICULTY 10 (MOLTO DIFFICILE)", padding="10")
        mining_frame.pack(fill=tk.X, pady=10)
        
        btn_frame = ttk.Frame(mining_frame)
        btn_frame.pack(fill=tk.X)
        
        mining_btn = ttk.Button(btn_frame, text="⛏️ Avvia Mining", command=self.start_mining)
        mining_btn.pack(side=tk.LEFT, padx=5)
        
        stop_btn = ttk.Button(btn_frame, text="⏹️ Ferma Mining", command=self.stop_mining)
        stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.mining_log = scrolledtext.ScrolledText(mining_frame, height=10, bg='#1a1a1a', fg='white', font=('Courier', 9))
        self.mining_log.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Transactions section
        trans_frame = ttk.LabelFrame(main_frame, text="💸 Invia & Ricevi RHO", padding="10")
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Send transaction
        send_frame = ttk.Frame(trans_frame)
        send_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(send_frame, text="A Indirizzo:").pack(side=tk.LEFT)
        self.recipient_entry = ttk.Entry(send_frame, width=50)
        self.recipient_entry.pack(side=tk.LEFT, padx=5)
        self.recipient_entry.insert(0, "jabo86...")
        
        ttk.Label(send_frame, text="Importo RHO:").pack(side=tk.LEFT, padx=(20,0))
        self.amount_entry = ttk.Entry(send_frame, width=15)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        send_btn = ttk.Button(send_frame, text="💸 Invia RHO", command=self.send_transaction)
        send_btn.pack(side=tk.LEFT, padx=10)
        
        # Transaction history
        history_label = ttk.Label(trans_frame, text="📜 Cronologia Transazioni:", font=('Arial', 11, 'bold'))
        history_label.pack(anchor=tk.W, pady=(10,5))
        
        columns = ('Tipo', 'Importo', 'Indirizzo', 'Data')
        self.transaction_tree = ttk.Treeview(trans_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(trans_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def update_display(self):
        """Aggiorna tutto il display"""
        try:
            # Sincronizza wallet
            self.wallet.sync_with_blockchain(self.blockchain)
            
            # Aggiorna saldo
            balance = self.wallet.get_balance()
            self.balance_label.config(text=f"💰 Saldo: {balance:.6f} RHO")
            
            # Aggiorna indirizzo
            self.address_label.config(text=f"👛 Indirizzo: {self.wallet.get_address()}")
            
            # Aggiorna info blockchain
            block_count = len(self.blockchain.chain)
            reward = self.blockchain.get_current_reward()
            self.info_label.config(text=f"🎯 Difficulty: 10 | 📦 Blocchi: {block_count} | 💰 Reward: {reward} RHO")
            
            # Aggiorna cronologia
            self.load_transaction_history()
            
        except Exception as e:
            print(f"❌ Errore aggiornamento: {e}")
    
    def load_transaction_history(self):
        """Carica la cronologia transazioni"""
        try:
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            transactions = self.wallet.get_complete_history(self.blockchain)
            
            for tx in transactions[-15:]:  # Ultime 15 transazioni
                self.transaction_tree.insert('', tk.END, values=(
                    tx.get('type', 'N/A'),
                    f"{tx.get('amount', 0):.8f} RHO",
                    tx.get('address', 'N/A'),
                    tx.get('date', 'N/A')
                ))
                
            if not transactions:
                self.transaction_tree.insert('', tk.END, values=(
                    'MINING', '0.00000000 RHO', 'Fai mining per iniziare!', 'Ora'
                ))
                
        except Exception as e:
            print(f"❌ Errore cronologia: {e}")
    
    def send_transaction(self):
        """Invia RHO"""
        recipient = self.recipient_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not recipient or not amount_str:
            messagebox.showerror("Errore", "Inserisci indirizzo destinatario e importo")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Errore", "L'importo deve essere positivo")
                return
        except:
            messagebox.showerror("Errore", "Importo non valido")
            return
        
        # Invia transazione
        success, message = self.wallet.send_transaction(recipient, amount, self.blockchain)
        
        if success:
            messagebox.showinfo("Successo", message)
            self.recipient_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.update_display()
            self.mining_log.insert(tk.END, f"💸 {message}\\n")
            self.mining_log.see(tk.END)
        else:
            messagebox.showerror("Errore", message)
    
    def start_mining(self):
        """Avvia il mining"""
        if not self.mining_thread or not self.mining_thread.is_alive():
            self.mining_active = True
            self.mining_thread = threading.Thread(target=self.mining_worker, daemon=True)
            self.mining_thread.start()
            self.mining_log.insert(tk.END, "⛏️ AVVIO MINING - Difficulty 10 (MOLTO DIFFICILE)\\n")
            self.mining_log.insert(tk.END, "⚠️  Potrebbero servire diversi minuti...\\n")
            self.mining_log.see(tk.END)
    
    def stop_mining(self):
        """Ferma il mining"""
        self.mining_active = False
        self.mining_log.insert(tk.END, "⏹️ Mining fermato\\n")
        self.mining_log.see(tk.END)
    
    def mining_worker(self):
        """Worker per il mining"""
        while self.mining_active:
            try:
                block = self.blockchain.mine_block(self.wallet.get_address())
                
                if block:
                    reward = self.blockchain.get_current_reward()
                    self.root.after(0, self.mining_log.insert, tk.END, 
                                   f"💰 RICOMPENSA OTTENUTA: {reward:.8f} RHO\\n")
                    self.root.after(0, self.update_display)
                else:
                    self.root.after(0, self.mining_log.insert, tk.END, 
                                   "❌ Mining fallito o interrotto\\n")
                
                self.root.after(0, self.mining_log.see, tk.END)
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, self.mining_log.insert, tk.END, f"❌ Errore: {e}\\n")
                self.root.after(0, self.mining_log.see, tk.END)
                time.sleep(5)

def main():
    root = tk.Tk()
    app = RhodiumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    print("🖥️  Avvio Rhodium Wallet - DIFFICULTY 10")
    print("⚠️   Il mining sarà MOLTO lento e difficile!")
    main()
