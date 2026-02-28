import requests
import os

# Try to find a working ONNX model URL
urls = [
    "https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/hey_jarvis_v0.1.onnx",
    "https://github.com/dscripka/openWakeWord/releases/download/v0.5.1/hey_jarvis_v0.1.onnx",
    "https://raw.githubusercontent.com/dscripka/openWakeWord/main/openwakeword/resources/models/hey_jarvis_v0.1.onnx"
]

target_dir = r"C:\Users\vivaa\Documents\jarvis\assets\models"
os.makedirs(target_dir, exist_ok=True)
output_path = os.path.join(target_dir, "hey_jarvis_v0.1.onnx")

for url in urls:
    print(f"Trying {url}...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Successfully downloaded to {output_path}")
            break
        else:
            print(f"Failed with status {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Could not download any model.")
