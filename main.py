import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import calendar
from fetch_html import fetch_html_content
from process_content import organise_by_date, extract_posts, filter_and_format, get_ordinal_for_date
from process_json import update_json_files, save_latest_id, load_latest_id
from chatgpt import chatgpt_create_score, chatgpt_create_summary
from teams import ms_teams_send_response
    
load_dotenv(override=True)
url = 'https://updates.snyk.io'
output_dir = Path(os.getenv('PATH_TO_PROJECT'))
latest_id_json = output_dir / Path('latest-id.json')

def main():
    # Set then parse HTML Collection mode and Summary Generation arguments
    mode = 'static'
    generate_summaries = True
    
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        print(f"Running with HTML {mode} collection.")
    
    if len(sys.argv) >= 3:
        generate_summaries = sys.argv[2].lower() != 'no-gen'
        print(f"Summary generation is {'enabled' if generate_summaries else 'disabled'}.")

    # 1. Get HTML Content 
    html_content = fetch_html_content(url, mode)

    # 2. If content is found extract posts from it, then filter, format and organise them by month and year.
    if html_content:
        posts = extract_posts(html_content)
        formatted_posts = filter_and_format(posts)
        posts_by_date = organise_by_date(formatted_posts)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 3. Get the latest post if one is available
        latest_post_id = load_latest_id(latest_id_json)
        found = False
        # 4. If latest post is found, check that it's title is in scan of new posts otherwise print a warning.
        if latest_post_id:
            found = any(post['title'] == latest_post_id['title'] for post in formatted_posts)
            if not found:
                print(f"Latest post '{latest_post_id['title']}' dated {latest_post_id['date']} was not found in the import.")
        
        # 5. Update JSON files with gathered posts and store most recent one seperately
        latest_post = update_json_files(posts_by_date, output_dir)
        
        if formatted_posts:
            # 6. If posts have been found (and formatted) the one with the most recent date and time is obtained and saved.
            latest_post = max(formatted_posts, key=lambda x: (x['year'], x['month'], x['day'], x['time']))
            save_latest_id({'title': latest_post['title'], 'date': f"{latest_post['year']}-{latest_post['month']:02d}-{latest_post['day']:02d} {latest_post['time']}"}, latest_id_json)
            
            # 7. The order of post are again reversed for summary generation, and processed if the post is newer than the latest post
            formatted_posts.sort(key=lambda x: (x['year'], x['month'], x['day'], x['time']), reverse=False)
            
            if generate_summaries:
                for post in formatted_posts:
                    post_date = f"{post['year']}-{post['month']:02d}-{post['day']:02d} {post['time']}"
                    if not latest_post_id or post_date > latest_post_id['date']:
                        score = chatgpt_create_score(post['title'], post['category'], post['body'])
                        if int(score) < 7: summary = 'Snyk update does not meet impact criteria.'
                        else: summary = chatgpt_create_summary(post['title'], post['category'], post['body'])
                        ms_teams_send_response(post['title'],
                                            #    Date Start
                                               f"{calendar.day_name[calendar.weekday(post['year'], post['month'], post['day'])]} "
                                               f"{post['day']}{get_ordinal_for_date(post['day'])} "
                                               f"{calendar.month_name[post['month']]} {post['year']}",
                                            #    Date End
                                               post['category'], score, summary, post['link'])

if __name__ == "__main__":
    main()