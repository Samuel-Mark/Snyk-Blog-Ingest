import os
import pymsteams

ms_teams_webhook_url=os.environ.get("MS_TEAMS_WEBHOOK_URL")

def ms_teams_swnd_response(chat):
    card = pymsteams.connectorcard(ms_teams_webhook_url)
    card.text(chat)
    assert card.send()