import json
import time
import requests
import os

SERVER_URL = os.environ.get("SERVER_URL", "http://agent-b:8000/tool")

payload = {
    "id": f"call-{int(time.time())}",
    "type": "tool_call",
    "tool": "read_file",
    "arguments": {"path": "/hello.txt"}
}

print("[Agent A] Sending POST /tool to:", SERVER_URL)
print("[Agent A] JSON:", json.dumps(payload, ensure_ascii=False))

r = requests.post(SERVER_URL, json=payload, timeout=10)

print("[Agent A] Status:", r.status_code)
print("[Agent A] Response:", r.text)
