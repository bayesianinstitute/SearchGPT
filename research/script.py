import re
import os
from typing import List, Tuple, Union

from dotenv import load_dotenv

from googlesearch import search as google_search
from duckduckgo_search import DDGS

import requests
import json
import concurrent.futures

import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def fetch_search_results(query: str, max_results: int = 5, verbose: bool = False, search_engine: str = 'duckduckgo', format_output: bool = False) -> Union[Tuple[List[str], List[str], List[str]], str]:
    """Fetches search results for a given query using the specified search engine.

    Args:
        query: The search query to be executed.
        max_results: Maximum number of search results to fetch per sentence.
        verbose: Whether to print the progress of fetching search results.
        search_engine: The search engine to use, either 'google', 'duckduckgo', or 'serper' (default: 'duckduckgo')
        format_output: If True, returns the formatted response string. Otherwise, returns the URLs, titles, and descriptions

    Returns:
        If format_output is True, returns the formatted response string from format_response.
        Otherwise, returns a tuple containing lists of URLs, titles, and descriptions of the search results.
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', query)
    urls: List[str] = []
    titles: List[str] = []
    descriptions: List[str] = []
    
    if verbose:
        print(f"\033[92mQuery Breakdown:\033[0m")
        for i, sentence in enumerate(sentences):
            print(f"  {i+1}. {sentence}")

    
    def fetch_results_for_sentence(sentence: str):
        sentence_urls = []
        sentence_titles = []
        sentence_descriptions = []
        if verbose:
            print(f"\033[92mFetching results for sentence: {sentence} using {search_engine}\033[0m")

        if search_engine.lower() == 'google':
            results = google_search(sentence, num_results=max_results, advanced=True)
            for j, link in enumerate(results):
                if verbose:
                    print(f"  \033[94mResult {j+1}\033[0m")
                    print(f"    URL: {link['url']}")
                    print(f"    Title: {link['title']}")
                    print(f"    Description: {link['description']}")
                sentence_urls.append(link['url'])
                sentence_titles.append(link['title'])
                sentence_descriptions.append(link['description'])

        elif search_engine.lower() == 'duckduckgo':
            results = DDGS().text(sentence, max_results=max_results)
            for j, result in enumerate(results):
                if verbose:
                    print(f"  \033[94mResult {j+1}\033[0m")
                    print(f"    URL: {result['href']}")
                    print(f"    Title: {result['title']}")
                    print(f"    Description: {result['body']}")
                sentence_urls.append(result['href'])
                sentence_titles.append(result['title'])
                sentence_descriptions.append(result['body'])

        elif search_engine.lower() == 'serper':
            url = "https://google.serper.dev/search"
            payload = json.dumps({"q": sentence})
            headers = {
                'X-API-KEY': os.getenv("SERPER_API_KEY"),
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                for j, result in enumerate(data.get("organic", [])):
                    if j == max_results:
                        break
                    if verbose:
                        print(f"  \033[94mResult {j+1}\033[0m")
                        print(f"    URL: {result.get('link')}")
                        print(f"    Title: {result.get('title')}")
                        print(f"    Description: {result.get('snippet')}")
                    sentence_urls.append(result.get('link'))
                    sentence_titles.append(result.get('title'))
                    sentence_descriptions.append(result.get('snippet'))
        return sentence_urls, sentence_titles, sentence_descriptions

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fetch_results_for_sentence, sentences)

    for sentence_urls, sentence_titles, sentence_descriptions in results:
        urls.extend(sentence_urls)
        titles.extend(sentence_titles)
        descriptions.extend(sentence_descriptions)
  
    if format_output:
        return format_response(urls, titles, descriptions)  # Assuming you have a format_response function
    else:
        return urls, titles, descriptions
    
def format_response(query: str, descriptions: List[str], verbose: bool = False) -> str:
    """
    Formats the response to the search tool. 

    Args:
        query: The user's search query.
        descriptions: List of descriptions retrieved from the search tool.
        verbose: Whether to print the formatted response to console. 

    Returns:
        A formatted string containing the instructions and synthesized information.
    """
    
    formatted_response: str = """    
    ***Instructions***
    1. **Gather Information from Provided Sources**
        - Carefully read through all the provided sources.
        - Extract relevant information that directly answers or contributes to answering the query.
        - Ensure the information is accurate and comes from a reliable source.
    2. **Synthesize and Integrate Information**
        - Combine information from multiple sources if applicable. 
        - Ensure that the synthesized response is coherent and logically consistent.
        - Avoid redundancy and ensure the response flows naturally.
    3. **Use Knowledge Cutoff**
        - If the provided sources do not contain valuable or relevant information, then rely on your pre-existing knowledge up to the cutoff date.
        - Ensure that any information provided from your knowledge is accurate as of the last update in October 2023.
    4. **Acknowledge Knowledge Limits**
        - If the query pertains to information or events beyond your knowledge cutoff date, clearly state this to the user. 
        - Avoid providing speculative or unverified information.
    5. **Maintain Clarity and Precision** 
        - Ensure that the response is clear, precise, and directly answers the query.
        - Avoid unnecessary jargon and ensure the language is accessible to the user.
    ***Sources:***
    """

    for i, description in enumerate(descriptions):
        formatted_response = f"{description}\n" 
        
    formatted_response += f"\n**Query:** {query}"

    if verbose:
        print(formatted_response)

    return formatted_response

def main():
    while True:
        example_query = input("Enter your query (or type 'q' to exit): ")
        if example_query.lower() == "q":
            break

        formatted_output = fetch_search_results(
            example_query, 
            verbose=True, 
            search_engine="duckduckgo", 
            format_output=True
        )

        if formatted_output:
            print(formatted_output)

            model = genai.GenerativeModel('gemini-1.5-flash')

            print("-" * 100)
            response = model.generate_content(
                f"""
                Based on this information: `{formatted_output}` 
                and this question: `{example_query}`
                respond to the user in a friendly manner.
                """
            )
            print(response.text)
        else:
            print("No results found.")

if __name__ == "__main__":
    main()



