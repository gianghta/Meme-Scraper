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
        # Parse in the result URL and soup object for it
        self.siteURL = meme_url
        r = requests.get(self.siteURL, headers=HEADERS)
        self.soup = BeautifulSoup(r.text, 'html.parser')

        # Parse in the definition of the result meme
        def_tag = self.soup.find('h2', {'id': 'about'})
        self.definition = def_tag.next_element.next_element.next_element.text

        # Parse in the according image URL
        meme_header_tag = self.soup.find('header', class_='rel c')
        img_tag = meme_header_tag.find('a', class_='photo left')['href']
        self.imageURL = img_tag

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

if __name__ == "__main__":
    
    # Sample test for the scraper
    search_word = input('Enter search for meme: ')
    print(MemeSearcher(search_word).definition)