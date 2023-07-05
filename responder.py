import openai
from config import model
import logging

def ask_further_question(conversation, role):
    return ask_question("Give me a sample response, but pretend you're a student who's " + role + ". Do so by completing the statement: \"My answer to your question is as follows:\"", conversation)

def ask_question(question, conversation):
    newConversation = conversation.copy()
    newConversation.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model=model,
        messages=newConversation
    )
    responseText = response['choices'][0]['message']['content']
    logging.info("GetQuestion: " + question)
    logging.info("ResponseQuestion: " + responseText)
    return responseText
