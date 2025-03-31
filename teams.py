import os
import requests

ms_teams_webhook_url=os.environ.get("MS_TEAMS_WEBHOOK_URL")

def ms_teams_send_response(chat):
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
                    "body": [ {
                            "type": "TextBlock",
                            "text": chat,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(ms_teams_webhook_url, headers=headers, json=payload)
    if response.status_code != 200 and response.status_code != 202:
        print (f"Request failed: {response.status_code}, {response.text}")
