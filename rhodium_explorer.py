#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import json
import os
from rhodium_core import RhodiumBlockchain

app = Flask(__name__)
blockchain = RhodiumBlockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/blocks')
def get_blocks():
    blocks_data = []
    for block in blockchain.chain:
        blocks_data.append({
            'index': block.index,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'transactions': len(block.transactions),
            'miner': block.miner,
            'nonce': block.nonce
        })
    return jsonify(blocks_data)

@app.route('/api/block/<int:block_index>')
def get_block(block_index):
    if 0 <= block_index < len(blockchain.chain):
        block = blockchain.chain[block_index]
        return jsonify(block.to_dict())
    return jsonify({'error': 'Block not found'}), 404

@app.route('/api/transactions')
def get_transactions():
    all_transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            tx_data = tx.to_dict()
            tx_data['block_index'] = block.index
            tx_data['block_hash'] = block.hash
            all_transactions.append(tx_data)
    return jsonify(all_transactions)

@app.route('/api/transaction/<txid>')
def get_transaction(txid):
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.txid == txid:
                tx_data = tx.to_dict()
                tx_data['block_index'] = block.index
                tx_data['block_hash'] = block.hash
                return jsonify(tx_data)
    return jsonify({'error': 'Transaction not found'}), 404

@app.route('/api/address/<address>')
def get_address(address):
    balance = blockchain.get_balance(address)
    transactions = []
    
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.sender == address or tx.recipient == address:
                tx_data = tx.to_dict()
                tx_data['block_index'] = block.index
                tx_data['type'] = 'sent' if tx.sender == address else 'received'
                transactions.append(tx_data)
    
    return jsonify({
        'address': address,
        'balance': balance,
        'transactions': transactions,
        'transaction_count': len(transactions)
    })

@app.route('/api/network')
def get_network_info():
    latest_block = blockchain.get_latest_block()
    difficulty = blockchain.bits_to_difficulty(latest_block.bits) if latest_block else 1
    
    return jsonify({
        'block_count': len(blockchain.chain),
        'total_mined': blockchain.total_mined,
        'difficulty': difficulty,
        'pending_transactions': len(blockchain.pending_transactions),
        'current_reward': blockchain.get_current_reward(),
        'max_supply': blockchain.max_supply
    })

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Cerca per hash blocco
    for block in blockchain.chain:
        if query in block.hash:
            return jsonify({'type': 'block', 'data': block.to_dict()})
    
    # Cerca per hash transazione
    for block in blockchain.chain:
        for tx in block.transactions:
            if query in tx.txid:
                tx_data = tx.to_dict()
                tx_data['block_index'] = block.index
                return jsonify({'type': 'transaction', 'data': tx_data})
    
    # Cerca per indirizzo
    if query.startswith('jabo86'):
        balance = blockchain.get_balance(query)
        if balance > 0:
            return jsonify({'type': 'address', 'data': {'address': query, 'balance': balance}})
    
    return jsonify({'error': 'Not found'}), 404

# Crea directory templates se non esiste
os.makedirs('templates', exist_ok=True)

# Crea template HTML base
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Rhodium Blockchain Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fade-in { animation: fadeIn 0.5s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body class="bg-gray-900 text-white">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-8 fade-in">
            <h1 class="text-4xl font-bold mb-2">🔍 Rhodium Explorer</h1>
            <p class="text-gray-400">Esplora la blockchain Rhodium in tempo reale</p>
        </div>

        <!-- Network Stats -->
        <div id="network-stats" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 fade-in">
            <div class="bg-gray-800 p-4 rounded-lg text-center">
                <div class="text-2xl font-bold" id="block-count">-</div>
                <div class="text-gray-400">Blocchi</div>
            </div>
            <div class="bg-gray-800 p-4 rounded-lg text-center">
                <div class="text-2xl font-bold" id="total-mined">-</div>
                <div class="text-gray-400">RHO Minati</div>
            </div>
            <div class="bg-gray-800 p-4 rounded-lg text-center">
                <div class="text-2xl font-bold" id="difficulty">-</div>
                <div class="text-gray-400">Difficulty</div>
            </div>
            <div class="bg-gray-800 p-4 rounded-lg text-center">
                <div class="text-2xl font-bold" id="pending-txs">-</div>
                <div class="text-gray-400">Tx Pendenti</div>
            </div>
        </div>

        <!-- Search -->
        <div class="mb-8 fade-in">
            <input type="text" id="search-input" placeholder="Cerca blocco, transazione o indirizzo..." 
                   class="w-full p-4 bg-gray-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>

        <!-- Blocks -->
        <div class="fade-in">
            <h2 class="text-2xl font-bold mb-4">Ultimi Blocchi</h2>
            <div id="blocks-list" class="space-y-4">
                <!-- Blocks will be loaded here -->
            </div>
        </div>
    </div>

    <script>
        // Load network stats
        async function loadNetworkStats() {
            const response = await fetch('/api/network');
            const data = await response.json();
            
            document.getElementById('block-count').textContent = data.block_count;
            document.getElementById('total-mined').textContent = data.total_mined.toLocaleString();
            document.getElementById('difficulty').textContent = data.difficulty.toFixed(2);
            document.getElementById('pending-txs').textContent = data.pending_transactions;
        }

        // Load blocks
        async function loadBlocks() {
            const response = await fetch('/api/blocks');
            const blocks = await response.json();
            
            const blocksList = document.getElementById('blocks-list');
            blocksList.innerHTML = '';
            
            blocks.slice(-10).reverse().forEach(block => {
                const blockElement = document.createElement('div');
                blockElement.className = 'bg-gray-800 p-4 rounded-lg hover:bg-gray-700 cursor-pointer';
                blockElement.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <div class="font-bold">Blocco #${block.index}</div>
                            <div class="text-sm text-gray-400">${block.hash.substring(0, 20)}...</div>
                        </div>
                        <div class="text-right">
                            <div>${block.transactions} tx</div>
                            <div class="text-sm text-gray-400">${new Date(block.timestamp * 1000).toLocaleString()}</div>
                        </div>
                    </div>
                `;
                blockElement.onclick = () => alert(`Hash: ${block.hash}`);
                blocksList.appendChild(blockElement);
            });
        }

        // Search functionality
        document.getElementById('search-input').addEventListener('keypress', async (e) => {
            if (e.key === 'Enter') {
                const query = e.target.value;
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                const result = await response.json();
                
                if (result.type === 'block') {
                    alert(`Trovato blocco #${result.data.index}`);
                } else if (result.type === 'transaction') {
                    alert(`Trovata transazione: ${result.data.txid.substring(0, 20)}...`);
                } else if (result.type === 'address') {
                    alert(`Indirizzo: ${result.data.address} - Balance: ${result.data.balance} RHO`);
                } else {
                    alert('Nessun risultato trovato');
                }
            }
        });

        // Initial load
        loadNetworkStats();
        loadBlocks();
        
        // Refresh every 30 seconds
        setInterval(() => {
            loadNetworkStats();
            loadBlocks();
        }, 30000);
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🌐 Avvio Rhodium Explorer su http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
