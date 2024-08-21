
# **Search LLM**

**Search LLM** is a Python-based project that combines the power of Large Language Models (LLMs) with web search to provide more accurate and contextually relevant answers. The project utilizes a variety of tools and frameworks, including DuckDuckGo for web search, Google Generative AI for text generation, and other utilities to streamline the development process.

## **Features**

- **Web Search Integration**: Leverages DuckDuckGo's search engine to fetch real-time information from the web.
- **LLM-based Text Generation**: Utilizes state-of-the-art language models for generating text based on user queries.
- **Asynchronous API**: FastAPI-based API for handling requests efficiently.
- **Logging**: Comprehensive logging using Loguru for monitoring and debugging.
- **Streamlit Frontend**: Easy-to-use web interface for interacting with the system.

## **Installation**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/bayesianinstitute/SearchGPT.git
    cd SearchGPT
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: `env\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install the Package**:
    ```bash
    python setup.py install
    ```

## **Usage**

1. **Run the FastAPI Server**:
    ```bash
    uvicorn app:app --reload
    ```

2. **Access the API**:
    Open your browser and navigate to `http://127.0.0.1:8000`. The API will be ready to accept queries.

3. **Example Request**:
    - **POST /ask**: Submit a query to the LLM with optional web search integration.
    
    ```bash
    curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"query":"What is the capital of France?"}'
    ```

## **Project Structure**

- `src/`: Contains the source code for the project.
- `app/`: Contains the source app code like UI and cli version.
- `backend/`: Contains the API Service.
- `requirements.txt`: Lists the Python packages required for the project.
- `setup.py`: Script for building and installing the package.

## **References**

- **[duckduckgo-search](https://pypi.org/project/duckduckgo-search/)**: A Python package for searching the web using DuckDuckGo's search engine without API keys.
- **[Loguru](https://loguru.readthedocs.io/)**: Loguru is a library that aims to bring enjoyable logging in Python. It offers a simple and easy-to-use syntax for logging.
- **[Google Generative AI](https://developers.generativeai.google/)**: This package allows interaction with Google's Generative AI models, providing access to powerful machine learning models for text generation and other tasks.
- **[Streamlit](https://docs.streamlit.io/)**: Streamlit is an open-source app framework in Python that lets you create beautiful, custom web apps for machine learning and data science.


