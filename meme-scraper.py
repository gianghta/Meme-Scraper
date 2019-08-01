#!/usr/bin/python
''' Python scraper that scrape the meme from
    Know Your Meme site
'''

import requests, re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')}

SEARCH_SIMILARITY_THRESHOLD = .4

def search_meme(text):
    try:
        re = requests.get(f'http://knowyourmeme.com/search?q={text}', headers=HEADERS)
        re.raise_for_status
    except Exception as e:
        print(f'Something wrong: {e}')
    soup = BeautifulSoup(re.text, 'html.parser')
    search_result = soup.find(class_='entry_list')
    if search_result:
        search_path = search_result.find('a', href=True)['href']
        print(search_path)
        print(search_path.replace('-', ' '), 'https://knowyourmeme.com{}'.format(search_path))
        return search_path.replace('-', ' '), 'https://knowyourmeme.com{}'.format(search_path)
    return None, None

def regexCompare(text):
    memeName, url = search_meme(text)
    print(memeName)
    memeRegex = re.compile(r'text')
    output = memeRegex.search(memeName)
    print(output.group())

# def search(text):
#     """Return a meme definition from a meme keywords.
#     """
#     meme_name, url = search_meme(text)
#     if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= SEARCH_SIMILARITY_THRESHOLD:
#         r = requests.get(url, headers=HEADERS)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         entry = soup.find('h2', {'id': 'about'})
#         return '%s. %s' % (meme_name.split('/')[-1].title(), entry.next.next.next.text)

if __name__ == "__main__":
    search = input('Enter search for meme: ')
    search_meme(search)
    regexCompare(search)