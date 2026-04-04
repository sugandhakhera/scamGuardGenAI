from google import genai
from utils.config   import get_logger
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = print(os.getenv("GEMINI_API_KEY"))

logger = get_logger(__name__)


class LLMClient:

    def __init__(self, model_name=DEFAULT_MODEL, max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
        self.model_name = model_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
    def call(self, prompt:str, **kargs) -> str:
        """Send Prompt to Gemini API"""
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    contents = prompt,
                    model = self.model_name,
                    **kargs
                )

                if response and response.text:
                    return response.text.strip()
                else:
                    raise Exception("Empty response recieved")
                
            except Exception as e :
                if attempt == self.max_retries :
                    raise Exception(f"API call failed after {self.max_retries + 1} attempts: {e}")

            time.sleep(self.retry_delay * (2 ** attempt))