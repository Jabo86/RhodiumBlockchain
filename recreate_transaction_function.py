import re

with open('rhodium_core_hard.py', 'r') as f:
    content = f.read()

# Nuova versione SEMPLICE e FUNZIONANTE della funzione
new_function = '''
    def get_all_transactions_for_address(self, address):
        """Restituisce TUTTE le transazioni per un indirizzo - VERSIONE SEMPLICE"""
        transactions = []
        print(f"\\\\n🔍 [CORE] Cerco transazioni per: {address[:10]}...")
        
        try:
            for i, block in enumerate(self.chain):
                #print(f"🔍 [CORE] Analizzo blocco {i} con {len(block.transactions)} transazioni")
                for tx in block.transactions:
                    # Transazione di MINING
                    if tx.sender == "0" and tx.recipient == address:
                        #print(f"💰 [CORE] Trovata ricompensa mining: {tx.amount} RHO")
                        transactions.append({
                            'type': 'MINING',
                            'amount': float(tx.amount),
                            'address': 'RICHIESTA MINING',
                            'date': '2024-01-01 10:00'
                        })
                    
                    # Transazione NORMALE (inviata)
                    elif tx.sender == address:
                        #print(f"💸 [CORE] Trovata transazione inviata: {tx.amount} RHO a {tx.recipient[:10]}...")
                        transactions.append({
                            'type': 'INVIO',
                            'amount': float(tx.amount),
                            'address': tx.recipient,
                            'date': '2024-01-01 10:00'
                        })
                    
                    # Transazione NORMALE (ricevuta)
                    elif tx.recipient == address and tx.sender != "0":
                        #print(f"💰 [CORE] Trovata transazione ricevuta: {tx.amount} RHO da {tx.sender[:10]}...")
                        transactions.append({
                            'type': 'RICEZIONE',
                            'amount': float(tx.amount),
                            'address': tx.sender,
                            'date': '2024-01-01 10:00'
                        })
            
            print(f"✅ [CORE] Transazioni trovate: {len(transactions)}")
            
        except Exception as e:
            print(f"❌ [CORE] Errore: {e}")
            import traceback
            traceback.print_exc()
            
        return transactions
'''

# Sostituisci la funzione esistente
pattern = r'def get_all_transactions_for_address\(self, address\):.*?return transactions'
content = re.sub(pattern, new_function, content, flags=re.DOTALL)

with open('rhodium_core_hard.py', 'w') as f:
    f.write(content)

print("✅ Funzione transazioni ricreata!")
