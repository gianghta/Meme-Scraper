#!/usr/bin/python
''' Python scraper that scrape the meme from
    Know Your Meme site
'''

import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')}

def searchMeme(text):
    try:
        re = requests.get(f'http://knowyourmeme.com/search?q={text}', headers=HEADERS)
        re.raise_for_status
    except Exception as e:
        print(f'Something wrong: {e}')
    soup = BeautifulSoup(re.text, 'html.parser')
    search_result = soup.find(class_='entry_list')
    if search_result:
        search_path = search_result.find('a', href=True)['href']
        print(f'https://knowyourmeme.com{search_path}')
        return search_path.replace('-', ' '), 'https://knowyourmeme.com{}'.format(search_path)
    return None, None

if __name__ == "__main__":
    search = input('Enter search for meme: ')
    searchMeme(search)