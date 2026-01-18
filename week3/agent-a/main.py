import os, time, requests, json

AGENT_B_URL = os.environ.get("AGENT_B_URL", "http://127.0.0.1:5200")
PROMPT = os.environ.get("PROMPT", "hello")

# ⬇⬇⬇ 추가된 부분
PROXY_URL = os.environ.get("AGENT_PROXY")
PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if PROXY_URL else None
# ⬆⬆⬆

def choose_action(prompt: str) -> str:
    return "read_file" if "file" in prompt.lower() else "echo"

def main():
    time.sleep(1.5)
    action = choose_action(PROMPT)

    prompt_msg = {
        "type": "prompt",
        "from": "agent-a",
        "prompt": PROMPT,
        "action": action
    }

    for i in range(5):
        try:
            r = requests.post(
                f"{AGENT_B_URL}/process",
                json=prompt_msg,
                timeout=8,
                proxies=PROXIES   # ⬅ 추가된 부분
            )
        except Exception as e:
            print(f"[A] 요청 실패: {e}")
            return

        print(f"\n--- REQUEST {i+1}/5 ---")
        print("[A] STATUS:", r.status_code)
        print("[A] RAW BODY:", repr(r.text[:300]))

        # JSON이 아니면 죽지 말고 종료
        try:
            res = r.json()
        except Exception as e:
            print("[A] JSONDecodeError:", e)
            print("[A] 응답이 JSON이 아님 → B에서 HTML오류 or tool-server 문제")
            return

        print(json.dumps(prompt_msg, ensure_ascii=False, indent=2))
        print(json.dumps(res, ensure_ascii=False, indent=2))
        time.sleep(0.6)

if __name__ == "__main__":
    main()
