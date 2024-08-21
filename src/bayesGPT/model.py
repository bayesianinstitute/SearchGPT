from bayesGPT.config import Config
from loguru import logger
import google.generativeai as genai

class GeminiModel:
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        self.model_name = model_name
        self.model = self.load_model()

    def load_model(self) -> genai.GenerativeModel:
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model= genai.GenerativeModel(self.model_name)
            logger.info(f"Model '{self.model_name}' loaded successfully.")
            return model
        except Exception as e:
            logger.exception("Error during model initialization.")
            raise
            
    def generate_text(self, prompt)->str:
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, 'text'):
                return response.text
            else:
                logger.error(f"Unexpected response format: {response}")
                return "Unexpected response format."
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return "An error occurred while generating text."
        
    def get_model(self) -> str:
        return self.model_name