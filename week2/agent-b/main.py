from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)
TOOL_URL = os.environ.get("TOOL_URL", "http://tool-server:5100")

@app.post("/process")
def process():
    # A → B prompt 메시지 수신
    msg = request.get_json(force=True)
    prompt = msg.get("prompt", "")
    action = msg.get("action", "echo")  # A가 정해준 값

    # ✅ 규칙 기반 처리 (판단 규칙 단순)
    # action 값이 read_file이면 read_file, 아니면 echo
    if action == "read_file":
        tool_call = {
            "type": "tool_call",
            "tool": "read_file",
            "args": {"path": "data/hello.txt"},
            "reason": "action=read_file from Agent A"
        }
    else:
        tool_call = {
            "type": "tool_call",
            "tool": "echo",
            "args": {"text": prompt},
            "reason": "action=echo from Agent A"
        }

    # Tool Server 호출
    r = requests.post(f"{TOOL_URL}/tool", json=tool_call, timeout=5)
    tool_result = r.json()

    # 최종 response 생성
    used_tool = tool_call["tool"]
    if used_tool == "read_file":
        final = tool_result.get("result", {}).get("content", "")
    else:
        final = tool_result.get("result", {}).get("text", "")

    return jsonify({
        "type": "response",
        "used_tool": used_tool,
        "final": final,
        # README/디버깅용: (네트워크로도 보임)
        "debug": {"prompt": prompt, "action": action}
    })

@app.get("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200)
