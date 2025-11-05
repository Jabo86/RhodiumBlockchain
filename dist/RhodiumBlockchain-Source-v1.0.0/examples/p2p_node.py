#!/usr/bin/env python3
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
