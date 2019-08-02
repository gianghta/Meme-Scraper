#!/usr/bin/python
''' Python scraper that scrape the meme from
    Know Your Meme site
'''

import requests, re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')}

class Meme:
    def __init__(self):
        self.definition = None
        self.imageURL = None
        self.siteURL = None
        self.soup = None
    
    def parse(self, meme_url):
        self.siteURL = meme_url
        r = requests.get(self.siteURL, headers=HEADERS)
        self.soup = BeautifulSoup(r.text, 'html.parser')

        def_tag = self.soup.find('h2', {'id': 'about'})
        print(def_tag)
        self.definition = def_tag.next_element.next_element.next_element.text

        img_tag = self.soup.find('header', class_='rel c')

class MemeSearcher(Meme):
    def __init__(self, search_keyword):
        super().__init__()
        self.search_keyword = search_keyword
        self.meme_result_url = None

        try:
            re = requests.get(f'http://knowyourmeme.com/search?q={search_keyword}', headers=HEADERS)
            re.raise_for_status
        except Exception as e:
            print(f'Something wrong: {e}')
        soup = BeautifulSoup(re.text, 'html.parser')
        search_result = soup.find(class_='entry_list')
        if search_result:
            search_path = search_result.find('a', href=True)['href']
        else:
            raise Exception(f'Sorry but there were no results for {search_keyword}')

        self.meme_result_url = 'https://knowyourmeme.com{}'.format(search_path)
        self.parse(self.meme_result_url)


# def meme_list(text):
#     try:
#         re = requests.get(f'http://knowyourmeme.com/search?q={text}', headers=HEADERS)
#         re.raise_for_status
#     except Exception as e:
#         print(f'Something wrong: {e}')
#     soup = BeautifulSoup(re.text, 'html.parser')
#     search_result = soup.find(class_='entry_list')
#     if search_result:
#         search_path = search_result.find('a', href=True)['href']
#         if search_path:
#             print(search_path.replace('-', ' '))
#             return search_path.replace('-', ' '), 'https://knowyourmeme.com{}'.format(search_path)
#         else:
#             raise Exception('Could not locate the content URL')
#     return None, None

# def search(text):
#     """Return a meme definition from a meme keywords.
#     """
#     meme_name, url = meme_list(text)
#     # if meme_name and SequenceMatcher(None, text, meme_name).ratio() >= 0.4:
#     r = requests.get(url, headers=HEADERS)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     entry = soup.find('h2', {'id': 'about'})
#     return '%s \n %s' % (meme_name.split('/')[-1].title(), entry.next.next.next.text)

if __name__ == "__main__":
    search_word = input('Enter search for meme: ')
    print(MemeSearcher(search_word).definition)