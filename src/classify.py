import json
from config import Config
from loguru import logger
import google.generativeai as genai

class QueryClassifier:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def classify(self, user_query: str):
        system_prompt = f"""
        You are an AI classifier. Determine if the following question requires real-time or up-to-date knowledge to answer. Respond in JSON format as {{"results": "yes"}} if it requires real-time data, or {{"results": "no"}} if it does not. Do not provide any explanation.

        Question: "{user_query}"
        """
        classification_result = json.loads(self.model.generate_content(system_prompt).text)
        logger.info(f"Classification result: {classification_result}")

        return classification_result['results'] == "yes"
