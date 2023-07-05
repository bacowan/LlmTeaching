import openai
from config import openapi_key, model
from frameworkModel import FrameworkModel
import logging

logging.basicConfig(filename='chat_logs.log', encoding='utf-8', level=logging.INFO)
  
openai.api_key = openapi_key

problem = input("Please input the problem statement\n")
code = input("Please input your code so far\n")
question = input("Please pose your question to ChatGPT\n")

model = FrameworkModel()

print(model.start_conversation(problem, question, code))

prompt = input()
while prompt != "exit":
    print(model.send_prompt(prompt))
    prompt = input()