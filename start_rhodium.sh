#!/bin/bash
echo "🚀 Rhodium Blockchain - Starter"
echo "================================"

# Check dependencies
echo "🔍 Checking dependencies..."
python3 -c "import flask" 2>/dev/null && echo "✅ Flask installed" || { echo "❌ Flask not installed. Installing..."; pip3 install flask; }
python3 -c "from Crypto.PublicKey import ECC" 2>/dev/null && echo "✅ PyCryptodome installed" || { echo "❌ PyCryptodome not installed. Installing..."; pip3 install pycryptodome; }
python3 -c "import base58" 2>/dev/null && echo "✅ Base58 installed" || { echo "❌ Base58 not installed. Installing..."; pip3 install base58; }

echo ""
echo "🎯 Available options:"
echo "1. 🌐 Web Explorer (http://localhost:5000)"
echo "2. 🖥️  GUI Wallet" 
echo "3. ⛏️  Miner"
echo "4. 🔗 P2P Network"
echo "5. 📱 All in one (Explorer + GUI)"
echo ""
read -p "Choose option (1-5): " choice

case $choice in
    1)
        echo "🌐 Starting Explorer..."
        python3 rhodium_explorer.py
        ;;
    2)
        echo "🖥️ Starting GUI Wallet..."
        python3 rhodium_gui.py
        ;;
    3)
        echo "⛏️ Starting Miner..."
        python3 rhodium_miner.py
        ;;
    4)
        echo "🔗 Starting P2P Network..."
        python3 rhodium_network.py
        ;;
    5)
        echo "📱 Starting All Services..."
        # Start explorer in background
        python3 rhodium_explorer.py &
        EXPLORER_PID=$!
        echo "✅ Explorer started (PID: $EXPLORER_PID)"
        
        # Start GUI
        echo "🖥️ Starting GUI Wallet..."
        python3 rhodium_gui.py
        
        # When GUI closes, stop explorer
        kill $EXPLORER_PID 2>/dev/null
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac
