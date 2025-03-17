from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime
from fetch_html import fetch_static, fetch_dynamic

def fetch_html_content(url, mode):
    if mode == 'static':
        return fetch_static(url)
    elif mode == 'dynamic':
        return fetch_dynamic(url)
    else:
        print("Invalid mode. Use 'static' or 'dynamic'.")
        return None
    
def organise_by_date(formatted_posts):
    posts_by_date = {}
    for post in formatted_posts:
        year_month = f"{post['year']}_{post['month']:02d}"
        if year_month not in posts_by_date:
            posts_by_date[year_month] = []
        posts_by_date[year_month].append(post)
    return posts_by_date

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
    replacements = {
        '\n': ' ',
        '\"': "'"
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)
    
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
        
        date_published = post['date_published']
        if date_published:
            dt = datetime.fromisoformat(date_published)
            year = dt.year
            month = dt.month
            day = dt.day
            time = dt.time().isoformat()
        else:
            year = month = day = time = None
        
        formatted_posts.append({
            'title': title,
            'body': body,
            'category': category,
            'year': year,
            'month': month,
            'day': day,
            'time': time
        })
    
    return formatted_posts