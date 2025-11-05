FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p blockchain_data

# Expose ports
EXPOSE 8334  # P2P port
EXPOSE 8335  # RPC port  
EXPOSE 5000  # Explorer port

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Rhodium Blockchain..."\n\
\n\
# Start Explorer in background\n\
python3 rhodium_explorer.py &\n\
\n\
# Start P2P node in background  \n\
python3 rhodium_network.py &\n\
\n\
# Start main interface\n\
if [ "$1" = "gui" ]; then\n\
    echo "🖥️  Starting GUI Wallet..."\n\
    python3 rhodium_gui.py\n\
else\n\
    echo "💻 Starting CLI..."\n\
    echo "Available commands:"\n\
    echo "  python3 rhodium_wallet.py    - Create wallet"\n\
    echo "  python3 rhodium_miner.py     - Start mining"\n\
    echo "  python3 rhodium_cli.py       - CLI interface"\n\
    echo "  http://localhost:5000        - Blockchain Explorer"\n\
    bash\n\
fi' > /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/bin/bash", "/app/start.sh"]
