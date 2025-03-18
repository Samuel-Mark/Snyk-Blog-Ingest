import sys
from pathlib import Path
from process_content import fetch_html_content, organise_by_date, extract_posts, filter_and_format
from process_json import update_json_files, save_latest_id, load_latest_id

def main():
    mode = 'static'
    
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        print("NOTE: Only first argument is used.")
    
    url = 'https://updates.snyk.io'

    html_content = fetch_html_content(url, mode)

    if html_content:
        posts = extract_posts(html_content)
        formatted_posts = filter_and_format(posts)
        posts_by_date = organise_by_date(formatted_posts)
        
        output_dir = Path('snyk_updates')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        latest_post_id = load_latest_id()
        found = False
        if latest_post_id:
            found = any(post['title'] == latest_post_id['title'] for post in formatted_posts)
            if not found:
                print(f"Latest post '{latest_post_id['title']}' dated {latest_post_id['date']} was not found in the import.")
        
        latest_post = update_json_files(posts_by_date, output_dir)
        
        if formatted_posts:
            latest_post = max(formatted_posts, key=lambda x: (x['year'], x['month'], x['day'], x['time']))
            save_latest_id({'title': latest_post['title'], 'date': f"{latest_post['year']}-{latest_post['month']:02d}-{latest_post['day']:02d} {latest_post['time']}"})

if __name__ == "__main__":
    main()