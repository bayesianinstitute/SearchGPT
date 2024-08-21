from bayesGPT.search import WebSearch
from bayesGPT.classify import QueryClassifier
from bayesGPT.model import GeminiModel
from loguru import logger

def main():
    model=GeminiModel()
    searcher = WebSearch()
    classifier = QueryClassifier(model=model)

    while True:
        query = input("Ask me a question or press q to exit: ")
        if query.lower() == "q":
            break

        if classifier.classify(query):
            prompt,webResult = searcher.search(query)
            result = model.generate_text(prompt)
            logger.info(f"LLM With Search result: {result}")
            # logger.debug(f'WeB Result : {webResult}')

            
        else:
            result = model.generate_text(query)
            logger.info(f"LLM Without Search result: {result}")

    logger.warning("Exiting")

if __name__ == '__main__':
    logger.add("logs/file_{time}.log",rotation="12:00")
    main()
