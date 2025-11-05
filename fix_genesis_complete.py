import re

with open('rhodium_core_hard.py', 'r') as f:
    content = f.read()

# Sostituisci TUTTI gli indirizzi nel Genesis Block
your_address = "jabo867WwmfUePRCzYDNn6iqbAw"

# Sostituisci la riga del Genesis Block
old_pattern = r'genesis_transaction = Transaction\("0", ".*?", 1000000\.0\)'
new_genesis = f'genesis_transaction = Transaction("0", "{your_address}", 1000000.0)'

content = re.sub(old_pattern, new_genesis, content)

with open('rhodium_core_hard.py', 'w') as f:
    f.write(content)

print(f"✅ Genesis Block modificato per: {your_address}")
