import cohere
from duckduckgo_search import DDGS
from bayesGPT.config import Config
from loguru import logger


class WebSearch:
    def __init__(self):
        # self.co = cohere.Client(api_key=Config.COHERENT_API_KEY)
        self.webAcc = self.load()

    def load(self)->DDGS:
        try:
            search=DDGS()
            logger.info("Searching Module loaded Successfully")
            return search
        except Exception as e:
            logger.error(f"Error occurred while loading search module: {e}")
            raise

    def search(self, query: str,max_results=6)->str:
        """
        Perform a web search using DuckDuckGo and return new Prompt.
        """
        logger.info(f"Performing web search for query: {query}")
        text_results = self.webAcc.text(query, max_results=max_results)
        description = [result.get('body') for result in text_results]
        # links = [result.get('href') for result in text_results]
        # titles = [result.get('title') for result in text_results]
        # logger.debug(f"Searching results : {text_results}")

        # rerank_response = self.co.rerank(
        #     model="rerank-english-v3.0",
        #     query=query,
        #     documents=docs,
        #     top_n=3
        # )

        # logger.info(f"Reranked results: {rerank_response}")
        system_prompt=f"""
            Based on this Web information: `{text_results}` 
            and this question: `{query}`,
            respond to the user in a friendly manner.
            """
        return system_prompt,text_results


if __name__ == '__main__':
    search = WebSearch()
    query = "What is the history of the Eiffel Tower?"
    print(search.search(query))