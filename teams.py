import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
ms_teams_webhook_url=os.getenv("MS_TEAMS_WEBHOOK_URL")

# 7C. Takes post date and creates an Adaptive Teams card to be sent via HTPP Post
def ms_teams_send_response(title, date, category, score, summary, link):
    headers = {
    # 7D. Send data in JSON format.
    "Content-Type": "application/json"
    }
    payload = {
        # 7E. Send data as an Adaptive Card.
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
                            # 7F. Add Italicised Date.
                            "type": "TextBlock",
                            "text": f"_{date}_",
                            "weight": "Lighter",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            # 7G. Add Large Title.
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Large",
                            "wrap": True
                        },
                        {
                            # 7H. Add Bold Category.
                            "type": "TextBlock",
                            "text": f"Category: {category}",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            # 7I. Add Bold Score.
                            "type": "TextBlock",
                            "text": f"Score: {score}/10",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True
                        },
                        {
                            # 7J. Add Summary.
                            "type": "TextBlock",
                            "text": summary,
                            "wrap": True
                        },
                        {
                            # 7K. Add Link.
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

    # 7L. Send data via post request and print error code if not Status 200 OK or Status 202 Recieved HTTP Request.
    response = requests.post(ms_teams_webhook_url, headers=headers, json=payload)
    if response.status_code != 200 and response.status_code != 202:
        print (f"Request failed: {response.status_code}, {response.text}")
