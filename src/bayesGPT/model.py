from bayesGPT.config import Config
from bayesGPT.constant import conversation
from loguru import logger
import google.generativeai as genai


class GeminiModel:
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        self.model_name = model_name
        self.model = self.load_model()
        

    def load_model(self) -> genai.GenerativeModel:
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            model = genai.GenerativeModel(self.model_name)
            logger.info(f"Model '{self.model_name}' loaded successfully.")
            return model
        except Exception as e:
            logger.exception("Error during model initialization.")
            raise
            
    def generate_text(self, prompt) -> str:
        try:
            response = self.model.generate_content(prompt)
            if hasattr(response, 'text'):
                return response.text
            else:
                logger.error(f"Unexpected response format: {response}")
                return "Unexpected response format."
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return "An error occurred while generating text."
        
    def chatAi(self, prompt, chat_history=None):
        if chat_history is None:
            chat_history = conversation.copy()  # Use a copy to avoid mutation issues

        try:
            # Append the user's message to the chat history
            chat_history.append({"role": "user", "parts": prompt})

            # Create a chat session with the current history
            chatSession = self.model.start_chat(history=chat_history)
            response = chatSession.send_message(prompt)

            # If the model generates a response, append it to the chat history
            if hasattr(response, 'text'):
                chat_history.append({"role": "model", "parts": response.text})
                return response.text, chat_history
            else:
                logger.error(f"Unexpected response format: {response}")
                return "Unexpected response format.", chat_history
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return "An error occurred while generating text.", chat_history

        
    def get_model(self) -> str:
        return self.model_name



def main():
    # Create an instance of GeminiModel
    gemini = GeminiModel()
    
    history=conversation.copy()
    while True:
        # Take input from the user
        prompt = input("Enter your question (or press 'q' to quit): ")
        
        # Check if the user wants to quit
        if prompt.lower() == 'q':
            print("Exiting the chat.")
            break
        
        # Generate a response using the chatAi method with the maintained chat history
        response,history = gemini.chatAi(prompt,history)
        

        print("Model:", response)
        print("Chat History:",history)
        



if __name__ == "__main__":
    main()
