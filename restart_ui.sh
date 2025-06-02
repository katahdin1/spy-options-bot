#!/bin/bash

echo "🔁 Restarting Streamlit UI on port 8080..."

# Kill any previous Streamlit instance using port 8080
if command -v fuser &> /dev/null; then
  fuser -k 8080/tcp
fi

# Start Streamlit with correct flags
streamlit run streamlit_app.py --server.port=8080 --server.address=0.0.0.0
