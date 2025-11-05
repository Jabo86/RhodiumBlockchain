import socket
import threading
import time
import json
import pickle
from typing import List, Dict, Set
from rhodium_core_hard import RhodiumBlockchain, Block, Transaction

class RhodiumP2PNode:
    def __init__(self, host='localhost', port=8333, bootstrap_nodes=None):
        self.host = host
        self.port = port
        self.bootstrap_nodes = bootstrap_nodes or []
        self.peers: Set[str] = set()
        self.server_socket = None
        self.running = False
        self.blockchain = RhodiumBlockchain()
        self.known_transactions: Set[str] = set()
        
        print(f"🔄 Inizializzazione nodo P2P su {host}:{port}")
        
    def start(self):
        """Avvia il nodo P2P"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            self.running = True
            
            print(f"🌐 Nodo P2P avviato su {self.host}:{self.port}")
            
            # Thread per accettare connessioni
            accept_thread = threading.Thread(target=self._accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Thread per connettersi a bootstrap nodes
            if self.bootstrap_nodes:
                bootstrap_thread = threading.Thread(target=self._connect_to_bootstrap)
                bootstrap_thread.daemon = True
                bootstrap_thread.start()
            
            # Thread per sync automatico
            sync_thread = threading.Thread(target=self._auto_sync)
            sync_thread.daemon = True
            sync_thread.start()
            
        except Exception as e:
            print(f"❌ Errore avvio nodo P2P: {e}")
    
    def _accept_connections(self):
        """Accetta connessioni in entrata"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                peer_addr = f"{address[0]}:{address[1]}"
                
                print(f"🔗 Connessione accettata da {peer_addr}")
                
                # Aggiungi ai peers
                self.peers.add(peer_addr)
                
                # Gestisci il peer
                peer_thread = threading.Thread(
                    target=self._handle_peer_connection,
                    args=(client_socket, peer_addr)
                )
                peer_thread.daemon = True
                peer_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"❌ Errore accettazione connessione: {e}")
    
    def _handle_peer_connection(self, client_socket, peer_addr):
        """Gestisce una connessione peer"""
        try:
            while self.running:
                # Ricevi la lunghezza del messaggio
                length_data = client_socket.recv(4)
                if not length_data:
                    break
                    
                message_length = int.from_bytes(length_data, 'big')
                
                # Ricevi il messaggio
                message_data = b''
                while len(message_data) < message_length:
                    chunk = client_socket.recv(min(4096, message_length - len(message_data)))
                    if not chunk:
                        break
                    message_data += chunk
                
                if message_data:
                    self._process_message(message_data, peer_addr)
                    
        except Exception as e:
            print(f"❌ Errore gestione peer {peer_addr}: {e}")
        finally:
            client_socket.close()
            if peer_addr in self.peers:
                self.peers.remove(peer_addr)
            print(f"🔌 Disconnesso da {peer_addr}")
    
    def _process_message(self, message_data: bytes, peer_addr: str):
        """Processa un messaggio ricevuto"""
        try:
            message = pickle.loads(message_data)
            msg_type = message.get('type')
            
            if msg_type == 'hello':
                print(f"👋 Hello ricevuto da {peer_addr}")
                self._send_peer_list(peer_addr)
                
            elif msg_type == 'peer_list':
                peers = message.get('peers', [])
                self._add_new_peers(peers)
                
            elif msg_type == 'new_block':
                block_data = message.get('block')
                block = Block(
                    block_data['index'],
                    [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block_data['transactions']],
                    block_data['timestamp'],
                    block_data['previous_hash'],
                    block_data['difficulty']
                )
                block.nonce = block_data['nonce']
                block.hash = block_data['hash']
                
                if self._validate_and_add_block(block):
                    print(f"📦 Blocco {block.index} aggiunto da {peer_addr}")
                    # Propaga agli altri peers
                    self.broadcast_message(message)
                
            elif msg_type == 'new_transaction':
                tx_data = message.get('transaction')
                tx = Transaction(tx_data['sender'], tx_data['recipient'], tx_data['amount'])
                tx.timestamp = tx_data['timestamp']
                tx.signature = tx_data['signature']
                
                tx_hash = self._get_transaction_hash(tx)
                if tx_hash not in self.known_transactions:
                    if self.blockchain.add_transaction(tx):
                        self.known_transactions.add(tx_hash)
                        print(f"💸 Transazione aggiunta da {peer_addr}")
                        # Propaga agli altri peers
                        self.broadcast_message(message)
                
            elif msg_type == 'blockchain_request':
                # Invia l'intera blockchain al peer
                self._send_blockchain(peer_addr)
                
        except Exception as e:
            print(f"❌ Errore processamento messaggio da {peer_addr}: {e}")
    
    def _connect_to_bootstrap(self):
        """Connetti ai bootstrap nodes"""
        time.sleep(2)  # Aspetta che il server sia avviato
        
        for bootstrap_node in self.bootstrap_nodes:
            try:
                host, port = bootstrap_node.split(':')
                self.connect_to_peer(host, int(port))
            except Exception as e:
                print(f"❌ Errore connessione bootstrap {bootstrap_node}: {e}")
    
    def connect_to_peer(self, host: str, port: int):
        """Connetti a un peer specifico"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((host, port))
            
            peer_addr = f"{host}:{port}"
            self.peers.add(peer_addr)
            
            # Invia messaggio hello
            hello_message = {'type': 'hello', 'node': f"{self.host}:{self.port}"}
            self._send_to_socket(peer_socket, hello_message)
            
            # Thread per ascoltare il peer
            peer_thread = threading.Thread(
                target=self._handle_peer_connection,
                args=(peer_socket, peer_addr)
            )
            peer_thread.daemon = True
            peer_thread.start()
            
            print(f"✅ Connesso a peer: {peer_addr}")
            
        except Exception as e:
            print(f"❌ Errore connessione a {host}:{port}: {e}")
    
    def _send_to_socket(self, sock: socket.socket, message: dict):
        """Invia messaggio a un socket"""
        try:
            message_data = pickle.dumps(message)
            message_length = len(message_data).to_bytes(4, 'big')
            sock.send(message_length + message_data)
        except Exception as e:
            print(f"❌ Errore invio messaggio: {e}")
    
    def broadcast_message(self, message: dict):
        """Invia un messaggio a tutti i peers"""
        for peer_addr in list(self.peers):
            try:
                host, port = peer_addr.split(':')
                self.send_message_to_peer(host, int(port), message)
            except Exception as e:
                print(f"❌ Errore broadcast a {peer_addr}: {e}")
                self.peers.remove(peer_addr)
    
    def send_message_to_peer(self, host: str, port: int, message: dict):
        """Invia messaggio a un peer specifico"""
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.settimeout(5)
            peer_socket.connect((host, port))
            self._send_to_socket(peer_socket, message)
            peer_socket.close()
        except Exception as e:
            print(f"❌ Errore invio a {host}:{port}: {e}")
    
    def _send_peer_list(self, peer_addr: str):
        """Invia la lista dei peers a un peer"""
        message = {
            'type': 'peer_list',
            'peers': list(self.peers)
        }
        host, port = peer_addr.split(':')
        self.send_message_to_peer(host, int(port), message)
    
    def _send_blockchain(self, peer_addr: str):
        """Invia l'intera blockchain a un peer"""
        blockchain_data = []
        for block in self.blockchain.chain:
            block_data = {
                'index': block.index,
                'transactions': [
                    {
                        'sender': tx.sender,
                        'recipient': tx.recipient,
                        'amount': tx.amount,
                        'timestamp': tx.timestamp,
                        'signature': tx.signature
                    } for tx in block.transactions
                ],
                'timestamp': block.timestamp,
                'previous_hash': block.previous_hash,
                'nonce': block.nonce,
                'hash': block.hash,
                'difficulty': block.difficulty
            }
            blockchain_data.append(block_data)
        
        message = {
            'type': 'blockchain_sync',
            'blocks': blockchain_data
        }
        
        host, port = peer_addr.split(':')
        self.send_message_to_peer(host, int(port), message)
    
    def _add_new_peers(self, new_peers: List[str]):
        """Aggiungi nuovi peers"""
        for peer in new_peers:
            if peer != f"{self.host}:{self.port}" and peer not in self.peers:
                self.peers.add(peer)
                print(f"➕ Nuovo peer scoperto: {peer}")
    
    def _validate_and_add_block(self, block: Block) -> bool:
        """Valida e aggiunge un blocco alla blockchain"""
        # Verifica hash del blocco
        if block.hash != block.calculate_hash():
            print(f"❌ Hash del blocco non valido")
            return False
        
        # Verifica Proof of Work
        if block.hash[:block.difficulty] != "0" * block.difficulty:
            print(f"❌ Proof of Work non valida")
            return False
        
        # Verifica chain linkage
        if block.index > 0:
            previous_block = self.blockchain.chain[block.index - 1]
            if block.previous_hash != previous_block.hash:
                print(f"❌ Linkage con blocco precedente non valido")
                return False
        
        # Aggiungi il blocco se non esiste già
        if block.index == len(self.blockchain.chain):
            self.blockchain.chain.append(block)
            self.blockchain.save_chain()
            print(f"✅ Blocco {block.index} aggiunto alla blockchain")
            return True
        
        return False
    
    def _get_transaction_hash(self, tx: Transaction) -> str:
        """Calcola l'hash di una transazione"""
        tx_data = f"{tx.sender}{tx.recipient}{tx.amount}{tx.timestamp}"
        return hashlib.sha256(tx_data.encode()).hexdigest()
    
    def _auto_sync(self):
        """Sincronizzazione automatica periodica"""
        while self.running:
            time.sleep(30)  # Sync ogni 30 secondi
            
            if self.peers:
                # Richiedi blockchain aggiornata a un peer casuale
                random_peer = list(self.peers)[0]
                host, port = random_peer.split(':')
                self.send_message_to_peer(host, int(port), {'type': 'blockchain_request'})
    
    def broadcast_new_block(self, block: Block):
        """Propaga un nuovo blocco alla rete"""
        block_data = {
            'index': block.index,
            'transactions': [
                {
                    'sender': tx.sender,
                    'recipient': tx.recipient,
                    'amount': tx.amount,
                    'timestamp': tx.timestamp,
                    'signature': tx.signature
                } for tx in block.transactions
            ],
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash,
            'difficulty': block.difficulty
        }
        
        message = {
            'type': 'new_block',
            'block': block_data
        }
        
        self.broadcast_message(message)
        print(f"📤 Blocco {block.index} propagato alla rete")
    
    def broadcast_new_transaction(self, transaction: Transaction):
        """Propaga una nuova transazione alla rete"""
        tx_data = {
            'sender': transaction.sender,
            'recipient': transaction.recipient,
            'amount': transaction.amount,
            'timestamp': transaction.timestamp,
            'signature': transaction.signature
        }
        
        message = {
            'type': 'new_transaction',
            'transaction': tx_data
        }
        
        self.broadcast_message(message)
        print(f"📤 Transazione propagata alla rete")
    
    def stop(self):
        """Ferma il nodo P2P"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("🛑 Nodo P2P fermato")

# Esempio di utilizzo
if __name__ == "__main__":
    # Nodo 1 (porta 8333)
    node1 = RhodiumP2PNode(port=8333)
    node1.start()
    
    # Nodo 2 (porta 8334) che si connette al nodo 1
    time.sleep(2)
    node2 = RhodiumP2PNode(port=8334, bootstrap_nodes=['localhost:8333'])
    node2.start()
    
    # Nodo 3 (porta 8335) che si connette al nodo 1
    time.sleep(3)
    node3 = RhodiumP2PNode(port=8335, bootstrap_nodes=['localhost:8333'])
    node3.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node1.stop()
        node2.stop()
        node3.stop()
