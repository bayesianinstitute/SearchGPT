from search import WebSearch
from classify import QueryClassifier
from loguru import logger

def main():
    searcher = WebSearch()
    classifier = QueryClassifier()

    while True:
        query = input("Ask me a question or press q to exit: ")
        if query.lower() == "q":
            break

        if classifier.classify(query):
            result = searcher.search(query)
            logger.info(f"Search result: {result}")
        else:
            result = classifier.model.generate_content(query).text
            logger.info(f"LLM result: {result}")

    logger.warning("Exiting")

if __name__ == '__main__':
    main()
