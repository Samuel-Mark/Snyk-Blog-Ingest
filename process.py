from bs4 import BeautifulSoup

def extract_titles(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    titles = [title.get_text() for title in soup.find_all('h2', class_='title')]
    return titles

def filter_and_format(titles):
    formatted_titles = [title.strip().title() for title in titles if title]
    return formatted_titles