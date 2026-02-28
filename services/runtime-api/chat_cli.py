import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


BASE_URL = "http://127.0.0.1:7777"
SESSION_ID = f"sess_cli_{int(time.time())}"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def post_json(path: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url=f"{BASE_URL}{path}",
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        body = response.read().decode("utf-8")
        return response.status, json.loads(body)


def check_health() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE_URL}/v1/health", timeout=5) as response:
            return response.status == 200
    except Exception:  # noqa: BLE001
        return False


def print_help() -> None:
    print("Commands:")
    print("  /help   Show commands")
    print("  /meta   Toggle meta details (risk/latency/plan/providers)")
    print("  /speak  Toggle spoken reply generation (via voice-pipeline)")
    print("  /raw    Toggle raw JSON response view")
    print("  /think  Toggle 'Thinking...' indicator")
    print("  /exit   Quit")


def write_tts_file(audio_b64: str, mime_type: str) -> str:
    import base64

    OUTPUT_DIR.mkdir(exist_ok=True)
    ext = ".mp3" if mime_type == "audio/mpeg" else ".wav"
    out_path = OUTPUT_DIR / f"jarvis_reply_{int(time.time() * 1000)}{ext}"
    with open(out_path, "wb") as handle:
        handle.write(base64.b64decode(audio_b64))
    return str(out_path)


def main() -> int:
    raw_mode = False
    meta_mode = False
    think_mode = True
    speak_mode = False

    print("JARVIS CLI")
    print(f"Session: {SESSION_ID}")
    print(f"API: {BASE_URL}")

    if not check_health():
        print("Runtime API is not reachable at /v1/health.")
        print("Start it with: uvicorn app.main:app --host 127.0.0.1 --port 7777 --reload")
        return 1

    print("Connected. Type your message and press Enter. Type /help for commands.")

    while True:
        try:
            user_text = input("\nYou > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return 0

        if not user_text:
            continue
        if user_text == "/exit":
            print("Exiting.")
            return 0
        if user_text == "/help":
            print_help()
            continue
        if user_text == "/meta":
            meta_mode = not meta_mode
            print(f"Meta mode: {'ON' if meta_mode else 'OFF'}")
            continue
        if user_text == "/raw":
            raw_mode = not raw_mode
            print(f"Raw mode: {'ON' if raw_mode else 'OFF'}")
            continue
        if user_text == "/speak":
            speak_mode = not speak_mode
            print(f"Speak mode: {'ON' if speak_mode else 'OFF'}")
            continue
        if user_text == "/think":
            think_mode = not think_mode
            print(f"Thinking indicator: {'ON' if think_mode else 'OFF'}")
            continue

        payload = {
            "session_id": SESSION_ID,
            "input": user_text,
            "modality": "text",
            "prefer_cloud": True,
            "speak_response": speak_mode,
            "context": {"source": "chat_cli"},
        }

        if think_mode:
            print("JARVIS > Thinking...")
        started = time.perf_counter()
        try:
            status, data = post_json("/v1/intent/execute", payload)
            elapsed_ms = int((time.perf_counter() - started) * 1000)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            print(f"HTTP error: {exc.code}")
            print(body)
            continue
        except Exception as exc:  # noqa: BLE001
            print(f"Request failed: {exc}")
            continue

        print(f"JARVIS > {data.get('assistant_output', '[no output]')}")
        if speak_mode and data.get("tts_audio_base64"):
            try:
                tts_path = write_tts_file(
                    audio_b64=data["tts_audio_base64"],
                    mime_type=data.get("tts_mime_type", "audio/wav"),
                )
                print(f"Audio > saved to {tts_path}")
            except Exception as exc:  # noqa: BLE001
                print(f"Audio > save failed: {exc}")
        if meta_mode:
            print(
                "Meta  > "
                f"status={status}  "
                f"latency={elapsed_ms}ms  "
                f"risk={data.get('risk', 'unknown')}  "
                f"approval={data.get('requires_approval', False)}"
            )
            providers = data.get("providers", {})
            plan = data.get("plan", [])
            print(f"Plan  > {', '.join(plan) if plan else '[none]'}")
            print(
                "Using > "
                f"llm={providers.get('llm', 'n/a')}  "
                f"stt={providers.get('stt', 'n/a')}  "
                f"face={providers.get('face', 'n/a')}  "
                f"tts={providers.get('tts', 'n/a')}"
            )

        if raw_mode:
            print("Raw   >")
            print(json.dumps(data, indent=2))


if __name__ == "__main__":
    sys.exit(main())
