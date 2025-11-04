#!/bin/bash
echo "🚀 Installing Rhodium Blockchain..."
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo "🔧 Making scripts executable..."
chmod +x rhodium_wallet.py rhodium_core.py rhodium_cli.py rhodium_miner.py

echo "✅ Rhodium Blockchain installed successfully!"
echo ""
echo "🎯 Next steps:"
echo "  1. Create wallet: python3 rhodium_wallet.py"
echo "  2. Start mining: python3 rhodium_miner.py"
echo "  3. Check balance: python3 rhodium_cli.py getbalance"
echo ""
echo "💎 Welcome to Rhodium Blockchain!"
