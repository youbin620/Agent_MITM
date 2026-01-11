from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.post("/tool")
def tool():
    data = request.get_json(force=True)
    tool_name = data.get("tool")
    args = data.get("args", {})

    # ✅ 판단 로직 없음: 요청대로만 수행
    if tool_name == "read_file":
        path = args.get("path", "data/hello.txt")
        full = os.path.join("/app", path)
        with open(full, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({
            "type": "tool_result",
            "tool": "read_file",
            "result": {"path": path, "content": content}
        })

    if tool_name == "echo":
        text = args.get("text", "")
        return jsonify({
            "type": "tool_result",
            "tool": "echo",
            "result": {"text": text}
        })

    return jsonify({"error": "unknown tool"}), 400

@app.get("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100)
