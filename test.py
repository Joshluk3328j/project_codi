import requests

try:
    r = requests.get("https://api-inference.huggingface.co")
    print("Connection successful:", r.status_code)
except Exception as e:
    print("Connection failed:", e)