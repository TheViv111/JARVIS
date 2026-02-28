import subprocess
import time
import sys
import os
import requests

def get_python():
    """Use venv Python if available, else sys.executable."""
    jarvis_root = os.path.dirname(os.path.abspath(__file__))
    if sys.platform == "win32":
        venv_python = os.path.join(jarvis_root, ".venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(jarvis_root, ".venv", "bin", "python")
    if os.path.isfile(venv_python):
        return venv_python
    return sys.executable


def launch_service(name, directory, port):
    print(f"Starting {name} on port {port}...")
    env = os.environ.copy()
    env["PYTHONPATH"] = directory
    python = get_python()

    process = subprocess.Popen(
        [
            python, "-m", "uvicorn", "app.main:app",
            "--host", "127.0.0.1", "--port", str(port),
            "--log-level", "warning",
        ],
        cwd=directory,
        env=env,
    )
    return process


def launch_voice_console(runtime_dir):
    print("Starting Voice Console (listening for 'Hey Jarvis')...")
    env = os.environ.copy()
    env["PYTHONPATH"] = runtime_dir
    python = get_python()
    process = subprocess.Popen(
        [python, "voice_console.py"],
        cwd=runtime_dir,
        env=env,
    )
    return process

def launch_control_center(control_center_dir):
    print("Starting JARVIS Control Center (web UI)...")
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=control_center_dir,
        shell=True,
    )
    return process

def check_health(url, process=None, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if process is not None and process.poll() is not None:
            return False
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False

def is_healthy(url):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def stop_service(process):
    if process is None:
        return
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

def main():
    jarvis_root = os.path.dirname(os.path.abspath(__file__))
    voice_dir = os.path.join(jarvis_root, "services", "voice-pipeline")
    runtime_dir = os.path.join(jarvis_root, "services", "runtime-api")
    voice_port = 7788
    runtime_port = 7777
    voice_console_proc = None
    orb_proc = None
    control_center_proc = None
    control_center_port = 3000

    print("=== JARVIS Master Launcher ===")
    
    # 1. Start Voice Pipeline
    voice_proc = None
    if is_healthy(f"http://127.0.0.1:{voice_port}/v1/health"):
        print(f"Voice Pipeline already running on port {voice_port}; reusing existing service.")
    else:
        voice_proc = launch_service("Voice Pipeline", voice_dir, voice_port)
    
    # 2. Start Runtime API
    runtime_proc = None
    if is_healthy(f"http://127.0.0.1:{runtime_port}/v1/health"):
        print(f"Runtime API already running on port {runtime_port}; reusing existing service.")
    else:
        runtime_proc = launch_service("Runtime API", runtime_dir, runtime_port)

    print("Waiting for services to initialize...")
    
    voice_ok = check_health(f"http://127.0.0.1:{voice_port}/v1/health", process=voice_proc, timeout=45)
    runtime_ok = check_health(f"http://127.0.0.1:{runtime_port}/v1/health", process=runtime_proc, timeout=45)

    if voice_ok and runtime_ok:
        voice_console_proc = launch_voice_console(runtime_dir)
        time.sleep(2)  # Let voice console initialize

        # Start the orb (Electron) if available
        orb_proc = None
        orb_dir = os.path.join(jarvis_root, "apps", "desktop-shell")
        if os.path.isfile(os.path.join(orb_dir, "package.json")):
            try:
                print("Starting JARVIS Orb...")
                orb_proc = subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=orb_dir,
                    shell=True,
                )
            except Exception:
                pass

        # Start the localhost web UI if available
        control_center_dir = os.path.join(jarvis_root, "apps", "control-center")
        if os.path.isfile(os.path.join(control_center_dir, "package.json")):
            if is_healthy(f"http://127.0.0.1:{control_center_port}"):
                print(
                    f"Control Center already running on port {control_center_port}; reusing existing service."
                )
            else:
                try:
                    control_center_proc = launch_control_center(control_center_dir)
                    if check_health(
                        f"http://127.0.0.1:{control_center_port}",
                        process=control_center_proc,
                        timeout=45,
                    ):
                        print(
                            f"Control Center online: http://127.0.0.1:{control_center_port}"
                        )
                    else:
                        print(
                            f"WARNING: Control Center did not report healthy on port {control_center_port}."
                        )
                except Exception as ex:
                    print(f"WARNING: Failed to start Control Center: {ex}")

        print("\nSUCCESS: JARVIS is now online.")
        print("-------------------------------")
        print(f"Ears (Voice): http://127.0.0.1:{voice_port}")
        print(f"Brain (API):  http://127.0.0.1:{runtime_port}")
        print(f"UI (Web):     http://127.0.0.1:{control_center_port}")
        print("-------------------------------\n")
        print("Voice console is listening. Say 'Hey Jarvis' to activate.")
        print("Press Ctrl+C to shut down JARVIS.\n")

        try:
            # Keep the main script running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down JARVIS...")
    else:
        print("\nERROR: One or more services failed to start.")
        if not voice_ok:
            print(f"- Voice Pipeline failed/timed out on port {voice_port}.")
            if voice_proc is not None and voice_proc.poll() is not None:
                print(f"  Voice process exited early with code {voice_proc.returncode}.")
        if not runtime_ok:
            print(f"- Runtime API failed/timed out on port {runtime_port}.")
            if runtime_proc is not None and runtime_proc.poll() is not None:
                print(f"  Runtime process exited early with code {runtime_proc.returncode}.")
    
    # Cleanup
    stop_service(orb_proc)
    stop_service(control_center_proc)
    stop_service(voice_console_proc)
    stop_service(voice_proc)
    stop_service(runtime_proc)
    print("Goodbye, Vivaan.")

if __name__ == "__main__":
    main()
