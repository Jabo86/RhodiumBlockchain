#!/usr/bin/env python3
import argparse
import json
import sys
import os
from rhodium_core import RhodiumBlockchain, Transaction
from rhodium_wallet import RhodiumWallet

def main():
    parser = argparse.ArgumentParser(description='Rhodium CLI - Gestisci la tua blockchain')
    subparsers = parser.add_subparsers(dest='command', help='Comandi disponibili')
    
    # Comando getinfo
    subparsers.add_parser('getinfo', help='Mostra informazioni blockchain')
    
    # Comando getbalance
    balance_parser = subparsers.add_parser('getbalance', help='Mostra balance')
    balance_parser.add_argument('address', nargs='?', help='Indirizzo (opzionale)')
    
    # Comando send
    send_parser = subparsers.add_parser('send', help='Invia RHO')
    send_parser.add_argument('to', help='Indirizzo destinatario')
    send_parser.add_argument('amount', type=float, help='Quantità RHO')
    send_parser.add_argument('--fee', type=float, default=0.001, help='Fee transazione')
    
    # Comando mine
    mine_parser = subparsers.add_parser('mine', help='Mina un blocco')
    mine_parser.add_argument('--address', help='Indirizzo miner')
    
    args = parser.parse_args()
    
    blockchain = RhodiumBlockchain()
    wallet = RhodiumWallet()
    
    if args.command == 'getinfo':
        print("=== RHODIUM BLOCKCHAIN ===")
        print(f"📦 Blocchi: {len(blockchain.chain)}")
        print(f"💰 RHO totali: {blockchain.total_mined:,.2f} / 21,000,000")
        print(f"⛏️  Difficulty: {blockchain.difficulty}")
        print(f"💸 Reward blocco: {blockchain.mining_reward} RHO")
        print(f"📊 Transazioni pendenti: {len(blockchain.pending_transactions)}")
        
        if blockchain.chain:
            latest = blockchain.get_latest_block()
            print(f"🔗 Ultimo blocco: #{latest.index} - {latest.hash[:16]}...")
    
    elif args.command == 'getbalance':
        address = args.address or wallet.get_address()
        balance = blockchain.get_balance(address)
        print(f"💰 Balance di {address}: {balance:,.6f} RHO")
    
    elif args.command == 'send':
        from_address = wallet.get_address()
        to_address = args.to
        amount = args.amount
        fee = args.fee
        
        balance = blockchain.get_balance(from_address)
        if balance >= amount + fee:
            tx = Transaction(from_address, to_address, amount, fee)
            if blockchain.add_transaction(tx):
                print(f"✅ Transazione creata!")
                print(f"📤 Da: {from_address}")
                print(f"📥 A: {to_address}")
                print(f"💸 Importo: {amount} RHO")
                print(f"💰 Fee: {fee} RHO")
                print(f"🔗 TXID: {tx.txid}")
                print("⏳ In attesa di essere minata...")
            else:
                print("❌ Errore creazione transazione")
        else:
            print(f"❌ Fondi insufficienti! Balance: {balance} RHO")
    
    elif args.command == 'mine':
        miner_address = args.address or wallet.get_address()
        print(f"⛏️  Inizio mining con indirizzo: {miner_address}")
        
        block = blockchain.mine_block(miner_address)
        if block:
            print(f"🎉 Blocco #{block.index} minato con successo!")
            print(f"💰 Ricompensa: {blockchain.mining_reward} RHO")
        else:
            print("❌ Mining fallito")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
