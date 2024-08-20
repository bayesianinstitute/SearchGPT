import streamlit as st
import cohere
import google.generativeai as genai
from duckduckgo_search import DDGS
from dotenv import load_dotenv
import os
import json
from loguru import logger

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize APIs
co = cohere.Client(api_key=os.getenv("COHERENT_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')
webAcc = DDGS()

def websearch(query: str):
    """Perform a web search and generate a response."""
    logger.info(f"Websearch Query: {query}")

    # Web search using DuckDuckGo
    text_results = webAcc.text(query, max_results=6)
    logger.debug(f"Websearch Results: {text_results}")
    docs = [search['body'] for search in text_results]

    # Rerank search results using Cohere
    rerank_response = co.rerank(
        model="rerank-english-v3.0",
        query=query,
        documents=docs,
        top_n=3
    )
    logger.debug(f"Reranked Results: {rerank_response}")

    # Generate response using Google Gemini
    result = model.generate_content(
        f"""
        Based on this information: `{docs}` 
        and this question: `{query}`,
        respond to the user in a friendly manner.
        """
    )
    return result.text

def classify_query(user_query: str):
    """Classify if the query needs real-time data and get the appropriate response."""
    # System prompt to classify the query
    system_prompt = f"""
    You are an AI classifier. Determine if the following question requires real-time or up-to-date knowledge to answer. Respond in JSON format as {{"results": "yes"}} if it requires real-time data, or {{"results": "no"}} if it does not. Do not provide any explanation.

    Question: "{user_query}"
    """
    # Generate classification using the generative model
    classification_result = json.loads(model.generate_content(system_prompt).text)
    logger.debug(f"Classification Result: {classification_result}")

    if classification_result['results'] == "yes":
        # Websearch to get information
        return websearch(user_query)
    else:
        # Normal LLM query response
        return model.generate_content(user_query).text

# Streamlit app title
st.title("Web Access LLM")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Enter your question:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = classify_query(prompt)
            st.markdown(response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
