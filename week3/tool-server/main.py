from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# main.py 있는 폴더 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/tool")
def tool():
    data = request.get_json(force=True) or {}

    tool_name = data.get("tool")
    args = data.get("args", {})

    # === read_file ============
    if tool_name == "read_file":
        # MITM에서 바꿀 부분: path
        path = args.get("path", "data/hello.txt")

        # "/data/passwd.txt" 이렇게 와도 처리되게
        safe_path = path.lstrip("/\\")  # 맨 앞 /, \ 제거
        full_path = os.path.join(DATA_DIR, safe_path.replace("..", ""))

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return jsonify({
            "type": "tool_result",
            "tool": "read_file",
            "result": {"path": safe_path, "content": content}
        })

    # === echo =================
    if tool_name == "echo":
        text = args.get("text", "")
        return jsonify({
            "type": "tool_result",
            "tool": "echo",
            "result": {"text": text}
        })

    # 알 수 없는 tool
    return jsonify({"error": "unknown tool"}), 400


@app.get("/health")
def health():
    return "ok", 200


if __name__ == "__main__":
    # 로그에 찍힌 tool_url 이 5100이었으니까 그대로 5100 사용
    app.run(host="127.0.0.1", port=5100, debug=True)
