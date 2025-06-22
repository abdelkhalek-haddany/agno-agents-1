import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.fire_crawl_api_key = os.getenv("FIRE_CRAWL_API_KEY")

    def validate(self):
        """Ensure all required settings are provided"""
        missing = []
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
