import openai
import os
from config import openapi_key, model
from frameworkModel import FrameworkModel
import logging
import random
from responder import ask_further_question

random.seed(0)

item = input("Which file to test? ")
problem = open("./problems/" + item + ".txt").read()
code = open("./code/" + item + ".txt").read()
question = open("./questions/" + item + ".txt").read()

student_type = input("Should the suggested questions be 1. for a student on the right track, or 2. for a student who feels lost? ")
if student_type == "1":
    logname = 'chat_logs_' + item + '_1.log'
    role = "on the right track, but need a little nudge"
elif student_type == "2":
    logname = 'chat_logs_' + item + '_2.log'
    role = "really stuck"
else:
    print("invalid role")
    exit()

logging.basicConfig(filename=logname, encoding='utf-8', level=logging.INFO)

print("Item: " + item)
print("Problem: " + problem)
print("Code: " + code)
print("Question: " + question)
  
openai.api_key = openapi_key

# Questions to ask: initial question, 5 questions in a category (categories are "on the right track",
#   "not on the right track" and "not sure").
# Questions are from here: https://www.geeksforgeeks.org/python-exercises-practice-questions-and-solutions/
# Get the LLM to suggest questions, and use those if they're reasonable use them. Otherwise get the LLM to
#   suggest a different question instead.
# If the LLM doesn't give any useful information in that time, or the information is misleading, then
#   consider it a failure. Otherwise consider it a success.
# Compare to raw LLM responses of the same questions.

logging.info("Problem: " + item)
initialQuestion = "Please help"
logging.info("VisibleQuestion: " + initialQuestion)

model = FrameworkModel()
response = model.start_conversation(problem, initialQuestion, code)
logging.info("VisibleResponse: " + response)
print(response)

for _ in range(5):
    retry = True
    while retry == True:
        try:
            newPrompt = ""
            while newPrompt == "":
                prompt = ask_further_question(model.conversation, role)
                logging.info("SuggestedQuestion: " + prompt)
                print("Suggested prompt:")
                print(prompt)
                newPrompt = input("New prompt: ")
            logging.info("VisibleQuestion: " + newPrompt)
            response = model.send_prompt(newPrompt)
            logging.info("VisibleResponse: " + response)
            print(response)
            retry = False
        except:
            print("oops; trying again")
            retry = True