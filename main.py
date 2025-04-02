import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import calendar
from fetch_html import fetch_html_content
from process_content import organise_by_date, extract_posts, filter_and_format
from process_json import update_json_files, save_latest_id, load_latest_id
from chatgpt import chatgpt_create_score, chatgpt_create_summary
from teams import ms_teams_send_response
    
load_dotenv(override=True)
url = 'https://updates.snyk.io'
output_dir = Path(os.getenv('PATH_TO_PROJECT'))
latest_id_json = output_dir / Path('latest-id.json')

def main():
    mode = 'static'
    generate_summaries = True
    
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        print(f"Running with HTML {mode} collection.")
    
    if len(sys.argv) >= 3:
        generate_summaries = sys.argv[2].lower() != 'no-gen'
        print(f"Summary generation is {'enabled' if generate_summaries else 'disabled'}.")

    html_content = fetch_html_content(url, mode)

    if html_content:
        posts = extract_posts(html_content)
        formatted_posts = filter_and_format(posts)
        posts_by_date = organise_by_date(formatted_posts)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        latest_post_id = load_latest_id(latest_id_json)
        found = False
        if latest_post_id:
            found = any(post['title'] == latest_post_id['title'] for post in formatted_posts)
            if not found:
                print(f"Latest post '{latest_post_id['title']}' dated {latest_post_id['date']} was not found in the import.")
        
        latest_post = update_json_files(posts_by_date, output_dir)
        
        if formatted_posts:
            latest_post = max(formatted_posts, key=lambda x: (x['year'], x['month'], x['day'], x['time']))
            save_latest_id({'title': latest_post['title'], 'date': f"{latest_post['year']}-{latest_post['month']:02d}-{latest_post['day']:02d} {latest_post['time']}"}, latest_id_json)
            
            # Undo reversal for order of summary generation.
            formatted_posts.sort(key=lambda x: (x['year'], x['month'], x['day'], x['time']), reverse=False)
            
            if generate_summaries:
                for post in formatted_posts:
                    post_date = f"{post['year']}-{post['month']:02d}-{post['day']:02d} {post['time']}"
                    if not latest_post_id or post_date > latest_post_id['date']:
                        score = chatgpt_create_score(post['title'], post['category'], post['body'])
                        summary = chatgpt_create_summary(score, post['title'], post['category'], post['body'])
                        ms_teams_send_response(post['title'], f"{post['day']:02d} {calendar.month_name[post['month']]} {post['year']}", post['category'], score, summary, post['link'])

if __name__ == "__main__":
    main()