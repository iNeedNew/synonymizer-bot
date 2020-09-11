import requests
from bs4 import BeautifulSoup as bs


def generate_url(clean_url, word):
    """Сгенерировать url на основе искаемого слова"""

    url = clean_url + word
    return url


def request_site(url):
    """Запрос к сайту"""

    response = requests.get(url)

    return response


def parsing_html(response):
    """Парсинг HTML разметки"""

    soup = bs(response.text, 'html.parser')
    items = soup.find_all("td", class_="ta-l")
    symbols_word = []
    for item in items:
        word = item.get_text(strip=True)
        for index, symbol in enumerate(item.get_text(strip=True)):
            if symbol == '[':
                symbols_word.append(word[:index])
    return symbols_word


def get_synonyms_word(word):
    """Основная функция обработчик"""
    clean_url = 'https://text.ru/synonym/'

    url = generate_url(clean_url, word)
    response = request_site(url)
    words = parsing_html(response)

    return words
