#!/usr/bin/env python3
import os
import subprocess
import json
from datetime import datetime

def create_github_release():
    """Crea una release su GitHub"""
    version = "1.0.0"
    release_notes = f"""
# 🎉 Rhodium Blockchain v{version}

## Nuove Funzionalità

### ✨ Wallet GUI Completo
- Interfaccia grafica intuitiva per Windows, Mac, Linux
- Mining integrato con un click
- Gestione transazioni e saldo
- Cronologia completa

### 🌐 Rete P2P Decentralizzata  
- Nodi multipli che si sincronizzano automaticamente
- Scoperta automatica dei peer
- Broadcast di blocchi e transazioni
- Resilienza alla rete

### ⛏️ Sistema di Mining
- Proof of Work con difficulty regolabile
- Pool mining collaborativo
- Ricompense di blocco con halving
- Mining sia CPU che (preparato per) GPU

### 💼 Caratteristiche Principali
- Wallet non-custodial
- Transazioni sicure
- Blockchain immutabile
- Smart contract base

## 🚀 Come Iniziare

1. **Scarica** il wallet per la tua piattaforma
2. **Esegui** l'installer
3. **Avvia** il mining
4. **Condividi** il tuo indirizzo per ricevere RHO

## 📋 System Requirements
- Python 3.8+ 
- 100MB spazio disco
- Connessione internet (per P2P)

---

**Data Release**: {datetime.now().strftime('%Y-%m-%d')}
"""

    # Salva le release notes
    with open("RELEASE_NOTES.md", "w") as f:
        f.write(release_notes)
    
    print("✅ Release notes create: RELEASE_NOTES.md")
    
    # Crea tag Git
    subprocess.run(["git", "tag", f"v{version}"])
    subprocess.run(["git", "push", "origin", f"v{version}"])
    
    print(f"✅ Tag v{version} creato e pushato")
    
    # Istruzioni per completare la release
    print(f"""
🎯 PER COMPLETARE LA RELEASE SU GITHUB:

1. Vai su: https://github.com/TUO_USERNAME/rhodium-blockchain/releases/new
2. Tag: v{version}
3. Titolo: Rhodium Blockchain v{version}
4. Descrizione: Copia il contenuto di RELEASE_NOTES.md
5. Allega i file dalla cartella dist/:
   - RhodiumBlockchain-Windows-v{version}.zip
   - RhodiumBlockchain-macOS-v{version}.zip  
   - RhodiumBlockchain-Linux-v{version}.tar.gz
   - RhodiumBlockchain-Source-v{version}.zip
6. Pubblica la release!

I tuoi utenti potranno poi scaricare direttamente i wallet pre-compilati!
""")

if __name__ == "__main__":
    create_github_release()
