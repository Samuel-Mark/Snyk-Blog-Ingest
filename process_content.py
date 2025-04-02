from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime
    
# 2A. Organises the posts into year_month categories.
def organise_by_date(formatted_posts):
    posts_by_date = {}
    for post in formatted_posts:
        year_month = f"{post['year']}_{post['month']:02d}"
        if year_month not in posts_by_date:
            posts_by_date[year_month] = []
        posts_by_date[year_month].append(post)
    return posts_by_date

# 2B. Extract useful data from the HTML content
def extract_posts(html_content):
    from main import url
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    
    for item in soup.find_all('div', class_='changelogItem'):
        title_tag = item.find('h2', class_='title').find('a')
        title = title_tag.get_text()
        path = title_tag['href']
        body = item.find('div', class_='content').get_text() if item.find('div', class_='content') else ''
        categories = [category.get_text() for category in item.find_all('h3', class_='category')]
        category = ', '.join(categories)
        
        date_published = item.find('time').get('datetime') if item.find('time') else ''

        link = url + path
        
        posts.append({
            'title': title,
            'url': link,
            'body': body,
            'category': category,
            'date_published': date_published
        })
    
    return posts

# 2C. Replace Unicode Charcters and Control Codes
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

# 2D. Return cleaned and formatted lists of posts.
def filter_and_format(posts):
    formatted_posts = []
    for post in posts:
        # 2E. Clean up Unicode Characters and get individual details.
        title = replace_unicode_characters(post['title'].strip())
        link = post['url']
        body = replace_unicode_characters(post['body'].strip())
        category = replace_unicode_characters(post['category'].strip())
        categories = category.split(', ')

        # Approach didn't work due to empty categeories?
        # while categories:
        #     for category in categories:
        #         if body.startswith(category):
        #             body = body[len(category):].strip()
        #             categories.remove(category)
        #             break

        # 2F. Remove each category from the body text.
        # Performed three times so can remove up to three categories.
        # Variation of above implementation may be better.
        loops = 3
        for num in range(loops):
            for categoryIndv in categories:
                if body.startswith(categoryIndv):
                    body = body[len(categoryIndv):].strip()
                    break
        
        body = replace_control_codes(body)
        
        # 2G. Extract year, month, day and time from string.
        date_published = post['date_published']
        if date_published:
            dt = datetime.fromisoformat(date_published)
            year = dt.year
            month = dt.month
            day = dt.day
            time = dt.time().isoformat()
        else:
            year = month = day = time = None
        
        # 2H. Add Post to formatted_posts.
        formatted_posts.append({
            'title': title,
            'link': link,
            'body': body,
            'category': category,
            'year': year,
            'month': month,
            'day': day,
            'time': time
        })
    
    return formatted_posts

# 7D. Returns ordinal for the number parsed through.
def get_ordinal_for_date(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]