import sys
import json
from static import fetch_static
from dynamic import fetch_dynamic
from process import extract_posts, filter_and_format
from pathlib import Path

def main():
    mode = 'static'
    
    if len(sys.argv) >= 2:
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

if __name__ == "__main__":
    main()