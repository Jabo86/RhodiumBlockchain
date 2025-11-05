#!/usr/bin/env python3
from rhodium_wallet import RhodiumWallet

# Crea un nuovo wallet di test
wallet2 = RhodiumWallet("wallet_test.dat")
address2 = wallet2.generate_keypair()
print(f"🎉 Secondo wallet creato!")
print(f"📬 Indirizzo: {address2}")
