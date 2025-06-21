import google.generativeai as genai
import os

class GeminiLLM:
    def __init__(self, model="gemini-1.5-flash",api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.7, max_tokens=1024):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        genai.configure(api_key=api_key)

    @property
    def id(self):
        return self.model
    
    @property
    def provider(self):
        return "google"
    
    # @property
    def get_instructions_for_model(self, tools=None):
        # This method is required by Agno. Here is a simple version:
        return "You are a helpful AI assistant. Use the provided tools when necessary."

    def get_system_message_for_model(self, tools=None):
        return "You are a helpful and knowledgeable AI assistant."  # Minimal system prompt
    
    def response_stream(self, *args, **kwargs):
        return iter([]) 
    
    @property
    def assistant_message_role(self):
        # Example: return the string expected by your framework
        return "assistant"

    def generate(self, prompt, **kwargs):
        generation_config = {
            "temperature": self.temperature,
            "max_output_tokens": self.max_tokens,
        }
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
