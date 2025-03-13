import sys
from static import fetch_static
from dynamic import fetch_dynamic
from process import extract_titles, filter_and_format

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
        titles = extract_titles(html_content)
        formatted_titles = filter_and_format(titles)
        for title in formatted_titles:
            print(title)

if __name__ == "__main__":
    main()