#!/usr/bin/env python3
"""
Script di installazione automatica per Rhodium Blockchain
"""
import os
import sys
import subprocess
import platform

def check_python():
    """Verifica che Python 3.8+ sia installato"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ è richiesto")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} trovato")
        return True
    except Exception as e:
        print(f"❌ Errore verifica Python: {e}")
        return False

def install_dependencies():
    """Installa le dipendenze Python"""
    try:
        print("📦 Installazione dipendenze...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dipendenze installate con successo")
        return True
    except Exception as e:
        print(f"❌ Errore installazione dipendenze: {e}")
        return False

def create_desktop_shortcut():
    """Crea scorciatoia desktop (Windows/macOS)"""
    system = platform.system()
    
    if system == "Windows":
        # Crea file .bat per Windows
        with open("RhodiumWallet.bat", "w") as f:
            f.write('@echo off\n')
            f.write('echo Starting Rhodium Wallet...\n')
            f.write('python rhodium_gui_perfetta.py\n')
            f.write('pause\n')
        print("✅ Scorciatoia Windows creata: RhodiumWallet.bat")
    
    elif system == "Darwin":  # macOS
        # Crea file .command per macOS
        with open("RhodiumWallet.command", "w") as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting Rhodium Wallet..."\n')
            f.write('cd "$(dirname "$0")"\n')
            f.write('python3 rhodium_gui_perfetta.py\n')
        os.chmod("RhodiumWallet.command", 0o755)
        print("✅ Scorciatoia macOS creata: RhodiumWallet.command")
    
    elif system == "Linux":
        # Crea file .sh per Linux
        with open("rhodium-wallet.sh", "w") as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Starting Rhodium Wallet..."\n')
            f.write('cd "$(dirname "$0")"\n')
            f.write('python3 rhodium_gui_perfetta.py\n')
        os.chmod("rhodium-wallet.sh", 0o755)
        print("✅ Scorciatoia Linux creata: rhodium-wallet.sh")

def main():
    print("🚀 Installazione Rhodium Blockchain")
    print("====================================")
    
    if not check_python():
        sys.exit(1)
    
    if not install_dependencies():
        print("⚠️  Proseguo senza alcune dipendenze...")
    
    create_desktop_shortcut()
    
    print("\\n🎉 Installazione completata!")
    print("\\nOra puoi:")
    print("1. Eseguire il wallet GUI")
    print("2. Iniziare a minare RHO")
    print("3. Unirti alla rete P2P")
    print("\\nPer avviare il wallet:")
    
    system = platform.system()
    if system == "Windows":
        print("   Esegui: RhodiumWallet.bat")
    elif system == "Darwin":
        print("   Esegui: ./RhodiumWallet.command")
    elif system == "Linux":
        print("   Esegui: ./rhodium-wallet.sh")
    else:
        print("   Esegui: python rhodium_gui_perfetta.py")

if __name__ == "__main__":
    main()
