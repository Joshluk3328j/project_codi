"""
Handles code explanation and question-answering using Hugging Face inference APIs.

Provides functionality to generate and send prompts to large language models 
(e.g., Mixtral or LLaMA)
to produce explanations or answers based on the uploaded code and selected explanation style.
"""

import requests

# Default model URL for inference
DEFAULT_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
# DEFAULT_MODEL_URL ="https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct"

class CodeExplainer:
    """
    A helper class that interacts with Hugging Face's inference API
    to explain Python code or answer code-related questions in various styles.
    """

    def __init__(self, api_key: str, model_url: str = None):
        """
        Initializes the CodeExplainer.

        Args:
            api_key (str): Hugging Face API key.
            model_url (str, optional): Custom model URL. Defaults to Mixtral 8x7B model.
        """
        self.api_key = api_key
        self.api_url = model_url or DEFAULT_MODEL_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Mapping for various explanation styles
        self.instruction_map = {
            "concise": (
                "Give a very short explanation of the following code and correct errors "
                "(indentation, syntax or any other) if any while explaining:"
            ),
            "reiterate": (
                "Reiterate what this code does step by step and correct errors "
                "(indentation, syntax or any other) if any while explaining:"
            ),
            "in-depth": (
                "Give a detailed, in-depth explanation of the following code and correct errors "
                "(indentation, syntax or any other) if any while explaining:"
            )
        }

    def generate_prompt(self, code: str, style: str = "concise") -> str:
        """
        Constructs a prompt for the model using the selected explanation style.

        Args:
            code (str): The code snippet to be explained.
            style (str): The explanation style ('concise', 'reiterate', or 'in-depth').

        Returns:
            str: Formatted prompt for model inference.
        """
        instruction = self.instruction_map.get(style.lower(), self.instruction_map["concise"])
        return f"<s>[INST] {instruction}\n\n{code}\n\n[/INST]"

    def explain_code(self, code: str, style: str = "concise") -> str:
        """
        Sends a code snippet to the API for explanation.

        Args:
            code (str): Python code to be explained.
            style (str): Explanation style ('concise', 'reiterate', 'in-depth').

        Returns:
            str: Model-generated explanation or error message.
        """
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
            result = response.json()

            # Extract explanation
            # Handle both list and dict return formats
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                generated_text = result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                generated_text = result["generated_text"]
            else:
                return "⚠️ Unexpected response format from API."
            explanation = generated_text.replace(prompt, "").strip().replace("\\_", "_")
            return explanation

        except Exception as e:
            return f"❌ Error explaining code: {str(e)}"

    def answer_question(self, question: str, style: str = "concise", uploaded_code: str = None) -> str:
        """
        Sends a natural language question (with optional code context) to the API.

        Args:
            question (str): The user's question.
            style (str): Response style ('concise', 'reiterate', or 'in-depth').
            uploaded_code (str, optional): Python code to provide as context.

        Returns:
            str: Model-generated answer or error message.
        """
        if not question:
            return "❌ Please enter a question."

        # Contextual code block (if any)
        code_section = (
            f"The code is:\n```python\n{uploaded_code}\n```"
            if uploaded_code else "just reply normally with the given style"
        )

        # Structured chat-like prompt
        chat_box = (
            f"Question: {question} "
            f"Only answer the question above. Do not answer or summarize anything else. "
            f"Answer ({style} style):"
        )

        prompt = (
            "You are Codi, an assistant that helps explain code and answer code-related and regular questions. "
            f"{code_section} {chat_box}"
        )

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt},
                timeout=40
            )
            response.raise_for_status()
            result = response.json()

            # Handle both list and dict return formats
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                full_response = result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                full_response = result["generated_text"]
            else:
                return "⚠️ Unexpected response format from API."

            answer = full_response.replace(prompt, "").strip()
            return answer

        except Exception as e:
            return f"❌ Error fetching answer: {str(e)}"
