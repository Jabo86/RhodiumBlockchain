#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

class DistributionBuilder:
    def __init__(self):
        self.project_name = "RhodiumBlockchain"
        self.version = "1.0.0"
        self.files_to_include = [
            "rhodium_gui_perfetta.py",
            "rhodium_wallet.py", 
            "rhodium_core_hard.py",
            "rhodium_p2p_network.py",
            "mining_pool.py",
            "smart_contracts.py",
            "requirements.txt",
            "README.md",
            "LICENSE"
        ]
        
    def build_all(self):
        """Crea distribuzioni per tutte le piattaforme"""
        print("🚀 Creando distribuzioni Rhodium Blockchain...")
        
        # Crea directory dist
        os.makedirs("dist", exist_ok=True)
        
        # Build per piattaforma corrente
        current_platform = platform.system()
        
        if current_platform == "Windows":
            self.build_windows()
        elif current_platform == "Darwin":  # macOS
            self.build_macos()
        elif current_platform == "Linux":
            self.build_linux()
        else:
            print(f"❌ Piattaforma non supportata: {current_platform}")
            
        # Crea sempre la distribuzione sorgente
        self.build_source()
        
        print("🎉 Distribuzioni completate!")
    
    def build_windows(self):
        """Crea distribuzione per Windows"""
        print("🔨 Creando distribuzione Windows...")
        
        win_dir = f"dist/{self.project_name}-Windows-v{self.version}"
        os.makedirs(win_dir, exist_ok=True)
        
        # Copia tutti i file
        for file in self.files_to_include:
            if os.path.exists(file):
                shutil.copy2(file, win_dir)
        
        # Rinomina il file GUI principale
        if os.path.exists(f"{win_dir}/rhodium_gui_perfetta.py"):
            os.rename(f"{win_dir}/rhodium_gui_perfetta.py", f"{win_dir}/rhodium_gui.py")
        
        # Crea script di avvio
        with open(f"{win_dir}/Start-Wallet.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting Rhodium Wallet...\n")
            f.write("echo.\n")
            f.write("python rhodium_gui.py\n")
            f.write("pause\n")
        
        # Crea script di installazione
        with open(f"{win_dir}/INSTALL.txt", "w") as f:
            f.write("Rhodium Blockchain - Installazione Windows\n")
            f.write("==========================================\n\n")
            f.write("1. Assicurati di avere Python 3.8+ installato\n")
            f.write("2. Installa le dipendenze: pip install -r requirements.txt\n")
            f.write("3. Esegui 'Start-Wallet.bat' per avviare il wallet\n")
            f.write("4. Inizia a minare! ⛏️\n\n")
            f.write("Per mining avanzato:\n")
            f.write("python mining_pool.py\n")
            f.write("python rhodium_p2p_network.py\n")
        
        print(f"✅ Distribuzione Windows creata: {win_dir}")
    
    def build_macos(self):
        """Crea distribuzione per macOS"""
        print("🔨 Creando distribuzione macOS...")
        
        mac_dir = f"dist/{self.project_name}-macOS-v{self.version}"
        os.makedirs(mac_dir, exist_ok=True)
        
        # Copia tutti i file
        for file in self.files_to_include:
            if os.path.exists(file):
                shutil.copy2(file, mac_dir)
        
        # Rinomina il file GUI principale
        if os.path.exists(f"{mac_dir}/rhodium_gui_perfetta.py"):
            os.rename(f"{mac_dir}/rhodium_gui_perfetta.py", f"{mac_dir}/rhodium_gui.py")
        
        # Crea script di avvio
        with open(f"{mac_dir}/Start-Wallet.command", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting Rhodium Wallet...'\n")
            f.write("cd \"$(dirname \"$0\")\"\n")
            f.write("python3 rhodium_gui.py\n")
        
        # Rendilo eseguibile
        os.chmod(f"{mac_dir}/Start-Wallet.command", 0o755)
        
        # Crea script di installazione
        with open(f"{mac_dir}/INSTALL.txt", "w") as f:
            f.write("Rhodium Blockchain - Installazione macOS\n")
            f.write("========================================\n\n")
            f.write("1. Assicurati di avere Python 3.8+ installato\n")
            f.write("   (brew install python3 oppure da python.org)\n")
            f.write("2. Installa le dipendenze: pip3 install -r requirements.txt\n")
            f.write("3. Esegui 'Start-Wallet.command' per avviare il wallet\n")
            f.write("4. Inizia a minare! ⛏️\n\n")
            f.write("Per mining avanzato:\n")
            f.write("python3 mining_pool.py\n")
            f.write("python3 rhodium_p2p_network.py\n")
        
        print(f"✅ Distribuzione macOS creata: {mac_dir}")
    
    def build_linux(self):
        """Crea distribuzione per Linux"""
        print("🔨 Creando distribuzione Linux...")
        
        linux_dir = f"dist/{self.project_name}-Linux-v{self.version}"
        os.makedirs(linux_dir, exist_ok=True)
        
        # Copia tutti i file
        for file in self.files_to_include:
            if os.path.exists(file):
                shutil.copy2(file, linux_dir)
        
        # Rinomina il file GUI principale
        if os.path.exists(f"{linux_dir}/rhodium_gui_perfetta.py"):
            os.rename(f"{linux_dir}/rhodium_gui_perfetta.py", f"{linux_dir}/rhodium_gui.py")
        
        # Crea script di avvio
        with open(f"{linux_dir}/start-wallet.sh", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("echo 'Starting Rhodium Wallet...'\n")
            f.write("cd \"$(dirname \"$0\")\"\n")
            f.write("python3 rhodium_gui.py\n")
        
        # Rendilo eseguibile
        os.chmod(f"{linux_dir}/start-wallet.sh", 0o755)
        
        # Crea script di installazione
        with open(f"{linux_dir}/INSTALL.txt", "w") as f:
            f.write("Rhodium Blockchain - Installazione Linux\n")
            f.write("========================================\n\n")
            f.write("1. Assicurati di avere Python 3.8+ installato\n")
            f.write("   (sudo apt install python3 python3-pip)\n")
            f.write("2. Installa le dipendenze: pip3 install -r requirements.txt\n")
            f.write("3. Esegui './start-wallet.sh' per avviare il wallet\n")
            f.write("4. Inizia a minare! ⛏️\n\n")
            f.write("Per mining avanzato:\n")
            f.write("python3 mining_pool.py\n")
            f.write("python3 rhodium_p2p_network.py\n")
        
        print(f"✅ Distribuzione Linux creata: {linux_dir}")
    
    def build_source(self):
        """Crea distribuzione sorgente completa"""
        print("📦 Creando distribuzione sorgente...")
        
        source_dir = f"dist/{self.project_name}-Source-v{self.version}"
        os.makedirs(source_dir, exist_ok=True)
        
        # Copia tutti i file Python
        python_files = [f for f in os.listdir('.') if f.endswith('.py')]
        for file in python_files:
            shutil.copy2(file, source_dir)
        
        # Copia file di documentazione
        docs_files = ['README.md', 'requirements.txt', 'LICENSE']
        for file in docs_files:
            if os.path.exists(file):
                shutil.copy2(file, source_dir)
        
        # Crea esempi directory
        examples_dir = f"{source_dir}/examples"
        os.makedirs(examples_dir, exist_ok=True)
        
        # Crea file di esempio
        with open(f"{examples_dir}/simple_miner.py", "w") as f:
            f.write('''#!/usr/bin/env python3
"""
Esempio di miner semplice per Rhodium Blockchain
"""
from rhodium_core_hard import RhodiumBlockchain
from rhodium_wallet import RhodiumWallet
import time

def simple_miner():
    print("⛏️  Simple Miner Avviato")
    
    wallet = RhodiumWallet()
    blockchain = RhodiumBlockchain()
    
    print(f"👛 Indirizzo: {wallet.get_address()}")
    print(f"📦 Altezza blockchain: {len(blockchain.chain)}")
    
    while True:
        print(f"\\n🎯 Minando blocco {len(blockchain.chain)}...")
        start_time = time.time()
        
        block = blockchain.mine_block(wallet.get_address())
        
        if block:
            mining_time = time.time() - start_time
            print(f"✅ Blocco minato in {mining_time:.2f}s")
            print(f"💰 Ricompensa: {blockchain.get_current_reward()} RHO")
        else:
            print("❌ Mining fallito")
        
        time.sleep(10)

if __name__ == "__main__":
    simple_miner()
''')
        
        with open(f"{examples_dir}/p2p_node.py", "w") as f:
            f.write('''#!/usr/bin/env python3
"""
Esempio di nodo P2P per Rhodium Blockchain
"""
from rhodium_p2p_network import RhodiumP2PNode
import time

def start_p2p_node():
    print("🌐 Avvio nodo P2P...")
    
    # Configura il nodo
    node = RhodiumP2PNode(
        host="0.0.0.0",
        port=8333,
        bootstrap_nodes=["localhost:8334"]  # Connetti ad altri nodi
    )
    
    node.start()
    
    print("✅ Nodo P2P avviato. Premi Ctrl+C per fermare.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()
        print("🛑 Nodo P2P fermato")

if __name__ == "__main__":
    start_p2p_node()
''')
        
        print(f"✅ Distribuzione sorgente creata: {source_dir}")

if __name__ == "__main__":
    builder = DistributionBuilder()
    builder.build_all()
