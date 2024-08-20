import cohere
from duckduckgo_search import DDGS
from config import Config
from loguru import logger
import google.generativeai as genai

class WebSearch:
    def __init__(self):
        self.co = cohere.Client(api_key=Config.COHERENT_API_KEY)
        self.model = 'gemini-1.5-flash'
        self.webAcc = DDGS()
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def search(self, query: str,max_results=6):
        logger.info(f"Performing web search for query: {query}")
        text_results = self.webAcc.text(query, max_results=max_results)
        docs = [search['body'] for search in text_results]

        rerank_response = self.co.rerank(
            model="rerank-english-v3.0",
            query=query,
            documents=docs,
            top_n=3
        )

        logger.info(f"Reranked results: {rerank_response}")

        result = self.generate_content(docs, query)
        return result.text

    def generate_content(self, docs, query):
        
        print("-" * 100)
        print("Response:")
        result = self.model.generate_content(
            f"""
            Based on this information: `{docs}` 
            and this question: `{query}`,
            respond to the user in a friendly manner.
            """
        )
        return result
        # Implement the logic to generate content based on docs and query
        pass
