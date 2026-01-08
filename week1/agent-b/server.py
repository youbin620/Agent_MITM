from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

@app.post("/tool")
def tool():
    data = request.get_json(silent=True) or {}
    print("\n[Agent B] Received POST /tool")
    print("[Agent B] JSON:", json.dumps(data, ensure_ascii=False))

    resp = {
        "status": "ok",
        "tool_result": {"echo": data},
        "server_time": time.time(),
    }
    print("[Agent B] Respond:", json.dumps(resp, ensure_ascii=False))
    return jsonify(resp), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
