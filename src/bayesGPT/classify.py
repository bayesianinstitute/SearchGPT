import json
from loguru import logger
from bayesGPT.model import GeminiModel
from typing import Optional

class QueryClassifier:
    def __init__(self,model:Optional[GeminiModel]=None):
        self.model=model or GeminiModel()

    def classify(self, user_query: str):
        """
        Classify if a given user query requires real-time or up-to-date knowledge.
        returns True if the query is valid, False otherwise
        """
        system_prompt = f"""
        You are an AI classifier. Determine if the following question requires real-time or up-to-date knowledge to answer. Respond in JSON format as {{"results": "yes"}} if it requires real-time data, or {{"results": "no"}} if it does not. Do not provide any explanation.

        Question: "{user_query}"
        """

        response = self.model.generate_text(prompt=system_prompt)
        try:
            classification_result = json.loads(response)

            if "results"  not in classification_result :
                logger.error(f"Unexpected response structure: {classification_result}")
                return False
            logger.info(f"Classification result: {classification_result}")
            return classification_result['results'] == "yes"
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response}")
            return False
        
