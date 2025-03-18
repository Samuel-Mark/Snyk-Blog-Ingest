import os
from openai import OpenAI
from prompt import prompt
import pymsteams

modelChatGPT = 'gpt-4o-mini'
client = OpenAI(
    api_key=os.environ.get("OPEN_AI_API_KEY"),
)

ms_teams_webhook_url=os.environ.get("MS_TEAMS_WEBHOOK_URL")

def chatgpt_create_summary(title, category, body):
    if body:
        post = f'Title: {title}\nCategory: {category}\nBody: {body}\n'
        chat = client.responses.create(
            model=modelChatGPT, instructions=prompt, input=post
        )
        card = pymsteams.connectorcard(ms_teams_webhook_url)
        card.text(chat.output_text)
        assert card.send()