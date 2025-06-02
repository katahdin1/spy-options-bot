#!/bin/bash

echo "🔪 Killing any process on port 8080..."
fuser -k 8080/tcp

echo "🚀 Starting SPY Options Bot..."
python main.py
