import os
import google.generativeai as genai
import json
from json_repair import repair_json
from groq import Groq


class Agent:
    def __init__(self, prompt_dir: str):
        self.gemini_api_keys = self._get_gemini_api_key()
        self._load_config()
        self.gemini = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp"
        )

        self.groq_api_keys = self._get_groq_api_key()
        self.groq = Groq(api_key=os.environ[next(self.groq_api_keys)])

        self.prompts = {}
        self._load_prompts(prompt_dir)

    def _load_prompts(self, prompt_dir: str):
        for filename in os.listdir(prompt_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(prompt_dir, filename), "r") as f:
                    self.prompts[filename.split(".")[0]] = f.read()

    @staticmethod
    def _get_gemini_api_key():
        list_keys = [
            "GEMINI_API_KEY_0",
            "GEMINI_API_KEY_1",
            "GEMINI_API_KEY_2",
            "GEMINI_API_KEY_3",
            "GEMINI_API_KEY_4",
            "GEMINI_API_KEY_5"
        ]
        idx = 0
        while True:
            if idx >= len(list_keys):
                idx = 0
            print(f'Using API key: {list_keys[idx]}')
            yield list_keys[idx]
            idx += 1

    @staticmethod
    def _get_groq_api_key():
        list_keys = [
            "GROQ_API_KEY_0",
        ]
        idx = 0
        while True:
            if idx >= len(list_keys):
                idx = 0
            print(f'Using API key: {list_keys[idx]}')
            yield list_keys[idx]
            idx += 1

    def _load_gemini_config(self):
        genai.configure(api_key=os.environ[next(self.gemini_api_keys)])
        self.gemini = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
        )

    def _load_groq_config(self):
        self.groq = Groq(api_key=os.environ[next(self.groq_api_keys)])

    def _load_config(self):
        self._load_gemini_config()

    def gemini_generate(self, prompt: str, response_type: str = "json"):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json" if response_type == "json" else "text/plain",
        }
        c = 0
        while True:
            try:
                response = self.gemini.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                if response_type == "json":
                    try:
                        return json.loads(response.text)
                    except json.JSONDecodeError:
                        return json.loads(repair_json(response.text))
                elif response_type == "text":
                    return response.text
            except Exception as e:
                if c > 5:
                    return None
                print(e)
                self._load_gemini_config()
                c += 1

    def groq_generate(self, prompt: str, response_type: str = "json"):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json" if response_type == "json" else "text/plain",
        }
        while True:
            try:
                response = self.groq.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    response_format={"type": "json_object"} if response_type == "json" else {"type": "text"},
                    model="llama-3.3-70b-versatile",
                )
                response = response.choices[0].message.content
                if response_type == "json":
                    try:
                        return json.loads(response)
                    except json.JSONDecodeError:
                        return json.loads(repair_json(response))
                elif response_type == "text":
                    return response
            except Exception as e:
                print(e)
                self._load_groq_config()

    def generate(self, prompt: str, response_type: str = "json"):
        response = self.gemini_generate(prompt, response_type)
        if response is not None:
            return response

        response = self.groq_generate(prompt, response_type)
        if response is not None:
            return response