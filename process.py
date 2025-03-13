from bs4 import BeautifulSoup
from unidecode import unidecode

def extract_posts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    
    for item in soup.find_all('div', class_='changelogItem'):
        title = item.find('h2', class_='title').get_text()
        body = item.find('div', class_='content').get_text() if item.find('div', class_='content') else ''
        category = item.find('h3', class_='category').get_text() if item.find('h3', class_='category') else ''
        date_published = item.find('time').get('datetime') if item.find('time') else ''
        
        posts.append({
            'title': title,
            'body': body,
            'category': category,
            'date_published': date_published
        })
    
    return posts

def replace_unicode_characters(text):
    return unidecode(text)

def replace_control_codes(text):
    text = text.replace('\\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\"', "'")
    return text

def filter_and_format(posts):
    formatted_posts = []
    for post in posts:
        title = replace_unicode_characters(post['title'].strip().title())
        body = replace_unicode_characters(post['body'].strip())
        category = replace_unicode_characters(post['category'].strip())
        
        if body.startswith(category):
            body = body[len(category):].strip()
        
        body = replace_control_codes(body)
        
        formatted_posts.append({
            'title': title,
            'body': body,
            'category': category,
            'date_published': post['date_published']
        })
    
    return formatted_posts