import openai
from config import model
import logging

logging.basicConfig(filename='chat_logs.log', encoding='utf-8', level=logging.INFO)

class FrameworkModel():
    def __init__(self, maxRetryCount=2):
        self.maxRetryCount = maxRetryCount

    def start_conversation(self, problem, question, code):
        self.conversation = []
        prompt = "I have been given the following instructions:\n"\
            + problem + "\n\n"\
            + "I have written the following code:\n"\
            + code + "\n\n"\
            + question + "\n"\
            + "I would like you to act as a teacher: "\
            + "ask me questions about why I have implemented "\
            + "the code this way in order for me to come to the conclusion myself. "\
            + "Ask me the questions one at a time."
        
        return self.__chat(prompt)
    
    def send_prompt(self, prompt):
        is_valid = self.__validate_prompt(prompt)
        if (is_valid):
            fullPrompt = prompt + "\n"\
                + "Remember to act as a teacher: don't give me any explicit answers."
            return self.__chat(fullPrompt)
        else:
            return self.__chat("Can you please rephrase?")
    
    def __validate_prompt(self, prompt):
        response = self.__chat("Does this answer your question (even if the answer is incorrect)? "\
                                + "\"" + prompt + "\""\
                                + ". Please answer with a simple yes or no.")
        return "yes" in response.lower()

    def __chat(self, prompt):
        #for _ in range(self.maxRetryCount):
        self.conversation.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.conversation
        )
        responseText = response['choices'][0]['message']['content']
        logging.info("Prompt: " + prompt)
        logging.info("Response: " + responseText)
        #if (self.__validate_response(responseText)):
        self.conversation.append({"role": "assistant", "content": responseText})
        return responseText
        #return responseText
    
    def __validate_response(self, response):
        return not response.startswith("#CODE#")