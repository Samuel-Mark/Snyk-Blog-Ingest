import json

def update_json_files(posts_by_date, output_dir):
    latest_post = None
    for year_month, new_posts in posts_by_date.items():
        json_file_path = output_dir / f'snyk_{year_month}.json'
        
        if json_file_path.exists():
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                existing_posts = json.load(json_file)
        else:
            existing_posts = []
        
        # key-value pairs of existing posts and sort by year, month, day, and time in descending order
        existing_posts_dict = {post['title']: post for post in existing_posts}
        new_posts.sort(key=lambda x: (x['year'], x['month'], x['day'], x['time']), reverse=True)
        
        # update existing or add new
        for new_post in new_posts:
            if new_post['title'] in existing_posts_dict:
                existing_post = existing_posts_dict[new_post['title']]
                if new_post['body'] != existing_post['body']:
                    existing_posts_dict[new_post['title']] = new_post
            else:
                existing_posts_dict[new_post['title']] = new_post
        
        updated_posts = sorted(existing_posts_dict.values(), key=lambda x: (x['year'], x['month'], x['day'], x['time']))
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(updated_posts, json_file, indent=4, ensure_ascii=False)
        
        # track most recnt post
        if not latest_post or (new_posts and new_posts[0]['year'] >= latest_post['year'] and new_posts[0]['month'] >= latest_post['month'] and new_posts[0]['day'] >= latest_post['day'] and new_posts[0]['time'] >= latest_post['time']):
            latest_post = new_posts[0]
    
    return latest_post

def save_latest_id(latest_post, latest_id_json):
    with open(latest_id_json, 'w', encoding='utf-8') as file:
        json.dump(latest_post, file, indent=4, ensure_ascii=False)

def load_latest_id(latest_id_json):
    try:
        with open(latest_id_json, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None