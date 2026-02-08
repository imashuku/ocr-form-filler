#!/bin/bash
# 8501番ポートを使っている古いプロセスを強制終了
fuser -k 8501/tcp > /dev/null 2>&1
lsof -ti:8501 | xargs kill -9 > /dev/null 2>&1

# Streamlitを起動
source venv/bin/activate
streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false
