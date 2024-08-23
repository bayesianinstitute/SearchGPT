from fastapi import FastAPI, HTTPException
from models import QueryRequest

from bayesGPT.search import WebSearch
from bayesGPT.classify import QueryClassifier
from bayesGPT.model import GeminiModel
from loguru import logger

logger.add("logs/file_{time}.log", rotation="12:00")

app = FastAPI()

# Initialize Module 
model = GeminiModel()
searcher = WebSearch()
classifier = QueryClassifier(model=model)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LLM with Search API!"}

@app.post("/ask/history")
async def history(request: QueryRequest):
    """
    Endpoint to handle user queries.
    Expects a JSON payload with a "query" key.
    """
    try:
        query = request.query
        history = request.history

        if not history:
            raise HTTPException(status_code=400, detail='Missing "history" parameter')

        if not query:
            raise HTTPException(status_code=400, detail='Missing "query" parameter')

        if classifier.classify(query):
            new_query = classifier.generate_web_query(query, history)
            logger.debug(f"new_query{new_query}")
            prompt, webResult = searcher.search(new_query)
            logger.debug(f"Search result: {webResult}")

            result, hist = model.chatAi(prompt, history)

            response = {
                "result": result,
                "hist": hist,
                "webResult": webResult,
            }
            logger.info(f"LLM With Search result: {result}")
        else:
            result, hist = model.chatAi(query, history)
            response = {
                "result": result,
                "history": hist,
            }
            logger.info(f"LLM Without Search result: {result}")

        return response

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail='Internal server error')

@app.post("/ask/search")
async def web(request: QueryRequest):
    """
    Endpoint to handle user queries.
    Expects a JSON payload with a "query" key.
    """
    try:
        query = request.query
        history = request.history  # Added history parameter

        if not query:
            raise HTTPException(status_code=400, detail='Missing "query" parameter')

        prompt, webResult = searcher.search(query)
        result, hist = model.chatAi(prompt, history)  # Use history here
        response = {
            "result": result,
            "hist": hist,
            "webResult": webResult,
        }
        logger.info(f"LLM With Search result: {result}")

        return response

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail='Internal server error')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") # Production
    # uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info") # Development
