import cohere
import json
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Load Module
co = cohere.Client(api_key=os.getenv("COHERENT_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
webAcc=DDGS()


def websearch(query: str):
    print("Query:", query)

    # Web search using DuckDuckGo (assuming webAcc.text is a function for this)
    text_results = webAcc.text(query, max_results=6)
    print("Results:\n", text_results)
    docs = [search['body'] for search in text_results]

    # Rerank results
    rerank_response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=docs,
        top_n=3
    )

    print("Reranked:", rerank_response)

    # Use the generative model for content generation
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("-" * 100)
    print("Response:")
    result = model.generate_content(
        f"""
        Based on this information: `{docs}` 
        and this question: `{query}`,
        respond to the user in a friendly manner.
        """
    )
    return result.text

def classify_query(user_query: str):


    # System prompt to classify the query
    system_prompt = f"""
    You are an AI classifier. Determine if the following question requires real-time or up-to-date knowledge to answer. Respond in JSON format as {{"results": "yes"}} if it requires real-time data, or {{"results": "no"}} if it does not. Do not provide any explanation.

    Question: "{user_query}"
    """
    # Generate classification using the generative model
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("-" * 100)
    print("Response:")
    classification_result =json.loads (model.generate_content(system_prompt).text)
    print(classification_result)

    
 
    if classification_result['results'] == "yes":
        # Websearch to get information
        logger.info(websearch(user_query))
    else:
        # Normal LLM query response
        logger.info(model.generate_content(user_query).text)



if __name__ == '__main__':
    while True:
        query = input("Ask me a question or press q to exit :")
        if query.lower() == "q":
            break
        classify_query(query)
    logger.warning(f"Exiting")