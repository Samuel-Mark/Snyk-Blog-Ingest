import os
from openai import OpenAI
from prompt import prompt
from dotenv import load_dotenv

load_dotenv(override=True)
modelChatGPT = 'gpt-4o-mini'
client = OpenAI(
    api_key=os.getenv("OPEN_AI_API_KEY"),
)

def chatgpt_create_summary(title, category, body, link):
    if body:
        post = f'Title: {title}\nCategory: {category}\nBody: {body}\nLink: {link}\n'
        chat = client.responses.create(
            model=modelChatGPT, instructions=prompt, input=post
        )
        
        return chat.output_text