import json

# 5A. Create files for eacj month per year, containing the posts from them.
def update_json_files(posts_by_date, output_dir):
    latest_post = None
    for year_month, new_posts in posts_by_date.items():
        json_file_path = output_dir / f'snyk_{year_month}.json'
        
        if json_file_path.exists():
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                existing_posts = json.load(json_file)
        else:
            existing_posts = []
        
        # 5B. Creates key-value pairs of title and post data for existing posts and sort them by year, month, day, and time in descending order
        existing_posts_dict = {post['title']: post for post in existing_posts}
        new_posts.sort(key=lambda x: (x['year'], x['month'], x['day'], x['time']), reverse=True)
        
        # 5C. Update existing posts by title or add new posts that were found.
        for new_post in new_posts:
            if new_post['title'] in existing_posts_dict:
                existing_post = existing_posts_dict[new_post['title']]
                if new_post['body'] != existing_post['body']:
                    existing_posts_dict[new_post['title']] = new_post
            else:
                existing_posts_dict[new_post['title']] = new_post
        
        # 5D. Sort existing post data by post date and then save in the relevant file.
        updated_posts = sorted(existing_posts_dict.values(), key=lambda x: (x['year'], x['month'], x['day'], x['time']))
        
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(updated_posts, json_file, indent=4, ensure_ascii=False)
        
        # 5E. Track the most recent post and return it after loop is completed.
        if not latest_post or (new_posts and new_posts[0]['year'] >= latest_post['year'] and new_posts[0]['month'] >= latest_post['month'] and new_posts[0]['day'] >= latest_post['day'] and new_posts[0]['time'] >= latest_post['time']):
            latest_post = new_posts[0]
    
    return latest_post

# 6A. Save the latest post in the Latest Post JSON
def save_latest_id(latest_post, latest_id_json):
    with open(latest_id_json, 'w', encoding='utf-8') as file:
        json.dump(latest_post, file, indent=4, ensure_ascii=False)

# 3A. Open and load the Latest Post JSON
def load_latest_id(latest_id_json):
    try:
        with open(latest_id_json, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None