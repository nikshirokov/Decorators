# Определяем список ключевых слов:
from logger import logger
import requests
import bs4

KEYWORDS = ['сети', 'парсер', 'телеграм', 'Python', 'SQL']

DATA_URL = 'https://habr.com/ru/articles/'


@logger
def web_scrapping(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features='lxml')

    articles = []
    articles_list = soup.findAll('article', class_='tm-articles-list__item')
    for article in articles_list:
        link = f"https://habr.com{article.find('a', class_='tm-title__link')['href']}"
        response = requests.get(link)
        soup = bs4.BeautifulSoup(response.text, features='lxml')
        title = soup.find('h1').text
        text = soup.find('div', id='post-content-body').text
        time = soup.find('time')['title']
        for word in KEYWORDS:
            if word in title or word in text:
                aricle_ = [time, title, link]
                articles.append(aricle_)
                break
    for i in articles:
        write_to_file('articles.txt', ' '.join(i))
    return f'Найдено {len(articles)} статьи(ей)'

@logger
def write_to_file(file, text):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(text + '\n')
    return 'Запись в файл успешна'

if __name__ == '__main__':
    web_scrapping(DATA_URL)
