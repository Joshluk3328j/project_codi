import requests

"https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"

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

        # prompt = "You are Codi, an assistant that helps explain code and answer code-related questions.\n\n"
        chat_box = (
            f"Question: {question} "
            f"Only answer the question above. Do not answer or summarize anything else. "
            f"Answer ({style} style):"
        )

        code_section = f"The code is:\n```python\n{uploaded_code}\n```" if uploaded_code else "just reply normally with the given style"

        prompt = (
            "You are Codi, an assistant that helps explain code and answer code-related and regular questions. "
            f"{code_section} {chat_box}"
        )

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt},
                timeout=40)
            response.raise_for_status()
            result = response.json()

            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                full_response = result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                full_response = result["generated_text"]
            else:
                return "⚠️ Unexpected response format from API."
            answer = full_response.replace(prompt,"").strip()
            return answer

        except Exception as e:
            return f"❌ Error fetching answer: {str(e)}"
