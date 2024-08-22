import streamlit as st
import requests
from loguru import logger

logger.add("logs/file_{time}.log", rotation="12:00")

# Define the FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000"

st.title("LLM with Search API")

st.write("This app interacts with the FastAPI service to handle user queries and provide responses.")

def main():
    # Initialize session state for messages and history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "history" not in st.session_state:
        st.session_state.history = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"])

    # Input field for user query
    if prompt := st.chat_input("Enter your query:"):
        st.session_state.messages.append({"role": "user", "parts": prompt})
        st.session_state.history.append(prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("ai"):
            try:
                # POST request to the /ask/history endpoint
                response = requests.post(f"{API_URL}/ask/history", json={"query": prompt, "history": st.session_state.messages})
                data = response.json()
                if response.status_code == 200:
                    result_message = data.get('result')
                    web_results = data.get('webResult')

                    st.session_state.messages.append({"role": "model", "parts": result_message})
                    st.markdown(result_message)

                    if web_results:
                        with st.expander("Web Results"):
                            for item in web_results:
                                st.markdown(f"### [{item['title']}]({item['href']})")
                                st.markdown(f"{item['body']}")
                                st.markdown("---")
                    
                    logger.info("Request successful")
                else:
                    error_message = f"Error: {data.get('detail')}"
                    st.session_state.messages.append({"role": "model", "parts": error_message})
                    logger.error("Request Failed")

            except requests.RequestException as e:
                st.session_state.messages.append({"role": "model", "parts": f"Request failed: {e}"})

if __name__ == "__main__":
    main()
