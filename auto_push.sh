#!/bin/bash
echo "📤 Auto-pushing latest changes..."
git add .
git commit -m "🚀 Auto update: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin main
