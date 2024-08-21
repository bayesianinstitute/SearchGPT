from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from bayesGPT.search import WebSearch
from bayesGPT.classify import QueryClassifier
from bayesGPT.model import GeminiModel
from loguru import logger

logger.add("logs/file_{time}.log", rotation="12:00")

app = FastAPI()

# Initialize objects outside the endpoint for performance
model = GeminiModel()
searcher = WebSearch()
classifier = QueryClassifier(model=model)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LLM with Search API!"}

@app.post("/ask")
async def ask(request: QueryRequest):
    """
    Endpoint to handle user queries.
    Expects a JSON payload with a "query" key.
    """
    try:
        query = request.query
        if not query:
            raise HTTPException(status_code=400, detail='Missing "query" parameter')

        if classifier.classify(query):
            prompt, webResult = searcher.search(query)
            result = model.generate_text(prompt)
            response = {
                "result": result,
                "webResult": webResult,
            }
            logger.info(f"LLM With Search result: {result}")
        else:
            result = model.generate_text(query)
            response = {
                "result": result,
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
        if not query:
            raise HTTPException(status_code=400, detail='Missing "query" parameter')

        prompt, webResult = searcher.search(query)
        result = model.generate_text(prompt)
        response = {
            "result": result,
            "webResult": webResult,
        }
        logger.info(f"LLM With Search result: {result}")


        return response

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail='Internal server error')

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") # Production
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info") # Development

