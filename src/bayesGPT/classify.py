import json
from loguru import logger
from bayesGPT.model import GeminiModel
from typing import Optional

class QueryClassifier:
    def __init__(self,model:Optional[GeminiModel]=None):
        self.model=model or GeminiModel()


    def generate_web_query(self, user_query: str, chat_history: list) -> str:
        """
        Generates a new web search query based on the user query and chat history.

        This method leverages the GeminiModel to create a refined search query.
        It provides a clear and concise prompt to the model, specifying the desired output format.

        Args:
            user_query (str): The original user query.
            chat_history (list): A list of previous user and assistant interactions.

        Returns:
            str: A refined web search query suitable for DuckDuckGo.
        """
        system_prompt = f"""
        You are a helpful AI assistant tasked with improving web search queries. 
        Given the user query and chat history, generate a concise and relevant search query for DuckDuckGo.

        User Query: "{user_query}"
        Chat History: {chat_history}

        Generate a query that focuses on the key information from the user's intent. 
        Keep it simple and avoid unnecessary words or phrases.
        """
        try:
            response = self.model.generate_text(prompt=system_prompt)
            return response.strip() 

        except Exception as e:
            logger.error(f"Failed to generate new web search query: {e}")
            return user_query
    
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
        