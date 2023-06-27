import openai
from config import openapi_key, model
  
openai.api_key = openapi_key

response = openai.ChatCompletion.create(
    model=model,
    messages={"role": "user", "content": "Hello, chatGPT!"}
)

print(response)