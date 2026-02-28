import requests
import os

models_to_download = [
    "hey_jarvis_v0.1.onnx",
    "melspectrogram.onnx",
    "embedding_model.onnx"
]

base_url = "https://github.com/dscripka/openWakeWord/raw/v0.5.1/openwakeword/resources/models/"
target_dir = "C:\\Users\\vivaa\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\openwakeword\\resources\\models"
os.makedirs(target_dir, exist_ok=True)

for model in models_to_download:
    output_path = os.path.join(target_dir, model)
    url = base_url + model
    print(f"Downloading {model} from {url}...")
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Successfully downloaded {model}")
    except Exception as e:
        print(f"Error downloading {model}: {e}")

print("Done.")
