PORT="${PORT:-8080}"
uvicorn open_webui.main:app --port $PORT --host 143.64.120.39 --forwarded-allow-ips '*' --reload