import re

with open('rhodium_core_hard.py', 'r') as f:
    content = f.read()

# Sostituisci l'indirizzo nel Genesis Block con il tuo
new_address = "'"$YOUR_ADDRESS"'"
old_pattern = r'genesis_transaction = Transaction\("0", "jabo867WwmfUePRCzYDNn6iqbAw", 1000000\.0\)'
new_genesis = f'genesis_transaction = Transaction("0", {new_address}, 1000000.0)'

content = re.sub(old_pattern, new_genesis, content)

with open('rhodium_core_hard.py', 'w') as f:
    f.write(content)

print(f"✅ Genesis Block modificato! Ora i 1,000,000 RHO sono tuoi: {new_address}")
