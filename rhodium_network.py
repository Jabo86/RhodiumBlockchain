import socket
import threading
import time
import json
from typing import List, Dict

class RhodiumNetwork:
    def __init__(self, host='localhost', port=8333):
        self.host = host
        self.port = port
        self.peers: List[str] = []
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """Avvia il server P2P"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"🌐 Nodo P2P avviato su {self.host}:{self.port}")
            
            # Thread per accettare connessioni
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
        except Exception as e:
            print(f"❌ Errore avvio server: {e}")
    
    def accept_connections(self):
        """Accetta connessioni in entrata"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"🔗 Nuova connessione da {address}")
                
                # Gestisci il peer in un thread separato
                peer_thread = threading.Thread(
                    target=self.handle_peer, 
                    args=(client_socket, address)
                )
                peer_thread.daemon = True
                peer_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"❌ Errore accettazione connessione: {e}")
    
    def handle_peer(self, client_socket, address):
        """Gestisce la comunicazione con un peer"""
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                self.process_message(data, address)
                
        except Exception as e:
            print(f"❌ Errore gestione peer {address}: {e}")
        finally:
            client_socket.close()
    
    def connect_to_peer(self, peer_host, peer_port):
        """Connetti a un peer"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            
            # Aggiungi alla lista peers
            peer_addr = f"{peer_host}:{peer_port}"
            if peer_addr not in self.peers:
                self.peers.append(peer_addr)
                print(f"✅ Connesso a peer: {peer_addr}")
            
            # Thread per ascoltare il peer
            peer_thread = threading.Thread(
                target=self.handle_peer,
                args=(peer_socket, (peer_host, peer_port))
            )
            peer_thread.daemon = True
            peer_thread.start()
            
        except Exception as e:
            print(f"❌ Errore connessione a {peer_host}:{peer_port}: {e}")
    
    def process_message(self, message: str, address):
        """Processa i messaggi ricevuti"""
        try:
            data = json.loads(message)
            msg_type = data.get('type')
            
            if msg_type == 'new_block':
                print(f"📦 Nuovo blocco ricevuto da {address}")
                # TODO: Validare e aggiungere alla blockchain
                
            elif msg_type == 'new_transaction':
                print(f"💸 Nuova transazione ricevuta da {address}")
                # TODO: Aggiungere alla pool transazioni
                
            elif msg_type == 'peer_list':
                peers = data.get('peers', [])
                self.add_peers(peers)
                
        except json.JSONDecodeError:
            print(f"❌ Messaggio non valido da {address}")
    
    def add_peers(self, new_peers: List[str]):
        """Aggiungi nuovi peers alla lista"""
        for peer in new_peers:
            if peer not in self.peers:
                self.peers.append(peer)
                print(f"➕ Nuovo peer aggiunto: {peer}")
    
    def broadcast_message(self, message: dict):
        """Invia un messaggio a tutti i peers"""
        for peer in self.peers[:]:  # Copia della lista
            try:
                host, port = peer.split(':')
                self.send_message_to_peer(host, int(port), message)
            except Exception as e:
                print(f"❌ Errore broadcast a {peer}: {e}")
                self.peers.remove(peer)
    
    def send_message_to_peer(self, host: str, port: int, message: dict):
        """Invia messaggio a un peer specifico"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((host, port))
            peer_socket.send(json.dumps(message).encode('utf-8'))
            peer_socket.close()
        except Exception as e:
            print(f"❌ Errore invio a {host}:{port}: {e}")
    
    def stop(self):
        """Ferma il network"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("🛑 Network P2P fermato")

if __name__ == "__main__":
    network = RhodiumNetwork()
    network.start_server()
    
    # Esempio: connetti a qualche peer
    # network.connect_to_peer('localhost', 8334)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        network.stop()
