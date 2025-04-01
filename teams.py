import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
ms_teams_webhook_url=os.getenv("MS_TEAMS_WEBHOOK_URL")

def ms_teams_send_response(title, date, category, grade, summary, link):
    headers = {
    "Content-Type": "application/json"
    }
    payload = {
        "type": "message",
        "attachments": [ {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.5",
                    "msteams": {
                        "width": "Full",
                        "height": "stretch"
                    },
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Large",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"Date: {date}",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"Category: {category}",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"Score: {grade}/10",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": summary,
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "text": f"[See the Original Update]({link})",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                    ]
                }
            }
        ]
    }

    response = requests.post(ms_teams_webhook_url, headers=headers, json=payload)
    if response.status_code != 200 and response.status_code != 202:
        print (f"Request failed: {response.status_code}, {response.text}")
