import json

filename = 'snyk_updates/latest-id.json'

def save_latest_id(latest_post):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(latest_post, file, indent=4, ensure_ascii=False)

def load_latest_id():
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None