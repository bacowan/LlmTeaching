import openai
import os
from config import openapi_key, model
from frameworkModel import FrameworkModel
import logging
import random
from responder import ask_further_question

logging.basicConfig(filename='chat_logs.log', encoding='utf-8', level=logging.INFO)
random.seed(0)
  
openai.api_key = openapi_key

problemFiles = os.listdir("./problems")
responseFiles = os.listdir("./responses")
with open("./questions/initial_questions.txt", "r") as f:
    initialQuestions = f.readlines()

# Questions to ask: initial question, 5 questions in a category (categories are "on the right track",
#   "not on the right track" and "not sure").
# If the LLM doesn't give any useful information in that time, or the information is misleading, then
#   consider it a failure. Otherwise consider it a success.
# Compare to raw LLM responses of the same questions.
for problemFile in problemFiles:
    for responseFile in filter(lambda f : os.path.splitext(f)[0].startswith(os.path.splitext(problemFile)[0]), responseFiles):
        logging.info("Problem: " + problemFile + "; Response: " + responseFile)
        problem = open("./problems/" + problemFile, "r").read()
        code = open("./responses/" + responseFile, "r").read()
        for role in ["on the right track, but need a little nudge", "really stuck"]:
            initialQuestion = random.choice(initialQuestions)
            logging.info("VisibleQuestion: " + initialQuestion)

            model = FrameworkModel()
            response = model.start_conversation(problem, initialQuestion, code)
            logging.info("VisibleResponse: " + response)

            for _ in range(5):
                prompt = ask_further_question(model.conversation, role)
                logging.info("VisibleQuestion: " + prompt)
                response = model.send_prompt(prompt)
                logging.info("VisibleResponse: " + response)