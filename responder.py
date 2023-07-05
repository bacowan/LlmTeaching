import openai
from config import model
import logging

class Responder():
    def ask_question(self, question, conversation):
        newConversation = conversation.copy()
        newConversation.append({"role": "user", "content": question})
        response = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        responseText = response['choices'][0]['message']['content']
        logging.info("Get Question: " + question)
        logging.info("Response question: " + responseText)
        return responseText
