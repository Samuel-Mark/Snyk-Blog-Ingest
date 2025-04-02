import os
from openai import OpenAI
from prompt import promptPreamble, promptScore, promptSummary
from dotenv import load_dotenv

load_dotenv(override=True)
modelChatGPT = 'gpt-4o-mini'
client = OpenAI(
    api_key=os.getenv("OPEN_AI_API_KEY"),
)

# 7A. Create and return a string containing the score for a post.
def chatgpt_create_score(title, category, body):
    if body:
        post = f'Title: {title}\nCategory: {category}\nBody: {body}'
        chat = client.responses.create(
            model=modelChatGPT, instructions=f"{promptPreamble} {promptScore}", input=post
        )
        
        return chat.output_text

# 7B. Create and return a summary string for a post.
def chatgpt_create_summary(title, category, body):
    if body:
        post = f'Title: {title}\nCategory: {category}\nBody: {body}\n'
        chat = client.responses.create(
            model=modelChatGPT, instructions=f"{promptPreamble} {promptSummary}", input=post
        )
        
        return chat.output_text