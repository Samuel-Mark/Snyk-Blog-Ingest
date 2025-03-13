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
        
        with open('posts.json', 'w') as json_file:
            json.dump(formatted_posts, json_file, indent=4)
        
        print("Data has been exported to posts.json")

if __name__ == "__main__":
    main()