import streamlit as st
import requests
from loguru import logger

logger.add("logs/file_{time}.log", rotation="12:00")





# Define the FastAPI endpoint URLs
API_URL = "http://127.0.0.1:8000"

st.title("LLM with Search API")

st.write("This app interacts with the FastAPI service to handle user queries and provide responses.")

def main():
        
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user query
    if prompt := st.chat_input("Enter your query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
                
            try:
                # POST request to the /ask endpoint
                response = requests.post(f"{API_URL}/ask", json={"query": prompt})
                data = response.json()
                if response.status_code == 200:
                    result_message = data.get('result')
                    web_result_message = data.get('webResult')
                    st.session_state.messages.append({"role": "assistant", "content": result_message})
                    # st.session_state.messages.append({"role": "assistant", "content": web_result_message})
                    st.markdown(result_message)

                    if web_result_message:
                        with st.expander("web_result"):
                            st.markdown(web_result_message)
                    logger.info("Request successful")
                else:
                    error_message = f"Error: {data.get('detail')}"
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
                    logger.error("Request Failed")

            except requests.RequestException as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Request failed: {e}"})


if __name__ == "__main__":
    main()