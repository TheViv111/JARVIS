import requests
import os

url = "https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/hey_jarvis_v0.1.onnx"
# Properly escaped path
output_path = "C:\\Users\\vivaa\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\openwakeword\\resources\\models\\hey_jarvis_v0.1.onnx"

print(f"Downloading to {output_path}...")
try:
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Download successful!")
except Exception as e:
    print(f"Download failed with error: {e}")
