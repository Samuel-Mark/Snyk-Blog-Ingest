import sys
import json
from static import fetch_static
from dynamic import fetch_dynamic
from process import extract_posts, filter_and_format

def main():
    mode = 'static'
    
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    
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
        
        for year_month, posts in posts_by_date.items():
            with open(f'snky_updates_{year_month}.json', 'w', encoding='utf-8') as json_file:
                json.dump(posts, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()