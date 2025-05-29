import requests

def query_huggingface(code: str, hf_token: str, style: str = "concise") -> str:
    api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    # api_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    # Adjust instruction based on selected style
    instruction_map = {
        "concise": "Give a very short explanation of the following code and correct errors(indentation, syntax or anyother) if any while explaining:",
        "reiterate": "Reiterate what this code does step by step and correct errors(indentation, syntax or anyother) if any if any while explaining:",
        "in-depth": "Give a detailed, in-depth explanation of the following code and correct errors(indentation, syntax or anyother) if any if any while explaining:"
    }
    instruction = instruction_map.get(style.lower(), instruction_map["concise"])

    prompt = f"<s>[INST] {instruction}\n\n{code}\n\n[/INST]"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.95,
            "do_sample": True
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    generated_text = response.json()[0]["generated_text"]
    explanation = generated_text.replace(prompt, "").strip().replace("\\_", "_")
    return explanation
    # high royal highness worked on this
