import requests

class CodeExplainer:
    def __init__(self, api_key: str, model_url: str = None):
        self.api_key = api_key
        self.api_url = model_url or "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.instruction_map = {
            "concise": "Give a very short explanation of the following code and correct errors(indentation, syntax or any other) if any while explaining:",
            "reiterate": "Reiterate what this code does step by step and correct errors(indentation, syntax or any other) if any while explaining:",
            "in-depth": "Give a detailed, in-depth explanation of the following code and correct errors(indentation, syntax or any other) if any while explaining:"
        }

    def generate_prompt(self, code: str, style: str = "concise") -> str:
        instruction = self.instruction_map.get(style.lower(), self.instruction_map["concise"])
        return f"<s>[INST] {instruction}\n\n{code}\n\n[/INST]"

    def explain_code(self, code: str, style: str = "concise") -> str:
        prompt = self.generate_prompt(code, style)
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.95,
                "do_sample": True
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=40)
            response.raise_for_status()
            generated_text = response.json()[0]["generated_text"]
            explanation = generated_text.replace(prompt, "").strip().replace("\\_", "_")
            return explanation
        except Exception as e:
            return f"❌ Error explaining code: {str(e)}"

    def answer_question(self, question: str, style: str = "concise", uploaded_code: str = None) -> str:
        if not question:
            return "❌ Please enter a question."

        prompt = "You are Codi, an assistant that helps explain code and answer code-related questions.\n\n"

        if uploaded_code:
            prompt += f"Here is the uploaded code:\n```python\n{uploaded_code}\n```\n\n"

        prompt += f"Question: {question}\nExplain in a {style} way."

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt}
            )
            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
            else:
                return "⚠️ Unexpected response format from API."

        except Exception as e:
            return f"❌ Error fetching answer: {str(e)}"
