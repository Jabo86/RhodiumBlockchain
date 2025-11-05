#!/bin/bash
echo 'Starting Rhodium Wallet...'
cd "$(dirname "$0")"
python3 rhodium_gui.py
