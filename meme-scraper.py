#!/usr/bin/python
"""
Python scraper that scrape the meme from
Know Your Meme site
"""

from collections import namedtuple
import requests
from bs4 import BeautifulSoup

Meme = namedtuple("Meme", ("definition", "image_url", "site_url"))


class MemeSearcher:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        )
    }

    ## PRIVATE ##

    def __get_soup_from_request(self, url):
        """Return a BeautifulSoup object from a GET response."""
        res = requests.get(url, headers=self.headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        return soup

    def __get_soup_from_request_by_keyword(self, search_keyword):
        url = f"http://knowyourmeme.com/search?q={search_keyword}"
        return self.__get_soup_from_request(url)

    def __get_meme_url_from_search_path(self, search_path):
        return "https://knowyourmeme.com{}".format(search_path)

    ## PUBLIC ##

    def search_by_keyword(self, search_keyword):
        """Return a <Meme> object found by searching with the given keyword."""
        soup = self.__get_soup_from_request_by_keyword(search_keyword)
        search_result = soup.find(class_="entry_list")

        if search_result:
            search_path = search_result.find("a", href=True)["href"]
            return self.search_by_url(self.__get_meme_url_from_search_path(search_path))

        raise Exception(f"Sorry but there were no results for {search_keyword}")

    def search_by_url(self, meme_url):
        """Return a <Meme> object found by searching with the given URL."""
        soup = self.__get_soup_from_request(meme_url)

        # Parse in the definition of the result meme
        def_tag = soup.find("h2", {"id": "about"})
        definition = def_tag.next_element.next_element.next_element.text

        # Parse in the according image URL
        img_tag = None
        try:
            meme_header_tag = soup.find("header", class_="rel c")
            img_tag = meme_header_tag.find("a", class_="photo left")["href"]
        except Exception:
            pass

        return Meme(definition=definition, site_url=meme_url, image_url=img_tag)


if __name__ == "__main__":

    # Sample test for the scraper
    # search_word = "sanic"
    search_word = "duwang"

    searcher = MemeSearcher()
    meme_found = searcher.search_by_keyword(search_word)

    print(meme_found)
