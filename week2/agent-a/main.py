import os, time, requests, json

AGENT_B_URL = os.environ.get("AGENT_B_URL", "http://agent-b:5200")
PROMPT = os.environ.get("PROMPT", "hello")

def choose_action(prompt: str) -> str:
    # ✅ Agent A 내부 로직: prompt에 따라 tool 선택
    # 'file' 포함이면 read_file, 아니면 echo
    return "read_file" if "file" in prompt.lower() else "echo"

def main():
    time.sleep(3.0)  # 컨테이너 기동 대기
    action = choose_action(PROMPT)

    # A → B로 보내는 메시지 = prompt (+ A가 선택한 action)
    prompt_msg = {
        "type": "prompt",
        "from": "agent-a",
        "prompt": PROMPT,
        "action": action
    }

    for i in range(5):
        r = requests.post(f"{AGENT_B_URL}/process", json=prompt_msg, timeout=8)
        res = r.json()
        print(f"\n--- REQUEST {i+1}/5 ---")
        print(json.dumps(prompt_msg, ensure_ascii=False, indent=2))
        print(json.dumps(res, ensure_ascii=False, indent=2))
        time.sleep(0.6)

if __name__ == "__main__":
    main()
