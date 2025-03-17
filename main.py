import sys
import json
from static import fetch_static
from dynamic import fetch_dynamic
from process import extract_posts, filter_and_format
from latest import save_latest_id, load_latest_id
from pathlib import Path

def main():
    mode = 'static'
    
    if len(sys.argv) > 2:
        mode = sys.argv[1]
        print("Only first argument is used.")
    
    url = 'https://updates.snyk.io'

    if mode == 'static':
        html_content = fetch_static(url)
    elif mode == 'dynamic':
        html_content = fetch_dynamic(url)
    else:
        print("Invalid mode. Use 'static' or 'dynamic'.")
        return

    if html_content:
        posts = extract_posts(html_content)
        formatted_posts = filter_and_format(posts)
        
        posts_by_date = {}
        for post in formatted_posts:
            year_month = f"{post['year']}_{post['month']:02d}"
            if year_month not in posts_by_date:
                posts_by_date[year_month] = []
            posts_by_date[year_month].append(post)
        
        output_dir = Path('snyk_updates')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        latest_post_id = load_latest_id()
        found = False
        if latest_post_id:
            found = any(post['title'] == latest_post_id['title'] for post in formatted_posts)
            if not found:
                print(f"Latest post '{latest_post_id['title']}' dated {latest_post_id['date']} was not found in the import.")
        
        latest_post = None
        for year_month, new_posts in posts_by_date.items():
            json_file_path = output_dir / f'snyk_{year_month}.json'
            
            if json_file_path.exists():
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    existing_posts = json.load(json_file)
            else:
                existing_posts = []
            
            # key-value pairs of existing posts
            existing_posts_dict = {post['title']: post for post in existing_posts}
            
            # sort by year, month, day, and time in descending order
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
        
        if formatted_posts:
            latest_post = max(formatted_posts, key=lambda x: (x['year'], x['month'], x['day'], x['time']))
            save_latest_id({'title': latest_post['title'], 'date': f"{latest_post['year']}-{latest_post['month']:02d}-{latest_post['day']:02d} {latest_post['time']}"})

if __name__ == "__main__":
    main()