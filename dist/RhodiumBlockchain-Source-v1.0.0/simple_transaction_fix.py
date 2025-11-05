with open('rhodium_core_hard.py', 'r') as f:
    content = f.read()

# Trova l'ultima riga e aggiungi prima della fine
if 'def get_transactions_for_address' not in content:
    simple_function = '''

    def get_transactions_for_address(self, address):
        """Versione semplificata - restituisce lista vuota"""
        print(f"🔍 Cerco transazioni per: {address[:10]}...")
        return []  # Per ora restituisce lista vuota

'''
    # Aggiungi prima dell'ultima riga
    if 'if __name__ == "__main__":' in content:
        content = content.replace('if __name__ == "__main__":', simple_function + 'if __name__ == "__main__":')
    else:
        content += simple_function

with open('rhodium_core_hard.py', 'w') as f:
    f.write(content)

print("✅ Funzione transazioni semplificata aggiunta!")
